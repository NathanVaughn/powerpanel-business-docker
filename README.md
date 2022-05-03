# Docker Image for [CyberPower PowerPanel Business](https://www.cyberpowersystems.com/products/software/power-panel-business/)

[![](https://img.shields.io/docker/v/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/image-size/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/docker/pulls/nathanvaughn/powerpanel-business)](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
[![](https://img.shields.io/github/license/nathanvaughn/powerpanel-business-docker)](https://github.com/NathanVaughn/powerpanel-business-docker)

This is a Docker image for [CyberPower PowerPanel Business](https://www.cyberpowersystems.com/products/software/power-panel-business/) served
over HTTP or HTTPS. It can be put behind a reverse proxy such as CloudFlare
or Traefik, or run standalone.

## Usage

### Quickstart

If you want to jump right in, take a look at the provided [docker-compose.yml](https://github.com/NathanVaughn/powerpanel-business-docker/blob/master/docker-compose.yml).

The default username and password is `admin` and `admin`.

### USB Devices

If you're using the `local` or `both` tag, the Docker image will need to be
able to access the UPS as a USB device. There are two ways to accomplish this:

**Option #1:** You could give the container access to the entire usb bus by sharing
`/dev/usb` (and possibly `/dev/bus/usb` on some distributions). To do this
in a `docker run` command, you would add `--device=/dev/usb:/dev/usb` (and
possibly `--device=/dev/bus/usb:/dev/bus/usb`) to your command. See
[docker-compose.yml](https://github.com/NathanVaughn/powerpanel-business-docker/blob/master/docker-compose.yml) for an example of how to do this in a compose file.

**Option #2:** You could share the specific device associated with the UPS,
but this has a problem: The device name may suddenly change its name for
any number of reasons. Some of them include:

- If the UPS is plugged into a different USB port.
- If another device is plugged into a USB port before it.
- If another device is plugged into a USB port *after* it.
- If the system is rebooted.
- If the linux kernel is updated.
- If certain software is updated.

Nonetheless, if you want to limit this container's access to other USB devices,
you can run the following commands in most modern Linux system shells:

```bash
$ ups_type="Cyber Power"
$ ups_dev_type="hiddev"
$ dev_bus_usb_name=$(lsusb | grep "$ups_type" | sed -E -e "s/^Bus ([[:digit:]][[:digit:]][[:digit:]]) Device ([[:digit:]][[:digit:]][[:digit:]]):.+$/\/dev\/bus\/usb\/\1\/\2/")
$ usb_product_name=$(sudo lsusb -D "$dev_bus_usb_name" 2>/dev/null | grep "iProduct" | sed -E -e "s/\s*iProduct\s*[0-9]*\s*//")
$ dev_usb_name=$(sudo dmesg | grep "$usb_product_name" | grep "$ups_dev_type" | tail -n 1 | sed -E -e "s/.*$ups_dev_type([0-9]+).*/\/dev\/usb\/$ups_dev_type\1/")
$ echo "$dev_usb_name"
```

Note that some UPSs may need a different `$ups_type` or `$ups_dev_type`.

For example, let's say `$dev_usb_name` is `/dev/usb/hiddev0`. You can
then add that to the appropriate part of your `docker run` command, 
as `--device="/dev/usb/hiddev0:/dev/usb/hiddev0"`, or, in your 
compose file, as in the following docker-compose fragment:

```yml
devices:
  - "/dev/usb/hiddev0:/dev/usb/hiddev0"
```

### Volumes

The image mounts a volume to `/usr/local/PPB/`, which contains all PPB programs and data.

See [docker-compose.yml](https://github.com/NathanVaughn/powerpanel-business-docker/blob/master/docker-compose.yml) for an example of how to mount this in a compose file.

### Network

The image exposes the following ports:
- 2003 (used by PowerPanel Watchdog process)
- 3052 (for HTTP access)
- 53566/udp (for unknown use)
- 53568/tcp (for HTTPS access)
- 161/udp (for SNMP)
- 162/udp (for SNMP)

If you don't enable SNMP or HTTPS, you may be able to get away
with exposing only the first three ports, but HTTPS is *highly*
recommended, and SNMP can be useful.

See [docker-compose.yml](https://github.com/NathanVaughn/powerpanel-business-docker/blob/master/docker-compose.yml) for an example of how to expose these ports.

## Tags

There are three versions of this image available: `local`, `remote`, 
and `both`. See the [User Manual](https://dl4jz3rbrsfum.cloudfront.net/documents/CyberPower_UM_PowerPanel-Business-481.pdf) for the difference between them, 
but in short:
- Install `local` if the UPS is directly connected to the computer
running this container. This is needed to run custom `*.sh`
files on UPS events, schedule shutdown/restarts, monitor power usage,
or configure the UPS itself.
- Install `remote` if this container is running on a computer which
needs to be *shut down or restarted* by UPS events on other computers
or network connected UPSs.
- Install `both` in a multi-UPS setup, where there are directly-connected
UPSs that need to be managed, but there is also a central UPS that is 
controlled elsewhere.

Example:
```yml
image: ghcr.io/nathanvaughn/powerpanel-business:local
```

### Specific Versions

Specific versions of PowerPanel can be accessed by appending a dash and a
three-digit version number to the image tag. For example,

```yml
image: ghcr.io/nathanvaughn/powerpanel-business:local-481
```

Note that as of `2022-05`, the only secure version is `481`. Previous
versions use insecure versions of [log4j](https://www.cve.org/CVERecord?id=CVE-2021-44228).

### Latest

Alternatively, you can access the latest version like so:

```yml
image: ghcr.io/nathanvaughn/powerpanel-business:remote-latest
```

## Registry

This image is available from 3 different registries. Choose whichever you want:

- [docker.io/nathanvaughn/powerpanel-business](https://hub.docker.com/r/nathanvaughn/powerpanel-business)
- [ghcr.io/nathanvaughn/powerpanel-business](https://github.com/users/nathanvaughn/packages/container/package/powerpanel-business)
- [cr.nthnv.me/library/powerpanel-business](https://cr.nthnv.me/harbor/projects/1/repositories/powerpanel-business) (experimental)

## Known Issues

- The volume contains all of the PowerPanel data, but *it also contains all 
of the executables* for the PowerPanel Business software (including a full 
Java runtime). This is an unfortunate result of how Cyber Power designed their
software and will make software updates, migrations, and back-ups much 
more difficult.

If you need to migrate to a new version of this container or PPB software,
you may need to manually save and restore your data. To assist with that,
here is a breakdown of the contents of `/usr/local/PPB/`:

| Directory Relative to /usr/local/PPB  | Directory Content         | Contains User Data?  |
| :-------------------------| :------------------------------------ | :------------------- |
| /db_cloud/                | your db if using the cloud service    | Yes                  |
| /db_local/                | your db if *not* using cloud service  | Yes                  |
| /extcmd/                  | \*.sh files to run when events happen | Yes                  |
| /jre/lib/security/cacerts | your SSL cert if you upload one       | Yes                  |
| /cert/                    | possibly your SSL security keys       | Probably             |
| /etc/                     | UPS test results                      | Probably             |
| /log/                     | PPB output logs                       | Probably Not         |
| /uploads/                 | Unknown                               | Probably Not         |
| /temp/                    | uploaded profile files                | Probably Not         |
| /.install4j/              | installation logs, programs, assets   | No                   |
| /bin/                     | PPB executable programs               | No                   |
| /fonts/                   | PPB fonts                             | No                   |
| /jre/                     | PPB's Java Runtime                    | No                   |
| /lib/                     | PPB program libraries                 | No                   |
| /licenses/                | PPB licenses                          | No                   |
| /web/work/                | assets for web interface              | No                   |
| /web-server/              | code/assets for web interface         | No                   |

Hopefully, future versions of PPB will have a better separation of programs and data.
