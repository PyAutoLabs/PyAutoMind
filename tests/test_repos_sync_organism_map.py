"""The organism-map compensating control (PyAutoMind#486).

A PR that edits repos.yaml cannot make the eight organ copies of the map match
it (they regenerate after merge), so the firewall gate skips that leg on such
a PR and asserts instead the thing the PR does control: the manifest renders a
well-formed map.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]


def test_the_map_renders_from_the_manifest():
    categories, repos = repos_sync.load_manifest(MIND)
    smap = repos_sync.system_map(categories, repos)
    organs = [name for name, repo in repos.items() if repo["category"] == "organ"]
    assert organs
    for name in organs:
        assert name in smap, name
    for line in smap.splitlines():
        assert "\t" not in line


def test_every_role_is_one_bounded_line():
    """The root routing table and the map are rendered from `role`; a row that
    runs to a paragraph loads into every session and every delegated subagent."""
    _, repos = repos_sync.load_manifest(MIND)
    for name, repo in repos.items():
        role = repo.get("role") or ""
        assert "\n" not in role, name
        assert len(role) <= 400, (name, len(role))


def test_the_leg_is_registered_under_its_label():
    assert repos_sync.MAP_BLOCKS == "organism-map blocks (generated)"
