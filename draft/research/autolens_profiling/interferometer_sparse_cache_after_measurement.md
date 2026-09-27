# Interferometer likelihood campaign: after-measurement for the sparse cached_property fix (harness counter fix + RAL CPU numba re-run)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- numba-cpu
- likelihood-profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: RAL CPU numba rows at sma / alma / alma_high, both meshes, measured on PyAutoArray main at or after e281abf3, show `evaluations_per_figure_of_merit` {1, 1}. The full call drops by roughly the redundant share. The figure of merit is unchanged against the pins -3162.627234657415 / -3168.595092417778.
Review-minutes: 8
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

- Status: split out of `interferometer-sparse-cache` at close-out. The library half shipped and is
  recorded in `complete/2026/09/interferometer-sparse-cache.md`
  (https://github.com/PyAutoLabs/PyAutoArray/pull/582, merge e281abf3). This prompt is the workspace
  after-measurement that did not ship.
- Fold option: campaign phase 2 (in-situ crossover) re-runs these RAL CPU rows anyway, so this
  work can be folded into phase 2. See
  `draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`.

## What

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

## Harness counter fix

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

## Done when

The witness holds. The before/after numbers must be recorded in the breakdown JSONs and in the
campaign's notes.
