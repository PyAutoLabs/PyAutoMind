# Close-out carries a generated prompt's Source-key into its completion record

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-28
Epic: autonomous-orchestrators
Phase: 14
Consequence: glance
Witness: `python3 scripts/lifecycle.py close <slug> … --apply` on a prompt that carries a `Source-key:` header writes a complete/ record that keeps `Source-key: <key>` (and the writer's `<!-- maint-key: … -->` mark); a test fails on the base commit; a prompt without one is unchanged
Review-minutes: 5
Lane: any
Unattended: ready

Found in the review of PyAutoBrain#747 (the Homeostasis board on the Brain board). The board derives each finding's status from Mind by its key marks. It shows "done" when a complete/ record carries the key, but `lifecycle.py close` writes the record from the completion body and drops the prompt's `Source-key:`. So a closed maintenance task never shows as "done". Carry the header and the mark into the record, either in the folded "Original prompt" section or as a top-level line, whichever `_homeostasis.mind_marks` reads (check PyAutoBrain `board/_homeostasis.py`).
