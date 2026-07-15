#!/usr/bin/env python3
"""Fetch newly *announced* strong-lensing papers from the arXiv API into arxiv_papers.json.

Stateless announcement-band window. A paper is not searchable when it is
submitted — it becomes searchable when arXiv *announces* it, one to three days
later. So the window is anchored to arXiv's announcement schedule, not to a
rolling "last N hours" of submission time:

  announcements   20:00 ET, Sun-Thu
  deadlines       14:00 ET, Mon-Fri

Each announcement covers submissions between the previous deadline and its own:

  submitted Mon 14:00 -> Tue 14:00 ET   announced Tue 20:00 ET
  submitted Tue 14:00 -> Wed 14:00 ET   announced Wed 20:00 ET
  submitted Wed 14:00 -> Thu 14:00 ET   announced Thu 20:00 ET
  submitted Thu 14:00 -> Fri 14:00 ET   announced Sun 20:00 ET
  submitted Fri 14:00 -> Mon 14:00 ET   announced Mon 20:00 ET   (3-day band)

The 02:00 UTC cron lands at 21:00-22:00 ET the *previous* day, just after that
day's 20:00 ET announcement, so the Mon-Fri runs take the bands Thu->Fri,
Fri->Mon, Mon->Tue, Tue->Wed, Wed->Thu. Their union is exactly one week with no
overlap: disjoint and gapless, with no cross-run state. The band is stable from
one 20:00 ET announcement to the next, so it absorbs ~22 h of cron slip (GitHub
cron only ever fires late).

The filter is still on <published> (v1), not <updated>, so v2 revisions and old
cross-lists do not resurface.

History: until 2026-07-15 this used a rolling 24 h window (72 h on Mondays)
against submission time. That silently and permanently dropped every paper whose
announcement lag pushed its v1 timestamp outside the window — e.g. 2607.12129
and 2607.12209, submitted Mon 2026-07-13 evening, announced Wed 00:00 UTC, and
by then already too old for Wednesday's 24 h look-back (PyAutoMind#79). Setting
LOOKBACK_HOURS restores the old rolling window for manual test-fires and
backfills.
"""
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"

# arXiv's schedule is defined in US Eastern wall-clock, so the UTC offset it
# implies moves with US DST (14:00 ET = 18:00 UTC in EDT, 19:00 UTC in EST).
# Derive it via zoneinfo rather than hard-coding either offset.
ET_ZONE = ZoneInfo("America/New_York")
ANNOUNCE_HOUR = 20  # 20:00 ET
DEADLINE_HOUR = 14  # 14:00 ET
ANNOUNCE_DAYS = {0, 1, 2, 3, 6}  # Mon-Thu + Sun (weekday() codes)
DEADLINE_DAYS = {0, 1, 2, 3, 4}  # Mon-Fri

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


def _walk_back(limit_et: dt.datetime, hour: int, days: set) -> dt.datetime:
    """The most recent `hour`:00 ET on a day in `days`, at or before `limit_et`."""
    day = limit_et.date()
    for _ in range(8):  # a week is always enough; bounded so a bug cannot hang CI
        moment = dt.datetime(day.year, day.month, day.day, hour, tzinfo=ET_ZONE)
        if moment <= limit_et and day.weekday() in days:
            return moment
        day -= dt.timedelta(days=1)
    raise RuntimeError(f"no {hour}:00 ET slot within a week of {limit_et}")


def announcement_band(now: dt.datetime) -> tuple:
    """The submission band whose papers are newly searchable at `now`.

    Returns (band_start, band_end) in UTC, half-open as
    `band_start < published <= band_end`. Monday's band reaches back to Friday,
    covering the weekend in one 3-day sweep.
    """
    now_et = now.astimezone(ET_ZONE)
    announced = _walk_back(now_et, ANNOUNCE_HOUR, ANNOUNCE_DAYS)
    band_end = _walk_back(announced, DEADLINE_HOUR, DEADLINE_DAYS)
    band_start = _walk_back(band_end - dt.timedelta(seconds=1), DEADLINE_HOUR, DEADLINE_DAYS)
    return (
        band_start.astimezone(dt.timezone.utc),
        band_end.astimezone(dt.timezone.utc),
    )


def fetch(query: str, max_results: int) -> bytes:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": max_results,
        }
    )
    url = f"https://export.arxiv.org/api/query?{params}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "PyAutoLabs-papers-digest/1.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def parse(raw: bytes, band_start: dt.datetime, band_end: dt.datetime) -> list:
    root = ET.fromstring(raw)
    papers = []
    seen = set()
    for entry in root.findall(f"{ATOM}entry"):
        published = entry.findtext(f"{ATOM}published")
        if not published:
            continue
        ts = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
        if not (band_start < ts <= band_end):
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
    return papers


