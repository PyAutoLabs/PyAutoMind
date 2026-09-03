"""Contract tests for the registry-integrity leg of `lifecycle.py check`.

The registry files are the first thing a task-selection pass reads, so a wrong
entry costs a whole session before anyone notices. `check` used to ignore them
completely — it never opened planned.md or parked.md and never resolved a
`prompt:` path — so it printed OK over a registry in which half the entries
pointed at files that had moved, shipped, or never existed.

Two things these tests deliberately do, matching `test_repos_sync_hygiene_coverage.py`:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template (see `test_spawn_privacy.py`), so nothing here names a real
   repository, task or prompt. It also keeps the tests hermetic — they assert
   the check's logic, not the state of whatever happens to be checked out.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
   Every condition below is driven with input that must trip it, and the
   clean-tree case proves the checks stay quiet when nothing is wrong.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def _tree(root: Path, *, draft=(), active=(), complete=(), registries=None):
    """Build a fictional Mind tree: prompt files in state folders + registries."""
    for rel in draft:
        p = root / "draft" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# fixture prompt\n")
    for name in active:
        p = root / "active" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# fixture prompt\n")
    for rel in complete:
        p = root / "complete" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# fixture record\n")
    for name, body in (registries or {}).items():
        (root / name).write_text(body)
    return root


def _entry(slug, prompt=None, extra=""):
    body = f"## {slug}\n- status: planned\n"
    if prompt is not None:
        body += f"- prompt: {prompt}\n"
    return body + extra + "\n"


# --------------------------------------------------------------------------- #
# the clean case — the checks must stay quiet
# --------------------------------------------------------------------------- #
def test_clean_tree_has_no_problems(tmp_path):
    root = _tree(
        tmp_path,
        draft=["feature/flywheel/sprocket_calibration.md"],
        active=["widget_alignment.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration",
                "draft/feature/flywheel/sprocket_calibration.md",
            ),
            "active.md": _entry("widget-alignment", "active/widget_alignment.md"),
        },
    )
    assert lifecycle.registry_problems(root) == []


def test_entry_without_a_prompt_field_is_not_a_problem(tmp_path):
    """Plenty of real entries legitimately carry no `prompt:` (release drives,
    trackers). Their absence must not be reported as unresolvable."""
    root = _tree(tmp_path, registries={"planned.md": _entry("no-prompt-here")})
    assert lifecycle.registry_problems(root) == []


# --------------------------------------------------------------------------- #
# leg 1 — the prompt path must resolve at all
# --------------------------------------------------------------------------- #
def test_unresolvable_prompt_path_is_drift(tmp_path):
    root = _tree(
        tmp_path,
        registries={
            "planned.md": _entry("ghost-task", "draft/bug/flywheel/never_written.md")
        },
    )
    problems = lifecycle.registry_problems(root)
    assert len(problems) == 1
    assert "does not resolve" in problems[0]
    assert "ghost-task" in problems[0]


# --------------------------------------------------------------------------- #
# leg 2 — resolving only via the legacy fallback is still drift
# --------------------------------------------------------------------------- #
def test_legacy_path_resolving_via_fallback_is_drift(tmp_path):
    """The pre-lifecycle `PyAutoMind/<work-type>/<target>/` form still resolves
    for $start-dev, but leaving it in the registry hides where the file is."""
    root = _tree(
        tmp_path,
        draft=["bug/flywheel/sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration",
                "PyAutoMind/bug/flywheel/sprocket_calibration.md",
            )
        },
    )
    problems = lifecycle.registry_problems(root)
    assert len(problems) == 1
    assert "legacy prompt path" in problems[0]
    # the message must name where it actually landed, or it is not actionable
    assert "draft/bug/flywheel/sprocket_calibration.md" in problems[0]


# --------------------------------------------------------------------------- #
# leg 3 — state contradictions
# --------------------------------------------------------------------------- #
def test_planned_entry_whose_prompt_is_in_active_is_drift(tmp_path):
    """planned.md means "scoped, not started". A prompt already advanced to
    active/ means the task is in flight and the registry is lying."""
    root = _tree(
        tmp_path,
        active=["sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration", "active/sprocket_calibration.md"
            )
        },
    )
    problems = lifecycle.registry_problems(root)
    assert len(problems) == 1
    assert "prompt is in active/" in problems[0]


def test_entry_whose_prompt_is_a_complete_record_is_drift(tmp_path):
    """The expensive class: work that shipped but is still listed as pending."""
    root = _tree(
        tmp_path,
        complete=["2031/07/sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration", "draft/bug/flywheel/sprocket_calibration.md"
            )
        },
    )
    problems = lifecycle.registry_problems(root)
    assert len(problems) == 1
    assert "shipped but still listed" in problems[0]


def test_parked_accepts_both_draft_and_active_prompts(tmp_path):
    """parked.md holds tasks that were merely scoped (prompt still in draft/)
    AND tasks that were started then parked (prompt already in active/).
    Treating it like planned.md flags every genuinely-parked task."""
    root = _tree(
        tmp_path,
        draft=["feature/flywheel/scoped_then_parked.md"],
        active=["started_then_parked.md"],
        registries={
            "parked.md": (
                _entry(
                    "scoped-then-parked",
                    "draft/feature/flywheel/scoped_then_parked.md",
                )
                + _entry("started-then-parked", "active/started_then_parked.md")
            )
        },
    )
    assert lifecycle.registry_problems(root) == []


# --------------------------------------------------------------------------- #
# leg 4 — a slug belongs to exactly one registry
# --------------------------------------------------------------------------- #
def test_slug_in_two_registries_is_drift(tmp_path):
    root = _tree(
        tmp_path,
        draft=["feature/flywheel/sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration",
                "draft/feature/flywheel/sprocket_calibration.md",
            ),
            "parked.md": _entry(
                "sprocket-calibration",
                "draft/feature/flywheel/sprocket_calibration.md",
            ),
        },
    )
    problems = lifecycle.registry_problems(root)
    assert any("listed in two registries" in p for p in problems)


# --------------------------------------------------------------------------- #
# parser contracts — these bit during development, so they are pinned
# --------------------------------------------------------------------------- #
def test_nested_repo_bullets_are_not_read_as_fields(tmp_path):
    """`  - SomeRepo: some-branch` under `repos:` is a VALUE, not a field.
    Reading indented bullets as fields invents keys out of branch names."""
    body = _entry(
        "sprocket-calibration",
        "draft/feature/flywheel/sprocket_calibration.md",
        extra="- repos:\n  - FlywheelRepo: feature/sprocket\n  - GadgetRepo: feature/sprocket\n",
    )
    (tmp_path / "planned.md").write_text(body)
    entries = lifecycle.registry_entries(tmp_path / "planned.md")
    assert len(entries) == 1
    _, fields = entries[0]
    assert set(fields) == {"status", "prompt", "repos"}
    assert "FlywheelRepo" not in fields


def test_trailing_parenthetical_after_the_path_is_tolerated(tmp_path):
    """Entries annotate the path with prose: `... .md (carries the table)`.
    The path is the first token; the annotation must not break resolution."""
    root = _tree(
        tmp_path,
        draft=["bug/flywheel/sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration",
                "draft/bug/flywheel/sprocket_calibration.md (carries the phase table)",
            )
        },
    )
    assert lifecycle.registry_problems(root) == []


# --------------------------------------------------------------------------- #
# the online leg — tracking-issue state
#
# `fetch` is injected so these stay hermetic: no network, no `gh`, no live repo.
# --------------------------------------------------------------------------- #
GHOST_ISSUE = "https://github.com/FictionalOrg/FlywheelRepo/issues/17"
OTHER_ISSUE = "https://github.com/FictionalOrg/FlywheelRepo/issues/18"


def _states(mapping):
    return lambda urls: {u: mapping.get(u, "unknown") for u in urls}


def test_closed_tracking_issue_on_a_pending_entry_is_drift(tmp_path):
    """The class no offline check can see: the entry reads as pending, the work
    is finished, and only GitHub knows."""
    (tmp_path / "planned.md").write_text(
        _entry("sprocket-calibration", extra=f"- issue: {GHOST_ISSUE}\n")
    )
    problems = lifecycle.issue_problems(tmp_path, fetch=_states({GHOST_ISSUE: "closed"}))
    assert len(problems) == 1
    assert "CLOSED" in problems[0]
    assert "sprocket-calibration" in problems[0]


def test_open_tracking_issue_is_not_drift(tmp_path):
    (tmp_path / "planned.md").write_text(
        _entry("sprocket-calibration", extra=f"- issue: {GHOST_ISSUE}\n")
    )
    assert lifecycle.issue_problems(tmp_path, fetch=_states({GHOST_ISSUE: "open"})) == []


def test_prose_instead_of_an_issue_url_is_skipped(tmp_path):
    """Real entries carry '(no issue — a human-authorized release drive)' and
    'NEEDS A FRESH ISSUE — ...'. There is nothing to query; not a finding."""
    body = (
        _entry("release-drive", extra="- issue: (no issue — a release drive)\n")
        + _entry("needs-one", extra="- issue: NEEDS A FRESH ISSUE — file at start_dev\n")
    )
    (tmp_path / "active.md").write_text(body)
    assert lifecycle.registry_issue_refs(tmp_path) == []
    assert lifecycle.issue_problems(tmp_path, fetch=_states({})) == []


def test_epic_field_is_treated_as_a_tracking_ref(tmp_path):
    (tmp_path / "planned.md").write_text(
        _entry("phased-task", extra=f"- epic: {GHOST_ISSUE} (the public watch point)\n")
    )
    problems = lifecycle.issue_problems(tmp_path, fetch=_states({GHOST_ISSUE: "closed"}))
    assert len(problems) == 1


def test_merged_pr_links_are_not_treated_as_tracking_refs(tmp_path):
    """A shipped task's library-pr/workspace-pr are merged by definition.
    Reporting those as closed would bury the real signal in noise."""
    body = _entry(
        "sprocket-calibration",
        extra=(
            f"- issue: {GHOST_ISSUE}\n"
            "- library-pr: https://github.com/FictionalOrg/FlywheelRepo/pull/99\n"
            "- workspace-pr: https://github.com/FictionalOrg/GadgetRepo/pull/12\n"
        ),
    )
    (tmp_path / "active.md").write_text(body)
    refs = lifecycle.registry_issue_refs(tmp_path)
    assert [r[2] for r in refs] == [GHOST_ISSUE]


def test_draft_citing_a_closed_issue_is_advisory(tmp_path):
    """draft/ is backlog no check grades, and it carries shipped work too. A
    closed cited issue is worth a look — but NOT drift, because a draft usually
    cites an issue as context ("Once #480 is fixed…"), so closed can mean newly
    unblocked rather than finished."""
    d = tmp_path / "draft" / "feature" / "flywheel"
    d.mkdir(parents=True)
    (d / "sprocket_calibration.md").write_text(f"Once {GHOST_ISSUE} is fixed, do X.\n")
    notes = lifecycle.draft_issue_notes(tmp_path, fetch=_states({GHOST_ISSUE: "closed"}))
    assert len(notes) == 1
    assert "shipped, or newly unblocked?" in notes[0]


def test_draft_with_an_open_issue_is_silent(tmp_path):
    d = tmp_path / "draft" / "feature" / "flywheel"
    d.mkdir(parents=True)
    (d / "sprocket_calibration.md").write_text(f"Blocked on {GHOST_ISSUE}.\n")
    assert lifecycle.draft_issue_notes(tmp_path, fetch=_states({GHOST_ISSUE: "open"})) == []


def test_drafts_are_not_mixed_into_registry_drift(tmp_path):
    """The advisory must never leak into `issue_problems`, which is the gate."""
    d = tmp_path / "draft" / "feature" / "flywheel"
    d.mkdir(parents=True)
    (d / "sprocket_calibration.md").write_text(f"Once {GHOST_ISSUE} is fixed.\n")
    assert lifecycle.issue_problems(tmp_path, fetch=_states({GHOST_ISSUE: "closed"})) == []


def test_missing_gh_propagates_rather_than_reporting_all_clear(tmp_path):
    """"gh is not installed" must never be mistaken for "no findings" — a check
    that silently could not run is worse than one that fails loudly."""
    import pytest

    (tmp_path / "planned.md").write_text(
        _entry("sprocket-calibration", extra=f"- issue: {GHOST_ISSUE}\n")
    )

    def _no_gh(urls):
        raise lifecycle.GhUnavailable

    with pytest.raises(lifecycle.GhUnavailable):
        lifecycle.issue_problems(tmp_path, fetch=_no_gh)


def test_unreadable_issue_state_is_reported_not_swallowed(tmp_path):
    """A deleted repo, a revoked token or a network failure must surface — a
    silent 'no findings' from a check that could not run is the worst outcome."""
    (tmp_path / "planned.md").write_text(
        _entry("sprocket-calibration", extra=f"- issue: {OTHER_ISSUE}\n")
    )
    problems = lifecycle.issue_problems(tmp_path, fetch=_states({}))
    assert len(problems) == 1
    assert "could not read issue state" in problems[0]


# --------------------------------------------------------------------------- #
# the default fetcher itself
#
# Everything above injects `fetch`, which is what keeps those tests hermetic —
# but it also means the real `_gh_issue_states` shim, the thing that runs on a
# machine that HAS gh, was never executed by the suite. These tests drive it
# with `subprocess.run` stubbed, so the argv, the parsing and both failure
# modes are pinned without a network or a `gh` binary.
#
# `_gh_issue_states` does `import subprocess` inside the function body, which
# rebinds the same module object from sys.modules — so patching the attribute
# on the real module reaches it.
# --------------------------------------------------------------------------- #
class _Completed:
    """Stand-in for subprocess.CompletedProcess."""

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _stub_run(monkeypatch, handler):
    """Patch subprocess.run, recording every argv the shim builds."""
    import subprocess

    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return handler(argv)

    monkeypatch.setattr(subprocess, "run", fake_run)
    return calls


def test_default_fetcher_builds_the_gh_argv_and_parses_state(monkeypatch):
    """The happy path: one `gh api` call per URL, `.state` jq-extracted, and
    the trailing newline gh emits stripped off."""
    calls = _stub_run(monkeypatch, lambda argv: _Completed(stdout="open\n"))

    states = lifecycle._gh_issue_states([GHOST_ISSUE])

    assert states == {GHOST_ISSUE: "open"}
    assert calls == [
        [
            "gh",
            "api",
            "repos/FictionalOrg/FlywheelRepo/issues/17",
            "--jq",
            ".state",
        ]
    ]


def test_default_fetcher_falls_back_to_http_when_gh_is_missing(monkeypatch):
    """No `gh` (cloud/web sessions, bare CI images) must not mean "could not
    run": the fetcher falls back to the stdlib HTTPS path and still returns
    real states. The HTTP helper is stubbed so the test stays offline."""

    def _missing(argv):
        raise FileNotFoundError(2, "No such file or directory: 'gh'")

    _stub_run(monkeypatch, _missing)

    http_calls = []

    def _fake_http(owner, repo, kind, num):
        http_calls.append((owner, repo, kind, num))
        return "open"

    monkeypatch.setattr(lifecycle, "_http_api_state", _fake_http)

    assert lifecycle._gh_issue_states([GHOST_ISSUE]) == {GHOST_ISSUE: "open"}
    assert http_calls == [("FictionalOrg", "FlywheelRepo", "issues", "17")]


def test_default_fetcher_reports_a_failed_call_as_unreadable(monkeypatch):
    """gh ran and said no (404, revoked token, rate limit). That is a finding,
    not a crash — and `issue_problems` grades any non-'open' state, so the
    string it stores must not be mistaken for 'closed'."""
    _stub_run(
        monkeypatch,
        lambda argv: _Completed(
            returncode=1,
            stderr="gh: Not Found (HTTP 404)\n",
        ),
    )

    states = lifecycle._gh_issue_states([GHOST_ISSUE])

    assert states[GHOST_ISSUE].startswith("unreadable: ")
    assert "HTTP 404" in states[GHOST_ISSUE]
    assert states[GHOST_ISSUE] != "closed"


def test_default_fetcher_survives_a_failure_with_no_stderr(monkeypatch):
    """The `or ["error"]` fallback: a non-zero exit with empty stderr must not
    IndexError its way out of the whole check."""
    _stub_run(monkeypatch, lambda argv: _Completed(returncode=1, stderr="   \n"))

    assert lifecycle._gh_issue_states([GHOST_ISSUE]) == {GHOST_ISSUE: "unreadable: error"}


def test_default_fetcher_skips_anything_that_is_not_an_issue_url(monkeypatch):
    """Guards the loop's `if not m: continue` — a malformed entry costs no
    subprocess call and contributes no state, rather than querying nonsense."""
    calls = _stub_run(monkeypatch, lambda argv: _Completed(stdout="open\n"))

    states = lifecycle._gh_issue_states(["(no issue — a release drive)"])

    assert states == {}
    assert calls == []


def test_default_fetcher_reads_each_url_in_a_mixed_batch(monkeypatch):
    """Two URLs, different answers — the shim must key states by URL rather
    than collapsing or reusing the last result."""

    def _by_number(argv):
        return _Completed(stdout="closed\n" if argv[2].endswith("/18") else "open\n")

    _stub_run(monkeypatch, _by_number)

    assert lifecycle._gh_issue_states([GHOST_ISSUE, OTHER_ISSUE]) == {
        GHOST_ISSUE: "open",
        OTHER_ISSUE: "closed",
    }


# --------------------------------------------------------------------------- #
# the online leg — `status: pr-open` PR state
#
# The crashed-ship signature: the PR merged but the shipping session died
# before the bookkeeping, so the tracking issue is still OPEN and the issue
# leg above stays green. The merged PR is the only signal that survives.
# --------------------------------------------------------------------------- #
GHOST_PR = "https://github.com/FictionalOrg/FlywheelRepo/pull/42"


def test_merged_pr_on_a_pr_open_entry_is_drift(tmp_path):
    (tmp_path / "active.md").write_text(
        _entry("sprocket-calibration").replace(
            "- status: planned", f"- status: pr-open ({GHOST_PR})")
    )
    problems = lifecycle.pr_problems(tmp_path, fetch=_states({GHOST_PR: "merged"}))
    assert len(problems) == 1
    assert "MERGED" in problems[0]
    assert "sprocket-calibration" in problems[0]


def test_open_pr_on_a_pr_open_entry_is_not_drift(tmp_path):
    (tmp_path / "active.md").write_text(
        _entry("sprocket-calibration").replace(
            "- status: planned", f"- status: pr-open ({GHOST_PR})")
    )
    assert lifecycle.pr_problems(tmp_path, fetch=_states({GHOST_PR: "open"})) == []


def test_closed_unmerged_pr_on_a_pr_open_entry_is_drift(tmp_path):
    """A PR closed without merging is not shipped — but the entry still claims
    an open PR, so its state is wrong either way and needs a human."""
    (tmp_path / "active.md").write_text(
        _entry("sprocket-calibration").replace(
            "- status: planned", f"- status: pr-open ({GHOST_PR})")
    )
    problems = lifecycle.pr_problems(tmp_path, fetch=_states({GHOST_PR: "closed"}))
    assert len(problems) == 1
    assert "CLOSED" in problems[0]


def test_pr_urls_outside_the_status_field_are_not_tracking_refs(tmp_path):
    """A shipped task's `library-pr:`/`workspace-pr:` history, or a PR cited in
    prose, is not a claim of in-flight state — only `status: pr-open` is."""
    body = _entry(
        "sprocket-calibration",
        extra=(
            f"- library-pr: {GHOST_PR}\n"
            f"- notes: superseded by {GHOST_PR} long ago\n"
        ),
    )
    (tmp_path / "active.md").write_text(body)
    assert lifecycle.registry_pr_refs(tmp_path) == []
    assert lifecycle.pr_problems(tmp_path, fetch=_states({})) == []


def test_pr_state_fetcher_builds_the_pulls_argv_with_merged_jq(monkeypatch):
    """PRs need the merged_at disambiguation: GitHub's `state` is "closed" for
    both a merged and an abandoned PR, and the two mean opposite things here."""
    calls = _stub_run(monkeypatch, lambda argv: _Completed(stdout="merged\n"))

    states = lifecycle._gh_pr_states([GHOST_PR])

    assert states == {GHOST_PR: "merged"}
    assert calls == [
        [
            "gh",
            "api",
            "repos/FictionalOrg/FlywheelRepo/pulls/42",
            "--jq",
            'if .merged_at then "merged" else .state end',
        ]
    ]


# --------------------------------------------------------------------------- #
# active/ strays — files the lifecycle tooling cannot see
#
# check/orphans/dashboard all scan active/*.md, top level only. Five completed
# leftovers (three with months-old records) hid in active/ subdirectories and
# as stray scripts until the 2026-08-19 sweep; this gate makes that class
# visible hermetically.
# --------------------------------------------------------------------------- #
def test_subdirectory_prompt_and_stray_script_are_strays(tmp_path):
    root = _tree(
        tmp_path,
        active=["tracked_task.md"],
        registries={"active.md": _entry("tracked-task", prompt="active/tracked_task.md")},
    )
    sub = root / "active" / "legacy_target"
    sub.mkdir()
    (sub / "old_prompt.md").write_text("# pre-migration leftover\n")
    (root / "active" / "ground_truth.py").write_text("print('retired scratch')\n")

    strays = [str(p.relative_to(root)) for p in lifecycle.active_strays(root)]
    assert strays == ["active/ground_truth.py", "active/legacy_target/old_prompt.md"]


def test_top_level_prompts_are_not_strays(tmp_path):
    root = _tree(
        tmp_path,
        active=["tracked_task.md"],
        registries={"active.md": _entry("tracked-task", prompt="active/tracked_task.md")},
    )
    assert lifecycle.active_strays(root) == []


# --------------------------------------------------------------------------- #
# the mirror direction — active/ prompts no registry claims
# --------------------------------------------------------------------------- #
def test_unclaimed_active_prompt_is_an_orphan(tmp_path):
    root = _tree(
        tmp_path,
        active=["sprocket_calibration.md", "nobody_tracks_this.md"],
        registries={
            "active.md": _entry(
                "sprocket-calibration", "active/sprocket_calibration.md"
            )
        },
    )
    orphans = [p.name for p in lifecycle.orphan_prompts(root)]
    assert orphans == ["nobody_tracks_this.md"]


def test_slug_match_claims_a_prompt_without_a_prompt_field(tmp_path):
    """Many entries predate the `prompt:` convention and identify their file by
    name alone. Requiring `prompt:` would report every one of them as an orphan."""
    root = _tree(
        tmp_path,
        active=["sprocket_calibration.md"],
        registries={"active.md": _entry("sprocket-calibration")},
    )
    assert lifecycle.orphan_prompts(root) == []


def test_a_parked_entry_also_claims_its_active_prompt(tmp_path):
    """Started-then-parked work keeps its prompt in active/ while it is listed
    in parked.md — that prompt is tracked, not orphaned."""
    root = _tree(
        tmp_path,
        active=["started_then_parked.md"],
        registries={
            "parked.md": _entry(
                "started-then-parked", "active/started_then_parked.md"
            )
        },
    )
    assert lifecycle.orphan_prompts(root) == []


def test_archive_material_does_not_satisfy_a_prompt_path(tmp_path):
    """complete/archive/ holds retired non-record material and is skipped
    everywhere else in this module; a shelved copy must not make a missing
    prompt look present."""
    root = _tree(
        tmp_path,
        complete=["archive/shelved/sprocket_calibration.md"],
        registries={
            "planned.md": _entry(
                "sprocket-calibration", "draft/bug/flywheel/sprocket_calibration.md"
            )
        },
    )
    problems = lifecycle.registry_problems(root)
    assert len(problems) == 1
    assert "does not resolve" in problems[0]


# --------------------------------------------------------------------------- #
# declared draft gates (`Closes-when:` / `Blocked-by:`)
#
# The 2026-08-09 draft/ sweep found five prompts whose stated gate had closed,
# and the two readings are OPPOSITE: a satisfied "epic closes when #N" means the
# prompt is DONE, a satisfied "blocked until #N merges" means it is READY. Prose
# cannot be graded, so `--drafts` had to report both as one ambiguous question.
# --------------------------------------------------------------------------- #
def _draft(root: Path, rel: str, body: str) -> Path:
    p = root / "draft" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return p


GATE_ISSUE = "https://github.com/FictionalOrg/FlywheelRepo/issues/77"
GATE_ISSUE_2 = "https://github.com/FictionalOrg/GadgetRepo/issues/88"


def test_closes_when_gate_closed_reads_as_shipped(tmp_path):
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nCloses-when: {GATE_ISSUE}\n")
    notes = lifecycle.draft_gate_notes(tmp_path, fetch=_states({GATE_ISSUE: "closed"}))
    assert len(notes["shipped"]) == 1
    assert "likely shipped" in notes["shipped"][0]
    assert notes["unblocked"] == []


def test_blocked_by_gate_closed_reads_as_unblocked(tmp_path):
    """The opposite reading — and the whole reason the two keys are distinct."""
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nBlocked-by: {GATE_ISSUE}\n")
    notes = lifecycle.draft_gate_notes(tmp_path, fetch=_states({GATE_ISSUE: "closed"}))
    assert len(notes["unblocked"]) == 1
    assert "ready to start" in notes["unblocked"][0]
    assert notes["shipped"] == []


def test_open_gate_is_silent(tmp_path):
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nBlocked-by: {GATE_ISSUE}\n")
    notes = lifecycle.draft_gate_notes(tmp_path, fetch=_states({GATE_ISSUE: "open"}))
    assert notes == {"shipped": [], "unblocked": [], "partial": [], "unreadable": []}


def test_repo_hash_shorthand_is_read_as_a_gate(tmp_path):
    """Prompts write `Repo#123`, not URLs. A URL-only extractor found 2 refs
    across the real backlog where the shorthand form found 8."""
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           "# Sprocket\n\nBlocked-by: FlywheelRepo#77   # the loader fix\n")
    refs = lifecycle.draft_gate_refs(tmp_path)
    assert len(refs) == 1
    assert refs[0][1] == "blocked-by"
    assert refs[0][2].endswith("/FlywheelRepo/issues/77")


def test_partly_closed_gates_are_not_reported_as_ready(tmp_path):
    """A prompt blocked on three PRs is unblocked when the LAST one lands.
    Reporting per-reference would claim 'ready to start' while still blocked."""
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nBlocked-by: {GATE_ISSUE}, {GATE_ISSUE_2}\n")
    notes = lifecycle.draft_gate_notes(
        tmp_path, fetch=_states({GATE_ISSUE: "closed", GATE_ISSUE_2: "open"}))
    assert notes["unblocked"] == []
    assert len(notes["partial"]) == 1
    assert "1 of 2" in notes["partial"][0]


def test_all_gates_closed_reports_once_not_per_reference(tmp_path):
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nBlocked-by: {GATE_ISSUE}, {GATE_ISSUE_2}\n")
    notes = lifecycle.draft_gate_notes(
        tmp_path, fetch=_states({GATE_ISSUE: "closed", GATE_ISSUE_2: "closed"}))
    assert len(notes["unblocked"]) == 1


def test_a_fenced_example_is_documentation_not_a_declaration(tmp_path):
    """The prompt that PROPOSED these keys shows them in a ```markdown block.
    Reading that as a real gate would invent a finding out of documentation."""
    _draft(tmp_path, "feature/mind/gate_keys.md",
           "# Propose gate keys\n\n"
           "Proposal:\n\n"
           "```markdown\n"
           f"Closes-when: {GATE_ISSUE}\n"
           "```\n\n"
           "That is the idea.\n")
    assert lifecycle.draft_gate_refs(tmp_path) == []


