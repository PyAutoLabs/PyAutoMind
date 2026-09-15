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

The second recorded miss, 2607.19459 on 2026-07-21, was a *recall* failure, not
a window one: its band and category were both correct, but its abstract says
"strong gravitational lenses" and "gravitational lensing simulations" and never
any of the phrases then in the query, so `"strong gravitational lensing"` was
added to it (PyAutoMind#92). The two failure modes look identical from the
outside — a paper that never appears — so when one is reported, check the band
and `cat:` clause before assuming either.
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"

USER_AGENT = "PyAutoLabs-papers-digest/1.0"

# --- talking to arXiv without getting throttled -------------------------------
#
# arXiv rate-limits the public API and answers HTTP 429 when it decides a client
# is going too fast. That is a TRANSIENT condition and it must never cost a
# morning: on 2026-09-14 both digests died on an unretried 429 (the lensing one
# in --livecheck, the interests one on its first page), so #papers was silent
# and neither Memory list moved — the failure this pacing and retry exist to
# stop.
#
# Two halves, and both are needed:
#   * PACING — arXiv asks for no more than one request every 3 s. The lensing
#     digest makes two requests a day and was never the problem; the interests
#     digest pages a whole day of astro-ph (up to MAX_PAGES back-to-back
#     requests) and is exactly the burst arXiv throttles. _pace() holds the
#     floor process-wide, so every caller of fetch() inherits it.
#   * RETRY — a 429 (or a 5xx, or a dropped connection) is retried with
#     exponential backoff, honouring `Retry-After` when arXiv sends one.
#     Bounded: worst case ~2 min of sleeping before giving up, well inside the
#     band's ~22 h of stability, so a retried run still takes the right papers.
#
# A 4xx that is NOT 429 is a bug in the query, not weather — it raises at once.
MIN_REQUEST_INTERVAL = 3.0   # seconds between requests (arXiv's stated rate)
MAX_ATTEMPTS = 5
BACKOFF_BASE = 4.0           # 4, 8, 16, 32 s between attempts
BACKOFF_CAP = 60.0
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})

_last_request_at = 0.0


def _pace() -> None:
    """Block until MIN_REQUEST_INTERVAL has passed since the last request."""
    global _last_request_at
    wait = MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()


def _retry_after(err: urllib.error.HTTPError, fallback: float) -> float:
    """Seconds to wait, from the server's `Retry-After` header when it sends a
    sane one (delta-seconds only; a HTTP-date is rare here and not worth
    parsing), else `fallback`. Capped so a hostile header cannot hang the run.
    """
    raw = (err.headers.get("Retry-After") or "").strip() if err.headers else ""
    try:
        return min(max(float(raw), 0.0), BACKOFF_CAP)
    except ValueError:
        return fallback


