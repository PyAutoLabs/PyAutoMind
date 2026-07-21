# Smoke-profile 16x16: cap-not-unset for modeling + parity/pixelization overrides

Shipped 2026-07-21. Tier 1 build-honesty from the 2026-07-20 full local build sweep.

**autolens_workspace_test #186 (MERGED):** `multi/dataset_model_parity_delaunay` unset
PYAUTO_SMALL_DATASETS (full-res physics parity test); `jax_grad/imaging_pixelization` unset +
NEEDS_FIX-parked (override cleared the 256-vs-441 fault-mask, exposing a real "Gradient is all
zeros" bug, same family as imaging_mge; likely needs custom_jvp).

**autolens_workspace #297 (MERGED):** revised from env-unset to cap-not-unset —
`multi/features/imaging_and_point_source/modeling.py` caps the downloaded 200x200 RXJ1131 cutout
via `al.util.dataset.cap_array_2d_for_small_datasets` so it runs AT 16x16 (from_fits doesn't honor
the cap; Grid2D.uniform does → was a 200-vs-16 broadcast). Notebook regenerated.

Direction: move smoke/CI toward "PYAUTO_SMALL_DATASETS works everywhere", not per-script unset
overrides. Opened under the Heart-RED corrective-PR exception (reason: workspace validation not
passing, 10 failed).

## Original prompt

# Smoke-profile PYAUTO_SMALL_DATASETS overrides for 3 full-data scripts

Type: bug
Target: workspaces
Repos:
- autolens_workspace
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Three scripts fail in the faithful build (`PyAutoHands/autobuild/run_all.py`)
**only** under the smoke profile's `PYAUTO_SMALL_DATASETS=1` grid/mask cap — all
verified as env-config gaps, not code bugs, during the 2026-07-20 full local
sweep triage. Fix is the established idiom: add per-script `unset:
[PYAUTO_SMALL_DATASETS]` overrides in each workspace's
`config/build/env_vars.yaml`, mirroring the many existing full-data overrides
(e.g. `jax_grad/imaging_lp`, `multi/visualization_imaging`,
`interferometer/visualization.py`). Smoke-profile only; **no library source
changes; do not touch global defaults.**

Explicitly OUT OF SCOPE (do not touch here): `cluster/visualization.py` — it is
genuinely slow (>200s at full size) and then hits the pre-tracked #1280
tangential-critical-curve assert; leave it parked.

## The three overrides

1. **autolens_workspace_test** — `multi/dataset_model_parity_delaunay.py`:
   `SMALL_DATASETS`→16² breaks the Delaunay parity floor (0.2 tol meaningless on
   tiny grids). CONFIRMED passes at full size (A0=-1144.359, A1=-1144.384, all
   four agree). Add `unset: [PYAUTO_SMALL_DATASETS]`.

2. **autolens_workspace_test** — `jax_grad/imaging_pixelization.py`: its
   subprocess `jax_likelihood_functions/imaging/simulator.py` inherits the
   parent's env; under `SMALL_DATASETS=1` the simulator builds a slim array of
   256 (16²) against a 441 (21²) mask → `ArrayException`. Add `unset:
   [PYAUTO_SMALL_DATASETS]` for `jax_grad/imaging_pixelization` (mirror the
   existing `jax_grad/imaging_lp` / `imaging_mge` entries). VERIFY during
   implementation that the subprocess inherits the unset (it should, since
   subprocess.run inherits os.environ); if the subprocess re-injects the var,
   scrub it at the call site instead.

3. **autolens_workspace** — `multi/features/imaging_and_point_source/modeling.py`:
   `al.Grid2D.uniform(shape_native=data.shape_native)` is capped to 16² while
   `data.shape_native` stays 200² → broadcast error at
   `quasar_image_circles |= distances < quasar_mask_radius` (line ~161). Add
   `unset: [PYAUTO_SMALL_DATASETS]`. `PYAUTO_TEST_MODE=2` stays set (no real
   search), so full-size data construction should stay well within the cap.

## Verification

Re-run each affected script through the faithful build harness with its
workspace's `env_vars.yaml` applied (`run_python.py <project> <scripts/dir>`),
confirm PASS within the per-script timeout, and confirm no other script in the
same directory regressed. No notebook regeneration needed (config-only change).

<!-- filed 2026-07-20 from the full-local-build-sweep triage; Tier 1 of the
     build-honesty follow-ups. Sibling to the env-profile campaign
     (env_profile_migration_steps_4_to_8) but scoped to smoke-profile overrides
     only — coordinate with that task's step-6 profile rename. -->