def test_declared_gates_are_not_repeated_as_ambiguous_advisories(tmp_path):
    """`--drafts` asks 'shipped, or newly unblocked?' precisely because prose
    cannot say. A prompt that DECLARED which it means must not be asked again."""
    _draft(tmp_path, "bug/flywheel/sprocket.md",
           f"# Sprocket\n\nBlocked-by: {GATE_ISSUE}\n\nContext: {GATE_ISSUE}\n")
    fetch = _states({GATE_ISSUE: "closed"})
    assert lifecycle.draft_gate_notes(tmp_path, fetch=fetch)["unblocked"]
    assert lifecycle.draft_issue_notes(tmp_path, fetch=fetch) == []


def test_an_undeclared_draft_still_gets_the_ambiguous_advisory(tmp_path):
    """The fallback must survive: most prompts carry no gate key at all."""
    _draft(tmp_path, "bug/flywheel/widget.md", f"# Widget\n\nFollow-up to {GATE_ISSUE}\n")
    notes = lifecycle.draft_issue_notes(tmp_path, fetch=_states({GATE_ISSUE: "closed"}))
    assert len(notes) == 1
    assert "shipped, or newly unblocked?" in notes[0]


# --------------------------------------------------------------------------- #
# the PR ledger: `library-pr:` / `workspace-pr:` / `pending-release:`
#
# The keys were written by ship_library and read by /prm long before anything
# validated them, so a row could declare `status: awaiting-merge` and name no
# PR at all. Fictional repos throughout (see the module docstring).
# --------------------------------------------------------------------------- #
def _as_root(monkeypatch, root: Path):
    """Point `cmd_check`'s module-level paths at a fixture tree.

    `check` reads ROOT/ACTIVE_MD/COMPLETE_DIR/ACTIVE_DIR as globals (it is a
    CLI, not a library), so a hermetic run has to rebind them."""
    monkeypatch.setattr(lifecycle, "ROOT", root)
    monkeypatch.setattr(lifecycle, "ACTIVE_MD", root / "active.md")
    monkeypatch.setattr(lifecycle, "ACTIVE_DIR", root / "active")
    monkeypatch.setattr(lifecycle, "COMPLETE_DIR", root / "complete")
    monkeypatch.setattr(lifecycle, "ARCHIVE_DIR", root / "complete" / "archive")


