- issue: none — filed as a PyAutoMind prompt from the first live run of the
  interests digest, not as a GitHub issue.
  Prompt: `draft/bug/pyautomind/over_pick_the_interests_batch_so_the.md`
  (retired by this record).
- shipped: 2026-08-27 — PyAutoMind#359 (main 44313731). Shipped in one PR with
  its sibling `interests-ranker-widened-categories`; both came out of the same
  run's logs and touch the same two files.
- classification: bug (PyAutoMind) — sixth in the paper-management line, first
  follow-up to `arxiv-interests-tier` shipped the same day.
- summary: the interests digest asked Claude for exactly 10 papers, and the
  `append` on the Memory side then dropped any already on the strong-lensing
  inbox or in the reading queue. On the very first live run (run 33105368017)
  that cost a slot: 2608.26039 was on both lists' radar, so a ten-pick day
  filed nine. Fixed by over-picking — `PICK_COUNT = BATCH_SIZE + OVERPICK`
  (13), returned ranked, and `append` trims to its own cap IN ORDER after
  deduping.
- why over-pick rather than loosen the dedup: the dedup is correct. 2608.26039
  is genuinely a lensed-quasar paper and genuinely belongs to the other list;
  the digest's job is to not duplicate it, and it did that. What was wrong was
  asking for exactly as many as should land, which leaves no slack for a
  correct rejection. Worth remembering as a shape: any pipeline whose last
  stage can reject must be fed more than its target.
- the load-bearing part is ORDERING, and the prompt now says so in those words.
  `append` takes the picks in order and stops at the cap, so the tail is what a
  no-overlap day discards and what a two-overlap day promotes. A prompt that
  returned 13 unordered picks would file an arbitrary ten.
- where the cap lives, and why it is not restated: `interests_actions.py` owns
  it (its `BATCH_SIZE`, the default of `append --limit`). The workflow
  deliberately passes NO `--limit`, and the comment says why — the same number
  in two repos is how they drift. PICK_COUNT on the Mind side is the ASK; the
  cap on the Memory side is the LAND. Two different numbers, two owners, one
  direction of travel.
- traps:
  - the obvious fix — bump PICK_COUNT to 13 — reads as "the batch is now 13"
    to the next person. Split into `BATCH_SIZE` + `OVERPICK` so the two numbers
    cannot be confused, and neither name lies.
  - the candidates JSON now carries `batch` alongside `pick`, because the
    prompt has to be told what actually lands to reason about the tail.
- verify on a live run: the picks file should carry 13 entries, and the append
  line should read `appended:10` on a day with an overlap (it read
  `appended:9` on the run that motivated this).
