#!/usr/bin/env python3
"""Measure the context paid by every PyAuto session and core dev procedures.

Approximate tokens are UTF-8 bytes / 4, rounded up. Report is read-only;
``check`` exits nonzero when a required file is missing or a budget is exceeded.
The root may be grouped or flat. Repository placement uses Brain's resolver.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

CORE = {
    "workspace AGENTS": (None, "AGENTS.md"),
    "Brain AGENTS": ("PyAutoBrain", "AGENTS.md"),
    "Mind AGENTS": ("PyAutoMind", "AGENTS.md"),
    "start_dev entry": ("PyAutoBrain", "skills/start_dev/SKILL.md"),
    "start_dev body": ("PyAutoBrain", "skills/start_dev/start_dev.md"),
    "prm entry": ("PyAutoBrain", "skills/prm/SKILL.md"),
    "prm body": ("PyAutoBrain", "skills/prm/prm.md"),
    "context guide": ("PyAutoBrain", "skills/CONTEXT.md"),
    "workflow guide": ("PyAutoBrain", "skills/WORKFLOW.md"),
}
CONDITIONAL = {
    "start_dev reference": ("PyAutoBrain", "skills/start_dev/reference.md"),
    "prm reference": ("PyAutoBrain", "skills/prm/reference.md"),
    "prm postmerge": ("PyAutoBrain", "skills/prm/closeout.md"),
    "prm MCP lane": ("PyAutoBrain", "skills/prm/mcp.md"),
    "prm freeze gate": ("PyAutoBrain", "skills/prm/freeze.md"),
    "GitHub reference": ("PyAutoBrain", "skills/GITHUB_ACCESS.md"),
    "Mind reference": ("PyAutoMind", "REFERENCE.md"),
}


def resolver():
    # This script lives in the Mind checkout. Brain is its sibling in both the
    # grouped main tree and flat bundles; use its canonical placement logic.
    module_path = Path(__file__).resolve().parents[2] / "PyAutoBrain/agents/_repo_paths.py"
    if not module_path.is_file():
        raise FileNotFoundError(f"Brain repository resolver missing: {module_path}")
    spec = importlib.util.spec_from_file_location("pyauto_repo_paths", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.repo_path


def measure(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path), "missing": True}
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data),
            "lines": len(data.splitlines()), "tokens_approx": math.ceil(len(data) / 4)}


def collect(root: Path) -> dict:
    locate = resolver()
    paths = {}
    for name, (repo, relative) in (CORE | CONDITIONAL).items():
        base = root if repo is None else locate(root, repo)
        paths[name] = measure(base / relative)
    agents = ("workspace AGENTS", "Brain AGENTS", "Mind AGENTS")
    totals = {}
    if all("missing" not in paths[name] for name in agents):
        totals["agents_tokens_approx"] = sum(paths[name]["tokens_approx"] for name in agents)
    shared = ("context guide", "workflow guide")
    start = ("start_dev entry", "start_dev body", *shared)
    prm = ("prm entry", "prm body", *shared)
    for label, names in (("start_dev_lines", start), ("prm_lines", prm),
                         ("core_union_lines", tuple(dict.fromkeys((*start, *prm))))):
        if all("missing" not in paths[name] for name in names):
            totals[label] = sum(paths[name]["lines"] for name in names)
    return {"root": str(root), "files": paths, "totals": totals}


def violations(result: dict, args: argparse.Namespace) -> list[str]:
    files = result["files"]
    errors = [f"missing: {name}: {row['path']}" for name, row in files.items()
              if "missing" in row]
    total = result["totals"].get("agents_tokens_approx")
    if total is not None and total > args.agents_budget:
        errors.append(f"AGENTS total: {total} > {args.agents_budget} approximate tokens")
    for name, budget in (("start_dev_lines", args.start_dev_budget),
                         ("prm_lines", args.prm_budget)):
        lines = result["totals"].get(name)
        if lines is not None and lines > budget:
            errors.append(f"{name}: {lines} > {budget} lines")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("report", "check"))
    parser.add_argument("--root", type=Path, default=Path(os.environ.get("PYAUTO_ROOT", ".")),
                        help="workspace root (grouped main or flat bundle)")
    parser.add_argument("--agents-budget", type=int, default=7500)
    parser.add_argument("--start-dev-budget", type=int, default=400)
    parser.add_argument("--prm-budget", type=int, default=450)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = collect(args.root.resolve())
    except (OSError, ValueError) as error:
        print(f"token load: {error}", file=sys.stderr)
        return 2
    issues = violations(result, args)
    result["violations"] = issues
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, row in result["files"].items():
            if "missing" in row:
                print(f"{name}: MISSING {row['path']}")
            else:
                print(f"{name}: {row['bytes']} bytes, {row['lines']} lines, "
                      f"~{row['tokens_approx']} tokens")
        print(f"AGENTS total: ~{result['totals'].get('agents_tokens_approx', 'unknown')} tokens")
        for name in ("start_dev_lines", "prm_lines", "core_union_lines"):
            print(f"{name}: {result['totals'].get(name, 'unknown')} lines")
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
    return 1 if args.command == "check" and issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
