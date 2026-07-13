#!/usr/bin/env python3
"""PyAutoMind prompt-file lifecycle engine.

The Mind runs the prompt file through three states that mirror the task ledger:

    draft/<work-type>/<target>/<name>.md   intaken, not started   (backlog)
    active/<name>.md                        issued, in flight      (active.md)
    complete/<YYYY>/<MM>/<slug>.md          shipped                (complete.md)

Historically the file lifecycle stopped at `issued/` and never advanced, so a
completed task's prompt sat in `issued/` forever while only the *ledger* entry
moved `active.md -> complete.md`. This tool advances the FILE in lockstep and
guards the invariant.

Subcommands
-----------
  move <name> [--date YYYY-MM-DD]
        Advance one file active/<name>.md -> complete/<YYYY>/<MM>/<name>.md.
        The month is zero-padded so lexical order == numerical order. Date is
        taken from --date, else derived from the matching complete.md entry's
        `- completed:` line. Called by ship_library / ship_workspace.

  split-complete [--apply]
        One-time (PR-B): explode the monolithic complete.md into one rich
        record per finished task under complete/<YYYY>/<MM>/<slug>.md. Dry-run
        prints the manifest; --apply writes the files (complete.md left intact
        for a human to retire once the split is verified).

  migrate [--apply]
        One-time (PR-B): classify every legacy active/ (formerly issued/) file
        as still-active or complete, emitting a REVIEW MANIFEST. Filenames map
        only fuzzily to complete.md slugs, so this NEVER auto-moves on a fuzzy
        match — it proposes; a human confirms. --apply executes only the
        high-confidence (ledger-backed) rows.

  check
        Drift guard (mirrors repos_sync.py --check; non-zero exit on drift):
          * no task slug in BOTH active.md and complete.md
          * every complete/**/*.md has a complete.md entry (pre-retirement)
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
DRAFT_DIR = ROOT / "draft"
ACTIVE_MD = ROOT / "active.md"
COMPLETE_MD = ROOT / "complete.md"

DATE_RE = re.compile(r"-\s*completed:\s*(\d{4})-(\d{2})-(\d{2})")
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


def parse_complete_md() -> "dict[str, dict]":
    """Return {slug: {"date": (yyyy, mm) | None, "lines": [...]}} from complete.md."""
    entries: "dict[str, dict]" = {}
    if not COMPLETE_MD.exists():
        return entries
    slug = None
    buf: "list[str]" = []
    date = None
    for line in COMPLETE_MD.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            if slug is not None:
                entries[slug] = {"date": date, "lines": buf}
            slug = _slugify_h2(m.group(1))
            buf = [line]
            date = None
            continue
        if slug is not None:
            buf.append(line)
            if date is None:
                dm = DATE_RE.search(line)
                if dm:
                    date = (dm.group(1), dm.group(2))
    if slug is not None:
        entries[slug] = {"date": date, "lines": buf}
    return entries


def ledger_slugs(path: Path) -> "set[str]":
    """H2 task slugs recorded in a ledger file (active.md / complete.md)."""
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

    date = None
    if args.date:
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", args.date)
        if not m:
            print(f"lifecycle move: bad --date {args.date!r}", file=sys.stderr)
            return 1
        date = (m.group(1), m.group(2))
    else:
        entries = parse_complete_md()
        # active file name may differ from the complete.md slug; try exact then
        # fuzzy (name tokens subset of slug tokens).
        entry = entries.get(name)
        if entry is None:
            cand = [s for s in entries if name.replace("_", "-") == s]
            if cand:
                entry = entries[cand[0]]
        if entry is None or entry["date"] is None:
            print(
                f"lifecycle move: no completed-date for {name!r}; pass --date",
                file=sys.stderr,
            )
            return 1
        date = entry["date"]

    dest = complete_bucket(date) / src.name
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
# split-complete
# --------------------------------------------------------------------------- #
def cmd_split_complete(args) -> int:
    entries = parse_complete_md()
    if not entries:
        print("lifecycle split-complete: complete.md empty or absent", file=sys.stderr)
        return 1
    n_dated = sum(1 for e in entries.values() if e["date"])
    print(f"complete.md: {len(entries)} entries ({n_dated} dated, "
          f"{len(entries) - n_dated} -> complete/unknown/)")
    wrote = 0
    for slug, e in entries.items():
        dest = complete_bucket(e["date"]) / f"{safe_name(slug)}.md"
        body = "\n".join(e["lines"]).rstrip() + "\n"
        # attach the original prompt if we can find it in active/
        legacy = ACTIVE_DIR / f"{safe_name(slug).replace('-', '_')}.md"
        if legacy.exists():
            body += "\n## Original prompt\n\n" + legacy.read_text(errors="replace")
        rel = dest.relative_to(ROOT)
        if args.apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body)
            wrote += 1
        else:
            print(f"  {rel}")
    if args.apply:
        print(f"wrote {wrote} records under complete/. "
              f"complete.md left intact — retire it by hand once verified.")
    else:
        print("(dry run; pass --apply)")
    return 0


# --------------------------------------------------------------------------- #
# record  (single-entry: the go-forward ship_* hook)
# --------------------------------------------------------------------------- #
def cmd_record(args) -> int:
    """Write ONE dated record from its complete.md entry, keeping complete.md and
    the record paired 1:1 by slug. Called by ship_library/ship_workspace after the
    rich entry is appended to complete.md, so a new completion lands as a dated
    record (not just a complete.md append + a thin active/ prompt)."""
    entries = parse_complete_md()
    slug = args.slug
    entry = entries.get(slug)
    if entry is None:  # tolerate kebab/space variants
        want = safe_name(slug)
        cand = [s for s in entries if safe_name(s) == want]
        if cand:
            slug, entry = cand[0], entries[cand[0]]
    if entry is None:
        print(f"lifecycle record: no complete.md entry for {args.slug!r} "
              f"(append it first)", file=sys.stderr)
        return 1
    date = entry["date"]
    if args.date:
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", args.date)
        if not m:
            print(f"lifecycle record: bad --date {args.date!r}", file=sys.stderr)
            return 1
        date = (m.group(1), m.group(2))

    dest = complete_bucket(date) / f"{safe_name(slug)}.md"
    body = "\n".join(entry["lines"]).rstrip() + "\n"
    # fold the original active/ prompt (explicit --prompt, else guess from slug)
    prompt = None
    if args.prompt:
        p = ACTIVE_DIR / args.prompt
        if p.exists():
            prompt = p
    if prompt is None:
        guess = ACTIVE_DIR / f"{safe_name(slug).replace('-', '_')}.md"
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
# migrate  (legacy issued/ -> active/ was a wholesale rename in PR-A; here we
#           classify those files into still-active vs complete)
# --------------------------------------------------------------------------- #
def cmd_migrate(args) -> int:
    active_files = sorted(ACTIVE_DIR.glob("*.md")) if ACTIVE_DIR.exists() else []
    if not active_files:
        print("lifecycle migrate: active/ empty or absent", file=sys.stderr)
        return 1
    a_slugs = ledger_slugs(ACTIVE_MD)
    c_entries = parse_complete_md()
    c_slugs = set(c_entries)

    def norm(s: str) -> str:
        return s.replace("_", "-").lower()

    a_norm = {norm(s) for s in a_slugs}
    c_norm = {norm(s): s for s in c_slugs}

    keep, done, unsure = [], [], []
    for f in active_files:
        stem = norm(f.stem)
        if stem in a_norm:
            keep.append(f.name)
        elif stem in c_norm:
            done.append((f.name, c_entries[c_norm[stem]]["date"]))
        else:
            unsure.append(f.name)

    print(f"active/ files: {len(active_files)}")
    print(f"  -> stay active (ledger-backed): {len(keep)}")
    print(f"  -> complete (ledger-backed):    {len(done)}")
    print(f"  -> UNSURE (needs human review): {len(unsure)}")
    print("\n# Ledger-backed COMPLETE (high confidence):")
    for name, date in done:
        bucket = complete_bucket(date).relative_to(ROOT)
        print(f"  active/{name} -> {bucket}/{name}")
    print("\n# UNSURE — filename matched no active.md/complete.md slug:")
    for name in unsure:
        print(f"  active/{name}  ??  (review: read the file, cross-ref git log)")
    if not args.apply:
        print("\n(dry run; --apply executes ONLY the ledger-backed COMPLETE rows)")
        return 0
    import subprocess

    for name, date in done:
        src = ACTIVE_DIR / name
        dest = complete_bucket(date) / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "-C", str(ROOT), "mv", str(src), str(dest)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            src.rename(dest)
    print(f"\nmoved {len(done)} ledger-backed files; {len(unsure)} UNSURE left in "
          f"active/ for review.")
    return 0


# --------------------------------------------------------------------------- #
# index  (Phase 2: token-light navigation over the complete/ archive)
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
        if f.name in ("index.md", "AGENTS.md"):
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
    a_slugs = ledger_slugs(ACTIVE_MD)
    c_entries = parse_complete_md()
    c_slugs = set(c_entries)

    both = a_slugs & c_slugs
    for s in sorted(both):
        problems.append(f"slug in BOTH active.md and complete.md: {s}")

    if COMPLETE_DIR.exists():
        for f in COMPLETE_DIR.rglob("*.md"):
            if f.name in ("index.md", "AGENTS.md"):
                continue
            slug = f.stem
            if slug not in {safe_name(s) for s in c_slugs}:
                problems.append(
                    f"complete/ record has no complete.md entry: "
                    f"{f.relative_to(ROOT)}"
                )

    # a file should not exist in two state dirs at once
    if ACTIVE_DIR.exists() and COMPLETE_DIR.exists():
        active_names = {f.name for f in ACTIVE_DIR.glob("*.md")}
        for f in COMPLETE_DIR.rglob("*.md"):
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
    m.add_argument("--date", help="completion date YYYY-MM-DD (else from complete.md)")
    m.add_argument("--apply", action="store_true")
    m.set_defaults(func=cmd_move)

    s = sub.add_parser("split-complete", help="explode complete.md into per-task records")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(func=cmd_split_complete)

    mg = sub.add_parser("migrate", help="classify legacy active/ files into active vs complete")
    mg.add_argument("--apply", action="store_true")
    mg.set_defaults(func=cmd_migrate)

    r = sub.add_parser("record", help="write one dated record from its complete.md entry (ship_* hook)")
    r.add_argument("slug", help="the complete.md heading slug for the shipped task")
    r.add_argument("--date", help="completion date YYYY-MM-DD (else from complete.md)")
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