GADGET_PR = "https://github.com/ExampleOrg/Gadgets/pull/12"
WIDGET_PR = "https://github.com/ExampleOrg/Widgets/pull/34"
SPROCKET_PR = "https://github.com/ExampleOrg/Sprockets/pull/56"


def test_a_row_claiming_open_prs_and_naming_none_is_drift(tmp_path):
    _tree(tmp_path, registries={
        "active.md": ("# Active\n\n## flywheel-rebuild\n"
                      "- status: library-shipped, awaiting-merge\n")})
    problems = lifecycle.pr_key_problems(tmp_path)
    assert len(problems) == 1
    assert "flywheel-rebuild" in problems[0]
    assert "library-pr" in problems[0]


def test_the_pr_keys_are_repeatable_one_line_each(tmp_path):
    """A task may ship several PRs of one kind; `registry_entries` keeps only
    the first occurrence of a key, so the check needs its own repeat-tolerant
    parse or it would read a three-PR row as a one-PR row."""
    _tree(tmp_path, registries={
        "active.md": ("# Active\n\n## flywheel-rebuild\n"
                      "- status: library-shipped, awaiting-merge\n"
                      f"- library-pr: {GADGET_PR}\n"
                      f"- library-pr: {WIDGET_PR}\n"
                      f"- workspace-pr: {SPROCKET_PR}\n")})
    assert lifecycle.pr_key_problems(tmp_path) == []
    _, multi = lifecycle.registry_multi(tmp_path / "active.md")[0]
    assert lifecycle.pr_urls(multi["library-pr"]) == [GADGET_PR, WIDGET_PR]


