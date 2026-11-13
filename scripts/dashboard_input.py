#!/usr/bin/env python3
"""Apply one dashboard input to `queue.md` or `goals.md` — or refuse it.

The published Mind dashboard has a ★ on each task row and a Goals box. A tap
opens one issue in this repository and labels it `dashboard-input`, with a
machine account's token that holds Issues permission on this repository and
nothing else. The `issues: labeled` event runs `.github/workflows/dashboard_input.yml` from the
default branch, which calls this script on the event payload, commits what it
wrote and closes the issue with a one-line result (PyAutoMind#565, design C).

**Every input is untrusted.** Anyone holding a leaked token can open such an
issue with any body, so this script is the whole of what stands between them
and the two files. The rules:

- inputs are read from the event JSON in Python, never through a shell;
- the `dashboard-input` label must just have been added to an open, unlocked
  issue, and the issue opened and labelled by the one
  configured machine account (`DASHBOARD_INPUT_LOGIN`), which must not be
  the human's login (`HUMAN_LOGIN`) — both repository variables;
- past `RATE_MAX` inputs in the last hour, an input is refused unprocessed;
- the body is a fixed `key: value` form (`ISSUE_MARKER` first, then `op:`,
  `ref:` or `goals:`, `nonce:`); any other line refuses it;
- `op` is one of `star`, `unstar`, `goals`;
- a `ref` is a `draft/…/<name>.md` or `active/<name>.md` path of a real prompt
  file inside this checkout, matched whole — no `..`, no symlink, no shell or
  markdown metacharacter, no trailing newline can pass;
- goals are at most 10 lines of at most 200 characters, with no control or
  format characters and none of `` ` $ < > \\ | ``;
- the result must not add a `lifecycle.py check` finding about either file;
- only `queue.md` and `goals.md` may change (`guard` re-checks the git tree
  before the workflow commits).

A refusal writes nothing and leaves a one-line `refused — <reason>` result
for the issue; a reason never quotes the raw input, so no input can forge a
workflow command or markup in the comment.

    python3 scripts/dashboard_input.py apply --event FILE [--root DIR]
        [--message-file F] [--result-file F]
    python3 scripts/dashboard_input.py guard [--root DIR]

Exit codes: 0 applied (or already so), 1 refused, 2 usage.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: The only files this door may change.
WRITABLE = ("queue.md", "goals.md")
OPS = ("star", "unstar", "goals")

REF_MAX = 200
TITLE_MAX = 120
GOALS_MAX = 10
GOAL_TEXT_MAX = 200
GOALS_INPUT_MAX = 4000
#: One path segment: starts with a letter, digit or underscore (so never `.` or
#: `..`), then letters, digits, `_`, `.` and `-` only.
_SEG = r"[A-Za-z0-9_][A-Za-z0-9_.-]*"
REF_RE = re.compile(rf"^(?:draft/{_SEG}/{_SEG}(?:/{_SEG}){{0,2}}|active/{_SEG})\.md$")
NONCE_RE = re.compile(r"^[A-Za-z0-9-]{0,40}$")
#: Characters a one-line goal never needs, refused so no goal can be read as
#: markup or shell by any later reader.
GOAL_FORBIDDEN = set("`$<>\\|")
#: A list marker the human may type in the box (`1.`, `-`, `#`) — stripped,
#: because the file numbers goals itself.
_GOAL_MARKER_RE = re.compile(r"^(?:\d+[.)]|[-*+]|#+)\s+")

#: The issue the page opens: this label, this first body line.
LABEL = "dashboard-input"
ISSUE_MARKER = "<!-- mind-dashboard-input v1 -->"
BODY_MAX = 6000
_BODY_FIELD_RE = re.compile(r"([a-z]+):[ \t]*(.*)")

QUEUE_ENTRY_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
QUEUE_FIELD_RE = re.compile(r"^-\s+(kind|ref|note):\s*(.+?)\s*$")
GOAL_ENTRY_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")


class Refused(Exception):
    """The input is not applied. The message is safe to print: it never
    quotes the raw input."""


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #
def _clean_line(text: str) -> str:
    """One line of display text: no control/format characters, one space."""
    text = "".join(" " if unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp")
                   else ch for ch in text)
    return re.sub(r"\s+", " ", text).strip()


def validate_ref(root: Path, ref: str, *, must_exist: bool) -> str:
    """The ref, if it is a prompt path this door may name; else Refused."""
    if not ref:
        raise Refused("ref: missing")
    if len(ref) > REF_MAX:
        raise Refused(f"ref: longer than {REF_MAX} characters")
    if not REF_RE.fullmatch(ref):
        raise Refused("ref: not a draft/<work-type>/<target>/<name>.md or "
                      "active/<name>.md prompt path")
    if Path(ref).name in ("README.md", "AGENTS.md"):
        raise Refused("ref: names a folder's guidance file, not a prompt")
    if not must_exist:
        return ref
    for cand in (root / ref, root / "active" / Path(ref).name):
        if cand.is_symlink():
            raise Refused("ref: is a symlink")
        if cand.is_file():
            real = cand.resolve()
            inside = any(real.is_relative_to((root / d).resolve())
                         for d in ("draft", "active"))
            if not inside:
                raise Refused("ref: resolves outside draft/ and active/")
            return ref
    raise Refused("ref: no such prompt in draft/ or active/")


def validate_goals(raw: str) -> "list[str]":
    """The goals, top first, from the Goals box's text; else Refused."""
    if len(raw) > GOALS_INPUT_MAX:
        raise Refused(f"goals: longer than {GOALS_INPUT_MAX} characters")
    goals = []
    for n, line in enumerate(raw.replace("\r\n", "\n").split("\n"), 1):
        bad = [ch for ch in line if ch in GOAL_FORBIDDEN or (
            unicodedata.category(ch) in ("Cc", "Cf") and ch != "\t")]
        if bad:
            raise Refused(f"goals: line {n} contains a character goals may not "
                          "use (control or format characters, or one of "
                          "` $ < > \\ |)")
        text = _GOAL_MARKER_RE.sub("", line.replace("\t", " ").strip()).strip()
        text = re.sub(r"\s+", " ", text)
        if not text:
            continue
        if len(text) > GOAL_TEXT_MAX:
            raise Refused(f"goals: line {n} is {len(text)} characters — at most "
                          f"{GOAL_TEXT_MAX}")
        goals.append(text)
    if len(goals) > GOALS_MAX:
        raise Refused(f"goals: {len(goals)} goals — at most {GOALS_MAX}")
    return goals


