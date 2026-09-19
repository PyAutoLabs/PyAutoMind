#!/usr/bin/env python3
"""Sync + drift-check the organism's body map (PyAutoMind/repos.yaml).

repos.yaml is the single source of repo IDENTITY (GitHub home, category,
one-line role). This script keeps the generated doc blocks in step with it and
checks every other hand-maintained repo list against it.

Usage:
    python3 repos_sync.py [--check]      # drift checks only (default)
    python3 repos_sync.py --write        # regenerate docs/hooks, then check
    python3 repos_sync.py --write --only "generated Codex hooks"
                                         # bounded Codex-hook regeneration
    python3 repos_sync.py --root <dir>   # override the workspace root
                                         # (default: PyAutoBrain's shared
                                         # resolver — see workspace_root)
    python3 repos_sync.py --only <label> # run one check leg (repeatable) —
                                         # what an organ's PR CI gate calls
    python3 repos_sync.py --skip <label> # run every leg BUT this one
                                         # (repeatable; subtracts from --only)

`--only` narrows the run to the legs it names; `--skip` then subtracts from
whatever is selected, so `--only A --only B --skip B` runs A. An unregistered
label is an error for either flag — a typo can never silently disable a gate.
A leg is skipped only when its precondition cannot be met by the caller: the
`generated hooks` leg, for one, compares every checked-out repo's installed
copy against the canonical hook, and a PR that EDITS the canonical hook cannot
make the sibling copies match — only the post-merge propagation workflow can.

--write writes `<root>/.pyauto-root`, the workspace-root marker every consumer
resolves the root by (`PyAutoBrain/agents/_pyauto_root.py`): a generated
artifact of the body map rather than a file each machine places by hand.

--write regenerates the blocks between `<!-- repos_sync:begin -->` /
`<!-- repos_sync:end -->` markers in:

  * <root>/AGENTS.md                       — the repo routing table
  * <root>/PyAutoBrain/skills/WORKFLOW.md  — the GitHub owner map

and, between `<!-- repos_sync:map:begin -->` / `<!-- repos_sync:map:end -->`
markers, the compact **organism map** in each organ repo's own AGENTS.md
(<root>/<organ>/AGENTS.md). The map is the always-loaded orientation an agent
sees first: the peer organs, their roles, the call chain and the
conductor/faculty rule — so a session opened in one repo still knows the whole
organism. A repo opts in by adding the map markers to its AGENTS.md; organ
repos (or roots) that are absent, or lack the markers, are skipped rather than
failing the run.

--write also installs the two generated hooks into every checked-out repo,
both registered in `<repo>/.claude/settings.json`:

  * `policy/session_start_hook.sh` -> `.claude/hooks/session-start.sh`
    (SessionStart) — what makes a Claude Code web/mobile session run Python
    3.12 instead of the container's 3.11 default;
  * `policy/end_at_deliverable_hook.sh` -> `.claude/hooks/end-at-deliverable.sh`
    (PreToolUse, matching the timer-shaped tools) — the guard that enforces
    `policy/end_at_deliverable.md`: a session ends at its deliverable and never
    arms `send_later` / `subscribe_pr_activity` / `CronCreate` / `ScheduleWakeup`
    / `RemoteTrigger` create-update-run to wait for CI, a review or a merge.

The copies must be byte-identical to the canonical files, so `--check` fails on
any edit made to a copy.

`.claude/` and `CLAUDE.md` are the only top-level entries --write creates in a
target repo, and a repo may lint its own layout. Before writing either one,
--write reads that repo's own allowlist (see "Structure-lint agreement" below)
and skips a repo that has not allowlisted the entry, rather than breaking that
repo's CI with a path it rejects.

--check (always run) verifies, against the manifest:

  * PyAutoHeart/config/repos.yaml          — polled repos exist, owners match,
    smoke: and version_skew: name manifest repos and manifest package names
  * PyAutoHands/pre_build.sh               — run_workspace repos exist
  * PyAutoHands/autohands/config/workspaces.yaml — run_all repos, library
    names/packages and slow_skip_default repos exist
  * PyAutoBrain/bin/ensure_workspace_labels.sh — owner/name pairs match
  * the hygiene conductor — the repo sets it scans are derived from this
    manifest, and no repo name has been hardcoded back into an array
  * the `origin` remote of every local checkout — manifest matches reality
  * the workspace checkouts, BOTH ways — every manifest repo is checked out
    here, and every checkout here is a manifest repo (or is declared under
    `unmapped_checkouts:`). Every other leg skips an absent repo, which is
    right for that leg and wrong in aggregate: eleven checks reporting OK
    over a repo that is not there is reduced coverage reading as health. Held
    only against a root carrying the `.pyauto-root` marker — a CI matrix or a
    web session clones a handful of repos side by side, where "you are missing
    thirty" is noise, so there the leg prints its denominator and fails
    nothing.
  * the tenant firewall — no instance fact (satellite repo name, GitHub
    owner, workspace path) in Brain/Heart/Build *.py / *.sh outside the
    declared config surfaces (FIREWALL_ALLOWLIST below)
  * both generated hooks — present, executable, byte-identical to
    policy/session_start_hook.sh and policy/end_at_deliverable_hook.sh, and
    registered in .claude/settings.json (SessionStart / PreToolUse)
  * the end-at-deliverable policy block — unlike the other generated blocks
    this one is NOT opt-in-silent: an AGENTS.md without the markers is
    reported, because a repo missing this safety rule is the failure mode.
    --write inserts the markers itself under an existing history block
  * target-repo layout lints — every checked-out repo that lints its own
    top-level entries allowlists the `.claude/` and `CLAUDE.md` that --write
    installs (a repo that does not is skipped by --write and named here)

Exit code 0 = no drift; 1 = drift found (each mismatch printed).
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import smoke_bootstrap_sync as smoke_sync

import yaml


def _repo_resolver(root):
    root = Path(root)
    candidates = [p for p in (
        root / "PyAutoBrain/agents/_repo_paths.py",
        root / "organs/PyAutoBrain/agents/_repo_paths.py",
    ) if p.is_file()]
    if len({p.resolve() for p in candidates}) > 1:
        raise ValueError("PyAutoBrain: ambiguous flat and grouped checkouts")
    module_path = candidates[0] if candidates else None
    if module_path is not None:
        spec = importlib.util.spec_from_file_location("_pyauto_repo_paths", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


ORGANS = frozenset({"PyAutoBrain", "PyAutoMind", "PyAutoCortex",
                    "PyAutoMemory", "PyAutoHeart", "PyAutoHands",
                    "PyAutoNerves", "PyAutoGut", "PyAutoScientist"})


def bootstrap_checkout(root, name):
    """Find an organ before its manifest or the shared resolver is available."""
    root = Path(root)
    flat, grouped = root / name, root / "organs" / name
    if flat.exists() and grouped.exists() and flat.resolve() != grouped.resolve():
        raise RuntimeError(f"{name}: ambiguous flat and grouped checkouts")
    return grouped if grouped.exists() else flat


def repo_checkout(root, name):
    """Resolve a manifest identity, retaining standalone flat CI checkouts."""
    root = Path(root)
    resolver = _repo_resolver(root)
    if resolver is not None:
        return resolver.repo_path(root, name)
    flat = bootstrap_checkout(root, name) if name in ORGANS else root / name
    if flat.exists():
        return flat
    # A family directory containing checkouts needs the shared resolver. It
    # must not silently turn a grouped checkout into an absent flat one.
    for family in root.iterdir() if root.is_dir() else ():
        if family.is_dir() and not (family / ".git").exists() and (family / name).exists():
            raise RuntimeError(f"{name}: grouped checkout requires PyAutoBrain/agents/_repo_paths.py")
    return flat


def all_checkouts(root):
    """Checkouts at the root or one family level below it."""
    root = Path(root)
    resolver = _repo_resolver(root)
    if resolver is not None:
        return resolver.iter_checkouts(root)
    if not root.is_dir():
        return []
    checkouts = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if is_checkout(entry):
            checkouts.append(entry)
        elif not entry.is_symlink():
            checkouts.extend(child for child in entry.iterdir()
                             if child.is_dir() and is_checkout(child))
    return sorted(checkouts)

MARK_BEGIN = "<!-- repos_sync:begin -->"
MARK_END = "<!-- repos_sync:end -->"
MAP_BEGIN = "<!-- repos_sync:map:begin -->"
MAP_END = "<!-- repos_sync:map:end -->"
HISTORY_BEGIN = "<!-- repos_sync:history:begin -->"
HISTORY_END = "<!-- repos_sync:history:end -->"
REMOTE_BEGIN = "<!-- repos_sync:remote:begin -->"
REMOTE_END = "<!-- repos_sync:remote:end -->"
DELIVERABLE_BEGIN = "<!-- repos_sync:deliverable:begin -->"
DELIVERABLE_END = "<!-- repos_sync:deliverable:end -->"
ORGANS_BEGIN = "<!-- repos_sync:organs:begin -->"
ORGANS_END = "<!-- repos_sync:organs:end -->"

# The universal "never rewrite history" safety policy is single-sourced in a
# markdown file (so it can be edited without touching this generator) and
# generated (verbatim) into a repos_sync:history block in every repo's AGENTS.md
# that opts in. Unlike the organism map / command surface — which live once in
# PyAutoBrain because Brain is loaded in every session — this stays inline in
# every repo on purpose: it is a git-operation safety rule that also serves a
# cold agent (or human) reading a single repo directly on GitHub, which never
# loads the workspace root. Inline everywhere, but one source of truth + a
# drift check, so the copies can't drift. The text is deliberately terse — it
# rides in every repo's AGENTS.md, so every extra line is paid in context in
# every session; keep it to the prohibition + the clean-tree recovery command.
HISTORY_POLICY_FILE = "policy/never_rewrite_history.md"

# The SessionStart hook that makes Python 3.12 the default in Claude Code
# web/mobile session containers. Single-sourced here (one file, editable
# without touching this generator) and installed verbatim into every checked-out
# repo, because the harness reads it per repo — a session opened on any repo has
# to bring its own copy. Same shape as the history policy: one source, N
# generated copies, a drift check so they cannot diverge. A repo's own
# dependencies stay OUT of the hook (they would make the copies differ) and go
# in that repo's `.claude/session-python.txt`, which the hook reads at run time.
SESSION_HOOK_FILE = "policy/session_start_hook.sh"
SESSION_HOOK_REL = ".claude/hooks/session-start.sh"
SESSION_SETTINGS_REL = ".claude/settings.json"
SESSION_HOOK_COMMAND = "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
SESSION_HOOKS = "generated hooks (session-start + end-at-deliverable)"
CHECKOUTS = "workspace checkouts (manifest ↔ disk)"
CODEX_HOOKS_REL = ".codex/hooks.json"
CODEX_HOOKS = "generated Codex hooks"


# What a Claude Code web/mobile session must know before its first command:
# bootstrap unconditionally, run the suite in parallel, and reach GitHub through
# the MCP tools because there is no `gh`. Same shape as the history policy —
# one source file, N generated copies, a drift check — and inline everywhere for
# the same reason: a session may hold any subset of the organs, and the session
# that needs this most (several organs, so no hook fires) is the one where only
# repo content is guaranteed to be loaded.
#
# It was hand-written per repo until three passes in a row found a copy that had
# not learned what the previous pass measured, and one pass found two organs
# still shipping a bug a third had fixed. The per-repo halves were the argument
# against generating it, so they are gone: no test counts, no timings, no
# declared deps — those rot, and a rotting number in every repo's context is
# worse than none. A repo's own dependencies stay in its
# `.claude/session-python.txt`, which the hook reads at run time.
REMOTE_SESSIONS_FILE = "policy/remote_sessions.md"

# The universal "sessions end at their deliverable" rule: never arm anything
# that outlives the turn (send_later, subscribe_pr_activity, CronCreate,
# ScheduleWakeup, /loop, RemoteTrigger create/update/run) to wait for CI, a
# review or a merge. Same shape as the history policy — one source file, N
# generated copies, a drift check — and inline in every repo for the same
# reason: it binds any session in any repo, including a cold one reading a
# single repo on GitHub, and the sessions that broke it were remote ones where
# only repo content is guaranteed to be loaded.
#
# It is single-sourced rather than restated per skill because it was already
# written in one place (the batch skill) and still broken elsewhere twice: five
# batch members on 2026-08-31, then a mobile `/prm` on 2026-09-02/03. The prose
# rides beside the PreToolUse hook below, which enforces it — prose for the
# reasoning, the hook for the moment of temptation.
DELIVERABLE_POLICY_FILE = "policy/end_at_deliverable.md"

# The PreToolUse guard that makes the rule above unbypassable by reasoning.
# Installed and drift-checked exactly like the SessionStart hook (same
# one-source/N-copies contract), but registered under `hooks.PreToolUse` with a
# matcher naming the timer-shaped tools. It reads the PreToolUse JSON on stdin,
# lets read-only `RemoteTrigger` actions and PYAUTO_ALLOW_TIMERS=1 through, and
# exits 2 with the policy reason on everything else.
DELIVERABLE_HOOK_FILE = "policy/end_at_deliverable_hook.sh"
DELIVERABLE_HOOK_REL = ".claude/hooks/end-at-deliverable.sh"
DELIVERABLE_HOOK_COMMAND = "$CLAUDE_PROJECT_DIR/.claude/hooks/end-at-deliverable.sh"
DELIVERABLE_HOOK_MATCHER = (
    "^(send_later|subscribe_pr_activity|ScheduleWakeup|CronCreate|"
    "RemoteTrigger|mcp__.*(send_later|subscribe_pr_activity).*)$"
)

# Codex reads project hooks from `.codex/hooks.json`, after the user has
# reviewed and trusted the exact current hook hash.  Keep this an adapter over
# the existing, tested implementations: no second copy of any guard script.
# Every command resolves from the repository root because Codex runs hooks from
# the session cwd, which may be a subdirectory.
CODEX_HOOK_DEFINITIONS = {
    "end-at-deliverable": {
        "matcher": DELIVERABLE_HOOK_MATCHER,
        "command": (
            'bash "$(git rev-parse --show-toplevel)/'
            f'{DELIVERABLE_HOOK_REL}"'
        ),
        "statusMessage": "Enforcing the end-at-deliverable policy",
    },
    "mind-commit-guard": {
        "matcher": "Bash",
        "command": (
            'python3 "$(git rev-parse --show-toplevel)/'
            'bin/mind_commit_guard.py"'
        ),
        "statusMessage": "Checking shared PyAutoMind commit safety",
    },
    "pyauto-api-gate": {
        "matcher": "Bash",
        "command": (
            'python3 "$(git rev-parse --show-toplevel)/'
            '.claude/hooks/validate_pyauto_code.py"'
        ),
        "statusMessage": "Checking PyAuto API symbols",
    },
}


def load_history_policy(mind_root):
    return (mind_root / HISTORY_POLICY_FILE).read_text().rstrip("\n")


def load_remote_sessions(mind_root):
    return (mind_root / REMOTE_SESSIONS_FILE).read_text().rstrip("\n")


def load_deliverable_policy(mind_root):
    return (mind_root / DELIVERABLE_POLICY_FILE).read_text().rstrip("\n")


def load_session_hook(mind_root):
    return (mind_root / SESSION_HOOK_FILE).read_text()


def load_deliverable_hook(mind_root):
    return (mind_root / DELIVERABLE_HOOK_FILE).read_text()

# The canonical content-free CLAUDE.md pointer. Guidance is agent-agnostic and
# lives in AGENTS.md (read natively by Codex, Cursor, etc.); Claude Code loads
# CLAUDE.md, not AGENTS.md, so every repo that has an AGENTS.md keeps a CLAUDE.md
# whose only job is to `@`-import it (Anthropic's documented bridge — imported in
# full at launch, recursive to depth 4). Kept as a real, greppable file (not a
# symlink) so it can carry a Claude-only section later and avoids Windows symlink
# friction. This is the body already committed to Mind and Brain.
CLAUDE_MD_POINTER = """\
@AGENTS.md

