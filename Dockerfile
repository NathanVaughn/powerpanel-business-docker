FROM debian:bullseye-slim

# installer doesn't like being run from /
WORKDIR "/root"

ENV POWERPANEL_VERSION=481

# See https://www.ej-technologies.com/resources/install4j/help/doc/installers/responseFile.html
# for definition of response files
COPY --from=copier response.varfile response.varfile

# Package reasons:
#   curl: to download installer
#   ca-certificates: to make https work
#   *usb*: to connect to UPSs over USB
RUN apt-get update && \
    apt-get install -y \
        curl \
        ca-certificates \
        libgusb2 \
        libusb-0.1 \
        libusb-1.0-0 \
        usb.ids \
        usbutils \
        --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    curl -s -L 'https://dl4jz3rbrsfum.cloudfront.net/software/PPB_Linux%2064bit_v4.8.1.sh' -o ppb-linux-x86_64.sh && \
    chmod +x ppb-linux-x86_64.sh && \
    ./ppb-linux-x86_64.sh -q -varfile response.varfile
    # See https://www.ej-technologies.com/resources/install4j/help/doc/installers/options.html

# Ports: ???, http, https, ???, snmp, snmp
# See https://dl4jz3rbrsfum.cloudfront.net/documents/CyberPower_UM_PowerPanel-Business-481.pdf
EXPOSE 2003
EXPOSE 3052
EXPOSE 53568/tcp
EXPOSE 53566/udp
EXPOSE 161/udp
EXPOSE 162/udp
VOLUME ["/usr/local/PPB/db_local/"]

HEALTHCHECK CMD curl -vs --fail http://127.0.0.1:3052/ || exit 1

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
