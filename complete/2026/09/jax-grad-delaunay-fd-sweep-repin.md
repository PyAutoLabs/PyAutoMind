# jax_grad/delaunay's FD step sweep re-pinned out of the round-off floor (Heart RED corrective)

autolens_workspace_test#305 → `4103234e`, closing autolens_workspace_test#304, merged 2026-09-07. The seventh and last corrective PR of 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reason: `release validation FAILED (stage integrate)`; Release Integrate run 34148543011 — the integrate-only re-dispatch on TestPyPI 2026.9.7.1.dev75601 after #300–#303 + agwt#119 — failed only this script). Fable session diagnosed via an Opus subagent, planned, and delegated implementation + ship to Opus; merged via /prm the same day. Validation of the RED clearing is a further integrate-only re-dispatch on the same TestPyPI version.

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/304
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/305
- corrective-red: authorization https://github.com/PyAutoLabs/autolens_workspace_test/issues/304#issuecomment-5575042508

## What shipped
- `scripts/imaging/jax_grad/delaunay.py`: `rel_steps=(1e-8, 1e-7, 1e-6)` → `(1e-6, 2e-6, 3e-6, 1e-5, 3e-5)`; the tolerance comment rewritten with the measured noise floor, per-parameter clean windows and flip distances. `rtol=1e-2`, the mass/shear liveness assert and both #302 checks unchanged.

## Key traps / findings
- **The library was innocent.** The CI miss (index 10 `mass.ell_comps_0`, ad=-2849.63 vs fd=-2944.08, 3.3%) looked like a PyAutoArray#526 regression (Delaunay zeroed-ring rework in the window). Discriminator: AD matched CI to 1.7e-9 and was bit-identical under pre-#526 PyAutoArray (base LL, all 14 AD entries, every FD sample) — a library gradient bug cannot leave AD unchanged.
- **The measuring stick was the defect.** The Delaunay LL carries a ~1.0e-5 rms / 4.4e-5 ptp summation-order noise floor along the seven mesh-moving mass+shear parameters (present eagerly, so not XLA; curvature matrix cond 77). The old sweep put h in 1.1e-9..1.1e-7 on ell_comps_0 — inside round-off (the 1e-8 step returned the wrong sign). CI's FD is a fixed per-environment draw from that band (numpy 2.4 vs 2.2 summation order); local FD was deterministic and passed.
- **The dataset rebuild exposed it.** awt#294 (2026-09-06) shrank AD[10] ~4x at the same absolute noise: noise/signal 1.8% → 6.8%. The check had never run on the new data before #302 unblocked it.
- **Clean windows differ per parameter** because `h = rel_step · max(|x|, 0.1)`: ell_comps_0 (x=0.11) is clean for h in [1e-7, 3.4e-6], first flip at h=+1.13e-5 (101/617 simplices, LL jumps 3.24); einstein_radius (x=1.6) is clean only for h ≤ 4.8e-6 and flips at h=-8e-6 (LL jumps 3.21), so rel_steps 1e-5/3e-5 are flip-contaminated for it. A first tuple `(1e-7, 1e-6, 1e-5, 3e-5)` left einstein_radius at 8.7e-3 against rtol 1e-2; the hold-and-probe before commit produced the final five-step tuple (worst rel err 1.13e-3, einstein_radius 7.05e-4). A benign simplex re-labelling (459 rows, dLL on the linear trend) at h=+4.8e-6 is not a flip — judge by the LL jump, not the row count.
- **Positive control**: AD scaled by 1.05 fails `assert_gradients_match` at all 14 indices under the new sweep — the check stays falsifiable.
- **Stale dataset trap**: `should_simulate` keeps a full-resolution stale copy, so the main checkout still held the pre-#294 180x180 `dataset/imaging/jax_test`; verify `data.fits` shape before trusting a local run. The task worktree regenerated its own copy.
- Memory: `feedback_fd_sweep_noise_floor_on_mesh_moving_params`.

## Original prompt

# imaging/jax_grad/delaunay.py: FD step sweep sits in the round-off floor on mass.ell_comps_0 after the dataset rebuild

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-07
Issued: 2026-09-07

