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


def test_default_fetcher_raises_gh_unavailable_when_gh_is_missing(monkeypatch):
    """The one error the command turns into "could not run" rather than a
    finding — so it must be the exception type, not a state string."""
    import pytest

    def _missing(argv):
        raise FileNotFoundError(2, "No such file or directory: 'gh'")

    _stub_run(monkeypatch, _missing)

    with pytest.raises(lifecycle.GhUnavailable):
        lifecycle._gh_issue_states([GHOST_ISSUE])


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
