"""Contract tests for `lifecycle.py close` — the Mind-side close-out verb.

Shipping a task ends with a fixed sequence of chores (write the record, remove
the prompt, drop the registry entry, feed the tier-`notify` shadow window,
regenerate `complete/index.md`, repoint what the merge falsified). Each one was
prose in a skill, which is to say each one was skippable; two of them were
folded into `record` after exactly that, each following its own drift-alarm
email storm. `close` is the composition — so what is pinned here is that it
COMPOSES rather than reimplements, that its dry run is genuinely inert, and
that it refuses the two states in which closing out is the wrong thing to do.

Same two rules as the other lifecycle tests: fictional fixtures only (`tests/**`
is KEEP-copied verbatim into the public template — see `test_spawn_privacy.py`),
and every refusal is driven with input that must trip it.
"""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
SHADOW_LOG = """\
# Autonomy calibration log

## Shadow window — the tier-`notify` merge decision

Count toward 40: 0 (stage 1: 0, stage 2: 0)

One row per tier-`notify` candidate at close-out.

| date | task | tier | gate (tests/smoke/review/heart/witness[/adversary]) \
| human action | stage |
|------|------|------|---------|--------------|-------|
| 2026-09-07 | flywheel-tuning (Flywheel#1) | notify | tests 3 pass \
| merged-unchanged | 1 |
"""


def _mind(tmp_path: Path, *, draft=False) -> Path:
    """A fictional Mind holding one in-flight task plus one bystander.

    `draft=True` files the task's prompt in draft/ instead of active/ — the
    ship-straight-off-a-draft case `record --prompt` cannot reach at all."""
    root = tmp_path
    (root / "active").mkdir()
    (root / "complete").mkdir()
    (root / "draft" / "feature" / "flywheel").mkdir(parents=True)

    prompt_body = "# Sprocket calibration\n\nRe-measure the torque baseline.\n"
    if draft:
        prompt = root / "draft" / "feature" / "flywheel" / "sprocket_calibration.md"
        prompt.write_text(prompt_body)
        listed = "draft/feature/flywheel/sprocket_calibration.md"
    else:
        prompt = root / "active" / "sprocket_calibration.md"
        prompt.write_text(prompt_body)
        listed = "active/sprocket_calibration.md"

    # a bystander task, to prove close touches exactly one entry
    (root / "active" / "widget_alignment.md").write_text("# Widget alignment\n")
    (root / "active.md").write_text(
        "# Active\n\n"
        "## sprocket-calibration\n"
        "- status: library-dev\n"
        f"- prompt: {listed}\n"
        "\n"
        "## widget-alignment\n"
        "- status: library-dev\n"
        "- prompt: active/widget_alignment.md\n"
    )
    (root / "parked.md").write_text(
        "# Parked\n\n"
        "## sprocket-calibration\n"
        "- parked: 2026-08-01\n"
        f"- prompt: {listed}\n"
    )
    (root / "epics.md").write_text(
        "# Epics\n\n## flywheel-programme\n"
        f"- phase 1: `{listed}` — in flight\n"
    )
    (root / "autonomy_log.md").write_text(SHADOW_LOG)
    (root / "body.md").write_text(
        "## sprocket-calibration\n"
        "- issue: https://github.com/ExampleOrg/Flywheel/issues/7\n"
        "- completed: 2026-09-17\n"
        "- summary: re-measured the torque baseline\n"
    )
    return root


def _at(monkeypatch, root: Path) -> None:
    """Point every module-level path `close` composes over at the fixture."""
    monkeypatch.setattr(lifecycle, "ROOT", root)
    monkeypatch.setattr(lifecycle, "ACTIVE_DIR", root / "active")
    monkeypatch.setattr(lifecycle, "ACTIVE_MD", root / "active.md")
    monkeypatch.setattr(lifecycle, "DRAFT_DIR", root / "draft")
    monkeypatch.setattr(lifecycle, "COMPLETE_DIR", root / "complete")
    monkeypatch.setattr(lifecycle, "ARCHIVE_DIR", root / "complete" / "archive")
    monkeypatch.setattr(lifecycle, "INDEX_MD", root / "complete" / "index.md")
    monkeypatch.setattr(lifecycle, "AUTONOMY_LOG", root / "autonomy_log.md")


def _args(root: Path, **kw):
    base = dict(slug="sprocket-calibration", date="2026-09-17",
                from_file=str(root / "body.md"), prompt=None, pr=[], tier=None,
                gate=None, action=None, stage="1", no_shadow_row=False,
                log=None, apply=False)
    base.update(kw)
    return SimpleNamespace(**base)


