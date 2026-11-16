#!/usr/bin/env python3
"""Edit `questions.md`, the human's inbox of parked questions (M3.5).

A shift worker that parks on a question leaves it on its issue; the shift
watcher adds one entry here through its one Mind writer (the `question-add`
op, which calls `add_text` from the tree it writes, PyAutoBrain#645). The
human clears the inbox in bulk, in a chat that ran `/questions` (PyAutoBrain
`skills/questions`). That skill never hand-edits the markdown: it runs this
script in a temporary Mind worktree detached on `origin/main`, then commits
with `prompt_sync_push` and runs `lifecycle.py check`.

    python3 scripts/questions_edit.py show   [--open | --all] [Q<n>]
    python3 scripts/questions_edit.py add    --task PATH --issue URL --kind question|blocked
                                             --ask TEXT [--option TEXT]... --shift S
                                             --asked T --worker K
    python3 scripts/questions_edit.py answer Q<n> --text TEXT [--comment URL]
                                             [--by LOGIN] [--via chat|issue]
    python3 scripts/questions_edit.py defer  Q<n> [--until YYYY-MM-DD] [--by LOGIN]
    python3 scripts/questions_edit.py drop   Q<n> --why TEXT [--by LOGIN]
    python3 scripts/questions_edit.py reopen Q<n>

The section an entry sits under is its state: Open, Deferred, Answered,
Dropped. Ids are global and increasing (the file's highest plus 1, worked out
in the tree being written), and `(shift, task, issue)` is unique: an add
whose triple exists is a silent repeat. `answer` also appends the answer to
the task's prompt under `## Answers from the human` (wherever the prompt is
now, `draft/` or `active/`) — the next worker reads it there — and prints
`prompt: <path>` so the caller commits that path too. A write that would add a
`lifecycle.py check` questions finding is undone and refused.

Exit 0: done (or no change). 1: refused, nothing written. 2: usage.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lifecycle  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FILE = "questions.md"
ID_RE = re.compile(r"^#?Q?(\d+)\.?$", re.I)
ISSUE_RE = re.compile(r"^https://github\.com/[^/\s]+/([^/\s]+)/(?:issues|pull)/(\d+)")
ANSWERS_HEADING = "## Answers from the human"
ASK_MAX, OPTION_MAX, OPTIONS_MAX, SHORT_MAX = 200, 120, 4, 70

TEMPLATE = """# Questions

