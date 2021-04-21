import json
import logging
import requests
import wireguard

from wireguard_parser import WireguardParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def get_proxy_ip(server, peer_id):
  url = '{}/proxy/ip?peer_id={}'.format(server, peer_id)
  logger.info('Requesting proxy ip for peer {}, url: {}'.format(peer_id, url))
  return requests.get(url).text

def get_ip(server, peer_id):
  url = '{}/peer/{}/ip'.format(server, peer_id)
  logger.info('Requesting ip for peer {}, url: {}'.format(peer_id, url))
  return requests.get(url).text

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

  wireguard.touch_config()

  with WireguardParser() as config:
    config.allowed_ip = get_ip(options['vpn_manager'], options['peer_id'])
    config.endpoint = get_proxy_ip(options['vpn_manager'], options['peer_id'])
    config.private_key = options['private_key']
    config.public_key = options['public_key']

  wireguard.restart()

if __name__ == '__main__':
  run_app()
