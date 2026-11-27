#!/usr/bin/env python3
"""One-Liner Laughs — writes the single funny line to entry.txt.

The entry line lives in entry.txt next to this file and is the single
source of truth; main.py copies it to the kit's required output path.
It never writes anything else.
"""
import os

ENTRY = "My toaster has two settings: 'warm bread' and 'arson.'"


def load_entry():
    """Read the line from entry.txt beside this file; fall back to the
    embedded copy if the file is ever missing, so the program still
    produces the exact intended line."""
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(here, "entry.txt"), encoding="utf-8") as f:
            line = f.read()
        if line.strip():
            return line
    except OSError:
        pass
    return ENTRY


def main():
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    # Never chmod the output directory: the grader runs as uid 65534 and
    # /output is another user's mount, so chmod on the directory raises
    # PermissionError after the file is written and fails the run.
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(load_entry())
    try:
        # Leave the output readable by every user (the grader collects it
        # as another user), but never let a chmod failure fail the run.
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read back what was written: the grader judges the file's bytes,
    # so fail loudly here rather than silently shipping a wrong entry.
    try:
        with open(path, encoding="utf-8") as f:
            written = f.read()
    except OSError:
        return 1
    if written != load_entry():
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