def test_the_older_single_line_comma_form_still_counts(tmp_path):
    """Rows written before the key was schematised must not start failing."""
    _tree(tmp_path, registries={
        "active.md": ("# Active\n\n## flywheel-rebuild\n"
                      "- status: shipped\n"
                      f"- library-pr: {GADGET_PR}, {WIDGET_PR}\n")})
    assert lifecycle.pr_key_problems(tmp_path) == []


def test_a_row_still_in_development_needs_no_pr_key(tmp_path):
    """The rule keys off the status DECLARING the PRs exist — an in-flight row
    that has not shipped anything yet is not withholding a thing."""
    _tree(tmp_path, registries={
        "active.md": ("# Active\n\n## flywheel-rebuild\n"
                      "- status: library-dev\n")})
    assert lifecycle.pr_key_problems(tmp_path) == []


def test_the_pr_key_rule_is_wired_into_check(tmp_path, monkeypatch, capsys):
    """`check` must exit 1 on it — a rule nothing runs is decoration."""
    _tree(tmp_path, registries={
        "active.md": ("# Active\n\n## flywheel-rebuild\n"
                      "- status: awaiting-merge\n")})
    _as_root(monkeypatch, tmp_path)
    assert lifecycle.cmd_check(None) == 1
    assert "flywheel-rebuild" in capsys.readouterr().out


