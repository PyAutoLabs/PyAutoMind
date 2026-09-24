# euclid_dr1: sanitise positions.json (drop central/spurious multiple images) before modelling

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Scheduled: 2026-09-24
Consequence: glance
Witness: the gate run on the 5 output_locked exemplar tiles resolves 4 to T = 0.3" and sends Tile102014702RA0131539972904DECNEG0557431062995 to review; on the census sample (inspect/positions_census) its pass/fail reproduces the RAL lock verdicts for >= 97% of locked and 100% of clean unlocked tiles and drops no image from a clean unlocked tile; unit tests cover the 0.15" cut, the one-drop rule, the T clamp and the SNR >= 2 walk-down floor.
Review-minutes: 3
Unattended: needs-slicing


Scheduled for 2026-09-24. Code: the positions.json producer lives in euclid_strong_lens_modeling_pipeline (preprocess/segmentation.py, util.py load path); then port it to the euclid_dr1 science project (/mnt/c/Users/Jammy/Science/euclid_dr1) and apply it to its dataset/dr1_sep1_rest tiles.

## Method (research settled 2026-09-24; supersedes the 2026-09-23 three-step draft)
Full reports and prototype scripts: euclid_dr1 `inspect/positions_census/research/` (A_central_radius.md, B_final_method.md, SYNTHESIS.md, quickfit3.py, policy.py, guard.py). Census data alongside in `inspect/positions_census/`.

Per tile, as a standalone pre-submit gate in `hpc/` writing a `positions_meta.json` sidecar; `positions.json` stays raw and untouched; `load_vis_dataset` reads the per-tile threshold from the sidecar and falls back to 0.2 when absent:

1. **Hard reject** positions within **0.15"** (one PSF FWHM) of the brightest-pixel light centre that vis_lp fixes its mass centre to. NOT 0.3": real counter-images of compact doubles (thetaE 0.5-0.66", inner/outer radius ratio >= 0.26) sit at 0.2-0.3"; the flat 0.3" cut costs 7 clean tiles and fixes only 114/734 locked, the 0.15" cut plus the step-3 drop fixes 201/734 at zero genuine cost.
2. **Quick fit in exactly vis_lp's model space**: SIE with the centre fixed at the light centre plus external shear, thetaE in [0,8], gamma_i in [-0.3,0.3], |e|<0.95. A multi-start `least_squares` on the source-plane chi^2 (sigma 0.05") with the ell_comps N(0,0.3) prior and a weak shear term gives a plausibility cost J; an SLSQP minimax seeded from it gives s_min, the exact max pairwise source-plane separation `PositionsLH` penalises. Take the minimum over these and the census Nelder-Mead starts plus a thetaE grid (the new fit alone misses the census minimum on ~5% of sets by <= 0.05").
3. **Outlier drop**: if s_min <= 0.2" keep all. Else, for n >= 3, leave one image out in turn; candidates are drops giving s <= 0.2". One candidate: drop it. Several: lowest J if it beats the next by dJ >= 4, else geometry (nearest if r < 0.3" or r < 0.6 x median radius of the others; outermost if r > 1.5 x that median); else review `ambiguous`. No candidate: review `no_single_drop`; n == 2 failing: review `n2_fail`. Never drop more than one image automatically, never leave fewer than 2; if fewer than 2 would survive step 1, run with the positions penalty off and flag `n_lt_2` (101 tiles).
4. **Plausibility flag, list only, no drop**: a traceable set where one drop lowers J by >= 10 uniquely (a mass model bending to absorb a central image at 0.15-0.3"; ~176 bent `pass_central` fits). Decision 2026-09-24: flag only.
5. **Per-tile threshold** T = min(max(2 x s_final, 0.3"), 0.5"); 2 x s_final > 0.5" goes to review. Factor 2: 0/3796 traceable fits locked when 0.2/s_min >= 2, the 7 traceable-but-locked all had a smaller margin. Floor 0.3": 22.7% of clean fits are pinned at the 0.2" wall (16% even at s_min ~ 0), pinned fits have median |gamma| 0.20 vs 0.14 and e 0.30 vs 0.23; a 0.1" floor would newly bind 50% of clean fits. Cap 0.5": the penalty rejects 99.9% of vis_lp prior volume at 0.2", 99.4% at 0.3", 97.6% at 0.5", 89% at 1.0"; uncapped, unresolved locked tiles get median T = 0.96". Decision 2026-09-24: floor 0.3" accepted.
6. **Review list** `positions_review.csv` per batch (~282 tiles, 2%); review tiles are held back from submission by default (decision 2026-09-24). vis_pix is unaffected: it re-derives its threshold from the vis_lp result via `positions_likelihood_from(factor=3, minimum_threshold=0.2)`.
7. **Fix the root cause in the finder** in the same task (decision 2026-09-24): `preprocess/segmentation.py:174-196` and `util._compute_positions_from_source_flux` walk the counter-image SNR threshold down in 0.1 steps to 0, and the "opposite side" test flips sign about the cutout centre (0,0), not the light centre. 59-80% of offending near-centre positions have source-flux SNR < 3. Floor the walk-down at SNR >= 2 and test about the light centre.

Expected on 14,032 tiles: 11,639 keep, 2,043 drop one image, 282 review; T at the floor for 96.4% (p95 0.30"); the drop resolves 647/735 locked. Prototype on 213 tiles: pass/fail matches RAL for 114/117 locked and 96/96 unlocked, drops nothing from unlocked fits, resolves 4/5 output_locked exemplars to T = 0.3 (Tile102014702... -> review); ~1 CPU-s per full-set fit, ~9 CPU-s per quad needing leave-one-out, ~12 CPU-h for the full set.

<!-- formalised by the Intake (Conception) Agent on 2026-09-23 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/f6d9d1ab-336c-4bd3-adb2-ec380b7ed943/scratchpad/intake_raw.md -->