def prompt_title(root: Path, ref: str) -> str:
    """The queue label for a prompt: its own `# ` title, cleaned and capped.

    Read from the file rather than taken from the request, so the label is
    never attacker text."""
    stem = Path(ref).stem.replace("_", " ")
    for cand in (root / ref, root / "active" / Path(ref).name):
        if not cand.is_file():
            continue
        for line in cand.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                title = _clean_line(line.lstrip("#"))
                title = "".join(ch for ch in title if ch not in "`<>")
                if title:
                    if len(title) > TITLE_MAX:
                        title = title[:TITLE_MAX - 1].rstrip() + "…"
                    return title
        break
    return stem


# --------------------------------------------------------------------------- #
# the issue
# --------------------------------------------------------------------------- #
def check_logins(allowed_login: str, human_login: str) -> None:
    """The dashboard writes as a dedicated machine account, never the human.

    The browser token belongs to `DASHBOARD_INPUT_LOGIN`. If that were the
    human's own login (`HUMAN_LOGIN`), a leaked token could speak as the human
    everywhere the human's word counts — shift steering commands, rulings in
    issue threads. So both must be configured, and they must differ."""
    if not allowed_login:
        raise Refused("no DASHBOARD_INPUT_LOGIN is configured — nobody may "
                      "write through the dashboard")
    if not human_login:
        raise Refused("no HUMAN_LOGIN is configured — the dashboard account "
                      "cannot be checked against the human's login")
    if allowed_login.strip().lower() == human_login.strip().lower():
        raise Refused("DASHBOARD_INPUT_LOGIN is the human's own login — the "
                      "dashboard token must belong to a dedicated machine account")