def _record(root: Path, rel: str, body: str):
    p = root / "complete" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return p


def test_a_long_uncleared_pending_release_is_a_warning_not_drift(tmp_path):
    _record(tmp_path, "2026/01/flywheel_rebuild.md",
            "## flywheel-rebuild\n"
            "- completed: 2026-01-01\n"
            f"- pending-release: Gadgets@{GADGET_PR}\n")
    notes = lifecycle.pending_release_problems(tmp_path, today="2026-03-01")
    assert len(notes) == 1 and "uncleared" in notes[0]
    # Fresh enough is silent: the key's whole meaning is "not released yet".
    assert lifecycle.pending_release_problems(tmp_path, today="2026-01-10") == []


def test_the_appended_original_prompt_is_not_read_as_the_records_own_fields(tmp_path):
    """`lifecycle.py record` appends the starting prompt verbatim, and that
    prompt may quote another task's keys. Reading past the boundary would
    invent a pending release the record never had."""
    _record(tmp_path, "2026/01/flywheel_rebuild.md",
            "## flywheel-rebuild\n"
            "- completed: 2026-01-01\n"
            "- summary: shipped clean\n"
            "\n## Original prompt\n\n"
            f"- pending-release: Gadgets@{GADGET_PR}\n")
    assert lifecycle.pending_release_problems(tmp_path, today="2026-06-01") == []


