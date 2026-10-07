"""Contract tests for the pending-release chain in `lifecycle.py`.

Two leaks shaped these: releases published without the ledger sweep, and links
naming repos that never publish, which no release could ever clear. So the
check must FAIL a malformed / unpublishable `pending-release:` line, and the
`clear-released` planner must clear exactly what a release tag contains.

Fictional fixtures only (`tests/**` is KEEP-copied into the public template,
see `test_spawn_privacy.py`): the published set is monkeypatched to fictional
repos, and every GitHub answer is an injected fake.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402

PUB = ("Gadgets", "Widgets")
G12 = "https://github.com/ExampleOrg/Gadgets/pull/12"
G13 = "https://github.com/ExampleOrg/Gadgets/pull/13"
W34 = "https://github.com/ExampleOrg/Widgets/pull/34"
S56 = "https://github.com/ExampleOrg/Sprockets/pull/56"


def _write(root: Path, rel: str, body: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return p


def _record(root, rel, *lines, prompt_tail=""):
    body = "## flywheel-rebuild\n- completed: 2026-01-01\n" + "".join(
        l + "\n" for l in lines) + "\n### What shipped\n- things\n" + prompt_tail
    return _write(root, f"complete/{rel}", body)


# --------------------------------------------------------------------------- #
# the format check
# --------------------------------------------------------------------------- #
def test_well_formed_published_links_are_quiet(tmp_path):
    _write(tmp_path, "active.md", "# Active\n\n## spindle\n"
           f"- pending-release: Gadgets@{G12}\n")
    _record(tmp_path, "2026/01/a.md", f"- pending-release: Widgets@{W34}")
    assert lifecycle.pending_release_format_findings(tmp_path, PUB) == []


def test_an_unpublished_repo_is_drift(tmp_path):
    _record(tmp_path, "2026/01/a.md", f"- pending-release: Sprockets@{S56}")
    found = lifecycle.pending_release_format_findings(tmp_path, PUB)
    assert len(found) == 1
    assert "not in the published set" in found[0].msg
    assert found[0].paths == ("complete/2026/01/a.md",)


def test_placeholders_and_short_forms_are_drift(tmp_path):
    _write(tmp_path, "active.md", "# Active\n\n## spindle\n"
           "- pending-release: none — workspace-only task\n"
           "- pending-release: Gadgets#12, Widgets#34 (merged, unreleased)\n"
           f"- pending-release: Gadgets@{W34}\n")
    found = lifecycle.pending_release_format_findings(tmp_path, PUB)
    assert len(found) == 3
    # Attributed to the row, not the whole registry file.
    assert all(f.entries == (("active.md", "spindle"),) for f in found)
    assert "names Gadgets but links a Widgets PR" in found[2].msg


def test_the_original_prompt_and_the_archive_are_not_read(tmp_path):
    _record(tmp_path, "2026/01/a.md", "- summary: ok",
            prompt_tail="\n## Original prompt\n\n- pending-release: none\n")
    _write(tmp_path, "complete/archive/epics/x.md",
           f"## x\n- pending-release: Sprockets@{S56}\n")
    assert lifecycle.pending_release_format_findings(tmp_path, PUB) == []


def test_the_format_rule_is_wired_into_check(tmp_path, monkeypatch, capsys):
    _record(tmp_path, "2026/01/a.md", "- pending-release: none")
    for name, val in (("ROOT", tmp_path), ("ACTIVE_MD", tmp_path / "active.md"),
                      ("ACTIVE_DIR", tmp_path / "active"),
                      ("COMPLETE_DIR", tmp_path / "complete"),
                      ("ARCHIVE_DIR", tmp_path / "complete" / "archive")):
        monkeypatch.setattr(lifecycle, name, val)
    monkeypatch.setattr(lifecycle, "PUBLISHED_REPOS", PUB)
    assert lifecycle.cmd_check(None) == 1
    assert "pending-release: none" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# clear-released
# --------------------------------------------------------------------------- #
def _fakes(released, labelled=()):
    calls = []

    def contained(owner, repo, num, tag):
        calls.append((repo, num, tag))
        return (repo, num) in released

    def gh_labelled(owner, repo):
        return [n for r, n in labelled if r == repo]
    return contained, gh_labelled, calls


def test_the_plan_clears_only_what_the_tag_contains(tmp_path):
    _write(tmp_path, "active.md", "# Active\n\n## spindle\n"
           f"- pending-release: Gadgets@{G13}\n")
    _record(tmp_path, "2026/01/a.md",
            f"- pending-release: Gadgets@{G12}",
            f"- pending-release: Widgets@{W34}",
            "- release-gate: Gadgets",
            "- release-gate: Widgets")
    contained, labelled, calls = _fakes({("Gadgets", 12)},
                                        labelled=[("Widgets", 99)])
    plan = lifecycle.plan_clear_released(
        tmp_path, "1.2.3", contained=contained, labelled=labelled,
        published=PUB, owner="ExampleOrg")
    assert [l.value for l in plan.released] == [f"Gadgets@{G12}"]
    # The Gadgets gate is spent; the Widgets one still guards W34.
    assert [g[2] for g in plan.gates] == ["Gadgets"]
    # Label candidates: the released link only (Widgets#99 is not in the tag).
    assert plan.labels == [("ExampleOrg", "Gadgets", 12)]
    assert all(tag == "1.2.3" for _, _, tag in calls)


def test_a_labelled_pr_with_no_mind_line_is_still_unlabelled(tmp_path):
    _write(tmp_path, "active.md", "# Active\n")
    contained, labelled, _ = _fakes({("Widgets", 99)},
                                    labelled=[("Widgets", 99)])
    plan = lifecycle.plan_clear_released(
        tmp_path, "1.2.3", contained=contained, labelled=labelled,
        published=PUB, owner="ExampleOrg")
    assert plan.released == [] and plan.labels == [("ExampleOrg", "Widgets", 99)]


def test_unknown_answers_and_unpublished_lines_are_left_in_place(tmp_path):
    _record(tmp_path, "2026/01/a.md",
            f"- pending-release: Gadgets@{G12}",
            f"- pending-release: Sprockets@{S56}")
    plan = lifecycle.plan_clear_released(
        tmp_path, "1.2.3", contained=lambda *a: None, labelled=lambda *a: [],
        published=PUB, owner="ExampleOrg")
    assert plan.released == [] and plan.unknown == [G12]


def test_apply_deletes_exactly_the_planned_lines(tmp_path):
    rec = _record(tmp_path, "2026/01/a.md",
                  f"- pending-release: Gadgets@{G12}",
                  f"- pending-release: Widgets@{W34}",
                  "- release-gate: Gadgets")
    contained, labelled, _ = _fakes({("Gadgets", 12)})
    plan = lifecycle.plan_clear_released(
        tmp_path, "1.2.3", contained=contained, labelled=labelled,
        published=PUB, owner="ExampleOrg")
    assert lifecycle.apply_release_plan(tmp_path, plan) == [
        "complete/2026/01/a.md"]
    text = rec.read_text()
    assert G12 not in text and "release-gate" not in text
    assert f"- pending-release: Widgets@{W34}" in text
    assert "### What shipped" in text


def test_release_version_strips_the_v_prefix():
    assert lifecycle.resolve_release_version("v1.2.3") == "1.2.3"
    assert lifecycle.resolve_release_version("1.2.3") == "1.2.3"
