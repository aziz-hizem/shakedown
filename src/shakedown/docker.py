import subprocess


class DockerError(Exception):
    """Raised when a docker command fails."""


def image_size(image: str) -> int:
    """Return the size of a local docker image, in bytes."""
    result = subprocess.run(
        ["docker", "image", "inspect", image, "--format", "{{.Size}}"],
        capture_output=True,  # keeps stdout and stderr in result instead of printing to terminal
        text=True,  # give normal text instead of bytes
    )

    if result.returncode != 0:
        raise DockerError(result.stderr.strip())

    return int(result.stdout.strip())
