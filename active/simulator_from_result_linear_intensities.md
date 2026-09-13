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
