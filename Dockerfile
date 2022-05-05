FROM docker.io/library/ubuntu:22.04

# installer does not like being run from /
WORKDIR "/root"

ENV POWERPANEL_VERSION=481

ENV ENABLE_LOGGING=false

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
    # See https://www.ej-technologies.com/resources/install4j/help/doc/installers/options.html
    ./ppb-linux-x86_64.sh -q -varfile response.varfile && \
    rm ppb-linux-x86_64.sh && \
    rm response.varfile

# Ports: ???, http, https, ???, snmp, snmp
# See https://dl4jz3rbrsfum.cloudfront.net/documents/CyberPower_UM_PowerPanel-Business-481.pdf
EXPOSE 2003
EXPOSE 3052
EXPOSE 53568/tcp
EXPOSE 53566/udp
EXPOSE 161/udp
EXPOSE 162/udp

# Bug: container will hang on start unless VOLUME is commented out
# Info: There are many other folders under /usr/local/PPB that probably need to be on a VOLUME:
#   /usr/local/PPB/cert/              (your ssl cert if you enable https)
#   /usr/local/PPB/db_cloud/          (db if using cloud service)
#   /usr/local/PPB/db_local/          (db if not using cloud service)
#   /usr/local/PPB/etc/               (some test logs)
#   /usr/local/PPB/extcmd/            (*.sh files to run when events happen)
#   /usr/local/PPB/log/               (possibly only installation logs)
#   /usr/local/PPB/temp/              (current version info)
#   /usr/local/PPB/uploads/           (possibly used for importing profile settings)
#   /usr/local/PPB/web/work/local/    (the icons needed for the specific UPS attached)
#   /usr/local/PPB/web-server/local/WEB-INF/classes/static/assets/   (dynamic translations)
# Info: https://docs.docker.com/engine/reference/builder/#notes-about-specifying-volumes
#   "Changing the volume from within the Dockerfile: If any build steps change the data within
#   the volume after it has been declared, those changes will be discarded."
#       Therefore, files in /usr/local/PPB/db_local generated on service start might be lost
# Solution: The volume must be /usr/local/PPB, not /usr/local/PPB/db_local. That means it will
#   also contain ~275 MB of program files that don't need to be in a volume, but the
#   alternative would be setting up ~10 volumes, which is too many.
VOLUME ["/usr/local/PPB/"]

HEALTHCHECK CMD curl -vs --fail http://127.0.0.1:3052/ || exit 1

COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
