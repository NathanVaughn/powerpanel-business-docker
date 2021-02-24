import argparse
import getpass
import json
import os
import subprocess
import sys
import urllib.request

REGISTRIES = ["docker.io", "ghcr.io"]
VARIANTS = ["local", "remote"]
CONTAINER = "nathanvaughn/powerpanel-business"


def get_version():
    # read the Dockerfile
    with open("Dockerfile", "r") as fp:
        lines = fp.readlines()

    # parse the version from the env line
    for line in lines:
        if "POWERPANEL_VERSION=" in line:
            return line[line.index("=") + 1 :].strip()


def build(version):
    for variant in VARIANTS:
        # build the filename we're going to build
        filename = "Dockerfile.{}".format(variant)
        tagging_list = []

        for registry in REGISTRIES:
            # build the image name
            full_image = "{}/{}".format(registry, CONTAINER)
            # create the list of tags for each variant
            tagging_list.append("{}:{}-latest".format(full_image, variant))
            tagging_list.append("{}:{}-{}".format(full_image, variant, version))

        # join everything together into a big command with a --tag for each tag
        tagging_cmd = " ".join("--tag {}".format(tagging) for tagging in tagging_list)

        # build the big docker build command
        build_command = 'docker build -f {} . --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` --build-arg VCS_REF=`git rev-parse --short HEAD` {}'.format(
            filename, tagging_cmd
        )

        # build the image
        print(build_command)
        subprocess.run(build_command, shell=True, check=True)

        # # push all the tags
        for tagging in tagging_list:
            subprocess.run("docker push {}".format(tagging), shell=True)


def main():
    version = get_version()
    build(version)


if __name__ == "__main__":
    main()
