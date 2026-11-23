import argparse
import sys
from importlib.metadata import version

from shakedown.docker import DockerError, image_size


def format_size(size_bytes: int) -> str:
    return f"{size_bytes / 1_000_000:.1f} MB"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="shakedown",
        description="Test-deploy every pull request before it is merged.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"shakedown {version('shakedown')}",
    )

    subcommands = parser.add_subparsers(dest="command", required=False)

    size_parser = subcommands.add_parser("size", help="show the size of a Docker image")
    size_parser.add_argument("image", help="image name and tag")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        return 2

    if args.command == "size":
        try:
            size = image_size(args.image)
        except DockerError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"{args.image}: {format_size(size)}")
        return 0

    return 0
