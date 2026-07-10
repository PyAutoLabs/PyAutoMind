#!/usr/bin/env python3
"""Fetch new strong-lensing papers from the arXiv API into arxiv_papers.json.

Stateless daily window: keep papers whose *original* submission timestamp
(<published>, i.e. v1 — not <updated>, so v2 revisions and old cross-lists do
not resurface) falls within LOOKBACK_HOURS of now. The caller sets a wider
window on Mondays to sweep the weekend. Consecutive daily runs then cover
disjoint day-bands (gapless; cron jitter yields at worst a small overlap =
a rare duplicate, never a gap). No cross-run state, mirroring the commit
digest's jitter-tolerant philosophy.
"""
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"

# Recall-first query: the arXiv step casts a wide net over strong-lensing
# vocabulary (many strong-lensing papers never use the literal phrase "strong
# lensing" — e.g. a lens-modelling / lensed-quasar paper), and the Claude step
# downstream drops the handful of keyword false-positives. Deliberately omits
# the broad catch-alls "gravitational lensing" / "weak lensing" / "microlensing"
# so the net stays strong-lensing-shaped. `cat:` also matches cross-lists, so a
# strong-lensing paper whose primary category is elsewhere (e.g. astro-ph.HE) is
# still caught. Validated 2026-07-10: catches the Li+Collett WFI2033 lensed-quasar
# paper that the narrow phrase-only query missed; ~1.5 papers/day, ~2 off-topic
# per fortnight for Claude to drop.
_ABS = [
    "strong lensing", "strongly lensed", "gravitationally lensed",
    "gravitational lens", "lensed quasar", "lensed galaxy", "lensed source",
    "lensed images", "lensed arc", "Einstein ring", "Einstein radius",
    "lens modelling", "lens modeling", "multiply imaged", "quadruply imaged",
    "doubly imaged", "double source plane",
]
_TI = ["lens modelling", "lens modeling", "lensed quasar", "Einstein ring"]
QUERY = (
    "(cat:astro-ph.CO OR cat:astro-ph.GA) AND ("
    + " OR ".join([f'abs:"{t}"' for t in _ABS] + [f'ti:"{t}"' for t in _TI])
    + ")"
)

lookback_hours = float(os.environ.get("LOOKBACK_HOURS", "24"))
now = dt.datetime.now(dt.timezone.utc)
since = now - dt.timedelta(hours=lookback_hours)
# The workflow computes the UK-local date (Europe/London) and passes it in;
# fall back to the UTC date if unset (e.g. local runs).
uk_date = os.environ.get("UK_DATE") or now.strftime("%Y-%m-%d")

params = urllib.parse.urlencode(
    {
        "search_query": QUERY,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": 100,
    }
)
url = f"https://export.arxiv.org/api/query?{params}"

req = urllib.request.Request(url, headers={"User-Agent": "PyAutoLabs-papers-digest/1.0"})
with urllib.request.urlopen(req, timeout=60) as resp:
    raw = resp.read()

root = ET.fromstring(raw)
papers = []
seen = set()
for entry in root.findall(f"{ATOM}entry"):
    published = entry.findtext(f"{ATOM}published")
    if not published:
        continue
    ts = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
    if ts < since:
        continue
    arxiv_id = (entry.findtext(f"{ATOM}id") or "").strip()
    if arxiv_id in seen:
        continue
    seen.add(arxiv_id)
    authors = [
        a.findtext(f"{ATOM}name")
        for a in entry.findall(f"{ATOM}author")
        if a.findtext(f"{ATOM}name")
    ]
    prim = entry.find(f"{ARXIV}primary_category")
    papers.append(
        {
            "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
            "authors": authors,
            "abstract": " ".join((entry.findtext(f"{ATOM}summary") or "").split()),
            "url": arxiv_id.replace("http://", "https://"),
            "primary_category": prim.get("term") if prim is not None else None,
            "published": published,
        }
    )

out = {
    "uk_date": uk_date,
    "since": since.isoformat(),
    "until": now.isoformat(),
    "lookback_hours": lookback_hours,
    "count": len(papers),
    "papers": papers,
}
with open("arxiv_papers.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"since={since.isoformat()} count={len(papers)}", file=sys.stderr)
for p in papers:
    print(f"  [{p['primary_category']}] {p['published'][:10]}  {p['title'][:70]}", file=sys.stderr)
