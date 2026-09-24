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
Blocked-by: euclid-dr1-positions-gate (#103)
Witness: on the census sample (euclid_dr1 inspect/positions_census) the regenerated positions carry no source-flux SNR < 2 counter-image and the fraction of tiles failing the gate's quick-fit trace drops from 16.6% (2,325/14,032); unit tests cover the SNR floor and the light-centre reflection.

Phase 2 of the positions work (phase 1: #103 positions gate). Root cause found 2026-09-24: 59-80% of the offending near-centre "multiple images" have source-flux SNR < 3. `preprocess/segmentation.py:174-196` and `util._compute_positions_from_source_flux` walk the counter-image SNR threshold down in 0.1 steps all the way to 0, and the "opposite side" test flips sign about the cutout centre (0,0) rather than the lens light centre. Floor the walk-down at SNR >= 2 and reflect about the brightest-pixel light centre. Kept separate from #103 because it changes the positions.json every future tile receives; existing tiles are handled by the gate. Research: euclid_dr1 `inspect/positions_census/research/A_central_radius.md` ("Separate finding").
