"""Writes a new AmberChest version into every place that names one.

The add-on is nothing but a pointer at a published image, so "updating" it
means changing that version - here, in both READMEs, in the issue template and
in the changelog. Used by the sync workflow, and by hand:

    python3 dev/bump.py 1.2.0 [--notes-url https://…]
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

CONFIG = Path("amberchest/config.yaml")
# Home Assistant reads the changelog from the add-on folder, not the root.
CHANGELOG = Path("amberchest/CHANGELOG.md")
BADGES = [Path("README.md"), Path("README.de.md")]
TEMPLATE = Path(".github/ISSUE_TEMPLATE/bug_report.yml")

VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def current_version() -> str:
    """Read the version the add-on points at right now."""
    match = re.search(r'^version:\s*"([^"]+)"', CONFIG.read_text(), re.MULTILINE)
    if not match:
        raise SystemExit("No version in amberchest/config.yaml")
    return match.group(1)


def bump(version: str, notes_url: str | None) -> None:
    """Replace the version everywhere and add a changelog entry."""
    old = current_version()

    CONFIG.write_text(
        re.sub(r'^version:\s*"[^"]+"', f'version: "{version}"', CONFIG.read_text(), count=1, flags=re.MULTILINE)
    )

    for path in BADGES:
        # The badge label differs by language, the version does not.
        path.write_text(re.sub(rf"(badge/[Vv]ersion-){re.escape(old)}", rf"\g<1>{version}", path.read_text()))

    TEMPLATE.write_text(TEMPLATE.read_text().replace(f'placeholder: "{old}"', f'placeholder: "{version}"'))

    link = notes_url or f"https://github.com/sphings79/amberchest/releases/tag/v{version}"
    entry = (
        f"## {version} - {date.today().isoformat()}\n\n"
        f"- Follows AmberChest {version}. See the\n"
        f"  [release notes]({link}) for what changed in the application.\n\n"
    )
    text = CHANGELOG.read_text()
    marker = "\n## "
    index = text.index(marker) + 1
    CHANGELOG.write_text(text[:index] + entry + text[index:])


def main() -> None:
    """Handle the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="The AmberChest version to follow, without the v")
    parser.add_argument("--notes-url", default=None, help="Link to the release notes")
    parser.add_argument("--check", action="store_true", help="Only print the current version")
    args = parser.parse_args()

    if args.check:
        print(current_version())
        return

    if not VERSION.match(args.version):
        raise SystemExit(f"Not a version: {args.version}")
    if args.version == current_version():
        print(f"Already at {args.version}")
        return

    bump(args.version, args.notes_url)
    print(f"Bumped {current_version()}")


if __name__ == "__main__":
    sys.exit(main())
