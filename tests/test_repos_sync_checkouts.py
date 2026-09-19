"""The drift check must see BOTH directions of "is what is declared here?".

Two blind spots, mirror images of each other:

1. **Declared but missing was silently skipped.** Every leg that reads a repo
   skips one that is not checked out — right for that leg, which has nothing to
   read, and wrong in aggregate: after a regroup that left a repo behind,
   eleven checks would report `OK` having inspected nothing, and a successful
   check that means reduced coverage is worse than no check.
2. **On disk but undeclared was silence.** The script walks the manifest and
   asks whether each entry is present, so it structurally could not see a
   checkout that no entry declares — invisible to every manifest-driven sweep,
   including the audit whose whole job was to answer "did we miss a repo?".

The same conventions as the repos_sync tests next door:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository and the assertions
   are about the leg's logic rather than whatever happens to be checked out.
2. **Prove each leg FAILS.** Both directions are driven with input that must
   trip them — a check that cannot fail is decoration.
"""

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MARKER = ".pyauto-root"

REPOS = {
    "OrganOne": {"github": "FictionalOrg/OrganOne", "category": "organ"},
    "LibTwo": {"github": "FictionalOrg/LibTwo", "category": "library"},
}


def make_checkout(root, name):
    """A directory that looks like a git checkout (a clone's `.git` is a
    directory; a worktree's is a file — the leg accepts either)."""
    repo = root / name
    repo.mkdir(parents=True)
    (repo / ".git").mkdir()
    return repo


def make_root(tmp_path, *, marked=True, names=tuple(REPOS)):
    root = tmp_path / "workspace"
    root.mkdir()
    if marked:
        (root / MARKER).write_text(repos_sync.ROOT_MARKER_TEXT)
    for name in names:
        make_checkout(root, name)
    return root


def check(root, repos=REPOS, unmapped=()):
    return repos_sync.check_checkouts(root, repos, list(unmapped), MARKER)


# --- manifest -> disk ------------------------------------------------------


def test_a_fully_checked_out_workspace_is_clean(tmp_path):
    assert check(make_root(tmp_path)) == []


def test_a_declared_repo_that_is_not_checked_out_is_drift(tmp_path):
    root = make_root(tmp_path, names=("OrganOne",))
    problems = check(root)
    assert len(problems) == 1
    assert "LibTwo" in problems[0] and "not checked out" in problems[0]


def test_a_file_where_a_repo_should_be_is_still_missing(tmp_path):
    """"Present" means a directory. A leftover file of the same name is not a
    checkout, and reading it as one is how a half-finished regroup passes."""
    root = make_root(tmp_path, names=("OrganOne",))
    (root / "LibTwo").write_text("moved\n")
    assert len(check(root)) == 1


# --- disk -> manifest ------------------------------------------------------


def test_a_checkout_the_manifest_does_not_declare_is_drift(tmp_path):
    root = make_root(tmp_path)
    make_checkout(root, "stray_tool")
    problems = check(root)
    assert len(problems) == 1
    assert "stray_tool" in problems[0] and "does not" in problems[0]


def test_a_declared_neighbour_is_not_drift(tmp_path):
    """`unmapped_checkouts:` is how a checkout that is deliberately NOT a
    body-map repo says so — the only alternative to a hard-coded skip list."""
    root = make_root(tmp_path)
    make_checkout(root, "stray_tool")
    assert check(root, unmapped=["stray_tool"]) == []


def test_a_directory_that_is_not_a_checkout_is_ignored(tmp_path):
    """Scratch directories at the root are not repos and never were; requiring
    them to be declared would make the leg go red on everybody's junk."""
    root = make_root(tmp_path)
    (root / "scratch").mkdir()
    (root / "notes.md").write_text("# notes\n")
    assert check(root) == []


def test_a_worktree_style_checkout_counts_too(tmp_path):
    root = make_root(tmp_path)
    (root / "stray_worktree").mkdir()
    (root / "stray_worktree" / ".git").write_text("gitdir: /elsewhere\n")
    assert len(check(root)) == 1


def test_both_directions_are_reported_together(tmp_path):
    root = make_root(tmp_path, names=("OrganOne",))
    make_checkout(root, "stray_tool")
    problems = check(root)
    assert len(problems) == 2
    assert any("LibTwo" in p for p in problems)
    assert any("stray_tool" in p for p in problems)


# --- what the leg may be held to ------------------------------------------


def test_an_unmarked_root_is_not_held_to_the_manifest(tmp_path):
    """The CI layout: a handful of repos cloned side by side with no root above
    them. "You are missing thirty repos" is noise there, not drift — and no
    assertion anywhere may REQUIRE the marker to exist."""
    root = make_root(tmp_path, marked=False, names=("OrganOne",))
    make_checkout(root, "stray_tool")
    assert check(root) == []


