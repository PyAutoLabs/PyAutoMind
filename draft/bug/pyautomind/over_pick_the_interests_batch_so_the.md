# Over-pick the interests batch so the dedup cannot shrink the day

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Over-pick the interests batch so the dedup cannot shrink the day

Type: bug
Target: PyAutoMind
Autonomy: supervised
Priority: normal

@PyAutoMind's arxiv_interests.yml asks Claude for exactly 10 papers, and the interests_actions.py append it calls on the Memory side then drops any that are already on another list. On the first live run (run 33105368017) that cost a slot: Claude picked 10, one of them (2608.26039) was already in the arXiv inbox from the morning strong-lensing digest, and the day's batch landed as 9. The dedup is correct and must stay — that paper genuinely belongs to the lensing list. The batch size is the casualty, and it recurs whenever a pick overlaps the inbox or the reading queue.

Fix: have the Claude step over-pick. Ask the prompt in .github/workflows/arxiv_interests.yml for ~12-13 papers, ranked most interesting first, and let the existing --limit 10 on the append call take the first ten that survive dedup. PICK_COUNT in .github/scripts/arxiv_interests.py is written into the candidates JSON and referenced by the prompt, so it moves with it — keep 10 as the batch size that reaches append and make the over-pick a separate, named constant so the two numbers cannot be confused.

One workflow prompt plus one constant. No change needed on the Memory side: append already caps at BATCH_SIZE and dedupes against all three files.

Verify by reading a live run's log: the picks file should carry the over-pick count and the append line should read appended:10 on a day with an overlap.

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from user-intake -->
