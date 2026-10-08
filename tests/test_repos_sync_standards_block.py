"""Universal standards discovery, bounded writes and honest partial coverage.

Fictional consumer fixtures only: tests are copied to the public template.
"""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import repos_sync as sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]
POLICY = sync.load_standards_policy(MIND)
REPOS = {"OrganCore": {"category": "organ", "board_owner": True},
         "LibAlpha": {"category": "library"}}


def repo(root, name, body="# Guidance\n\nKeep original content.\n"):
    path = root / name / "AGENTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return path


def block(spec=None):
    return (sync.STANDARDS_BEGIN + "\n" +
            sync.render_standards_policy(POLICY, spec or {}) + "\n" +
            sync.STANDARDS_END + "\n")


def cli(root, monkeypatch, *flags):
    monkeypatch.setattr(sync, "load_manifest", lambda _: ({}, REPOS))
    monkeypatch.setattr(sync, "system_map", lambda *_: "")
    monkeypatch.setattr(sys, "argv", ["repos_sync.py", "--root", str(root), *flags])
    with pytest.raises(SystemExit) as error:
        sync.main()
    return error.value.code


def snapshot(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_canonical_text_is_short_and_standalone():
    text = sync.render_standards_policy(POLICY, {})
    assert "https://github.com/PyAutoLabs/PyAutoBrain/blob/main/docs/standards.md" in text
    assert "on demand" in text and "consumers" in text and "validate" in text
    assert "canonical source" in text
    assert len(text.splitlines()) <= 8


def test_owner_guidance_is_explicit_and_independent_of_filing_exclusions():
    assert "For board changes" in sync.render_standards_policy(POLICY, REPOS["OrganCore"])
    assert "For board changes" not in sync.render_standards_policy(POLICY, {"category": "organ"})
    assert "organism standard" in sync.render_standards_policy(POLICY, {"filing_block": False})


def test_manifest_ownership_is_boolean_and_includes_dna_and_broca():
    _, specs = sync.load_manifest(MIND)
    owners = [spec for spec in specs.values() if spec.get("board_owner")]
    assert len(owners) == 15
    assert specs["PyAutoDNA"]["board_owner"] is True
    assert specs["PyAutoBroca"]["board_owner"] is True
    assert all(isinstance(spec.get("board_owner", False), bool) for spec in specs.values())


def test_mind_owns_an_exact_generated_block():
    text = (MIND / "AGENTS.md").read_text()
    _, specs = sync.load_manifest(MIND)
    assert sync.extract_block(text, sync.STANDARDS_BEGIN, sync.STANDARDS_END) == sync.render_standards_policy(POLICY, specs[MIND.name])


def test_writer_appends_preserving_original_bytes_and_is_idempotent(tmp_path):
    original = "# Guidance\n\nNo generated anchors."
    path = repo(tmp_path, "OrganCore", original)
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    once = path.read_bytes()
    assert once.startswith(original.encode())
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert once == path.read_bytes()
    assert sync.check_standards_blocks(tmp_path, REPOS, POLICY) == []


def test_replacement_preserves_other_blocks_and_surrounding_text(tmp_path):
    prefix = "# Guidance\n<!-- repos_sync:map:begin -->\nstale map\n<!-- repos_sync:map:end -->\n"
    suffix = "\nKeep trailing details exactly."
    path = repo(tmp_path, "LibAlpha", prefix + block().replace("on demand", "always") + suffix)
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert path.read_text() == prefix + block() + suffix


@pytest.mark.parametrize("body,expected", [("# Guidance\n", "no shared-standards block"),
    (block().replace("on demand", "always"), "stale"),
    (sync.STANDARDS_BEGIN + "\nmissing end", "malformed"),
    (sync.STANDARDS_END + "\n" + sync.STANDARDS_BEGIN, "malformed"),
    (block() + block(), "duplicate")])
def test_checker_reports_missing_stale_and_malformed(tmp_path, body, expected):
    repo(tmp_path, "LibAlpha", body)
    problems = sync.check_standards_blocks(tmp_path, REPOS, POLICY)
    assert len(problems) == 1 and expected in problems[0]


def test_present_checkout_without_agents_is_a_failure(tmp_path):
    (tmp_path / "LibAlpha").mkdir()
    assert "no AGENTS.md" in sync.check_standards_blocks(tmp_path, REPOS, POLICY)[0]
    with pytest.raises(ValueError, match="no AGENTS.md"):
        sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert not (tmp_path / "LibAlpha/AGENTS.md").exists()


def test_writer_preflights_all_targets_before_mutation(tmp_path):
    repo(tmp_path, "OrganCore")
    repo(tmp_path, "LibAlpha", sync.STANDARDS_BEGIN)
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="malformed"):
        sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert snapshot(tmp_path) == before


