"""Contract tests for `lifecycle.py epics [--retire]`.

epics.md is a live board — the dashboard renders every entry with a "continue
the epic" prompt — and until this verb existed nothing ever took an entry off
it, so programmes that had shipped kept inviting a session to resume them.
Retirement is destructive (an entry leaves the board, a ledger moves), so the
tests below pin BOTH halves: what must be retired, and what must be left
exactly as it was.

Same two rules as `test_lifecycle_check.py`:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template (`test_spawn_privacy.py`), so no real epic, repo or ledger
   is named here. It also keeps the tests hermetic.
2. **Prove each leg FAILS.** A "done" detector that cannot say no is
   decoration, so the not-done statuses are driven through the same path and
   must survive untouched.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402


HEADER = """# Epics

Fictional header prose that must survive every retirement untouched.

Schema per entry: `## <slug>` then `- title:` / `- ledger:` / `- notes:`.

"""

RUNNING = """## kite-weaving
- title: Kite weaving — the long programme
- ledger: draft/feature/widgets/kite_weaving.md
- notes: still going.

"""

MID_STATUS = """## lantern-relay
- title: Lantern relay
- ledger: draft/feature/widgets/lantern_relay.md
- status: phase 2 SHIPPED 2031-04-04; phase 3 open
- notes: a status that MENTIONS a shipped phase is not a retired epic.

"""

SHIPPED_DRAFT = """## pebble-sorting
- title: Pebble sorting — done and dusted
- ledger: draft/feature/widgets/pebble_sorting.md
- status: SHIPPED 2031-05-05 — every phase complete.
  Continuation lines belong to the status value.
- notes: fictional.

"""

DONE_EXTERNAL = """## thimble-census
- title: Thimble census
- ledger: OtherFictionalRepo/results/thimble/PROGRAMME.md
- status: complete 2031-06-06 — lowercase status, ledger in another repo.
- notes: fictional.

"""

DONE_DATED = """## quill-audit
- title: Quill audit
- ledger: complete/2031/07/quill-audit.md
- status: COMPLETE 2031-07-07.
- notes: fictional.

"""

DONE_ARCHIVED = """## marble-run
- title: Marble run
- ledger: complete/archive/epics/marble_run.md
- status: SHIPPED 2031-08-08.
- notes: fictional.