def _selftest() -> int:
    """Band maths, no network. Covers both DST regimes and every run weekday."""
    utc = dt.timezone.utc
    failures = 0

    def check(label, ok):
        nonlocal failures
        failures += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {label}", file=sys.stderr)

    # Run times are the nominal 02:00 UTC cron, Mon-Fri.
    # EDT (UTC-4): 14:00 ET = 18:00 UTC. Week of 2026-07-13.
    # EST (UTC-5): 14:00 ET = 19:00 UTC. Week of 2026-01-12.
    cases = [
        # Mon run -> Sun 20:00 ET announcement -> Thu 14:00 -> Fri 14:00 ET band
        ("2026-07-13T02:00:00+00:00", "2026-07-09T18:00:00+00:00", "2026-07-10T18:00:00+00:00"),
        # Tue run -> Mon 20:00 ET announcement -> the 3-day Fri -> Mon weekend band
        ("2026-07-14T02:00:00+00:00", "2026-07-10T18:00:00+00:00", "2026-07-13T18:00:00+00:00"),
        # Wed run -> Tue 20:00 ET announcement -> Mon 14:00 -> Tue 14:00 ET band
        ("2026-07-15T02:00:00+00:00", "2026-07-13T18:00:00+00:00", "2026-07-14T18:00:00+00:00"),
        ("2026-07-16T02:00:00+00:00", "2026-07-14T18:00:00+00:00", "2026-07-15T18:00:00+00:00"),
        ("2026-07-17T02:00:00+00:00", "2026-07-15T18:00:00+00:00", "2026-07-16T18:00:00+00:00"),
        # EST: same shape, one hour later in UTC.
        ("2026-01-13T02:00:00+00:00", "2026-01-09T19:00:00+00:00", "2026-01-12T19:00:00+00:00"),
        ("2026-01-14T02:00:00+00:00", "2026-01-12T19:00:00+00:00", "2026-01-13T19:00:00+00:00"),
    ]
    for run, want_start, want_end in cases:
        start, end = announcement_band(dt.datetime.fromisoformat(run))
        ok = (start.isoformat(), end.isoformat()) == (want_start, want_end)
        check(
            f"run {run} -> {start.isoformat()} .. {end.isoformat()}"
            + ("" if ok else f"\n         wanted {want_start} .. {want_end}"),
            ok,
        )

    # Regression (PyAutoMind#79): the two papers the old rolling window dropped.
    # Submitted Mon 2026-07-13 20:24 / 23:18 UTC, announced Wed 00:00 UTC; the
    # Wed 02:00 UTC run must include them.
    start, end = announcement_band(dt.datetime(2026, 7, 15, 2, 0, tzinfo=utc))
    for name, ts in [
        ("2607.12129", dt.datetime(2026, 7, 13, 20, 24, 11, tzinfo=utc)),
        ("2607.12209", dt.datetime(2026, 7, 13, 23, 18, 46, tzinfo=utc)),
    ]:
        check(f"{name} falls in the Wed band", start < ts <= end)

    # Cron only ever fires late: a run slipped 3 h must compute the same band.
    for nominal in ("2026-07-15T02:00:00+00:00", "2026-07-14T02:00:00+00:00"):
        base = dt.datetime.fromisoformat(nominal)
        check(
            f"3 h slip stable at {nominal}",
            announcement_band(base) == announcement_band(base + dt.timedelta(hours=3)),
        )

    # Consecutive runs must be disjoint and gapless: each band ends exactly where
    # the next begins, across Mon-Fri including the weekend seam.
    runs = [c[0] for c in cases[:5]]
    for earlier, later in zip(runs, runs[1:]):
        prev_end = announcement_band(dt.datetime.fromisoformat(earlier))[1]
        next_start = announcement_band(dt.datetime.fromisoformat(later))[0]
        check(f"seam {earlier[:10]} -> {later[:10]}", prev_end == next_start)

    print(
        f"selftest: {'PASS' if not failures else f'{failures} FAILURE(S)'}",
        file=sys.stderr,
    )
    return 1 if failures else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()

    now = dt.datetime.now(dt.timezone.utc)
    # An explicit LOOKBACK_HOURS restores the legacy rolling window, for manual
    # test-fires and for backfilling papers the old submission-anchored window
    # dropped. Unset (the scheduled path) = the announcement band.
    override = os.environ.get("LOOKBACK_HOURS", "").strip()
    if override:
        mode = "lookback"
        band_start, band_end = now - dt.timedelta(hours=float(override)), now
    else:
        mode = "announcement-band"
        band_start, band_end = announcement_band(now)

    # The workflow computes the UK-local date (Europe/London) and passes it in;
    # fall back to the UTC date if unset (e.g. local runs).
    uk_date = os.environ.get("UK_DATE") or now.strftime("%Y-%m-%d")

    papers = parse(fetch(QUERY, max_results=200), band_start, band_end)

    out = {
        "uk_date": uk_date,
        "mode": mode,
        # `since`/`until` keep their names so the downstream Claude and Slack
        # steps read the window unchanged.
        "since": band_start.isoformat(),
        "until": band_end.isoformat(),
        "count": len(papers),
        "papers": papers,
    }
    with open("arxiv_papers.json", "w") as f:
        json.dump(out, f, indent=2)

    print(
        f"mode={mode} band={band_start.isoformat()}..{band_end.isoformat()} "
        f"count={len(papers)}",
        file=sys.stderr,
    )
    for p in papers:
        print(
            f"  [{p['primary_category']}] {p['published'][:10]}  {p['title'][:70]}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
