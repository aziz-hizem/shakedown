import argparse
import sys
from importlib.metadata import version

from shakedown.docker import DockerError, build_image, image_size
from shakedown.git import GitError, archive
from shakedown.report import build_failure_report, format_size, size_report


def run_compare(base: str, head: str, path: str) -> int:
    try:
        print(f"building base ({base})...", file=sys.stderr)
        build_image(archive(base, path), "shakedown-check:base")
        base_size = image_size("shakedown-check:base")
    except (GitError, DockerError) as error:
        print(f"error: could not build {base}: {error}", file=sys.stderr)
        return 1

    try:
        print(f"building head ({head})...", file=sys.stderr)
        build_image(archive(head, path), "shakedown-check:head")
        head_size = image_size("shakedown-check:head")
    except GitError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except DockerError:
        print(build_failure_report(head))
        return 1

    print(size_report(base, head, base_size, head_size))
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
        "compare", help="build two versions of an app and compare them"
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