<!-- Guidance is agent-agnostic and lives in AGENTS.md (read natively by Codex,
     Cursor, etc.). Claude Code loads CLAUDE.md, not AGENTS.md, so this file exists
     only to import that one source. Keep it a pointer — put content in AGENTS.md. -->
"""

# An `@AGENTS.md` import on its own line — the real bridge, not prose that merely
# mentions AGENTS.md (the dead-pointer failure mode that motivated this check).
CLAUDE_IMPORT_RE = re.compile(r"(?m)^@AGENTS\.md\s*$")


def load_manifest(mind_root):
    data = yaml.safe_load((mind_root / "repos.yaml").read_text())
    return data["categories"], data["repos"]


def load_unmapped_checkouts(mind_root):
    """Directory names at the workspace root that ARE git checkouts but are
    deliberately not body-map repos (`unmapped_checkouts:` in repos.yaml).

    The disk -> manifest half of `check_checkouts` has no other way to tell a
    deliberate neighbour (the org `.github` profile repo) from a checkout
    somebody forgot to declare. An absent key means none.
    """
    data = yaml.safe_load((mind_root / "repos.yaml").read_text())
    return list(data.get("unmapped_checkouts") or [])


# --------------------------------------------------------------------------
# Where the workspace root is
# --------------------------------------------------------------------------

# The marker a workspace root carries to say that it is one. Only a fallback:
# where the Brain checkout is beside us the name comes from the resolver that
# reads it (`_pyauto_root.ROOT_MARKER`), because two spellings of the filename
# would be two answers to the same question.
ROOT_MARKER_FALLBACK = ".pyauto-root"

# The marker's content, written by --write into whatever root it resolved. It
# is a generated artifact of the body map rather than a file each machine
# places by hand — the resolver needs it, this script is what knows where the
# root is, so this script is what writes it. Deliberately says nothing about
# THIS organism: scripts/ is copied verbatim into the public template.
ROOT_MARKER_TEXT = """\
# Workspace root marker.
#
# Its presence is what makes this directory the workspace root: the directory
# holding the organ and library checkouts. `PyAutoBrain/agents/_pyauto_root.py`
# and `PyAutoBrain/bin/_pyauto_root.sh` walk UP from a checkout and take the
# first ancestor holding this file, so the root stays right however the
# checkouts below are grouped into subdirectories.
#
# Intentionally unversioned: the workspace root is not a git repo, so this file
# belongs to no repository. It is a local, per-machine artifact — generated by
# `python3 PyAutoMind/scripts/repos_sync.py --write`, which writes it into the
# root it resolved, so a new workspace or worktree bundle gets one by running
# that command there rather than by hand.
"""

_RESOLVER = {}


def load_root_resolver(mind_root):
    """PyAutoBrain's shared root resolver, or None when Brain is not beside us.

    Imported rather than reimplemented: a second copy of the walk would be a
    second answer to "where is the root?", which is the defect the resolver
    exists to remove. Bootstrapping it needs a root of its own — the Brain
    checkout beside this one — and that is the same one-level assumption every
    consumer here used to make, kept for this single lookup: the resolver then
    walks up from its OWN location, so a workspace that grows subdirectories
    still resolves correctly from the marker.
    """
    if "module" not in _RESOLVER:
        root = mind_root.parent.parent if mind_root.parent.name == "organs" else mind_root.parent
        agents = bootstrap_checkout(root, "PyAutoBrain") / "agents"
        module = None
        if (agents / "_pyauto_root.py").is_file():
            if str(agents) not in sys.path:
                sys.path.insert(0, str(agents))
            try:
                import _pyauto_root as module
            except ImportError:  # pragma: no cover - a broken Brain checkout
                module = None
        _RESOLVER["module"] = module
    return _RESOLVER["module"]


def root_marker(mind_root):
    """The marker filename the resolver looks for."""
    resolver = load_root_resolver(mind_root)
    return getattr(resolver, "ROOT_MARKER", ROOT_MARKER_FALLBACK)


def workspace_root(mind_root):
    """The workspace root this Mind checkout belongs to — the `--root` default.

    The shared resolver where it is available (an explicit PYAUTO_ROOT, then a
    marked ancestor, then a parent holding a sibling organ); the Mind's parent
    otherwise, which is what this script assumed before the resolver existed
    and is still right for a side-by-side CI checkout with no Brain.

    One guard: the resolver anchors on the BRAIN checkout, so a worktree bundle
    whose PyAutoBrain is a symlink into the canonical workspace resolves to the
    CANONICAL root — and --write would then regenerate somebody else's tree
    from this Mind's manifest. When the resolved root does not hold this very
    checkout, take the parent instead. An explicit PYAUTO_ROOT is the
    operator's word and is never second-guessed.
    """
    resolver = load_root_resolver(mind_root)
    if resolver is None:
        return mind_root.parent.parent if mind_root.parent.name == "organs" else mind_root.parent
    root, _reason = resolver.workspace_root_reason()
    if os.environ.get("PYAUTO_ROOT"):
        return root
    if bootstrap_checkout(root, mind_root.name).resolve() != mind_root:
        return mind_root.parent.parent if mind_root.parent.name == "organs" else mind_root.parent
    return root


def write_root_marker(root, marker):
    """Generate the workspace-root marker — the file the resolver reads."""
    path = root / marker
    if path.exists() and path.read_text() == ROOT_MARKER_TEXT:
        print(f"unchanged: {path}")
    else:
        path.write_text(ROOT_MARKER_TEXT)
        print(f"wrote: {path}")


def owner_of(repo_spec):
    return repo_spec["github"].split("/")[0]


# --------------------------------------------------------------------------
# Generated blocks
# --------------------------------------------------------------------------

def routing_table(categories, repos):
    lines = [
        "| Repo | Canonical location | Role — go here when the task is about… |",
        "|------|--------------------|----------------------------------------|",
    ]
    for cat, spec in categories.items():
        members = {n: r for n, r in repos.items() if r["category"] == cat}
        if not members:
            continue
        if spec and spec.get("collapse"):
            locations = sorted({Path(repo.get('path', name)).parent.as_posix()
                                for name, repo in members.items()})
            label = ', '.join(f'`{location}/`' for location in locations)
            lines.append(f"| **{spec['label']}** | {label} | {spec['role']} |")
        else:
            for name, repo in members.items():
                location = repo.get('path', name)
                lines.append(f"| **{name}** | `{location}` | {repo['role']} |")
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


def system_map(categories, repos):
    """The compact organism orientation block for each organ repo's AGENTS.md.

    A pure function of the body map (`repos.yaml`, organ rows) plus the three
    stable invariants from `PyAutoBrain/ORGANISM.md` (call chain, the
    conductor/faculty split, the no-new-organs-by-default rule). This is the
    always-loaded map a session sees first — it exists so a session opened in a
    single repo still knows it is one *peer organ* among others, not a part of
    another.
    """
    organs = {n: r for n, r in repos.items() if r["category"] == "organ"}
    lines = [
        "**You are one organ of the PyAuto organism** — an agentic ecosystem for",
        "human-led, natural-language software development. The organs below are",
        "peer repositories; this repo is one of them, not a part of another.",
        "Canonical boundaries live in `PyAutoBrain/ORGANISM.md`; the full body map",
        "(every repo, not just organs) is `PyAutoMind/repos.yaml`.",
        "",
        "| Organ | Repo | Role |",
        "|-------|------|------|",
    ]
    for name, repo in organs.items():
        lines.append(f"| **{repo.get('organ', name)}** | {name} | {repo['role']} |")
    lines += [
        "",
        "Call chain (always this order): **Brain → Heart (gate) → Build "
        "(execute)**. Brain agents are **conductors** (front-door; a human "
        "drives them; they decide *and* act) or **faculties** (read-only "
        "opinions the conductors consult; they judge and stop). New capability "
        "grows as a faculty, not a new organ, unless it owns state or effects no "
        "existing organ can.",
        "",
        "Generated from `PyAutoMind/repos.yaml` + `PyAutoBrain/ORGANISM.md`; edit "
        "there, then run `python3 PyAutoMind/scripts/repos_sync.py --write`.",
    ]
    return "\n".join(lines)


def public_organs(repos):
    """The front-door organ set: every `category: organ` row (manifest order)
    plus any repo flagged `front_door: true` (e.g. Nerves/PyAutoNerves — a
    library that is part of the organism's public self-presentation without
    being a category:organ). This is a *superset* of the internal organism map
    (`system_map`, strict category:organ per PyAutoBrain/ORGANISM.md); the two
    are deliberately allowed to differ."""
    organs = [(n, r) for n, r in repos.items() if r["category"] == "organ"]
    front = [(n, r) for n, r in repos.items()
             if r.get("front_door") and r["category"] != "organ"]
    return organs + front


def organ_public_table(repos, *, bold):
    """The organ table for a public front-door README, a pure function of the
    body map. `bold` bold-links the repo cell (the `.github` org-profile style)
    vs a plain link (the PyAutoScientist README style). Role text is
    `public_role` (the curated public copy) falling back to the terse manifest
    `role`."""
    lines = ["| Organ | Repo | Role |", "|---|---|---|"]
    for name, repo in public_organs(repos):
        url = f"https://github.com/{repo['github']}"
        link = f"[**{name}**]({url})" if bold else f"[{name}]({url})"
        role = repo.get("public_role", repo["role"])
        lines.append(f"| {repo.get('organ', name)} | {link} | {role} |")
    return "\n".join(lines)


# The public front-door docs that must list every organ. The two READMEs carry
# a generated table between ORGANS markers; the hub blurb is prose, so it is
# presence-checked (every organ name must appear) rather than regenerated. All
# are soft-skipped when the sibling repo is not checked out.
PUBLIC_TABLE_TARGETS = [
    (".github/profile/README.md", True),
    ("PyAutoScientist/README.md", False),
]
HUB_BLURB = "pyautolabs.github.io/index.html"


def public_target(root, rel):
    if rel.startswith("PyAutoScientist/"):
        return bootstrap_checkout(root, "PyAutoScientist") / rel.split("/", 1)[1]
    return root / rel


def replace_block(path, content, begin=MARK_BEGIN, end=MARK_END):
    text = path.read_text()
    if begin not in text or end not in text:
        raise SystemExit(f"repos_sync: no marker block in {path}")
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
    new = pattern.sub(f"{begin}\n{content}\n{end}", text, count=1)
    changed = new != text
    if changed:
        path.write_text(new)
    return changed


def extract_block(text, begin, end):
    """Return the exact content --write would have placed between the markers,
    or None if the marker pair is absent or empty. The counterpart to
    replace_block, used by the drift check so a generated block that has been
    hand-edited or left stale (repos.yaml changed without a --write) is caught."""
    m = re.search(
        re.escape(begin) + r"\n(.*?)\n" + re.escape(end), text, re.DOTALL
    )
    return m.group(1) if m else None


def write_block(path, content, begin=MARK_BEGIN, end=MARK_END, *, required):
    """Fill a marked block, tolerant of partial checkouts.

    An absent file is always skipped (a partial/web checkout won't have every
    organ or the workspace-root AGENTS.md). A present file missing its markers
    is a hard error for `required` targets (the routing table / owner map,
    which must stay generated) but a soft skip for opt-in targets (an organ
    repo that has not yet added the map markers)."""
    if not path.exists():
        print(f"skipped (absent): {path}")
        return
    if begin not in path.read_text() or end not in path.read_text():
        if required:
            raise SystemExit(f"repos_sync: no marker block in {path}")
        print(f"skipped (no markers): {path}")
        return
    changed = replace_block(path, content, begin, end)
    print(f"{'updated' if changed else 'unchanged'}: {path}")


# --------------------------------------------------------------------------
# Drift checks
# --------------------------------------------------------------------------

def check_heart(root, repos):
    problems = []
    heart_yaml = bootstrap_checkout(root, "PyAutoHeart") / "config/repos.yaml"
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
    # The smoke: block (heart/smoke.py's workspace table, extracted 2026-08 —
    # PyAutoMind#198) names repos too, so its identity is checked the same way
    # version_skew's never was. Soft-skip when absent: a Heart checkout
    # predating the extraction is not drift (Heart's own strict loader fails
    # loudly if the block ever disappears after it).
    smoke = data.get("smoke") or {}
    for key, spec in (smoke.get("workspaces") or {}).items():
        if spec.get("directory") not in repos:
            problems.append(
                f"Heart smoke workspace '{key}' directory "
                f"'{spec.get('directory')}' — not in the manifest"
            )
        for lib in spec.get("chain", ()):
            if lib not in repos:
                problems.append(
                    f"Heart smoke workspace '{key}' chain entry '{lib}' — "
                    f"not in the manifest"
                )
    for name in smoke.get("import_names") or {}:
        if name not in repos:
            problems.append(
                f"Heart smoke import_names key '{name}' — not in the manifest"
            )
    # version_skew: <workspace repo> -> {library, package}. Heart compares the
    # library version a workspace pins against the library repo's own, so every
    # field here is identity the body map owns — and none of it was checked
    # until now, while the polled list beside it was checked from the start.
    # A workspace or library renamed in the map, or a package renamed on PyPI,
    # skewed Heart silently. Soft-skip when absent, like the smoke: block: a
    # Heart checkout predating it is not drift, and Heart's own loader is what
    # decides the block is required.
    for name, spec in (data.get("version_skew") or {}).items():
        spec = spec or {}
        if name not in repos:
            problems.append(
                f"Heart version_skew '{name}' — not in the manifest"
            )
        library = spec.get("library")
        if library not in repos:
            problems.append(
                f"Heart version_skew '{name}' library '{library}' — "
                f"not in the manifest"
            )
            continue
        expected = repos[library].get("package")
        if expected is None:
            problems.append(
                f"Heart version_skew '{name}' names library '{library}', "
                f"which has no 'package:' in the manifest"
            )
        elif spec.get("package") != expected:
            problems.append(
                f"Heart version_skew '{name}' package "
                f"'{spec.get('package')}', manifest says '{expected}'"
            )
    return problems


def check_hands_workspaces(root, repos):
    """The Build run matrix names repos too.

    `PyAutoHands/autohands/config/workspaces.yaml` says in its own header that
    repo identity must match the body map and that this check flags drift. It
    said so from the day it was extracted and no leg read it, so the claim was
    aspirational. Policy stays Hands' — the short keys, the report directories,
    the release matrix order are all its own; only the names are checked."""
    path = bootstrap_checkout(root, "PyAutoHands") / "autohands/config/workspaces.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    problems = []
    for key, spec in (data.get("run_all") or {}).items():
        repo = (spec or {}).get("repo")
        if repo not in repos:
            problems.append(
                f"Hands run_all '{key}' repo '{repo}' — not in the manifest"
            )
    for entry in data.get("libraries") or ():
        entry = entry or {}
        name = entry.get("name")
        if name not in repos:
            problems.append(
                f"Hands libraries entry '{name}' — not in the manifest"
            )
            continue
        expected = repos[name].get("package")
        if expected is None:
            problems.append(
                f"Hands libraries entry '{name}' has no 'package:' in the "
                f"manifest"
            )
        elif entry.get("package") != expected:
            problems.append(
                f"Hands libraries '{name}' package '{entry.get('package')}', "
                f"manifest says '{expected}'"
            )
    for name in data.get("slow_skip_default") or ():
        if name not in repos:
            problems.append(
                f"Hands slow_skip_default '{name}' — not in the manifest"
            )
    return problems


def check_pre_build(root, repos):
    script = bootstrap_checkout(root, "PyAutoHands") / "pre_build.sh"
    if not script.exists():
        return []
    names = re.findall(r'^run_workspace "([^"]+)"', script.read_text(), re.M)
    return [
        f"pre_build.sh runs '{n}' — not in the manifest"
        for n in names
        if n not in repos
    ]


HYGIENE_DIR = "PyAutoBrain/agents/conductors/hygiene"
HYGIENE_SCRIPT = f"{HYGIENE_DIR}/hygiene.sh"
HYGIENE_HELPER = f"{HYGIENE_DIR}/_hygiene_repos.py"

# The hygiene conductor scans repositories, so its repo sets must equal this
# manifest's. They used to be bash arrays, and they drifted: five libraries
# where the manifest declared six, four organs of seven. The drift was invisible
# because an unscanned repo yields no findings — the conductor reported clean and
# was believed. The tenant firewall could not catch it either; its allowlist
# PERMITTED the stale names rather than checking coverage.
#
# So this check has two legs, because either alone is escapable:
#
#   A. every reader the conductor might use returns exactly the sets declared
#      here. Note what this can and cannot prove: the conductor reads THIS file,
#      so a manifest edit moves both sides together and can never desynchronise
#      them — that is the whole point of deriving. What leg A really guards is
#      the READER, and specifically the PyYAML-free fallback, which is used only
#      where PyYAML is absent and would otherwise be verified nowhere. A
#      fallback parser that quietly drops a repo is precisely this bug's class,
#      so both readers are run and both must agree with the manifest.
#   B. no repo name is written back into a *_REPOS=(...) array literal — what
#      stops a future edit from "simplifying" the derivation away.
HYGIENE_ARRAY = re.compile(r"^[ \t]*[A-Za-z_]*REPOS=\(([^)]*)\)", re.M)
HYGIENE_CATEGORIES = ("library", "organ", "workspace")


def check_hygiene_coverage(root, repos, mind_root):
    helper, script = bootstrap_checkout(root, "PyAutoBrain") / HYGIENE_HELPER.removeprefix("PyAutoBrain/"), bootstrap_checkout(root, "PyAutoBrain") / HYGIENE_SCRIPT.removeprefix("PyAutoBrain/")
    if not helper.exists() or not script.exists():
        return []  # Brain not checked out in this environment

    problems = []
    for reader in ("auto", "minimal"):
        result = subprocess.run(
            [sys.executable, str(helper), "--json", "--parser", reader],
            capture_output=True,
            text=True,
            env={**os.environ, "PYAUTO_MIND": str(mind_root)},
        )
        if result.returncode != 0:
            problems.append(
                f"{HYGIENE_HELPER} ({reader} reader): cannot read the body map "
                f"(exit {result.returncode}) — the conductor would scan nothing: "
                f"{result.stderr.strip()}"
            )
            continue
        try:
            derived = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            problems.append(
                f"{HYGIENE_HELPER} ({reader} reader): output is not JSON — {exc}"
            )
            continue
        for category in HYGIENE_CATEGORIES:
            declared = {n for n, r in repos.items() if r["category"] == category}
            seen = set(derived.get(category, []))
            for name in sorted(declared - seen):
                problems.append(
                    f"hygiene ({reader} reader) does not scan '{name}' ({category}) "
                    f"— declared in the manifest but missing from the derived set"
                )
            for name in sorted(seen - declared):
                problems.append(
                    f"hygiene ({reader} reader) scans '{name}' ({category}) "
                    f"— not in the manifest"
                )

    for match in HYGIENE_ARRAY.finditer(script.read_text()):
        hardcoded = sorted(
            {tok.strip("\"'") for tok in match.group(1).split()} & set(repos)
        )
        if hardcoded:
            problems.append(
                f"{HYGIENE_SCRIPT}: repo name(s) hardcoded in an array — "
                f"{', '.join(hardcoded)}; derive them from the body map instead"
            )
    return problems


def check_labels(root, repos):
    script = bootstrap_checkout(root, "PyAutoBrain") / "bin/ensure_workspace_labels.sh"
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


# --------------------------------------------------------------------------
# Generated-block drift (the organism map is written into each organ)
# --------------------------------------------------------------------------
#
# The organism-map block is generated into any organ that opts in via the map
# markers. In practice that is PyAutoBrain, which is loaded in every session
# (web, mobile/code, local), so its auto-loaded AGENTS.md carries the map into
# every session's context — one copy, no per-organ duplication. Wherever a copy
# exists it must not drift from the manifest, so — mirroring how the command
# surface is checked by install.sh --check-agents-surface — this verifies each
# present map block still equals what system_map() generates. A block that was
# hand-edited, or left stale after a repos.yaml change without a --write, is
# reported as drift.


def check_map_blocks(root, repos, smap):
    problems = []
    for name, repo in repos.items():
        if repo["category"] != "organ":
            continue
        agents = repo_checkout(root, name) / "AGENTS.md"
        if not agents.exists():
            continue  # not checked out, or an organ without its own AGENTS.md
        text = agents.read_text()
        if MAP_BEGIN not in text or MAP_END not in text:
            continue  # opt-in: an organ that has not added the map markers
        if extract_block(text, MAP_BEGIN, MAP_END) != smap:
            problems.append(
                f"'{name}': organism-map block is stale — run "
                f"`python3 PyAutoMind/scripts/repos_sync.py --write`"
            )
    return problems


def check_history_blocks(root, repos, hpol):
    """Every AGENTS.md that opts into the repos_sync:history markers must carry
    the canonical policy verbatim. Single source (policy/never_rewrite_history.md)
    + this check is what lets the safety text live inline in every repo without
    drifting."""
    problems = []
    for name in repos:
        agents = repo_checkout(root, name) / "AGENTS.md"
        if not agents.exists():
            continue
        text = agents.read_text()
        if HISTORY_BEGIN not in text or HISTORY_END not in text:
            continue  # opt-in: repo hasn't added the history markers yet
        if extract_block(text, HISTORY_BEGIN, HISTORY_END) != hpol:
            problems.append(
                f"'{name}': never-rewrite-history block is stale — run "
                f"`python3 PyAutoMind/scripts/repos_sync.py --write`"
            )
    return problems


def check_remote_blocks(root, repos, remote):
    """Same contract as the history block: opt in with the markers, and the copy
    must then be the canonical text verbatim.

    Opt-in, not mandatory, so a repo that has not added the markers is skipped
    rather than failing a session (or a CI leg) that cannot see it. That is also
    the honest state of this rollout — see the module comment on
    REMOTE_SESSIONS_FILE."""
    problems = []
    for name in repos:
        agents = repo_checkout(root, name) / "AGENTS.md"
        if not agents.exists():
            continue
        text = agents.read_text()
        if REMOTE_BEGIN not in text or REMOTE_END not in text:
            continue  # opt-in: repo hasn't added the remote-session markers yet
        if extract_block(text, REMOTE_BEGIN, REMOTE_END) != remote:
            problems.append(
                f"'{name}': remote-session block is stale — run "
                f"`python3 PyAutoMind/scripts/repos_sync.py --write`"
            )
    return problems


def check_deliverable_blocks(root, repos, policy):
    """Same one-source contract as the history block, but NOT opt-in silence.

    The other blocks skip a repo that has not added their markers, because a
    repo can reasonably not carry them yet. This one is a safety rule that was
    already written down somewhere and still broken twice, so a repo missing it
    is the failure mode, not a pending nicety — a missing block is reported
    rather than skipped, and the report says which of the two states it is in:

    * the history markers are there and the deliverable markers are not —
      `--write` inserts the block itself, so the fix is to run it;
    * neither marker pair is present — the repo carries no generated policy at
      all, and a human has to place the markers before --write can fill them.
    """
    problems = []
    for name in repos:
        agents = repo_checkout(root, name) / "AGENTS.md"
        if not agents.exists():
            continue  # not checked out here
        text = agents.read_text()
        if DELIVERABLE_BEGIN in text and DELIVERABLE_END in text:
            if extract_block(text, DELIVERABLE_BEGIN, DELIVERABLE_END) != policy:
                problems.append(
                    f"'{name}': end-at-deliverable block is stale — run "
                    f"`python3 PyAutoMind/scripts/repos_sync.py --write`"
                )
        elif HISTORY_BEGIN in text and HISTORY_END in text:
            problems.append(
                f"'{name}': no deliverable block — run "
                f"`python3 PyAutoMind/scripts/repos_sync.py --write` "
                f"(it inserts one after the history block)"
            )
        else:
            problems.append(
                f"'{name}': no deliverable block — add the markers "
                f"({DELIVERABLE_BEGIN} / {DELIVERABLE_END}) to its AGENTS.md, "
                f"then run `python3 PyAutoMind/scripts/repos_sync.py --write`"
            )
    return problems


def insert_deliverable_markers(root, repos):
    """Place the deliverable markers under the history block where they are
    missing, so `--write` can fill them on the same run.

    Only a repo that already carries the history markers is touched: that pair
    proves the file has a generated-policy section and pins where the new block
    belongs. A repo with neither pair is left alone (there is no non-arbitrary
    place to put it) and named by `check_deliverable_blocks` instead."""
    for name in repos:
        agents = repo_checkout(root, name) / "AGENTS.md"
        if not agents.exists():
            continue
        text = agents.read_text()
        if DELIVERABLE_BEGIN in text or DELIVERABLE_END in text:
            continue
        if HISTORY_END not in text:
            continue  # no anchor — reported by the check, not guessed at here
        text = text.replace(
            HISTORY_END,
            f"{HISTORY_END}\n\n{DELIVERABLE_BEGIN}\n{DELIVERABLE_END}",
            1,
        )
        agents.write_text(text)
        print(f"inserted deliverable markers: {agents}")


# --------------------------------------------------------------------------
# CLAUDE.md → AGENTS.md pointer (repo hygiene)
# --------------------------------------------------------------------------
#
# Standard: guidance lives in the agnostic AGENTS.md; Claude Code reads
# CLAUDE.md, so every repo that HAS an AGENTS.md keeps a content-free CLAUDE.md
# that `@`-imports it. This is a pure function of "is this repo checked out and
# does it have an AGENTS.md?", so it lives here beside the other body-map drift
# checks. Repos with no AGENTS.md are reported (for a human) but not auto-stubbed
# — writing real per-repo guidance is its own work, out of scope here. Absent
# (not-checked-out) repos are skipped, exactly like the map-block generation, so
# this runs cleanly in a partial/web checkout.


def check_public_tables(root, repos):
    """Every front-door README's generated organ table must match the body map
    (so a new organ can never silently drop out of the public front door).
    Soft-skips a target that is not checked out."""
    problems = []
    for rel, bold in PUBLIC_TABLE_TARGETS:
        path = public_target(root, rel)
        if not path.exists():
            continue
        text = path.read_text()
        if ORGANS_BEGIN not in text or ORGANS_END not in text:
            problems.append(
                f"{rel}: no repos_sync:organs marker block "
                "(add the markers, then run --write)"
            )
        elif extract_block(text, ORGANS_BEGIN, ORGANS_END) != \
                organ_public_table(repos, bold=bold):
            problems.append(
                f"{rel}: organ table stale — run "
                "`python3 PyAutoMind/scripts/repos_sync.py --write`"
            )
    return problems


def check_hub_blurb(root, repos):
    """The hub's prose organism blurb is not regenerated (it is grammar, not a
    table), but every organ name must appear in it. Soft-skips when absent."""
    path = root / HUB_BLURB
    if not path.exists():
        return []
    text = path.read_text()
    return [
        f"{HUB_BLURB}: organ '{repo.get('organ', name)}' missing from the "
        "organism blurb"
        for name, repo in public_organs(repos)
        if repo.get("organ", name) not in text
    ]


def claude_md_is_pointer(text):
    """A CLAUDE.md counts as compliant iff it `@`-imports AGENTS.md on its own
    line (a real import that expands into context), not merely prose naming it."""
    return CLAUDE_IMPORT_RE.search(text) is not None


def check_claude_md_pointers(root, repos):
    problems = []
    for name in repos:
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            # Not checked out here, so there is nothing for THIS leg to
            # read. Absence itself is no longer silent — the "workspace
            # checkouts" leg owns it — so this narrows the leg, not the
            # coverage.
            continue
        if not (repo_dir / "AGENTS.md").exists():
            continue  # AGENTS-less repos are reported separately, not drift
        if structure_lint_forbids(repo_dir, "CLAUDE.md"):
            continue  # --write skips it; check_structure_lints reports it
        claude = repo_dir / "CLAUDE.md"
        if not claude.exists():
            problems.append(f"'{name}': has AGENTS.md but no CLAUDE.md pointer")
        elif not claude_md_is_pointer(claude.read_text()):
            problems.append(
                f"'{name}': CLAUDE.md does not @-import AGENTS.md (dead pointer)"
            )
    return problems


def repos_without_agents_md(root, repos):
    """Checked-out repos that have no AGENTS.md at all — the pointer is
    meaningless without a target, so these are reported for a human to write
    real guidance rather than auto-stubbed."""
    return [
        name
        for name in repos
        if repo_checkout(root, name).is_dir() and not (repo_checkout(root, name) / "AGENTS.md").exists()
    ]


def write_claude_md_pointers(root, repos):
    """Create the canonical pointer wherever a checked-out repo has an AGENTS.md
    but a missing or non-compliant CLAUDE.md. Idempotent: a repo already carrying
    the `@AGENTS.md` import is left untouched; a repo with no AGENTS.md is
    skipped (nothing to point at)."""
    for name in repos:
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            continue
        if not (repo_dir / "AGENTS.md").exists():
            print(f"skipped (no AGENTS.md): {repo_dir / 'CLAUDE.md'}")
            continue
        if structure_lint_forbids(repo_dir, "CLAUDE.md"):
            print(
                "SKIPPED (repo's layout lint disallows it): "
                f"{repo_dir / 'CLAUDE.md'}"
            )
            continue
        claude = repo_dir / "CLAUDE.md"
        if claude.exists() and claude_md_is_pointer(claude.read_text()):
            print(f"unchanged: {claude}")
            continue
        verb = "rewrote (dead pointer)" if claude.exists() else "created"
        claude.write_text(CLAUDE_MD_POINTER)
        print(f"{verb}: {claude}")


# --------------------------------------------------------------------------
# Structure-lint agreement
# --------------------------------------------------------------------------
#
# `--write` creates exactly two top-level entries in a target repo: the
# `.claude/` tooling folder and the `CLAUDE.md` pointer. A repo may lint its
# own layout — an allowlist of the top-level entries it accepts — and such a
# repo has no way to know this script is about to write into it. Installing
# `.claude/` into a repo whose lint has not allowlisted it breaks that repo's
# CI, and the breakage reads as the repo's fault rather than as this script's.
#
# So: before writing, ask the target's own lint whether it accepts what is
# about to be created. The lint stays the single authority — its allowlist is
# READ (never executed, never copied here), so a repo that adds `.claude` to
# its allowlist is covered again on the next run with no change on this side.
# Repos with no lint are the common case and are untouched by any of this.

# Where a repo is expected to keep its layout lint. A repo that keeps one
# somewhere else is not covered — a real, bounded gap: extend this tuple when a
# repo lints its layout from a different path. Detection is by convention
# because the alternative (a per-repo key in repos.yaml) would put POLICY in the
# body map, which is identity-only by contract.
STRUCTURE_LINT_CANDIDATES = ("scripts/validate_structure.py",)

# The top-level entries --write creates, each flagged with whether it is a
# directory — which picks the allowlist that governs it.
GENERATED_TOP_LEVEL = ((".claude", True), ("CLAUDE.md", False))

# The module-level names a layout lint uses for its two allowlists. Matched
# exactly: accepting near-miss spellings would turn "no allowlist found"
# (reported) into "wrong allowlist read" (silent).
ALLOWLIST_NAMES = {True: "ALLOWED_TOP_DIRS", False: "ALLOWED_TOP_FILES"}


def find_structure_lint(repo_dir):
    """The repo's own layout lint, or None if it keeps none."""
    for rel in STRUCTURE_LINT_CANDIDATES:
        path = repo_dir / rel
        if path.is_file():
            return path
    return None