Parked questions from shift workers, waiting for the human (M3.5,
PyAutoBrain#645). The shift watcher adds entries through its one Mind writer;
a `/questions` chat (PyAutoBrain `skills/questions`) answers, defers or drops
them with `scripts/questions_edit.py`. Never edit by hand: the section an
entry sits under is its state, and `lifecycle.py check` validates the file.
An answer releases the parked task: the next shift resumes it with the answer
in its prompt.

```markdown
### Q<n>. <task> — <short ask>
- task: draft/<work-type>/<target>/<name>.md
- issue: https://github.com/<owner>/<repo>/issues/<n>
- kind: question
- ask: <one line>
- options: (a) <first> · (b) <second>
- shift: <slot>
- asked: <YYYY-MM-DDTHH:MMZ>
- worker: <session key>
```

## Open

## Deferred      <!-- entries add: - until: YYYY-MM-DD (absent: until the next sitting) -->

## Answered      <!-- entries add: - answered: <time> by <login> (chat|issue), - answer:, - answer-comment: <url> -->

## Dropped       <!-- entries add: - dropped: <date> by <login> — <why> (task shelved) -->
"""


class Refused(Exception):
    """The edit is not made; the message says why."""


# --------------------------------------------------------------------------- #
# reading
# --------------------------------------------------------------------------- #
def parse(text: str) -> "list[dict]":
    """The entries, in file order (`lifecycle.questions_parse`)."""
    return lifecycle.questions_parse(text)[0]


def _read(root: Path) -> str:
    try:
        return (root / FILE).read_text(encoding="utf-8")
    except OSError:
        return ""


def _one_line(text) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _clip(text: str, limit: int) -> str:
    text = _one_line(text)
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def _qid(who: str) -> str:
    m = ID_RE.match((who or "").strip())
    if not m:
        raise Refused(f"`{who}` is not a question id (Q<n>)")
    return f"Q{int(m.group(1))}"


def _find(text: str, who: str) -> dict:
    qid = _qid(who)
    e = next((x for x in parse(text) if x["id"] == qid), None)
    if e is None:
        raise Refused(f"{qid} is not in questions.md")
    return e


def issue_short(url: str) -> str:
    """`autolens_workspace#670` for an issue URL; the URL itself otherwise."""
    m = ISSUE_RE.match(url or "")
    return f"{m.group(1)}#{m.group(2)}" if m else (url or "?")


def task_now(root: Path, task: str) -> "str | None":
    """Where the task's prompt is now: the path itself, else `active/<name>`
    (a draft claimed since), else None."""
    if not task.startswith(("draft/", "active/")) or ".." in Path(task).parts:
        return None
    if (root / task).is_file():
        return task
    act = f"active/{Path(task).name}"
    return act if (root / act).is_file() else None


def _today() -> str:
    return _dt.date.today().isoformat()


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


# --------------------------------------------------------------------------- #
# the watcher's add (a pure text function: the Mind writer calls it)
# --------------------------------------------------------------------------- #
def _labelled(options) -> str:
    out = []
    for i, o in enumerate([o for o in (options or []) if _one_line(o)][:OPTIONS_MAX]):
        o = _clip(o, OPTION_MAX)
        out.append(o if re.match(r"^\([a-z]\)\s", o) else f"({'abcd'[i]}) {o}")
    return " · ".join(out)


def entry_errors(entry: dict) -> "list[str]":
    """What is wrong with an add's entry; empty when it may be added."""
    if not isinstance(entry, dict):
        return ["the entry is not an object"]
    errs = [f"{k} is missing" for k in lifecycle.QUESTION_REQUIRED
            if not isinstance(entry.get(k), str) or not _one_line(entry.get(k))]
    if entry.get("kind") and entry.get("kind") not in lifecycle.QUESTION_KINDS:
        errs.append(f"kind must be one of {' | '.join(lifecycle.QUESTION_KINDS)}")
    task = entry.get("task")
    if isinstance(task, str) and task and (not task.startswith(("draft/", "active/"))
                                           or ".." in Path(task).parts):
        errs.append("task must be a draft/ or active/ prompt path")
    opts = entry.get("options", [])
    if not isinstance(opts, list) or not all(isinstance(o, str) for o in opts):
        errs.append("options must be a list of strings")
    return errs


def add_text(text: str, entry: dict, root: "Path | None" = None) -> "tuple[str, str, bool]":
    """(`questions.md` with `entry` added at the end of `## Open`, its id,
    whether it was added). An entry whose `(shift, task, issue)` is already
    in the file is a silent repeat: (text unchanged, that id, False).

    `entry`: {task, issue, kind, ask, options: [..], shift, asked, worker}.
    With `root` (the tree being written), `task` is resolved to where the
    prompt is now and refused when it is in neither `draft/` nor `active/`."""
    errs = entry_errors(entry)
    if errs:
        raise Refused("question add: " + "; ".join(errs))
    task = _one_line(entry["task"])
    if root is not None:
        now = task_now(Path(root), task)
        if now is None:
            raise Refused(f"question add: task {task} resolves to no draft/ or active/ prompt")
        task = now
    text = text if text.strip() else TEMPLATE
    entries = parse(text)
    issue, shift = _one_line(entry["issue"]), _one_line(entry["shift"])
    for e in entries:
        f = e["fields"]
        if (f.get("shift"), Path(f.get("task", "")).name, f.get("issue")) == \
                (shift, Path(task).name, issue):
            return text, e["id"], False
    n = max([e["n"] for e in entries] or [0]) + 1
    ask = _clip(entry["ask"], ASK_MAX)
    block = [f"### Q{n}. {Path(task).stem} — {_clip(ask, SHORT_MAX)}",
             f"- task: {task}", f"- issue: {issue}", f"- kind: {entry['kind']}",
             f"- ask: {ask}"]
    options = _labelled(entry.get("options"))
    if options:
        block.append(f"- options: {options}")
    block += [f"- shift: {shift}", f"- asked: {_one_line(entry['asked'])}",
              f"- worker: {_one_line(entry['worker'])}"]
    try:
        lines = lifecycle.question_insert(text.split("\n"), "open", block)
    except ValueError as e:
        raise Refused(str(e))
    return lifecycle._questions_tidy(lines), f"Q{n}", True


# --------------------------------------------------------------------------- #
# writing
# --------------------------------------------------------------------------- #
def _write(root: Path, writes: "list[tuple[str, str, str]]") -> None:
    """Write each `(path, old, new)`, undoing them all if they add a
    `lifecycle.py check` questions finding."""
    writes = [w for w in writes if w[1] != w[2]]
    if not writes:
        return
    before = {f.msg for f in lifecycle.questions_findings(root)}
    for rel, _old, new in writes:
        (root / rel).write_text(new, encoding="utf-8")
    added = [f.msg for f in lifecycle.questions_findings(root) if f.msg not in before]
    if added:
        for rel, old, _new in writes:
            p = root / rel
            if old is None:
                p.unlink(missing_ok=True)
            else:
                p.write_text(old, encoding="utf-8")
        raise Refused("the edit would add lifecycle drift: " + added[0])


def add(root: Path, entry: dict) -> str:
    old = _read(root)
    new, qid, added = add_text(old, entry, root)
    if not added:
        return f"{qid} already holds this question (same shift, task and issue) — no change"
    _write(root, [(FILE, old if (root / FILE).exists() else None, new)])
    return f"added {qid}"


def append_answer(prompt_text: str, line: str) -> str:
    """The prompt with `line` at the end of its `## Answers from the human`
    section (made at the end of the file when it has none)."""
    lines = prompt_text.rstrip("\n").split("\n")
    head = next((i for i, ln in enumerate(lines) if ln.strip() == ANSWERS_HEADING), None)
    if head is None:
        return "\n".join(lines + ["", ANSWERS_HEADING, line]) + "\n"
    end = next((j for j in range(head + 1, len(lines)) if lines[j].startswith("#")), len(lines))
    last = end - 1
    while last > head and not lines[last].strip():
        last -= 1
    lines[last + 1:last + 1] = [line]
    return "\n".join(lines) + "\n"


def answer(root: Path, who: str, text: str, comment: str = "", by: str = "",
           via: str = "chat", day: str = "", at: str = "") -> "tuple[str, str | None]":
    """Answer an Open or Deferred entry: (the ack, the prompt path appended to
    or None when the prompt is gone)."""
    old = _read(root)
    e = _find(old, who)
    if e["state"] not in ("open", "deferred"):
        raise Refused(f"{e['id']} is {e['state']} — reopen it first")
    said = _one_line(text)
    if not said:
        raise Refused("no answer text given")
    if via not in ("chat", "issue"):
        raise Refused("--via is chat or issue")
    comment = _one_line(comment)
    if comment and not comment.startswith("https://"):
        raise Refused("--comment must be the answer comment's URL")
    by = _one_line(by) or "the human"
    fields = {"answered": f"{at or _now()} by {by} ({via})", "answer": said}
    if comment:
        fields["answer-comment"] = comment
    new = lifecycle.question_move_text(old, e["id"], "answered", fields,
                                       drop=("until", "deferred"))
    f = e["fields"]
    writes = [(FILE, old, new)]
    prompt = task_now(root, f.get("task", ""))
    if prompt is not None:
        line = (f"- {e['id']} ({day or _today()}, shift {f.get('shift', '?')} question on "
                f"{issue_short(f.get('issue', ''))}): {said}" + (f" {comment}" if comment else ""))
        ptext = (root / prompt).read_text(encoding="utf-8")
        writes.append((prompt, ptext, append_answer(ptext, line)))
    _write(root, writes)
    if prompt is None:
        return (f"answered {e['id']} (the prompt {f.get('task')} is gone — the answer is "
                "recorded on the entry; no task is resumed)", None)
    return f"answered {e['id']}; the answer is in {prompt}", prompt


def defer(root: Path, who: str, until: str = "", by: str = "", day: str = "") -> str:
    old = _read(root)
    e = _find(old, who)
    if e["state"] not in ("open", "deferred"):
        raise Refused(f"{e['id']} is {e['state']} — reopen it first")
    until = (until or "").strip()
    if until and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", until):
        raise Refused("--until is a date, YYYY-MM-DD")
    fields = {"deferred": f"{day or _today()} by {_one_line(by) or 'the human'}"}
    if until:
        fields["until"] = until
    new = lifecycle.question_move_text(old, e["id"], "deferred", fields,
                                       drop=() if until else ("until",))
    _write(root, [(FILE, old, new)])
    return f"deferred {e['id']}" + (f" until {until}" if until else " to the next sitting")


def drop(root: Path, who: str, why: str, by: str = "", day: str = "") -> str:
    old = _read(root)
    e = _find(old, who)
    if e["state"] not in ("open", "deferred"):
        raise Refused(f"{e['id']} is {e['state']} — reopen it first")
    why = _one_line(why)
    if not why:
        raise Refused("drop needs --why")
    fields = {"dropped": f"{day or _today()} by {_one_line(by) or 'the human'} — {why} "
                         "(task shelved)"}
    new = lifecycle.question_move_text(old, e["id"], "dropped", fields,
                                       drop=("until", "deferred"))
    _write(root, [(FILE, old, new)])
    return f"dropped {e['id']} — its task stays held (shelved) until reopened, named in a " \
           "brief, or /add-ed"


def reopen(root: Path, who: str, day: str = "") -> str:
    old = _read(root)
    e = _find(old, who)
    if e["state"] == "open":
        return f"no change: {e['id']} is already open"
    new = lifecycle.question_move_text(old, e["id"], "open",
                                       {"reopened": day or _today()},
                                       drop=lifecycle.QUESTION_STATE_KEYS)
    _write(root, [(FILE, old, new)])
    return f"reopened {e['id']} (was {e['state']})"


def due(e: dict, today: str) -> bool:
    """Open, or Deferred with no `until:` or one that has passed."""
    if e["state"] == "open":
        return True
    return e["state"] == "deferred" and (e["fields"].get("until") or "") <= today


def show(root: Path, which: str = "", who: str = "", today: str = "") -> "list[str]":
    """The inbox, oldest first. `open`: Open plus Deferred entries that are
    due (a sitting's list); `all`: every entry; default: Open and Deferred."""
    entries = parse(_read(root))
    today = today or _today()
    if who:
        e = next((x for x in entries if x["id"] == _qid(who)), None)
        if e is None:
            raise Refused(f"{_qid(who)} is not in questions.md")
        return [f"{e['id']} [{e['state']}] {e['title']}"] + [
            f"  {k}: {v}" for k, v in e["fields"].items()]
    if which == "open":
        picked = [e for e in entries if due(e, today)]
    elif which == "all":
        picked = entries
    else:
        picked = [e for e in entries if e["state"] in ("open", "deferred")]
    picked.sort(key=lambda e: (e["fields"].get("asked", ""), e["n"]))
    out = []
    for e in picked:
        f = e["fields"]
        out.append(f"{e['id']} [{e['state']}] {e['title']} — {issue_short(f.get('issue', ''))}"
                   + (f" (until {f['until']})" if f.get("until") else ""))
    counts = {s.lower(): sum(e["state"] == s.lower() for e in entries)
              for s in lifecycle.QUESTION_SECTIONS}
    return (out or ["(no questions)"]) + [
        ", ".join(f"{n} {s}" for s, n in counts.items())]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="questions_edit.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(ROOT), help="the Mind checkout (default: this one)")
    sub = ap.add_subparsers(dest="verb", required=True)
    s = sub.add_parser("show")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--open", dest="which", action="store_const", const="open")
    g.add_argument("--all", dest="which", action="store_const", const="all")
    s.add_argument("qid", nargs="?", default="")
    s.add_argument("--today", default="", help=argparse.SUPPRESS)
    a = sub.add_parser("add")
    for k in ("task", "issue", "kind", "ask", "shift", "asked", "worker"):
        a.add_argument(f"--{k}", required=True)
    a.add_argument("--option", action="append", default=[])
    r = sub.add_parser("answer")
    r.add_argument("qid")
    r.add_argument("--text", required=True)
    r.add_argument("--comment", default="")
    r.add_argument("--by", default="")
    r.add_argument("--via", default="chat")
    r.add_argument("--date", default="", help=argparse.SUPPRESS)
    r.add_argument("--at", default="", help=argparse.SUPPRESS)
    d = sub.add_parser("defer")
    d.add_argument("qid")
    d.add_argument("--until", default="")
    d.add_argument("--by", default="")
    d.add_argument("--date", default="", help=argparse.SUPPRESS)
    p = sub.add_parser("drop")
    p.add_argument("qid")
    p.add_argument("--why", required=True)
    p.add_argument("--by", default="")
    p.add_argument("--date", default="", help=argparse.SUPPRESS)
    o = sub.add_parser("reopen")
    o.add_argument("qid")
    o.add_argument("--date", default="", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    root = Path(args.root)
    try:
        if args.verb == "show":
            print("\n".join(show(root, args.which or "", args.qid, args.today)))
            return 0
        if args.verb == "add":
            entry = {k: getattr(args, k) for k in
                     ("task", "issue", "kind", "ask", "shift", "asked", "worker")}
            entry["options"] = list(args.option)
            print(f"questions.md: {add(root, entry)}")
        elif args.verb == "answer":
            msg, prompt = answer(root, args.qid, args.text, args.comment, args.by, args.via,
                                 args.date, args.at)
            print(f"questions.md: {msg}")
            if prompt:
                print(f"prompt: {prompt}")
        elif args.verb == "defer":
            print(f"questions.md: {defer(root, args.qid, args.until, args.by, args.date)}")
        elif args.verb == "drop":
            print(f"questions.md: {drop(root, args.qid, args.why, args.by, args.date)}")
        elif args.verb == "reopen":
            print(f"questions.md: {reopen(root, args.qid, args.date)}")
    except Refused as e:
        print(f"questions_edit: refused — {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