#: Issue spam: GitHub cannot be told to refuse an issue, so past this many
#: dashboard inputs in the last hour every new one is closed unprocessed.
RATE_MAX = 30


def rate_check(repo: str, token: str, now: "_dt.datetime | None" = None,
               fetch=None) -> int:
    """How many `dashboard-input` issues were opened in the last hour (this
    one included); Refused past RATE_MAX, or when the count cannot be read."""
    import urllib.parse
    import urllib.request
    now = now or _dt.datetime.now(_dt.timezone.utc)
    since = (now - _dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+", repo or ""):
        raise Refused("rate: no repository to count inputs in")
    q = f"repo:{repo} is:issue label:{LABEL} created:>={since}"
    url = "https://api.github.com/search/issues?per_page=1&q=" + urllib.parse.quote(q)

    def _get(u):
        req = urllib.request.Request(u, headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}", "User-Agent": "mind-dashboard-input"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    try:
        count = int((fetch or _get)(url).get("total_count"))
    except Exception:
        raise Refused("rate: could not count recent dashboard inputs; tap again")
    if count > RATE_MAX:
        raise Refused(f"rate: {count} dashboard inputs in the last hour — at most "
                      f"{RATE_MAX}; this one is closed unprocessed")
    return count


def should_respond(event: dict, allowed_login: str, human_login: str) -> "tuple[bool, str]":
    """(respond?, why not). Whether this run may write ANYTHING on the issue.

    The label can be added to any open Mind issue — a task issue, a live
    shift's issue — by anyone with Triage, a leaked dashboard token included.
    The workflow comments on, closes and locks only an issue the machine
    account itself opened AND labelled; on any other it writes nothing, so
    the label cannot be used to close or lock someone else's thread."""
    if not allowed_login or not human_login or \
            allowed_login.strip().lower() == human_login.strip().lower():
        return False, "the dashboard logins are not configured (or are the human's)"
    issue = event.get("issue")
    if not isinstance(issue, dict) or not isinstance(issue.get("number"), int):
        return False, "not an issue event"
    user, sender = issue.get("user") or {}, event.get("sender") or {}
    if user.get("type") != "User" or \
            str(user.get("login", "")).lower() != allowed_login.strip().lower():
        return False, "the issue was not opened by the dashboard account"
    if str(sender.get("login", "")).lower() != allowed_login.strip().lower():
        return False, "the label was not added by the dashboard account"
    if event.get("action") != "labeled" or \
            (event.get("label") or {}).get("name") != LABEL:
        return False, f"not the {LABEL} label being added"
    if issue.get("state") != "open" or issue.get("locked"):
        return False, "the issue is already answered (closed or locked)"
    return True, ""


def parse_issue(event: dict, allowed_login: str, human_login: str = "") -> dict:
    """The input an `issues: labeled` payload carries, or Refused.

    Who and what are both checked here: the label, the one configured author
    (a machine account that is not the human, and a User, not an App), and a
    body that is exactly the page's form."""
    check_logins(allowed_login, human_login)
    issue = event.get("issue")
    if not isinstance(issue, dict):
        raise Refused("event: not an issue event")
    number = issue.get("number")
    if not isinstance(number, int) or number <= 0:
        raise Refused("event: no issue number")
    # The trigger is the label being added (Triage can add one; only push
    # access can set one at creation). A re-label of an answered issue, or
    # someone else adding the label to the machine account's issue, is no input.
    if event.get("action") != "labeled" or \
            (event.get("label") or {}).get("name") != LABEL:
        raise Refused(f"event: not the {LABEL} label being added")
    if issue.get("state") != "open" or issue.get("locked"):
        raise Refused("issue: already answered (closed or locked)")
    sender = event.get("sender") or {}
    if str(sender.get("login", "")).lower() != allowed_login.lower():
        raise Refused("event: the label was not added by the dashboard account")
    user = issue.get("user") or {}
    if user.get("type") != "User" or str(user.get("login", "")).lower() \
            != allowed_login.lower():
        raise Refused("issue: not opened by the configured dashboard login")
    body = issue.get("body") or ""
    if not isinstance(body, str) or len(body) > BODY_MAX:
        raise Refused(f"issue body: missing or longer than {BODY_MAX} characters")
    lines = body.replace("\r\n", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines or lines[0].strip() != ISSUE_MARKER:
        raise Refused("issue body: not the dashboard's form")
    fields: "dict[str, str]" = {}
    goals: "list[str] | None" = None
    for line in lines[1:]:
        if goals is not None:
            if line.startswith("- "):
                goals.append(line[2:])
                continue
            if not line.strip():
                continue
        if not line.strip():
            continue
        m = _BODY_FIELD_RE.fullmatch(line.strip())
        if not m or m.group(1) not in ("op", "ref", "nonce", "goals") \
                or m.group(1) in fields:
            raise Refused("issue body: a line that is not one of op:, ref:, "
                          "nonce:, goals: (each once)")
        fields[m.group(1)] = m.group(2).strip()
        if m.group(1) == "goals":
            if fields["goals"]:
                raise Refused("issue body: goals are listed as `- ` lines")
            goals = []
    return {"number": number, "op": fields.get("op", ""),
            "ref": fields.get("ref", ""), "nonce": fields.get("nonce", ""),
            "goals": "\n".join(goals or [])}


# --------------------------------------------------------------------------- #
# queue.md
# --------------------------------------------------------------------------- #
def _live_blocks(lines: "list[str]") -> "list[dict]":
    """Each numbered `## <n>. <label>` entry outside a fence: its line span and
    fields. A block runs to the next heading of any level."""
    blocks, fenced, cur = [], False, None
    for i, line in enumerate(lines + ["#"]):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("#"):
            if cur is not None:
                cur["end"] = i
                blocks.append(cur)
            m = QUEUE_ENTRY_RE.match(line)
            cur = {"start": i, "label": m.group(2), "fields": {}} if m else None
            continue
        if cur is not None:
            m = QUEUE_FIELD_RE.match(line)
            if m and m.group(1) not in cur["fields"]:
                value = m.group(2)
                if m.group(1) != "note":
                    value = value.split("#")[0].strip()
                cur["fields"][m.group(1)] = value
    return blocks


def _queued(block: dict, name: str) -> bool:
    f = block["fields"]
    return f.get("kind") == "prompt" and Path(f.get("ref", "")).name == name


def _renumber(lines: "list[str]") -> "list[str]":
    out = list(lines)
    for n, b in enumerate(_live_blocks(out), 1):
        out[b["start"]] = f"## {n}. {b['label']}"
    return out


def _tidy(lines: "list[str]") -> str:
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return text.rstrip("\n") + "\n"


def queue_position(text: str, ref: str) -> "int | None":
    """The 1-based place of the entry queuing `ref`'s prompt, or None."""
    name = Path(ref).name
    for n, b in enumerate(_live_blocks(text.split("\n")), 1):
        if _queued(b, name):
            return n
    return None


def queue_star(text: str, ref: str, title: str) -> "tuple[str, int, bool]":
    """(new text, position, changed). Appends a `kind: prompt` entry as the
    last live entry, before `## Retired`. Already queued is a no-op."""
    pos = queue_position(text, ref)
    if pos is not None:
        return text, pos, False
    lines = text.split("\n")
    blocks = _live_blocks(lines)
    entry = [f"## 0. {title}", "- kind: prompt", f"- ref: {ref}",
             f"- note: starred on the dashboard ({_dt.date.today().isoformat()})", ""]
    if blocks:
        at = blocks[-1]["end"]
        while at > blocks[-1]["start"] + 1 and not lines[at - 1].strip():
            at -= 1
        lines[at:at] = [""] + entry
    else:
        head = next((i for i, ln in enumerate(lines) if ln.strip() == "## Retired"), None)
        if head is None:
            while lines and not lines[-1].strip():
                lines.pop()
            lines += [""] + entry
        else:
            lines[head:head] = entry + [""]
    new = _tidy(_renumber(lines))
    return new, queue_position(new, ref) or 0, True


def queue_unstar(text: str, ref: str, day: str) -> "tuple[str, bool]":
    """(new text, changed). Every live entry queuing `ref`'s prompt moves to
    the `## Retired` footer with `shelved-as:`, keeping its note."""
    name = Path(ref).name
    lines = text.split("\n")
    moving = [b for b in _live_blocks(lines) if _queued(b, name)]
    if not moving:
        return text, False
    for b in reversed(moving):
        del lines[b["start"]:b["end"]]
    retired = []
    for b in moving:
        retired += [f"### {b['label']}",
                    f"- shelved-as: unstarred on the dashboard ({day})"]
        if b["fields"].get("note"):
            retired.append(f"- note: {b['fields']['note']}")
        retired.append("")
    head = next((i for i, ln in enumerate(lines) if ln.strip() == "## Retired"), None)
    if head is None:
        while lines and not lines[-1].strip():
            lines.pop()
        lines += ["", "## Retired", ""] + retired
    else:
        first = next((i for i in range(head + 1, len(lines))
                      if lines[i].startswith("### ") or lines[i].startswith("## ")),
                     len(lines))
        lines[first:first] = ([""] if first == len(lines) else []) + retired
    return _tidy(_renumber(lines)), True


# --------------------------------------------------------------------------- #
# goals.md
# --------------------------------------------------------------------------- #
def _goal_blocks(text: str) -> "tuple[list[str], list[dict]]":
    """(header lines before the first goal, goals with their field lines)."""
    lines = text.split("\n")
    header, goals, fenced, cur = [], [], False, None
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("#"):
            m = GOAL_ENTRY_RE.match(line)
            if m:
                cur = {"text": m.group(2), "fields": []}
                goals.append(cur)
                continue
            if goals:
                # A non-goal heading after the list: kept with the goal above.
                cur["fields"].append(line)
                continue
        if cur is None:
            header.append(line)
        elif line.strip():
            cur["fields"].append(line)
    return header, goals


def goals_write(text: str, goals: "list[str]") -> "tuple[str, bool]":
    """(new goals.md, changed). The header prose is kept; a goal whose text is
    unchanged keeps its `epics:`/`tags:`/`note:` lines even if it moved."""
    header, old = _goal_blocks(text)
    if [g["text"] for g in old] == goals:
        return text, False
    fields = {}
    for g in old:
        fields.setdefault(g["text"], g["fields"])
    lines = list(header)
    while lines and not lines[-1].strip():
        lines.pop()
    for n, goal in enumerate(goals, 1):
        lines += ["", f"## {n}. {goal}"] + fields.get(goal, [])
    return "\n".join(lines).rstrip("\n") + "\n", True


# --------------------------------------------------------------------------- #
# the lifecycle check, before and after
# --------------------------------------------------------------------------- #
def check_problems(root: Path) -> "set[str]":
    """The drift lines `lifecycle.py check --paths queue.md goals.md` reports.

    Compared before and after the write, so drift already on main never
    blames a tap — only a finding the write adds refuses it."""
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "lifecycle.py"), "check",
         "--paths", *WRITABLE],
        cwd=root, capture_output=True, text=True,
        env=dict(os.environ, LIFECYCLE_NO_GH="1"))
    if proc.returncode not in (0, 1):
        raise Refused(f"lifecycle.py check could not run (exit {proc.returncode})")
    return {ln.strip()[2:] for ln in proc.stdout.splitlines()
            if ln.startswith("  - ")}