def string_set_literal(node):
    """The strings in a set/list/tuple literal, or None if the node is not one
    — or holds anything but plain strings. A computed allowlist cannot be read
    without running the lint, and this never runs the lint."""
    if not isinstance(node, (ast.Set, ast.List, ast.Tuple)):
        return None
    names = set()
    for element in node.elts:
        if not isinstance(element, ast.Constant) or not isinstance(
            element.value, str
        ):
            return None
        names.add(element.value)
    return names


def structure_lint_allowlists(path):
    """Read `{is_dir: allowed names}` out of a layout lint without running it.

    A missing entry means that allowlist could not be read (absent, computed,
    or the file does not parse) — never that it is empty, and never that it is
    permissive. check_structure_lints reports the difference.
    """
    try:
        tree = ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return {}
    wanted = {name: is_dir for is_dir, name in ALLOWLIST_NAMES.items()}
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                names = string_set_literal(node.value)
                if names is not None:
                    found[wanted[target.id]] = names
    return found


def structure_lint_verdict(repo_dir):
    """`(lint_path, forbidden, unreadable)` for one checked-out repo.

    `forbidden` names the generated top-level entries this repo's lint would
    reject — the writers skip those. `unreadable` names allowlists that exist
    in principle but could not be read; those do NOT block the write, because
    "cannot tell" is not "forbids", and refusing on a guess would strand the
    common case. They are surfaced for a human instead.
    """
    lint = find_structure_lint(repo_dir)
    if lint is None:
        return None, [], []
    allowlists = structure_lint_allowlists(lint)
    forbidden, unreadable = [], []
    for entry, is_dir in GENERATED_TOP_LEVEL:
        allowed = allowlists.get(is_dir)
        if allowed is None:
            unreadable.append(ALLOWLIST_NAMES[is_dir])
        elif entry not in allowed:
            forbidden.append(entry)
    return lint, forbidden, sorted(set(unreadable))


