# mask_irregular fails under SMALL_DATASETS: slim array 256 (16^2) vs mask 961 (31^2)

Type: bug
Target: autoarray
Repos:
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Un-parked by a parallel chat (old "silent failure" resolved) — now the REAL error is a
SMALL_DATASETS cap mismatch, i.e. an env-config gap, not a deep code bug:

```
imaging/data_preparation/manual/mask_irregular.py
  autoarray/structures/arrays/array_2d_util.py:69 check_array_2d_and_mask_2d
  ArrayException: slim array_2d_slim.shape = 256  vs  mask_2d.pixels_in_mask = 961, shape_native (31,31)
```

The data array is capped to 16x16 (256) under PYAUTO_SMALL_DATASETS=1 but the manually-drawn
irregular mask is 31x31 (961) — sizes disagree. Fix options (mirror the 2026-07-21 cap/should_simulate
work): add a per-script `unset: [PYAUTO_SMALL_DATASETS]` override in each repo's config/build/env_vars.yaml
(this script loads pre-committed/real data at full res), OR cap the mask via the same 16x16 lever.
Affected: autogalaxy_workspace + autolens_workspace (+ HowToGalaxy/HowToLens if they carry the script).
Currently un-parked and FAILING — remove/refresh any NEEDS_FIX marker once green.
