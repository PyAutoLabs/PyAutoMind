"""Contract tests for the task-date leg of `lifecycle.py`.

The Mind used to date only what it FINISHED — every `complete/` record carries
`completed:`, but a task that had merely been picked up carried no date a
reader could parse, so nothing could answer "what did we start recently?".
These tests pin the convention that fixed it: one machine-readable date field
per registry entry, an `Issued:` header on every issued prompt, and a backfill
that reconstructs both from evidence the repo already holds.

Same two rules as `test_lifecycle_check.py`:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repo, task or prompt.
2. **Prove each leg fails.** A backfill that cannot report a gap is
   decoration — every case below drives input that must trip it.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def _mind(root: Path, *, active=None, registries=None) -> Path:
    for name, body in (active or {}).items():
        p = root / "active" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    for name, body in (registries or {}).items():
        (root / name).write_text(body)
    return root


def _prompt(status="formalised", extra=""):
    return ("# Sprocket calibration\n\nType: feature\nTarget: flywheel\n"
            f"Difficulty: medium\nAutonomy: safe\nStatus: {status}\n{extra}"
            "\nBody prose about sprockets.\n")


# --------------------------------------------------------------------------- #
# reading a date back
# --------------------------------------------------------------------------- #
def test_the_key_names_the_event_not_just_the_date():
    """A bare timestamp says nothing; `- parked: <date>` says what happened."""
    assert lifecycle.entry_date({"parked": "2026-08-18 — deferred"}) == (
        "2026-08-18", "parked")


def test_the_most_specific_event_wins_when_an_entry_carries_several():
    """Filed, then issued: the task dates from the later, more specific event."""
    date, key = lifecycle.entry_date({"filed": "2026-07-01",
                                      "issued": "2026-08-19"})
    assert (date, key) == ("2026-08-19", "issued")


def test_a_date_buried_in_another_fields_prose_is_not_a_date():
    """`- issue: …/1501 (issued 2026-08-19)` is exactly the habit the
    convention replaces — invisible on purpose, so the gap gets reported."""
    fields = {"issue": "https://example.invalid/issues/1 (issued 2026-08-19)"}
    assert lifecycle.entry_date(fields) == (None, None)


def test_an_issued_prompt_carries_its_own_date_in_the_header():
    assert lifecycle.prompt_issued_date(
        _prompt(extra="Issued: 2026-08-19\n")) == "2026-08-19"


def test_a_date_deep_in_the_prompt_body_is_prose_not_a_header():
    body = _prompt() + "\n" * 40 + "Issued: 2026-08-19\n"
    assert lifecycle.prompt_issued_date(body) is None


# --------------------------------------------------------------------------- #
# reporting the gap
# --------------------------------------------------------------------------- #
def test_an_undated_entry_and_an_undated_prompt_are_both_reported(tmp_path):
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md": _prompt()},
                 registries={"active.md": "## sprocket-calibration\n"
                                          "- status: library-dev\n"})
    assert [e["slug"] for e in lifecycle.undated_entries(root)] == [
        "sprocket-calibration"]
    assert [f.name for f in lifecycle.undated_prompts(root)] == [
        "sprocket_calibration.md"]


def test_a_dated_registry_and_a_dated_prompt_report_nothing(tmp_path):
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md":
                         _prompt(extra="Issued: 2026-08-19\n")},
                 registries={"active.md": "## sprocket-calibration\n"
                                          "- issued: 2026-08-19\n"})
    assert lifecycle.undated_entries(root) == []
    assert lifecycle.undated_prompts(root) == []


# --------------------------------------------------------------------------- #
# backfilling it
# --------------------------------------------------------------------------- #
def test_backfill_reconstructs_a_prompt_date_from_the_registry_that_claims_it(tmp_path):
    """No git history to read here — the Mind's own record is the evidence,
    and the written date says so rather than passing itself off as observed."""
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md": _prompt()},
                 registries={"parked.md":
                             "## sprocket-calibration\n"
                             "- parked: 2026-08-18 — deferred\n"
                             "- prompt: active/sprocket_calibration.md\n"})
    results = lifecycle.backfill_dates(root, apply=True)
    written = (root / "active" / "sprocket_calibration.md").read_text()
    assert "Issued: 2026-08-18 (backfilled from parked.md `parked:`)" in written
    assert lifecycle.prompt_issued_date(written) == "2026-08-18"
    assert [r["source"] for r in results] == ["parked.md `parked:`"]


def test_backfill_never_guesses_and_says_so(tmp_path):
    root = _mind(tmp_path, active={"sprocket_calibration.md": _prompt()})
    results = lifecycle.backfill_dates(root, apply=True)
    assert [(r["date"], r["source"]) for r in results] == [(None, "unknown")]
    assert "Issued:" not in (root / "active" / "sprocket_calibration.md").read_text()


def test_backfill_is_read_only_without_apply(tmp_path):
    body = _prompt()
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md": body},
                 registries={"parked.md": "## sprocket-calibration\n"
                                          "- parked: 2026-08-18\n"
                                          "- prompt: active/sprocket_calibration.md\n"})
    assert lifecycle.backfill_dates(root)[0]["date"] == "2026-08-18"
    assert (root / "active" / "sprocket_calibration.md").read_text() == body


def test_the_date_lands_after_the_header_never_inside_a_wrapped_value(tmp_path):
    """A header value may run onto a bare continuation line. Inserting between
    the two halves would silently rewrite what the value says."""
    prompt = ("# Sprocket calibration\n\nType: feature\n"
              "Status: issued as flywheel#1 — awaiting review\n"
              "(do not start dev until it lands)\n\nBody prose.\n")
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md": prompt},
                 registries={"active.md": "## sprocket-calibration\n"
                                          "- issued: 2026-08-19\n"
                                          "- prompt: active/sprocket_calibration.md\n"})
    lifecycle.backfill_dates(root, apply=True)
    written = (root / "active" / "sprocket_calibration.md").read_text()
    assert "(do not start dev until it lands)\nIssued: 2026-08-19" in written


def test_a_repos_bullet_list_survives_the_insert(tmp_path):
    prompt = ("# Sprocket calibration\n\nType: feature\nRepos:\n- Flywheel\n"
              "- Sprocket\nStatus: formalised\n\nBody prose.\n")
    root = _mind(tmp_path,
                 active={"sprocket_calibration.md": prompt},
                 registries={"active.md": "## sprocket-calibration\n"
                                          "- issued: 2026-08-19\n"
                                          "- prompt: active/sprocket_calibration.md\n"})
    lifecycle.backfill_dates(root, apply=True)
    written = (root / "active" / "sprocket_calibration.md").read_text()
    assert "Repos:\n- Flywheel\n- Sprocket\nStatus: formalised\nIssued:" in written


def test_backfill_dates_a_registry_entry_after_its_issue_field(tmp_path):
    root = _mind(tmp_path, registries={
        "active.md": "## sprocket-calibration\n"
                     "- issue: https://example.invalid/issues/1 (opened 2026-08-19)\n"
                     "- status: library-dev\n"})
    lifecycle.backfill_dates(root, apply=True)
    written = (root / "active.md").read_text().splitlines()
    assert written[1].startswith("- issue:")
    assert written[2] == "- issued: 2026-08-19 (backfilled from prose)"


def test_every_registry_gets_the_key_that_names_its_own_state(tmp_path):
    """`issued:` for in flight, `filed:` for planned, `parked:` for parked —
    one vocabulary, so a merged feed can say what each date means."""
    root = _mind(tmp_path, registries={
        "active.md": "## alpha\n- note: started 2026-08-19\n",
        "planned.md": "## beta\n- note: scoped 2026-08-10\n",
        "parked.md": "## gamma\n- note: stopped 2026-08-01\n"})
    lifecycle.backfill_dates(root, apply=True)
    assert "- issued: 2026-08-19" in (root / "active.md").read_text()
    assert "- filed: 2026-08-10" in (root / "planned.md").read_text()
    assert "- parked: 2026-08-01" in (root / "parked.md").read_text()


def test_several_undated_entries_in_one_registry_all_land_correctly(tmp_path):
    """Inserting into one entry shifts every later entry's line numbers — the
    off-by-one that would put a date under the wrong task."""
    root = _mind(tmp_path, registries={
        "planned.md": "## alpha\n- note: scoped 2026-08-01\n\n"
                      "## beta\n- note: scoped 2026-08-02\n\n"
                      "## gamma\n- note: scoped 2026-08-03\n"})
    lifecycle.backfill_dates(root, apply=True)
    entries = dict(lifecycle.registry_entries(root / "planned.md"))
    assert lifecycle.entry_date(entries["alpha"])[0] == "2026-08-01"
    assert lifecycle.entry_date(entries["beta"])[0] == "2026-08-02"
    assert lifecycle.entry_date(entries["gamma"])[0] == "2026-08-03"


# --------------------------------------------------------------------------- #
# git as evidence — and knowing when it is not
# --------------------------------------------------------------------------- #
def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True)


def _repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "config", "user.name", "Fixture")
    return root


def test_backfill_prefers_the_commit_that_introduced_the_entry(tmp_path):
    root = _repo(tmp_path / "mind")
    (root / "active.md").write_text("## sprocket-calibration\n- status: library-dev\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "register sprocket calibration",
         "--date=2026-08-19T12:00:00")
    results = lifecycle.backfill_dates(root, apply=True)
    assert [(r["date"], r["source"]) for r in results] == [("2026-08-19", "git")]
    assert "- issued: 2026-08-19 (backfilled from git)" in (root / "active.md").read_text()


def test_a_shallow_clone_is_not_evidence_of_when_anything_started(tmp_path):
    """A shallow checkout reports its boundary commit as the day everything
    older appeared, so every backfill in one clone would come out the same
    wrong date. The boundary is discarded and the Mind's own record used."""
    origin = _repo(tmp_path / "origin")
    (origin / "active.md").write_text("## sprocket-calibration\n- status: library-dev\n")
    _git(origin, "add", "-A")
    _git(origin, "commit", "-q", "-m", "register", "--date=2026-06-01T12:00:00")
    (origin / "active.md").write_text(
        "## sprocket-calibration\n- status: library-dev\n"
        "- prompt: active/sprocket_calibration.md\n")
    (origin / "active").mkdir()
    (origin / "active" / "sprocket_calibration.md").write_text(_prompt())
    _git(origin, "add", "-A")
    _git(origin, "commit", "-q", "-m", "attach prompt", "--date=2026-08-21T12:00:00")

    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "--depth", "1",
                    f"file://{origin}", str(clone)], check=True,
                   capture_output=True)
    assert lifecycle._shallow_boundary(clone) == "2026-08-21"
    # The prompt's only visible "add" is the boundary commit — refused, so the
    # gap is reported honestly instead of being dated 2026-08-21.
    assert lifecycle.git_prompt_issued_date(
        clone, "active/sprocket_calibration.md", "2026-08-21") is None
