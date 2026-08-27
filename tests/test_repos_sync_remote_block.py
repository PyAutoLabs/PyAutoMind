"""The remote-session block is generated, so no organ can be born without it.

Three passes of mobile-performance review in a row found a repo whose copy of
this guidance had not learned what the previous pass measured — and one of them
found two organs still shipping a bug an earlier pass had fixed, in a file that
looked like cosmetic drift and was executable. The text was hand-written per
repo because the copies genuinely differed: each named its own test count, its
own timings, its own declared deps.

Those per-repo halves are the thing that rots, so the canonical text has none of
them, and this file pins that: a number in every repo's always-loaded context is
worse than no number as soon as it is wrong.

Conventions, as in the sibling repos_sync tests:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]
CANON = repos_sync.load_remote_sessions(MIND)

REPOS = {"OrganCore": {"category": "organ"}, "LibAlpha": {"category": "library"}}


def _repo(root, name, body):
    (root / name).mkdir(parents=True, exist_ok=True)
    (root / name / "AGENTS.md").write_text(body)


def _blocked(text):
    return f"# OrganCore\n\n{repos_sync.REMOTE_BEGIN}\n{text}\n{repos_sync.REMOTE_END}\n"


def test_a_repo_carrying_the_canonical_text_is_clean(tmp_path):
    _repo(tmp_path, "OrganCore", _blocked(CANON))
    assert repos_sync.check_remote_blocks(tmp_path, REPOS, CANON) == []


def test_a_stale_copy_is_drift(tmp_path):
    stale = CANON.replace("unconditionally", "if pytest misbehaves")
    assert stale != CANON
    _repo(tmp_path, "OrganCore", _blocked(stale))
    problems = repos_sync.check_remote_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "OrganCore" in problems[0]
    assert "--write" in problems[0]


def test_a_repo_without_the_markers_is_skipped_not_failed(tmp_path):
    """Opt-in: a session that cannot see an organ must not fail on its behalf.

    Half of the organs are attached in a typical remote session, and the check
    runs there as well as in CI.
    """
    _repo(tmp_path, "OrganCore", "# OrganCore\n\nno markers here\n")
    assert repos_sync.check_remote_blocks(tmp_path, REPOS, CANON) == []


def test_a_repo_that_is_not_checked_out_is_skipped(tmp_path):
    assert repos_sync.check_remote_blocks(tmp_path, REPOS, CANON) == []


def test_write_fills_the_block_and_is_idempotent(tmp_path):
    _repo(tmp_path, "OrganCore", _blocked("stale text"))
    agents = tmp_path / "OrganCore" / "AGENTS.md"

    repos_sync.write_block(agents, CANON, repos_sync.REMOTE_BEGIN,
                           repos_sync.REMOTE_END, required=False)
    assert repos_sync.check_remote_blocks(tmp_path, REPOS, CANON) == []
    once = agents.read_text()

    repos_sync.write_block(agents, CANON, repos_sync.REMOTE_BEGIN,
                           repos_sync.REMOTE_END, required=False)
    assert agents.read_text() == once


def test_the_canonical_text_carries_no_per_repo_numbers():
    """The reason it could not be generated before, removed rather than encoded.

    A test count or a timing is true of one repo on one day; generated into
    every repo's always-loaded context, it is a confident wrong answer in the
    other three the moment a suite grows.
    """
    offenders = [line for line in CANON.splitlines()
                 if re.search(r"\b\d+\s*(tests|s on|cores? and)\b", line)]
    assert not offenders, offenders


def test_the_text_names_the_three_things_a_session_must_do_first():
    for needle in ("session_bootstrap.sh", "-n auto", "GITHUB_ACCESS.md",
                   "is-ancestor"):
        assert needle in CANON, f"the block no longer mentions {needle}"
