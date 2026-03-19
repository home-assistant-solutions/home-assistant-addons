# Wireguard Peer

[![Release](https://img.shields.io/github/v/release/home-assistant-solutions/home-assistant-addons?filter=wireguard-peer*)](https://github.com/home-assistant-solutions/home-assistant-addons/releases)

A Home Assistant add-on that sets up a WireGuard VPN peer, connecting your Home Assistant instance to a WireGuard server. Supports remote control via the Odoo VPN addon.

## Installation

1. Navigate to **Settings → Add-ons → Add-on Store** in Home Assistant.
2. Click the menu icon (⋮) in the top right and select **Repositories**.
3. Add the following repository URL:
   ```
   https://github.com/home-assistant-solutions/home-assistant-addons
   ```
4. Find **Wireguard Peer** in the store and click **Install**.

## Configuration

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `private_key` | Yes | — | Your WireGuard private key |
| `ip` | Yes | — | The IP address assigned to this peer (e.g. `10.13.13.9`) |
| `endpoint` | No | `homeassistant-solutions.pl` | The WireGuard server hostname or IP |
| `public_key` | No | *(server default)* | The WireGuard server public key |

### Example configuration

```yaml
private_key: +LdVGd2ypFeVpIjF6nBrYIEge1XP0wDSZId9WRZgzUs=
ip: 10.13.13.9
endpoint: homeassistant-solutions.pl
public_key: lkVpFNKZ/WefGBARwtuEOkpI0DOF/7eObKGThtt0ZnE=
```

### Generating a key pair

You can generate a WireGuard key pair using the `wg` tool:

```bash
wg genkey | tee privatekey | wg pubkey > publickey
```

## How it works

On startup the add-on:
1. Reads your configuration from Home Assistant options.
2. Writes a WireGuard config file (`/etc/wireguard/wg0.conf`).
3. Brings up the `wg0` interface using `wg-quick`.

A `PersistentKeepalive` of 25 seconds is set automatically to keep the tunnel alive behind NAT.

## Supported architectures

- `amd64`
- `aarch64`
- `armv7`
- `armhf`
- `i386`

## Support

- [Issue tracker](https://github.com/home-assistant-solutions/home-assistant-addons/issues)
- [Changelog](CHANGELOG.md)
