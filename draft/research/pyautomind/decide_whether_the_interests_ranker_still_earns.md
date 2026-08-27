# Decide whether the interests ranker still earns its place

Type: research
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised

Decide whether the interests ranker still earns its place

Type: research
Target: PyAutoMind
Autonomy: supervised
Priority: low

@PyAutoMind's .github/scripts/arxiv_interests.py was designed around an assumption the first live run falsified. It scores the whole announcement band against a keyword interest profile and passes the top CANDIDATE_CAP=60 to Claude, on the premise that astro-ph.CO/GA/HE/IM announce several hundred papers a day and no single prompt could read them all.

The first live run measured band_count=61, scored_count=52, truncated=false. So the band is ~60 papers, not several hundred; the keyword net dropped 9 of 61; and the 60-paper cap never bound. The curation is already entirely Claude's judgement over essentially the whole day, and the interest vocabulary in INTERESTS is doing almost no filtering work.

That may be the better outcome — it is truer to 'the ten most relevant papers that day' than a keyword shortlist is — but it means a whole deterministic stage may be dead weight, and the paging (MAX_PAGES=12) is guarding against a volume that does not exist.

This needs a decision, not a patch. The options:
- drop the ranker and pass the band straight to Claude, keeping only the strong_lensing flag and the topic hint;
- keep it purely as a runaway guard for the 3-day Monday band, and say so in the docstring instead of describing it as a shortlist;
- widen CATEGORIES now that there is headroom, which is the only option that makes the ranker matter again.

Do not decide on one day's data. Collect band_count / scored_count from the run logs for at least a full week, including a Monday (the 3-day band, which is the only run that could plausibly need the paging), then choose. The numbers are already logged by the shortlist step on every run — this task is mostly reading them.

Sibling of the shipped arxiv-interests-tier record in complete/2026/08/, which records the original assumption and why it was made.

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from user-intake -->
