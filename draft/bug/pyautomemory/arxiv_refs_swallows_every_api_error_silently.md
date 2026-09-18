# `arxiv_refs.py` swallows every API error, so an arXiv outage resolves nothing and still reports green

Type: bug
Target: pyautomemory
Repos:
- PyAutoMemory
Themes:
- ci
- robustness
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: a test driving `resolve_title()` with an injected `query` raising `HTTPError(429)` asserts the run is *reported* as an API failure rather than as "no unique match" — it fails on current source (the bare `except Exception` returns `None`, indistinguishable from a genuine non-match) and passes after the fix. The backfill's stats gain a distinct counter, and a run whose lookups all failed on transport exits non-zero rather than logging "N ref-less, 0 resolved".
Review-minutes: 4
Filed: 2026-09-18

Found while diagnosing the PyAutoMind digest outage
(`complete/2026/09/arxiv-digest-api-retry.md`, PyAutoMind#410). This is
the *opposite* failure, in the sibling script, and it is why the two jobs
behaved so differently through the same arXiv outage.

## The finding

`scripts/arxiv_refs.py:243` wraps every lookup:

```python
try:
    raw = query({"search_query": f'ti:"{phrase}"', ...})
except Exception:
    return None
```

A `None` from `resolve_title()` means "no unique title match" everywhere
downstream — `backfill()` counts it as `unmatched` and logs
`· no unique match  <title>`. So an arXiv 429, a 406, a DNS failure and a
genuine non-match are **all the same observation**.

The consequence showed up on 2026-09-14..18, when arXiv answered the shared
GitHub Actions egress with 429s and 406s. `arxiv_refs.yml` ran green every one
of those nights — 1m30s to 1m53s, exit 0, cheerful log lines — while
PyAutoMind's digest died loudly on the same API from the same runner pool. The
green was not evidence of health; it was the `except` clause.

Worse, with `--mark-unresolved` a transport-failed line would be **NOTE-marked**
so later runs skip it — a permanent decision made from a transient error. That
flag is human-driven and was not used in the outage window, so nothing appears
to have been mis-marked; confirm that from git history before closing.

## What to do

1. Narrow the `except`. Distinguish a *transport* failure (`HTTPError`,
   `URLError`, timeout) from an empty/ambiguous result set. Let the caller see
   the difference — an exception type, a sentinel, or a `(ref, status)` pair;
   `None` must keep meaning "arXiv answered, and no unique match".
2. Retry transport failures. PyAutoMind#410 adds a back-off ladder honouring
   `Retry-After` for 429/406/5xx in `arxiv_fetch.py:_get()` — reuse that shape
   rather than inventing a second one, and note that arXiv returns **406** as
   edge mitigation, not as a content-negotiation verdict.
3. Report them. `backfill()`'s stats gain an `api_failed` counter; the summary
   line and the workflow step summary say so; a run where transport failure was
   the dominant outcome exits non-zero so the job goes red instead of quietly
   resolving nothing.
4. Make `--mark-unresolved` refuse to mark a line whose lookup failed on
   transport. A NOTE-mark is permanent and must only ever follow an actual
   answer from arXiv.

## Not in scope

The PyAutoMind side (`arxiv_fetch.py`, both digests) — that is #410. This prompt
is only the PyAutoMemory half.
