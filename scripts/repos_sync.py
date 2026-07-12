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

and, between `<!-- repos_sync:map:begin -->` / `<!-- repos_sync:map:end -->`
markers, the compact **organism map** in each organ repo's own AGENTS.md
(<root>/<organ>/AGENTS.md). The map is the always-loaded orientation an agent
sees first: the peer organs, their roles, the call chain and the
conductor/faculty rule — so a session opened in one repo still knows the whole
organism. A repo opts in by adding the map markers to its AGENTS.md; organ
repos (or roots) that are absent, or lack the markers, are skipped rather than
failing the run.

--check (always run) verifies, against the manifest:

  * PyAutoHeart/config/repos.yaml          — polled repos exist, owners match
  * PyAutoBuild/pre_build.sh               — run_workspace repos exist
  * admin_jammy/software/ensure_workspace_labels.sh — owner/name pairs match
  * the `origin` remote of every local checkout — manifest matches reality
  * the tenant firewall — no instance fact (satellite repo name, GitHub
    owner, workspace path) in Brain/Heart/Build *.py / *.sh outside the
    declared config surfaces (FIREWALL_ALLOWLIST below)

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
MAP_BEGIN = "<!-- repos_sync:map:begin -->"
MAP_END = "<!-- repos_sync:map:end -->"

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
        print(f"skipped (no map markers): {path}")
        return
    changed = replace_block(path, content, begin, end)
    print(f"{'updated' if changed else 'unchanged'}: {path}")


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
        agents = root / name / "AGENTS.md"
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


def claude_md_is_pointer(text):
    """A CLAUDE.md counts as compliant iff it `@`-imports AGENTS.md on its own
    line (a real import that expands into context), not merely prose naming it."""
    return CLAUDE_IMPORT_RE.search(text) is not None


def check_claude_md_pointers(root, repos):
    problems = []
    for name in repos:
        repo_dir = root / name
        if not repo_dir.is_dir():
            continue  # not checked out in this environment
        if not (repo_dir / "AGENTS.md").exists():
            continue  # AGENTS-less repos are reported separately, not drift
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
        if (root / name).is_dir() and not (root / name / "AGENTS.md").exists()
    ]


def write_claude_md_pointers(root, repos):
    """Create the canonical pointer wherever a checked-out repo has an AGENTS.md
    but a missing or non-compliant CLAUDE.md. Idempotent: a repo already carrying
    the `@AGENTS.md` import is left untouched; a repo with no AGENTS.md is
    skipped (nothing to point at)."""
    for name in repos:
        repo_dir = root / name
        if not repo_dir.is_dir():
            continue
        if not (repo_dir / "AGENTS.md").exists():
            print(f"skipped (no AGENTS.md): {repo_dir / 'CLAUDE.md'}")
            continue
        claude = repo_dir / "CLAUDE.md"
        if claude.exists() and claude_md_is_pointer(claude.read_text()):
            print(f"unchanged: {claude}")
            continue
        verb = "rewrote (dead pointer)" if claude.exists() else "created"
        claude.write_text(CLAUDE_MD_POINTER)
        print(f"{verb}: {claude}")


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

FIREWALL_ORGANS = ("PyAutoBrain", "PyAutoHeart", "PyAutoBuild")

