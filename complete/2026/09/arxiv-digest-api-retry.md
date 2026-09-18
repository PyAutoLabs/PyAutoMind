### The fix already existed — it had simply never been opened as a PR

Slack `#papers` went silent for four of five nights (09-14, 09-15, 09-17,
09-18). The digest died in its `--livecheck` step before fetching anything:
HTTP 429 on 09-15, HTTP 406 on 09-17 and 09-18. `arxiv_interests.yml` failed
on the same nights. `PyAutoMemory/arxiv-inbox.md` froze at
`last digest: 2026-09-16`, which is how the loss was visible at all.

Two corrections to the report, both load-bearing:

- **The locus was PyAutoMind, not PyAutoMemory.** PyAutoMemory only receives
  the filing; its own `arxiv_refs.yml` was green every night.
- **It was not a new bug.** The repair was written on 2026-09-16 on
  `claude/papers-slack-pyautomemory-39wrt1` (commit `9f5fbab6`), verified by a
  `workflow_dispatch` on that branch — and never opened as a PR. That is the
  whole reason `main` stayed dark. This branch was cut from that one so the
  commit kept its history and its authorship.

It would also not have been enough: its `RETRY_STATUSES` omitted `406`, so
`_get()` re-raised unretried and the **fetch** step died even though
`_livecheck()` survived. Proven, not assumed — the two new witnesses fail on
that branch's source and pass after.

### What shipped

`406` joins the retry ladder; the comment calling every non-429 4xx "a bad
request" is corrected. The User-Agent gains a contact URL and the request an
explicit `Accept: application/atom+xml`, both commented in-source as courtesy
and explicitly **not** the fix. `arxiv_interests.py` coverage was proven by
execution — a harness patched only `arxiv_fetch`'s opener and watched the
interests path climb the ladder through 3x406.

### The finding that outlived the fix

The 406 is **not transient and not egress-specific**. It never reaches arXiv:
the response carries `via: 1.1 varnish` with no `1.1 google` — Fastly's edge
refuses it. Ten header combinations across `urllib.request` and raw
`http.client` all 406 on **uncached** URLs, while `curl` and `requests`/urllib3
get 200. Leading hypothesis: bot mitigation on the stdlib client fingerprint.

So this change converts an instant failure into a slow one and may not be
sufficient on its own. Follow-up filed:
`draft/bug/pyautomind/arxiv_edge_refuses_the_stdlib_urllib_client.md`.

**A measurement trap worth not repeating:** an early probe in this session
concluded "headers are irrelevant, all four combinations return 200" and was
reading its own Fastly **cache hits** — every probe reused one URL. Cache-bust
every attempt and record `x-cache:`.

### Collateral: the privacy check was red on main, twice

`tests/test_ledger_merge.py::test_the_real_registries_round_trip_through_split`
was failing on `main` before this task's stack existed (verified at `0b16fb9f`),
failing the `privacy` check on **every** PyAutoMind PR. Cause: a doubled blank
line where `ledger_merge.join_entries` emits one — in `planned.md` (`67387c0f`)
and then, as another session's close-out landed mid-task, in `epics.md`
(`9f0aef44`). All five `ENTRY_MERGED_FILES` now round-trip.

`registry_toc.render` is idempotent on the repaired file and repairs the broken
one, so the defect comes from hand edits, not the tooling — no generator change
was warranted. Note also that a `pull_request` re-run reuses its original merge
commit, so fixing `main` does nothing until the branch itself moves.

### Open

- **Backfill of the four lost nights is NOT done.** Held for human approval
  because it posts to the shared Slack channel. Recovery is a
  `workflow_dispatch` with `lookback_hours=168` — the value the workflow's own
  error text prescribes, because the lookback is submission-anchored. The inbox
  `append` dedupes; **Slack does not**, so a 168 h window re-posts the 09-16
  batch.
- `draft/bug/pyautomemory/arxiv_refs_swallows_every_api_error_silently.md` —
  the sibling defect: a bare `except Exception: return None` is why that job ran
  green through the same outage while resolving nothing.

## Original prompt

# The arXiv digest fix was written, never merged — and it does not cover the 406 that is failing now

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- ci
- robustness
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `tests/test_arxiv_fetch_retry.py` gains a case driving `_get()` with an injected opener raising `HTTPError(406)` three times then returning a body. On the abandoned branch's source it fails — 406 is absent from `RETRY_STATUSES`, so the first error re-raises — and passes after the fix. A second case asserts `fetch()` (the path `arxiv_interests.py` also uses) survives the same 406 sequence, which is the step that would still have killed the run on 09-17/18.
Review-minutes: 6
Unattended: ready
Filed: 2026-09-18

Reported by the user as "PyAutoMemory had another bug and didn't post to Slack
papers again". Two corrections to that framing, both load-bearing:

- The fix locus is **PyAutoMind**, not PyAutoMemory. PyAutoMemory only receives
  the filing into `arxiv-inbox.md`; its own `arxiv_refs.yml` has been green
  every night through the outage.
