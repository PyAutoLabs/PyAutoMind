# interferometer-mesh-numba-p2

- Repo: autolens_profiling (workspace-only)
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/332 (closed by the merge)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/333 (MERGED, merge commit `f075a6c5`, head `9a4981d`, 2026-09-27; lint green, the only check)
- Epic: interferometer-likelihood-campaign — phase 2 of `draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`
- Folds in the retired `interferometer_sparse_cache_after_measurement.md` (cached_property counter).

## What shipped

Phase 2 of the interferometer mesh numba-CPU campaign: the in-situ numba-vs-FFT
crossover, the CPU lever arms, the cached_property counter fold-in and RAL CPU rows.

- **Crossover on the cached library:** Delaunay nnz/col ~66-67, rectangular ~72-73.
  Bracketing cells: Delaunay r5.0 0.886 / r6.0 1.169; rect r4.25 0.749 / r5.0 1.225
  (numba/FFT time ratio).
- **Gate:** the current gate 60 routes every measured cell to the right path; the
  single-gate minimax is ~70 (retune filed as a draft, below).
- **Caching fix confirmed on RAL:** 0.5-0.6x at alma / alma_high (RAL jobs
  358985 / 358986 / 359000).
- **alma baseline:** numba 1.26 s vs FFT 2.59 s (Delaunay); 1.83 s vs 2.94 s (rect).
- **Lever ranking:** fnnls memo guard, gate retune, prange load balance, rect
  edge-zeroed log-det Cholesky miss.
- **Not levers:** marshalling, the MGE+mesh route, FFT size (already drafted).

## Caveat

The phase-1 alma N-sweep rows remain on the **uncached** library; phase 4's decision
matrix must not mix them with the cached-library crossover without a note.

## Follow-ups filed

- `draft/research/autolens_profiling/interferometer_nnls_memo_scattered_stream_guard.md`
- `draft/feature/autoarray/interferometer_numba_gate_retune_70.md`
- `draft/feature/autoarray/interferometer_direct_conv_prange_load_balance.md`
- `draft/feature/autoarray/edge_zeroed_log_det_cholesky_reuse.md`

Campaign next: phase 3 (A100 mask-radius sweep), then phase 4 (decision matrix).
RAL worktrees `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-numba-p{1,2}`
left in place for phase 3 dataset reuse.

## Heart ack carried from the active.md row

- heart-ack: "2026-09-27 YELLOW acknowledged by the human ('approve you to continue', same set as #328/#582, none touch autolens_profiling): manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source"

## Original prompt

# Interferometer likelihood campaign 3/3 — phase 2: numba vs FFT CPU crossover + CPU lever list

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- numba-cpu
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: for each mesh (Delaunay-1500, rectangular 39²) the numba / NumPy-FFT full-call ratio from the RAL CPU crossover rows crosses 1 between two measured alma mask radii (one row < 1, the next > 1), each row recording nnz/col and masked pixels; and every RAL CPU numba row on PyAutoArray main >= e281abf3 reads `evaluations_per_figure_of_merit` {1, 1} with the sma prior-median figure of merit unchanged against the pins -3162.627234657415 (Delaunay) / -3168.595092417778 (rectangular).
Review-minutes: 8
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27
Issued: 2026-09-27
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/332
Campaign: draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md

