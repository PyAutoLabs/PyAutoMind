"""Both generated hooks are installed into every repo — and must not drift.

The SessionStart hook is what makes a Claude Code web/mobile session run Python
3.12 instead of the container's 3.11 default; the PreToolUse
end-at-deliverable guard is what stops a session arming a timer that outlives
its turn. The harness reads hooks per repo, so neither can live once in the
workspace: every repo carries a copy of each. Copies rot — that is the whole
reason `policy/session_start_hook.sh` and `policy/end_at_deliverable_hook.sh`
are the single sources and `check_session_hooks` exists.

Conventions this file follows (see `test_repos_sync_hygiene_coverage.py`):

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository, and the assertions
   are about the check's logic rather than whatever happens to be checked out.
2. **Prove each leg FAILS.** Every failure mode below is driven with input that
   must trip it — a check that cannot fail is decoration.
"""

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

HOOK_TEXT = "#!/usr/bin/env bash\necho canonical\n"
DELIVERABLE_TEXT = "#!/usr/bin/env bash\necho canonical guard\n"
# `role` is carried because the tests that drive main() end-to-end render the
# organism map from the same manifest dict.
REPOS = {
    "OrganOne": {"category": "organ", "role": "A first organ."},
    "LibTwo": {"category": "library", "role": "A second repo."},
}
# A third repo the manifest opts OUT of the hook (`session_hook: false`).
REPOS_WITH_EXCLUSION = dict(
    REPOS,
    ToolThree={
        "category": "admin", "role": "Local tooling.", "session_hook": False
    },
)


def make_repo(root, name, *, hook=HOOK_TEXT, deliverable=DELIVERABLE_TEXT,
              executable=True, settings="register"):
    """A checked-out repo with both generated hooks installed in one of several
    states. `hook` / `deliverable` set to None leave that copy out; `executable`
    applies to whichever copies are written."""
    repo = root / name
    (repo / ".claude" / "hooks").mkdir(parents=True)
    for text, rel in ((hook, repos_sync.SESSION_HOOK_REL),
                      (deliverable, repos_sync.DELIVERABLE_HOOK_REL)):
        if text is None:
            continue
        path = repo / rel
        path.write_text(text)
        path.chmod(0o755 if executable else 0o644)
    if settings == "register":
        registered = repos_sync.register_deliverable_hook(
            repos_sync.register_session_hook({})
        )
        (repo / repos_sync.SESSION_SETTINGS_REL).write_text(
            json.dumps(registered, indent=2) + "\n"
        )
    elif settings is not None:
        (repo / repos_sync.SESSION_SETTINGS_REL).write_text(settings)
    return repo


def test_fully_installed_repo_is_clean(tmp_path):
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT) == []


def test_repo_that_is_not_checked_out_is_skipped(tmp_path):
    make_repo(tmp_path, "OrganOne")  # LibTwo absent entirely
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT) == []


def test_missing_hook_fails(tmp_path):
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=None)
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT)
    assert len(problems) == 1 and "LibTwo" in problems[0]


def test_edited_copy_fails(tmp_path):
    """The failure mode the whole check exists for: someone fixes the hook in
    one repo instead of in the canonical file."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=HOOK_TEXT + "# local tweak\n")
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT)
    assert len(problems) == 1 and "differs" in problems[0]


def test_non_executable_hook_fails(tmp_path):
    """A hook without +x is silently never run by the harness — and that is as
    true of the PreToolUse guard as of the SessionStart hook, so both copies are
    checked, not just the first one that happens to be looked at."""
    make_repo(tmp_path, "OrganOne", executable=False)
    make_repo(tmp_path, "LibTwo")
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 2, problems
    assert all("OrganOne" in p and "not executable" in p for p in problems)
    assert any(repos_sync.SESSION_HOOK_REL in p for p in problems)
    assert any(repos_sync.DELIVERABLE_HOOK_REL in p for p in problems)


def test_missing_or_unregistering_settings_fails(tmp_path):
    """An installed hook nothing points at is dead weight — both of them."""
    make_repo(tmp_path, "OrganOne", settings=None)
    make_repo(tmp_path, "LibTwo", settings=json.dumps({"hooks": {"Stop": []}}))
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 3, problems
    assert any("no .claude/settings.json" in p for p in problems)
    assert any("does not register the SessionStart hook" in p for p in problems)
    assert any("does not register the PreToolUse" in p for p in problems)


def test_unparseable_settings_counts_as_unregistered(tmp_path):
    make_repo(tmp_path, "OrganOne", settings="{not json")
    make_repo(tmp_path, "LibTwo")
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 2, problems
    assert all("OrganOne" in p and "does not register" in p for p in problems)


def test_a_missing_deliverable_hook_fails_on_its_own(tmp_path):
    """The half-installed state the propagation exists to prevent: the session
    hook landed, the guard did not, and nothing else in the workspace notices."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", deliverable=None)
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 1, problems
    assert "LibTwo" in problems[0] and repos_sync.DELIVERABLE_HOOK_REL in problems[0]


