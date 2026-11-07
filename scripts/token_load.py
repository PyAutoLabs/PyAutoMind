#!/usr/bin/env python3
"""Measure the context paid by every PyAuto session and core dev procedures.

Approximate tokens are UTF-8 bytes / 4, rounded up. Report is read-only;
``check`` exits nonzero when a required file is missing or a budget is exceeded.
It also reports the three numbers `complete/2026/11/reduce-session-token-load.md` targets: the
four organs' AGENTS.md total, the core procedure lines, and the median
completion-record length of the newest month. The Cortex/Memory AGENTS and the
record median are report-only unless their budget flag is given, so Mind-only
CI (no sibling organs) still passes ``check``.
The root may be grouped or flat. Repository placement uses Mind's checkout helper (Brain's resolver when present).
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import sys

from repos_sync import repo_checkout

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
# Measured for the four-organ AGENTS total; absent checkouts are reported, not
# failed, because Mind-only CI and flat task bundles hold just Brain + Mind.
ORGAN_AGENTS = {
    "Cortex AGENTS": ("PyAutoCortex", "AGENTS.md"),
    "Memory AGENTS": ("PyAutoMemory", "AGENTS.md"),
}
FOUR_ORGANS = ("Brain AGENTS", "Mind AGENTS", "Cortex AGENTS", "Memory AGENTS")


def measure(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path), "missing": True}
    data = path.read_bytes()
    return {
        "path": str(path),
        "bytes": len(data),
        "lines": len(data.splitlines()),
        "tokens_approx": math.ceil(len(data) / 4),
    }


def record_median(mind: Path, month: str | None = None) -> dict | None:
    """Median line count of the completion records of one month
    (`complete/YYYY/MM/*.md`; default the newest month present)."""
    complete = mind / "complete"
    months = sorted(
        d for d in complete.glob("[0-9][0-9][0-9][0-9]/[0-9][0-9]") if d.is_dir()
    )
    if month:
        months = [d for d in months if d.relative_to(complete).as_posix() == month]
    if not months:
        return None
    records = sorted(months[-1].glob("*.md"))
    if not records:
        return None
    counts = sorted(len(r.read_bytes().splitlines()) for r in records)
    mid = len(counts) // 2
    median = counts[mid] if len(counts) % 2 else (counts[mid - 1] + counts[mid]) / 2
    return {
        "month": months[-1].relative_to(complete).as_posix(),
        "records": len(counts),
        "median_lines": median,
    }


def collect(root: Path, month: str | None = None) -> dict:
    paths = {}
    for name, (repo, relative) in (CORE | CONDITIONAL).items():
        base = root if repo is None else repo_checkout(root, repo)
        paths[name] = measure(base / relative)
    optional = {}
    for name, (repo, relative) in ORGAN_AGENTS.items():
        try:
            base = repo_checkout(root, repo)
        except (OSError, ValueError, RuntimeError):
            base = root / repo
        optional[name] = measure(base / relative)
    agents = ("workspace AGENTS", "Brain AGENTS", "Mind AGENTS")
    totals = {}
    if all("missing" not in paths[name] for name in agents):
        totals["agents_tokens_approx"] = sum(
            paths[name]["tokens_approx"] for name in agents
        )
    shared = ("context guide", "workflow guide")
    start = ("start_dev entry", "start_dev body", *shared)
    prm = ("prm entry", "prm body", *shared)
    for label, names in (
        ("start_dev_lines", start),
        ("prm_lines", prm),
        ("core_union_lines", tuple(dict.fromkeys((*start, *prm)))),
    ):
        if all("missing" not in paths[name] for name in names):
            totals[label] = sum(paths[name]["lines"] for name in names)
    organs = paths | optional
    if all("missing" not in organs[name] for name in FOUR_ORGANS):
        totals["organ_agents_tokens_approx"] = sum(
            organs[name]["tokens_approx"] for name in FOUR_ORGANS
        )
    records = record_median(repo_checkout(root, "PyAutoMind"), month)
    if records is not None:
        totals["completion_records"] = records
    return {"root": str(root), "files": paths, "organ_files": optional,
            "totals": totals}


def violations(result: dict, args: argparse.Namespace) -> list[str]:
    files = result["files"]
    errors = [
        f"missing: {name}: {row['path']}"
        for name, row in files.items()
        if "missing" in row
    ]
    total = result["totals"].get("agents_tokens_approx")
    if total is not None and total > args.agents_budget:
        errors.append(
            f"AGENTS total: {total} > {args.agents_budget} approximate tokens"
        )
    for name, budget in (
        ("start_dev_lines", args.start_dev_budget),
        ("prm_lines", args.prm_budget),
    ):
        lines = result["totals"].get(name)
        if lines is not None and lines > budget:
            errors.append(f"{name}: {lines} > {budget} lines")
    if args.organ_agents_budget is not None:
        organs = result["totals"].get("organ_agents_tokens_approx")
        if organs is None:
            errors.append("organ AGENTS total: unknown (an organ checkout is absent)")
        elif organs > args.organ_agents_budget:
            errors.append(
                f"organ AGENTS total: {organs} > {args.organ_agents_budget} "
                "approximate tokens"
            )
    if args.record_median_budget is not None:
        records = result["totals"].get("completion_records")
        if records is None:
            errors.append("completion-record median: unknown (no records)")
        elif records["median_lines"] > args.record_median_budget:
            errors.append(
                f"completion-record median ({records['month']}): "
                f"{records['median_lines']} > {args.record_median_budget} lines"
            )
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("report", "check"))
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(os.environ.get("PYAUTO_ROOT", ".")),
        help="workspace root (grouped main or flat bundle)",
    )
    parser.add_argument("--agents-budget", type=int, default=7500)
    parser.add_argument("--start-dev-budget", type=int, default=400)
    parser.add_argument("--prm-budget", type=int, default=450)
    parser.add_argument(
        "--organ-agents-budget", type=int, default=None,
        help="enforce the four-organ AGENTS.md total (target 6000; report-only "
             "when omitted)",
    )
    parser.add_argument(
        "--record-median-budget", type=float, default=None,
        help="enforce the median completion-record length (target 60; "
             "report-only when omitted)",
    )
    parser.add_argument("--month", help="completion-record month YYYY/MM "
                        "(default: newest)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = collect(args.root.resolve(), args.month)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"token load: {error}", file=sys.stderr)
        return 2
    issues = violations(result, args)
    result["violations"] = issues
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, row in (result["files"] | result["organ_files"]).items():
            if "missing" in row:
                print(f"{name}: MISSING {row['path']}")
            else:
                print(
                    f"{name}: {row['bytes']} bytes, {row['lines']} lines, "
                    f"~{row['tokens_approx']} tokens"
                )
        print(
            f"AGENTS total: ~{result['totals'].get('agents_tokens_approx', 'unknown')} tokens"
        )
        print(
            "organ AGENTS total (Brain+Mind+Cortex+Memory): "
            f"~{result['totals'].get('organ_agents_tokens_approx', 'unknown')} "
            "tokens (target <= 6000)"
        )
        for name in ("start_dev_lines", "prm_lines", "core_union_lines"):
            print(f"{name}: {result['totals'].get(name, 'unknown')} lines")
        records = result["totals"].get("completion_records")
        if records:
            print(
                f"completion-record median ({records['month']}, "
                f"{records['records']} records): {records['median_lines']} "
                "lines (target <= 60)"
            )
        else:
            print("completion-record median: unknown (no records)")
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
    return 1 if args.command == "check" and issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
