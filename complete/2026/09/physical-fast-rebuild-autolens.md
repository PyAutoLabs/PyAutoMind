# Physical + fast rebuild of the autolens_workspace_test smoke gate — coarser datasets, matched models, one pin wave

autolens_workspace_test#294 → `fd4e17f`, closing autolens_workspace_test#293,
merged 2026-09-06 on branch `claude/ci-test-timing-epic-ke2lul`; the
`fast-tests` epoch boundary landed as PyAutoHeart#212 → `6d5c1c4`. Phase 6 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`)
— the flagship repo, applying the phase-5 template plus the one regeneration of
this repo's absolute likelihood pins. Fable-planned on the issue from a
per-script inventory of all 27 gate entries (an Opus survey), implemented by an
Opus subagent in two passes plus an off-gate wave, from a web session (no task
worktree; the PyAutoLens stack installed from source in the container).

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/293
- completed: 2026-09-06
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/294
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/212

## What shipped

- **Coarser shared datasets, sized to what the models resolve**: imaging
  `jax_test`/`jax_test_dspl` 180×180 @0.2″ → 100×100 @0.3″ (PSF 11×11 σ0.35″,
  lens light 4.0/2.0 → 1.0/0.5 on sky 1.0; peak S/N 89, arcs 30); interferometer
  `simple` real-space 256×256 @0.1″ → 128×128 @0.2″; `multi_dataset/lens_sersic`
  150×150 @0.1″ → 80×80 @0.2″ plus a new `lens_sersic_light` dataset for the
  five scripts whose model carries a lens MGE; `build/imaging/with_lens_light`
  80×80 @0.2″ → 60×60 @0.3″ with a resolved source, an Isothermal truth and a
  noise seed.
- **Every gate model matches its data**: lens light in the imaging models that
  fit lens-light data (the 20-Gaussian MGE that was dead code in `mge.py` is now
  the lens light, replacing `NFWSph` + a fixed mass-to-light basis), shear
  wherever the truth has shear, priors whose medians are the simulated values,
  `ps.Point` for the point truth, the no-op over-sampling loop and the swapped
  `ell_comps` priors fixed. Mesh ≤ masked pixels applied against measured
  counts before the first run (28×28 → 20×20 on the gate; 15 off-gate meshes).
- **Levers, coverage preserved**: vmap `batch_size` 50 → 10, radial
  over-sampling `[4,2,2]` → `[2,2,1]`, the `delaunay_nn.py` timing block to one
  repeat. `smoke_tests.txt`, every `# ENV:` line, the profile, `no_run.yaml`,
  every tolerance, the composite multi-dataset vmap structure and its
  `XLA_FLAGS` workaround untouched.
- **The whole pin wave, once**: 9 gate literals + 25 off-gate scripts (23
  regenerated, 2 still hold), each re-run past its pin so the relational
  assertions were exercised; three gate pins are now positive (+717, +618,
  +1207) where they were −6.5e5, −6.7e8 and −1.3e9.
- **Measured**: 27/27 green before and after; 396.3 s → 321.9 s cold locally
  (−19%); CI runner step 8.5 min cold → 5.5 min warm per leg (legacy 9.2 min).
  The 67-file diff and the full write-up are on #294.

## Key traps / findings

- **Mesh ≤ masked pixels before the first run gave 27/27 first time** (phase 5:
  38/39). The sharper form is the *ratio*: the two `jax_grad` scripts satisfy
  the inequality (330 source px in 432 image px) and still regressed because
  their 1e-10 eager-vs-jit and 1% FD certifications are conditioning
  assertions. `regularization.py` was fixed by sizing its mesh from the mask
  (`pixels` 300 → 200; 130 under-resolves); `delaunay.py` could not be —
  five configurations, none passes both guards — and is filed.
- **An adapt image is an image-plane quantity.** Adapting to the *unlensed*
  true source gave NumPy a finite likelihood with a divide warning and JAX
  NaN (`_vmap` → −1e99). Ray-tracing the true source through the true lens is
  the right object; the backend divergence is filed for PyAutoArray.
