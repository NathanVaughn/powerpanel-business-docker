import subprocess

VARIANTS = ["local", "remote"]
IMAGES = [
    "docker.io/nathanvaughn/powerpanel-business",
    "ghcr.io/nathanvaughn/powerpanel-business",
    "cr.nthnv.me/powerpanel-business",
]


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
        filename = f"Dockerfile.{variant}"
        tagging_list = []

        for image in IMAGES:
            tagging_list.append(f"{image}:{variant}-latest")
            tagging_list.append(f"{image}:{variant}-{version}")

        # join everything together into a big command with a --tag for each tag
        tagging_cmd = " ".join("--tag {}".format(tagging) for tagging in tagging_list)

        # build the big docker build command
        build_command = f'docker build -f {filename} . --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` --build-arg VCS_REF=`git rev-parse --short HEAD` {tagging_cmd}'

        # build the image
        print(build_command)
        subprocess.run(build_command, shell=True, check=True)

        # # push all the tags
        for tagging in tagging_list:
            subprocess.run(f"docker push {tagging}", shell=True, check=True)


def main():
    version = get_version()
    build(version)


if __name__ == "__main__":
    main()