def test_partial_checkout_is_reported_as_unverified(tmp_path, monkeypatch, capsys):
    repo(tmp_path, "LibAlpha", block())
    assert cli(tmp_path, monkeypatch, "--check", "--only", sync.STANDARDS_BLOCKS) == 0
    out = capsys.readouterr().out
    assert "1 of 2 selected registered repos checked out" in out
    assert "checkout absent, adoption unverified: OrganCore" in out


@pytest.mark.parametrize("flags", [
    ["--only", "typo"], ["--skip", "typo"],
    ["--only", sync.STANDARDS_BLOCKS, "--repo", "Unknown"],
    ["--repo", "LibAlpha"],
    ["--only", sync.FILING_BLOCKS, "--repo", "LibAlpha"],
])
def test_invalid_selection_never_writes(tmp_path, monkeypatch, flags):
    repo(tmp_path, "OrganCore")
    repo(tmp_path, "LibAlpha")
    before = snapshot(tmp_path)
    assert cli(tmp_path, monkeypatch, "--write", *flags) != 0
    assert snapshot(tmp_path) == before


def test_scoped_write_touches_only_selected_agents(tmp_path, monkeypatch):
    repo(tmp_path, "OrganCore")
    repo(tmp_path, "LibAlpha")
    rootfile = tmp_path / "AGENTS.md"
    rootfile.write_text("no routing markers")
    before = snapshot(tmp_path)
    def forbidden(*_args, **_kwargs):
        raise AssertionError("unrelated generator invoked")
    for name in ("write_root_marker", "write_block", "write_codex_hooks", "write_session_hooks", "remove_claude_md_pointers"):
        monkeypatch.setattr(sync, name, forbidden)
    monkeypatch.setattr(sync.smoke_sync, "write", forbidden)
    assert cli(tmp_path, monkeypatch, "--write", "--only", sync.STANDARDS_BLOCKS, "--repo", "LibAlpha") == 0
    after = snapshot(tmp_path)
    assert {name for name in before if before[name] != after[name]} == {Path("LibAlpha/AGENTS.md")}
    assert before.keys() == after.keys()


def test_repeated_repo_scope_checks_both_targets(tmp_path, monkeypatch):
    repo(tmp_path, "OrganCore", block(REPOS["OrganCore"]))
    repo(tmp_path, "LibAlpha")
    assert cli(tmp_path, monkeypatch, "--only", sync.STANDARDS_BLOCKS,
               "--repo", "OrganCore", "--repo", "LibAlpha") == 1


def test_skipped_only_leg_does_not_write(tmp_path, monkeypatch):
    repo(tmp_path, "OrganCore")
    before = snapshot(tmp_path)
    assert cli(tmp_path, monkeypatch, "--write", "--only", sync.STANDARDS_BLOCKS,
               "--skip", sync.STANDARDS_BLOCKS, "--repo", "OrganCore") == 0
    assert before == snapshot(tmp_path)


def test_cli_malformed_markers_fail_without_writes(tmp_path, monkeypatch):
    repo(tmp_path, "OrganCore")
    repo(tmp_path, "LibAlpha", sync.STANDARDS_END)
    before = snapshot(tmp_path)
    assert cli(tmp_path, monkeypatch, "--write", "--only", sync.STANDARDS_BLOCKS) != 0
    assert before == snapshot(tmp_path)


