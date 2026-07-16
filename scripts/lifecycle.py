#!/usr/bin/env python3
"""PyAutoMind prompt-file lifecycle engine.

The Mind runs the prompt file through three states that mirror the task ledger:

    draft/<work-type>/<target>/<name>.md   intaken, not started   (backlog)
    active/<name>.md                        issued, in flight      (active.md)
    complete/<YYYY>/<MM>/<slug>.md          shipped                (the record IS the ledger)

Completion state lives ONLY in the dated records plus the generated
`complete/index.md`. The monolithic `complete.md` ledger was retired on
2026-07-16 (issue #81) — its history is in git, and the one-time split/backfill
tooling (`split-complete`, `migrate`) was deleted with it.

Subcommands
-----------
  move <name> [--date YYYY-MM-DD]
        Advance one file active/<name>.md -> complete/<YYYY>/<MM>/<name>.md.
        Date from --date, else inferred from an existing dated record with the
        same slug. For a shipped task prefer `record`, which writes the rich
        record and folds the prompt in one step.

  record <slug> --date YYYY-MM-DD --from-file <path> [--prompt <name>]
        The ship_* hook: write complete/<YYYY>/<MM>/<slug>.md from the rich
        completion body in <path> (drafted by the ship skill), folding and
        removing the active/ prompt. Run `index --apply` afterwards.

  index [--apply | --check]
        Generate complete/index.md (token-light navigation over the records);
        --check fails if it is stale (CI).

  check
        Drift guard (mirrors repos_sync.py --check; non-zero exit on drift):
          * no active.md slug has a complete/ record (finished but still active)
          * no file lives in two states at once
        Wire into /health and CI.

This file is intentionally stdlib-only (no PyAuto imports) so it runs in any
environment, including a bare template checkout.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTIVE_DIR = ROOT / "active"
COMPLETE_DIR = ROOT / "complete"
# complete/archive/ holds non-record material (retired epic trackers, shelved
# prompts) — NOT dated task records, so check/index skip it.
ARCHIVE_DIR = COMPLETE_DIR / "archive"
DRAFT_DIR = ROOT / "draft"
ACTIVE_MD = ROOT / "active.md"

H2_RE = re.compile(r"^##\s+(.+?)\s*$")


def _slugify_h2(heading: str) -> str:
    """First token of an H2 heading is the task slug: `## slug (parenthetical)`."""
    return heading.split("(")[0].strip()


def safe_name(slug: str) -> str:
    """Kebab-case filename stem safe for the filesystem (no spaces/slashes).

    Used for BOTH writing complete/ filenames and comparing them back in
    `check`, so the round-trip is consistent (a raw H2 slug may carry spaces,
    `/`, em-dashes, etc.)."""
    s = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return s or "untitled"


def ledger_slugs(path: Path) -> "set[str]":
    """H2 task slugs recorded in a ledger file (active.md)."""
    slugs = set()
    if not path.exists():
        return slugs
    for line in path.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            slugs.add(_slugify_h2(m.group(1)))
    return slugs


def complete_bucket(date: "tuple[str, str] | None") -> Path:
    if date is None:
        return COMPLETE_DIR / "unknown"
    return COMPLETE_DIR / date[0] / date[1]


def _parse_date(arg: str) -> "tuple[str, str] | None":
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", arg)
    return (m.group(1), m.group(2)) if m else None


def _record_bucket_for(name: str) -> "Path | None":
    """Bucket of an existing dated record whose slug matches <name>, if any."""
    want = safe_name(name)
    for _, slug, path in _all_records():
        if safe_name(slug) == want:
            return path.parent
    return None


# --------------------------------------------------------------------------- #
# move
# --------------------------------------------------------------------------- #
def cmd_move(args) -> int:
    name = args.name
    if name.endswith(".md"):
        name = name[:-3]
    src = ACTIVE_DIR / f"{name}.md"
    if not src.exists():
        print(f"lifecycle move: not found in active/: {src.name}", file=sys.stderr)
        return 1

    if args.date:
        date = _parse_date(args.date)
        if date is None:
            print(f"lifecycle move: bad --date {args.date!r}", file=sys.stderr)
            return 1
        bucket = complete_bucket(date)
    else:
        bucket = _record_bucket_for(name)
        if bucket is None:
            print(
                f"lifecycle move: no --date and no existing record for {name!r}; "
                f"pass --date",
                file=sys.stderr,
            )
            return 1

    dest = bucket / src.name
    print(f"active/{src.name} -> {dest.relative_to(ROOT)}")
    if not args.apply:
        print("(dry run; pass --apply)")
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Prefer git mv to preserve history; fall back to a plain rename.
    import subprocess

    r = subprocess.run(
        ["git", "-C", str(ROOT), "mv", str(src), str(dest)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        src.rename(dest)
    return 0


# --------------------------------------------------------------------------- #
# record  (single-entry: the go-forward ship_* hook)
# --------------------------------------------------------------------------- #
def cmd_record(args) -> int:
    """Write ONE dated record from the rich completion body the ship skill
    drafted (--from-file), folding + removing the active/ prompt. The record is
    the sole completion ledger — regenerate complete/index.md afterwards."""
    src = Path(args.from_file)
    if not src.is_file():
        print(f"lifecycle record: --from-file not found: {src}", file=sys.stderr)
        return 1
    date = _parse_date(args.date)
    if date is None:
        print(f"lifecycle record: bad --date {args.date!r}", file=sys.stderr)
        return 1

    dest = complete_bucket(date) / f"{safe_name(args.slug)}.md"
    body = src.read_text(errors="replace").rstrip() + "\n"
    # fold the original active/ prompt (explicit --prompt, else guess from slug)
    prompt = None
    if args.prompt:
        p = ACTIVE_DIR / args.prompt
        if p.exists():
            prompt = p
    if prompt is None:
        guess = ACTIVE_DIR / f"{safe_name(args.slug).replace('-', '_')}.md"
        if guess.exists():
            prompt = guess
    if prompt is not None:
        body += "\n## Original prompt\n\n" + prompt.read_text(errors="replace")

    print(f"record: {dest.relative_to(ROOT)}"
          + (f"  (+folds active/{prompt.name})" if prompt else ""))
    if not args.apply:
        print("(dry run; pass --apply)")
        return 0
    import subprocess

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body)
    subprocess.run(["git", "-C", str(ROOT), "add", str(dest)],
                   capture_output=True, text=True)
    if prompt is not None:
        r = subprocess.run(["git", "-C", str(ROOT), "rm", "-q", str(prompt)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            prompt.unlink(missing_ok=True)
    return 0


# --------------------------------------------------------------------------- #
# index  (token-light navigation over the complete/ archive)
# --------------------------------------------------------------------------- #
INDEX_MD = COMPLETE_DIR / "index.md"
CURATED_START = "<!-- CURATED:START -->"
CURATED_END = "<!-- CURATED:END -->"
GEN_START = "<!-- GENERATED:START — edit records, not this block; regenerate with `lifecycle.py index --apply` -->"
GEN_END = "<!-- GENERATED:END -->"


def _record_hook(path: Path) -> str:
    """One-line hook for a record: the H2 parenthetical, else the summary snippet."""
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return ""
    first = text.splitlines()[0] if text else ""
    m = re.search(r"\((.*)\)\s*$", first)
    hook = m.group(1).strip() if m else ""
    # a bare date / trivial paren is no hook — fall back to the summary line
    if not hook or re.fullmatch(r"[\d\-/ ]+|MERGED|complete|done", hook, re.I):
        sm = re.search(r"^-\s*summary:\s*(.+)$", text, re.MULTILINE)
        if sm:
            hook = sm.group(1)
    hook = re.sub(r"\s+", " ", hook).strip(" |")
    return (hook[:110] + "…") if len(hook) > 111 else hook


def _all_records() -> "list[tuple[str, str, Path]]":
    """(bucket, slug, path) for every complete/ record, newest bucket first."""
    if not COMPLETE_DIR.exists():
        return []
    recs = []
    for f in COMPLETE_DIR.rglob("*.md"):
        if f.name in ("index.md", "AGENTS.md") or ARCHIVE_DIR in f.parents:
            continue
        bucket = "/".join(f.relative_to(COMPLETE_DIR).parts[:-1]) or "unknown"
        recs.append((bucket, f.stem, f))

    def _key(r):
        b = r[0]
        if b == "unknown":
            return (1, 0, 0, r[1])          # unknown bucket sorts last
        parts = b.split("/")
        y = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        return (0, -y, -m, r[1])            # dated: reverse-chronological, then slug

    recs.sort(key=_key)
    return recs


def _render_index(curated: str) -> str:
    recs = _all_records()
    from collections import OrderedDict
    by_bucket: "OrderedDict[str, list]" = OrderedDict()
    for bucket, slug, path in recs:
        by_bucket.setdefault(bucket, []).append((slug, path))
    lines = [
        "# complete/ — finished-work archive index",
        "",
        "Token-light navigation over the finished-work records (schema:",
        "[`AGENTS.md`](AGENTS.md)). **Generated** from the records by",
        "`scripts/lifecycle.py index` — read this, follow one or two links, and",
        "only then grep a dated bucket. Curators: edit the band between the CURATED",
        "markers; everything below GENERATED is rebuilt.",
        "",
        f"{len(recs)} records across {len(by_bucket)} buckets.",
        "",
        CURATED_START,
        curated.strip() or "## Highlights\n\n_(curate hard-won records here — survives regeneration.)_",
        CURATED_END,
        "",
        GEN_START,
        "",
    ]
    for bucket, items in by_bucket.items():
        lines.append(f"## {bucket}")
        lines.append("")
        for slug, path in sorted(items):
            hook = _record_hook(path)
            rel = path.relative_to(COMPLETE_DIR).as_posix()
            lines.append(f"- [{slug}]({rel})" + (f" — {hook}" if hook else ""))
        lines.append("")
    lines.append(GEN_END)
    return "\n".join(lines).rstrip() + "\n"


def _existing_curated() -> str:
    if not INDEX_MD.exists():
        return ""
    text = INDEX_MD.read_text(errors="replace")
    if CURATED_START in text and CURATED_END in text:
        return text.split(CURATED_START, 1)[1].split(CURATED_END, 1)[0].strip()
    return ""


def cmd_index(args) -> int:
    rendered = _render_index(_existing_curated())
    if args.check:
        current = INDEX_MD.read_text(errors="replace") if INDEX_MD.exists() else ""
        if current != rendered:
            print("lifecycle index: DRIFT — complete/index.md is stale; "
                  "run `lifecycle.py index --apply`", file=sys.stderr)
            return 1
        print("lifecycle index: OK")
        return 0
    if args.apply:
        INDEX_MD.write_text(rendered)
        print(f"wrote {INDEX_MD.relative_to(ROOT)} ({len(_all_records())} records)")
    else:
        print(rendered)
    return 0


# --------------------------------------------------------------------------- #
# check
# --------------------------------------------------------------------------- #
def cmd_check(args) -> int:
    problems: "list[str]" = []
    a_slugs = {safe_name(s) for s in ledger_slugs(ACTIVE_MD)}
    rec_by_slug: "dict[str, Path]" = {}
    for _, slug, path in _all_records():
        rec_by_slug.setdefault(safe_name(slug), path)

    for s in sorted(a_slugs & set(rec_by_slug)):
        problems.append(
            f"active.md slug has a complete/ record (finished but still "
            f"active?): {s} -> {rec_by_slug[s].relative_to(ROOT)}"
        )

    # a file should not exist in two state dirs at once
    if ACTIVE_DIR.exists() and COMPLETE_DIR.exists():
        active_names = {f.name for f in ACTIVE_DIR.glob("*.md")}
        for f in COMPLETE_DIR.rglob("*.md"):
            if ARCHIVE_DIR in f.parents:
                continue
            if f.name in active_names:
                problems.append(f"file in both active/ and complete/: {f.name}")

    if problems:
        print("lifecycle check: DRIFT")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("lifecycle check: OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PyAutoMind prompt-file lifecycle engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("move", help="advance active/<name> -> complete/YYYY/MM/")
    m.add_argument("name")
    m.add_argument("--date", help="completion date YYYY-MM-DD (else from the matching record)")
    m.add_argument("--apply", action="store_true")
    m.set_defaults(func=cmd_move)

    r = sub.add_parser("record", help="write one dated record from a completion body (ship_* hook)")
    r.add_argument("slug", help="the task slug for the shipped task")
    r.add_argument("--date", required=True, help="completion date YYYY-MM-DD")
    r.add_argument("--from-file", required=True, dest="from_file",
                   help="path to the rich completion body drafted by the ship skill")
    r.add_argument("--prompt", help="active/ prompt filename to fold + remove")
    r.add_argument("--apply", action="store_true")
    r.set_defaults(func=cmd_record)

    ix = sub.add_parser("index", help="generate complete/index.md (token-light archive navigation)")
    ix.add_argument("--apply", action="store_true", help="write complete/index.md")
    ix.add_argument("--check", action="store_true", help="fail if index.md is stale (CI)")
    ix.set_defaults(func=cmd_index)

    c = sub.add_parser("check", help="drift guard (non-zero exit on drift)")
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
