- issue: none — filed as a PyAutoMind prompt from the first live run's logs.
  Prompt: `draft/research/pyautomind/decide_whether_the_interests_ranker_still_earns.md`
  (retired by this record).
- shipped: 2026-08-27 — PyAutoMind#359 (main 44313731), one PR with its sibling
  `interests-overpick-dedup-slack`.
- classification: research → decision + implementation (PyAutoMind). Filed as
  research because it needed a judgement, not a patch; closed the same day
  because the human made the judgement.
- the measurement that started it: the first live run logged
  `band_count=61, scored_count=52, truncated=false`. `arxiv_interests.py` was
  designed on the premise that astro-ph.CO/GA/HE/IM announce several hundred
  papers a day and no prompt could read them all — hence a keyword ranker and
  `CANDIDATE_CAP = 60`. At 61 papers the cap never bound, the keyword net
  dropped 9 of 61, and the whole shortlist stage was decoration. The paging
  (`MAX_PAGES = 12`) was guarding a volume that does not exist.
- the decision (human, overruling the prompt): WIDEN the categories rather than
  retire the ranker. Four → eight: `gr-qc` (black-hole theory, GW, primordial
  black holes — a real gap, none of it reaches astro-ph), `astro-ph.SR` (the
  stellar populations galaxy-evolution work is built on), and
  `stat.ME`/`stat.ML` (the inference methods behind the Stats bucket). Spends
  the headroom on coverage; the cap binds again, so the stage does the job it
  was written for.
  The rejected options are recorded because they stay available: retire the
  ranker and pass the band straight to Claude (simplest, no backstop), or keep
  it purely as a runaway guard for the 3-day Monday band (smallest change).
- THE OVERRULE, recorded deliberately: the filed prompt said explicitly not to
  decide on one day's data and to collect a week including a Monday 3-day band
  first. That caution was the agent's; the human overruled it. Noted because
  the widening is the reversible half — `CATEGORIES` is one tuple — and because
  a later reader finding a prompt that says "collect a week" beside a record
  that says "decided the same day" should see that as a choice, not drift.
- HOME_BONUS, the part nobody asked for and the list needed: widening alone
  would have made the digest WORSE. In `stat.ME`/`stat.ML`, "Bayesian",
  "posterior", "inference" and "hierarchical model" are the house vocabulary —
  every paper there scores on the Stats terms, so a Bayesian method for
  clinical trials out-scores a lens-modelling paper on keywords alone and
  crowds it off a 60-paper shortlist. A paper whose primary category is
  `astro-ph.*` or `gr-qc` now starts +4 ahead.
  Three properties, each pinned by a selftest check rather than left to prose:
  it rides on a NON-ZERO keyword score (a tie-breaker among papers already on
  topic, never a way in for one that matched nothing); it is not a filter (a
  strong stats paper still makes the list, and Claude still judges what
  survives); and `keyword_score` + `home` ride in the candidates JSON so the
  prompt sees the thumb on the scale instead of inferring it.
  The generalisable bit: widening a net changes what the net's weights MEAN.
  Terms tuned against one population silently mis-rank another.
- gr-qc counts as a home category, not a borrowed one — it was added for the
  black-hole work, so penalising it would defeat its own addition.
- traps:
  - `cat:` matches cross-lists, so a stats paper cross-listed to astro-ph was
    already reachable before this change. What widening adds is the papers that
    NEVER cross-list — which is most of gr-qc's theory output.
  - the band volume is still unmeasured after this change: arXiv is unreachable
    from a web session (`export.arxiv.org` 403s at the agent proxy), so the
    widened query is syntax-checked and the scoring tested offline only.
- verify on the next live run: `announced=` should jump from ~61 into the low
  hundreds and `shortlisted=` should sit AT the 60 cap rather than below it. If
  it lands somewhere silly in either direction, that is the signal to trim
  `CATEGORIES` or raise `CANDIDATE_CAP` — and the week of `band_count` data the
  original prompt asked for is still worth reading before tuning further.