Original request (verbatim): "ok lets begin to work towards making heart get off red" — after
the integrate-only re-dispatch (PyAutoHeart run 34148543011) cleared five of the six 2026-09-07
failures, this script is the last one holding `release validation FAILED (stage integrate)`.

## Failure

Release Integrate run https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/34148543011
(TestPyPI 2026.9.7.1.dev75601; PyAutoArray bcd15cd9, PyAutoLens 9468e3e1, PyAutoFit 088013c1):

    scripts/imaging/jax_grad/delaunay.py  FAIL (65.2s)
    AssertionError: Autodiff vs finite-difference mismatch at parameter indices [10]:
    ad=[-2849.63049799], fd=[-2944.07821968], abs_err=[94.44772169], tolerance=[29.4408822]

Index 10 is `galaxies.lens.mass.ell_comps_0`; the other 13 parameters pass at rtol=1e-2. The
two preceding checks (mesh-callback constant folding, eager-vs-jit rtol=1e-6, both from #302)
pass. The check had never run on the rebuilt dataset (#294, 2026-09-06) until #302 unblocked it.

## Diagnosis (2026-09-07, Opus subagent, local source install at the CI SHAs; control lp.py PASS)

- Not the library. AD[10] matches CI to 1.7e-9 and is bit-identical under pre-#526 PyAutoArray
  (de92d09): base LL, all 14 AD entries and every FD sample identical. PyAutoArray#526 exonerated.
- The Delaunay LL carries a ~1.0e-5 rms / 4.4e-5 ptp summation-order noise floor on the seven
  mesh-moving mass/shear parameters (present eagerly too; curvature matrix cond 77, so not
  conditioning). The lens-light parameters do not move source vertices and match at 1e-10..1e-8.
- The script's sweep `rel_steps=(1e-8, 1e-7, 1e-6)` gives h = 1.1e-9..1.1e-7 on x[10]=0.113:
  1e-8 returns the wrong sign (+2756), 1e-7 is 10% off, 1e-6 sits at the noisy edge (band ±6.8%
  of AD[10] against rtol 1e-2). Clean plateau bracketing AD: h in [1e-7, 3.4e-6]. First triangle
  flip at h=+1.13e-5 (101/617 simplices rewire, LL jumps 3.24); no rewiring at any sweep step.
- The rebuild shrank AD[10] 4x (old data -11512 -> new -2850) at the same absolute noise, so
  noise/signal went 1.8% -> 6.8%. Only index 10 exceeds the tolerance band (next worst 1.65%).
- CI's FD is a fixed per-environment draw (numpy 2.4 summation order); local FD is deterministic
  (-2852.98, four runs) and passes. Seed 43 also passes, same signature.

## Fix

In `scripts/imaging/jax_grad/delaunay.py` change the sweep to `rel_steps=(1e-7, 1e-6, 1e-5, 3e-5)`
and rewrite the adjacent "Documented tolerance" comment with the measured numbers: valid FD window
h in [1e-7, 3.4e-6] on the mesh-moving parameters, first re-wiring at h=1.13e-5, noise floor
4.4e-5 ptp, noise band at 3e-5 = ±0.23% (FD -2852.86 vs AD -2849.63, 0.11%). Keep `rtol=1e-2`
and the mass/shear liveness assert. Do not add `skip_indices`; do not loosen the tolerance.

Acceptance: the script passes locally under the resolved release env (`ENV: jax full_datasets`,
cwd = workspace root, dataset/imaging/jax_test at 100x100 — `should_simulate` keeps a stale
180x180 copy, verify data.fits shape) with index 10 rel err < 3e-3 at the chosen step, and
`jax_grad/lp.py` still passes as the control. Then re-dispatch `release-integrate.yml` on
PyAutoHeart with testpypi_version=2026.9.7.1.dev75601 and this morning's commit_shas.

Diagnosis logs: session scratchpad `characterise_seed42.log`, `bigstep.log`, `flipcensus.log`,
`noisefloor_new.log`, `noisefloor_old.log`, `pre526_probe.log`.
