"""Contract tests for `scripts/questions_edit.py`, the questions inbox (M3.5).

Parked shift questions land in `questions.md` (the watcher's `question-add`
op calls `add_text` from the tree it writes) and the human clears them in bulk
from a `/questions` chat (PyAutoBrain#645). The witness: add, answer, defer,
drop and reopen round-trip; an add replayed on a moved main takes the next free
id; an answer is appended to the task's prompt wherever it is now (`draft/` or
`active/`); a refused write changes nothing and leaves `lifecycle.py check`
clean; `lifecycle.py close` answers a closed task's open questions. Fictional
fixtures only (`tests/**` ships in the public template).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

MIND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MIND / "scripts"))

import lifecycle  # noqa: E402
import questions_edit as qe  # noqa: E402

ISSUE = "https://github.com/example-owner/flywheel/issues/70"
ISSUE2 = "https://github.com/example-owner/flywheel/issues/71"
PROMPTS = {
    "draft/feature/flywheel/sprocket_calibration.md": "# Sprocket calibration\n\nBody.\n",
    "draft/feature/flywheel/gearbox_rattle.md": "# Gearbox rattle\n",
    "active/axle_balance.md": "# Axle balance\n\nIssued.\n",
}


def _entry(task="draft/feature/flywheel/sprocket_calibration.md", issue=ISSUE,
           shift="2026-11-14-pm2", **kw):
    e = {"task": task, "issue": issue, "kind": "question",
         "ask": "Should the sprocket default to brass or steel?",
         "options": ["brass, as the manual", "steel, as the pipeline"],
         "shift": shift, "asked": "2026-11-14T18:12Z", "worker": "a1b2c3d4"}
    e.update(kw)
    return e


@pytest.fixture
def mind(tmp_path):
    root = tmp_path / "mind"
    (root / "scripts").mkdir(parents=True)
    for name in ("lifecycle.py", "questions_edit.py"):
        shutil.copy(MIND / "scripts" / name, root / "scripts" / name)
    for rel, body in PROMPTS.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    (root / "active.md").write_text(
        "# Active\n\n## axle-balance\n- status: issued\n- prompt: active/axle_balance.md\n")
    (root / "questions.md").write_text(qe.TEMPLATE)
    return root


def _run(root, *args):
    env = dict(os.environ, LIFECYCLE_NO_GH="1")
    return subprocess.run([sys.executable, str(root / "scripts" / "questions_edit.py"), *args],
                          cwd=root, env=env, capture_output=True, text=True)


def _check(root):
    """`python3 scripts/lifecycle.py check` on the fixture Mind, as the skill runs it."""
    env = dict(os.environ, LIFECYCLE_NO_GH="1")
    res = subprocess.run([sys.executable, str(root / "scripts" / "lifecycle.py"), "check"],
                         cwd=root, env=env, capture_output=True, text=True)
    assert "questions.md" not in res.stdout, res.stdout
    return res


def _states(root):
    return {e["id"]: e["state"] for e in qe.parse((root / "questions.md").read_text())}


def _cli_add(root, **kw):
    e = _entry(**kw)
    args = ["add"]
    for k in ("task", "issue", "kind", "ask", "shift", "asked", "worker"):
        args += [f"--{k}", e[k]]
    for o in e["options"]:
        args += ["--option", o]
    return _run(root, *args)


def test_the_template_is_clean_and_empty(mind):
    assert qe.parse(qe.TEMPLATE) == []
    assert lifecycle.questions_findings(mind) == []
    assert qe.show(mind)[0] == "(no questions)"
    _check(mind)


def test_add_round_trip(mind):
    res = _cli_add(mind)
    assert res.returncode == 0, res.stderr
    assert "questions.md: added Q1" in res.stdout
    text = (mind / "questions.md").read_text()
    assert ("## Open\n\n### Q1. sprocket_calibration — Should the sprocket default to brass "
            "or steel?\n- task: draft/feature/flywheel/sprocket_calibration.md\n"
            f"- issue: {ISSUE}\n- kind: question\n"
            "- ask: Should the sprocket default to brass or steel?\n"
            "- options: (a) brass, as the manual · (b) steel, as the pipeline\n"
            "- shift: 2026-11-14-pm2\n- asked: 2026-11-14T18:12Z\n- worker: a1b2c3d4\n\n"
            "## Deferred") in text
    [e] = qe.parse(text)
    assert (e["id"], e["state"], e["fields"]["kind"]) == ("Q1", "open", "question")
    # The same (shift, task, issue) again is a silent repeat.
    res = _cli_add(mind)
    assert res.returncode == 0 and "Q1 already holds this question" in res.stdout
    assert (mind / "questions.md").read_text() == text
    _check(mind)


def test_add_text_is_pure_and_its_id_follows_the_tree_it_is_replayed_on(mind):
    """The watcher's op replays on a moved main: the id is worked out inside
    the text being written, so a concurrent Q1 makes this one Q2."""
    base = qe.TEMPLATE
    mine, qid, added = qe.add_text(base, _entry())
    assert (qid, added) == ("Q1", True)
    moved_main, other, _ = qe.add_text(base, _entry(task="draft/feature/flywheel/gearbox_rattle.md",
                                                    issue=ISSUE2))
    assert other == "Q1"
    replay, qid, added = qe.add_text(moved_main, _entry())
    assert (qid, added) == ("Q2", True)
    assert [e["id"] for e in qe.parse(replay)] == ["Q1", "Q2"]
    # A second replay of the same op is a repeat, not a Q3.
    again, qid, added = qe.add_text(replay, _entry())
    assert (again, qid, added) == (replay, "Q2", False)


def test_add_with_root_resolves_a_claimed_draft_to_active(mind):
    text, qid, _ = qe.add_text(qe.TEMPLATE, _entry(task="draft/feature/flywheel/axle_balance.md"),
                               mind)
    assert qe.parse(text)[0]["fields"]["task"] == "active/axle_balance.md"
    with pytest.raises(qe.Refused, match="resolves to no draft/ or active/ prompt"):
        qe.add_text(qe.TEMPLATE, _entry(task="draft/feature/flywheel/gone.md"), mind)
    with pytest.raises(qe.Refused, match="kind must be one of"):
        qe.add_text(qe.TEMPLATE, _entry(kind="musing"))
    with pytest.raises(qe.Refused, match="ask is missing"):
        qe.add_text(qe.TEMPLATE, _entry(ask="  "))


def test_answer_moves_the_entry_and_appends_to_a_draft_prompt(mind):
    _cli_add(mind)
    res = _run(mind, "answer", "Q1", "--text", "(a), and note steel in the docstring",
               "--comment", f"{ISSUE}#issuecomment-9", "--by", "example-human",
               "--date", "2026-11-16", "--at", "2026-11-16T09:00Z")
    assert res.returncode == 0, res.stderr
    assert "prompt: draft/feature/flywheel/sprocket_calibration.md" in res.stdout
    assert _states(mind) == {"Q1": "answered"}
    [e] = qe.parse((mind / "questions.md").read_text())
    assert e["fields"]["answered"] == "2026-11-16T09:00Z by example-human (chat)"
    assert e["fields"]["answer"] == "(a), and note steel in the docstring"
    assert e["fields"]["answer-comment"] == f"{ISSUE}#issuecomment-9"
    prompt = (mind / "draft/feature/flywheel/sprocket_calibration.md").read_text()
    assert prompt == ("# Sprocket calibration\n\nBody.\n\n## Answers from the human\n"
                      "- Q1 (2026-11-16, shift 2026-11-14-pm2 question on flywheel#70): (a), "
                      f"and note steel in the docstring {ISSUE}#issuecomment-9\n")
    _check(mind)


def test_answer_follows_a_claimed_prompt_into_active(mind):
    """The entry still names the draft/ path; the prompt has been issued since."""
    qe.add(mind, _entry(task="draft/feature/flywheel/axle_balance.md"))
    qe.add(mind, _entry(task="draft/feature/flywheel/axle_balance.md", issue=ISSUE2,
                        ask="And the bearing?"))
    msg, prompt = qe.answer(mind, "Q1", "steel", day="2026-11-16")
    assert prompt == "active/axle_balance.md"
    qe.answer(mind, "q2", "sealed", day="2026-11-16")
    text = (mind / "active/axle_balance.md").read_text()
    # One section, both answers, in order.
    assert text.count("## Answers from the human") == 1
    assert text.endswith("## Answers from the human\n"
                         "- Q1 (2026-11-16, shift 2026-11-14-pm2 question on flywheel#70): steel\n"
                         "- Q2 (2026-11-16, shift 2026-11-14-pm2 question on flywheel#71): "
                         "sealed\n")
    _check(mind)


def test_answer_with_the_prompt_gone_records_it_on_the_entry_only(mind):
    qe.add(mind, _entry(task="draft/feature/flywheel/gearbox_rattle.md"))
    (mind / "draft/feature/flywheel/gearbox_rattle.md").unlink()   # completed since
    # The Open entry now dangles: check reports it, and an answer clears it.
    assert any("Q1 (open) task" in f.msg for f in lifecycle.questions_findings(mind))
    msg, prompt = qe.answer(mind, "Q1", "rattle fixed upstream")
    assert prompt is None and "no task is resumed" in msg
    assert _states(mind) == {"Q1": "answered"}
    assert lifecycle.questions_findings(mind) == []


def test_defer_show_open_and_reopen(mind):
    qe.add(mind, _entry())
    qe.add(mind, _entry(task="draft/feature/flywheel/gearbox_rattle.md", issue=ISSUE2,
                        asked="2026-11-14T19:00Z"))
    res = _run(mind, "defer", "Q1", "--until", "2026-11-20", "--date", "2026-11-16")
    assert res.returncode == 0 and "deferred Q1 until 2026-11-20" in res.stdout
    assert _states(mind) == {"Q1": "deferred", "Q2": "open"}
    # A sitting's list skips a deferral that is not due yet, then shows it.
    assert [ln.split()[0] for ln in qe.show(mind, "open", today="2026-11-16")[:-1]] == ["Q2"]
    assert [ln.split()[0] for ln in qe.show(mind, "open", today="2026-11-20")[:-1]] == ["Q1", "Q2"]
    assert qe.show(mind)[-1] == "1 open, 1 deferred, 0 answered, 0 dropped"
    # Deferred with no date: due at the next sitting.
    qe.defer(mind, "Q2")
    assert "until" not in qe.parse((mind / "questions.md").read_text())[1]["fields"]
    assert [ln.split()[0] for ln in qe.show(mind, "open", today="2026-11-16")[:-1]] == ["Q2"]
    assert qe.reopen(mind, "Q1", day="2026-11-17") == "reopened Q1 (was deferred)"
    e = next(x for x in qe.parse((mind / "questions.md").read_text()) if x["id"] == "Q1")
    assert e["state"] == "open" and "until" not in e["fields"] and "deferred" not in e["fields"]
    assert e["fields"]["reopened"] == "2026-11-17"
    _check(mind)


def test_drop_then_reopen(mind):
    qe.add(mind, _entry())
    res = _run(mind, "drop", "Q1", "--why", "not worth it", "--by", "example-human",
               "--date", "2026-11-16")
    assert res.returncode == 0 and "shelved" in res.stdout
    [e] = qe.parse((mind / "questions.md").read_text())
    assert e["state"] == "dropped"
    assert e["fields"]["dropped"] == "2026-11-16 by example-human — not worth it (task shelved)"
    # The prompt is untouched: dropping a question is not answering it.
    assert "Answers" not in (mind / "draft/feature/flywheel/sprocket_calibration.md").read_text()
    qe.reopen(mind, "Q1")
    [e] = qe.parse((mind / "questions.md").read_text())
    assert e["state"] == "open" and "dropped" not in e["fields"]
    _check(mind)


def test_answered_entries_reopen_and_lose_their_answer_keys(mind):
    qe.add(mind, _entry())
    qe.answer(mind, "Q1", "brass")
    qe.reopen(mind, "Q1")
    [e] = qe.parse((mind / "questions.md").read_text())
    assert e["state"] == "open"
    assert not {"answered", "answer", "answer-comment"} & set(e["fields"])


@pytest.mark.parametrize("args,why", [
    (("answer", "Q9", "--text", "x"), "Q9 is not in questions.md"),
    (("answer", "Q1", "--text", "   "), "no answer text given"),
    (("answer", "Q1", "--text", "x", "--comment", "not-a-url"), "--comment must be"),
    (("answer", "Q1", "--text", "x", "--via", "carrier-pigeon"), "--via is chat or issue"),
    (("answer", "seventeen", "--text", "x"), "is not a question id"),
    (("defer", "Q1", "--until", "next week"), "--until is a date"),
    (("drop", "Q1", "--why", " "), "drop needs --why"),
])
def test_refused_writes_change_nothing_and_check_stays_clean(mind, args, why):
    qe.add(mind, _entry())
    before = (mind / "questions.md").read_text()
    prompt = (mind / "draft/feature/flywheel/sprocket_calibration.md").read_text()
    res = _run(mind, *args)
    assert res.returncode == 1 and why in res.stderr, res.stderr
    assert (mind / "questions.md").read_text() == before
    assert (mind / "draft/feature/flywheel/sprocket_calibration.md").read_text() == prompt
    _check(mind)


def test_a_settled_entry_is_refused_until_reopened(mind):
    qe.add(mind, _entry())
    qe.answer(mind, "Q1", "brass")
    before = (mind / "questions.md").read_text()
    for verb in (lambda: qe.answer(mind, "Q1", "steel"), lambda: qe.defer(mind, "Q1"),
                 lambda: qe.drop(mind, "Q1", "x")):
        with pytest.raises(qe.Refused, match="Q1 is answered — reopen it first"):
            verb()
    assert (mind / "questions.md").read_text() == before


def test_a_write_that_adds_lifecycle_drift_is_undone_with_its_prompt(mind, monkeypatch):
    qe.add(mind, _entry())
    before = (mind / "questions.md").read_text()
    prompt_path = mind / "draft/feature/flywheel/sprocket_calibration.md"
    prompt = prompt_path.read_text()
    real, calls = lifecycle.questions_findings, {"n": 0}

    def flaky(root):
        calls["n"] += 1
        found = real(root)
        if calls["n"] == 2:
            found = found + [lifecycle.Finding("questions.md: injected", ("questions.md",))]
        return found

    monkeypatch.setattr(lifecycle, "questions_findings", flaky)
    with pytest.raises(qe.Refused, match="would add lifecycle drift"):
        qe.answer(mind, "Q1", "brass")
    assert (mind / "questions.md").read_text() == before
    assert prompt_path.read_text() == prompt


def test_add_creates_the_file_from_the_template_when_absent(mind):
    (mind / "questions.md").unlink()
    assert qe.add(mind, _entry()) == "added Q1"
    text = (mind / "questions.md").read_text()
    assert text.startswith("# Questions\n") and "## Dropped" in text
    _check(mind)


# --- lifecycle.py check ----------------------------------------------------------

def _findings(mind, text):
    (mind / "questions.md").write_text(text)
    return [f.msg for f in lifecycle.questions_findings(mind)]


def test_check_reports_malformed_and_dangling_entries(mind):
    good, _q, _a = qe.add_text(qe.TEMPLATE, _entry())
    assert _findings(mind, good) == []
    dup = good.replace("## Deferred", good[good.index("### Q1"):good.index("## Deferred")]
                       .replace(ISSUE, ISSUE2) + "## Deferred")
    assert any("Q1 is used twice" in m for m in _findings(mind, dup))
    assert any("Q1 has no worker:" in m
               for m in _findings(mind, good.replace("- worker: a1b2c3d4\n", "")))
    assert any("has kind `musing`" in m
               for m in _findings(mind, good.replace("kind: question", "kind: musing")))
    assert any("is not `### Q<n>. <task> — <ask>`" in m
               for m in _findings(mind, good.replace("### Q1.", "### Question 1:")))
    gone = good.replace("sprocket_calibration.md", "no_such_prompt.md")
    assert any("Q1 (open) task `draft/feature/flywheel/no_such_prompt.md` resolves to no"
               in m for m in _findings(mind, gone))
    # Answered and dropped entries may name a prompt that is gone; they need
    # their own keys.
    answered = lifecycle.question_move_text(gone, "Q1", "answered", {"answered": "t by h (chat)",
                                                                     "answer": "x"})
    assert _findings(mind, answered) == []
    assert any("Q1 has no answer:" in m for m in _findings(
        mind, answered.replace("- answer: x\n", "")))


def test_lifecycle_check_runs_the_questions_leg(mind):
    (mind / "questions.md").write_text(qe.TEMPLATE.replace("## Open", "## Open\n\n### Q1. x"))
    env = dict(os.environ, LIFECYCLE_NO_GH="1")
    res = subprocess.run([sys.executable, "scripts/lifecycle.py", "check"], cwd=mind, env=env,
                         capture_output=True, text=True)
    assert res.returncode == 1 and "questions.md: Q1 has no task:" in res.stdout


# --- lifecycle.py close ----------------------------------------------------------

def test_questions_close_text_answers_the_closed_tasks_entries():
    text, _q, _a = qe.add_text(qe.TEMPLATE, _entry())
    text, _q, _a = qe.add_text(text, _entry(issue=ISSUE2, ask="Bearings?"))
    text, _q, _a = qe.add_text(text, _entry(task="draft/feature/flywheel/gearbox_rattle.md"))
    text = lifecycle.question_move_text(text, "Q2", "deferred", {"until": "2026-12-01"})
    out, ids = lifecycle.questions_close_text(text, "sprocket_calibration.md", "2026-11-16")
    assert ids == ["Q1", "Q2"]
    states = {e["id"]: (e["state"], e["fields"].get("answer"), e["fields"].get("until"))
              for e in qe.parse(out)}
    assert states == {"Q1": ("answered", "(task completed)", None),
                      "Q2": ("answered", "(task completed)", None),
                      "Q3": ("open", None, None)}
    assert lifecycle.questions_close_text(out, "sprocket_calibration.md", "x") == (out, [])


def test_close_moves_the_tasks_open_questions_to_answered(tmp_path, monkeypatch):
    root = tmp_path
    (root / "active").mkdir()
    (root / "complete").mkdir()
    (root / "active" / "sprocket_calibration.md").write_text("# Sprocket calibration\n")
    (root / "active.md").write_text("# Active\n\n## sprocket-calibration\n- status: x\n"
                                    "- prompt: active/sprocket_calibration.md\n")
    (root / "body.md").write_text("## sprocket-calibration\n- completed: 2026-09-17\n")
    text, _q, _a = qe.add_text(qe.TEMPLATE, _entry())
    (root / "questions.md").write_text(text)
    for name, value in (("ROOT", root), ("ACTIVE_DIR", root / "active"),
                        ("ACTIVE_MD", root / "active.md"), ("DRAFT_DIR", root / "draft"),
                        ("COMPLETE_DIR", root / "complete"),
                        ("ARCHIVE_DIR", root / "complete" / "archive"),
                        ("INDEX_MD", root / "complete" / "index.md"),
                        ("AUTONOMY_LOG", root / "autonomy_log.md")):
        monkeypatch.setattr(lifecycle, name, value)
    args = SimpleNamespace(slug="sprocket-calibration", date="2026-09-17",
                           from_file=str(root / "body.md"), prompt=None, pr=[], tier=None,
                           gate=None, action=None, stage="1", no_shadow_row=False, log=None,
                           apply=False)
    assert lifecycle.cmd_close(args) == 0
    assert (root / "questions.md").read_text() == text      # the dry run writes nothing
    args.apply = True
    assert lifecycle.cmd_close(args) == 0
    [e] = qe.parse((root / "questions.md").read_text())
    assert e["state"] == "answered" and e["fields"]["answer"] == "(task completed)"
    assert lifecycle.questions_findings(root) == []
