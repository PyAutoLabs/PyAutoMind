#!/usr/bin/env python3
"""Print every repo's rendered `.codex/hooks.json`, as one JSON object, for a Mind tree.

    python3 scripts/codex_hooks_render.py --mind <PyAutoMind tree>

The tree's own `scripts/repos_sync.py` and `repos.yaml` do the rendering, so the
same helper renders a pull request's base tree and its head alike. The firewall
gate compares the two to decide whether a PR changes what the Codex adapters
should say: if it does, every opted-in repo's installed `.codex/hooks.json` is
stale by construction until `session_hook_propagate.yml` runs after merge.
A repo whose `codex_hooks` the tree cannot render prints as its error, so a
broken manifest still reads as a change rather than hiding one.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path


def rendered(mind_root: Path) -> dict:
    sys.path.insert(0, str(mind_root / "scripts"))
    try:
        repos_sync = importlib.import_module("repos_sync")
    finally:
        sys.path.pop(0)
    _, repos = repos_sync.load_manifest(mind_root)
    out = {}
    for name, spec in sorted(repos.items()):
        if not repos_sync.codex_hook_names(spec):
            continue
        try:
            out[name] = repos_sync.render_codex_hooks(spec)
        except ValueError as error:
            out[name] = f"error: {error}"
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mind", type=Path, required=True)
    args = parser.parse_args(argv)
    print(json.dumps(rendered(args.mind.resolve()), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
