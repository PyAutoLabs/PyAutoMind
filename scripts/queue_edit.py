#!/usr/bin/env python3
"""Edit `queue.md`, the human's ranked list, for a `/queue` chat.

`queue.md` has one writer: the human, in a chat that ran `/queue`
(PyAutoBrain `skills/queue`, PyAutoBrain#640). That skill never hand-edits the
markdown; it runs this script in a temporary Mind worktree detached on
`origin/main`, then commits with `prompt_sync_push` and runs
`lifecycle.py check`.

    python3 scripts/queue_edit.py show
    python3 scripts/queue_edit.py add  <ref> [--note TEXT] [--at N|top] [--label TEXT]
    python3 scripts/queue_edit.py remove <who> [--why TEXT]
    python3 scripts/queue_edit.py move <who> up|down|top|bottom|<n>

`<ref>` names one prompt in `draft/` or `active/`, read from its FIRST line
only: the dashboard's copy text (`Use the start-dev skill. <path>`), a path or
GitHub link alone, a whole pasted prompt (its `# Title` line, matched
exactly), or on a one-line paste a basename or exact title. Give `-` to read
it from stdin. A ref that resolves to no draft/ or active/ prompt
is refused. `<who>` names a live entry: its rank (`3` or `#3`), its ref, or its
label.

Ranks are the planner's: `kind: prompt` entries in file order (PyAutoBrain
`_steer.read_queue`). Every write renumbers the headings `1..n`, so a heading's
number is its rank. `remove` moves the entry to the `## Retired` footer with
`shelved-as:`, keeping its note (`lifecycle.queue_retire_text`, the same
footer form `lifecycle.py close` writes). A write that would add a
`lifecycle.py check` queue finding is undone and refused.

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

#: A prompt path anywhere in a paste: bare, in backticks, or inside a URL.
PATH_RE = re.compile(r"(?:^|[\s`'\"(/])((?:draft|active)/[A-Za-z0-9_.\-/]+?\.md)(?=$|[\s`'\")#?,;:.])")
FIELD_RE = re.compile(r"^-\s+(kind|ref|note):\s*(.*?)\s*$")
RANK_RE = re.compile(r"^#?(\d+)\.?$")
WHERE = ("up", "down", "top", "bottom")


class Refused(Exception):
    """The edit is not made; the message says why."""


# --------------------------------------------------------------------------- #
# reading
# --------------------------------------------------------------------------- #
def _blocks(lines: "list[str]") -> "list[dict]":
    """Each numbered `## <n>. <label>` entry outside a fence: its line span
    `[start, end)` and fields. A block runs to the next heading of any level,
    exactly as `lifecycle.queue_entries` and the planner read it."""
    out, fenced, cur = [], False, None
    for i, line in enumerate(lines + ["#"]):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or not line.startswith("#"):
            if cur is not None and not fenced:
                m = FIELD_RE.match(line)
                if m and m.group(1) not in cur:
                    value = m.group(2)
                    cur[m.group(1)] = value if m.group(1) == "note" \
                        else value.split("#")[0].strip()
            continue
        if cur is not None:
            cur["end"] = i
            out.append(cur)
        m = lifecycle.QUEUE_ENTRY_RE.match(line)
        cur = {"start": i, "label": m.group(1)} if m else None
    return out


def entries(text: str) -> "list[dict]":
    """The live entries, top first: `{label, kind, ref, note, start, end}`."""
    return [dict(b, kind=b.get("kind", ""), ref=b.get("ref", ""),
                 note=b.get("note", "")) for b in _blocks(text.split("\n"))]


def _read(root: Path) -> str:
    try:
        return (root / "queue.md").read_text(encoding="utf-8")
    except OSError:
        raise Refused("queue.md: not found in " + str(root))


def _title(path: Path) -> str:
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.startswith("# "):
                    return line[2:].strip()
                if line.strip():
                    break
    except OSError:
        pass
    return path.stem.replace("_", " ")


def _prompts(root: Path) -> "list[Path]":
    """Every live prompt: `draft/**/*.md` and `active/*.md`."""
    out = sorted(p for p in (root / "draft").rglob("*.md")
                 if p.is_file() and p.name not in ("AGENTS.md", "README.md"))
    out += sorted(p for p in (root / "active").glob("*.md") if p.is_file())
    return out


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip(".:—-").strip()).lower()


#: The first line forms that name a path: the dashboard's 📋 line, or the
#: path alone (bare, in backticks, or as a GitHub link to it).
COPY_LINE_RE = re.compile(r"^Use the start-dev skill\.\s+`?(\S+?\.md)`?\s*$")
BARE_PATH_RE = re.compile(
    r"^`?(?:https://github\.com/[^/\s]+/[^/\s]+/blob/[^/\s]+/)?"
    r"((?:draft|active)/[A-Za-z0-9_.\-/]+\.md)`?$")


def _found(root: Path, rel: str) -> "tuple[str, str]":
    if ".." in Path(rel).parts or not rel.startswith(("draft/", "active/")):
        raise Refused(f"`{rel}` is not a draft/ or active/ prompt path")
    if (root / rel).is_file():
        return rel, _title(root / rel)
    if lifecycle._queue_ref_resolves(root, rel):  # issued: now in active/
        act = f"active/{Path(rel).name}"
        return act, _title(root / act)
    raise Refused(f"`{rel}` resolves to no draft/ or active/ prompt")


def _one(root: Path, hits: "list[Path]", said: str,
         near: "list[Path] | None" = None) -> "tuple[str, str]":
    if len(hits) == 1:
        return hits[0].relative_to(root).as_posix(), _title(hits[0])
    listed = hits or near or []
    names = ", ".join(p.relative_to(root).as_posix() for p in listed[:5])
    if len(hits) > 1:
        raise Refused(f"`{said[:80]}` matches {len(hits)} prompts ({names}) — give the path")
    raise Refused(f"`{said[:80]}` resolves to no draft/ or active/ prompt"
                  + (f" (did you mean: {names}?)" if names else ""))


def resolve_prompt(root: Path, ref: str) -> "tuple[str, str]":
    """(path relative to the Mind, title) of the one prompt `ref` names.

    Only the paste's FIRST non-blank line is read, never the body: a real
    prompt cites other prompts, and taking a path from its body queues the
    wrong task. In order:

    a. the dashboard's 📋 line `Use the start-dev skill. <path>`, or a path
       alone (bare, in backticks, or a GitHub link);
    b. a paste that opens with `# ` — a whole prompt — matched exactly, by
       title, against the draft/ and active/ prompt files;
    c. a one-line paste: a prompt basename, or an exact title.

    Anything else, an ambiguous title included, is refused with candidates."""
    text = (ref or "").strip()
    if not text:
        raise Refused("no task given")
    lines = text.split("\n")
    first = lines[0].strip()
    m = COPY_LINE_RE.match(first) or BARE_PATH_RE.match(first)
    if m:
        return _found(root, m.group(1))
    prompts = _prompts(root)
    if first.startswith("# "):
        want = _norm(first[2:])
        titled = [(p, _norm(_title(p))) for p in prompts]
        return _one(root, [p for p, t in titled if t == want], first,
                    [p for p, t in titled if want and want in t])
    if len(lines) > 1:
        raise Refused("a multi-line paste must open with the 📋 line, a prompt "
                      "path, or the prompt's `# Title` line")
    if first.endswith(".md") or ("/" not in first and " " not in first):
        name = first if first.endswith(".md") else first + ".md"
        hits = [p for p in prompts if p.name == Path(name).name]
        if hits or "/" in first:
            return _one(root, hits, first)
    want = _norm(first)
    titled = [(p, _norm(_title(p))) for p in prompts]
    return _one(root, [p for p, t in titled if t == want], first,
                [p for p, t in titled if len(want) >= 4 and want in t])


def find_entry(root: Path, live: "list[dict]", who: str) -> int:
    """The index in `live` (the queue's prompt entries) that `who` names."""
    who = (who or "").strip()
    m = RANK_RE.match(who)
    if m:
        n = int(m.group(1))
        if not 1 <= n <= len(live):
            raise Refused(f"there is no #{n} — the queue has {len(live)} entr"
                          + ("y" if len(live) == 1 else "ies"))
        return n - 1
    paths = PATH_RE.findall(who)
    names = {Path(p).name for p in paths} or (
        {who if who.endswith(".md") else who + ".md"} if " " not in who else set())
    for i, e in enumerate(live):
        if Path(e["ref"]).name in names:
            return i
    want = _norm(who)
    for i, e in enumerate(live):
        if _norm(e["label"]) == want or _norm(_title(root / e["ref"])) == want:
            return i
    hits = [i for i, e in enumerate(live) if len(want) >= 4 and want in _norm(e["label"])]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        raise Refused(f"`{who[:80]}` matches {len(hits)} queued entries — "
                      "give its number")
    raise Refused(f"`{who[:80]}` is not in the queue")


# --------------------------------------------------------------------------- #
# writing
# --------------------------------------------------------------------------- #
def _render(text: str, order: "list[dict]") -> str:
    """`text` with its live entries replaced by `order`, renumbered 1..n."""
    lines = text.split("\n")
    blocks = _blocks(lines)
    if blocks:
        for a, b in zip(blocks, blocks[1:]):
            if any(ln.strip() for ln in lines[a["end"]:b["start"]]):
                raise Refused("queue.md has a heading between two entries; "
                              "fix it by hand first")
        head, tail = lines[:blocks[0]["start"]], lines[blocks[-1]["end"]:]
    else:
        at = next((i for i, ln in enumerate(lines) if ln.strip() == "## Retired"),
                  len(lines))
        head, tail = lines[:at], lines[at:]
    while head and not head[-1].strip():
        head.pop()
    body: "list[str]" = []
    for n, e in enumerate(order, 1):
        block = [f"## {n}. {e['label']}"] + list(e["body"])
        while len(block) > 1 and not block[-1].strip():
            block.pop()
        body += block + [""]
    while tail and not tail[0].strip():
        tail.pop(0)
    out = head + [""] + body + (tail if tail else [])
    return "\n".join(out).rstrip("\n") + "\n"


def _with_bodies(text: str) -> "list[dict]":
    lines = text.split("\n")
    return [dict(e, body=lines[e["start"] + 1:e["end"]]) for e in entries(text)]


def _live(es: "list[dict]") -> "list[dict]":
    odd = [e for e in es if e["kind"] != "prompt" or not e["ref"]]
    if odd:
        raise Refused(f"queue.md entry `{odd[0]['label']}` is not a `kind: prompt` "
                      "entry with a ref — move it under `## Retired` first")
    return es


def _write(root: Path, old: str, new: str) -> None:
    """Write `new`, undoing it if it adds a `lifecycle.py check` queue finding."""
    if new == old:
        return
    before = {f.msg for f in lifecycle.queue_findings(root)}
    path = root / "queue.md"
    path.write_text(new, encoding="utf-8")
    added = [f.msg for f in lifecycle.queue_findings(root) if f.msg not in before]
    if added:
        path.write_text(old, encoding="utf-8")
        raise Refused("the edit would add lifecycle drift: " + added[0])


def _one_line(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def add(root: Path, ref: str, note: str = "", at: "str | int | None" = None,
        label: str = "") -> str:
    text = _read(root)
    es = _live(_with_bodies(text))
    rel, title = resolve_prompt(root, ref)
    for n, e in enumerate(es, 1):
        if Path(e["ref"]).name == Path(rel).name:
            raise Refused(f"already queued at #{n} ({e['label']}) — "
                          "say move to change its place")
    pos = len(es)
    if at not in (None, ""):
        pos = 0 if str(at) == "top" else _rank(str(at), len(es) + 1) - 1
    label = _one_line(label) or _one_line(title)
    body = ["- kind: prompt", f"- ref: {rel}"]
    if _one_line(note):
        body.append(f"- note: {_one_line(note)}")
    es.insert(pos, {"label": label, "body": body, "ref": rel})
    _write(root, text, _render(text, es))
    return f"added `{label}` at #{pos + 1}"


def remove(root: Path, who: str, why: str = "", day: str = "") -> str:
    text = _read(root)
    es = _live(_with_bodies(text))
    e = es[find_entry(root, es, who)]
    day = day or _dt.date.today().isoformat()
    shelved = f"{e['ref']} — off the queue {day}" + (f"; {_one_line(why)}" if _one_line(why) else "")
    new, moved = lifecycle.queue_retire_text(text, Path(e["ref"]).name, shelved,
                                             key="shelved-as", by="a `/queue` chat")
    if not moved:
        raise Refused(f"`{who}` is not in the queue")
    new = _render(new, _with_bodies(new))
    _write(root, text, new)
    return f"removed `{e['label']}` (to ## Retired, shelved-as:)"


def _rank(where: str, size: int) -> int:
    m = RANK_RE.match(where.strip())
    if not m:
        raise Refused(f"`{where}` is not up, down, top, bottom or a number")
    n = int(m.group(1))
    if not 1 <= n <= size:
        raise Refused(f"#{n} is out of range — 1 to {size}")
    return n


def move(root: Path, who: str, where: str) -> str:
    text = _read(root)
    es = _live(_with_bodies(text))
    i = find_entry(root, es, who)
    w = where.strip().lower()
    j = {"up": max(i - 1, 0), "down": min(i + 1, len(es) - 1), "top": 0,
         "bottom": len(es) - 1}.get(w)
    if j is None:
        j = _rank(w, len(es)) - 1
    if i == j:  # a no-op writes nothing, not even a renumber
        return f"no change: `{es[i]['label']}` stays at #{i + 1}"
    e = es.pop(i)
    es.insert(j, e)
    _write(root, text, _render(text, es))
    return f"moved `{e['label']}` from #{i + 1} to #{j + 1}"


def show(root: Path) -> "list[str]":
    """The queue as a numbered list: `n. label — ref`."""
    es = entries(_read(root))
    out = []
    n = 0
    for e in es:
        if e["kind"] == "prompt" and e["ref"]:
            n += 1
            out.append(f"{n}. {e['label']} — {e['ref']}")
        else:
            out.append(f"–  {e['label']} (kind: {e['kind'] or 'none'}; not ranked)")
    return out or ["(the queue is empty)"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="queue_edit.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(ROOT), help="the Mind checkout (default: this one)")
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("show")
    a = sub.add_parser("add")
    a.add_argument("ref", help="a prompt path, link, copy text, title, or - for stdin")
    a.add_argument("--note", default="")
    a.add_argument("--at", default=None, help="a rank, or top (default: bottom)")
    a.add_argument("--label", default="")
    r = sub.add_parser("remove")
    r.add_argument("who")
    r.add_argument("--why", default="")
    r.add_argument("--date", default="", help=argparse.SUPPRESS)
    m = sub.add_parser("move")
    m.add_argument("who")
    m.add_argument("where", help="up, down, top, bottom or a rank")
    args = ap.parse_args(argv)
    root = Path(args.root)
    try:
        if args.verb == "add":
            ref = sys.stdin.read() if args.ref == "-" else args.ref
            print(f"queue.md: {add(root, ref, args.note, args.at, args.label)}")
        elif args.verb == "remove":
            print(f"queue.md: {remove(root, args.who, args.why, args.date)}")
        elif args.verb == "move":
            print(f"queue.md: {move(root, args.who, args.where)}")
    except Refused as e:
        print(f"queue_edit: refused — {e}", file=sys.stderr)
        return 1
    print("\n".join(show(root)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
