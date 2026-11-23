SIZE_WARNING_PERCENT = 20


def format_size(size_bytes: int) -> str:
    """Turn a number of bytes into readable text, e.g, 176.0MB or 1.61 GB."""
    if size_bytes >= 1_000_000_000:
        return f"{size_bytes / 1_000_000_000:.2f} GB"
    return f"{size_bytes / 1_000_000:.1f} MB"


def percent_change(old: int, new: int) -> float:
    """How much NEW differs from OLD, in percentage"""
    return (new - old) / old * 100


def size_report(base_ref: str, head_ref: str, base_size: int, head_size: int) -> str:
    """Markdown report comparing the image sizes of two versions."""
    change = percent_change(base_size, head_size)
    if change > SIZE_WARNING_PERCENT:
        mark = "⚠️"
        verdict = (
            f"⚠️ The image grew by more than {SIZE_WARNING_PERCENT}%. "
            "Not blocking, but check that it's intended."
        )
    else:
        mark = "✅"
        verdict = "✅ No regression found."

    lines = [
        "## Shakedown report",
        "",
        f"| | `{base_ref}` | `{head_ref}` | Change |",
        "|---|---|---|---|",
        f"| Image size on disk | {format_size(base_size)} | {format_size(head_size)} | {mark} {change:+.0f}% |",
        "",
        verdict,
    ]
    return "\n".join(lines)


def build_failure_report(head_ref: str) -> str:
    """Markdown report for a pull request whose image doesn't build."""
    lines = [
        "## Shakedown report",
        "",
        f"❌ `{head_ref}` does not build. Merging it would break the deployment.",
        "",
        "See the build log in the CI output for the exact error.",
    ]
    return "\n".join(lines)