def get(url: str, *, timeout: int = 60) -> bytes:
    """GET `url`, paced and retried. The one door to the arXiv API.

    Raises the last error once MAX_ATTEMPTS are spent — a caller that can
    tolerate the loss (the recall livecheck) catches it; one that cannot (the
    fetch itself) lets it fail the run.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, MAX_ATTEMPTS + 1):
        _pace()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code not in RETRY_STATUSES or attempt == MAX_ATTEMPTS:
                raise
            backoff = min(BACKOFF_BASE * 2 ** (attempt - 1), BACKOFF_CAP)
            delay = _retry_after(err, backoff)
            reason = f"HTTP {err.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
            if attempt == MAX_ATTEMPTS:
                raise
            delay = min(BACKOFF_BASE * 2 ** (attempt - 1), BACKOFF_CAP)
            reason = str(err)
        print(
            f"  arXiv {reason} — attempt {attempt}/{MAX_ATTEMPTS}, "
            f"retrying in {delay:.0f}s",
            file=sys.stderr,
        )
        time.sleep(delay)
    raise RuntimeError("unreachable: the loop either returns or raises")

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
# the *bare* catch-alls "gravitational lensing" / "weak lensing" /
# "microlensing" so the net stays strong-lensing-shaped; the qualified
# "strong gravitational lensing" is kept, since the qualifier does that job
# itself. `cat:` also matches cross-lists, so a strong-lensing paper whose
# primary category is elsewhere (e.g. astro-ph.IM) is still caught. Validated
# 2026-07-10: catches the Li+Collett WFI2033 lensed-quasar paper that the narrow
# phrase-only query missed; ~1.5 papers/day, ~2 off-topic per fortnight for
# Claude to drop.
#
# Note that arXiv stems most of these singular/plural pairs interchangeably
# ("lensed galaxy"/"galaxies", "Einstein ring"/"rings", "lensed arc"/"arcs" each
# return the same papers) — but "gravitational lens" does *not* match
# "gravitational lenses", so do not assume a singular term covers its plural
# when adding to this list; measure it.
_ABS = [
    "strong lensing", "strong gravitational lensing", "strongly lensed",
    "gravitationally lensed", "gravitational lens", "lensed quasar",
    "lensed galaxy", "lensed source", "lensed images", "lensed arc",
    "Einstein ring", "Einstein radius", "lens modelling", "lens modeling",
    "multiply imaged", "quadruply imaged", "doubly imaged",
    "double source plane",
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


def fetch(query: str, max_results: int, start: int = 0) -> bytes:
    """One page of the API. `start` pages a query too broad for one request —
    the strong-lensing digest never needs it (a band is ~1.5 papers), the
    interests digest beside it always does (a band is a whole day of astro-ph).
    """
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": start,
            "max_results": max_results,
        }
    )
    return get(f"https://export.arxiv.org/api/query?{params}")


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

    # Regression (PyAutoMind#92): the term that recovers the 2607.19459 recall
    # miss must stay in the query. This is all that can be asserted offline —
    # arXiv matched that paper by stemming ("lensing" <-> "lenses"); its
    # abstract literally contains only "strong gravitational lenses", so a
    # substring test against the abstract text would wrongly fail. `--livecheck`
    # asserts the real behaviour against the API.
    check('_ABS keeps "strong gravitational lensing"', "strong gravitational lensing" in _ABS)

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


KNOWN_MATCHES = {
    # Papers a past version of QUERY missed, kept as live recall regressions.
    "2607.12129": "lensed-arc candidate in MACS J0308.9+2645 (PyAutoMind#79)",
    "2607.12209": "NGC 6505 Einstein ring, OSN recovery (PyAutoMind#79)",
    "2607.19459": "diffusion + RIM pixel-space lens posteriors (PyAutoMind#92)",
}


def _livecheck() -> int:
    """Assert QUERY still matches every paper in KNOWN_MATCHES. Needs network.

    `id_list` intersects with `search_query`, so this asks arXiv directly
    "would today's query return this paper?" — independent of how long ago it
    was published, unlike a look-back over recent results. Runs in the workflow
    just before the fetch, which needs the same API anyway, so it adds no new
    failure mode beyond a genuine recall regression — and that claim is load
    bearing, because this guard runs BEFORE the fetch and a non-zero exit here
    costs the whole digest. So an API that will not answer (429 after every
    retry, a 5xx, a dropped connection) is reported and PASSED: only a query
    that answers and no longer returns a known paper is a recall regression.
    The fetch below hits the same API moments later and fails loudly there if
    arXiv is genuinely down.
    """
    params = urllib.parse.urlencode(
        {
            "search_query": QUERY,
            "id_list": ",".join(KNOWN_MATCHES),
            "max_results": len(KNOWN_MATCHES) * 2,
        }
    )
    try:
        raw = get(f"https://export.arxiv.org/api/query?{params}")
    except urllib.error.HTTPError as err:
        if err.code not in RETRY_STATUSES:
            # A 400 here is the query itself being rejected — a real regression,
            # and the fetch below would hit it too. Fail.
            print(f"  [FAIL] arXiv rejected the query (HTTP {err.code})", file=sys.stderr)
            print("livecheck: QUERY REJECTED", file=sys.stderr)
            return 1
        print(
            f"  [skip] arXiv throttled or down (HTTP {err.code} after "
            f"{MAX_ATTEMPTS} attempts) — recall not checked",
            file=sys.stderr,
        )
        print("livecheck: SKIPPED (transport)", file=sys.stderr)
        return 0
    except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
        print(
            f"  [skip] arXiv unreachable ({err}) — recall not checked",
            file=sys.stderr,
        )
        print("livecheck: SKIPPED (transport)", file=sys.stderr)
        return 0
    root = ET.fromstring(raw)
    returned = {
        (entry.findtext(f"{ATOM}id") or "").rsplit("/", 1)[-1].split("v")[0]
        for entry in root.findall(f"{ATOM}entry")
    }
    missing = [i for i in KNOWN_MATCHES if i not in returned]
    for arxiv_id, why in KNOWN_MATCHES.items():
        hit = arxiv_id not in missing
        print(f"  [{'ok' if hit else 'FAIL'}] {arxiv_id} — {why}", file=sys.stderr)
    print(
        f"livecheck: {'PASS' if not missing else f'{len(missing)} NO LONGER MATCHED'}",
        file=sys.stderr,
    )
    return 1 if missing else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    if "--livecheck" in sys.argv:
        return _livecheck()

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
