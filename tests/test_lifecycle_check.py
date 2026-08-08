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
