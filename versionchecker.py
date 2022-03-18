import json

IMAGE_NAME = "powerpanel-business"
VARIANTS = ["local", "remote"]
IMAGES = [
    f"docker.io/nathanvaughn/{IMAGE_NAME}",
    f"ghcr.io/nathanvaughn/{IMAGE_NAME}",
    f"cr.nthnv.me/library/{IMAGE_NAME}",
]


def main():
    # extract version from Dockerfile
    with open("Dockerfile", "r") as fp:
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
            {"dockerfile": f"Dockerfile.{variant}", "images": ",".join(tagging_list)}
        )

    print(json.dumps(matrix_data))


if __name__ == "__main__":
    main()
