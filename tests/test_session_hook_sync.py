"""The SessionStart hook is generated into every repo — and must not drift.

The hook is what makes a Claude Code web/mobile session run Python 3.12 instead
of the container's 3.11 default. The harness reads it per repo, so it cannot
live once in the workspace: every repo carries a copy. Copies rot — that is the
whole reason `policy/session_start_hook.sh` is the single source and
`check_session_hooks` exists.

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
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

HOOK_TEXT = "#!/usr/bin/env bash\necho canonical\n"
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


def make_repo(root, name, *, hook=HOOK_TEXT, executable=True, settings="register"):
    """A checked-out repo with the hook installed in one of several states."""
    repo = root / name
    (repo / ".claude" / "hooks").mkdir(parents=True)
    if hook is not None:
        path = repo / repos_sync.SESSION_HOOK_REL
        path.write_text(hook)
        path.chmod(0o755 if executable else 0o644)
    if settings == "register":
        (repo / repos_sync.SESSION_SETTINGS_REL).write_text(
            json.dumps(repos_sync.register_session_hook({}), indent=2) + "\n"
        )
    elif settings is not None:
        (repo / repos_sync.SESSION_SETTINGS_REL).write_text(settings)
    return repo


def test_fully_installed_repo_is_clean(tmp_path):
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT) == []


def test_repo_that_is_not_checked_out_is_skipped(tmp_path):
    make_repo(tmp_path, "OrganOne")  # LibTwo absent entirely
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT) == []


def test_missing_hook_fails(tmp_path):
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=None)
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert len(problems) == 1 and "LibTwo" in problems[0]


def test_edited_copy_fails(tmp_path):
    """The failure mode the whole check exists for: someone fixes the hook in
    one repo instead of in the canonical file."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=HOOK_TEXT + "# local tweak\n")
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert len(problems) == 1 and "differs" in problems[0]


def test_non_executable_hook_fails(tmp_path):
    """A hook without +x is silently never run by the harness."""
    make_repo(tmp_path, "OrganOne", executable=False)
    make_repo(tmp_path, "LibTwo")
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert len(problems) == 1 and "not executable" in problems[0]


def test_missing_or_unregistering_settings_fails(tmp_path):
    """An installed hook nothing points at is dead weight."""
    make_repo(tmp_path, "OrganOne", settings=None)
    make_repo(tmp_path, "LibTwo", settings=json.dumps({"hooks": {"Stop": []}}))
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert len(problems) == 2
    assert any("no .claude/settings.json" in p for p in problems)
    assert any("does not register" in p for p in problems)


def test_unparseable_settings_counts_as_unregistered(tmp_path):
    make_repo(tmp_path, "OrganOne", settings="{not json")
    make_repo(tmp_path, "LibTwo")
    problems = repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert len(problems) == 1 and "does not register" in problems[0]


def test_write_fixes_every_failure_mode_and_is_idempotent(tmp_path):
    make_repo(tmp_path, "OrganOne", hook=HOOK_TEXT + "# drift\n", executable=False)
    make_repo(tmp_path, "LibTwo", hook=None, settings=None)
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT) != []

    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert repos_sync.check_session_hooks(tmp_path, REPOS, HOOK_TEXT) == []

    installed = tmp_path / "OrganOne" / repos_sync.SESSION_HOOK_REL
    assert installed.read_text() == HOOK_TEXT
    assert installed.stat().st_mode & stat.S_IXUSR
    before = {
        p: p.read_bytes()
        for p in (tmp_path / "LibTwo" / ".claude").rglob("*")
        if p.is_file()
    }
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT)
    assert {p: p.read_bytes() for p in before} == before


def test_write_preserves_other_settings_keys(tmp_path):
    """A repo's own permissions/env/hooks must survive the registration."""
    repo = make_repo(tmp_path, "OrganOne", settings=json.dumps(
        {"env": {"KEEP": "me"}, "hooks": {"Stop": [{"hooks": []}]}}
    ))
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT)
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
        tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT
    ) == []


def test_excluded_repo_is_not_written_into(tmp_path):
    """--write must not re-create the directory a human decided to leave out."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo")
    (tmp_path / "ToolThree").mkdir()
    repos_sync.write_session_hooks(tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT)
    assert not (tmp_path / "ToolThree" / ".claude").exists()


def test_an_exclusion_cannot_silence_a_real_repos_drift(tmp_path):
    """Proving the leg still fails: the exclusion is per-repo, not a kill switch."""
    make_repo(tmp_path, "OrganOne")
    make_repo(tmp_path, "LibTwo", hook=HOOK_TEXT + "# stale wave\n")
    (tmp_path / "ToolThree").mkdir()
    problems = repos_sync.check_session_hooks(
        tmp_path, REPOS_WITH_EXCLUSION, HOOK_TEXT
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
    assert "propagate" in spec["jobs"]


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