def test_check_reports_a_stale_pending_release_and_still_exits_zero(tmp_path,
                                                                    monkeypatch,
                                                                    capsys):
    _record(tmp_path, "2026/01/flywheel_rebuild.md",
            "## flywheel-rebuild\n"
            "- completed: 2026-01-01\n"
            f"- pending-release: Gadgets@{GADGET_PR}\n")
    _as_root(monkeypatch, tmp_path)
    assert lifecycle.cmd_check(None) == 0
    out = capsys.readouterr().out
    assert "warning" in out and "pending-release" in out


# --------------------------------------------------------------------------- #
# the batch ledger
#
# `batches/<date>-<slot>.md` is the record of one unattended shift and the
# evidence base the review-minute budget is calibrated from. Nothing checked
# it: a member could cite a prompt path nobody ever wrote, and a closed record
# could carry no measured review cost at all.
# --------------------------------------------------------------------------- #
def _batch_record(root: Path, name: str, *members, keys=""):
    d = root / "batches"
    d.mkdir(parents=True, exist_ok=True)
    body = ["# Batch " + name, "",
            "- dispatched: 2026-01-01T17:40Z",
            "- review-at: 2026-01-02T08:00Z",
            "- members:"]
    body += list(members)
    if keys:
        body.append(keys)
    body += ["- notes: |", "    - members: this line is prose, not a key"]
    (d / f"{name}.md").write_text("\n".join(body) + "\n")
    return d / f"{name}.md"


