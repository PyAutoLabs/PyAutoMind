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