def test_the_counts_say_what_was_seen_and_whether_it_was_enforced(tmp_path):
    root = make_root(tmp_path, names=("OrganOne",))
    assert repos_sync.checkout_counts(root, REPOS, MARKER) == (1, 2, True)
    (root / MARKER).unlink()
    assert repos_sync.checkout_counts(root, REPOS, MARKER) == (1, 2, False)


def test_grouped_manifest_is_checked_in_both_directions(tmp_path, monkeypatch):
    root = make_root(tmp_path, names=("OrganOne",))
    write_manifest(root / "PyAutoMind", """categories: {}
repos:
  OrganOne:
    category: organ
  LibTwo:
    path: family/LibTwo
    category: library
""")
    grouped = make_checkout(root / "family", "LibTwo")

    class Resolver:
        def repo_path(self, _root, name):
            return {"OrganOne": root / "OrganOne", "LibTwo": grouped}[name]

        def iter_checkouts(self, _root):
            return [path for path in (root / "OrganOne", grouped,
                                      root / "family" / "stray_tool")
                    if (path / ".git").exists()]

    monkeypatch.setattr(repos_sync, "_repo_resolver", lambda _root: Resolver())
    assert check(root) == []
    make_checkout(root / "family", "stray_tool")
    assert "stray_tool" in check(root)[0]
    assert "stray_tool" in check(root, unmapped=["stray_tool"])[0]
    (root / "family" / "LibTwo" / ".git").rmdir()
    assert any("LibTwo" in problem and "not checked out" in problem
               for problem in check(root))


def test_grouped_and_flat_duplicate_identity_fails(tmp_path, monkeypatch):
    root = make_root(tmp_path)
    make_checkout(root / "family", "LibTwo")

    class AmbiguousResolver:
        def repo_path(self, _root, name):
            if name == "LibTwo":
                raise ValueError("LibTwo: ambiguous checkouts")
            return root / name

    monkeypatch.setattr(repos_sync, "_repo_resolver", lambda _root: AmbiguousResolver())
    with pytest.raises(ValueError, match="ambiguous"):
        check(root)


# --- the marker is generated, and generating it is what arms the leg -------


def test_write_root_marker_creates_then_leaves_the_marker(tmp_path, capsys):
    root = tmp_path / "workspace"
    root.mkdir()
    repos_sync.write_root_marker(root, MARKER)
    assert (root / MARKER).read_text() == repos_sync.ROOT_MARKER_TEXT
    assert capsys.readouterr().out.startswith("wrote:")
    repos_sync.write_root_marker(root, MARKER)
    assert capsys.readouterr().out.startswith("unchanged:")


def test_the_bootstrap_is_additive(tmp_path):
    """The chain has to close: the leg needs the marker, the marker is written
    by --write, and --write itself resolves the root. With no marker the root
    still resolves (the parent of a checkout) and the leg simply does not
    enforce; writing the marker is what arms it for every later run."""
    root = make_root(tmp_path, marked=False, names=("OrganOne",))
    assert check(root) == []
    repos_sync.write_root_marker(root, MARKER)
    assert len(check(root)) == 1


def test_the_generated_marker_names_no_particular_workspace(tmp_path):
    """It is written into a directory that belongs to no repository, and
    `scripts/` is copied verbatim into the public template — so the text may
    describe the mechanism and nothing about this instance."""
    text = repos_sync.ROOT_MARKER_TEXT
    assert text.startswith("# Workspace root marker.")
    # It says how it is generated, and no longer says to create one by hand.
    assert "repos_sync.py --write" in text
    assert "rather than by hand" in text
    assert "/home/" not in text and "~/" not in text


# --- the manifest key ------------------------------------------------------


def write_manifest(mind_root, body):
    mind_root.mkdir(parents=True, exist_ok=True)
    (mind_root / "repos.yaml").write_text(body)
    return mind_root


def test_unmapped_checkouts_defaults_to_none(tmp_path):
    mind = write_manifest(tmp_path / "TheMind", "categories: {}\nrepos: {}\n")
    assert repos_sync.load_unmapped_checkouts(mind) == []


def test_unmapped_checkouts_is_read_from_the_manifest(tmp_path):
    mind = write_manifest(
        tmp_path / "TheMind",
        "categories: {}\nunmapped_checkouts:\n  - .profile_repo\nrepos: {}\n",
    )
    assert repos_sync.load_unmapped_checkouts(mind) == [".profile_repo"]