def structure_lint_forbids(repo_dir, entry):
    """True when this repo's own layout lint would reject `entry`."""
    return entry in structure_lint_verdict(repo_dir)[1]


def check_structure_lints(root, repos):
    """Report repos whose own layout lint disagrees with what --write creates.

    Not drift in the generated-copy sense — nothing here has rotted. It is the
    coupling this script would otherwise break blind: the writers skip these
    repos, and this names them, so the skip gets resolved (extend the
    allowlist) rather than going unnoticed.
    """
    problems = []
    for name in repos:
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            continue  # not checked out in this environment
        lint, forbidden, unreadable = structure_lint_verdict(repo_dir)
        if lint is None:
            continue  # no layout lint: nothing to disagree with
        rel = lint.relative_to(repo_dir)
        for entry in forbidden:
            # Already on disk is the worse case, and the one that actually
            # happened: a --write from before this guard existed left the entry
            # behind, so the repo's own lint is failing right now. Skipping the
            # next write does not undo that — say so, rather than reporting it
            # as a write this run declined to make.
            if (repo_dir / entry).exists():
                problems.append(
                    f"'{name}': {rel} does not allow '{entry}', which is "
                    "already installed — that lint is failing now; allowlist "
                    f"'{entry}' or remove it from the repo"
                )
            else:
                problems.append(
                    f"'{name}': {rel} does not allow '{entry}' — --write skips "
                    f"the repo; add '{entry}' to that lint's allowlist"
                )
        for allowlist in unreadable:
            problems.append(
                f"'{name}': {rel} has no readable {allowlist} — cannot tell "
                "whether it accepts the generated .claude/ and CLAUDE.md"
            )
    return problems


