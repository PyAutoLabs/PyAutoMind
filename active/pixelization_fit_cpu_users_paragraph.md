# Fix the imaging pixelization `fit.py` "CPU Users" paragraph (interferometer text pasted into imaging)

Type: docs
Target: autolens_workspace
Repos:
- @autolens_workspace
- @HowToLens
- @PyAutoArray
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Issued: 2026-08-28
Filed: 2026-08-28

Found by the numba-cpu-likelihood epic close-out docs sweep (2026-08-28); pre-existing, not caused by
the epic.

1. `autolens_workspace/scripts/imaging/features/pixelization/fit.py:20-25` (+ the Contents bullet at
   `:29`): the `__CPU Users__` block is the *interferometer* paragraph (talks about visibilities, "over
   hours", and points at `features/pixelization/many_visibilities_preparation`, which only exists under
   `scripts/interferometer/`). Replace with the imaging statement: on CPU use
   `dataset.apply_sparse_operator_cpu()` (a few seconds to a few minutes of one-off setup), see
   `features/pixelization/cpu_fast_modeling`. Mirror the fix wherever the same paragraph was pasted
   (grep `many_visibilities_preparation` under `scripts/imaging/`, and the autogalaxy_workspace twin).
2. `HowToLens/scripts/chapter_2_lens_modeling/tutorial_8_need_for_speed.py:111-113`:
   "numba … JAX supersedes it" — add one clause: except for pixelized sources, where the numba CPU
   path (`imaging/features/pixelization/cpu_fast_modeling.py`) is the faster route on many-core
   machines.

3. PyAutoArray `autoarray/settings.py` (`nnls_warm_start_memo` / `nnls_warm_start_error_tolerance`
   properties + `__init__` docstring): the comments say a workspace `general.yaml` "shadows" autoarray's
   so the `KeyError` fallback "is the production default". Overstated — autoconf's path list falls
   through to autoarray's packaged config for a missing key (measured: `nnls_warm_start_memo -> True`
   from autolens_workspace); the fallback only fires when the workspace config is the sole path (e.g. a
   test that pushes one config dir). Reword: the fallback matches the packaged default so both routes
   resolve identically; comment-only, no behaviour change, no test change.

Not needed (verified): workspace `general.yaml` `inversion:` blocks — do not add the keys.
