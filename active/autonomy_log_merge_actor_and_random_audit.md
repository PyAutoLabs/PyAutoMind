# Autonomy log: record who merged, and audit a random sample

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: normal
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: (a) each new shadow row carries a merge actor written by the tool (from `gh pr view --json mergedBy` and whether `/prm` was typed by the human), shown on one real row; (b) a test shows the count function leaves out human-typed `/prm` rows; (c) the recount of the 69 stage-1 rows is printed in three classes (expected: about 30 human `/prm`, 8 to 10 automatic or in-turn, about 29 not stated); (d) the sampler draws the same 1-in-5 sample twice from the same seed
Review-minutes: 10
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, finding FLOW-2, confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B4 and Appendix A. Data: `evidence/workflows_as_run/`.

**What was measured.** In the 69 counted rows of the glance window (2026-10-06 to 11-03, all recorded merged-unchanged), about 30 merges were a human-typed `/prm` according to the matching completion records, 8 to 10 state an automatic or in-turn merge, and about 29 do not say who merged. The ruling's own ledger-accuracy rule says human-typed `/prm` rows are re-marked and left out of the count; it was applied to one row, and the counting code has no merge-actor test, so the count still includes them. The 8 of 8 audit was a sample chosen by the session that proposed the grant.

Doctrine already withholds unattended merging until ten adversary-legged stage-2 rows exist, and that table has 0 rows. So the gap is the uncounted merge actor and the non-random audit, not a missing gate.

**The change.**
1. Add a merge-actor column to the shadow row, written by the tool at close-out.
2. Make the count function apply the ledger-accuracy rule in code, and print the recount of stage 1.
3. Replace hand-picked audits with a seeded random sample (for example 1 row in 5), audited within a week.
4. Record "read by the human on <date>", so that merged-unchanged is an answer and not a default.

**What this does not do.** It does not change the glance ruling. If the recount changes what the ruling rests on, that is a `judge` question for the human and a separate prompt. The ten stage-2 rows need real shifts, not code.

`Unattended: never` because it changes the autonomy ledger itself.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
