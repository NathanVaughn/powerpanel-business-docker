import json
import os

IMAGE_NAME = "powerpanel-business"
VARIANTS = ["local", "remote", "both"]
IMAGES = [
    f"docker.io/nathanvaughn/{IMAGE_NAME}",
    f"ghcr.io/nathanvaughn/{IMAGE_NAME}",
]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    # extract version from Dockerfile
    with open(os.path.join(ROOT_DIR, "docker", "Dockerfile"), "r") as fp:
        lines = fp.readlines()

    version = next(
        (
            line[line.index("=") + 1 :].strip()
            for line in lines
            if "POWERPANEL_VERSION=" in line
        ),
        None,
    )

    assert version is not None

    # build matrix data
    matrix_data = {"include": []}
    for variant in VARIANTS:
        tagging_list = []

        for image in IMAGES:
            tagging_list.extend(
                (f"{image}:{variant}-latest", f"{image}:{variant}-{version}")
            )

        matrix_data["include"].append(
            {"dockerfile": f"Dockerfile.{variant}", "tags": ",".join(tagging_list)}
        )

    # save output
    print(json.dumps(matrix_data, indent=4))

    if github_output := os.getenv("GITHUB_OUTPUT"):
        with open(github_output, "w") as fp:
            fp.write(f"matrix={json.dumps(matrix_data)}")


if __name__ == "__main__":
    main()
