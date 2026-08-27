- issue: none — the task arrived ad hoc in a web session ("pyautomemory has a 1 week
  waiting list thing for all strong lensing papers. it works great. I now want another
  list that functions the same but for other papers id be interested in"), so there is
  no PyAutoMind prompt and no GitHub issue. Recorded here anyway: this is the fifth
  entry in the paper-management line and the reasoning is worth finding again.
- shipped: 2026-08-27 — PyAutoMemory#66 (main 52c9f68), PyAutoMind#356 (main b7b609c4).
- classification: feature (PyAutoMemory + PyAutoMind) — fifth in the paper-management
  line after #35 (structured queue + arXiv ingest), #42 (per-paper board actions),
  #48 (claude-action filing) and `arxiv-inbox-tier` (#57, the strong-lensing inbox this
  one is modelled on).
- summary: a SECOND overnight suggestion tier, `arxiv-interests.md`, for everything the
  reader wants that is not strong lensing — black holes, dark matter, galaxy formation,
  statistics. PyAutoMind's new `arxiv_interests.yml` files the day's ten; the knowledge
  board renders them directly under the strong-lensing inbox with the same five
  per-paper actions (📄 ➕ 📥 📑 ✖️), plus one 🧹 button on the batch itself.
  `scripts/interests_actions.py` owns the format and the transitions and IMPORTS
  `inbox_actions` rather than restating the line grammar, the identity rule, the
  freshness stamp or `add_to_queue`.
- THE ONE DELIBERATE DIVERGENCE from the inbox, and the point of the feature: this is a
  day-batched BACKLOG, not a seven-day timer. Each run appends one dated batch, the
  board shows the OLDEST un-cleared batch only, and 🧹 drops that whole day and reveals
  the next. The human asked to "cycle through all recommended papers" — a lapse window
  would silently delete exactly what they asked to walk through. So `sweep` exists on
  the inbox and is deliberately absent here; the workflow comment says so, so a later
  reader does not add one back as "consistency".
- topic routing (new, and only needed here): every inbox paper routes to one section,
  but these span domains. Each line carries `<date> — [Topic] <title>[ — <ref>]`, the
  topic being the reading-queue section ➕ files into. A topic naming no real section
  falls back to a new `## Interests` section rather than returning `no-section` — the
  topic is a nightly prompt's GUESS, and a guess that misses must not cost a paper.
  `interests_actions.add_to_queue` wraps the inbox's with exactly that one retry.
- the cross-list gap, and why strong lensing is FLAGGED not EXCLUDED: the obvious design
  is to drop anything matching the lensing net, since those have their own list. That
  opens a hole — a dark matter paper that mentions a lensing constraint in passing
  matches the net here, is dropped by the lensing digest as off-topic, and appears on
  NEITHER list. So candidates carry `strong_lensing: true|false` and the prompt makes
  the judgement. Belt and braces: `append` dedupes against `arxiv-inbox.md` as well as
  the interests list and the reading queue, so a wrong judgement costs a duplicate that
  never happens rather than a paper that vanishes. Verified against the live repo — the
  2608.26039 lensed-quasar paper already in the inbox was skipped (appended:4 of 5).
- why a separate workflow rather than a second leg of arxiv_papers.yml: that digest is
  the morning's Slack product and its Claude step is the single point of failure for the
  post. A broad second query, a much bigger prompt and a second cross-repo push do not
  belong on that critical path. arxiv_interests.yml has no Slack leg at all — it exists
  to fill one board surface. A bad day here costs the interests list and nothing else.
- the rank/judge split (the house pattern, applied to a much bigger input): the lensing
  query is narrow enough that Claude only drops the odd false positive. "Which ten of
  today's astro-ph would this reader most want?" has no such query, and no budget to
  hand Claude a whole day's abstracts either. So `.github/scripts/arxiv_interests.py`
  pages the band across astro-ph.CO/GA/HE/IM, scores every paper against an interest
  profile (title hit ×3, abstract hit ×1; best-scoring topic becomes the suggested
  section) and passes the top 60 with full abstracts; Claude then judges those. The
  scoring is a SHORTLIST, never a verdict — generous on purpose, recall first, exactly
  as the lensing query is.
- traps:
  - `arxiv_fetch.fetch()` was hardcoded to `start=0`. Fine for a lensing band (~1.5
    papers); a whole day of astro-ph needs paging. Added `start=` there rather than
    forking the fetch, so both digests share one API client.
  - the two digests MUST take the same announcement band or a paper falls into the
    seam. `announcement_band()` is imported, never restated, and the interests cron is
    30 min behind the lensing one (02:30 UTC) — same band, and by then the inbox is
    filed, which is what the dedup reads.
  - `interests_actions.py` could not reuse `inbox_actions.parse_body` wholesale: that
    one defaults a missing `section:` to `INBOX_TARGET_SECTION` ("Strong Lensing"),
    which is the single section these papers are never for. Overridden to None, and
    there is a test that says why.
  - `board.py`'s `_fresh_span` was a closure over the inbox's `fresh` dict. Rendering a
    second tier through it would have reported the healthy digest's date for the broken
    one — the exact ambiguity the stamp exists to remove. Made the tier an explicit
    parameter; test `test_the_two_tiers_carry_their_own_stamps` pins it.
  - the label trap from #42/#57 again: three new labels (`interests-add`,
    `interests-dismiss`, `interests-clear`) added to knowledge_board.yml's ensure step.
    A prefilled `labels=` silently drops a label the repo lacks, and queue_actions.yml
    gates on the label, so a missing one makes a tapped button look like it worked.
  - `spawn.py` still has no root-file catch-all: `arxiv-interests.md` needed an explicit
    EMPTY rule and an EMPTY_TITLES entry, and `arxiv_interests.yml` a DROP rule, or the
    spawn run fails on an unmatched file. `.github/scripts/*` is already DROP and
    `scripts/*`/`tests/*` KEEP, so the ranker and the new module needed nothing.
  - three pre-existing board tests moved because the synthetic tree now writes an
    interests file: the two inbox-freshness helpers blank the other tier so they still
    assert about the inbox alone, and the PDF-button count went 4 → 6. Worth knowing
    that `_tree()` is shared and grows.
- NOT verified live: arXiv is unreachable from a web session's network policy
  (`export.arxiv.org` 403s at the agent proxy), so the ranker is tested offline only and
  the real band volume — and therefore whether `MAX_PAGES = 12` is generous enough — was
  unmeasured at merge. The first run logs `announced=/scored=/shortlisted=` to check
  against, and a truncated band emits a `::warning::` rather than silently dropping the
  band's oldest papers.
- testing: PyAutoMemory `make validate` + 168 tests green (34 new in
  `tests/test_interests_actions.py`, 13 new in `tests/test_board.py`); PyAutoMind 245
  tests green plus both script `--selftest`s. Exercised end to end against a clone of
  the live Memory repo: append → stamp → add (routed by topic) → add (fallback) →
  dismiss → clear → next day revealed.
