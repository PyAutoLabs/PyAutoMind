"""Contract tests for `scripts/queue_edit.py`, the `/queue` chat's only writer.

`queue.md` is maintained by the human in chat (PyAutoBrain#640): the skill
pastes what the human gave it into this script, never hand-edits the markdown.
The witness: `add` (from a pasted dashboard copy line, a path, a title or a
whole prompt), `remove` and `move` each write the expected order, keep the
headings numbered as the planner ranks them, and leave `lifecycle.py check`
clean on a fixture Mind; a ref that resolves to no draft/ or active/ prompt is
refused with nothing written. Fictional fixtures only (`tests/**` ships in the
public template).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

MIND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MIND / "scripts"))

import lifecycle  # noqa: E402
import queue_edit as qe  # noqa: E402

QUEUE = """# Queue

Prose header.

```markdown
## <n>. <label>
- kind: prompt
- ref: draft/<work-type>/<target>/<name>.md
```

<!-- the ranked list starts here -->

## 1. Sprockets
- kind: prompt
- ref: draft/feature/flywheel/sprocket_calibration.md
- note: the first wish

## 4. Gearbox
- kind: prompt
- ref: draft/bug/flywheel/gearbox_rattle.md

## 9. Axle
- kind: prompt
- ref: draft/feature/flywheel/axle_balance.md
- note: issued since; keeps its place

## Retired

Entries that have left the queue.

