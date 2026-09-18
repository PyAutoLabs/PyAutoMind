#!/usr/bin/env python3
"""Generate only smoke bootstrap blocks; never replace a repository's runner.

The rollout flag gates writes/automatic delivery, not dry runs. Before rollout,
repos_sync reports the held adoption separately; --check here always checks the
actual installations. --require-all is for the propagation job, whose coverage
must not silently shrink after a failed clone.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

LABEL = "generated smoke bootstraps"
REL = Path(".github/scripts/run_smoke.py")
SOURCE = Path("policy/smoke_bootstrap.py")
BEGIN = "# pyauto:smoke-bootstrap:begin\n"
END = "# pyauto:smoke-bootstrap:end\n"
LEGACY = '''# CI puts PyAutoHands/autohands on PYTHONPATH (PyAutoHeart's reusable
# smoke-tests.yml clones it alongside the dependency chain); for local runs,
# fall back to the sibling checkout.
try:
    import build_util
except ImportError:  # pragma: no cover - local-run fallback
    sys.path.insert(0, str(WORKSPACE.parent / "PyAutoHands" / "autohands"))
    import build_util

AUTOHANDS = Path(build_util.__file__).resolve().parent
'''


def targets(repos):
    for name, spec in repos.items():
        flag = spec.get("smoke_bootstrap", False)
        if type(flag) is not bool:
            raise ValueError(f"{name}: smoke_bootstrap must be a boolean")
        if flag:
            if Path(name).name != name or name in (".", ".."):
                raise ValueError(f"unsafe repo name: {name}")
            yield name, spec


def rollout_enabled(mind):
    data = yaml.safe_load((mind / "repos.yaml").read_text())
    flag = data.get("smoke_bootstrap_rollout", False)
    if type(flag) is not bool:
        raise ValueError("smoke_bootstrap_rollout must be a boolean")
    return flag


def render(text, source):
    """Exact legacy migration, then bounded replacement. Exterior is immutable."""
    block = BEGIN + source.rstrip("\n") + "\n" + END
    if BEGIN in text or END in text:
        if text.count(BEGIN) != 1 or text.count(END) != 1:
            raise ValueError("expected exactly one bootstrap marker pair")
        start = text.index(BEGIN)
        stop = text.index(END)
        if stop < start:
            raise ValueError("reversed bootstrap markers")
        return text[:start] + block + text[stop + len(END):]
    if text.count(LEGACY) != 1:
        raise ValueError("unknown legacy bootstrap; refusing to guess")
    return text.replace(LEGACY, block, 1)


def installations(root, repos, require_all=False):
    """Identity lookup supports flat runners and one-level family layouts.

    No manifest.path rule: flat CI and task checkouts remain valid. Ambiguous
    identities fail rather than silently selecting a checkout to write.
    """
    root = root.absolute()
    for name, _ in targets(repos):
        candidates = [root / name] if (root / name).exists() else []
        for family in root.iterdir():
            if (family.is_dir() and not family.is_symlink()
                    and not (family / ".git").exists()
                    and not family.name.startswith(".")):
                candidate = family / name
                if candidate.exists():
                    candidates.append(candidate)
        if len(candidates) > 1:
            raise ValueError(f"{name}: ambiguous checkouts: {candidates}")
        if not candidates:
            if require_all:
                raise ValueError(f"{name}: checkout missing")
            continue
        yield name, candidates[0] / REL


def changes(root, repos, source, require_all=False):
    result = []
    for name, path in installations(root, repos, require_all):
        # Reject symlinks at every level, including the file and .github. Read
        # checks may inspect symlinked repos, but mutations must stay in-tree.
        if not path.is_file():
            raise ValueError(f"{name}: missing {REL}")
        text = path.read_bytes().decode("utf-8")
        try:
            expected = render(text, source)
        except ValueError as error:
            raise ValueError(f"{name}: {error}") from error
        if expected != text:
            result.append((path, expected))
    return result


def write(root, repos, source, *, require_all=False, dry_run=False):
    pending = changes(root, repos, source, require_all)
    # Preflight the entire set before the first write.
    for path, _ in pending:
        current = path
        while current != root.absolute():
            if current.is_symlink():
                raise ValueError(f"refusing to write through symlink: {current}")
            current = current.parent
    for path, expected in pending:
        if not dry_run:
            path.write_bytes(expected.encode("utf-8"))
        print(f"{'would write' if dry_run else 'wrote'}: {path}")
    return len(pending)


def check(root, repos, source):
    try:
        return [f"{path}: bootstrap differs from canonical source"
                for path, _ in changes(root, repos, source)]
    except (OSError, ValueError) as error:
        return [str(error)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--mind", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--require-all", action="store_true")
    parser.add_argument("--targets", action="store_true", help="JSON for propagation")
    args = parser.parse_args()
    repos = yaml.safe_load((args.mind / "repos.yaml").read_text())["repos"]
    selected = list(targets(repos))
    if args.targets:
        print(json.dumps({"enabled": rollout_enabled(args.mind), "targets": [
            {"name": name, "github": spec["github"]} for name, spec in selected]}))
        return 0
    if args.root is None:
        parser.error("--root is required (writes never infer a destination)")
    if not selected:
        parser.error("no smoke bootstrap targets selected")
    source = (args.mind / SOURCE).read_text()
    if args.write or args.dry_run:
        if args.write and not rollout_enabled(args.mind):
            parser.error("rollout is held; use --dry-run until coordination clears")
        write(args.root, repos, source, require_all=args.require_all,
              dry_run=args.dry_run)
    problems = check(args.root, repos, source)
    seen = list(installations(args.root, repos, args.require_all))
    print(f"check {LABEL}: {'OK' if not problems else str(len(problems)) + ' mismatch(es)'}")
    print(f"  coverage: {len(seen)} of {len(selected)} checked out")
    for problem in problems:
        print(f"  {problem}")
    return 0 if args.dry_run else int(bool(problems))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        sys.exit(f"smoke bootstrap: {error}")
