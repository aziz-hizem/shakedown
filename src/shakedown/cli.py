import argparse
from importlib.metadata import version

def main() -> int: 
    parser = argparse.ArgumentParser(
        prog="shakedown",
        description = "Test-deploy every pull request before it is merged.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"shakedown {version('shakedown')}",
    )

    parser.parse_args()
    parser.print_help()
    return 0