# --------------------------------------------------------------------------- #
# apply
# --------------------------------------------------------------------------- #
def apply(root: Path, op: str, ref: str = "", goals_raw: str = "",
          nonce: str = "", today: "str | None" = None) -> dict:
    """Validate and apply one input. Returns the result; raises Refused with
    nothing written."""
    day = today or _dt.date.today().isoformat()
    if op not in OPS:
        raise Refused("op: not one of " + ", ".join(OPS))
    if not NONCE_RE.fullmatch(nonce):
        raise Refused("nonce: letters, digits and '-' only, at most 40")
    queue_md, goals_md = root / "queue.md", root / "goals.md"
    for f in (queue_md, goals_md):
        if f.is_symlink():
            raise Refused(f"{f.name}: is a symlink")
    before_text = {f: (f.read_text(encoding="utf-8") if f.is_file() else None)
                   for f in (queue_md, goals_md)}
    name = Path(ref).name if ref else ""

    if op == "star":
        ref = validate_ref(root, ref, must_exist=True)
        text = before_text[queue_md] or "# Queue\n"
        new, pos, changed = queue_star(text, ref, prompt_title(root, ref))
        target = queue_md
        message = f"dashboard: ★ queue {Path(ref).stem} (#{pos})"
        summary = (f"★ queued `{ref}` at #{pos}" if changed
                   else f"`{ref}` was already queued at #{pos} — nothing to do")
    elif op == "unstar":
        ref = validate_ref(root, ref, must_exist=False)
        text = before_text[queue_md] or ""
        if queue_position(text, ref) is None:
            validate_ref(root, ref, must_exist=True)
        new, changed = queue_unstar(text, ref, day) if text else (text, False)
        pos = None
        target = queue_md
        message = f"dashboard: unqueue {Path(ref).stem}"
        summary = (f"unqueued `{ref}` (moved to the Retired footer)" if changed
                   else f"`{ref}` was not queued — nothing to do")
    else:
        goals = validate_goals(goals_raw)
        text = before_text[goals_md] or "# Goals\n"
        new, changed = goals_write(text, goals)
        pos = None
        target = goals_md
        message = f"dashboard: goals ({len(goals)})"
        summary = (f"goals set ({len(goals)})" if changed
                   else "goals unchanged — nothing to do")

    result = {"ok": True, "op": op, "ref": ref, "name": name, "position": pos,
              "changed": changed, "file": target.name, "summary": summary,
              "message": message}
    if not changed:
        return result

    before = check_problems(root)
    target.write_text(new, encoding="utf-8")
    try:
        added = sorted(check_problems(root) - before)
    except Refused:
        _restore(before_text)
        raise
    if added:
        _restore(before_text)
        raise Refused("the write would add lifecycle.py check drift: "
                      + "; ".join(added)[:600])
    return result