MEMBER = ("  - widget-polish: draft/feature/widgets/polish.md — glance — 3 — "
          "DELIVERED (Gadgets#12, 4/4 checks green)")


def test_a_member_citing_a_prompt_that_was_never_here_is_drift(tmp_path):
    """The member's question and its pre-registered witness are read from that
    file at collect. A path nobody ever wrote makes the member unreadable, and
    the record wrong about what it dispatched."""
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    problems = lifecycle.batch_member_problems(tmp_path)
    assert len(problems) == 1
    assert "widget-polish" in problems[0]
    assert "draft/feature/widgets/polish.md" in problems[0]


def test_a_member_prompt_still_in_draft_is_not_drift(tmp_path):
    _tree(tmp_path, draft=("feature/widgets/polish.md",))
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_a_member_prompt_issued_into_active_is_not_drift(tmp_path):
    """The record names where the prompt was AT DISPATCH; the lifecycle moves
    it the moment the issue opens."""
    _tree(tmp_path, active=("polish.md",))
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_a_member_prompt_retired_into_complete_is_not_drift(tmp_path):
    _tree(tmp_path, complete=("2026/01/polish.md",))
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_a_prompt_absorbed_into_its_record_is_not_drift(tmp_path):
    """A completion record is filed under the TASK's name and the prompt file
    is gone, so the member's path resolves nowhere on disk. Git is the only
    thing that tells that apart from a path nobody ever wrote."""
    import shutil
    import subprocess
    if not shutil.which("git"):
        import pytest
        pytest.skip("no git")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "t"],
                   check=True)
    _tree(tmp_path, draft=("feature/widgets/polish.md",))
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "filed"],
                   check=True)
    (tmp_path / "draft" / "feature" / "widgets" / "polish.md").unlink()
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_a_member_line_that_is_not_the_grammar_is_left_alone(tmp_path):
    """A hand submission has a sentence where the path goes. Reporting it as a
    missing prompt would be reporting the wrong thing."""
    _batch_record(tmp_path, "2026-01-01-pm",
                  "  - hand-run-42: (no prompt — hand submission) — notify — "
                  "1 — UNREVIEWED, carried to the next packet")
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_prose_below_the_members_block_is_not_a_member(tmp_path):
    """The member list ends at the first key that is not `members:` — the
    `notes: |` body of every real record quotes member-shaped lines."""
    _tree(tmp_path, draft=("feature/widgets/polish.md",))
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys="- collected: 2026-01-02T08:30Z")
    assert lifecycle.batch_member_problems(tmp_path) == []


