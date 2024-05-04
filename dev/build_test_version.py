import argparse
import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(image_type: str) -> None:
    subprocess.run(
        [
            "docker",
            "build",
            "-f",
            f"Dockerfile.{image_type}",
            "-t",
            "powerpanel:test",
            ".",
        ],
        cwd=os.path.join(ROOT_DIR, "docker"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image-type", default="local", choices=["local", "remote", "both"]
    )
    args = parser.parse_args()

    main(args.image_type)
