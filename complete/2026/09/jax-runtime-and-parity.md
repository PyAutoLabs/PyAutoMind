# jax-runtime-and-parity — release JAX runtime compatibility + likelihood parity

**Date:** 2026-09-17
**Issue:** [autolens_workspace_test#317](https://github.com/PyAutoLabs/autolens_workspace_test/issues/317) (closed)
**PRs:** [autolens_workspace_test#320](https://github.com/PyAutoLabs/autolens_workspace_test/pull/320) (merged `3b34b22`), [autogalaxy_workspace_test#122](https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/122) (merged `e8b2f38`)
**Outcome:** defect refuted twice; one smoke-gate residue fixed; **no library code changed**.

## What this task was

Release run `28784914443` (2026-07-06) reported six `jax_likelihood` scripts failing on the
release stack — TensorFlow Probability importing the removed `jax.interpreters.xla.pytype_aval_mappings`
and NumPy-vs-JAX likelihood mismatches — across `autogalaxy_workspace_test` (imaging /
interferometer / multi_dataset `delaunay_mge.py`) and `autolens_workspace_test` (interferometer
`delaunay_mge.py`, multi_dataset `rectangular.py` / `rectangular_mge.py`). The prompt prescribed a
library-side repair (fix or replace the TFP path, chase parity through inversion and
regularization, add library regression tests). Sized `too-large`, `Autonomy: supervised`,
`Consequence: judge`.

## What was actually done

Reproduction-gated, on the same method that closed the siblings PyAutoFit#1508
(`autofit-sampler-database`) and PyAutoArray#467: every script from a moved-aside `output/`,
env resolved by `autohands.env_config.build_env_for_script` under the workspace's
`config/build/profile_release.yaml`, `PYAUTO_TEST_MODE=0`, one fresh process each, 1800 s cap.

**Gate 1 — 2026-08-21:** 6/6 PASS on the exact parity assertions (libraries at PyAutoFit
`248ca971f`, PyAutoArray `b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`).
Four of the six were then still parked SLOW for an *intermittent* release-cap timeout, so the
prompt stayed open: one green run cannot clear an intermittent hang.

**Gate 2 — 2026-09-15:** 6/6 PASS again (PyAutoFit `27d41e7c8`, PyAutoArray `5e2bc0f4`,
PyAutoGalaxy `840ffde0`, PyAutoLens `ccf9295f3`, PyAutoNerves `fac8b17`; Python 3.12.10).
Every NumPy-vs-JIT pair agrees to ~1e-10 relative against script `rtol`s of 1e-4 / 1e-2; the
string `pytype_aval_mappings` appears in no log. Timings 17–92 s.

| Package | Version |
|---|---|
| jax / jaxlib | 0.10.2 / 0.10.2 |
| numpy | 2.2.6 |
| nufftax | 0.6.1 |
| pynufft | 2025.1.1 |
| tensorflow-probability | 0.25.0 |
| numba / scipy | 0.62.1 / 1.17.1 |

By gate 2 the blocker had moved: none of the six was in either `no_run.yaml` any more
(PyAutoFit#1528 restored the family on 2026-08-27), so re-validation is automatic on every
release pass — the same ground on which the siblings were closed.

## The one real residue, fixed

Both `smoke_tests.txt` files still carried
`# imaging/jax_likelihood/delaunay_mge.py  # disabled: jax 0.7 removed jax.interpreters.xla.pytype_aval_mappings — see PyAutoPrompt/autohands/smoke_workspace_fixes.md`,
pointing at a file that no longer exists anywhere. Measured under `profile_smoke.yaml`, three
cold-XLA-compile repeats each (no persistent JAX compilation cache is configured, so every repeat
is a genuine cold compile): autogalaxy 68.1 / 70.7 / 71.1 s, autolens 62.1 / 58.7 / 53.3 s against
the 300 s cap. The two PRs drop the stale line and add the entry beside
`imaging/jax_likelihood/delaunay.py` with a dated promotion comment (the #296 pattern). Both
`workspace-smoke` legs (3.12, 3.13) ran green with the entry executing.

## What this does NOT establish

1. **The intermittent 1805 s hangs are untouched.** They are a different failure (XLA
   FftThunk/ducc0 Eigen-pool deadlock under `--xla_cpu_multi_thread_eigen=false`) on *other*
   `jax_likelihood` scripts, owned by the `xla-cpu-eigen-pool-deadlock` epic. Nothing here
   lifts a `no_run.yaml` parking.
2. Both gates were **source-tree** runs, not the TestPyPI wheels a release run installs.
3. Prompt item 5 ("add library regression tests") was declared **out of scope**: the six
   workspace_test scripts *are* the regression tests and run in every smoke / weekly / release
   pass; a jit-vs-NumPy parity unit-test layer would be a feature, not a fix for a refuted defect.

## Incidental findings (not fixed, no issue filed)

- `autoarray/inversion/regularization/matern_kernel.py` lazily imports
  `tensorflow_probability.substrates.jax` for `bessel_kve`; every Matern-using script emits 20
  identical protobuf gencode-version `UserWarning`s. Log noise, but a lazily-imported dependency
  on the pixelized path — `/hygiene` if wanted.
- Four docstrings still cite the jax 0.7 `pytype_aval_mappings` removal as a live hazard:
  `autogalaxy_workspace_test/scripts/{imaging,interferometer,multi_dataset}/jax_likelihood/delaunay_mge.py`
  and `misc/jax_assertions/matern_regularization.py`. Stale prose.

## Session notes

- The feature commits were pushed from the CLI worktree on 2026-09-15; the PRs were opened,
  merged and closed out from a web session on 2026-09-17 (Mind state carried the handoff).
- The autolens branch was two commits behind `main` (#319) at merge; a trial merge showed no
  conflict, so it was merged as is.
- Worktree `~/Code/PyAutoLabs-wt/jax-runtime-and-parity` is on the laptop and could not be
  removed from the web surface — `worktree_remove jax-runtime-and-parity` there.

## Original prompt

# Fix release JAX runtime compatibility and likelihood parity

Type: bug
Target: health_fixes
Themes:
- release
- ci-smoke
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Issued: 2026-09-15
Filed: 2026-07-06 (backfilled from git)

## 2026-08-09 — EVERY SCRIPT PATH BELOW IS STALE (they moved, they were not deleted)

Checked by the draft/ sweep. All 6 scripts named in § Scripts return **404** at the
paths written below, and **all 6 still exist** under a renamed layout. Do not read the
404s as "the scripts were deleted" or "this was fixed by removal".

Two systematic renames landed in both test workspaces since this prompt was filed:

```
scripts/jax_likelihood_functions/<dataset>/X.py  ->  scripts/<dataset>/jax_likelihood/X.py
scripts/<dataset>/modeling_visualization_jit.py  ->  scripts/<dataset>/visualization/modeling_visualization_jit.py
scripts/multi/...                                ->  scripts/multi_dataset/...
```

Verified in `autolens_workspace_test` (`4cea3f8c`, cloned) and
`autogalaxy_workspace_test` (raw, every path resolves 200). This is the **same rename
family** that cost a previous session time on
`draft/bug/autolens/jax_point_source_point_smoke_sentinel.md` — treat a 404 in this
cluster as path drift until proven otherwise.

Corrected paths:

| named in § Scripts | actual path on main | repo |
|---|---|---|
| `…/jax_likelihood_functions/imaging/delaunay_mge.py` | `scripts/imaging/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/interferometer/delaunay_mge.py` | `scripts/interferometer/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/multi/delaunay_mge.py` | `scripts/multi_dataset/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/interferometer/delaunay_mge.py` | `scripts/interferometer/jax_likelihood/delaunay_mge.py` | autolens_workspace_test |
| `…/jax_likelihood_functions/multi/rectangular.py` | `scripts/multi_dataset/jax_likelihood/rectangular.py` | autolens_workspace_test |
| `…/jax_likelihood_functions/multi/rectangular_mge.py` | `scripts/multi_dataset/jax_likelihood/rectangular_mge.py` | autolens_workspace_test |

### Parking state — read before assuming CI still exercises these

**4 of the 6 are parked SLOW**, all dated 2026-07-14 and all citing PyAutoHeart#74
(flaking at the 1800s `mode=release` cap):

- `autogalaxy_workspace_test` `no_run.yaml`: `imaging/jax_likelihood/delaunay_mge.py`,
  `interferometer/jax_likelihood/delaunay_mge.py`, `multi_dataset/jax_likelihood/delaunay_mge`
- `autolens_workspace_test` `no_run.yaml`: `interferometer/jax_likelihood/delaunay_mge.py`

The two `multi_dataset/jax_likelihood/rectangular*.py` scripts are **not** parked.

Also note `autolens_workspace_test` parks `multi_dataset/jax_likelihood/delaunay.py`
as `NEEDS_FIX 2026-08-01 - hangs to the 1800s release cap in 3 of 5 release-integrate
runs` — a sibling in the same family, filed after this prompt, suggesting the JAX
likelihood timeout story has moved on independently of this prompt.

**This changes what the prompt's premise means.** A parked script cannot fail in
release validation, so the 2026-08-07 release drive's Stage 3 result (51/51 jobs green,
`657p/0f/101s/0t` — note the **101 skips**) is *not* evidence these were fixed. Nothing
here is graded shipped; the failures are simply no longer being provoked. Note too that
the parkings are for **timeouts**, a different failure from the defect this prompt
describes — so unparking is a precondition for reproducing it at all.

Not re-graded here: whether the underlying defect still reproduces. That needs real
runs, which a cloud session cannot do.

---
## Context

Six JAX likelihood scripts failed with the rehearsed release stack. CI included
TensorFlow Probability using removed JAX internals and NumPy/JAX likelihood mismatches.
All six passed locally with current `main` and JAX 0.9.2, so verify whether upstream
library changes already fixed them or whether environment/order sensitivity remains.

Owners: @PyAutoArray, @PyAutoFit, @PyAutoGalaxy, @PyAutoLens,
@autogalaxy_workspace_test, and @autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/imaging/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/multi/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular_mge.py`

## Required work

1. Reproduce in a clean source environment using the release dependency constraints and
   record exact JAX, jaxlib, TFP, NumPy, nufftax, and pynufft versions.
2. Confirm whether current `main` fixes every CI traceback without cached compiled state.
3. If TFP remains incompatible, fix or replace the owning library path rather than
   disabling JAX in JAX-specific scripts.
4. Investigate parity differences from data/model construction through inversion and
   regularization; do not merely loosen tolerances without a numerical error budget.
5. Add library regression tests and rerun all six scripts in both fresh processes and
   their normal directory sequence.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## 2026-08-21 — REPRODUCTION GATE RUN: **6/6 PASS**

Method (identical to the gate that closed the sibling `autofit_sampler_database`, PyAutoFit#1508):
every script run from a **cleared** `output/`, under its workspace's
`config/build/profile_release.yaml`, env resolved by `autohands.env_config.build_env_for_script`
at workspace CWD, 1800s `mode=release` cap. Libraries at `main`: PyAutoFit `248ca971f`,
PyAutoArray `b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`, PyAutoNerves `f6d6d52`.
Three workspace checkouts were **behind `origin/main`** and were synced first.

| Script (resolved path) | Result | Secs |
|---|---|--:|
| `autolens_workspace_test` `multi_dataset/jax_likelihood/rectangular.py` | PASS | 31 |
| `autolens_workspace_test` `multi_dataset/jax_likelihood/rectangular_mge.py` | PASS | 32 |
| `autolens_workspace_test` `interferometer/jax_likelihood/delaunay_mge.py` *(parked)* | PASS | 95 |
| `autogalaxy_workspace_test` `imaging/jax_likelihood/delaunay_mge.py` *(parked)* | PASS | 72 |
| `autogalaxy_workspace_test` `interferometer/jax_likelihood/delaunay_mge.py` *(parked)* | PASS | 66 |
| `autogalaxy_workspace_test` `multi_dataset/jax_likelihood/delaunay_mge.py` *(parked)* | PASS | 46 |

All six at `PYAUTO_TEST_MODE=0` (real full searches). The passes are on **the exact assertion this
prompt is about**, not merely exit 0:

```
NumPy log_likelihood_function: 12448.66325394023
JIT   log_likelihood_function: 12448.663253713981
PASS: jit(log_likelihood_function) round-trip matches NumPy scalar.
PASS: TransformerNUFFT cross-check matches TransformerDFT.
```

**The defect claim (TFP using removed JAX internals; NumPy/JAX likelihood mismatch) is refuted.**

**The parkings are NOT refuted, and must not be lifted on this evidence.** All four parked entries
describe an *intermittent* failure ("flakes at the 1800s cap"; the sibling NEEDS_FIX entries name an
"intermittent XLA compile stall … passes ~19s otherwise"). One green run each is exactly what those
notes predict, so it is consistent with them rather than contrary to them. Unparking needs repeated
runs; a single sample cannot clear an intermittent hang.

### Script-path corrections (three renames, verified on disk 2026-08-21)

The tables in this folder have drifted **again** since the 2026-08-09 sweep. All paths resolve;
a 404 here still means drift, never deletion.

- `scripts/jax_likelihood_functions/<dataset>/X.py` -> `scripts/<dataset>/jax_likelihood/X.py`
- `scripts/<dataset>/modeling_visualization_jit.py` -> `scripts/<dataset>/visualization/modeling_visualization_jit.py`
- `scripts/multi/...` -> `scripts/multi_dataset/...`  (this one bit `slam/simultaneous.py`, still
  listed under `multi/` above)
- `double_einstein_ring` -> `double_source_plane_lens`  (autolens_workspace#394) — so
  `imaging/features/advanced/double_einstein_ring/chaining.py` is now
  `imaging/features/advanced/double_source_plane_lens/chaining.py`
