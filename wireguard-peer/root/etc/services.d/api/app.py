import json
import logging
import os
import subprocess
import time
from threading import Thread

import requests
from flask import Flask, request

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

def generate_config(ip, proxy_ip, private_key, public_key):
  config = get_config(ip, proxy_ip, private_key, public_key)
  config_file = open('/etc/wireguard/wg0.conf', 'w')
  config_file.write(config)
  config_file.close()

def run_app():
  logger.info('Starting wireguard addon')
  options_file = open('/data/options.json', 'r')
  options = json.load(options_file)
  options_file.close()

  if 'private_key' not in options or options['private_key'] == '':
    logger.error('Please provide your private_key in configuration')
    return
  
  if 'peer_id' not in options or options['peer_id'] == '':
    logger.error('Please provide your peer_id in configuration')
    return

  ip = get_ip(options['peer_id'])
  proxy_ip = get_proxy_ip(options['peer_id'])
  private_key = options['private_key']
  public_key = os.getenv('PUBLIC_KEY')
  logger.info('IP: {}, proxy IP: {}'.format(ip, proxy_ip))

  @app.route('/peer', methods=['PATCH'])
  def update_peer():
    new_ip = ip
    new_proxy_ip = proxy_ip
    if 'peer_ip' in request.json:
      logger.info('Peer IP changes: {}'.format(request.json['peer_ip']))
      new_ip = request.json['peer_ip']
    if 'proxy_ip' in request.json:
      new_proxy_ip = request.json['proxy_ip']

    generate_config(new_ip, new_proxy_ip, private_key, public_key)
    logger.info('New IP: {}, new proxy IP: {}'.format(new_ip, new_proxy_ip))

    def restart_wireguard():
      time.sleep(1)
      logger.info('Restarting wirequard interface')
      subprocess.run(['wg-quick', 'down', 'wg0'])
      subprocess.run(['wg-quick', 'up', 'wg0'])

    thread = Thread(target=restart_wireguard)
    thread.start()

    return '', 200

  generate_config(ip, proxy_ip, private_key, public_key)
  subprocess.run(['wg-quick', 'up', 'wg0'])
    
  app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
  run_app()