# --------------------------------------------------------------------------
# Tenant firewall
# --------------------------------------------------------------------------
#
# The framework organs (Brain, Heart, Build) must stay adoptable as a
# config-diff fork: an adopter replaces only the declared config surfaces
# and pulls upstream cleanly. This check keeps instance facts — satellite
# repo names, GitHub owners, workspace paths — from leaking into organ code
# outside those surfaces. Skills prose (*.md) and AGENTS.md are out of scope
# by design (production prompts, never genericised).

FIREWALL_ORGANS = ("PyAutoBrain", "PyAutoHeart", "PyAutoHands")

# The declared config surfaces, frozen as a per-file token baseline (seeded
# 2026-07-10 from the live mains; the §1 inventory of the PyAutoScientist
# assessment names the load-bearing ones). Semantics: a NEW instance fact in
# a listed file, or ANY instance fact in an unlisted file, is drift. Phase-3
# config extraction shrinks this list; never grow it casually — a new entry
# means a new file an adopting fork must rewrite.
#
# 2026-08-26: seven entries dropped or narrowed. Each named the owner only
# because it hardcoded a workspace root under $HOME; they now delegate to
# bin/_pyauto_root.sh / agents/_pyauto_root.py, which name no absolute path
# at all. The two resolvers carry no entry here, and must not need one.
FIREWALL_ALLOWLIST = {
    "PyAutoBrain/agents/conductors/bug/_bug.py": {"PyAutoArray"},
    "PyAutoBrain/agents/conductors/bug/bug.sh": {"PyAutoLabs"},
    "PyAutoBrain/agents/conductors/health/health.sh": {"PyAutoNerves"},
    "PyAutoBrain/agents/conductors/hygiene/_hygiene_config.py": {"PyAutoArray", "PyAutoCTI", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBrain/agents/conductors/hygiene/_hygiene_optdeps.py": {"HowToFit", "HowToGalaxy", "HowToLens", "autocti_workspace", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBrain/agents/conductors/hygiene/_hygiene_refs.py": {"PyAutoArray", "PyAutoCTI", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace"},
    # hygiene.sh and _hygiene_repos.py carry NO entry on purpose: the conductor
    # now derives its repo sets from the body map, so it names no instance fact
    # at all. Re-adding an entry here would re-permit the drift that
    # check_hygiene_coverage exists to catch.
    "PyAutoBrain/agents/conductors/clone/_clone.py": {"HowToFit", "PyAutoFit", "PyAutoLens", "autofit_assistant", "autofit_workspace", "autolens_assistant"},
    "PyAutoBrain/agents/conductors/clone/clone.sh": {"HowToFit", "PyAutoFit", "autofit_workspace", "autolens_assistant"},
    "PyAutoBrain/agents/conductors/community/_community.py": {"Jammy2211", "PyAutoLabs"},
    # autofit_workspace: the `_upstream_noise` docstring cites measured noise
    # counts ("autofit_workspace in 26 files") as the evidence for rejecting a
    # file-spread threshold — the names ARE the finding; the code itself
    # derives its repo sets from the body map.
    "PyAutoBrain/agents/conductors/intake/_intake.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autofit_workspace", "autolens_workspace"},
    "PyAutoBrain/agents/conductors/profiling/_profiling.py": {"autolens_profiling"},
    "PyAutoBrain/agents/conductors/profiling/profiling.sh": {"autolens_profiling"},
    "PyAutoBrain/agents/conductors/release/nightly.sh": {"PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/conductors/release/rehearse.sh": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/conductors/release/validate.sh": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/conductors/workspace/_workspace.py": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoReduce", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace", "autoreduce_workspace"},
    "PyAutoBrain/agents/faculties/memory/_memory.py": {"autolens_assistant"},
    "PyAutoBrain/agents/faculties/memory/memory.sh": {"autolens_assistant"},
    # The two autolens tokens are the findings maturation lane's experiment and
    # mature tiers — surfaces, not new files, so the entries grow rather than
    # the list.
    "PyAutoBrain/agents/faculties/samplers/_samplers.py": {"PyAutoFit", "autofit_workspace_developer", "autofit_workspace_test", "autolens_inference", "autolens_profiling", "autolens_workspace_developer"},
    "PyAutoBrain/agents/faculties/samplers/samplers.sh": {"PyAutoFit", "autofit_workspace_developer", "autofit_workspace_test", "autolens_inference", "autolens_profiling", "autolens_workspace_developer"},
    "PyAutoBrain/agents/faculties/sizing/_sizing.py": {"PyAutoFit"},
    "PyAutoBrain/docs/conf.py": {"PyAutoScientist"},
    "PyAutoBrain/bin/check_skill_line_counts.sh": {"admin_jammy", "autolens_profiling"},
    "PyAutoBrain/bin/clean_slate.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autocti_workspace", "autofit_workspace", "autogalaxy_workspace", "autolens_inference", "autolens_profiling", "autolens_workspace"},
    "PyAutoBrain/bin/ensure_workspace_labels.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "Jammy2211", "PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "PyAutoCTI", "autocti_workspace", "autocti_workspace_test", "autofit_workspace", "autofit_workspace_test", "autogalaxy_workspace", "autogalaxy_workspace_test", "autolens_workspace", "autolens_workspace_test", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoBrain/bin/install.sh": {"PyAutoFit", "PyAutoLabs", "admin_jammy", "autolens_profiling"},
    "PyAutoBrain/bin/overnight_status.sh": {"PyAutoLabs", "autolens_assistant"},
    "PyAutoBrain/bin/pull_all_main.sh": {"PyAutoLabs"},
    "PyAutoBrain/bin/version_drift.sh": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBrain/bin/worktree.sh": {"PyAutoArray", "PyAutoCTI", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "admin_jammy", "autolens_workspace"},
    "PyAutoBrain/tests/test_activity_gate.py": {"HowToFit", "HowToLens", "PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoBrain/tests/test_clean_slate.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "autolens_workspace", "euclid_assistant"},
    "PyAutoBrain/tests/test_clone_conductor.py": {"autofit_assistant", "autolens_assistant"},
    # Load-bearing real names: the sync fixture exercises the LIVE reference
    # profile (keyed `autolens_assistant`) and the library-name resolution that
    # maps a sibling to its own library dir, so synthetic names would test
    # neither. The fixture is a temp dir; nothing here reaches a real checkout.
    "PyAutoBrain/tests/test_clone_sync.py": {"PyAutoCTI", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autocti_assistant", "autogalaxy_assistant", "autolens_assistant"},
    "PyAutoBrain/tests/test_community_conductor.py": {"Jammy2211", "PyAutoFit", "PyAutoLabs", "PyAutoLens", "admin_jammy"},
    "PyAutoBrain/tests/test_hygiene_conductor.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "autofit_workspace", "autolens_workspace"},
    # Load-bearing real names: the ranking tests pin resolution against the
    # LIVE body map (`slug == "PyAutoLabs/PyAutoFit"`; `_upstream_noise`
    # filters via KNOWN_REPOS), so synthetic names would test nothing.
    "PyAutoBrain/tests/test_intake_reconcile_ranking.py": {"PyAutoArray", "PyAutoFit", "PyAutoLabs", "autofit_workspace", "autolens_workspace"},
    "PyAutoBrain/tests/test_mind_commit_guard.py": {"/home/jammy", "PyAutoFit", "PyAutoLabs"},
    "PyAutoBrain/tests/test_policy_seams.py": {"PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoBrain/tests/test_review_inplace.py": {"PyAutoArray", "PyAutoLabs"},
    "PyAutoBrain/tests/test_skill_install.py": {"PyAutoLabs"},
    "PyAutoBrain/tests/test_workspace_conductor.py": {"HowToGalaxy", "HowToLens", "autolens_workspace", "autoreduce_workspace"},
    "PyAutoHands/autohands/aggregate_results.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    # PyAutoScientist: the cross-board footer nav names the organism board.
    "PyAutoHands/autohands/board.py": {"PyAutoScientist"},
    "PyAutoHands/autohands/build_util.py": {"PyAutoNerves"},
    "PyAutoHands/autohands/bump_colab_urls.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHands/autohands/check_search_memory.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHands/autohands/clone_seed.py": {"autofit_assistant"},
    "PyAutoHands/autohands/create_analysis_issue.py": {"PyAutoLabs"},
    "PyAutoHands/autohands/env_config.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHands/autohands/generate_autofit.py": {"autofit_workspace"},
    "PyAutoHands/autohands/generate_markdown.py": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoHands/autohands/generate_release_notes.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "PyAutoScientist"},
    "PyAutoHands/autohands/navigator.py": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoCTI", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoHands/autohands/repro_command.py": {"PyAutoLabs", "autogalaxy_workspace_test"},
    "PyAutoHands/autohands/run_all.py": {"HowToLens", "PyAutoLabs", "autolens_workspace", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoHands/autohands/run_notebook.py": {"autolens_workspace"},
    "PyAutoHands/autohands/slack_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoHands/autohands/tag_and_merge.sh": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoHands/pre_build.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "admin_jammy", "autofit_workspace", "autofit_workspace_developer", "autofit_workspace_test", "autogalaxy_workspace", "autogalaxy_workspace_test", "autolens_assistant", "autolens_workspace", "autolens_workspace_developer", "autolens_workspace_test", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoHands/tests/test_bump_colab_urls.py": {"Jammy2211", "PyAutoFit", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHands/tests/test_check_search_memory.py": {"PyAutoFit", "autogalaxy_workspace"},
    "PyAutoHands/tests/test_env_config.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHands/tests/test_generate_markdown.py": {"PyAutoArray", "autolens_workspace"},
    "PyAutoHands/tests/test_python_matrix_workflow.py": {"PyAutoFit"},
    "PyAutoHands/tests/test_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoHands/tests/test_repro_command.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHands/tests/test_run_all_history.py": {"HowToLens", "autogalaxy_workspace_test", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoHands/tests/test_slack_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoHands/tests/test_workspace_config_precedence.py": {"autofit_workspace", "autofit_workspace_test", "autogalaxy_workspace", "autogalaxy_workspace_test", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/heart/_color.sh": {"PyAutoFit"},
    "PyAutoHeart/heart/_common.sh": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/ci_status.py": {"autolens_workspace"},
    "PyAutoHeart/heart/checks/manifest_drift.py": {"PyAutoLabs", "admin_jammy"},
    "PyAutoHeart/heart/checks/profiling_drift.py": {"PyAutoLabs", "autolens_profiling", "autolens_workspace_test"},
    "PyAutoHeart/heart/checks/script_timing.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/test_run.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/unit_test_timing.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoHeart/heart/checks/url_check.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "Jammy2211", "PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHeart/heart/checks/url_check_live.py": {"PyAutoLabs", "PyAutoLens", "admin_jammy"},
    "PyAutoHeart/heart/checks/url_sweep.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoHeart/heart/checks/verify_install.sh": {"PyAutoNerves", "PyAutoLabs", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/heart/checks/version_skew.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/workspace_testmode_timing.py": {"PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHeart/heart/checks/worktree_drift.py": {"PyAutoLabs"},
    # PyAutoScientist: the cross-board footer nav names the organism board
    # (the family's one non-organ member) — same surface as the Hands entry.
    "PyAutoHeart/heart/dashboard.py": {"autolens_profiling", "pyautolabs.github.io", "PyAutoScientist"},
    "PyAutoHeart/heart/fix.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHeart/heart/readiness.py": {"autolens_profiling", "autolens_workspace_test"},
    "PyAutoHeart/heart/shell/heart_prompt.sh": {"PyAutoLabs"},
    "PyAutoHeart/heart/state.py": {"PyAutoFit"},
    "PyAutoHeart/heart/tick.sh": {"autolens_profiling"},
    "PyAutoHeart/heart/validate.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/scripts/health_audit.sh": {"PyAutoLabs"},
    "PyAutoHeart/scripts/health_release.sh": {"PyAutoLabs"},
    "PyAutoHeart/scripts/health_sync.sh": {"PyAutoLabs", "admin_jammy"},
    "PyAutoHeart/tests/test_ci_status.py": {"PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/tests/test_dashboard.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/tests/test_manifest_drift.py": {"PyAutoNerves", "PyAutoFit", "PyAutoLabs"},
    "PyAutoHeart/tests/test_noise.py": {"HowToFit", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_readiness.py": {"HowToLens", "PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autogalaxy_workspace", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_repo_config.py": {"PyAutoCTI", "autocti_workspace", "autocti_workspace_test"},
    "PyAutoHeart/tests/test_state.py": {"PyAutoArray", "PyAutoFit"},
    "PyAutoHeart/tests/test_test_run.py": {"autofit_workspace", "autolens_workspace"},
    "PyAutoHeart/tests/test_unit_test_timing.py": {"PyAutoFit"},
    "PyAutoHeart/tests/test_url_check.py": {"HowToFit", "HowToGalaxy", "HowToLens", "Jammy2211", "PyAutoFit", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHeart/tests/test_validate.py": {"PyAutoArray", "PyAutoNerves", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_verify_install_script.py": {"Jammy2211", "PyAutoLabs", "autolens_workspace"},
    "PyAutoHeart/tests/test_version_skew.py": {"HowToFit", "PyAutoFit", "PyAutoLens", "autofit_workspace", "autolens_assistant", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_workspace_testmode_timing.py": {"autolens_workspace"},
}


def firewall_tokens(repos):
    """Instance facts to hunt for: every non-organ repo name, every GitHub
    owner, and the local workspace home. Organ names are framework identity
    (a fork keeps them), so they are not tokens."""
    tokens = {name for name, r in repos.items() if r["category"] != "organ"}
    tokens |= {owner_of(r) for r in repos.values()}
    tokens.add("/home/jammy")
    return sorted(tokens, key=len, reverse=True)


def check_tenant_firewall(root, repos):
    pattern = re.compile(
        "|".join(
            r"(?<![A-Za-z0-9_])" + re.escape(t) + r"(?![A-Za-z0-9_])"
            for t in firewall_tokens(repos)
        )
    )
    problems = []
    for organ in FIREWALL_ORGANS:
        base = bootstrap_checkout(root, organ)
        if not base.is_dir():
            continue  # not checked out in this environment
        for path in sorted(base.rglob("*")):
            if path.suffix not in (".py", ".sh") or not path.is_file():
                continue
            rel = f"{organ}/{path.relative_to(base).as_posix()}"
            if "__pycache__" in rel:
                continue
            hits = {}
            for lineno, line in enumerate(
                path.read_text(errors="replace").splitlines(), start=1
            ):
                for m in pattern.finditer(line):
                    hits.setdefault(m.group(0), lineno)
            new = {t: n for t, n in hits.items() if t not in FIREWALL_ALLOWLIST.get(rel, ())}
            if new:
                facts = ", ".join(
                    f"'{tok}' (line {lineno})" for tok, lineno in sorted(new.items())
                )
                listed = "allowlisted file" if rel in FIREWALL_ALLOWLIST else "unlisted file"
                problems.append(
                    f"{rel}: new instance fact(s) in {listed} — {facts}"
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
    # Fallback: extract the trailing "<owner>/<repo>" slug from any other
    # remote form — e.g. a cloud-session git-proxy URL like
    # "http://user@host:port/git/<owner>/<repo>", or a local mirror. Identity
    # is the slug, not the host, so a correct slug served behind a different
    # host is not drift (this keeps the origin check meaningful in web/CI
    # sessions instead of flagging every checkout). A genuinely wrong owner or
    # repo name still fails the comparison downstream.
    parts = [p for p in url.split("/") if p]
    if len(parts) >= 2:
        return "/".join(parts[-2:])
    return url


def is_checkout(path):
    """Is this directory a git checkout? `.git` is a directory in a clone and a
    file in a worktree, so ask whether it exists, not what it is."""
    return (path / ".git").exists()


def check_origins(root, repos):
    problems = []
    for name, repo in repos.items():
        checkout = repo_checkout(root, name)
        if not is_checkout(checkout):
            # Not checked out here, so there is nothing for THIS leg to
            # read. Absence itself is no longer silent — the "workspace
            # checkouts" leg owns it — so this narrows the leg, not the
            # coverage.
            continue
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


def root_checkouts(root):
    """Every checkout at the root or directly inside a family directory."""
    return [entry.name for entry in all_checkouts(root)]


def checkout_counts(root, repos, marker):
    """`(checked_out, declared, enforced)` — the denominator for the leg below,
    and whether this root is one the leg can hold to it."""
    checked_out = sum(1 for name in repos if repo_checkout(root, name).is_dir())
    return checked_out, len(repos), (root / marker).is_file()


def check_checkouts(root, repos, unmapped, marker):
    """Both directions of "is what is declared what is actually here?".

    manifest -> disk: a declared repo that is not checked out. Every other leg
    SKIPS an absent repo — correctly, since it has nothing to inspect — so a
    regroup that left a repo behind read as a clean bill of health from eleven
    checks that inspected nothing. Somebody has to say it once, and this is the
    leg that does; the skips elsewhere now narrow the leg, not the coverage.

    disk -> manifest: a checkout at the root that no manifest entry declares.
    Walking the manifest and asking whether each entry is present structurally
    cannot see this, so an undeclared checkout was not a failure but silence —
    invisible to every manifest-driven sweep, including the audit whose whole
    job was to answer "did we miss a repo?" (PyAutoMind, manifest_gap).
    `unmapped_checkouts:` is how a deliberate neighbour says so.

    Enforced only under a root that says it is one by carrying the marker. A CI
    matrix or a web session clones four repos side by side with no root above
    them, and "you are missing thirty-four repos" is noise there, not drift, so
    an unmarked root reports its denominator (the session-hook leg's lesson)
    and fails nothing. Nothing here REQUIRES a marker to exist.
    """
    if not (root / marker).is_file():
        return []
    problems = [
        f"'{name}': declared in repos.yaml but not checked out at the "
        f"workspace root"
        for name in repos
        if not is_checkout(repo_checkout(root, name))
    ]
    declared_paths = {repo_checkout(root, name).resolve() for name in repos}
    problems += [
        f"'{name}': a checkout at the workspace root that repos.yaml does not "
        f"declare (add it to repos.yaml, or to unmapped_checkouts:)"
        for path in all_checkouts(root)
        for name in [path.name]
        if path.resolve() not in declared_paths and not (
            path.parent == root and name in unmapped)
    ]
    return problems


# --------------------------------------------------------------------------

def session_start_entries(settings):
    """Every hook command registered under SessionStart, whatever the nesting
    (the harness accepts a list of matcher groups, each holding a hooks list)."""
    commands = []
    for group in settings.get("hooks", {}).get("SessionStart", []) or []:
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []) or []:
            if isinstance(hook, dict) and "command" in hook:
                commands.append(hook["command"])
    return commands


def settings_registers_hook(text):
    try:
        settings = json.loads(text)
    except (ValueError, TypeError):
        return False
    if not isinstance(settings, dict):
        return False
    return SESSION_HOOK_COMMAND in session_start_entries(settings)


def pre_tool_use_entries(settings):
    """Every hook command registered under PreToolUse, whatever the nesting."""
    commands = []
    for group in settings.get("hooks", {}).get("PreToolUse", []) or []:
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []) or []:
            if isinstance(hook, dict) and "command" in hook:
                commands.append(hook["command"])
    return commands


def settings_registers_deliverable_hook(text):
    try:
        settings = json.loads(text)
    except (ValueError, TypeError):
        return False
    if not isinstance(settings, dict):
        return False
    return DELIVERABLE_HOOK_COMMAND in pre_tool_use_entries(settings)


def register_deliverable_hook(settings):
    """Add the PreToolUse registration, preserving every other hook the repo
    already runs on PreToolUse (the workspace root, for one, guards Bash)."""
    hooks = settings.setdefault("hooks", {})
    groups = hooks.setdefault("PreToolUse", [])
    groups.append({
        "matcher": DELIVERABLE_HOOK_MATCHER,
        "hooks": [{"type": "command", "command": DELIVERABLE_HOOK_COMMAND}],
    })
    return settings


def register_session_hook(settings):
    """Add the SessionStart registration, preserving everything else the repo
    keeps in its settings.json (permissions, env, other hook events)."""
    hooks = settings.setdefault("hooks", {})
    groups = hooks.setdefault("SessionStart", [])
    groups.append({"hooks": [{"type": "command", "command": SESSION_HOOK_COMMAND}]})
    return settings


def session_hook_excluded(repo_spec):
    """A manifest entry carrying `session_hook: false` is out of scope entirely.

    A recorded exclusion, not drift: the repos that carry it live in a personal
    namespace, are already outside the org-wide dev sweeps, and never had a
    `.claude/`. Every other repo keeps the hook (PyAutoMind#369).
    """
    return isinstance(repo_spec, dict) and repo_spec.get("session_hook") is False


def session_hook_counts(root, repos):
    """The denominator for the hook leg — `(checked_out, in_scope, excluded)`.

    * `excluded` — manifest repos with `session_hook: false`. They are a
      recorded exclusion, never counted as drift, and NOT part of `in_scope`.
    * `in_scope` — every OTHER manifest repo, whether or not it is checked out
      here. This is the true rollout surface of the canonical hook.
    * `checked_out` — the in-scope repos that exist on disk in this
      environment: the only ones `--check` can inspect or `--write` can fix.

    Printed beside the leg's status so a session holding four repos can see
    that it is seeing four of thirty-four. Two regeneration waves run from
    four-repo sessions silently re-staled the other thirty precisely because
    the check reported `OK` with no denominator (PyAutoMind#369).
    """
    excluded = sum(1 for spec in repos.values() if session_hook_excluded(spec))
    in_scope = [n for n, spec in repos.items() if not session_hook_excluded(spec)]
    checked_out = sum(1 for name in in_scope if repo_checkout(root, name).is_dir())
    return checked_out, len(in_scope), excluded


def _check_installed_hook(problems, name, repo_dir, rel, canonical, text):
    """One installed copy: present, byte-identical to its canonical file, +x."""
    hook = repo_dir / rel
    if not hook.exists():
        problems.append(f"'{name}': no {rel}")
    elif hook.read_text() != text:
        problems.append(f"'{name}': {rel} differs from {canonical}")
    elif not os.access(hook, os.X_OK):
        problems.append(f"'{name}': {rel} is not executable")


def check_session_hooks(root, repos, hook_text, deliverable_text):
    """Both generated hooks, in every checked-out in-scope repo.

    One leg, not two: they share a rollout surface, a manifest exclusion and a
    settings.json, and a repo that has one but not the other is exactly the
    half-installed state the propagation workflow exists to prevent."""
    problems = []
    for name, spec in repos.items():
        if session_hook_excluded(spec):
            continue  # recorded manifest exclusion — see session_hook_excluded
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            continue  # not checked out in this environment
        if structure_lint_forbids(repo_dir, ".claude"):
            continue  # --write skips it; check_structure_lints reports it
        _check_installed_hook(problems, name, repo_dir, SESSION_HOOK_REL,
                              SESSION_HOOK_FILE, hook_text)
        _check_installed_hook(problems, name, repo_dir, DELIVERABLE_HOOK_REL,
                              DELIVERABLE_HOOK_FILE, deliverable_text)
        settings = repo_dir / SESSION_SETTINGS_REL
        if not settings.exists():
            problems.append(f"'{name}': no {SESSION_SETTINGS_REL}")
            continue
        settings_text = settings.read_text()
        if not settings_registers_hook(settings_text):
            problems.append(
                f"'{name}': {SESSION_SETTINGS_REL} does not register the "
                "SessionStart hook"
            )
        if not settings_registers_deliverable_hook(settings_text):
            problems.append(
                f"'{name}': {SESSION_SETTINGS_REL} does not register the "
                "PreToolUse end-at-deliverable hook"
            )
    return problems


def _install_hook(repo_dir, rel, text):
    """Write one hook copy verbatim and make it executable. Idempotent."""
    hook = repo_dir / rel
    hook.parent.mkdir(parents=True, exist_ok=True)
    if hook.exists() and hook.read_text() == text:
        print(f"unchanged: {hook}")
    else:
        hook.write_text(text)
        print(f"wrote: {hook}")
    hook.chmod(0o755)


def write_session_hooks(root, repos, hook_text, deliverable_text):
    """Install both generated hooks + their registrations in every checked-out
    repo: the SessionStart hook (Python 3.12) and the PreToolUse
    end-at-deliverable guard. Idempotent: an up-to-date copy is left alone, and
    a settings.json that already registers a hook keeps its own formatting and
    every other key. Repos flagged `session_hook: false` in the manifest are
    skipped entirely."""
    for name, spec in repos.items():
        if session_hook_excluded(spec):
            continue  # recorded manifest exclusion — see session_hook_excluded
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            continue
        if structure_lint_forbids(repo_dir, ".claude"):
            print(
                "SKIPPED (repo's layout lint disallows .claude/): "
                f"{repo_dir / SESSION_HOOK_REL}"
            )
            continue
        _install_hook(repo_dir, SESSION_HOOK_REL, hook_text)
        _install_hook(repo_dir, DELIVERABLE_HOOK_REL, deliverable_text)

        settings = repo_dir / SESSION_SETTINGS_REL
        if settings.exists():
            text = settings.read_text()
            missing = [
                register for register, registered in (
                    (register_session_hook, settings_registers_hook(text)),
                    (register_deliverable_hook,
                     settings_registers_deliverable_hook(text)),
                ) if not registered
            ]
            if not missing:
                print(f"unchanged: {settings}")
                continue
            try:
                current = json.loads(text)
            except ValueError:
                print(f"SKIPPED (unparseable JSON, fix by hand): {settings}")
                continue
            if not isinstance(current, dict):
                print(f"SKIPPED (not a JSON object): {settings}")
                continue
        else:
            current = {}
            missing = [register_session_hook, register_deliverable_hook]
        for register in missing:
            current = register(current)
        settings.write_text(json.dumps(current, indent=2) + "\n")
        print(f"wrote: {settings}")


def codex_hook_names(repo_spec):
    """The ordered Codex adapters opted into by one manifest entry.

    Absence is deliberate exclusion.  Keeping the rollout explicit prevents a
    generator run in a full workspace from materialising `.codex/` in repos
    whose hook behavior has not yet been reviewed.
    """
    if not isinstance(repo_spec, dict):
        return []
    names = repo_spec.get("codex_hooks", [])
    return names if isinstance(names, list) else None


def render_codex_hooks(repo_spec):
    """Render one deterministic `.codex/hooks.json` adapter."""
    names = codex_hook_names(repo_spec)
    if names is None:
        raise ValueError("codex_hooks must be a list")
    unknown = [name for name in names if name not in CODEX_HOOK_DEFINITIONS]
    if unknown:
        raise ValueError("unknown codex hook(s): " + ", ".join(unknown))
    if len(names) != len(set(names)):
        raise ValueError("codex_hooks contains a duplicate")

    groups = []
    for name in names:
        definition = CODEX_HOOK_DEFINITIONS[name]
        groups.append({
            "matcher": definition["matcher"],
            "hooks": [{
                "type": "command",
                "command": definition["command"],
                "statusMessage": definition["statusMessage"],
            }],
        })
    return json.dumps({
        "description": (
            "Generated by PyAutoMind/scripts/repos_sync.py. Review and trust "
            "the current hook definition with Codex /hooks before relying on it."
        ),
        "hooks": {"PreToolUse": groups},
    }, indent=2) + "\n"


def check_codex_hooks(root, repos):
    """Check only explicitly opted-in Codex hook surfaces."""
    problems = []
    for name, spec in repos.items():
        hook_names = codex_hook_names(spec)
        if hook_names == []:
            continue
        if hook_names is None:
            problems.append(f"'{name}': codex_hooks must be a list")
            continue
        try:
            expected = render_codex_hooks(spec)
        except ValueError as error:
            problems.append(f"'{name}': {error}")
            continue
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            # Not checked out here, so there is nothing for THIS leg to
            # read. Absence itself is no longer silent — the "workspace
            # checkouts" leg owns it — so this narrows the leg, not the
            # coverage.
            continue
        path = repo_dir / CODEX_HOOKS_REL
        if not path.exists():
            problems.append(f"'{name}': no {CODEX_HOOKS_REL}")
        elif path.read_text() != expected:
            problems.append(
                f"'{name}': {CODEX_HOOKS_REL} differs from repos.yaml"
            )
    return problems


def write_codex_hooks(root, repos):
    """Write Codex hook adapters only for manifest entries that opt in."""
    for name, spec in repos.items():
        hook_names = codex_hook_names(spec)
        if hook_names == []:
            continue
        if hook_names is None:
            raise SystemExit(f"repos_sync: '{name}': codex_hooks must be a list")
        try:
            text = render_codex_hooks(spec)
        except ValueError as error:
            raise SystemExit(f"repos_sync: '{name}': {error}") from error
        repo_dir = repo_checkout(root, name)
        if not repo_dir.is_dir():
            continue
        path = repo_dir / CODEX_HOOKS_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text() == text:
            print(f"unchanged: {path}")
        else:
            path.write_text(text)
            print(f"wrote: {path}")



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=None)
    # An organ's PR gate must fail only on the leg that PR can cause — a Brain
    # PR should not go red because a Mind-side generated block is stale. The
    # label is the check's printed name, e.g. "tenant firewall (organ code)".
    parser.add_argument(
        "--only",
        action="append",
        metavar="CHECK",
        help="run only this drift-check leg (repeatable; use the label the "
             "check prints)",
    )
    # The complement, for the narrower case: every leg is the caller's to fail
    # EXCEPT one whose precondition that caller cannot meet. Subtracts from
    # whatever --only selected; an unknown label is an error either way, so a
    # typo cannot quietly turn a gate off.
    parser.add_argument(
        "--skip",
        action="append",
        metavar="CHECK",
        help="run every drift-check leg but this one (repeatable; use the "
             "label the check prints; subtracts from --only)",
    )
    args = parser.parse_args()

    mind_root = Path(__file__).resolve().parents[1]
    # `--root` still wins — only the default changed, from "the directory above
    # this checkout" to the shared resolver (see workspace_root).
    root = args.root or workspace_root(mind_root)
    marker = root_marker(mind_root)
    categories, repos = load_manifest(mind_root)
    unmapped = load_unmapped_checkouts(mind_root)

    smap = system_map(categories, repos)
    hpol = load_history_policy(mind_root)
    remote = load_remote_sessions(mind_root)
    deliverable = load_deliverable_policy(mind_root)
    hook_text = load_session_hook(mind_root)
    deliverable_hook_text = load_deliverable_hook(mind_root)

    # `--write --only "generated Codex hooks"` is the bounded rollout command:
    # it must not fan out unrelated generated docs or Claude hooks while a task
    # intentionally holds only the Codex opt-in repos.
    codex_only_write = args.only and set(args.only) == {CODEX_HOOKS}
    smoke_only_write = args.only and set(args.only) == {smoke_sync.LABEL}
    if args.write and not codex_only_write and not smoke_only_write:
        # The marker goes with the routing table: both are workspace-root
        # artifacts of the body map, and the marker is what lets the resolver
        # (and the checkout leg below) find this root again from anywhere under
        # it. Additive by construction — with no marker the resolver falls back
        # to the parent of a checkout, which is how --write reaches a root that
        # has none yet, and every later call takes the marker instead.
        write_root_marker(root, marker)
        write_block(root / "AGENTS.md", routing_table(categories, repos),
                    required=True)
        write_block(bootstrap_checkout(root, "PyAutoBrain") / "skills/WORKFLOW.md",
                    owner_map(categories, repos), required=True)
        for name, repo in repos.items():
            if repo["category"] != "organ":
                continue
            write_block(repo_checkout(root, name) / "AGENTS.md", smap, MAP_BEGIN, MAP_END,
                        required=False)
        # The history policy is universal — written into every repo (not just
        # organs) that has added the markers.
        #
        # The deliverable policy is universal AND self-installing: a repo that
        # already carries the history block gets the markers placed under it
        # here, so the block lands without thirty hand-edits. (The rule it
        # carries was broken twice by sessions reasoning past prose; waiting for
        # each repo to opt in is how the long tail stays unprotected.)
        insert_deliverable_markers(root, repos)
        for name in repos:
            write_block(repo_checkout(root, name) / "AGENTS.md", hpol,
                        HISTORY_BEGIN, HISTORY_END, required=False)
            write_block(repo_checkout(root, name) / "AGENTS.md", remote,
                        REMOTE_BEGIN, REMOTE_END, required=False)
            write_block(repo_checkout(root, name) / "AGENTS.md", deliverable,
                        DELIVERABLE_BEGIN, DELIVERABLE_END, required=False)
        for rel, bold in PUBLIC_TABLE_TARGETS:
            write_block(public_target(root, rel), organ_public_table(repos, bold=bold),
                        ORGANS_BEGIN, ORGANS_END, required=False)
        write_claude_md_pointers(root, repos)
        write_session_hooks(root, repos, hook_text, deliverable_hook_text)
    if args.write and not smoke_only_write:
        write_codex_hooks(root, repos)
    smoke_enabled = smoke_sync.rollout_enabled(mind_root)
    if args.write and not codex_only_write and smoke_enabled:
        smoke_sync.write(root, repos, (mind_root / smoke_sync.SOURCE).read_text())
    if args.write and smoke_only_write and not smoke_enabled:
        raise SystemExit("smoke bootstrap rollout is held; use smoke_bootstrap_sync.py --dry-run")

    # Lazy (label -> thunk) so --only pays for exactly the selected legs.
    checks = {
        smoke_sync.LABEL: lambda: smoke_sync.check(
            root, repos, (mind_root / smoke_sync.SOURCE).read_text()),
        "PyAutoHeart/config/repos.yaml": lambda: check_heart(root, repos),
        "PyAutoHands/pre_build.sh": lambda: check_pre_build(root, repos),
        "PyAutoHands/autohands/config/workspaces.yaml":
            lambda: check_hands_workspaces(root, repos),
        "ensure_workspace_labels.sh": lambda: check_labels(root, repos),
        "hygiene conductor coverage":
            lambda: check_hygiene_coverage(root, repos, mind_root),
        "local checkout origins": lambda: check_origins(root, repos),
        CHECKOUTS: lambda: check_checkouts(root, repos, unmapped, marker),
        "tenant firewall (organ code)": lambda: check_tenant_firewall(root, repos),
        "organism-map blocks (generated)":
            lambda: check_map_blocks(root, repos, smap),
        "never-rewrite-history blocks (generated)":
            lambda: check_history_blocks(root, repos, hpol),
        "remote-session blocks (generated)":
            lambda: check_remote_blocks(root, repos, remote),
        "end-at-deliverable blocks (generated)":
            lambda: check_deliverable_blocks(root, repos, deliverable),
        "public front-door organ tables (generated)":
            lambda: check_public_tables(root, repos),
        "hub organism blurb (organs present)": lambda: check_hub_blurb(root, repos),
        "CLAUDE.md → AGENTS.md pointers":
            lambda: check_claude_md_pointers(root, repos),
        SESSION_HOOKS: lambda: check_session_hooks(
            root, repos, hook_text, deliverable_hook_text),
        CODEX_HOOKS: lambda: check_codex_hooks(root, repos),
        "target-repo layout lints": lambda: check_structure_lints(root, repos),
    }
    # Both flags match the printed label exactly, and both are validated
    # against the FULL registry before anything is narrowed — naming a real leg
    # that --only already excluded is a no-op, naming a leg that does not exist
    # is a typo, and only the second one is allowed to be silent.
    for flag, selected in (("--only", args.only), ("--skip", args.skip)):
        unknown = [label for label in selected or [] if label not in checks]
        if unknown:
            raise SystemExit(
                f"repos_sync: unknown {flag} check(s): "
                + ", ".join(f"'{u}'" for u in unknown)
                + "; choose from: "
                + ", ".join(f"'{label}'" for label in checks)
            )
    if args.only:
        checks = {label: checks[label] for label in args.only}
    if args.skip:
        # Subtraction, after selection: --only says what to run, --skip takes
        # legs back off that list.
        checks = {label: run_check for label, run_check in checks.items()
                  if label not in args.skip}
    drift = False
    for label, run_check in checks.items():
        if label == smoke_sync.LABEL and not smoke_enabled:
            print(f"deferred {label}: rollout held in repos.yaml; installations not graded")
            continue
        problems = run_check()
        status = "OK" if not problems else f"{len(problems)} mismatch(es)"
        if label == SESSION_HOOKS:
            # The one leg whose blind spot is invisible in its own verdict: it
            # skips absent repos by design, so a four-repo session reads "OK"
            # for a 34-repo rollout surface. Say the denominator out loud.
            seen, in_scope, excluded = session_hook_counts(root, repos)
            status += f" ({seen} of {in_scope} checked out, {excluded} excluded)"
        print(f"check {label}: {status}")
        if label == smoke_sync.LABEL:
            try:
                seen = len(list(smoke_sync.installations(root, repos)))
                total = len(list(smoke_sync.targets(repos)))
                print(f"  • {seen} of {total} smoke bootstrap targets checked out")
            except (OSError, ValueError) as error:
                print(f"  • coverage unavailable: {error}")
        if label == CHECKOUTS:
            # The same lesson from the other side: this is the leg that CAN say
            # "a repo is missing", so where it is not enforcing (an unmarked
            # root — CI, a web session) it has to say so out loud, or a silent
            # OK reads as full coverage all over again. Printed BELOW the
            # verdict, not appended to it: PyAutoHeart's manifest-drift check
            # parses `check <label>: <status>` with the status anchored at the
            # end of the line, so a suffix would drop this leg out of Heart's
            # view entirely.
            seen, declared, enforced = checkout_counts(root, repos, marker)
            detail = f"{seen} of {declared} declared repo(s) checked out"
            if not enforced:
                detail += f"; no {marker} at this root — presence not enforced"
            print(f"  • {detail}")
        for p in problems:
            drift = True
            print(f"  ✗ {p}")

    # AGENTS-less repos are reported (for a human to write real guidance), never
    # auto-stubbed, and never fail the run.
    missing = repos_without_agents_md(root, repos)
    if missing:
        print(f"note: {len(missing)} checked-out repo(s) have no AGENTS.md "
              f"(pointer not applicable — needs human-written guidance):")
        for name in missing:
            print(f"  • {name}")

    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
