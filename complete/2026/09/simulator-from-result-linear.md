## simulator-from-result-linear
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77 (closed completed 2026-09-17)
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/87 (head `f068d21`, merge `dc91d9a`, label `pending-release`)
- summary: |
    `scripts/simulator.py --from-result` rebuilt the tracer from `files/model.json` plus the
    max-log-likelihood parameter vector, but every profile this pipeline fits is linear
    (`al.lp_linear.*`), so the rebuilt profiles carried no intensity and the mock was noise —
    tile 0 of `dr1_sep1_sersics` simulated at mock VIS peak SNR 3.9 against 81 for the real data.
    The fix reads `files/tracer.json` instead: the solved-intensity tracer that
    `AnalysisDataset.save_results` already writes from
    `fit.model_obj_linear_light_profiles_to_light_profiles`, resolved under the same
    `resolve_files_path` hash, with a guard that no `lp_linear` profile survives the rebuild.
    A second commit clips PSF-convolution round-off negatives before PyAutoArray's Poisson draw.
    New tests `tests/test_simulator_from_result.py` and `tests/test_simulator_round_off_clip.py`;
    the `--from-result` bullet of `scripts/README.md` updated.

    Shipped under a human override. The 2026-09-13 `--auto` run parked at the autonomous ship
    gate on PyAutoHeart RED — verbatim "install verification FAILED (testpypi; checks F)" and
    "release validation FAILED (stage integrate)", both organism-scope and unrelated to this
    branch. On 2026-09-17 the human resumed the session and authorised the ship and the merge
    in-session with the words, verbatim: "prm if needed and then wrap up remove from mind etc".
    That quote is on the PR body, on issue #77 and in `autonomy_log.md`.
- witness: |
    Tile `Tile102008855RA0680593469007DECNEG0634007351862`: mock VIS peak/median-RMS 72.3 against
    81.1 for the real data (3.9 before the fix); `truth.json` lens intensity 0.008437 /
    source 8.180.
- ci: |
    162 fast + 10 slow tests pass after merging `origin/main` (`f068d21`), smoke 9/9,
    PR CI 9/9 legs green. Merged as `dc91d9a`.
- notes: |
    (1) The prompt's own fix sketch — rebuild the `FitImaging` through the aggregator to recover
    solved intensities — was not what shipped: `files/tracer.json` is already on disk beside
    `model.json` under the same hash, so no aggregator round-trip is needed.
    (2) The workspace's `--from-result` path had no test at all before this; both new test files
    are the first coverage it has ever had.

## Original prompt

# simulator.py --from-result rebuilds a dark tracer from linear-light-profile fits

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- simulation
Difficulty: medium
Autonomy: safe
Priority: high
Status: active
Consequence: judge
Witness: resimulating a `sersic_lens_model_baseline/vis` result of the euclid_sersics sample gives a mock whose VIS peak SNR is comparable to the real tile (order 80, not 4) and whose truth.json lens/source intensities are non-zero
Review-minutes: 20
Filed: 2026-09-13
Issued: 2026-09-13

User request (verbatim, 2026-09-13, after the euclid_sersics variants array 342808
produced its Sersic baseline results):

"""
ok, there was also part of the plane where we resimulate these 100 euclid lenses and
then model their simulated versions identically, can you produce that simulated package
of 100 lenses and get their vis_lp runs going
"""

followed by "im going out so autonomously get these sersic things simulatedf and their
vis_lp runs going".

## Defect

`scripts/simulator.py --from-result` (`tracer_from_result`) rebuilds the tracer from
`files/model.json` + the max-log-likelihood parameter vector. Every light profile this
pipeline fits is **linear** (`al.lp_linear.*`, MGE Gaussians included): their
intensities are solved inside the fit and are not model parameters, so the rebuilt
profiles carry no flux and the simulated image is pure noise. Observed on tile 0
of `dataset/dr1_sep1_sersics` from its `sersic_lens_model_baseline/vis` result:
peak SNR 3.9 in the mock against 81 in the real cut-out. No test covers
`--from-result`, which is why the documented "resimulate a fit" workflow never worked
on a real result.

## Fix

Recover the solved intensities the way the pipeline already does at fit end
(`util.py` uses `result.max_log_likelihood_fit` and
`fit.tracer_linear_light_profiles_to_light_profiles`): rebuild the max-log-likelihood
`FitImaging` from the result directory (aggregator over the search dir, which holds the
fitted dataset under `files/dataset/`, or an equivalent that uses the on-disk result
only) and take `fit.tracer_linear_light_profiles_to_light_profiles`, so
`tracer_from_result` returns standard profiles with their solved intensities. Keep
the prior-edge rule, `truth.json` contents and every CLI flag unchanged. Add a test
that resimulates a small linear-profile result fixture and asserts the mock's peak
SNR and non-zero truth intensities; add a regression assertion that the returned
tracer has no `lp_linear` profiles.

## Out of scope

Colour-correct SEDs (`sed: flat` stays), simulator fidelity knobs (shape, mask radius
are already CLI flags), and the science runs themselves (Cortex euclid_sersics).
