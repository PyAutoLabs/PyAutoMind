"""Which directory `repos_sync` and `spawn` act on when no `--root` is given.

Both used to answer "the directory above this checkout", which is only true
while the checkouts sit side by side directly under the root. The answer now
comes from PyAutoBrain's shared resolver (`agents/_pyauto_root.py`), so a
workspace that groups its checkouts into subdirectories still resolves to the
root that carries the `.pyauto-root` marker — and there is one answer to the
question instead of one per consumer.

Two properties matter enough to pin:

* **Nothing is required.** No Brain checkout beside us, or no marker anywhere,
  must still yield a usable root — the old answer — because a CI matrix and a
  single-repo web session both look exactly like that.
* **The resolver is Brain-anchored.** It walks up from the BRAIN checkout, so a
  worktree bundle whose PyAutoBrain is a symlink into the canonical workspace
  resolves to the canonical root. Acting on it would regenerate somebody
  else's tree from this checkout's manifest, so a root that does not hold this
  very checkout is refused — unless the operator named it explicitly.

Fictional fixtures only (`tests/**` is copied verbatim into the public
template); the stub resolver below stands in for the real module so the
behaviour under test is this script's, not the Brain's.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

STUB = '''\
"""A stand-in for PyAutoBrain/agents/_pyauto_root.py."""
from pathlib import Path

ROOT_MARKER = "{marker}"


def workspace_root_reason():
    return Path(r"{root}"), "stub"
'''


@pytest.fixture(autouse=True)
def forget_the_resolver():
    """Each test brings its own stub; the import cache must not leak."""
    before = list(sys.path)
    repos_sync._RESOLVER.clear()
    sys.modules.pop("_pyauto_root", None)
    yield
    repos_sync._RESOLVER.clear()
    sys.modules.pop("_pyauto_root", None)
    sys.path[:] = before


def make_mind(root, name="PyAutoMind"):
    mind = root / name
    mind.mkdir(parents=True)
    return mind


def install_stub(workspace, resolved, marker=".pyauto-root"):
    agents = workspace / "PyAutoBrain" / "agents"
    agents.mkdir(parents=True)
    (agents / "_pyauto_root.py").write_text(
        STUB.format(root=resolved, marker=marker)
    )


def test_without_a_brain_checkout_the_root_is_the_parent(tmp_path):
    """A Mind-only clone, a spawned template, a workspace whose Brain has not
    been cloned yet: the pre-resolver answer, which is still a real directory."""
    mind = make_mind(tmp_path / "workspace")
    assert repos_sync.workspace_root(mind) == tmp_path / "workspace"
    assert repos_sync.root_marker(mind) == repos_sync.ROOT_MARKER_FALLBACK


def test_the_resolver_decides_when_it_can_see_this_checkout(tmp_path):
    workspace = tmp_path / "workspace"
    mind = make_mind(workspace)
    install_stub(workspace, workspace, marker=".stub-root")
    assert repos_sync.workspace_root(mind) == workspace
    # The marker's NAME comes from the resolver too — two spellings of the
    # filename would be two answers to the same question.
    assert repos_sync.root_marker(mind) == ".stub-root"


def test_a_root_that_does_not_hold_this_checkout_is_refused(tmp_path):
    """The symlinked-Brain bundle: the resolver lands on another workspace, and
    acting on it would regenerate that one from this manifest."""
    bundle = tmp_path / "bundle"
    canonical = tmp_path / "canonical"
    make_mind(canonical)
    mind = make_mind(bundle)
    install_stub(bundle, canonical)
    assert repos_sync.workspace_root(mind) == bundle


def test_an_explicit_override_is_never_second_guessed(tmp_path, monkeypatch):
    """`PYAUTO_ROOT` is the operator pointing the tooling somewhere; the
    resolver takes it verbatim and so does the guard above."""
    bundle = tmp_path / "bundle"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    mind = make_mind(bundle)
    install_stub(bundle, elsewhere)
    monkeypatch.setenv("PYAUTO_ROOT", str(elsewhere))
    assert repos_sync.workspace_root(mind) == elsewhere
