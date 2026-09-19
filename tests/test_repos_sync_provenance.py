"""Generated provenance must work from either workspace checkout layout."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import repos_sync  # noqa: E402


def test_routing_and_owner_provenance_use_mind_checkout():
    categories = {"organ": {"label": "Organ", "role": "example"}}
    repos = {"OrganOne": {"category": "organ", "path": "organs/OrganOne",
                          "github": "Example/OrganOne", "role": "example"}}
    for render in (repos_sync.routing_table, repos_sync.owner_map):
        text = render(categories, repos)
        assert "from the resolved mind checkout" in text.lower()
        assert "python3 scripts/repos_sync.py --write" in text
        assert "python3 PyAutoMind/scripts/repos_sync.py --write" not in text