### Old widget work
- shipped-as: Gadgets#1
- note: history
"""

PROMPTS = {
    "draft/feature/flywheel/sprocket_calibration.md": "# Sprocket calibration\n",
    "draft/bug/flywheel/gearbox_rattle.md": "# Gearbox rattle\n",
    "draft/feature/flywheel/widget_polish.md": "# Widget polish for the flywheel\n\nBody.\n",
    "draft/docs/flywheel/widget_guide.md": "# Widget guide\n",
    "active/axle_balance.md": "# Axle balance\n",
    "complete/2026/01/old_thing.md": "# Old thing\n",
}


@pytest.fixture
def mind(tmp_path):
    root = tmp_path / "mind"
    (root / "scripts").mkdir(parents=True)
    for name in ("lifecycle.py", "queue_edit.py"):
        shutil.copy(MIND / "scripts" / name, root / "scripts" / name)
    for rel, body in PROMPTS.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    (root / "queue.md").write_text(QUEUE)
    (root / "active.md").write_text(
        "# Active\n\n## axle-balance\n- status: issued\n- prompt: active/axle_balance.md\n")
    return root


def _run(root, *args, stdin=None):
    env = dict(os.environ, LIFECYCLE_NO_GH="1")
    return subprocess.run([sys.executable, str(root / "scripts" / "queue_edit.py"), *args],
                          cwd=root, env=env, capture_output=True, text=True, input=stdin)


def _check(root):
    """`python3 scripts/lifecycle.py check` on the fixture Mind, as the skill runs it."""
    env = dict(os.environ, LIFECYCLE_NO_GH="1")
    res = subprocess.run([sys.executable, str(root / "scripts" / "lifecycle.py"), "check"],
                         cwd=root, env=env, capture_output=True, text=True)
    assert "queue.md" not in res.stdout, res.stdout
    return res


def _order(root):
    return [(e["label"], e["ref"]) for e in qe.entries((root / "queue.md").read_text())]


def _headings(root):
    return [ln for ln in (root / "queue.md").read_text().split("\n")
            if ln.startswith("## ") and ln[3:4].isdigit()]


def test_the_fixture_is_clean_before_any_edit(mind):
    assert lifecycle.queue_findings(mind) == []
    _check(mind)


def test_show_numbers_the_queue_as_the_planner_ranks_it(mind):
    res = _run(mind, "show")
    assert res.returncode == 0
    assert res.stdout.splitlines() == [
        "1. Sprockets — draft/feature/flywheel/sprocket_calibration.md",
        "2. Gearbox — draft/bug/flywheel/gearbox_rattle.md",
        "3. Axle — draft/feature/flywheel/axle_balance.md"]
    assert (mind / "queue.md").read_text() == QUEUE, "show writes nothing"


def test_add_from_the_dashboards_copy_line(mind):
    res = _run(mind, "add", "Use the start-dev skill. draft/feature/flywheel/widget_polish.md",
               "--note", "after the gearbox")
    assert res.returncode == 0, res.stderr
    assert "added `Widget polish for the flywheel` at #4" in res.stdout
    assert res.stdout.rstrip().endswith(
        "4. Widget polish for the flywheel — draft/feature/flywheel/widget_polish.md")
    text = (mind / "queue.md").read_text()
    assert ("## 4. Widget polish for the flywheel\n- kind: prompt\n"
            "- ref: draft/feature/flywheel/widget_polish.md\n- note: after the gearbox\n\n"
            "## Retired") in text
    # Every write renumbers: a heading's number is its rank.
    assert _headings(mind) == ["## 1. Sprockets", "## 2. Gearbox", "## 3. Axle",
                               "## 4. Widget polish for the flywheel"]
    # The rest of the file is untouched.
    assert text.startswith(QUEUE.split("## 1. Sprockets")[0])
    assert text.endswith(QUEUE.split("## 9. Axle")[1].split("## Retired")[1])
    _check(mind)


@pytest.mark.parametrize("ref", [
    "draft/docs/flywheel/widget_guide.md",
    "`draft/docs/flywheel/widget_guide.md`",
    "https://github.com/example-owner/PyAutoMind/blob/main/draft/docs/flywheel/widget_guide.md",
    "widget_guide.md",
    "widget_guide",
    "Widget guide",
    "# Widget guide\n\nType: docs\nThe whole pasted prompt.\n",
])
def test_add_resolves_every_form_a_human_pastes(mind, ref):
    res = _run(mind, "add", "-", "--at", "top", stdin=ref)
    assert res.returncode == 0, res.stderr
    assert _order(mind)[0] == ("Widget guide", "draft/docs/flywheel/widget_guide.md")
    _check(mind)


def test_add_at_a_rank_and_with_a_label(mind):
    assert qe.add(mind, "draft/feature/flywheel/widget_polish.md", at=2,
                  label="Polish") == "added `Polish` at #2"
    assert [r for _l, r in _order(mind)][1] == "draft/feature/flywheel/widget_polish.md"
    assert _headings(mind)[1] == "## 2. Polish"
    _check(mind)


@pytest.mark.parametrize("ref,why", [
    ("draft/feature/flywheel/no_such_prompt.md", "resolves to no draft/ or active/ prompt"),
    ("complete/2026/01/old_thing.md", "resolves to no draft/ or active/ prompt"),
    ("Old thing", "resolves to no draft/ or active/ prompt"),
    ("Widget", "did you mean: draft/docs/flywheel/widget_guide.md, "
               "draft/feature/flywheel/widget_polish.md"),
    ("Notes first\nthen draft/docs/flywheel/widget_guide.md", "a multi-line paste must open"),
    ("draft/bug/flywheel/gearbox_rattle.md", "already queued at #2"),
    ("active/axle_balance.md", "already queued at #3"),
])
def test_add_refuses_and_writes_nothing(mind, ref, why):
    res = _run(mind, "add", ref)
    assert res.returncode == 1
    assert why in res.stderr, res.stderr
    assert (mind / "queue.md").read_text() == QUEUE


def test_remove_retires_the_entry_with_shelved_as(mind):
    res = _run(mind, "remove", "#2", "--why", "not this month", "--date", "2026-11-16")
    assert res.returncode == 0, res.stderr
    assert _order(mind) == [("Sprockets", "draft/feature/flywheel/sprocket_calibration.md"),
                            ("Axle", "draft/feature/flywheel/axle_balance.md")]
    assert _headings(mind) == ["## 1. Sprockets", "## 2. Axle"]
    text = (mind / "queue.md").read_text()
    footer = text[text.index("## Retired"):]
    assert ("### Gearbox\n- shelved-as: draft/bug/flywheel/gearbox_rattle.md — off the "
            "queue 2026-11-16; not this month\n- note: retired by a `/queue` chat\n") in footer
    assert "### Old widget work" in footer, "earlier history is kept"
    # The prompt itself is untouched: removing from the queue is not shelving work.
    assert (mind / "draft/bug/flywheel/gearbox_rattle.md").is_file()
    _check(mind)


@pytest.mark.parametrize("who", ["1", "Sprockets", "sprocket_calibration.md",
                                 "Use the start-dev skill. draft/feature/flywheel/sprocket_calibration.md",
                                 "Sprocket calibration"])
def test_remove_finds_the_entry_by_rank_ref_label_or_title(mind, who):
    qe.remove(mind, who, day="2026-11-16")
    assert [l for l, _r in _order(mind)] == ["Gearbox", "Axle"]
    assert "- note: the first wish — retired by a `/queue` chat" in (mind / "queue.md").read_text()
    _check(mind)


def test_remove_by_its_active_path_matches_the_draft_entry(mind):
    qe.remove(mind, "active/axle_balance.md", day="2026-11-16")
    assert [l for l, _r in _order(mind)] == ["Sprockets", "Gearbox"]
    _check(mind)


@pytest.mark.parametrize("who,where,order", [
    ("3", "top", ["Axle", "Sprockets", "Gearbox"]),
    ("Gearbox", "up", ["Gearbox", "Sprockets", "Axle"]),
    ("1", "down", ["Gearbox", "Sprockets", "Axle"]),
    ("Sprockets", "bottom", ["Gearbox", "Axle", "Sprockets"]),
    ("#1", "3", ["Gearbox", "Axle", "Sprockets"]),
    ("Axle", "#2", ["Sprockets", "Axle", "Gearbox"]),
])
def test_move(mind, who, where, order):
    res = _run(mind, "move", who, where)
    assert res.returncode == 0, res.stderr
    assert [l for l, _r in _order(mind)] == order
    assert _headings(mind) == [f"## {n}. {l}" for n, l in enumerate(order, 1)]
    assert "- note: the first wish" in (mind / "queue.md").read_text(), "bodies travel"
    _check(mind)


def test_move_at_the_edge_is_no_change(mind):
    assert qe.move(mind, "1", "up") == "no change: `Sprockets` stays at #1"
    assert (mind / "queue.md").read_text() == QUEUE, "a no-op writes nothing"


@pytest.mark.parametrize("args,why", [
    (("move", "7", "top"), "there is no #7"),
    (("move", "1", "sideways"), "is not up, down, top, bottom or a number"),
    (("move", "1", "9"), "out of range"),
    (("remove", "Flux capacitor"), "is not in the queue"),
])
def test_bad_moves_and_removes_are_refused(mind, args, why):
    res = _run(mind, *args)
    assert res.returncode == 1 and why in res.stderr, res.stderr
    assert (mind / "queue.md").read_text() == QUEUE


def test_an_empty_queue_takes_its_first_entry_above_the_footer(mind):
    (mind / "queue.md").write_text(QUEUE.split("## 1. Sprockets")[0] + "## Retired\n\nNone.\n")
    qe.add(mind, "draft/docs/flywheel/widget_guide.md")
    text = (mind / "queue.md").read_text()
    assert ("<!-- the ranked list starts here -->\n\n## 1. Widget guide\n- kind: prompt\n"
            "- ref: draft/docs/flywheel/widget_guide.md\n\n## Retired\n") in text
    _check(mind)


def test_a_non_prompt_numbered_entry_blocks_writes_not_reads(mind):
    (mind / "queue.md").write_text(QUEUE.replace(
        "## Retired", "## 10. A theme sweep\n- kind: retired\n\n## Retired"))
    assert "not ranked" in "\n".join(qe.show(mind))
    res = _run(mind, "move", "1", "down")
    assert res.returncode == 1 and "not a `kind: prompt` entry" in res.stderr


def test_a_write_that_adds_lifecycle_drift_is_undone(mind, monkeypatch):
    """Belt and braces: whatever the edit, a new queue finding restores the file."""
    real = lifecycle.queue_findings
    calls = {"n": 0}

    def flaky(root):
        calls["n"] += 1
        found = real(root)
        if calls["n"] == 2:
            found = found + [lifecycle.Finding("queue.md: injected", ("queue.md",))]
        return found

    monkeypatch.setattr(lifecycle, "queue_findings", flaky)
    with pytest.raises(qe.Refused, match="would add lifecycle drift"):
        qe.move(mind, "1", "down")
    assert (mind / "queue.md").read_text() == QUEUE


def test_planner_order_matches_after_edits(mind):
    """The ranks this script prints are the planner's: `kind: prompt` refs in
    file order, read exactly as `lifecycle.queue_entries` reads them."""
    qe.move(mind, "3", "top")
    qe.add(mind, "draft/docs/flywheel/widget_guide.md", at=2)
    refs = [ref for _l, kind, ref in lifecycle.queue_entries(mind) if kind == "prompt"]
    assert refs == [r for _l, r in _order(mind)] == [
        "draft/feature/flywheel/axle_balance.md", "draft/docs/flywheel/widget_guide.md",
        "draft/feature/flywheel/sprocket_calibration.md", "draft/bug/flywheel/gearbox_rattle.md"]


# --- a pasted prompt is matched by its title line, never by paths in its body --

CITING = """# Widget polish for the flywheel