Phase 2 of the campaign prompt above (retained in `draft/` as the campaign intent; its
campaign contract and #235 discipline govern). Plan approved by the human 2026-09-27. Folds in
`draft/research/autolens_profiling/interferometer_sparse_cache_after_measurement.md` (retired
on filing; its content is carried verbatim under "Folded in" below).

## Context

Phase 1 (autolens_profiling#328, `ea2711d9`) landed the library-dispatch harness
`scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py` with `--mask-radius`, and
RAL CPU rows at r3.5: numba / FFT full-call ratio 0.25 sma Delaunay (nnz/col 6.2), 0.47 alma
Delaunay (29.1), 0.62 alma rect (40.4), 1.52 alma_high Delaunay (117.6), 2.05 alma_high rect
(161.9). Since then PyAutoArray#582 (main `e281abf3`) made `curvature_matrix` / `data_vector`
`cached_property`s on the sparse inversions: in phase 1 every NumPy `figure_of_merit` evaluated
F and D twice (the reconstruction and `fast_chi_squared`), so both arms' full calls drop and the
ratios shift. The phase-1 harness counter wraps `property.fget`, which breaks on the autonerves
`CachedProperty` (it has `.func`, no `.fget`).

From the phase-1 F-alone sub-rows, numba F scales as nnz x masked pixels and FFT F as the
extent area, so at a fixed pixel scale the F ratio scales with nnz/col alone: predicted
crossover nnz/col ~70 (Delaunay, ~r5.4 at alma) and ~71 (rect, ~r4.6) — above the packaged
gate 60.0, near the #226 rect ~77. The sweep measures it.

## What

1. **Counter fix (fold-in)** — the `cached_property`-aware call counter (diff below) plus a
   unit test; the F-alone / D-alone sub-rows pop the cached value before each repeat so they
   time the computation, not a dict lookup.
2. **Crossover sweep** — numba vs NumPy FFT, both meshes, alma at r2.0 / 3.5 / 5.0 plus the
   radii that bracket the measured crossover (chosen from a 2-3 instance laptop calibration
   probe on the cached code; candidates r4.25 / r6.0), alma_high r3.5 and sma r3.5 (the
   fold-in's re-run). Every row records nnz/col (re-derived in situ, incl. rect), masked
   pixels, extent, and the phase-1 row it replaces (`previous_row`) for the before/after
   delta. The adapt image is the May-18 `lensed_source.fits` cache (md5 recorded; a missing
   cache at a non-preset radius is a hard error, never a silent regeneration).
3. **CPU lever arms** (separate RAL job, alma r3.5 both meshes, headline rows untouched):
   `prange` kernel at `NUMBA_NUM_THREADS` 1 / 2 / 4 (F alone + implied full call), fnnls
   warm-start memo on vs off on the iid stream and a local-walk stream, Cholesky-reuse check
   (reused log-det vs a fresh dense Cholesky: time + agreement), `kernel_index_arrays`
   marshalling split into its instance-independent part (extent index) vs the per-instance
   CSR / CSC build. MGE+mesh numba route: static read only (never routed), in the lever list.
4. **RAL CPU submits** (`gpu` partition, no `--gres`, 1 thread pinned except the lever job's
   declared numba pool) with WALL-BASIS rows; `check_submits.py --check` green.
5. **Notes (after the RAL rows land)** — new in-situ crossover section in
   `results/notes/numba_interferometer_verdict.md` (confirm 60 / ~77 or file the PyAutoArray
   `general.yaml` retune prompt); `results/notes/interferometer_mesh_cpu_breakdown_2026_09.md`
   with ranked levers (step / bound / gain) and one draft prompt per worthwhile lever; README
   dashboards regenerated.

## Verification

- Local sma smoke of every new arm; counter unit test green; `{1, 1}` counts locally.
- Repo lint as CI: ruff, ruff format --check, `build_readme.py --check`,
  `check_submits.py --check`, `pytest scripts/misc/test/`, smoke scripts.
- RAL: HPCPullPyAuto so the mirror equals the local mains (PyAutoArray >= e281abf3), pip freeze
  vs floors (numba, nufftax); jobs 0 Tracebacks; JSON `source_revisions` match the mains.

## Out of scope

A100 mask-radius jobs (phase 3), the decision matrix (phase 4), any library edit (a gate
retune is filed as a prompt, not made here).

## Folded in: interferometer_sparse_cache_after_measurement.md (verbatim)

_Retired from `draft/research/autolens_profiling/` on filing phase 2 (2026-09-27)._

Witness: RAL CPU numba rows at sma / alma / alma_high, both meshes, measured on PyAutoArray main at or after e281abf3, show `evaluations_per_figure_of_merit` {1, 1}. The full call drops by roughly the redundant share. The figure of merit is unchanged against the pins -3162.627234657415 / -3168.595092417778.

- Status: split out of `interferometer-sparse-cache` at close-out. The library half shipped and is
  recorded in `complete/2026/09/interferometer-sparse-cache.md`
  (https://github.com/PyAutoLabs/PyAutoArray/pull/582, merge e281abf3). This prompt is the workspace
  after-measurement that did not ship.

### What

1. Apply the harness counter fix below to
   `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`. The current counter
   wraps each attribute in `property(... .fget)`, and that **breaks on `cached_property`**, which
   has no `.fget`. The fix unwraps `.func` and re-wraps the counter in the original descriptor
   type. The "F alone" / "D alone" sub-rows also have to pop the cached value before each repeat.
   Without that, they time a dict lookup instead of the computation.
2. Re-run the RAL CPU numba breakdown rows on merged PyAutoArray main (at or after e281abf3):
   sma, alma and alma_high, for both meshes. The result paths are
   `results/breakdown/interferometer/{,sma/,alma_high/}*_numba_hpc_ral_cpu_fp64.json`.
3. Regenerate the README dashboards (`build_readme.py`), then record the before/after full-call
   deltas.

### Harness counter fix

Taken verbatim from https://github.com/PyAutoLabs/PyAutoArray/issues/581#issuecomment-5857574751:

```diff
diff --git a/scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py b/scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py
index de7d80f..516ec3a 100644
--- a/scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py
+++ b/scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py
@@ -89,6 +89,7 @@ is the headline (``steps`` / ``total_step_by_step``), the FFT arm is under
 
 from __future__ import annotations
 
+import functools
 import gc
 import json
 import os
@@ -409,13 +410,15 @@ def run(
             (InversionInterferometerSparse, "data_vector"),
         ):
             original = cls.__dict__[name]
+            _fn = original.fget if isinstance(original, property) else original.func
 
-            def getter(self, _original=original, _name=name):
+            @functools.wraps(_fn)
+            def getter(self, _fn=_fn, _name=name):
                 counts[_name] += 1
-                return _original.fget(self)
+                return _fn(self)
 
             patched.append((cls, name, original))
-            setattr(cls, name, property(getter))
+            setattr(cls, name, type(original)(getter))
         try:
             fom = float(fit_from(median_instance, arm).figure_of_merit)
         finally:
@@ -530,8 +533,8 @@ def run(
         inv = fit_from(median_instance, arm).inversion
         mapper = inv.cls_list_from(cls=Mapper)[0]
         rows_arm = {
-            "F alone (curvature_matrix_diag)": repeat_s(lambda inv=inv: inv.curvature_matrix_diag),
-            "D alone (data_vector = Lᵀ d~)": repeat_s(lambda inv=inv: inv.data_vector),
+            "F alone (curvature_matrix_diag)": repeat_s(lambda inv=inv: (inv.__dict__.pop("curvature_matrix_diag", None), inv.curvature_matrix_diag)),
+            "D alone (data_vector = Lᵀ d~)": repeat_s(lambda inv=inv: (inv.__dict__.pop("data_vector", None), inv.data_vector)),
         }
         if arm == "numpy_fft":
             rows_arm["Sparse triplets alone (extent grid)"] = repeat_s(
```

### Done when

The witness holds. The before/after numbers must be recorded in the breakdown JSONs and in the
campaign's notes.
