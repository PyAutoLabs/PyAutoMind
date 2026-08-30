"""The organ *config* surfaces must not drift from the body map.

Two mirrors sat unchecked while the file headers claimed otherwise:

1. **Heart `version_skew:`** — `<workspace repo>: {library, package}`. Every
   field is identity the body map owns, and `check_heart` read the polled-repo
   list, the owners and (since PyAutoMind#198) the `smoke:` block, but never
   this one. A workspace renamed in the map, or a library whose package name
   changed, would have skewed Heart silently.
2. **Hands `autohands/config/workspaces.yaml`** — its own header says "Repo
   IDENTITY must match PyAutoMind/repos.yaml (the body map); repos_sync.py
   --check flags drift". No leg read the file. The claim was aspirational from
   the day it was written.

Same two rules as the hygiene-coverage tests next door:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template (see `test_spawn_privacy.py`), so nothing here names a real
   repository, and the tests assert the checks' logic rather than the state of
   whatever happens to be checked out.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
   Every leg below is driven with input that must trip it.
"""

import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

HEART_REL = "PyAutoHeart/config/repos.yaml"
HANDS_REL = "PyAutoHands/autohands/config/workspaces.yaml"

# A fictional organism: two packaged libraries, one packaged organ, one library
# the map declares without a package, plus a workspace and a howto.
MANIFEST = {
    "OrganOne": {
        "github": "FictionalOrg/OrganOne",
        "category": "organ",
        "package": "organone",
    },
    "LibTwo": {
        "github": "FictionalOrg/LibTwo",
        "category": "library",
        "package": "libtwo",
    },
    "LibThree": {
        "github": "FictionalOrg/LibThree",
        "category": "library",
        "package": "libthree",
    },
    # Declared without a `package:` — the body map carries one only for the
    # libraries/organs that ship as a distribution.
    "LibFour": {"github": "FictionalOrg/LibFour", "category": "library"},
    "libtwo_workspace": {
        "github": "FictionalOrg/libtwo_workspace",
        "category": "workspace",
    },
    "HowToTwo": {"github": "FictionalOrg/HowToTwo", "category": "howto"},
}

HEART_REPOS = {
    "libraries": [
        {"name": "LibTwo", "owner": "FictionalOrg"},
        {"name": "LibThree", "owner": "FictionalOrg"},
    ],
    "workspaces": [{"name": "libtwo_workspace", "owner": "FictionalOrg"}],
}

VERSION_SKEW_OK = {
    "libtwo_workspace": {"library": "LibTwo", "package": "libtwo"},
    "HowToTwo": {"library": "LibThree", "package": "libthree"},
}

WORKSPACES_OK = {
    "run_all": {
        "libtwo": {"repo": "libtwo_workspace", "report": "libtwo"},
        "howtotwo": {"repo": "HowToTwo", "report": "howtotwo"},
    },
    "libraries": [
        {"name": "LibTwo", "package": "libtwo"},
        {"name": "LibThree", "package": "libthree"},
    ],
    "slow_skip_default": ["libtwo_workspace"],
}


def _heart(tmp_path, *, version_skew=..., repos=None):
    """Write a Heart config; `version_skew=None` omits the block entirely."""
    data = {"repos": HEART_REPOS if repos is None else repos}
    skew = VERSION_SKEW_OK if version_skew is ... else version_skew
    if skew is not None:
        data["version_skew"] = skew
    path = tmp_path / HEART_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data))
    return repos_sync.check_heart(tmp_path, MANIFEST)


def _hands(tmp_path, data=None):
    path = tmp_path / HANDS_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(WORKSPACES_OK if data is None else data))
    return repos_sync.check_hands_workspaces(tmp_path, MANIFEST)


# --------------------------------------------------------------------------
# Heart: version_skew
# --------------------------------------------------------------------------

def test_a_version_skew_block_matching_the_map_is_clean(tmp_path):
    assert _heart(tmp_path) == []


def test_a_version_skew_key_the_map_does_not_declare_is_drift(tmp_path):
    skew = {**VERSION_SKEW_OK, "ghost_workspace": {"library": "LibTwo",
                                                   "package": "libtwo"}}

    problems = _heart(tmp_path, version_skew=skew)

    assert any("ghost_workspace" in p and "not in the manifest" in p
               for p in problems)


