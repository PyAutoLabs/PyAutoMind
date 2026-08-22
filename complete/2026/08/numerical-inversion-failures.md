# numerical-inversion-failures — release-run non-positive-definite inversion failures

**Date:** 2026-08-22
**Issue:** [PyAutoArray#467](https://github.com/PyAutoLabs/PyAutoArray/issues/467) (closed)
**PRs:** none — **no code was changed in any repo**
**Outcome:** investigated to a definitive verdict; no defect exists to fix.

## What this task was

Release run `28784914443` (PyAutoHeart#27, the first real release-profile validation) reported 42
script failures, split across seven prompts in `PyAutoMind/draft/bug/health_fixes/`. This task owned
two, both alleging `LinAlgError`-class failures from non-positive-definite matrices in inversion
paths:

- `autolens_workspace_test/scripts/interferometer/model_fit.py`
- `autogalaxy_workspace/scripts/interferometer/features/pixelization/galaxy_reconstruction.py`

The prompt asserted the autolens leg "reproduces on current `main`" and prescribed a five-step
repair: capture curvature/regularization matrix properties at failure, localise the defect between
sampled parameters, regularization construction, numerical stabilization or an underdetermined
script model, then fix the owning library.

Brain sized it `too-large` (score 16), fix-locus "library source", strategy "split into phases".

## What was actually done

Not started as the prescribed repair. The premise was gated first, for the same reason its sibling
`autofit_sampler_database` was: the claim was six weeks old, and the cluster around it had already
produced two independent findings that it had aged out.

Both scripts were re-run on current `main` from a **cleared** `output/`, under each workspace's
`config/build/profile_release.yaml`, env resolved by `autohands.env_config.build_env_for_script` at
workspace CWD, 1800s `mode=release` cap. Libraries at `main`: PyAutoFit `248ca971f`, PyAutoArray
`b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`, PyAutoNerves `f6d6d52`. Three workspace
checkouts were behind `origin/main` and were synced first.

## Result: 0 / 2 reproduce

| Script | Result | Secs |
|---|---|--:|
| `autolens_workspace_test/scripts/interferometer/model_fit.py` | PASS | 78 |
| `autogalaxy_workspace/scripts/interferometer/features/pixelization/galaxy_reconstruction.py` | PASS | 70 |

No non-positive-definite failure and no `LinAlgError` in either. The prompt's specific claim that the
autolens leg reproduces on `main` is false.

## Why this verdict is strong: two prior independent refutations of the same hypothesis

This is not a lone green run. The same hypothesis — that PyAuto's inversion path produces
non-positive-definite curvature/regularization matrices — had already been tested and refuted twice:

1. **`complete/2026/07/pix-inversion-not-positive-definite.md`** (2026-07-21) investigated a
   six-marker `LinAlgError: matrix not positive definite / singular` cluster across
   autogalaxy_workspace + HowToGalaxy. Outcome **inverted**: all six markers were stale and **no code
   was fixed**. The pix `LinAlgError` had been cured on 2026-04-10 — the same day the markers were
   filed — by PyAutoArray's `GaussianKernel` PD-guarantee `f1817af0` (symmetrise + trace-scaled
   diagonal jitter). Evidence was a 40-draw numpy inversion A/B across the full `GaussianKernel`
   LogUniform prior (coeff/scale `1e-6`..`~5e5`): **0 raises / 0 non-finite** on both `cholesky` and
   `slogdet`.
2. **`complete/2026/08/autofit-sampler-database.md`** (PyAutoFit#1508, 2026-08-21) — the sibling from
   this same release run, **0/9 reproduce**, closed with no code change.

A PD-guarantee landed in the owning library four months ago, was independently verified by direct
matrix probing, and both of this prompt's scripts now pass. The defect described here does not exist
on `main`.

## Why the issue was closed rather than parked open

The same test the sibling applied, and it passes here: **neither script is parked.** Checked against
`main` on 2026-08-22 —

- `autogalaxy_workspace/config/build/no_run.yaml` — 8 entries, none matching
  `interferometer/features/pixelization/galaxy_reconstruction` (GUI scripts, fits/png_make,
  search-viz, and one SLOW shapelets entry).
- `autolens_workspace_test/config/build/no_run.yaml` — no `interferometer/model_fit` entry. It
  appears only as a *consumer* on line 62, where `interferometer/simulator/with_lens_light.py` is
  marked `BOOTSTRAP-TARGET` because it produces `model_fit`'s dataset — which confirms `model_fit`
  itself runs.

So both scripts re-execute under exactly this profile in **every** `mode=release` pass. Re-validation
is automatic; a surviving defect fails the next release run loudly and earns a fresh issue with fresh
evidence. There is no human reminder to lose — the same reasoning that closed PyAutoFit#1508, and the
reason this prompt closes while `samples_parameter_paths` (#1327) stays parked.

This is now the **fourth** independent finding that this cluster aged out. The consistent explanation
across all of them is the one #1327 reached: stale cached `output/` in the 2026-07 release run,
against libraries that have since absorbed dozens of fixes.

## What this does NOT establish

1. **The autolens leg ran on numpy, not JAX.** `autolens_workspace_test`'s release profile *defaults*
   `PYAUTO_DISABLE_JAX="1"`; scripts opt back in with an in-file `ENV: jax` declaration, and
   `model_fit.py` carries none. That is release-faithful — it is what the release run itself executes
   — but JAX-on and JAX-off are different numerical code paths, and this refutation covers only the
   numpy one. A JAX-only inversion conditioning defect would not appear here.
2. **These were source-tree runs**, not the TestPyPI wheels the release run installed. A wheel-only
   packaging defect would not show.

## Incidental finding — filed as its own prompt

`galaxy_reconstruction.py` passes while emitting 4x `RuntimeWarning: invalid value encountered in
sqrt` from `PyAutoArray/autoarray/inversion/inversion/abstract.py:859`. **This looks exactly like
evidence for the prompt's hypothesis and is not** — it is a separate, unconditional defect:

```python
@property
def reconstruction_noise_map_with_covariance(self) -> np.ndarray:
    return np.sqrt(np.linalg.inv(self.curvature_reg_matrix))
```

`sqrt` is applied **elementwise to the whole inverse matrix**, whose off-diagonal entries are
covariances and are generally negative — so those entries are NaN *by construction*, for any input
matrix, however well-conditioned. It is not a conditioning symptom and does not rescue the prompt.

Confirmed still present on PyAutoArray `main` @ `a6b07cd` (2026-08-22). The 1D
`reconstruction_noise_map` is unaffected — it takes the diagonal, and elementwise-sqrt commutes with
taking the diagonal — so the science path is correct; only the covariance-aware consumer and the
warning spam are hit.

Filed as **`draft/bug/autoarray/reconstruction_noise_map_covariance_sqrt.md`**, not fixed here: the
correct off-diagonal semantics are an API/science decision, and the fix has a real trap (the 1D
science path is derived from this property's diagonal, so a naive change silently converts a
standard-deviation into a variance).


**2026-08-22 follow-up — the incidental finding got bigger.** Research into *why* source-reconstruction
noise maps have been unreliable found the sqrt bug is **not** the cause: `np.sqrt` is elementwise, so it
commutes with taking the diagonal and provably cannot reach the 1D noise map. Three deeper defects were
found in the same property, and split into a second prompt,
`draft/bug/autoarray/reconstruction_noise_map_solver_mismatch.md`:

1. **Estimator mismatch (the big one).** `inv(curvature_reg_matrix)` is the posterior covariance of the
   *unconstrained* Warren & Dye solve. But `use_positive_only_solver: true` is the shipped default, so the
   reconstruction is an NNLS active-set solve. Imposing `s >= 0` truncates the posterior, so the reported
   noise is overstated near the boundary and meaningless for pinned pixels — and a compact lensed source
   pins a large fraction of the mesh at zero, so the formula is worst exactly where it is most used.
2. **Edge-zeroed pixels ignored.** `use_edge_zeroed_pixels: true` is also default; the reconstruction
   solves on `zeroed_ids_to_keep` and scatters back zeros, while the noise map inverts the *full* matrix —
   re-admitting the poorly-constrained boundary vertices the zeroing exists to remove.
3. ~~**`use_edge_zeroed_pixels` is nested inside the positive-only branch**~~ — **withdrawn
   2026-08-22: this is intended behaviour, confirmed by the author, not a defect.** The control-flow
   description was accurate; calling it a bug was not.

Corroboration for the numerics half: `abstract.py:805` already documents `~1e-6` evidence round-off from
"factorizing the explicitly formed inverse" at `cond(C) ~ 1e9` on clustered traced mesh vertices — applied
to the log-det, never to the noise map. And `inversion_plots.py:395` already wraps the noise map in
`except np.linalg.LinAlgError`, writing NaN to the CSV: a guard that exists because this fails in practice.

## Follow-on state of the cluster

`draft/bug/health_fixes/README.md` row struck through. Of the original seven prompts: two shipped or
closed with code (`aggregator_output_contracts`), two closed as refuted with no code change
(`autofit_sampler_database`, this one), one parked not-reproducing (`samples_parameter_paths`,
#1327), and three remain in `draft/` with dated gate annotations
(`jax_runtime_and_parity`, `jit_visualization_outputs`, `release_timeout_policy`) — those are *not*
complete, because their SLOW/NEEDS_FIX parkings describe *intermittent* failures that a single green
run cannot clear.

## Original prompt

# Fix release-profile numerical inversion failures

Type: bug
Target: health_fixes
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## Context

Two interferometer scripts fail in inversion paths with non-positive-definite matrices.
The Autolens test failure reproduces on current `main`; the Autogalaxy script passed in a
stateful local checkout and needs a clean confirmation.

Owners: @PyAutoArray, @PyAutoGalaxy, @PyAutoLens, @autogalaxy_workspace, and
@autolens_workspace_test.

## Scripts

- `autogalaxy_workspace/scripts/interferometer/features/pixelization/galaxy_reconstruction.py`
- `autolens_workspace_test/scripts/interferometer/model_fit.py`

## Required work

1. Reproduce in clean output/worktrees with deterministic seeds and release settings.
2. Capture the curvature and regularization matrix properties at failure: symmetry,
   conditioning, eigenvalue range, dtype, backend, and mapper configuration.
3. Identify whether the defect is invalid sampled parameters, regularization construction,
   numerical stabilization, or a script model that permits an undefined inversion.
4. Fix the owning library for valid inputs. Do not catch `LinAlgError` or alter the script
   to hide a genuine inversion failure.
5. Add numerical regression tests and rerun both scripts repeatedly under the profile.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## 2026-08-21 — REPRODUCTION GATE RUN: **2/2 PASS — prompt refuted**

Method (identical to the gate that closed the sibling `autofit_sampler_database`, PyAutoFit#1508):
every script run from a **cleared** `output/`, under its workspace's
`config/build/profile_release.yaml`, env resolved by `autohands.env_config.build_env_for_script`
at workspace CWD, 1800s `mode=release` cap. Libraries at `main`: PyAutoFit `248ca971f`,
PyAutoArray `b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`, PyAutoNerves `f6d6d52`.
Three workspace checkouts were **behind `origin/main`** and were synced first.

| Script | Result | Secs |
|---|---|--:|
| `autolens_workspace_test/scripts/interferometer/model_fit.py` | PASS | 78 |
| `autogalaxy_workspace/scripts/interferometer/features/pixelization/galaxy_reconstruction.py` | PASS | 70 |

The prompt states the autolens leg "reproduces on current `main`". It does not. No
non-positive-definite failure, no `LinAlgError`, in either.

**Note which numerical path each took.** `autolens_workspace_test`'s release profile *defaults*
`PYAUTO_DISABLE_JAX="1"`, and scripts opt back in with an in-file `ENV: jax` declaration.
`model_fit.py` has no such declaration, so it ran on **numpy** — release-faithful, but worth
knowing for a claim about inversion numerics, since JAX-on and JAX-off are different code paths.

### Incidental finding — a real defect, but NOT this prompt's

`galaxy_reconstruction.py` passes while emitting 4x
`RuntimeWarning: invalid value encountered in sqrt` from
`PyAutoArray/autoarray/inversion/inversion/abstract.py:859`:

```python
def reconstruction_noise_map_with_covariance(self):
    return np.sqrt(np.linalg.inv(self.curvature_reg_matrix))
```

`sqrt` is applied **elementwise to the whole inverse matrix**, whose off-diagonal entries are
covariances and are generally negative — so those entries are NaN *by construction*, for any
matrix, however well-conditioned.

**This is not evidence of a non-positive-definite matrix** and does not rescue the prompt's
hypothesis, despite looking exactly like it would. It is a separate defect: a property whose
docstring promises a matrix that "accounts for the covariance of the noise between pixels" returns
NaN wherever that covariance is negative. The 1D `reconstruction_noise_map` is unaffected — it
takes the diagonal, and `diag(sqrt(M)) == sqrt(diag(M))` — so the science path is correct; only
the covariance-aware consumer and the warning spam are hit. Worth its own PyAutoArray prompt.