def test_an_edited_deliverable_hook_copy_fails(tmp_path):
    """Someone weakening the guard in one repo instead of in the canonical file
    is precisely the drift this whole one-source contract exists for."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo",
              deliverable=DELIVERABLE_TEXT + "exit 0  # local tweak\n")
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 1, problems
    assert "differs" in problems[0]
    assert repos_sync.DELIVERABLE_HOOK_FILE in problems[0]


def test_settings_registering_only_the_session_hook_fails(tmp_path):
    """A repo carrying both files but registering one of them runs one of them."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", settings=json.dumps(
        repos_sync.register_session_hook({}), indent=2
    ))
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 1, problems
    assert "does not register the PreToolUse" in problems[0]


def test_write_fixes_every_failure_mode_and_is_idempotent(tmp_path):
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# drift\n", executable=False)
    make_repo(tmp_path, "LibTwo", hook=None, settings=None)
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT) != []

    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT)
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT) == []

    installed = tmp_path / "OrganOne" / repos_sync.SESSION_HOOK_REL
    assert installed.read_text() == HOOK_TEXT
    assert installed.stat().st_mode & stat.S_IXUSR
    before = {
        p: p.read_bytes()
        for p in (tmp_path / "LibTwo" / ".claude").rglob("*")
        if p.is_file()
    }
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT)
    assert {p: p.read_bytes() for p in before} == before


def test_write_preserves_other_settings_keys(tmp_path):
    """A repo's own permissions/env/hooks must survive the registration."""
    repo = make_repo(tmp_path, "OrganOne", settings=json.dumps(
        {"env": {"KEEP": "me"}, "hooks": {"Stop": [{"hooks": []}]}}
    ))
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT)
    settings = json.loads((repo / repos_sync.SESSION_SETTINGS_REL).read_text())
    assert settings["env"] == {"KEEP": "me"}
    assert "Stop" in settings["hooks"]
    assert repos_sync.SESSION_HOOK_COMMAND in repos_sync.session_start_entries(settings)


def test_canonical_hook_ships_and_is_the_installed_text():
    """The real file, not a fixture: it must exist, be executable and be what
    `--write` would install."""
    mind_root = Path(__file__).resolve().parents[1]
    canonical = mind_root / repos_sync.SESSION_HOOK_FILE
    assert canonical.exists(), f"{repos_sync.SESSION_HOOK_FILE} is missing"
    assert os.access(canonical, os.X_OK)
    text = repos_sync.load_session_hook(mind_root)
    assert text.startswith("#!")
    assert text == (mind_root / repos_sync.SESSION_HOOK_REL).read_text()


def test_canonical_deliverable_hook_ships_and_is_the_installed_text():
    """Same contract for the guard, and checked here because PyAutoMind is the
    one repo the propagation workflow never writes to."""
    mind_root = Path(__file__).resolve().parents[1]
    canonical = mind_root / repos_sync.DELIVERABLE_HOOK_FILE
    assert canonical.exists(), f"{repos_sync.DELIVERABLE_HOOK_FILE} is missing"
    assert os.access(canonical, os.X_OK)
    text = repos_sync.load_deliverable_hook(mind_root)
    assert text.startswith("#!")
    assert text == (mind_root / repos_sync.DELIVERABLE_HOOK_REL).read_text()


