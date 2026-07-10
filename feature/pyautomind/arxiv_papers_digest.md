# Daily arXiv strong-lensing paper digest → Slack #papers

**Target:** @PyAutoMind
**Work type:** feature (Slack/digest infrastructure)
**Autonomy:** safe
**Difficulty:** small

## Original request (verbatim)

> We have successfully made piprelease post on SLACK showing release notes.
> Could we have it so that an AI I subscribe too looks at the arxiv each day,
> finds all strong lensing papers, and produces a concise summary which is
> posted to the #papers channel

Follow-ups (same session, 2026-07-10):
> can this be done on just a claude subscription though?
> make sure it runs late enough that its "that mornings" arxiv papers for UK scientists

## Scope decisions (user, 2026-07-10)

- **Scope:** strong lensing only. Measured rate is ~1.5 papers/day (strong
  lensing is a small field); the query is recall-first (see below) so genuinely
  relevant papers are not missed, and Claude drops the ~2 keyword false-positives
  per fortnight.
- **Format:** curated — 1–3 AI-chosen highlights (2–3 sentence summaries) then a
  compact list of the rest.
- **Cadence:** weekday mornings, skip silently on empty days (no quiet-day post).
- **Timing:** run late enough to be "that morning's" papers for UK scientists.
- **Billing:** must run on the Claude *subscription*, not a metered API key.

## Goal

A daily GitHub Actions job (sibling of `morning_status.yml`, the commit digest)
that fetches new strong-lensing papers from arXiv, has Claude summarise them,
and posts the summary to Slack **#papers**.

## Plan

New workflow `@PyAutoMind/.github/workflows/arxiv_papers.yml` + helper
`@PyAutoMind/.github/scripts/arxiv_fetch.py`, three steps mirroring
`morning_status.yml`:

1. **Fetch** (`arxiv_fetch.py`): recall-first arXiv API query over
   `cat:astro-ph.CO OR cat:astro-ph.GA` matching strong-lensing vocabulary in
   abstract/title — not just the literal phrase "strong lensing" but also
   "lensed quasar", "lens modelling", "Einstein ring/radius", "quadruply/doubly
   imaged", "double source plane", etc. (Deliberately omits the broad
   "gravitational lensing" / "weak lensing" / "microlensing" catch-alls so the
   net stays strong-lensing-shaped; `cat:` also matches cross-lists.) Validated
   2026-07-10: the narrow phrase-only query *missed* the Li+Collett WFI2033
   lensed-quasar paper (07-09) — the broadened query catches it. Sorted by
   `submittedDate` desc. Keep papers whose **original**
   submission timestamp (`<published>`, v1 — so revisions and old cross-lists
   don't resurface) falls within the look-back window: 24 h on Tue–Fri, 72 h on
   Monday to sweep the weekend. Stateless (no cross-run dedupe store); windows
   anchored to wall-clock `now` cover disjoint day-bands. Emits
   `arxiv_papers.json`.
2. **Summarise** (`claude-code-action@v1`, `--allowedTools "Write"`,
   `show_full_output`): reuses `CLAUDE_CODE_OAUTH_TOKEN` (the **Claude
   subscription** OAuth token already set for the commit digest — no API key, no
   metered billing). Drops keyword-false-positives using the abstract, picks
   1–3 highlights with short summaries + a compact list of the rest, writes
   `slack_payload.json`. Skipped entirely (via `if: fetch.count != 0`) on empty
   fetch days.
3. **POST**: `curl` `slack_payload.json` to `secrets.PYAUTO_PAPERS_WEBHOOK_URL`.
   Missing payload (Claude judged nothing on-topic) → skip silently, no post.

**Timing:** `cron: "0 6 * * 1-5"` (06:00 UTC, Mon–Fri). arXiv's astro-ph
announcement is live by ~00:00–01:00 UTC; GitHub cron jitters 0–3 h later, so
actual delivery is UK ~07:00–10:00 — firmly after the overnight announcement, so
it reads as "this morning's papers." `workflow_dispatch` for manual test-fires.

## Required human setup (one-time, before first useful run)

1. Create a Slack **incoming webhook** pointing at **#papers**; add its URL as
   the `PYAUTO_PAPERS_WEBHOOK_URL` secret in PyAutoMind.
2. `CLAUDE_CODE_OAUTH_TOKEN` is already present in PyAutoMind (used by the commit
   digest) — no action needed.

Until (1) is done the fetch + summarise steps run but the POST step errors
loudly (by design — a misconfigured webhook must not pass silently).

## Notes

- The arXiv fetcher was validated against the live API before shipping (HTTPS
  endpoint, Atom XML parse, submission-date window, dedupe).
- Effective level under `--auto`: safe (feature cap, small difficulty). Parked
  at the Heart-YELLOW ship checkpoint (YELLOW·60 at launch, no reason set acked)
  — see the autonomy contract, leg 4. Merge/close human.
