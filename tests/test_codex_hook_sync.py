"""Generated Codex project-hook adapters stay scoped, valid and current."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402


REPOS = {
    "OrganOne": {
        "category": "organ",
        "role": "A first organ.",
        "codex_hooks": ["mind-commit-guard", "end-at-deliverable"],
    },
    "AssistantTwo": {
        "category": "assistant",
        "role": "An assistant.",
        "codex_hooks": ["pyauto-api-gate", "end-at-deliverable"],
    },
    "LibraryThree": {"category": "library", "role": "Not opted in."},
}


def test_render_uses_codex_wire_names_and_repo_root_commands():
    config = json.loads(repos_sync.render_codex_hooks(REPOS["AssistantTwo"]))
    groups = config["hooks"]["PreToolUse"]
    assert [group["matcher"] for group in groups] == [
        "Bash", repos_sync.DELIVERABLE_HOOK_MATCHER
    ]
    commands = [group["hooks"][0]["command"] for group in groups]
    assert all("git rev-parse --show-toplevel" in command for command in commands)
    assert any("validate_pyauto_code.py" in command for command in commands)
    assert any("end-at-deliverable.sh" in command for command in commands)
    assert "SessionStart" not in config["hooks"]


def test_write_is_opt_in_and_idempotent(tmp_path):
    for name in REPOS:
        (tmp_path / name).mkdir()
    repos_sync.write_codex_hooks(tmp_path, REPOS)
    first = (tmp_path / "OrganOne" / repos_sync.CODEX_HOOKS_REL).read_bytes()
    assert (tmp_path / "AssistantTwo" / repos_sync.CODEX_HOOKS_REL).exists()
    assert not (tmp_path / "LibraryThree" / ".codex").exists()

    repos_sync.write_codex_hooks(tmp_path, REPOS)
    assert (tmp_path / "OrganOne" / repos_sync.CODEX_HOOKS_REL).read_bytes() == first
    assert repos_sync.check_codex_hooks(tmp_path, REPOS) == []


def test_missing_malformed_and_drifted_configs_fail(tmp_path):
    for name in REPOS:
        (tmp_path / name).mkdir()
    repos_sync.write_codex_hooks(tmp_path, REPOS)

    organ = tmp_path / "OrganOne" / repos_sync.CODEX_HOOKS_REL
    organ.unlink()
    assistant = tmp_path / "AssistantTwo" / repos_sync.CODEX_HOOKS_REL
    assistant.write_text("{malformed json\n")

    problems = repos_sync.check_codex_hooks(tmp_path, REPOS)
    assert len(problems) == 2
    assert any("OrganOne" in problem and "no .codex/hooks.json" in problem
               for problem in problems)
    assert any("AssistantTwo" in problem and "differs" in problem
               for problem in problems)


@pytest.mark.parametrize("value", ["end-at-deliverable", {"bad": "shape"}])
def test_manifest_requires_a_list(value):
    with pytest.raises(ValueError, match="must be a list"):
        repos_sync.render_codex_hooks({"codex_hooks": value})


def test_manifest_rejects_unknown_and_duplicate_adapters():
    with pytest.raises(ValueError, match="unknown codex hook"):
        repos_sync.render_codex_hooks({"codex_hooks": ["invented"]})
    with pytest.raises(ValueError, match="duplicate"):
        repos_sync.render_codex_hooks({
            "codex_hooks": ["end-at-deliverable", "end-at-deliverable"]
        })


def test_main_write_only_codex_does_not_run_the_broad_writer(
    tmp_path, monkeypatch
):
    (tmp_path / "OrganOne").mkdir()
    monkeypatch.setattr(repos_sync, "load_manifest", lambda _root: ({}, REPOS))
    monkeypatch.setattr(
        repos_sync, "write_block",
        lambda *_args, **_kwargs: pytest.fail("broad writer ran"),
    )
    monkeypatch.setattr(
        sys, "argv",
        ["repos_sync.py", "--write", "--root", str(tmp_path),
         "--only", repos_sync.CODEX_HOOKS],
    )
    with pytest.raises(SystemExit) as exit_info:
        repos_sync.main()
    assert exit_info.value.code == 0
    assert (tmp_path / "OrganOne" / repos_sync.CODEX_HOOKS_REL).exists()


def test_live_manifest_opts_in_exactly_the_phase_two_repos():
    mind_root = Path(__file__).resolve().parents[1]
    _, repos = repos_sync.load_manifest(mind_root)
    opted_in = {
        name for name, spec in repos.items() if repos_sync.codex_hook_names(spec)
    }
    assert opted_in == {
        "PyAutoMind", "PyAutoBrain", "autofit_assistant",
        "autogalaxy_assistant", "autolens_assistant", "autocti_assistant",
    }