def test_this_repos_settings_registers_the_deliverable_hook_with_the_matcher():
    settings = json.loads(
        (Path(__file__).resolve().parents[1]
         / repos_sync.SESSION_SETTINGS_REL).read_text()
    )
    assert repos_sync.DELIVERABLE_HOOK_COMMAND in repos_sync.pre_tool_use_entries(
        settings
    )
    matchers = [
        group.get("matcher")
        for group in settings["hooks"]["PreToolUse"]
    ]
    assert repos_sync.DELIVERABLE_HOOK_MATCHER in matchers


# --------------------------------------------------------------------------
# Manifest exclusions (`session_hook: false`)
# --------------------------------------------------------------------------

def test_excluded_repo_is_not_checked_even_when_it_has_no_hook(tmp_path):
    """The recorded exclusion is the point: a checked-out repo with no .claude/
    at all must not be reported as drift."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    (tmp_path / "ToolThree").mkdir()
    assert repos_sync.check_session_hooks(
        tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT, DELIVERABLE_TEXT
    ) == []


def test_excluded_repo_is_not_written_into(tmp_path):
    """--write must not re-create the directory a human decided to leave out."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    (tmp_path / "ToolThree").mkdir()
    repos_sync.write_session_hooks(tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT, DELIVERABLE_TEXT)
    assert not (tmp_path / "ToolThree" / ".claude").exists()


def test_an_exclusion_cannot_silence_a_real_repos_drift(tmp_path):
    """Proving the leg still fails: the exclusion is per-repo, not a kill switch."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT, DELIVERABLE_TEXT
    )
    assert len(problems) == 1 and "LibTwo" in problems[0] and "differs" in problems[0]


# --------------------------------------------------------------------------
# The denominator
# --------------------------------------------------------------------------

def test_counts_report_the_partial_checkout(tmp_path):
    """The whole point of the denominator: a session holding one of two in-scope
    repos must be able to see that it is holding one of two."""
    make_repo(tmp_path, "OrganOne")  # LibTwo absent
    (tmp_path / "ToolThree").mkdir()
    assert repos_sync.session_hook_counts(tmp_path, REPOS_WITH_EXCLUSION) == (1, 2, 1)


def test_counts_exclude_the_excluded_from_the_denominator(tmp_path):
    """An excluded repo is not a repo that is 'missing its hook' — it is out of
    the rollout surface entirely, so it never enters the total."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    make_repo(tmp_path, "ToolThree")  # present AND fully installed
    checked_out, in_scope, excluded = repos_sync.session_hook_counts(
        tmp_path, REPOS_WITH_EXCLUSION
    )
    assert (checked_out, in_scope, excluded) == (2, 2, 1)


def test_counts_on_an_empty_checkout_are_zero_of_the_full_surface(tmp_path):
    """The failure this exists to make visible: nothing on disk, nothing to
    check, and a leg that would otherwise print a bare 'OK'."""
    assert repos_sync.session_hook_counts(tmp_path, REPOS_WITH_EXCLUSION) == (0, 2, 1)


def test_check_leg_prints_the_denominator(tmp_path, capsys, monkeypatch):
    """End to end through main(): the status line for this leg — and only this
    leg — carries the counts."""
    make_repo(tmp_path, "OrganOne")  # LibTwo absent, ToolThree excluded
    monkeypatch.setattr(
        repos_sync, "load_manifest", lambda _root: ({}, REPOS_WITH_EXCLUSION)
    )
    monkeypatch.setattr(repos_sync, "load_session_hook", lambda _root: HOOK_TEXT)
    monkeypatch.setattr(
        repos_sync, "load_deliverable_hook", lambda _root: DELIVERABLE_TEXT
    )
    monkeypatch.setattr(
        sys, "argv",
        ["repos_sync.py", "--check", "--root", str(tmp_path),
         "--only", repos_sync.SESSION_HOOKS],
    )
    with pytest.raises(SystemExit) as exit_info:
        repos_sync.main()
    assert exit_info.value.code == 0
    out = capsys.readouterr().out
    assert (
        f"check {repos_sync.SESSION_HOOKS}: OK (1 of 2 checked out, 1 excluded)"
        in out
    ), out