def test_invalid_owner_metadata_fails_without_writes(tmp_path, monkeypatch):
    repo(tmp_path, "OrganCore")
    before = snapshot(tmp_path)
    monkeypatch.setitem(REPOS, "OrganCore", {"board_owner": "true"})
    assert cli(tmp_path, monkeypatch, "--write", "--only", sync.STANDARDS_BLOCKS) != 0
    assert before == snapshot(tmp_path)


def test_grouped_target_uses_resolver(tmp_path, monkeypatch):
    path = repo(tmp_path / "family", "LibAlpha")
    monkeypatch.setattr(sync, "repo_checkout", lambda root, name: root / "family" / name)
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert sync.check_standards_blocks(tmp_path, REPOS, POLICY) == []
    assert sync.STANDARDS_BEGIN in path.read_text()


def test_ci_grades_standards_universally_on_cloned_mains():
    """The staged rollout (#474) is complete, so the broad drift legs grade the
    standards block on every cloned main; the hermetic generator step stays."""
    data = yaml.safe_load((MIND / ".github/workflows/firewall_gate.yml").read_text())
    steps = next(iter(data["jobs"].values()))["steps"]
    target = [step for step in steps if step.get("name") == "Shared standards generator and Mind-owned block"][0]
    assert 'test_repos_sync_standards_block.py' in target['run']
    assert '--repo PyAutoMind' in target['run']
    broad = [step for step in steps if step.get("name", "").startswith("Drift check")]
    assert len(broad) == 2
    for step in broad:
        assert sync.STANDARDS_BLOCKS not in step['run']


@pytest.mark.parametrize("kind", ["checkout", "family", "agents", "agents-inside"])
def test_writer_rejects_symlink_alias_before_any_mutation(tmp_path, kind, monkeypatch):
    selected = tmp_path / "selected"
    selected.mkdir()
    repo(selected, "OrganCore")
    outside = tmp_path / "unselected"
    outside.mkdir()
    victim = repo(outside, "LibAlpha")
    if kind == "checkout":
        (selected / "LibAlpha").symlink_to(victim.parent, target_is_directory=True)
    elif kind == "family":
        (selected / "family").symlink_to(outside, target_is_directory=True)
        monkeypatch.setattr(sync, "repo_checkout", lambda root, name:
                            root / "family" / name if name == "LibAlpha" else root / name)
    else:
        target = selected / "LibAlpha"
        target.mkdir()
        if kind == "agents-inside":
            victim = target / "other.md"
            victim.write_text("Keep exact contents.\n")
        (target / "AGENTS.md").symlink_to(victim)
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="symlink|escapes"):
        sync.write_standards_blocks(selected, REPOS, POLICY)
    assert snapshot(tmp_path) == before


def test_cli_rejects_selected_checkout_alias_before_unrelated_writes(tmp_path, monkeypatch):
    victim = repo(tmp_path / "unselected", "LibAlpha")
    root = tmp_path / "selected"
    root.mkdir()
    repo(root, "OrganCore")
    (root / "LibAlpha").symlink_to(victim.parent, target_is_directory=True)
    before = snapshot(tmp_path)
    assert cli(root, monkeypatch, "--write", "--only", sync.STANDARDS_BLOCKS) != 0
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("existing", [False, True])
def test_writer_preserves_crlf_bytes_outside_block(tmp_path, existing):
    prefix = "# Guidance\r\n\r\nPreserve é and line endings.\r\n"
    suffix = "Keep trailing CRLF.\r\n"
    original = prefix + ((block().replace("on demand", "always").replace("\n", "\r\n")) if existing else "") + suffix
    path = repo(tmp_path, "LibAlpha")
    path.write_bytes(original.encode("utf-8"))
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    after = path.read_bytes()
    assert after.startswith(prefix.encode("utf-8"))
    if existing:
        assert after.endswith(suffix.encode("utf-8"))
    else:
        assert after.startswith(original.encode("utf-8"))
    assert b"\n" not in after.replace(b"\r\n", b"")
    assert sync.check_standards_blocks(tmp_path, REPOS, POLICY) == []
    sync.write_standards_blocks(tmp_path, REPOS, POLICY)
    assert path.read_bytes() == after
