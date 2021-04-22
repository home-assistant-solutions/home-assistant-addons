import re

from wireguard_config import WireguardConfig


class WireguardParser():
  config: WireguardConfig

  def __enter__(self):
    with open('/etc/wireguard/wg0.conf', 'r') as file:
      self.config = WireguardParser.parse(file.read())
    return self.config

  def __exit__(self, *kw):
    with open('/etc/wireguard/wg0.conf', 'w') as file:
      file.write(WireguardParser.build(self.config))

  @staticmethod
  def parse(wireguard_config: str) -> WireguardConfig:
    config = WireguardConfig()
    try:
      config.endpoint = re.search('Endpoint = .*\n', wireguard_config)[0].split(' = ')[1].split(':')[0]
    except:
      config.endpoint = None

    try:
      config.allowed_ip = re.search('Address = .*\n', wireguard_config)[0].split(' = ')[1][:-1]
    except:
      config.allowed_ip = None

    try:
      config.private_key = re.search('PrivateKey = .*\n', wireguard_config)[0].split(' = ')[1][:-1]
    except:
      config.private_key = None

    try:
      config.public_key = re.search('PublicKey = .*\n', wireguard_config)[0].split(' = ')[1][:-1]
    except:
      config.public_key = None

    try:
      config.persistent_keppalive = re.search('PersistentKeepalive = .*\n', wireguard_config)[0].split(' = ')[1][:-1]
    except:
      config.persistent_keppalive = None

    return config

  @staticmethod
  def build(config: WireguardConfig) -> str:
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
      'AllowedIPs = 10.0.0.0/8\n' \
      'PersistentKeepalive = {}\n'.format(
        config.allowed_ip,
        config.private_key, 
        config.public_key, 
        config.endpoint,
        config.persistent_keppalive
      )