def test_denominator_rides_along_with_a_mismatch_count(tmp_path, capsys, monkeypatch):
    """A red leg still says how much of the surface it could see — otherwise the
    fix looks complete once the visible repos go green."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale\n")
    monkeypatch.setattr(
        repos_sync, "load_manifest", lambda _root: ({}, REPOS_WITH_EXCLUSION)
    )
    monkeypatch.setattr(repos_sync, "load_session_hook", lambda _root: HOOK_TEXT)
    monkeypatch.setattr(
        repos_sync, "load_deliverable_hook", lambda _root: DELIVERABLE_TEXT
    )
    monkeypatch.setattr(
        sys, "argv",
        ["repos_sync.py", "--check", "--root", str(tmp_path),
         "--only", repos_sync.SESSION_HOOKS],
    )
    with pytest.raises(SystemExit) as exit_info:
        repos_sync.main()
    assert exit_info.value.code == 1
    out = capsys.readouterr().out
    assert (
        f"check {repos_sync.SESSION_HOOKS}: 1 mismatch(es) "
        "(1 of 2 checked out, 1 excluded)" in out
    ), out


# --------------------------------------------------------------------------
# The propagation workflow (the mechanism that stops the long tail re-staling)
# --------------------------------------------------------------------------

def test_propagation_workflow_parses_and_carries_its_two_load_bearing_names():
    """Not a fixture: the real workflow file.

    It must parse (a YAML error here is a workflow that never runs, and nothing
    else in this repo would notice), reach the siblings with the org-wide PAT
    (this repo's GITHUB_TOKEN cannot write to them), and derive its targets from
    the same `session_hook` manifest key the check above honours — a hard-coded
    repo list would drift from repos.yaml the first time a repo is added.
    """
    workflow = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/session_hook_propagate.yml"
    )
    assert workflow.exists(), f"{workflow.name} is missing"
    text = workflow.read_text()
    spec = yaml.safe_load(text)
    assert "PAT_PYAUTOLABS" in text
    assert "session_hook" in text
    # `on:` is YAML 1.1's boolean True — the key is not the string "on".
    triggers = spec[True]
    assert "workflow_dispatch" in triggers
    assert repos_sync.SESSION_HOOK_FILE in triggers["push"]["paths"]
    assert repos_sync.DELIVERABLE_HOOK_FILE in triggers["push"]["paths"]
    assert "repos.yaml" in triggers["push"]["paths"]
    assert "propagate" in spec["jobs"]
    # Both installed copies have to be staged and pushed: a workflow that
    # regenerates a file it never `git add`s reports every repo "already
    # current" and propagates nothing.
    assert text.count(repos_sync.DELIVERABLE_HOOK_REL) >= 2, text
    assert "write_codex_hooks" in text
    assert text.count(repos_sync.CODEX_HOOKS_REL) >= 2, text


def test_firewall_gate_triggers_on_the_canonical_hook():
    """The gate that runs the drift check must fire when the thing it checks
    changes — it did not, which is how two waves of staleness got in."""
    gate = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/firewall_gate.yml"
    )
    triggers = yaml.safe_load(gate.read_text())[True]
    for event in ("push", "pull_request"):
        assert repos_sync.SESSION_HOOK_FILE in triggers[event]["paths"], event
        assert repos_sync.DELIVERABLE_HOOK_FILE in triggers[event]["paths"], event
        assert "repos.yaml" in triggers[event]["paths"], event


@pytest.mark.parametrize(
    'body, expected',
    [
        ('', 'main'),
        ('No dependency declaration', 'main'),
        ('Brain-ref: feature/paired-hooks\r\n', 'feature/paired-hooks'),
        ('Brain-ref: abc123\nBrain-ref: ignored\n', 'abc123'),
        ('Brain-ref: $(touch injected)\n', 'main'),
    ],
)
def test_firewall_brain_ref_resolution(tmp_path, body, expected):
    """Execute the CI resolver: pairing selects a ref without executing PR text."""
    gate = Path(__file__).resolve().parents[1] / '.github/workflows/firewall_gate.yml'
    steps = yaml.safe_load(gate.read_text())['jobs']['firewall']['steps']
    resolver = next(step for step in steps if step.get('id') == 'brainref')
    checkout = next(step for step in steps if step.get('name') == 'Checkout PyAutoBrain')
    assert checkout['with']['ref'] == '${{ steps.brainref.outputs.ref }}'
    output = tmp_path / 'output'
    subprocess.run(
        ['bash', '-e', '-c', resolver['run']],
        cwd=tmp_path,
        env={**os.environ, 'PR_BODY': body, 'GITHUB_OUTPUT': str(output)},
        check=True,
        capture_output=True,
        text=True,
    )
    assert output.read_text() == f'ref={expected}\n'
    assert not (tmp_path / 'injected').exists()


# --------------------------------------------------------------------------
# `--skip`: dropping a leg whose precondition the caller cannot meet
# --------------------------------------------------------------------------

# The same fictional manifest, plus the `github:` identity the tenant-firewall
# leg reads: the tests below run the WHOLE registry rather than one --only leg,
# because the point of --skip is what happens to everything else.
REPOS_FULL_RUN = {
    name: dict(spec, github=f"FictionalOrg/{name}")
    for name, spec in REPOS_WITH_EXCLUSION.items()
}


def run_check(tmp_path, monkeypatch, capsys, *argv):
    """Drive main() over a fictional root; return (exit code, stdout)."""
    monkeypatch.setattr(
        repos_sync, "load_manifest", lambda _root: ({}, REPOS_FULL_RUN)
    )
    monkeypatch.setattr(repos_sync, "load_session_hook", lambda _root: HOOK_TEXT)
    monkeypatch.setattr(
        repos_sync, "load_deliverable_hook", lambda _root: DELIVERABLE_TEXT
    )
    monkeypatch.setattr(
        sys, "argv",
        ["repos_sync.py", "--check", "--root", str(tmp_path), *argv],
    )
    with pytest.raises(SystemExit) as exit_info:
        repos_sync.main()
    return exit_info.value.code, capsys.readouterr().out


def dead_pointer(root, name):
    """An unrelated red leg — a CLAUDE.md that imports nothing."""
    (root / name / "AGENTS.md").write_text("# guidance\n")
    (root / name / "CLAUDE.md").write_text("# nothing useful\n")


def test_the_hook_leg_is_red_when_a_copy_is_stale(tmp_path, monkeypatch, capsys):
    """The baseline the skip exists for — and proof the leg still bites.

    A miniature of the PR gate's failure: the canonical hook has moved on and
    the checked-out copy has not, which is exactly what a PR that edits the
    canonical hook does to every sibling checked out at its main.
    """
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()

    code, out = run_check(tmp_path, monkeypatch, capsys)

    assert code == 1
    assert f"check {repos_sync.SESSION_HOOKS}: 1 mismatch(es)" in out, out


def test_skip_subtracts_the_named_leg(tmp_path, monkeypatch, capsys):
    """Same tree, one flag: the leg is gone and the run is green."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()

    code, out = run_check(
        tmp_path, monkeypatch, capsys, "--skip", repos_sync.SESSION_HOOKS
    )

    assert code == 0
    assert f"check {repos_sync.SESSION_HOOKS}:" not in out, out


def test_skip_leaves_every_other_leg_running(tmp_path, monkeypatch, capsys):
    """Not a kill switch: the legs it did not name still run and still print."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()

    _, out = run_check(
        tmp_path, monkeypatch, capsys, "--skip", repos_sync.SESSION_HOOKS
    )

    for label in ("tenant firewall (organ code)", repos_sync.CHECKOUTS,
                  repos_sync.CODEX_HOOKS, "CLAUDE.md → AGENTS.md pointers"):
        assert f"check {label}: " in out, (label, out)


def test_skip_does_not_change_the_exit_code_of_the_remaining_legs(
    tmp_path, monkeypatch, capsys
):
    """The failure mode that would make this dangerous: a second, unrelated
    problem must still fail the run once the hook leg is dropped."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    make_repo(tmp_path, "LibTwo")
    (tmp_path / "ToolThree").mkdir()
    dead_pointer(tmp_path, "OrganOne")

    code, out = run_check(
        tmp_path, monkeypatch, capsys, "--skip", repos_sync.SESSION_HOOKS
    )

    assert code == 1
    assert f"check {repos_sync.SESSION_HOOKS}:" not in out, out
    assert "dead pointer" in out, out


def test_skip_subtracts_from_what_only_selected(tmp_path, monkeypatch, capsys):
    """The documented composition: --only picks, --skip then takes back."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()

    code, out = run_check(
        tmp_path, monkeypatch, capsys,
        "--only", repos_sync.SESSION_HOOKS,
        "--only", repos_sync.CODEX_HOOKS,
        "--skip", repos_sync.SESSION_HOOKS,
    )

    assert code == 0
    assert f"check {repos_sync.SESSION_HOOKS}:" not in out, out
    assert f"check {repos_sync.CODEX_HOOKS}: OK" in out, out


def test_skipping_a_leg_only_did_not_select_is_a_no_op(tmp_path, monkeypatch, capsys):
    """A real label --only had already excluded subtracts nothing — it is not
    an error, because nothing about it is ambiguous."""
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()

    code, out = run_check(
        tmp_path, monkeypatch, capsys,
        "--only", repos_sync.CODEX_HOOKS,
        "--skip", repos_sync.CHECKOUTS,
    )

    assert code == 0
    assert out.splitlines()[0] == f"check {repos_sync.CODEX_HOOKS}: OK", out


def test_skip_rejects_an_unknown_label(tmp_path):
    """A typo must not quietly disable nothing-at-all — or, worse, read as a
    gate that was turned off. Same refusal, and same "choose from" listing, as
    `--only`."""
    proc = subprocess.run(
        [sys.executable, str(Path(repos_sync.__file__)), "--check",
         "--root", str(tmp_path), "--skip", "no-such-check"],
        capture_output=True, text=True,
    )

    assert proc.returncode != 0
    assert "unknown --skip check(s): 'no-such-check'" in proc.stderr
    assert f"'{repos_sync.SESSION_HOOKS}'" in proc.stderr


def test_an_unknown_skip_is_refused_even_beside_a_valid_only(tmp_path):
    """Validation is against the whole registry and happens before anything is
    narrowed, so --only cannot hide a bad --skip."""
    proc = subprocess.run(
        [sys.executable, str(Path(repos_sync.__file__)), "--check",
         "--root", str(tmp_path), "--only", repos_sync.CODEX_HOOKS,
         "--skip", "no-such-check"],
        capture_output=True, text=True,
    )

    assert proc.returncode != 0
    assert "unknown --skip check(s)" in proc.stderr


# --------------------------------------------------------------------------
# The gate's canonical-hook PR path (the leg that is red by construction)
# --------------------------------------------------------------------------

def gate_steps():
    gate = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/firewall_gate.yml"
    )
    return yaml.safe_load(gate.read_text())["jobs"]["firewall"]["steps"]


def test_the_skip_is_reachable_only_from_a_pull_request():
    """`push` to main must still run every leg: the decision step that enables
    the skip is itself gated on the event, and every step carrying `--skip` is
    gated on that step's output."""
    steps = gate_steps()
    decision = next(step for step in steps if step.get("id") == "hookpr")
    assert decision["if"] == "github.event_name == 'pull_request'"

    skipping = [step for step in steps if "--skip" in (step.get("run") or "")]
    assert skipping, steps
    for step in skipping:
        assert step["if"] == "steps.hookpr.outputs.hook_pr == 'true'", step

    full = next(step for step in steps
                if "--skip" not in (step.get("run") or "")
                and "repos_sync.py --check" in (step.get("run") or ""))
    assert full["if"] == "steps.hookpr.outputs.hook_pr != 'true'"


def test_the_gate_skips_that_one_leg_by_its_printed_label():
    """`--skip` matches the label exactly, so a renamed leg must break here
    rather than silently stop being skipped (or, worse, stop being run)."""
    step = next(step for step in gate_steps()
                if "--skip" in (step.get("run") or ""))
    assert f'--skip "{repos_sync.SESSION_HOOKS}"' in step["run"], step["run"]
    assert repos_sync.CHECKOUTS not in step["run"]


def test_the_gate_says_out_loud_that_the_leg_was_skipped_and_why():
    """A green run must never read as 'the hooks are in sync'. The skip names
    itself, names propagation as what will sync the copies, and says what is
    still enforced."""
    run = next(step["run"] for step in gate_steps()
               if "--skip" in (step.get("run") or ""))
    assert "SKIPPED LEG" in run
    assert repos_sync.SESSION_HOOKS in run
    assert "session_hook_propagate.yml" in run
    assert "STILL ENFORCED" in run
    assert repos_sync.SESSION_HOOK_FILE in run


def test_the_gate_still_asserts_this_repos_own_installed_copies():
    """The compensating control, and the reason the gate did not just get
    weaker: PyAutoMind is the one repo propagation never writes to, so its own
    copies ARE the PR's to keep in step — pinned by the tests in this file."""
    step = next(step for step in gate_steps()
                if step.get("if") == "steps.hookpr.outputs.hook_pr == 'true'"
                and "pytest" in (step.get("run") or ""))
    assert Path(__file__).name in step["run"]
    # The `-k` expression must select BOTH copies — the SessionStart hook and
    # the end-at-deliverable guard — or half the compensating control is a
    # silent "deselected".
    selector = step["run"].split('-k "')[1].split('"')[0]
    for name in (test_canonical_hook_ships_and_is_the_installed_text,
                 test_canonical_deliverable_hook_ships_and_is_the_installed_text):
        assert selector in name.__name__, (selector, name.__name__)


def test_mind_checkout_is_deep_enough_to_diff_against_the_base():
    """The decision below diffs against the base branch; a depth-1 checkout has
    no merge base to diff from."""
    checkout = next(step for step in gate_steps()
                    if step.get("name") == "Checkout PyAutoMind")
    assert checkout["with"]["fetch-depth"] == 0


@pytest.mark.parametrize(
    "changed, expected",
    [
        ([repos_sync.SESSION_HOOK_FILE], "true"),
        ([repos_sync.DELIVERABLE_HOOK_FILE], "true"),
        (["repos.yaml"], "false"),
        (["scripts/repos_sync.py", ".github/workflows/firewall_gate.yml"],
         "false"),
        ([repos_sync.SESSION_HOOK_FILE, "repos.yaml"], "true"),
        # A path the hook's name is only a SUBSTRING of is a different file.
        (["docs/policy/session_start_hook.sh.md"], "false"),
    ],
)
def test_the_gate_decides_from_the_changed_files(tmp_path, changed, expected):
    """Execute the CI decision against a real two-branch repo.

    The `paths:` filter cannot answer this — it has already matched, and it
    lists four other paths besides — so the step reads the PR's own diff.
    """
    step = next(step for step in gate_steps() if step.get("id") == "hookpr")
    git = ["git", "-c", "user.email=t@example.invalid", "-c", "user.name=t"]

    base = tmp_path / "base"
    base.mkdir()
    subprocess.run(git + ["init", "-q", "-b", "main", str(base)], check=True)
    for rel in ("repos.yaml", repos_sync.SESSION_HOOK_FILE,
                repos_sync.DELIVERABLE_HOOK_FILE, "scripts/repos_sync.py",
                ".github/workflows/firewall_gate.yml",
                "docs/policy/session_start_hook.sh.md"):
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("base\n")
    subprocess.run(git + ["-C", str(base), "add", "-A"], check=True)
    subprocess.run(git + ["-C", str(base), "commit", "-qm", "base"], check=True)

    head = tmp_path / "PyAutoMind"
    subprocess.run(["git", "clone", "-q", str(base), str(head)], check=True)
    subprocess.run(git + ["-C", str(head), "checkout", "-q", "-b", "feature"],
                   check=True)
    for rel in changed:
        (head / rel).write_text("edited\n")
    subprocess.run(git + ["-C", str(head), "commit", "-qam", "edit"], check=True)

    output = tmp_path / "output"
    proc = subprocess.run(
        ["bash", "-e", "-c", step["run"]],
        cwd=tmp_path,
        env={**os.environ, "BASE_REF": "main", "GITHUB_OUTPUT": str(output)},
        check=True, capture_output=True, text=True,
    )

    assert output.read_text().strip() == f"hook_pr={expected}", proc.stdout
