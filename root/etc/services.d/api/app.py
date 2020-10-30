import json
import logging
import os
import signal
import sys

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
  return """
    [Interface]
    Address = {}
    PrivateKey = {}
    ListenPort = 51820
    DNS = 10.13.13.1

    [Peer]
    PublicKey = {}
    Endpoint = {}:51820
    AllowedIPs = 0.0.0.0/0
  """.format(ip, private_key, public_key, proxy_ip)

if __name__ == '__main__':
  with open('/data/options.json') as options_file:
    options = json.load(options_file)
    ip = get_ip(options['peer_id'])
    proxy_ip = get_proxy_ip(options['peer_id'])
    private_key = options['private_key']
    public_key = os.getenv('PUBLIC_KEY')

    logger.info('IP: {}, Proxy IP: {}, Private key: {}, Public key: {}'.format(ip, proxy_ip, private_key, public_key))
    
    config = get_config(ip, proxy_ip, private_key, public_key)
    config_file = open('/config/wg0.conf', 'w')
    config_file.write(config)
    config_file.close()

    os.system('wg-quick up wg0')

    @app.route('/healthcheck')
    def healthcheck():
      return 'Hey, we have Flask in a Docker container!'

  app.run(debug=True, host='0.0.0.0')
