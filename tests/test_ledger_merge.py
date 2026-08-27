"""Tests for scripts/ledger_merge.py — the auto-merge safety gate.

This gate decides what lands on `main` with no human in the loop, so the
properties that matter are the refusals: default deny for anything
unclassified, no traversal or dotfile route past the ledger prefixes, no
pytest-collectable file smuggled in as a prompt asset, and every code home the
repo actually has (scripts/, tests/, .github/, skills/, policy/, docs/,
repos.yaml, the prose pages) staying on the human side of the line.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ledger_merge  # noqa: E402

SCRIPT = Path(ledger_merge.__file__)


def test_ledger_dirs_and_registry_files_are_ledger():
    for path in (
        "draft/feature/autolens/potential_corrections.md",
        "draft/triage/unclear.md",
        "active/some-task.md",
        "complete/2026/08/a-record.md",
        "complete/index.md",
        "complete/archive/shelved/old.md",
        "active.md",
        "planned.md",
        "parked.md",
        "condemned.md",
        "epics.md",
        "ideas.md",
        "autonomy_log.md",
        "dashboard.md",
        "dashboard.html",
    ):
        assert ledger_merge.is_ledger_path(path), path


def test_every_code_home_needs_a_human():
    for path in (
        "scripts/lifecycle.py",
        "scripts/ledger_merge.py",
        "tests/test_ledger_merge.py",
        ".github/workflows/mind_ledger_merge.yml",
        ".github/scripts/anything.py",
        ".gitignore",
        ".claude/settings.json",
        "skills/intake/SKILL.md",
        "policy/anything.md",
        "docs/pyautobrain/page.md",
        "repos.yaml",
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "REFERENCE.md",
        "ROUTING.md",
        "CONTRIBUTING.md",
        "AI_POLICY.md",
        "LICENSE",
        "logo.png",
    ):
        assert not ledger_merge.is_ledger_path(path), path


def test_unclassified_paths_default_to_deny():
    """A root file or top-level folder nobody has thought about is code."""
    for path in ("brand_new_root_file.md", "newfolder/thing.md", "notes.txt"):
        assert not ledger_merge.is_ledger_path(path), path


def test_traversal_cannot_smuggle_code_behind_a_ledger_prefix():
    for path in ("draft/../scripts/evil.py", "active/../../etc/passwd", ".."):
        assert not ledger_merge.is_ledger_path(path), path


def test_dot_paths_are_never_ledger_wherever_they_sit():
    for path in ("draft/.github/workflows/x.yml", "complete/.hidden", ".draft/x.md"):
        assert not ledger_merge.is_ledger_path(path), path


def test_inert_prompt_assets_ride_along_but_collectable_tests_do_not():
    """The ledger dirs really do carry reproduction scripts; those are inert.

    A file pytest would COLLECT is not — CI runs it from anywhere in the tree.
    """
    assert ledger_merge.is_ledger_path("draft/bug/autofit/ep_assets/run_once.py")
    assert ledger_merge.is_ledger_path("draft/bug/autofit/ep_assets/sweep.sh")
    for path in (
        "draft/bug/autofit/ep_assets/conftest.py",
        "draft/bug/autofit/ep_assets/test_thing.py",
        "complete/2026/08/assets/thing_test.py",
    ):
        assert not ledger_merge.is_ledger_path(path), path


def test_classify_splits_and_dedupes_preserving_order():
    ledger, blocked = ledger_merge.classify(
        ["active.md", "scripts/x.py", "active.md", "draft/a/b.md", "", "  "]
    )
    assert ledger == ["active.md", "draft/a/b.md"]
    assert blocked == ["scripts/x.py"]


def _run(*args, stdin=""):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "classify", *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def test_cli_exit_codes_separate_ledger_from_code():
    assert _run("active.md", "draft/a/b.md").returncode == 0
    result = _run("active.md", "scripts/lifecycle.py")
    assert result.returncode == 1
    assert "scripts/lifecycle.py" in result.stdout


def test_an_empty_diff_is_not_permission_to_merge():
    """Exit 0 means 'go'. Nothing to merge must never read as go."""
    result = _run(stdin="\n")
    assert result.returncode == 1
    assert "nothing to merge" in result.stdout


def test_this_repos_own_workflow_cannot_auto_merge_itself():
    """Self-consistency: the gate is on the code side of its own line."""
    assert not ledger_merge.is_ledger_path(".github/workflows/mind_ledger_merge.yml")
    assert not ledger_merge.is_ledger_path("scripts/ledger_merge.py")
