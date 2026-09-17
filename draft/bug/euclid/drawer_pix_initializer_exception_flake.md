# `test_latent_run_level.py` slow suite flakes 1-in-7: the `drawer_pix` Drawer raises `InitializerException` because all three draws share one figure of merit

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- ci
- source-reconstruction
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: euclid-dr1-prep
Filed: 2026-09-16
Updated: 2026-09-16

## Observed

Seen 2026-09-16 while shipping pipeline issue #78 (task `pixelized-clumps-robust-scale`).
Across 7 runs of `pytest tests/test_latent_run_level.py -m slow` in the task worktree,
6 passed and 1 errored at the module fixture `run_level` with
`autofit.exc.InitializerException: The initial samples all have the same figure of merit`,
raised inside `search.fit` for the `drawer_pix` leg (`af.Drawer`,
`total_draws=PIXELIZED_TOTAL_DRAWS` = 3 uniform draws of `einstein_radius` within +/-10% of
truth; Delaunay mesh + adapt image built once at the truth lens, `tests/pixelized_model.py`).
The light-profile `drawer` leg never errored.

## Structural

This is upstream of `save_results` and the wcs.json clump finder, so #78 cannot cause it: it
is pre-existing, masked by the suite having no repeat runs. The same `run_level` fixture also
showed the pixelized clump count is chaotic in the drawn `einstein_radius` (#78's PR body has
the sweep). The two are likely one root cause: an off-truth draw fitted through a mesh built
at truth can fail the inversion for every draw, and PyAutoFit collapses identical figures of
merit into `InitializerException`.

## Ask

1. Reproduce with a fixed-seed sweep over `einstein_radius` (+/-10%) on the committed
   simulated dataset, and record which draws produce the identical penalty — is it the
   `positive_only` solver failing, a `LinAlgError` caught into a penalty, or regularisation
   blow-up?
2. Decide the fix: seed the Drawer in the fixture / narrow the prior, rebuild the mesh per
   draw (what the production pipeline does), or make the fixture retry.
3. Document the choice in the module docstring.

The run-level suite must be deterministic before it gates CI.

## Evidence pointers

- `$SCRATCH/relaxed_run*.log` from the 2026-09-16 session (may be gone).
- The PR for #78 carries the `einstein_radius` sweep table.

- 2026-09-16 (/prm on #79): `main`'s own Tests run 34677820679 (a363f57, slow py3.13 leg, 2026-09-12) is red on exactly this `InitializerException` at `run_level` setup — 6 errors, 12 s in — so main has carried this flake since the #73 merge; the PR-side legs never ran (see the pyautoheart relevance-gate prompt).
- 2026-09-17 (/prm on #83 / PR #85, `feature/astrometric-offsets-catalogue`, a producer-and-docs-only diff): PR-side Tests run 35209199550 red on the `slow` py3.12 leg only — all 10 `run_level` tests errored at setup, `drawer_pix` leg ("Performing DrawerSearch for a total of 3 points" then `InitializerException`), 13 s in; the py3.13 twin and the `drawer` light-profile leg passed. Log saved from `gh run view 35209199550 --log-failed`. Second sighting on CI, first on a PR leg.