def _snapshot(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


RECORD = "complete/2026/09/sprocket-calibration.md"


# --------------------------------------------------------------------------- #
# the dry run is inert
# --------------------------------------------------------------------------- #
def test_the_dry_run_changes_nothing_at_all(tmp_path, monkeypatch, capsys):
    """Default-dry-run is the whole reason a session can be told to run this
    verb before it has decided to: it must not write a byte."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    before = _snapshot(root)
    assert lifecycle.cmd_close(_args(root)) == 0
    assert _snapshot(root) == before


def test_the_dry_run_names_every_step_it_would_take(tmp_path, monkeypatch,
                                                    capsys):
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    lifecycle.cmd_close(_args(root))
    out = capsys.readouterr().out
    assert RECORD in out                                  # the record path
    assert "remove:   active/sprocket_calibration.md" in out
    assert "active.md — drop the `## sprocket-calibration` entry" in out
    assert "parked.md — drop the `## sprocket-calibration` entry" in out
    assert "complete/index.md" in out
    assert "dry run" in out


# --------------------------------------------------------------------------- #
# --apply
# --------------------------------------------------------------------------- #
def test_apply_writes_the_record_and_leaves_check_clean(tmp_path, monkeypatch,
                                                        capsys):
    """The one assertion that matters: after a close-out the Mind is not in
    drift — no shipped slug left in a registry, no prompt left in a state
    folder, no stale index."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, apply=True)) == 0

    record = root / RECORD
    assert record.is_file()
    assert "## Original prompt" in record.read_text()
    assert "torque baseline" in record.read_text()          # the prompt, folded
    assert not (root / "active" / "sprocket_calibration.md").exists()
    assert "sprocket-calibration" not in (root / "active.md").read_text()
    assert "sprocket-calibration" not in (root / "parked.md").read_text()
    assert "widget-alignment" in (root / "active.md").read_text()
    assert "sprocket-calibration" in (root / "complete" / "index.md").read_text()

    capsys.readouterr()
    assert lifecycle.cmd_check(SimpleNamespace(paths=[], base=None)) == 0


def test_apply_folds_and_removes_a_draft_prompt_too(tmp_path, monkeypatch):
    """`record --prompt` resolves under active/ ONLY and no-ops in silence when
    it misses — the trap that leaves a record with no `## Original prompt` and
    an orphan behind. A task may ship straight off a draft."""
    root = _mind(tmp_path, draft=True)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, apply=True)) == 0
    assert "torque baseline" in (root / RECORD).read_text()
    assert not (root / "draft" / "feature" / "flywheel"
                / "sprocket_calibration.md").exists()


def test_apply_stages_nothing(tmp_path, monkeypatch):
    """`close` touches the worktree only — the caller stages what it changed.
    A `git` call here would also be a lie in a fixture that is not a repo."""
    calls = []
    import subprocess
    real = subprocess.run
    monkeypatch.setattr(subprocess, "run",
                        lambda argv, *a, **k: (calls.append(argv),
                                               real(["true"], *a, **k))[1])
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, apply=True)) == 0
    assert [c for c in calls if "git" in c[0]] == []


# --------------------------------------------------------------------------- #
# the two refusals
# --------------------------------------------------------------------------- #
def test_it_refuses_when_the_record_already_exists(tmp_path, monkeypatch,
                                                   capsys):
    """A completion record is the one file here that is not regenerable, so a
    second `close` must never overwrite it from a --from-file body."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, apply=True)) == 0
    keep = (root / RECORD).read_bytes()
    assert lifecycle.cmd_close(_args(root, apply=True)) == 1
    assert "already exists" in capsys.readouterr().err
    assert (root / RECORD).read_bytes() == keep


def test_it_refuses_a_record_filed_under_another_month(tmp_path, monkeypatch,
                                                       capsys):
    """The slug is the identity, not the bucket — a record filed in August
    still means this task is closed out."""
    root = _mind(tmp_path)
    old = root / "complete" / "2026" / "08" / "sprocket-calibration.md"
    old.parent.mkdir(parents=True)
    old.write_text("## sprocket-calibration\n- completed: 2026-08-02\n")
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, apply=True)) == 1
    assert "2026/08" in capsys.readouterr().err


def test_it_refuses_a_slug_that_resolves_to_no_prompt(tmp_path, monkeypatch,
                                                      capsys):
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(
        _args(root, slug="never-written", apply=True)) == 1
    err = capsys.readouterr().err
    assert "no prompt" in err
    assert not (root / "complete" / "2026").exists()


def test_it_refuses_a_bad_date_and_a_missing_body(tmp_path, monkeypatch,
                                                  capsys):
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(root, date="last tuesday")) == 1
    assert lifecycle.cmd_close(_args(root, from_file=str(root / "nope.md"))) == 1


# --------------------------------------------------------------------------- #
# the shadow window leg
# --------------------------------------------------------------------------- #
def test_tier_notify_with_a_gate_and_an_action_appends_one_row(tmp_path,
                                                               monkeypatch):
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    assert lifecycle.cmd_close(_args(
        root, apply=True, tier="notify", gate="tests 3 pass",
        action="merged-unchanged", pr=["Flywheel#8"])) == 0
    log = (root / "autonomy_log.md").read_text()
    assert "sprocket-calibration (Flywheel#8)" in log
    assert "Count toward 40: 2" in log


def test_a_tier_that_is_not_notify_appends_nothing(tmp_path, monkeypatch):
    """Anything but `notify` is outside the pre-registered window: no row, no
    question, no ledger line."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    before = (root / "autonomy_log.md").read_text()
    assert lifecycle.cmd_close(_args(
        root, apply=True, tier="glance", gate="tests 3 pass",
        action="merged-unchanged")) == 0
    assert (root / "autonomy_log.md").read_text() == before