def test_a_version_skew_library_the_map_does_not_declare_is_drift(tmp_path):
    # A library renamed in the body map leaves Heart comparing against nothing.
    skew = {"libtwo_workspace": {"library": "LibGhost", "package": "libtwo"}}

    problems = _heart(tmp_path, version_skew=skew)

    assert any("LibGhost" in p and "not in the manifest" in p
               for p in problems)


def test_a_version_skew_package_that_is_not_the_maps_package_is_drift(tmp_path):
    # The exact skew the check exists for: right library, stale import name.
    skew = {"libtwo_workspace": {"library": "LibTwo", "package": "libtwo_old"}}

    problems = _heart(tmp_path, version_skew=skew)

    assert any("libtwo_old" in p and "libtwo" in p for p in problems)


def test_a_version_skew_library_with_no_package_in_the_map_is_drift(tmp_path):
    # Nothing to compare against — the map does not claim this repo ships a
    # package, so Heart must not be asserting one.
    skew = {"libtwo_workspace": {"library": "LibFour", "package": "libfour"}}

    problems = _heart(tmp_path, version_skew=skew)

    assert any("LibFour" in p and "package" in p for p in problems)


def test_a_heart_config_without_a_version_skew_block_is_tolerated(tmp_path):
    # A Heart checkout predating the block is not drift; only Heart's own
    # loader decides whether it is required.
    assert _heart(tmp_path, version_skew=None) == []


def test_the_heart_leg_skips_when_heart_is_not_checked_out(tmp_path):
    # Partial/web checkouts are normal; a missing organ is skipped, not failed.
    assert repos_sync.check_heart(tmp_path, MANIFEST) == []


# --------------------------------------------------------------------------
# Hands: workspaces.yaml
# --------------------------------------------------------------------------

def test_a_workspaces_yaml_matching_the_map_is_clean(tmp_path):
    assert _hands(tmp_path) == []


def test_a_run_all_repo_the_map_does_not_declare_is_drift(tmp_path):
    data = {**WORKSPACES_OK, "run_all": {
        **WORKSPACES_OK["run_all"],
        "ghost": {"repo": "ghost_workspace", "report": "ghost"},
    }}

    problems = _hands(tmp_path, data)

    assert any("ghost_workspace" in p and "not in the manifest" in p
               for p in problems)


def test_a_libraries_name_the_map_does_not_declare_is_drift(tmp_path):
    data = {**WORKSPACES_OK,
            "libraries": [{"name": "LibGhost", "package": "libghost"}]}

    problems = _hands(tmp_path, data)

    assert any("LibGhost" in p and "not in the manifest" in p for p in problems)


def test_a_libraries_package_that_is_not_the_maps_package_is_drift(tmp_path):
    # The release board renders versions from this package name; a stale one
    # reads as "not on PyPI" rather than as drift.
    data = {**WORKSPACES_OK,
            "libraries": [{"name": "LibTwo", "package": "libtwo_old"}]}

    problems = _hands(tmp_path, data)

    assert any("libtwo_old" in p and "libtwo" in p for p in problems)


def test_a_slow_skip_default_repo_the_map_does_not_declare_is_drift(tmp_path):
    data = {**WORKSPACES_OK, "slow_skip_default": ["ghost_workspace"]}

    problems = _hands(tmp_path, data)

    assert any("ghost_workspace" in p for p in problems)


def test_the_hands_leg_skips_when_hands_is_not_checked_out(tmp_path):
    assert repos_sync.check_hands_workspaces(tmp_path, MANIFEST) == []


def test_the_hands_leg_is_registered_so_only_can_select_it(tmp_path):
    # --only selects by the printed label, and an unregistered leg never runs
    # however good the function is. `--only <unknown>` lists every registered
    # label, so it is the cheapest proof the leg is wired in.
    proc = subprocess.run(
        [sys.executable, str(Path(repos_sync.__file__)), "--check",
         "--root", str(tmp_path), "--only", "no-such-check"],
        capture_output=True, text=True,
    )

    assert proc.returncode != 0
    assert f"'{HANDS_REL}'" in proc.stderr


# --------------------------------------------------------------------------
# The live tree
# --------------------------------------------------------------------------

def test_the_real_organ_configs_match_the_real_body_map():
    """The live workspace, if it is checked out here."""
    mind_root = Path(__file__).resolve().parents[1]
    root = mind_root.parent
    _, repos = repos_sync.load_manifest(mind_root)

    assert repos_sync.check_heart(root, repos) == []
    assert repos_sync.check_hands_workspaces(root, repos) == []
