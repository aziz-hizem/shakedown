import subprocess


class GitError(Exception):
    """Raised when a git command fails"""


def archive(ref: str, path: str) -> bytes:
    """Return the folder PATH, as it is in commit REF, packed as a tar archive."""
    result = subprocess.run(
        ["git", "archive", "--format=tar", f"{ref}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        raise GitError(result.stderr.decode().strip())
    return result.stdout
