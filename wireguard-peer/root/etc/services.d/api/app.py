import json
import logging
import subprocess
import signal
import sys
import os

import requests
from flask import Flask

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def get_proxy_ip(peer_id):
  url = '{}/proxy/ip?peer_id={}'.format(os.getenv('VPN_MANAGER_URL'), peer_id)
  logger.info('Requesting proxy ip for peer {}, url: {}'.format(peer_id, url))
  return requests.get(url).text

def get_ip(peer_id):
  url = '{}/peer/{}/ip'.format(os.getenv('VPN_MANAGER_URL'), peer_id)
  logger.info('Requesting ip for peer {}, url: {}'.format(peer_id, url))
  return requests.get(url).text

def get_config(ip, proxy_ip, private_key, public_key):
  return \
    '[Interface]\n' \
    'Address = {}\n' \
    'PrivateKey = {}\n' \
    'ListenPort = 51820\n' \
    'DNS = 10.13.13.1\n' \
    '\n' \
    '[Peer]\n' \
    'PublicKey = {}\n' \
    'Endpoint = {}:51820\n' \
    'AllowedIPs = 0.0.0.0/0\n'.format(ip, private_key, public_key, proxy_ip)

options_file = open('/data/options.json', 'r')
options = json.load(options_file)
options_file.close()

ip = get_ip(options['peer_id'])
proxy_ip = get_proxy_ip(options['peer_id'])
private_key = options['private_key']
public_key = os.getenv('PUBLIC_KEY')
logger.info('IP: {}, proxy IP: {}'.format(ip, proxy_ip))

@app.route('/healthcheck')
def healthcheck():
  new_ip = get_ip(options['peer_id'])
  new_proxy_ip = get_proxy_ip(options['peer_id'])

  if new_ip != ip or new_proxy_ip != proxy_ip:
    generate_config(new_ip, new_proxy_ip, private_key, public_key)
    logger.info('New IP: {}, new proxy IP: {}'.format(ip, proxy_ip))

    subprocess.run(['wg-quick', 'down', 'wg0'])
    subprocess.run(['wg-quick', 'up', 'wg0'])

  return '', 200

def generate_config(ip, proxy_ip, private_key, public_key):
  config = get_config(ip, proxy_ip, private_key, public_key)
  config_file = open('/config/wg0.conf', 'w')
  config_file.write(config)
  config_file.close()

if __name__ == '__main__':
  generate_config(ip, proxy_ip, private_key, public_key)
  subprocess.run(['wg-quick', 'up', 'wg0'])
  app.run(debug=True, host='0.0.0.0')
