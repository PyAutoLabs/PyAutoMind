"""Local seed contract; all records and identities here are synthetic."""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('seed_spawn', ROOT / 'scripts/spawn.py')
spawn = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(spawn)


@pytest.fixture
def source(tmp_path):
    root = tmp_path / 'source'
    root.mkdir()
    files = {'README.md': 'Original guide', 'repos.yaml': 'private live identity',
             'AGENTS.md': '# Source instance\nRoute to SourceLab community. Require OptionalCampaignOrgan.\n',
             'active.md': '# private task entry', 'planned.md': 'private plan',
             'draft/feature/demo.md': 'private prompt',
             '.github/workflows/lifecycle_drift.yml': 'name: example',
             'scripts/lifecycle.py': (ROOT / 'scripts/lifecycle.py').read_text()}
    for name, content in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    return root


def test_minimal_empty_privacy_and_default_unchanged(source, tmp_path):
    minimal, default = tmp_path / 'minimal', tmp_path / 'full'
    spawn.generate_mind(source, minimal, minimal=True)
    spawn.generate_mind(source, default)
    assert yaml.safe_load((minimal / 'repos.yaml').read_text()) == {'categories': {}, 'repos': {}}
    assert (default / 'repos.yaml').read_text() == spawn.BODY_MAP_TEMPLATE
    assert (default / '.github/workflows/lifecycle_drift.yml').exists()
    assert not (minimal / '.github').exists()
    assert (minimal / 'complete/index.md').exists()
    assert not (minimal / 'draft/feature/demo.md').exists()
    assert 'private' not in (minimal / 'active.md').read_text()
    assert 'private' not in (minimal / 'planned.md').read_text()
    assert 'local' in (minimal / 'README.md').read_text().lower()
    instructions = (minimal / 'AGENTS.md').read_text()
    assert 'SourceLab' not in instructions
    assert 'OptionalCampaignOrgan' not in instructions
    assert 'No community destination is configured' in instructions
    assert 'needs neither an assistant' in instructions
    assert (default / 'AGENTS.md').read_bytes() == (source / 'AGENTS.md').read_bytes()


def test_dry_run_and_nonoverwrite(source, tmp_path):
    assert spawn.minimal_mind(source) == 0
    dest = tmp_path / 'mind'
    assert spawn.minimal_mind(source, dest) == 0
    record = dest / 'active.md'
    record.write_text('user records')
    instructions = dest / 'AGENTS.md'
    instructions.write_text('user-owned policy')
    with pytest.raises(ValueError, match='already exists'):
        spawn.minimal_mind(source, dest)
    assert record.read_text() == 'user records'
    assert instructions.read_text() == 'user-owned policy'
    link = tmp_path / 'link'
    link.symlink_to(tmp_path / 'absent')
    with pytest.raises(ValueError, match='already exists'):
        spawn.minimal_mind(source, link)
    assert link.is_symlink()


@pytest.mark.parametrize('unsafe', ['unmatched', 'canary'])
def test_unsafe_staging_never_creates_destination(source, tmp_path, unsafe):
    name = 'unclassified.extension' if unsafe == 'unmatched' else 'scripts/example.py'
    path = source / name
    path.parent.mkdir(exist_ok=True)
    path.write_text('example' if unsafe == 'unmatched' else spawn.CANARY_TOKENS[0])
    subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
    dest = tmp_path / 'refused'
    assert spawn.minimal_mind(source, dest) == spawn.EXIT_UNSAFE
    assert not dest.exists()


@pytest.mark.parametrize('option', ['--root', '--check', '--stamp-family'])
def test_incompatible_cli_options(tmp_path, option):
    dest = tmp_path / 'absent'
    run = subprocess.run([sys.executable, str(ROOT / 'scripts/spawn.py'),
                          '--minimal-mind', '--write', str(dest), option, str(tmp_path)],
                         capture_output=True, text=True)
    assert run.returncode == 2
    assert 'cannot combine' in run.stderr
    assert not dest.exists()
