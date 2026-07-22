## convolver-gaussian-small-datasets-cap

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/397 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoArray/pull/398 (merged, `402ffba7`)
- repos: PyAutoArray

### What it was

`mask_irregular.py` failed under `PYAUTO_SMALL_DATASETS=1` with
`ArrayException: array_2d_slim.shape = 256 vs mask_2d.pixels_in_mask = 961, shape_native (31,31)`.

**The originating prompt's diagnosis was wrong.** It read this as an env-config gap needing
`unset: [PYAUTO_SMALL_DATASETS]` in each workspace's `config/build/env_vars.yaml`, or mask
capping. Reproducing it showed the traceback never reaches the mask-building code — it dies
at line 53 in `al.Convolver.from_gaussian`, before any data/mask comparison.

Root cause: `Convolver.from_gaussian` evaluates its Gaussian on `Grid2D.uniform`, which the
fast-mode cap silently shrinks to 16x16 (`uniform_2d.py:499`), then wraps those 256 values in
an `Array2D` using the caller's **uncapped** `shape_native` (961) — self-inconsistent. Any
Gaussian kernel above 16x16 was broken in smoke mode.

### Fix

One call site, `autoarray/operators/convolver.py:721` — pass the already-existing opt-out
`Grid2D.uniform(respect_small_datasets=False)`. A kernel's shape is intrinsic to the
convolution operator, not a dataset size; a 31x31 kernel convolving a 16x16 image is valid.
Plus a numpy-only regression test in `test_autoarray/operators/test_convolver.py`.

### Verification

- Regression test verified **RED on `main`** with the exact production `ArrayException`
- PyAutoArray suite: 927 passed
- Smoke, all six workspaces: 50 pass / 4 skip / 1 pre-existing unrelated failure
- `mask_irregular.py` green in both workspaces with the flag set *and* unset
- 11x11 consumer (`imaging/simulator.py`) unchanged — no behaviour change below the cap

### Notes for future work

- **No workspace changes were needed.** The prompt listed 5 repos; 4 dropped out. Adding the
  suggested `unset:` override would have masked a live library bug and left every >16x16
  kernel broken.
- **Latent siblings:** the only other >16x16 `from_gaussian` call sites are two `(21,21)` ones
  (`autolens_workspace/scripts/imaging/simulator.py:435`,
  `guides/advanced/over_sampling.py:494`) — both inside non-executed fenced prose blocks, and
  `guides/` already unsets the flag. They were latent, not failing.
- **Diff hygiene:** `test_autoarray/operators/test_convolver.py` is mixed CRLF/LF in HEAD
  (336 CRLF + 191 LF). A normal `Edit` normalises the whole file to CRLF, turning a 24-line
  addition into a 215/191 diff. Re-inserted preserving the original endings. Both touched
  files are also already non-black-clean on `main` — left alone rather than burying the fix
  in reformatting.
- **Spun out:** `autolens_workspace_test/.../point_source/point.py` JAX-vmap parity assert is
  **non-deterministic** (`-1e+99` in a parallel batch, `16.131221` in serial re-runs).
  Confirmed unrelated by A/B against the pre-fix `convolver.py`. Filed as
  `draft/bug/autolens/point_jax_vmap_parity_nondeterministic.md`.

## Original prompt

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