"""


def _mind(root: Path, body: str, *, ledgers=()) -> Path:
    """A fictional Mind holding one epics.md plus any ledger files it names."""
    (root / "epics.md").write_text(body)
    for rel in ledgers:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# fictional ledger\n\nphases for {Path(rel).stem}.\n")
    return root


# --------------------------------------------------------------------------- #
# parsing
# --------------------------------------------------------------------------- #
def test_blocks_preserve_header_and_entry_text(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + SHIPPED_DRAFT)
    header, blocks = lifecycle.epic_blocks(tmp_path / "epics.md")

    assert "\n".join(header).startswith("# Epics")
    assert [slug for slug, _ in blocks] == ["kite-weaving", "pebble-sorting"]
    # verbatim: the block is exactly the source text of that entry
    assert "\n".join(blocks[0][1]).rstrip("\n") == RUNNING.rstrip("\n")


def test_fields_take_the_first_value_and_ignore_continuations(tmp_path):
    _mind(tmp_path, HEADER + SHIPPED_DRAFT)
    _, blocks = lifecycle.epic_blocks(tmp_path / "epics.md")
    fields = lifecycle.epic_fields(blocks[0][1])

    assert fields["title"] == "Pebble sorting — done and dusted"
    assert fields["ledger"] == "draft/feature/widgets/pebble_sorting.md"
    assert fields["status"].startswith("SHIPPED 2031-05-05")


# --------------------------------------------------------------------------- #
# done detection — and the cases that must NOT trip it
# --------------------------------------------------------------------------- #
def test_done_detection(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + MID_STATUS + SHIPPED_DRAFT + DONE_EXTERNAL)
    _, blocks = lifecycle.epic_blocks(tmp_path / "epics.md")
    verdict = {slug: lifecycle.epic_is_done(lifecycle.epic_fields(b))
               for slug, b in blocks}

    assert verdict == {
        "kite-weaving": False,     # no status at all
        "lantern-relay": False,    # SHIPPED only mid-status
        "pebble-sorting": True,    # SHIPPED prefix
        "thimble-census": True,    # lowercase complete prefix
    }


# --------------------------------------------------------------------------- #
# report mode
# --------------------------------------------------------------------------- #
def test_report_mode_lists_done_entries_and_moves_nothing(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + SHIPPED_DRAFT,
          ledgers=["draft/feature/widgets/pebble_sorting.md"])
    before = (tmp_path / "epics.md").read_text()

    done = lifecycle.retire_epics(tmp_path, apply=False)

    assert [d["slug"] for d in done] == ["pebble-sorting"]
    assert (tmp_path / "epics.md").read_text() == before
    assert (tmp_path / "draft/feature/widgets/pebble_sorting.md").exists()
    assert not (tmp_path / "complete/archive/epics").exists()


def test_report_mode_is_quiet_when_nothing_is_done(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + MID_STATUS)
    assert lifecycle.retire_epics(tmp_path, apply=False) == []


# --------------------------------------------------------------------------- #
# retire — a draft/ ledger follows its epic into the archive
# --------------------------------------------------------------------------- #
def test_retire_moves_a_draft_ledger_and_appends_the_entry(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + MID_STATUS + SHIPPED_DRAFT,
          ledgers=["draft/feature/widgets/pebble_sorting.md"])

    done = lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")

    assert [d["archive"] for d in done] == ["complete/archive/epics/pebble_sorting.md"]
    archived = tmp_path / "complete/archive/epics/pebble_sorting.md"
    assert not (tmp_path / "draft/feature/widgets/pebble_sorting.md").exists()

    text = archived.read_text()
    assert text.startswith("# fictional ledger")           # the ledger body survives
    assert "## Retired from epics.md (2031-09-09)" in text
    assert SHIPPED_DRAFT.rstrip("\n") in text              # the entry text, verbatim

    # the board loses that entry and nothing else
    remaining = (tmp_path / "epics.md").read_text()
    assert "## pebble-sorting" not in remaining
    assert remaining == HEADER + RUNNING + MID_STATUS.rstrip("\n") + "\n"


def test_retire_leaves_untouched_entries_byte_identical(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + SHIPPED_DRAFT + MID_STATUS,
          ledgers=["draft/feature/widgets/pebble_sorting.md"])

    lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")
    remaining = (tmp_path / "epics.md").read_text()

    for kept in (HEADER, RUNNING, MID_STATUS.rstrip("\n") + "\n"):
        assert kept in remaining


def test_retire_moves_an_active_ledger_too(tmp_path):
    body = SHIPPED_DRAFT.replace("draft/feature/widgets/pebble_sorting.md",
                                 "active/pebble_sorting.md")
    _mind(tmp_path, HEADER + body, ledgers=["active/pebble_sorting.md"])

    lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")

    assert not (tmp_path / "active/pebble_sorting.md").exists()
    assert (tmp_path / "complete/archive/epics/pebble_sorting.md").exists()


# --------------------------------------------------------------------------- #
# retire — ledgers that are not ours to move
# --------------------------------------------------------------------------- #
def test_external_ledger_gets_a_slug_named_archive_file(tmp_path):
    _mind(tmp_path, HEADER + DONE_EXTERNAL)

    done = lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")

    assert [d["archive"] for d in done] == ["complete/archive/epics/thimble-census.md"]
    text = (tmp_path / "complete/archive/epics/thimble-census.md").read_text()
    assert text.startswith("# Thimble census\n")           # created with a heading
    assert DONE_EXTERNAL.rstrip("\n") in text
    assert (tmp_path / "epics.md").read_text() == HEADER.rstrip("\n") + "\n"


def test_dated_record_ledger_is_left_where_it_is(tmp_path):
    _mind(tmp_path, HEADER + DONE_DATED, ledgers=["complete/2031/07/quill-audit.md"])

    done = lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")

    assert [d["archive"] for d in done] == ["complete/archive/epics/quill-audit.md"]
    assert (tmp_path / "complete/2031/07/quill-audit.md").exists()   # frozen record
    assert DONE_DATED.rstrip("\n") in (
        tmp_path / "complete/archive/epics/quill-audit.md").read_text()


def test_already_archived_ledger_receives_the_entry_in_place(tmp_path):
    _mind(tmp_path, HEADER + DONE_ARCHIVED,
          ledgers=["complete/archive/epics/marble_run.md"])

    done = lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")

    assert [d["archive"] for d in done] == ["complete/archive/epics/marble_run.md"]
    text = (tmp_path / "complete/archive/epics/marble_run.md").read_text()
    assert text.startswith("# fictional ledger")
    assert DONE_ARCHIVED.rstrip("\n") in text
    assert not (tmp_path / "complete/archive/epics/marble-run.md").exists()


# --------------------------------------------------------------------------- #
# idempotence
# --------------------------------------------------------------------------- #
def test_second_retire_is_a_no_op(tmp_path):
    _mind(tmp_path, HEADER + RUNNING + SHIPPED_DRAFT,
          ledgers=["draft/feature/widgets/pebble_sorting.md"])

    lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-09")
    after_first = (tmp_path / "epics.md").read_text()
    archived = (tmp_path / "complete/archive/epics/pebble_sorting.md").read_text()

    assert lifecycle.retire_epics(tmp_path, apply=True, day="2031-09-10") == []
    assert (tmp_path / "epics.md").read_text() == after_first
    assert (tmp_path / "complete/archive/epics/pebble_sorting.md").read_text() == archived