def test_tier_notify_without_a_gate_writes_no_row_and_says_why(tmp_path,
                                                               monkeypatch,
                                                               capsys):
    """The row records the gate that RAN and what the human DID — inventing
    either is the one thing the protocol cannot survive."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    before = (root / "autonomy_log.md").read_text()
    assert lifecycle.cmd_close(_args(root, apply=True, tier="notify")) == 0
    assert (root / "autonomy_log.md").read_text() == before
    assert "--gate/--action are missing" in capsys.readouterr().out


def test_no_shadow_row_suppresses_the_leg_outright(tmp_path, monkeypatch):
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    before = (root / "autonomy_log.md").read_text()
    assert lifecycle.cmd_close(_args(
        root, apply=True, tier="notify", gate="tests 3 pass",
        action="merged-unchanged", no_shadow_row=True)) == 0
    assert (root / "autonomy_log.md").read_text() == before


# --------------------------------------------------------------------------- #
# the sweep — reported, never rewritten
# --------------------------------------------------------------------------- #
def test_remaining_references_are_reported_and_left_alone(tmp_path, monkeypatch,
                                                          capsys):
    """Which mentions the merge falsified is a judgement; `close` hands them
    over rather than guessing."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    epics_before = (root / "epics.md").read_text()
    assert lifecycle.cmd_close(_args(root, apply=True)) == 0
    out = capsys.readouterr().out
    assert "repoint these" in out
    assert "epics.md:" in out
    assert (root / "epics.md").read_text() == epics_before


def test_the_dashboard_is_named_as_a_next_step_not_rendered(tmp_path,
                                                            monkeypatch,
                                                            capsys):
    """State is the Mind's, the renderer is the Brain's — and `main` heals the
    render anyway (dashboard_refresh.yml)."""
    root = _mind(tmp_path)
    _at(monkeypatch, root)
    lifecycle.cmd_close(_args(root, apply=True))
    out = capsys.readouterr().out
    assert lifecycle.DASHBOARD_NEXT in out
    assert not (root / "dashboard.md").exists()


# --------------------------------------------------------------------------- #
# resolution
# --------------------------------------------------------------------------- #
def test_the_prompt_is_found_through_a_registry_path_it_does_not_name(
        tmp_path, monkeypatch):
    """A slug need not match its filename — the registry `prompt:` is the
    authority when it does not."""
    root = _mind(tmp_path)
    (root / "active" / "sprocket_calibration.md").rename(
        root / "active" / "torque_rebaseline.md")
    (root / "active.md").write_text(
        (root / "active.md").read_text().replace(
            "active/sprocket_calibration.md", "active/torque_rebaseline.md"))
    _at(monkeypatch, root)
    found, how = lifecycle.close_prompt(root, "sprocket-calibration")
    assert found == root / "active" / "torque_rebaseline.md"
    assert "active.md" in how


def test_an_explicit_prompt_takes_a_path_or_a_bare_filename(tmp_path,
                                                            monkeypatch):
    root = _mind(tmp_path, draft=True)
    _at(monkeypatch, root)
    rel = "draft/feature/flywheel/sprocket_calibration.md"
    assert lifecycle.close_prompt(root, "x", rel)[0] == root / rel
    assert lifecycle.close_prompt(
        root, "x", "sprocket_calibration.md")[0] == root / rel
    assert lifecycle.close_prompt(root, "x", "nothing_here.md")[0] is None
