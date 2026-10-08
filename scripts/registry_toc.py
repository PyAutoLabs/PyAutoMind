#!/usr/bin/env python3
"""Maintain a clickable contents block in the long registry files.

`planned.md`, `parked.md` and `condemned.md` hold one `## <slug>` section per
task; once they grow past a screen the reader has no way to see what is in the
file without scrolling. This script rewrites a generated block

    <!-- toc:start -->  ...  <!-- toc:end -->

near the top of each file, listing every `## ` heading as a GitHub-anchor
link. The block is generated, never hand-edited — `dashboard_refresh.yml`
self-heals it on pushes to main, the same contract as the dashboard pages.
Placement: an existing marker block is rewritten in place; a file without one
gets the block inserted just above its first `## ` heading, so preamble prose
stays on top. Files with fewer than MIN_SECTIONS sections carry no block (a
contents line above two entries is noise), and an existing block is removed
if the file shrinks below that.

`ideas.md` is deliberately out of scope: it is a flat bullet inbox with no
headings. `dashboard.md` has its own generated navigation.

Usage:
    python3 scripts/registry_toc.py --check   # exit 1 if any block is stale
    python3 scripts/registry_toc.py --write   # rewrite stale blocks in place
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ("planned.md", "parked.md", "condemned.md")
TOC_START = "<!-- toc:start -->"
TOC_END = "<!-- toc:end -->"
MIN_SECTIONS = 3


def _headings(lines: list[str]) -> list[str]:
    """Every `## ` heading outside fenced code blocks, in order."""
    out, fenced = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            out.append(line[3:].strip())
    return out


def _anchor(heading: str, seen: dict) -> str:
    """The GitHub auto-anchor for a heading (lowercase, spaces to hyphens,
    punctuation stripped, `-<n>` suffix on duplicates)."""
    slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
    n = seen.get(slug, 0)
    seen[slug] = n + 1
    return f"{slug}-{n}" if n else slug


def _toc_block(headings: list[str]) -> list[str]:
    seen: dict = {}
    lines = [TOC_START, "", "**Contents**", ""]
    lines += [f"- [{h}](#{_anchor(h, seen)})" for h in headings]
    lines += ["", TOC_END]
    return lines


def _strip_block(lines: list[str]) -> tuple[list[str], int | None]:
    """Remove an existing marker block; return (lines, insertion index)."""
    if TOC_START not in lines:
        return lines, None
    a = lines.index(TOC_START)
    b = lines.index(TOC_END)
    rest = lines[:a] + lines[b + 1 :]
    # swallow the blank line the block was padded with, if doubled
    if 0 < a < len(rest) and rest[a - 1] == "" and rest[a] == "":
        del rest[a]
    return rest, a


def render(text: str) -> str:
    lines = text.splitlines()
    body, at = _strip_block(lines)
    headings = _headings(body)
    if len(headings) < MIN_SECTIONS:
        out = body
    else:
        if at is None:
            # no prior block: insert just above the first `## ` heading
            at = next((i for i, l in enumerate(body) if l.startswith("## ")), 0)
        block = _toc_block(headings)
        pad_before = [""] if at > 0 and body[at - 1] != "" else []
        pad_after = [""] if at < len(body) and body[at] != "" else []
        out = body[:at] + pad_before + block + pad_after + body[at:]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check", action="store_true", help="exit 1 if any contents block is stale"
    )
    mode.add_argument(
        "--write", action="store_true", help="rewrite stale contents blocks in place"
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Mind repo root (default: this script's repo)",
    )
    args = ap.parse_args()

    stale = []
    for name in FILES:
        path = args.root / name
        if not path.exists():
            continue
        old = path.read_text()
        new = render(old)
        if new != old:
            stale.append(name)
            if args.write:
                path.write_text(new)

    if not stale:
        print("registry contents blocks: fresh")
        return 0
    if args.write:
        print(f"registry contents blocks: rewrote {', '.join(stale)}")
        return 0
    print(
        f"registry contents blocks: STALE — {', '.join(stale)} "
        "(run `python3 scripts/registry_toc.py --write`)"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
