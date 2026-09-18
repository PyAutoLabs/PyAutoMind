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
