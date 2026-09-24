# euclid_dr1: fix the segmentation counter-image finder (SNR walk-down floor, opposite side about the light centre)

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-24
Related: euclid-dr1-positions-gate (#103, PR #104) — logical predecessor, disjoint code; not a hard block
Witness: on the census sample (euclid_dr1 inspect/positions_census) the regenerated positions carry no source-flux SNR < 2 counter-image and the fraction of tiles failing the gate's quick-fit trace drops from 16.6% (2,325/14,032); unit tests cover the SNR floor and the light-centre reflection.

Phase 2 of the positions work (phase 1: #103 positions gate). Root cause found 2026-09-24: 59-80% of the offending near-centre "multiple images" have source-flux SNR < 3. `preprocess/segmentation.py:174-196` and `util._compute_positions_from_source_flux` walk the counter-image SNR threshold down in 0.1 steps all the way to 0, and the "opposite side" test flips sign about the cutout centre (0,0) rather than the lens light centre. Floor the walk-down at SNR >= 2 and reflect about the brightest-pixel light centre. Kept separate from #103 because it changes the positions.json every future tile receives; existing tiles are handled by the gate. Research: euclid_dr1 `inspect/positions_census/research/A_central_radius.md` ("Separate finding").

## Parked 2026-09-24 — resume here
Human sequencing decision (2026-09-24): first get runs going with the current updates (PR #104 gate) and confirm they are OK, then do this positions-finder update, then the full DR1 run (phase 3). Plan presented in-session, not yet approved; no issue, no worktree.

Code today (both copies identical): `preprocess/segmentation.py:151 compute_positions` (canonical positions.json writer) and `util.py:55 _compute_positions_from_source_flux` (fallback in load_vis_dataset). Local maxima of segmentation/source_flux.fits with SNR > 3, brightest N_POSITIONS kept; if none is on the "opposite side" of the brightest, the SNR threshold is walked down in 0.1 steps to 0 and the first opposite-side peak replaces the weakest position. Two defects: `while threshold >= 0` has no floor (accepts noise/nucleus residuals); the opposite-side test `p[0]*p0[0] < 0 or p[1]*p0[1] < 0` is a per-axis sign flip about the cutout origin (0,0), not a test about the light centre.

Plan (to approve at resume):
1. One shared finder function (util.py, or a preprocess-safe module if util's autolens import is too heavy for preprocess) called by both writers, parameters `snr_floor=2.0`, `light_centre`.
2. Opposite-side test = dot product about the light centre: (cand - c)·(p0 - c) < 0.
3. Both writers pass the brightest lens-flux pixel as light centre (same definition as the gate), fallback mask centre.
4. Tests (tests/test_util.py): walk-down stops at the floor and returns the set without a counter-image; reflection accepts a true counter-image, rejects the (0.5,-0.5) vs (0.5,0.5) case; parity between the two writers on a synthetic map.
5. Witness on the census: regenerate positions for a few hundred tiles with segmentation/source_flux.fits, run the #104 gate over old vs new positions, report the drop in trace failures and the removal of SNR < 2 counter-images.
Branch `feature/euclid-dr1-finder-snr-floor`, own worktree; issue title `fix: counter-image finder — SNR floor and light-centre opposite test`.