- It is not a *new* bug. The fix was written on **2026-09-16**, verified, pushed
  — and then abandoned without a PR.

## The finding

`pyauto-arxiv-papers` has failed four of the last five nights, always in the
`--livecheck` step, before a single paper is fetched. `arxiv_interests.yml`
fails on exactly the same nights.

| date | run | outcome | error |
|------|-----|---------|-------|
| 09-14 | 34819742473 | failure (12 s) | — |
| 09-15 | 34942645969 | failure (12 s) | `HTTP Error 429` |
| 09-16 | 35069362244 | success | — |
| 09-17 | 35195116083 | failure (9 s) | `HTTP Error 406: Not Acceptable` |
| 09-18 | 35318977894 | failure (11 s) | `HTTP Error 406: Not Acceptable` |

`PyAutoMemory/arxiv-inbox.md` still reads `last digest: 2026-09-16` — the
staleness stamp did its job and is how the loss is visible at all.

### Defect 1 (primary) — the repair exists and was never merged

`origin/claude/papers-slack-pyautomemory-39wrt1` carries commit `9f5fbab6`,
*"arxiv digest: retry arXiv 429s, never fail the recall guard on a network
error"* (2026-09-16, 103 lines of `arxiv_fetch.py` plus a 116-line
`tests/test_arxiv_fetch_retry.py`). It adds `_get()` with a ~5.5 min back-off
ladder honouring `Retry-After`, and makes `_livecheck()` warn-and-exit-0 on a
network failure instead of failing the run.

**There is no PR for it** (`gh pr list --state all --head …` is empty) and no
`active.md` / `planned.md` / `complete/` record. The 09-16 success in the table
is a `workflow_dispatch` *on that branch* — the fix was demonstrated working and
then dropped. `main` has been failing ever since.

### Defect 2 — the abandoned branch would still fail today

`RETRY_STATUSES = {429, 500, 502, 503, 504}`, with the comment *"Any other 4xx
is a bad request and retrying it would only mask the bug."* **406 is not in the
set.** On the branch's source:

- `_livecheck()` catches *any* `HTTPError` and warns → the guard survives a 406;
- but `_get()` re-raises the 406 without retrying, so the **fetch step** — the
  one the branch's own docstring nominates as the step that "gets to fail
  loudly" — dies instead. The digest still posts nothing.

So merging the branch as-is fixes 09-14/15 and not 09-17/18. 406 must join the
retried set, and the comment's premise — that a 4xx is always our bug — is what
needs revising: arXiv returns 406 as a *mitigation* response, not a
content-negotiation verdict.

### Not the cause — the User-Agent (tested, refuted)

An earlier reading of this blamed the bare `PyAutoLabs-papers-digest/1.0`
User-Agent (no contact URL, no `Accept` header) versus PyAutoMemory's
policy-conformant one. **Probed live on 2026-09-18 from a home IP**, all four
combinations of {bare UA, contact UA} × {no Accept, `application/atom+xml`}
returned **HTTP 200**. The headers are not the discriminator; the shared GitHub
Actions egress is. Adding a contact URL and an `Accept` header is worth doing as
arXiv-policy courtesy, but it must not be described in the PR as the fix.

### Not the cause — cron placement

The 02:00 UTC cron fires at ~07:20 UTC because of GitHub's global scheduler
backlog, measured at a stable ~+5 h in `complete/2026/09/cron-delivery-headroom.md`
(issue #396). Moving the cron does not move the run.

## What to do

1. Branch from `origin/claude/papers-slack-pyautomemory-39wrt1` (do not
   re-implement `_get()` — it is good work; recover it).
2. Add `406` to `RETRY_STATUSES` and rewrite the adjoining comment: 429 and 406
   are both arXiv edge mitigation against a shared egress, not bad requests.
   Leave the other 4xx unretried.
3. Add a contact URL to `USER_AGENT` and an explicit
   `Accept: application/atom+xml`, labelled as policy courtesy — not the fix.
4. Extend `tests/test_arxiv_fetch_retry.py` with the witness above: the 406
   ladder through `_get()`, and `fetch()` surviving the same sequence.
5. `arxiv_interests.py` imports `arxiv_fetch` and calls `arxiv_fetch.fetch()`
   (line 258), so it is covered by the same change — **verify, do not assume**,
   and say so in the PR.
6. Open the PR this time, and record the task in Mind.

## Recovery — four nights of papers are lost

The digest is announcement-band anchored, so tonight's run will **not** pick up
09-14, 09-15, 09-17 or 09-18. After the fix merges, recover them with a manual
`workflow_dispatch` of `arxiv_papers.yml` setting `LOOKBACK_HOURS` wide enough
to cover the gap, then check `PyAutoMemory/arxiv-inbox.md` gains the missing
dates. A deliberate, reviewed dispatch — a too-wide window floods Slack and the
inbox.

## Follow-up worth its own prompt

`PyAutoMemory/scripts/arxiv_refs.py:243` wraps every lookup in a bare
`except Exception: return None`. That is why its nightly job stayed green
through the same outage — it resolved nothing, silently. The opposite failure to
this one, and not in scope here.