def test_the_agents_page_is_not_a_batch_record(tmp_path):
    (tmp_path / "batches").mkdir()
    (tmp_path / "batches" / "AGENTS.md").write_text(
        "# Batch records\n\n- members:\n" + MEMBER + "\n")
    assert lifecycle.batch_records(tmp_path) == []


def test_a_closed_record_with_no_measured_review_cost_warns(tmp_path):
    """`review-minutes-actual:` is "the only calibration there is" — without it
    the budget every batch is planned against never improves."""
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys="- review: batches/reviews/2026-01-01-pm.md")
    warnings = lifecycle.batch_record_warnings(tmp_path)
    assert len(warnings) == 1
    assert "review-minutes-actual" in warnings[0]


def test_the_placeholder_counts_as_no_measurement(tmp_path):
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys=("- reviewed-at: 2026-01-02T08:30Z\n"
                        "- review-minutes-actual: (not given)"))
    assert len(lifecycle.batch_record_warnings(tmp_path)) == 1


def test_a_measured_review_cost_silences_the_warning(tmp_path):
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys=("- review: batches/reviews/2026-01-01-pm.md\n"
                        "- review-minutes-actual: 38"))
    assert lifecycle.batch_record_warnings(tmp_path) == []


def test_an_open_slot_is_not_warned_about(tmp_path):
    """The number is written after the review. A record whose review has not
    landed is not missing anything."""
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER)
    assert lifecycle.batch_record_warnings(tmp_path) == []


def test_check_fails_on_a_bad_member_path_and_warns_on_the_minutes(
        tmp_path, monkeypatch, capsys):
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys="- review: batches/reviews/2026-01-01-pm.md")
    _as_root(monkeypatch, tmp_path)
    assert lifecycle.cmd_check(None) == 1
    out = capsys.readouterr().out
    assert "widget-polish" in out
    assert "warning" in out and "review-minutes-actual" in out


def test_check_stays_quiet_on_a_clean_batch_ledger(tmp_path, monkeypatch,
                                                   capsys):
    _tree(tmp_path, draft=("feature/widgets/polish.md",))
    _batch_record(tmp_path, "2026-01-01-pm", MEMBER,
                  keys=("- review: batches/reviews/2026-01-01-pm.md\n"
                        "- review-minutes-actual: 38"))
    _as_root(monkeypatch, tmp_path)
    assert lifecycle.cmd_check(None) == 0
    assert capsys.readouterr().out.strip() == "lifecycle check: OK"
