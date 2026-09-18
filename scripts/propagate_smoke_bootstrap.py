#!/usr/bin/env python3
"""Isolated-clone propagation; a failed target never reads as already current."""
import argparse
from pathlib import Path
import subprocess
import tempfile

import yaml

import smoke_bootstrap_sync as sync


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def propagate(mind, tree, *, dry_run):
    repos = yaml.safe_load((mind / "repos.yaml").read_text())["repos"]
    selected = list(sync.targets(repos))
    if not selected:
        raise ValueError("no targets selected")
    if not dry_run and not sync.rollout_enabled(mind):
        raise ValueError("rollout held in repos.yaml; only dry runs are permitted")
    # Clone everything before generation. No credentials in remote URLs/logs.
    for name, spec in selected:
        slug = spec["github"]
        parts = slug.split("/")
        if len(parts) != 2 or any(not p or not all(c.isalnum() or c in "-_." for c in p)
                                  for p in parts):
            raise ValueError(f"invalid GitHub identity for {name}")
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        f"https://github.com/{slug}.git", str(tree / name)], check=True)
    source = (mind / sync.SOURCE).read_text()
    # A dry run still generates into disposable clones, so it can assert the
    # post-generation drift check and show precisely what would be committed.
    sync.write(tree, repos, source, require_all=True)
    problems = sync.check(tree, repos, source)
    if problems:
        raise ValueError("; ".join(problems))
    failed = []
    for name, _ in selected:
        repo = tree / name
        try:
            changed = git(repo, "diff", "--name-only").splitlines()
            if changed != [str(sync.REL)] and changed:
                raise ValueError(f"unexpected changed paths: {changed}")
            if not changed:
                print(f"{name}: already current", flush=True)
                continue
            print(git(repo, "diff", "--stat"), flush=True)
            if dry_run:
                print(f"{name}: would push", flush=True)
                continue
            git(repo, "config", "user.name", "github-actions[bot]")
            git(repo, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
            git(repo, "add", "--", str(sync.REL))
            git(repo, "commit", "-m", "ci: propagate canonical smoke bootstrap")
            git(repo, "push", "origin", "HEAD")
            print(f"{name}: pushed", flush=True)
        except (subprocess.CalledProcessError, ValueError) as error:
            # Commands have no secrets; don't print captured credential helpers.
            print(f"{name}: FAILED ({type(error).__name__})", flush=True)
            failed.append(name)
    if failed:
        raise ValueError("propagation failed: " + ", ".join(failed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    mind = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="smoke-bootstrap-") as directory:
        propagate(mind, Path(directory), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
