import argparse
import sys
from importlib.metadata import version

from shakedown.docker import DockerError, build_image, image_size
from shakedown.git import GitError, archive


def format_size(size_bytes: int) -> str:
    return f"{size_bytes / 1_000_000:.1f} MB"


def run_compare(base: str, head: str, path: str) -> int:
    sizes = {}
    for name, ref in [("base", base), ("head", head)]:
        tag = f"shakedown-check:{name}"
        print(f"building {name} ({ref})...", file=sys.stderr)
        try:
            build_image(archive(ref, path), tag)
            sizes[name] = image_size(tag)
        except (GitError, DockerError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
    print(f"base ({base}): {format_size(sizes['base'])}")
    print(f"head ({head}): {format_size(sizes['head'])}")
    return 0


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

    # Size subcommand
    size_parser = subcommands.add_parser("size", help="show the size of a Docker image")
    size_parser.add_argument("image", help="image name and tag")

    # Compare subcommand
    compare_parser = subcommands.add_parser(
        "compare", help="build two version of an app and compare them"
    )
    compare_parser.add_argument(
        "--base", required=True, help="git ref to compare against, e.g, main"
    )
    compare_parser.add_argument(
        "--head", required=True, help="git ref to test, e.g a PR branch"
    )
    compare_parser.add_argument(
        "--path", default=".", help="folder with Dockerfile, relative to the repo root"
    )

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

    if args.command == "compare":
        return run_compare(args.base, args.head, args.path)

    return 0
