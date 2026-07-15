# arXiv #papers digest silently drops papers — window anchored to submission, not announcement

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

The #papers digest missed two strong-lensing papers announced on 2026-07-15
(arXiv:2607.12129, a lensed-arc candidate in MACS J0308.9+2645; arXiv:2607.12209,
the NGC 6505 Einstein ring OSN recovery test). Both are matched by the keyword
query — re-running `.github/scripts/arxiv_fetch.py` with LOOKBACK_HOURS=72
returns both — so the recall-first `QUERY` is not at fault.

Root cause: `arxiv_fetch.py:77` keeps papers whose `<published>` (v1 *submission*
timestamp) falls within `LOOKBACK_HOURS` of now, but the arXiv search API only
indexes a paper once it is *announced*, which is 1–3 days after submission.
Both papers were submitted Mon 2026-07-13 at 20:24 and 23:18 UTC — after the
Mon 14:00 ET cut-off — so they went into the Tue 20:00 ET announcement batch and
became searchable at 00:00 UTC Wed 2026-07-15. Wednesday's 02:00 UTC run looked
back 24 h to Tue 02:00 UTC; their Monday timestamps fall ~3 h the wrong side of
that boundary. Tuesday's run could not have seen them either (not yet announced).
Permanently dropped, with no error and no gap in the heartbeat.

The module docstring's claim that consecutive runs "cover disjoint day-bands
(gapless)" only holds if papers are searchable at submission time. They are not,
so every run has a dropped tail, and Monday/Tuesday are worst:

| Run (02:00 UTC) | Window queried (by submission) | Batch actually announced by then | Gap |
|---|---|---|---|
| Tue (24 h) | Mon 02:00 → Tue 02:00 | Fri 18:00 → Mon 18:00 UTC | misses Fri 18:00 → Mon 02:00 |
| Wed–Fri (24 h) | prev 02:00 → 02:00 | prev-day 18:00 → 18:00 UTC | misses the 18:00 → 02:00 tail |
| Mon (72 h) | Fri 02:00 → Mon 02:00 | Thu 18:00 → Fri 18:00 UTC | sweeps three days not yet announced |

Monday's 72 h "weekend sweep" is the clearest illustration: weekend submissions
are not announced until Mon 20:00 ET — after Monday's run — and Tuesday's 24 h
window has already moved past them.

Fix: anchor the window to arXiv's announcement bands rather than a rolling
"last N hours", preserving the existing stateless disjoint-band design and its
jitter tolerance; only the band edges change. At a 02:00 UTC run the freshly
announced batch is submissions from roughly 32 h to 8 h ago; the Monday run needs
the three-day Fri 14:00 ET → Mon 14:00 ET band. The ET→UTC offset shifts by an
hour across DST (14:00 ET = 18:00 UTC in EDT, 19:00 UTC in EST) and must be
computed, not hard-coded. Update the docstring's gapless-band rationale to state
the announcement anchor. Include a one-off backfill run to recover papers the
current windows have already dropped.

<!-- filed from a CLI session on 2026-07-15 after the user reported the miss -->