def _restore(before_text: dict) -> None:
    for f, text in before_text.items():
        if text is None:
            f.unlink(missing_ok=True)
        else:
            f.write_text(text, encoding="utf-8")


def commit_message(result: dict, actor: str = "", run_id: str = "",
                   issue: int = 0) -> str:
    actor = re.sub(r"[^A-Za-z0-9\[\]-]", "", actor)[:40]
    run_id = re.sub(r"[^0-9]", "", run_id)[:20]
    lines = [result["message"], "", result["summary"], ""]
    if issue:
        lines.append(f"Input-issue: #{int(issue)}")
    if actor:
        lines.append(f"Dispatched-by: {actor}")
    if run_id:
        lines.append(f"Run: {run_id}")
    lines.append("Via: mind-dashboard")
    return "\n".join(lines) + "\n"


def changed_paths(root: Path) -> "list[str]":
    """Every path git sees as changed or untracked under `root`."""
    proc = subprocess.run(["git", "status", "--porcelain", "-z",
                           "--untracked-files=all"],
                          cwd=root, capture_output=True, text=True, check=True)
    out = []
    for item in proc.stdout.split("\0"):
        if len(item) > 3:
            out.append(item[3:])
    return out


def result_line(result: "dict | None", reason: str = "") -> str:
    """The issue's one-line result comment; the page reads its first word."""
    if result is None:
        return f"dashboard-input: refused — {_clean_line(reason)}"
    word = "applied" if result["changed"] else "no change"
    return f"dashboard-input: {word} — {result['summary']}"