# The declared config surfaces, frozen as a per-file token baseline (seeded
# 2026-07-10 from the live mains; the §1 inventory of the PyAutoScientist
# assessment names the load-bearing ones). Semantics: a NEW instance fact in
# a listed file, or ANY instance fact in an unlisted file, is drift. Phase-3
# config extraction shrinks this list; never grow it casually — a new entry
# means a new file an adopting fork must rewrite.
FIREWALL_ALLOWLIST = {
    "PyAutoBrain/agents/_common.sh": {"PyAutoLabs"},
    "PyAutoBrain/agents/conductors/bug/_bug.py": {"PyAutoArray"},
    "PyAutoBrain/agents/conductors/bug/bug.sh": {"PyAutoLabs"},
    "PyAutoBrain/agents/conductors/health/health.sh": {"PyAutoConf"},
    "PyAutoBrain/agents/conductors/clone/_clone.py": {"HowToFit", "PyAutoFit", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autolens_assistant"},
    "PyAutoBrain/agents/conductors/clone/clone.sh": {"HowToFit", "PyAutoFit", "autofit_workspace", "autolens_assistant"},
    "PyAutoBrain/agents/conductors/intake/_intake.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace"},
    "PyAutoBrain/agents/conductors/profiling/_profiling.py": {"PyAutoLabs", "autolens_profiling"},
    "PyAutoBrain/agents/conductors/profiling/profiling.sh": {"autolens_profiling"},
    "PyAutoBrain/agents/conductors/release/nightly.sh": {"PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/conductors/release/rehearse.sh": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/conductors/release/validate.sh": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBrain/agents/faculties/memory/_memory.py": {"autolens_assistant"},
    "PyAutoBrain/agents/faculties/memory/memory.sh": {"autolens_assistant"},
    "PyAutoBrain/agents/faculties/review/_review.py": {"PyAutoLabs"},
    "PyAutoBrain/agents/faculties/review/review.sh": {"PyAutoLabs"},
    "PyAutoBrain/agents/faculties/samplers/_samplers.py": {"PyAutoFit", "autofit_workspace_developer", "autofit_workspace_test"},
    "PyAutoBrain/agents/faculties/samplers/samplers.sh": {"PyAutoFit", "autofit_workspace_developer", "autofit_workspace_test"},
    "PyAutoBrain/agents/faculties/sizing/_sizing.py": {"PyAutoFit"},
    "PyAutoBrain/bin/check_skill_line_counts.sh": {"admin_jammy", "autolens_profiling"},
    "PyAutoBrain/bin/install.sh": {"PyAutoFit", "PyAutoLabs", "admin_jammy", "autolens_profiling"},
    "PyAutoBrain/tests/test_activity_gate.py": {"HowToFit", "HowToLens", "PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoBrain/tests/test_policy_seams.py": {"PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoBrain/tests/test_review_inplace.py": {"PyAutoArray", "PyAutoLabs"},
    "PyAutoBuild/autobuild/aggregate_results.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBuild/autobuild/build_util.py": {"PyAutoConf"},
    "PyAutoBuild/autobuild/bump_colab_urls.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBuild/autobuild/create_analysis_issue.py": {"PyAutoLabs"},
    "PyAutoBuild/autobuild/generate_autofit.py": {"autofit_workspace"},
    "PyAutoBuild/autobuild/generate_markdown.py": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoBuild/autobuild/generate_release_notes.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBuild/autobuild/navigator.py": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoBuild/autobuild/repro_command.py": {"PyAutoLabs", "autogalaxy_workspace_test"},
    "PyAutoBuild/autobuild/run_all.py": {"HowToLens", "PyAutoLabs", "autolens_workspace", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoBuild/autobuild/slack_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBuild/autobuild/tag_and_merge.sh": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens"},
    "PyAutoBuild/pre_build.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "admin_jammy", "autofit_workspace", "autofit_workspace_developer", "autofit_workspace_test", "autogalaxy_workspace", "autogalaxy_workspace_test", "autolens_assistant", "autolens_workspace", "autolens_workspace_developer", "autolens_workspace_test", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoBuild/tests/test_bump_colab_urls.py": {"Jammy2211", "PyAutoFit", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoBuild/tests/test_generate_markdown.py": {"PyAutoArray", "autolens_workspace"},
    "PyAutoBuild/tests/test_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBuild/tests/test_run_all_history.py": {"HowToLens", "autogalaxy_workspace_test", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoBuild/tests/test_slack_release_notes.py": {"PyAutoArray", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens"},
    "PyAutoBuild/tests/test_workspace_config_precedence.py": {"autofit_workspace", "autofit_workspace_test", "autogalaxy_workspace", "autogalaxy_workspace_test", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/heart/_color.sh": {"PyAutoFit"},
    "PyAutoHeart/heart/_common.sh": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/ci_status.py": {"autolens_workspace"},
    "PyAutoHeart/heart/checks/manifest_drift.py": {"PyAutoLabs", "admin_jammy"},
    "PyAutoHeart/heart/checks/profiling_drift.py": {"PyAutoLabs", "autolens_profiling", "autolens_workspace_test"},
    "PyAutoHeart/heart/checks/script_timing.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/test_run.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/url_check.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "Jammy2211", "PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLabs", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHeart/heart/checks/url_check_live.py": {"PyAutoLabs", "PyAutoLens", "admin_jammy"},
    "PyAutoHeart/heart/checks/url_sweep.sh": {"HowToFit", "HowToGalaxy", "HowToLens", "PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace", "euclid_strong_lens_modeling_pipeline"},
    "PyAutoHeart/heart/checks/verify_install.sh": {"PyAutoConf", "PyAutoLabs", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/heart/checks/version_skew.py": {"PyAutoLabs"},
    "PyAutoHeart/heart/checks/worktree_drift.sh": {"PyAutoLabs"},
    "PyAutoHeart/heart/dashboard.py": {"autolens_profiling", "pyautolabs.github.io"},
    "PyAutoHeart/heart/fix.py": {"PyAutoFit", "PyAutoLabs"},
    "PyAutoHeart/heart/readiness.py": {"autolens_profiling", "autolens_workspace_test"},
    "PyAutoHeart/heart/shell/heart_prompt.sh": {"PyAutoLabs"},
    "PyAutoHeart/heart/state.py": {"PyAutoFit"},
    "PyAutoHeart/heart/tick.sh": {"autolens_profiling"},
    "PyAutoHeart/heart/validate.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/scripts/health_audit.sh": {"PyAutoLabs"},
    "PyAutoHeart/scripts/health_release.sh": {"PyAutoLabs"},
    "PyAutoHeart/scripts/health_sync.sh": {"PyAutoLabs", "admin_jammy"},
    "PyAutoHeart/tests/test_ci_status.py": {"PyAutoFit", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/tests/test_dashboard.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace"},
    "PyAutoHeart/tests/test_manifest_drift.py": {"PyAutoConf", "PyAutoFit", "PyAutoLabs"},
    "PyAutoHeart/tests/test_noise.py": {"HowToFit", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_readiness.py": {"HowToLens", "PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autogalaxy_workspace", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_state.py": {"PyAutoArray", "PyAutoFit"},
    "PyAutoHeart/tests/test_test_run.py": {"autofit_workspace", "autolens_workspace"},
    "PyAutoHeart/tests/test_url_check.py": {"HowToFit", "HowToGalaxy", "HowToLens", "Jammy2211", "PyAutoFit", "PyAutoLabs", "autofit_workspace", "autogalaxy_workspace", "autolens_workspace"},
    "PyAutoHeart/tests/test_validate.py": {"PyAutoArray", "PyAutoConf", "PyAutoFit", "PyAutoGalaxy", "PyAutoLens", "autolens_workspace", "autolens_workspace_test"},
    "PyAutoHeart/tests/test_verify_install_script.py": {"Jammy2211", "PyAutoLabs", "autolens_workspace"},
    "PyAutoHeart/tests/test_version_skew.py": {"HowToFit", "PyAutoFit", "PyAutoLens", "autofit_workspace", "autolens_assistant", "autolens_workspace", "autolens_workspace_test"},
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
        base = root / organ
        if not base.is_dir():
            continue  # not checked out in this environment
        for path in sorted(base.rglob("*")):
            if path.suffix not in (".py", ".sh") or not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
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

    smap = system_map(categories, repos)

    if args.write:
        write_block(root / "AGENTS.md", routing_table(categories, repos),
                    required=True)
        write_block(root / "PyAutoBrain/skills/WORKFLOW.md",
                    owner_map(categories, repos), required=True)
        for name, repo in repos.items():
            if repo["category"] != "organ":
                continue
            write_block(root / name / "AGENTS.md", smap, MAP_BEGIN, MAP_END,
                        required=False)
        write_claude_md_pointers(root, repos)

    checks = {
        "PyAutoHeart/config/repos.yaml": check_heart(root, repos),
        "PyAutoBuild/pre_build.sh": check_pre_build(root, repos),
        "ensure_workspace_labels.sh": check_labels(root, repos),
        "local checkout origins": check_origins(root, repos),
        "tenant firewall (organ code)": check_tenant_firewall(root, repos),
        "organism-map blocks (generated)": check_map_blocks(root, repos, smap),
        "CLAUDE.md → AGENTS.md pointers": check_claude_md_pointers(root, repos),
    }
    drift = False
    for label, problems in checks.items():
        status = "OK" if not problems else f"{len(problems)} mismatch(es)"
        print(f"check {label}: {status}")
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
