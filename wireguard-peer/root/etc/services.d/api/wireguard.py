import subprocess

def touch_config():
  subprocess.run(['mkdir', '-p', '/etc/wireguard'])
  subprocess.run(['touch', '/etc/wireguard/wg0.conf'])

def up():
  subprocess.run(['wg-quick', 'up', 'wg0'])

def down():
  subprocess.run(['wg-quick', 'down', 'wg0'])

def restart():
  down()
  up()