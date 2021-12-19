# Docker Image for [CyberPower PowerPanel Business](https://www.cyberpowersystems.com/products/software/power-panel-business/)

[![](https://img.shields.io/docker/v/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/image-size/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/pulls/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/github/license/nathanvaughn/powerpanel-business-docker)](https://github.com/NathanVaughn/powerpanel-business-docker)

This is a Docker image for
[CyberPower PowerPanel Business](https://www.cyberpowersystems.com/products/software/power-panel-business/)
served over HTTP or HTTPS.
This can be put behind a reverse proxy such as CloudFlare or Traefik, or run standalone.

## Usage

### Quickstart

If you want to jump right in, take a look at the provided
[docker-compose.yml](https://github.com/NathanVaughn/powerpanel-business-docker/blob/master/docker-compose.yml).

The default username and password is `admin` and `admin`.

### USB Devices

If you're using the `local` version, the Docker image will need to be able
to access USB device of the UPS. There's two ways to accomplish this.
First, you can give the container access to the specific USB device.
Find the USB ID with `lsusb`:

```bash
nathan@zeus:[~]$ lsusb
Bus 002 Device 002: ID 8087:8001 Intel Corp.
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 8087:8009 Intel Corp.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 002: ID 0bda:2832 Realtek Semiconductor Corp. RTL2832U DVB-T
Bus 003 Device 006: ID 0764:0601 Cyber Power System, Inc. PR1500LCDRT2U UPS
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
nathan@zeus:[~]$
```

Then pass in the specific USB device:

```yml
devices:
  - /dev/bus/usb/003/006:/dev/bus/usb/003/006
```

However, the ID of the USB device is liable to change given a host reboot. Thus,
if security isn't as important, you can run the container in privileged mode:

```yml
privileged: true
```

This will automatically detect the correct USB device with no configuration.

### Volumes

The image mounts:

- `/usr/local/ppbe/db_local/`

Example `docker-compose`:

```yml
volumes:
  - app_data:/usr/local/ppbe/db_local/
---
volumes:
  app_data:
    driver: local
```

### Network

The image exposes port 3052 (HTTP), 53568 (HTTPS), and 162 (SNMP).

Example `docker-compose`:

```yml
ports:
  - 80:3052
  - 443:53568
```

## Tags

There are two versions available: `local` and `remote`.
See the [User Manual](https://dl4jz3rbrsfum.cloudfront.net/documents/CyberPower-UM-PPB-470.pdf)
for the difference between them.

### Specific Versions

Example:

```yml
image: ghcr.io/nathanvaughn/powerpanel-business:local-470
```

### Latest

Example:

```yml
image: ghcr.io/nathanvaughn/powerpanel-business:remote-latest
```

## Registry

This image is available from 3 different registries. Choose whichever you want:

- [docker.io/nathanvaughn/powerpanel-business](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
- [ghcr.io/nathanvaughn/powerpanel-business](https://github.com/users/nathanvaughn/packages/container/package/powerpanel-business)
- [cr.nthnv.me/powerpanel-business](https://cr.nthnv.me/repository/library/powerpanel-business) (experimental)

## Known Issues

- Versions 450+ appear to try to redirect to the HTTP port no matter what and don't work behind a reverse proxy (that I've figured out)
- Version 480 always returns a 404 (no known fix)
- This application does use Log4J, but I have personally not found any vulnerabilities for unauthenicated users (take this with a grain of salt)