Type: feature
Blocked-by: draft/bug/flywheel/gearbox_rattle.md

Follows `draft/docs/flywheel/widget_guide.md`; see also
https://github.com/example-owner/PyAutoMind/blob/main/active/axle_balance.md
"""


def test_a_pasted_prompt_that_cites_other_prompts_queues_itself(mind):
    assert qe.resolve_prompt(mind, CITING) == (
        "draft/feature/flywheel/widget_polish.md", "Widget polish for the flywheel")
    res = _run(mind, "add", "-", stdin=CITING)
    assert res.returncode == 0, res.stderr
    assert _order(mind)[-1] == ("Widget polish for the flywheel",
                                "draft/feature/flywheel/widget_polish.md")
    _check(mind)


def test_a_cited_path_in_a_title_less_paste_is_never_taken(mind):
    body = CITING.split("\n", 2)[2]  # the body alone, no `# Title` line
    with pytest.raises(qe.Refused, match="a multi-line paste must open"):
        qe.resolve_prompt(mind, body)


def test_an_ambiguous_title_is_refused_with_candidates(mind):
    twin = mind / "draft" / "docs" / "flywheel" / "widget_guide_v2.md"
    twin.write_text("# Widget guide\n")
    with pytest.raises(qe.Refused, match="matches 2 prompts"):
        qe.resolve_prompt(mind, "# Widget guide\n\nBody.\n")


def _live_citing_prompts():
    """Every live prompt in THIS checkout whose body cites another prompt —
    the real texts that once queued the wrong task. Read at run time, so no
    live string is written here; none in a fresh template (the test skips)."""
    out = []
    for p in qe._prompts(MIND):
        text = p.read_text(encoding="utf-8", errors="replace")
        own = p.relative_to(MIND).as_posix()
        cited = {c for c in qe.PATH_RE.findall(text.split("\n", 1)[-1])
                 if Path(c).name != p.name}
        if text.startswith("# ") and cited:
            out.append((own, text))
    return out


@pytest.mark.skipif(not _live_citing_prompts(), reason="no live prompts (template)")
def test_real_prompts_that_cite_other_prompts_resolve_to_themselves_or_refuse():
    titles: "dict[str, int]" = {}
    for p in qe._prompts(MIND):
        t = qe._norm(qe._title(p))
        titles[t] = titles.get(t, 0) + 1
    checked = 0
    for own, text in _live_citing_prompts():
        title = qe._norm(text.split("\n", 1)[0][2:])
        if titles.get(title, 0) == 1:
            assert qe.resolve_prompt(MIND, text)[0] == own, own
            checked += 1
        else:  # a shared title is refused, never resolved to a cited prompt
            with pytest.raises(qe.Refused, match="matches"):
                qe.resolve_prompt(MIND, text)
    assert checked
