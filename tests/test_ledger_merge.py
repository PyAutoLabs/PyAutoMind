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
        "bundles.md",
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
        # A CONTROLLED vocabulary, not registry state: a `Themes:` keyword
        # added with no human in the loop is a grouping key nobody chose, and
        # the dashboard groups every bundle on it.
        "themes.md",
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


def test_base_and_explicit_paths_never_wait_on_an_open_stdin():
    """A Claude Code web/mobile session runs commands with a stdin that is not
    a TTY and never closes (a harness socket). `classify --base origin/main`
    hung there twice on 2026-09-17, because the old source order tried stdin
    before `--base`. With paths or `--base` given, stdin must not be touched:
    hold the pipe open and never write to it, and the run must still return.
    """
    for args in (["--base", "HEAD"], ["active.md" if "_run" == "_run" else "projects/a.md"]):
        proc = subprocess.Popen(
            [sys.executable, str(SCRIPT), "classify", *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            rc = proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            raise AssertionError(f"classify {' '.join(args)} blocked on an open stdin")
        finally:
            proc.stdin.close()
        out = proc.stdout.read()
        # `--base HEAD` diffs HEAD against itself: an empty diff, which blocks
        # (exit 1) — the point is that it answered, not what it answered.
        assert rc == (1 if args[0] == "--base" else 0), out


def test_base_takes_precedence_over_piped_paths():
    """Piped paths are read only when nothing else names the source."""
    result = _run("--base", "HEAD", stdin="README.md\n")
    assert result.returncode == 1
    assert "nothing to merge" in result.stdout


def test_this_repos_own_workflow_cannot_auto_merge_itself():
    """Self-consistency: the gate is on the code side of its own line."""
    assert not ledger_merge.is_ledger_path(".github/workflows/mind_ledger_merge.yml")
    assert not ledger_merge.is_ledger_path("scripts/ledger_merge.py")


# --- merge-entries ---------------------------------------------------------------

PRE = "# Active Tasks\n\n"


def _entry(slug, body="- status: issued\n"):
    return f"## {slug}\n{body}\n"


def test_entries_added_and_deleted_on_different_sides_merge_cleanly():
    base = PRE + _entry("a") + _entry("b")
    ours = PRE + _entry("a") + _entry("b") + _entry("c")          # main issued c
    theirs = PRE + _entry("b")                                       # branch closed a
    merged, conflicts = ledger_merge.merge_entries(base, ours, theirs)
    assert conflicts == []
    assert merged == (PRE + _entry("b") + _entry("c")).rstrip("\n") + "\n"


def test_a_row_rewritten_on_one_side_wins_over_the_untouched_other():
    base = PRE + _entry("a") + _entry("b")
    ours = PRE + _entry("a") + _entry("b")
    theirs = PRE + _entry("a", "- status: awaiting-merge\n") + _entry("b")
    merged, conflicts = ledger_merge.merge_entries(base, ours, theirs)
    assert conflicts == [] and "awaiting-merge" in merged


def test_theirs_addition_keeps_its_neighbour():
    base = PRE + _entry("a") + _entry("c")
    ours = PRE + _entry("a") + _entry("c") + _entry("d")
    theirs = PRE + _entry("a") + _entry("b") + _entry("c")
    merged, _ = ledger_merge.merge_entries(base, ours, theirs)
    slugs = [s for s, _ in ledger_merge.split_entries(merged)[1]]
    assert slugs == ["## a", "## b", "## c", "## d"]


def test_the_same_slug_changed_differently_on_both_sides_is_a_conflict():
    base = PRE + _entry("a")
    ours = PRE + _entry("a", "- status: pr-open\n")
    theirs = PRE + _entry("a", "- status: parked\n")
    merged, conflicts = ledger_merge.merge_entries(base, ours, theirs)
    assert merged is None and conflicts == ["## a"]


def test_a_deleted_row_edited_on_the_other_side_is_a_conflict():
    base = PRE + _entry("a")
    ours = PRE + _entry("a", "- status: pr-open\n")
    theirs = PRE
    assert ledger_merge.merge_entries(base, ours, theirs)[1] == ["## a"]


def test_identical_changes_on_both_sides_are_not_a_conflict():
    base = PRE + _entry("a")
    both = PRE + _entry("a", "- status: done\n")
    merged, conflicts = ledger_merge.merge_entries(base, both, both)
    assert conflicts == [] and merged == both.rstrip("\n") + "\n"


def test_a_trailing_blank_line_is_layout_not_a_change():
    # the last entry gains a blank line the moment something is appended after it
    base = PRE + _entry("a").rstrip("\n") + "\n"
    ours = PRE + _entry("a") + _entry("b")
    theirs = PRE + _entry("a", "- status: closed\n").rstrip("\n") + "\n"
    merged, conflicts = ledger_merge.merge_entries(base, ours, theirs)
    assert conflicts == [] and "closed" in merged and "## b" in merged


def test_merge_entries_cli_writes_and_exits_by_outcome(tmp_path):
    for name, text in (("base", PRE + _entry("a")), ("ours", PRE + _entry("a") + _entry("b")),
                       ("theirs", PRE)):
        (tmp_path / name).write_text(text)
    out = tmp_path / "merged"
    r = subprocess.run([sys.executable, str(SCRIPT), "merge-entries", str(tmp_path / "base"),
                        str(tmp_path / "ours"), str(tmp_path / "theirs"), "--write", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert out.read_text() == (PRE + _entry("b")).rstrip("\n") + "\n"
    (tmp_path / "theirs").write_text(PRE + _entry("a", "- x\n"))
    (tmp_path / "ours").write_text(PRE + _entry("a", "- y\n"))
    r = subprocess.run([sys.executable, str(SCRIPT), "merge-entries", str(tmp_path / "base"),
                        str(tmp_path / "ours"), str(tmp_path / "theirs")],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "## a" in r.stdout


def test_the_real_registries_round_trip_through_split():
    for name in ledger_merge.ENTRY_MERGED_FILES:
        path = SCRIPT.resolve().parents[1] / name
        text = path.read_text(encoding="utf-8")
        pre, entries = ledger_merge.split_entries(text)
        assert ledger_merge.join_entries(pre, entries).rstrip("\n") == text.rstrip("\n"), name


# --- resolve: inside a real conflicted merge ------------------------------------

def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)


def _ledger_repo(tmp_path):
    """main and a branch that both touched active.md, dashboard.md and autonomy_log.md."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / ".gitattributes").write_text("autonomy_log.md merge=union\n")
    (repo / "active.md").write_text(PRE + _entry("a") + _entry("b").rstrip("\n") + "\n")
    (repo / "dashboard.md").write_text("render v0\n")
    (repo / "autonomy_log.md").write_text("| date | task |\n|---|---|\n| d0 | t0 |\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-qb", "claude/x")
    # the branch closes b (the last entry — the region main appends c into,
    # so git's line merge conflicts) and appends a row
    (repo / "active.md").write_text(PRE + _entry("a").rstrip("\n") + "\n")
    (repo / "dashboard.md").write_text("render branch\n")
    (repo / "autonomy_log.md").write_text("| date | task |\n|---|---|\n| d0 | t0 |\n| d1 | branch |\n")
    _git(repo, "commit", "-qam", "branch closes a")
    _git(repo, "checkout", "-q", "main")
    # main issues c and appends its own row
    (repo / "active.md").write_text(PRE + _entry("a") + _entry("b") + _entry("c").rstrip("\n") + "\n")
    (repo / "dashboard.md").write_text("render main\n")
    (repo / "autonomy_log.md").write_text("| date | task |\n|---|---|\n| d0 | t0 |\n| d1 | main |\n")
    _git(repo, "commit", "-qam", "main issues c")
    return repo


def test_resolve_settles_registries_by_entry_and_renders_by_main(tmp_path):
    repo = _ledger_repo(tmp_path)
    merge = subprocess.run(["git", "merge", "--no-ff", "--no-commit", "claude/x"], cwd=repo,
                           capture_output=True, text=True)
    assert merge.returncode != 0, "the fixture must actually conflict"
    resolved, unresolved = ledger_merge.resolve_conflicts(repo)
    assert unresolved == [], unresolved
    assert any(line.startswith("active.md") for line in resolved)
    assert any(line.startswith("dashboard.md") for line in resolved)
    assert (repo / "active.md").read_text() == PRE + _entry("a") + _entry("c").rstrip("\n") + "\n"
    assert (repo / "dashboard.md").read_text() == "render main\n"
    # the append-only log unioned by the attribute, never by us
    log = (repo / "autonomy_log.md").read_text()
    assert "| d1 | branch |" in log and "| d1 | main |" in log
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == ""


def test_resolve_leaves_a_real_entry_conflict_and_foreign_paths_for_a_human(tmp_path):
    repo = _ledger_repo(tmp_path)
    # main rewrites b, which the branch deleted: a genuine both-sides change
    (repo / "active.md").write_text(PRE + _entry("a") + _entry("b", "- status: pr-open\n") + _entry("c").rstrip("\n") + "\n")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "x.py").write_text("main\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "main edits a and adds a script")
    _git(repo, "checkout", "-q", "claude/x")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "x.py").write_text("branch\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "branch adds the same script")
    _git(repo, "checkout", "-q", "main")
    subprocess.run(["git", "merge", "--no-ff", "--no-commit", "claude/x"], cwd=repo, capture_output=True)
    resolved, unresolved = ledger_merge.resolve_conflicts(repo)
    assert any(u.startswith("active.md") and "## b" in u for u in unresolved), unresolved
    assert any(u.startswith("scripts/x.py") for u in unresolved), unresolved


def test_resolve_cli_exit_code_follows_unresolved(tmp_path):
    repo = _ledger_repo(tmp_path)
    subprocess.run(["git", "merge", "--no-ff", "--no-commit", "claude/x"], cwd=repo, capture_output=True)
    r = subprocess.run([sys.executable, str(SCRIPT), "resolve", "--root", str(repo)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "resolved: active.md" in r.stdout
