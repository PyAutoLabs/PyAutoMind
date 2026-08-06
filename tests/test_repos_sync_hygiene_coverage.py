"""The hygiene conductor's repo coverage must not drift from the body map.

The conductor once held its scanned repos as bash arrays. They drifted — five
libraries where the map declared six, four organs of seven — and nothing caught
it, because a repo that is never scanned produces no findings and so reads as a
clean bill of health. The tenant firewall could not catch it either: its entry
for the conductor ALLOWLISTED the stale names rather than checking coverage.

`check_hygiene_coverage` is the check that closes that gap, and these are its
contract tests. Two things they deliberately do:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template (see `test_spawn_privacy.py`), so nothing here names a real
   repository. It also keeps the tests hermetic — they assert the check's logic,
   not the state of whatever happens to be checked out.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration. Every
   leg below is driven with input that must trip it.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

HYGIENE_REL = "PyAutoBrain/agents/conductors/hygiene"

# A fictional organism: two libraries, one organ, one workspace.
MANIFEST = {
    "LibAlpha": {"category": "library"},
    "LibBeta": {"category": "library"},
    "OrganCore": {"category": "organ"},
    "wsalpha_workspace": {"category": "workspace"},
}

DERIVED_OK = {
    "library": ["LibAlpha", "LibBeta"],
    "organ": ["OrganCore"],
    "workspace": ["wsalpha_workspace"],
}

# A conductor that derives its sets — no repo name in any array literal.
CLEAN_SCRIPT = """\
#!/usr/bin/env bash
mapfile -t LIB_REPOS < <(_body_map library)
mapfile -t ORG_REPOS < <(_body_map organ)
CODE_REPOS=("${LIB_REPOS[@]}" "${ORG_REPOS[@]}")
"""


def _stub_helper(derived, exit_code=0):
    """A stand-in for _hygiene_repos.py that prints whatever we hand it."""
    return (
        "import json, sys\n"
        f"if {exit_code}:\n"
        f"    sys.exit({exit_code})\n"
        f"print(json.dumps({derived!r}))\n"
    )


def _tree(tmp_path, *, derived=None, script=CLEAN_SCRIPT, exit_code=0, helper=True):
    hygiene = tmp_path / HYGIENE_REL
    hygiene.mkdir(parents=True)
    (hygiene / "hygiene.sh").write_text(script)
    if helper:
        (hygiene / "_hygiene_repos.py").write_text(
            _stub_helper(DERIVED_OK if derived is None else derived, exit_code)
        )
    mind = tmp_path / "PyAutoMind"
    mind.mkdir()
    return tmp_path, mind


def _check(tmp_path, **kwargs):
    root, mind = _tree(tmp_path, **kwargs)
    return repos_sync.check_hygiene_coverage(root, MANIFEST, mind)


def test_a_conductor_deriving_the_declared_sets_is_clean(tmp_path):
    assert _check(tmp_path) == []


def test_a_repo_missing_from_the_derived_set_is_drift(tmp_path):
    # The original bug: a declared library the conductor never scans.
    thinned = {**DERIVED_OK, "library": ["LibAlpha"]}

    problems = _check(tmp_path, derived=thinned)

    assert problems
    assert any("does not scan 'LibBeta'" in p for p in problems)


def test_a_repo_the_manifest_does_not_declare_is_drift(tmp_path):
    padded = {**DERIVED_OK, "organ": ["OrganCore", "OrganGhost"]}

    problems = _check(tmp_path, derived=padded)

    assert any("scans 'OrganGhost'" in p for p in problems)


def test_both_readers_are_exercised_so_the_pyyaml_free_path_cannot_rot(tmp_path):
    # The fallback runs only where PyYAML is absent, so nothing else verifies it.
    # Each reader is invoked separately and each is reported by name.
    problems = _check(tmp_path, derived={**DERIVED_OK, "library": []})

    assert any("(auto reader)" in p for p in problems)
    assert any("(minimal reader)" in p for p in problems)


def test_a_hardcoded_repo_name_in_an_array_is_drift(tmp_path):
    # Leg B: what stops a future edit from "simplifying" the derivation away.
    script = 'LIB_REPOS=(LibAlpha LibBeta)\nORG_REPOS=(OrganCore)\n'

    problems = _check(tmp_path, script=script)

    assert any("hardcoded in an array" in p and "LibAlpha" in p for p in problems)


def test_an_array_built_from_other_arrays_is_not_drift(tmp_path):
    # Composition is how the derived sets are assembled; it must stay legal.
    script = 'SCAN_REPOS=("${LIB_REPOS[@]}" "${WS_REPOS[@]}")\n'

    assert _check(tmp_path, script=script) == []


def test_a_helper_that_cannot_read_the_body_map_is_drift(tmp_path):
    # Exiting non-zero means the conductor would scan nothing at all — the
    # loudest possible version of this bug, and it must not pass silently.
    problems = _check(tmp_path, exit_code=3)

    assert problems
    assert any("cannot read the body map" in p for p in problems)


def test_the_check_skips_when_the_brain_is_not_checked_out(tmp_path):
    # Partial/web checkouts are normal; missing organs are skipped, never failed.
    mind = tmp_path / "PyAutoMind"
    mind.mkdir()

    assert repos_sync.check_hygiene_coverage(tmp_path, MANIFEST, mind) == []


def test_the_real_conductor_matches_the_real_body_map():
    """The live tree, if it is checked out here."""
    mind_root = Path(__file__).resolve().parents[1]
    root = mind_root.parent
    if not (root / HYGIENE_REL / "hygiene.sh").exists():
        return  # Brain not present in this environment
    _, repos = repos_sync.load_manifest(mind_root)

    assert repos_sync.check_hygiene_coverage(root, repos, mind_root) == []
