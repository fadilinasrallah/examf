from __future__ import annotations

import argparse
from pathlib import Path
import sys


DEFAULT_OUTPUT = "repo-snapshot.txt"


def iter_files(root: Path, output_name: str):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        rel = path.relative_to(root)
        if ".git" in rel.parts:
            continue
        if rel.name == output_name:
            continue
        if rel.name == Path(__file__).name:
            continue

        yield rel, path


def build_snapshot(root: Path, output_name: str) -> str:
    lines: list[str] = [
        "# Repo Snapshot",
        "# Excludes: .git",
        "# Format: each file is listed with its relative path followed by its exact text contents.",
        "",
    ]

    for rel, path in iter_files(root, output_name):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Skipping non-UTF-8 file: {rel}", file=sys.stderr)
            continue

        lines.append(f"--- FILE: {rel.as_posix()} ---")
        lines.append(content.rstrip("\n"))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a plain-text snapshot of all text files in the repo."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output file name relative to the repo root (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    root = Path.cwd()
    output_path = root / args.output
    snapshot = build_snapshot(root, output_path.name)
    output_path.write_text(snapshot, encoding="utf-8")
    print(f"Wrote {output_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
