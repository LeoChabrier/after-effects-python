"""
Generates docs/changelog.md from git tags at build time.
Falls back gracefully if git history is not available.
"""
import subprocess
from pathlib import Path


def on_pre_build(config):
    out = Path("docs/changelog.md")
    try:
        tags = subprocess.check_output(
            ["git", "tag", "--sort=-version:refname"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip().splitlines()
    except Exception:
        out.write_text("# Changelog\n\nNo release history yet.\n")
        return

    if not tags:
        out.write_text("# Changelog\n\nNo releases yet.\n")
        return

    lines = ["# Changelog\n"]
    for i, tag in enumerate(tags):
        try:
            date = subprocess.check_output(
                ["git", "log", "-1", "--format=%ad", "--date=short", tag],
                text=True,
            ).strip()
            prev = tags[i + 1] if i + 1 < len(tags) else ""
            log_range = f"{prev}..{tag}" if prev else tag
            commits = subprocess.check_output(
                ["git", "log", log_range, "--pretty=format:- %s"],
                text=True,
            ).strip()
        except Exception:
            date = ""
            commits = ""

        lines.append(f"## {tag}" + (f" — {date}" if date else "") + "\n")
        if commits:
            lines.append(commits + "\n")
        lines.append("")

    out.write_text("\n".join(lines))
