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

def run_app():
  logger.info('Starting wireguard addon')
  options_file = open('/data/options.json', 'r')
  options = json.load(options_file)
  options_file.close()

  if 'private_key' not in options or options['private_key'] == '':
    logger.error('Please provide your private key in configuration')
    return
  
  if 'ip' not in options or options['ip'] == '':
    logger.error('Please provide your IP in configuration')
    return

  wireguard.touch_config()

  with WireguardParser() as config:
    config.allowed_ip = options['ip']
    config.endpoint = options['endpoint']
    config.private_key = options['private_key']
    config.public_key = options['public_key']
    config.persistent_keppalive = 25

  wireguard.restart()

if __name__ == '__main__':
  run_app()
