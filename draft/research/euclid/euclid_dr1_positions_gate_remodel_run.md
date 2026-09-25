# euclid_dr1: run the positions gate over DR1 and submit the remodel set

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-09-24
Unblocked 2026-09-25: phase 1 gate shipped (`complete/2026/09/euclid-dr1-positions-gate.md`, PR #104) and phase 2 finder shipped (`complete/2026/09/euclid-dr1-positions-finder.md`, PR #106). Run on the rewritten positions: the finder rollout (rewrite_positions over dr1_sep1_rest + dr1_sep1_top1000, RAL array 350731 onwards, then rsync) was still in progress at close-out — confirm it has landed first.
Witness: positions_meta.json sidecars exist for every dataset/dr1_sep1_rest tile, positions_review.csv lists the review tiles (~280 expected), and the resubmitted locked set's vis_lp fits no longer end on the penalty plateau (f_live < 1, N_eff > 1) for >= 85% of the 736 previously locked tiles.

Phase 3 of the positions work (phase 1: #103 gate; phase 2: finder SNR floor). Science/Cortex task in the euclid_dr1 clone (/mnt/c/Users/Jammy/Science/euclid_dr1): port the gate, run it over the 14,032 tiles (~12 CPU-h, RAL array), hold back review tiles, then resubmit the remodel set: 736 locked + 294 unlocked-central + 5 unlocked failing + 85 unfinished, and gate pending tiles before submission. Record the census and outcome in the euclid_dr1 Cortex ledger. Expected: 11,639 keep, 2,043 drop one image, 282 review; T at the 0.3" floor for 96%.