def _summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(text)


def _output(key: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(f"{key}={value}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="dashboard_input.py")
    ap.add_argument("verb", choices=["apply", "guard"])
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--event", type=Path, default=None,
                    help="apply: the issues event JSON (default $GITHUB_EVENT_PATH)")
    ap.add_argument("--message-file", type=Path, default=None,
                    help="apply: write the commit message here when a file changed")
    ap.add_argument("--result-file", type=Path, default=None,
                    help="apply: write the one-line issue result here")
    ap.add_argument("--rate-check", action="store_true",
                    help="apply: refuse past RATE_MAX inputs in the last hour "
                         "(GitHub search; needs GITHUB_REPOSITORY and GH_TOKEN)")
    a = ap.parse_args(argv)
    root = a.root.resolve()

    if a.verb == "guard":
        stray = sorted(p for p in changed_paths(root) if p not in WRITABLE)
        if stray:
            print("::error title=Dashboard input refused::the tree changed outside "
                  f"queue.md and goals.md ({len(stray)} path(s)) — nothing is committed")
            for p in stray:
                print(f"  stray: {p!r}")
            return 1
        print("guard: only " + " / ".join(WRITABLE) + " changed")
        return 0

    event_path = a.event or (Path(os.environ["GITHUB_EVENT_PATH"])
                             if os.environ.get("GITHUB_EVENT_PATH") else None)
    if event_path is None:
        print("apply: --event or GITHUB_EVENT_PATH is required", file=sys.stderr)
        return 2
    lock = "resolved"
    allowed = os.environ.get("DASHBOARD_INPUT_LOGIN", "")
    human = os.environ.get("HUMAN_LOGIN", "")
    try:
        event = json.loads(event_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        event = None
    respond, why = should_respond(event, allowed, human) if isinstance(event, dict) \
        else (False, "the event could not be read")
    if not respond:
        # Not the dashboard's own input: touch nothing on the issue. A
        # misconfiguration still fails the run, loudly, without writing.
        _output("respond", "false")
        if "logins are not configured" in why:
            try:
                check_logins(allowed, human)
            except Refused as e:
                why = str(e)
            print(f"::error title=Dashboard input refused::{why}; nothing is written")
            _output("outcome", "refused")
            return 1
        level = "notice" if "not opened by" in why or "not an issue" in why else "warning"
        print(f"::{level} title=Dashboard input ignored::{why}; nothing is written")
        _output("outcome", "ignored")
        return 0
    _output("respond", "true")
    try:
        req = parse_issue(event, os.environ.get("DASHBOARD_INPUT_LOGIN", ""),
                          os.environ.get("HUMAN_LOGIN", ""))
        if a.rate_check:
            try:
                rate_check(os.environ.get("GITHUB_REPOSITORY", ""),
                           os.environ.get("GH_TOKEN", ""))
            except Refused:
                lock = "spam"
                raise
        result = apply(root, req["op"], ref=req["ref"], goals_raw=req["goals"],
                       nonce=req["nonce"])
    except (Refused, ValueError, OSError) as e:
        reason = str(e) if isinstance(e, Refused) else "the event could not be read"
        line = result_line(None, reason)
        if a.result_file:
            a.result_file.write_text(line + "\n", encoding="utf-8")
        print(f"::error title=Dashboard input refused::{_clean_line(reason).replace('::', ': :')}")
        _summary(f"## Dashboard input refused\n\n{_clean_line(reason)}\n\n"
                 "Nothing was committed.\n")
        _output("outcome", "refused")
        _output("lock", lock)
        return 1
    if a.result_file:
        a.result_file.write_text(result_line(result) + "\n", encoding="utf-8")
    if result["changed"] and a.message_file:
        a.message_file.write_text(commit_message(
            result, os.environ.get("GITHUB_ACTOR", ""), os.environ.get("GITHUB_RUN_ID", ""),
            req["number"]), encoding="utf-8")
    _output("outcome", "applied" if result["changed"] else "unchanged")
    _output("lock", "resolved")
    print(result["summary"])
    _summary(f"## Dashboard input — {result['op']}\n\n{result['summary']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