- **A pin's magnitude is a diagnostic.** Two literals orders of magnitude out
  of line with their neighbours after the first pass were the only signal that
  two models were still at default priors; a second pass fixed both.
- **Re-running past the pin catches what a mechanical re-pin hides**: a +5%
  mass-sensitivity floor that stopped clearing because near-delta priors sat
  off truth (fixed), and `imaging/jax_likelihood/mge_group.py` whose source
  basis the positive-only solver zeroes on the coarser data (bit-identical
  likelihood under perturbation; two levers backed off; filed).
- **Dead code hides mismatches better than wrong code**: the discarded
  `mge_model_from` call and a `mask_radius` rebind after the mask was built
  both read as working code.
- **Dataset constants re-typed in every consumer** are why a resolution change
  touched 57 files; a shared module per family would make the sweep one edit.
- **Local is a faithful proxy for this repo but not for the user workspaces**:
  a probe for phase 8 ran the pixelization tutorials 4–6× slower locally than
  CI under the same env — phase 8's first task.

## Follow-ups (tracked, not started here)

- `draft/bug/autolens_workspace_test/mge_group_source_basis_zeroed_on_coarse_data.md`
- `draft/bug/autolens_workspace_test/jax_grad_delaunay_eager_jit_guard_float64_scatter.md`
- `draft/bug/autoarray/jax_delaunay_returns_more_than_five_values.md` (pre-existing on `main`)
- `draft/bug/autoarray/mapper_adapt_zero_signal_jax_nan.md`
- Hot-vs-cold cache numbers for both `_test` repos from `timings/scripts/`
  now that each has had a cold and a warm run (the first `fast-tests`-epoch
  rows land with the next daily heart-health run).
- Phase 8: `draft/test/workspaces/user_workspace_howto_slow_script_pass.md`.

## Original prompt

# autolens_workspace_test physical + fast rebuild (flagship)

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 6
Issued: 2026-09-06

autolens_workspace_test physical + fast rebuild (flagship repo; applies the phase-5 template).

Same one-wave realism+speed rebuild as phase 5, on the 26 smoke-gate entries (158 scripts
total, 92 carrying `# ENV:` declarations). Known concrete defects from the 2026-08-31
survey to fix (and sweep siblings for the same patterns):

- `imaging/jax_likelihood/mge.py`: dataset simulated with elliptical Isothermal+shear lens
  (Sersic+Exp light) but fitted with NFWSph mass + fixed mass_to_light_ratio=10.0
  GaussianGradient basis — structurally mismatched, pinned at a low-likelihood
  prior-median point (pin -86283.10 at line ~248). Rebuild as a consistent, physical,
  high-likelihood setup.
- `imaging/model_fit.py`: fits DevVaucouleursSph + IsothermalSph (no shear) against
  `with_lens_light.py`'s sim of elliptical PowerLaw slope=1.8 + shear; sim source
  ExponentialSph r_eff=0.1" is barely resolved at 0.2".
- `imaging/simulator/simple.py`: lens light intensity 4.0 / sersic_index 3.0 + Exp 2.0 on
  background_sky_level=1.0 — implausibly bright vs the "HST-representative" claim; pixel
  scales in the repo: 0.2 (58x), 0.1 (52x), 0.05 (11x), 0.3 (4x) — move the default test
  resolution coarser (0.3" still just resolves a lens) wherever coverage allows.
- multi_dataset sim is the closest to consistent (shared SIE, per-band Sersic source) —
  use it as the in-repo reference pattern.

Same constraints as phase 5: one pin-regeneration wave at the end; preserve the Eigen-pool
bug-class coverage in `multi_dataset/jax_likelihood/*` (delaunay_mge still hangs
intermittently WITH the flag — do not alter its reproduction conditions without recording
it in the jax-compile-stall epic ledger); unit tests + developer/profiling workspaces
validate; before/after per-script seconds against the phase-4 legacy snapshot. The 900s
`jax_grad/` cap class (measured 41-568s) is in scope — it is the largest single wall-clock
block on the gate.
