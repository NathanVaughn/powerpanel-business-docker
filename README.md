# Docker Image for [CyberPower PowerPanel Business](https://www.cyberpowersystems.com/products/software/power-panel-business/)

[![](https://img.shields.io/docker/v/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/image-size/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/pulls/nathanvaughnpowerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
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

### Volumes

The image mounts:

-   `/usr/local/ppbe/db_local/`

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

The image exposes port 3052 (HTP) and 53568 (HTTPS).

Example `docker-compose`:

```yml
ports:
  - 80:3052
  - 443:53568
```

## Tags

There are two versions available: `local` and `remote`.
See the [User Manual](https://dl4jz3rbrsfum.cloudfront.net/documents/CyberPower-UM-PPB-440.pdf)
for the difference between them.

### Specific Versions

Example:

```yml
image: nathanvaughn/powerpanel-business:local-440
```

### Latest

Example:

```yml
image: nathanvaughn/powerpanel-business:remote-latest
```