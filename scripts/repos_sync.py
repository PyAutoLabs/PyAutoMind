#!/usr/bin/env python3
"""Sync + drift-check the organism's body map (PyAutoMind/repos.yaml).

repos.yaml is the single source of repo IDENTITY (GitHub home, category,
one-line role). This script keeps the generated doc blocks in step with it and
checks every other hand-maintained repo list against it.

Usage:
    python3 repos_sync.py [--check]      # drift checks only (default)
    python3 repos_sync.py --write        # regenerate doc blocks, then check
    python3 repos_sync.py --root <dir>   # override the workspace root

--write regenerates the blocks between `<!-- repos_sync:begin -->` /
`<!-- repos_sync:end -->` markers in:

  * <root>/AGENTS.md                       — the repo routing table
  * <root>/PyAutoBrain/skills/WORKFLOW.md  — the GitHub owner map

--check (always run) verifies, against the manifest:

  * PyAutoHeart/config/repos.yaml          — polled repos exist, owners match
  * PyAutoBuild/pre_build.sh               — run_workspace repos exist
  * admin_jammy/software/ensure_workspace_labels.sh — owner/name pairs match
  * the `origin` remote of every local checkout — manifest matches reality

Exit code 0 = no drift; 1 = drift found (each mismatch printed).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

MARK_BEGIN = "<!-- repos_sync:begin -->"
MARK_END = "<!-- repos_sync:end -->"


def load_manifest(mind_root):
    data = yaml.safe_load((mind_root / "repos.yaml").read_text())
    return data["categories"], data["repos"]


def owner_of(repo_spec):
    return repo_spec["github"].split("/")[0]


# --------------------------------------------------------------------------
# Generated blocks
# --------------------------------------------------------------------------

def routing_table(categories, repos):
    lines = [
        "| Repo | Role — go here when the task is about… |",
        "|------|----------------------------------------|",
    ]
    for cat, spec in categories.items():
        members = {n: r for n, r in repos.items() if r["category"] == cat}
        if not members:
            continue
        if spec and spec.get("collapse"):
            lines.append(f"| **{spec['label']}** | {spec['role']} |")
        else:
            for name, repo in members.items():
                lines.append(f"| **{name}** | {repo['role']} |")
    provenance = (
        "Generated from `PyAutoMind/repos.yaml` (the body map — the single "
        "source of repo identity). Edit that file, then run "
        "`python3 PyAutoMind/scripts/repos_sync.py --write`."
    )
    return "\n".join(lines) + "\n\n" + provenance


def owner_map(categories, repos):
    owners = {}
    for name, repo in repos.items():
        owners.setdefault(owner_of(repo), []).append(name)
    majority = max(owners, key=lambda o: len(owners[o]))
    exceptions = [
        f"`{repo['github']}`"
        for name, repo in repos.items()
        if owner_of(repo) != majority
    ]
    libraries = [n for n, r in repos.items() if r["category"] == "library"]
    ws_cats = ("workspace", "workspace_test", "howto", "pipeline")
    workspaces = [n for n, r in repos.items() if r["category"] in ws_cats]
    lines = [
        f"All repos live at `{majority}/<local dir name>` on GitHub, except: "
        + ", ".join(exceptions)
        + ".",
        "",
        "**Library repos:** " + ", ".join(libraries) + ".",
        "**Workspace repos:** " + ", ".join(workspaces) + ".",
        "",
        "Generated from `PyAutoMind/repos.yaml`; edit there, then run "
        "`python3 PyAutoMind/scripts/repos_sync.py --write`.",
    ]
    return "\n".join(lines)


def replace_block(path, content):
    text = path.read_text()
    if MARK_BEGIN not in text or MARK_END not in text:
        raise SystemExit(f"repos_sync: no marker block in {path}")
    pattern = re.compile(
        re.escape(MARK_BEGIN) + r".*?" + re.escape(MARK_END), re.DOTALL
    )
    new = pattern.sub(f"{MARK_BEGIN}\n{content}\n{MARK_END}", text, count=1)
    changed = new != text
    if changed:
        path.write_text(new)
    return changed


# --------------------------------------------------------------------------
# Drift checks
# --------------------------------------------------------------------------

def check_heart(root, repos):
    problems = []
    heart_yaml = root / "PyAutoHeart/config/repos.yaml"
    if not heart_yaml.exists():
        return [f"missing {heart_yaml} (skipped)"] if False else []
    data = yaml.safe_load(heart_yaml.read_text())
    for group, entries in data.get("repos", {}).items():
        for entry in entries:
            name, owner = entry["name"], entry["owner"]
            if name not in repos:
                problems.append(
                    f"Heart polls '{name}' ({group}) — not in the manifest"
                )
            elif owner != owner_of(repos[name]):
                problems.append(
                    f"Heart owner for '{name}' is '{owner}', manifest says "
                    f"'{owner_of(repos[name])}'"
                )
    return problems


def check_pre_build(root, repos):
    script = root / "PyAutoBuild/pre_build.sh"
    if not script.exists():
        return []
    names = re.findall(r'^run_workspace "([^"]+)"', script.read_text(), re.M)
    return [
        f"pre_build.sh runs '{n}' — not in the manifest"
        for n in names
        if n not in repos
    ]


def check_labels(root, repos):
    script = root / "admin_jammy/software/ensure_workspace_labels.sh"
    if not script.exists():
        return []
    block = re.search(r"REPOS=\((.*?)\)", script.read_text(), re.DOTALL)
    problems = []
    for slug in block.group(1).split():
        owner, _, name = slug.partition("/")
        if name not in repos:
            problems.append(
                f"ensure_workspace_labels targets '{slug}' — '{name}' not in the manifest"
            )
        elif slug != repos[name]["github"]:
            problems.append(
                f"ensure_workspace_labels targets '{slug}', manifest says "
                f"'{repos[name]['github']}'"
            )
    return problems


def normalize_remote(url):
    url = url.strip().removesuffix(".git")
    m = re.match(r"git@github\.com:(.+)", url)
    if m:
        return m.group(1)
    m = re.match(r"https://github\.com/(.+)", url)
    if m:
        return m.group(1)
    return url


def check_origins(root, repos):
    problems = []
    for name, repo in repos.items():
        checkout = root / name
        if not (checkout / ".git").exists():
            continue  # not checked out in this environment
        result = subprocess.run(
            ["git", "-C", str(checkout), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            problems.append(f"'{name}': cannot read origin remote")
            continue
        actual = normalize_remote(result.stdout)
        if actual != repo["github"]:
            problems.append(
                f"'{name}': origin is '{actual}', manifest says '{repo['github']}'"
            )
    return problems


# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()

    mind_root = Path(__file__).resolve().parents[1]
    root = args.root or mind_root.parent
    categories, repos = load_manifest(mind_root)

    if args.write:
        targets = {
            root / "AGENTS.md": routing_table(categories, repos),
            root / "PyAutoBrain/skills/WORKFLOW.md": owner_map(categories, repos),
        }
        for path, content in targets.items():
            changed = replace_block(path, content)
            print(f"{'updated' if changed else 'unchanged'}: {path}")

    checks = {
        "PyAutoHeart/config/repos.yaml": check_heart(root, repos),
        "PyAutoBuild/pre_build.sh": check_pre_build(root, repos),
        "ensure_workspace_labels.sh": check_labels(root, repos),
        "local checkout origins": check_origins(root, repos),
    }
    drift = False
    for label, problems in checks.items():
        status = "OK" if not problems else f"{len(problems)} mismatch(es)"
        print(f"check {label}: {status}")
        for p in problems:
            drift = True
            print(f"  ✗ {p}")
    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
