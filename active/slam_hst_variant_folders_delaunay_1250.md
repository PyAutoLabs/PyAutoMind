# Run-variant folders on the HST SLaM cell, and the Delaunay-1250 A100 legs

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- inference
- slam
- jax
Difficulty: moderate
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: the four completed A100 base rows render from `results/slam/imaging/hst/slam_base/`; a `PYAUTO_TEST_MODE` delaunay leg builds, traces under jit and writes a row at `results/slam/imaging/hst/delaunay_1250/`; `check_submits.py` GREEN on both new submits; two A100 arrays queued on RAL
Review-minutes: 25
Filed: 2026-09-14
Issued: 2026-09-14

User request (verbatim, 2026-09-14):

"""
WE began our timing runs in autolens_inference, and the first runs looks good, I
would now like us to movre these into a folder from imaging/hst to
imaging/hst/slam_base, and for us to perform delaunay runs with 1250 pixels which
go in this folder on a100, both via normal route and sparse.
"""

## Context

The first four A100 legs of the SLaM base run (`slam_hst_base`, Cortex) finished:
dense and sparse, seeds 0 and 1, all five stages `completed` (~2570 s/seed dense,
~4012 s/seed sparse). They are untracked in `results/slam/imaging/hst/`.

Every leg of every experiment on this cell currently lands directly in
`results/slam/imaging/hst/<config_name>/`, and `build_readme.py` groups rows into
a parity row by the payload's `target` (`hst/slam5/seed<n>`). A second experiment
on the same cell — a different mesh — would therefore share both the directory and
the parity group, and claim to be the same run under a different backend. The cell
needs a **run-variant** level: `imaging/hst/slam_base/` for the mesh-28x28
workspace-default run, `imaging/hst/delaunay_1250/` for the new one.

The new experiment is the Delaunay source: `al.mesh.Delaunay(pixels=1250,
zeroed_pixels=0)` in place of the rectangular adapt meshes, on the A100, dense and
sparse, seeds 0-1. Decided with the human 2026-09-14: sibling variant folders,
seeds 0-1 on both routes, `al.reg.AdaptSplit` on the Delaunay stages.

Grounded against the installed stack (2026.8.17.1): `al.mesh.Delaunay` takes the
vertex count directly and is jit/grad-safe (qhull connectivity via `pure_callback`
+ `stop_gradient`); it needs an adapt image, and `_runner.py:_adapt_images()`
already builds one at every pixelized stage. `al.reg.Adapt` — what the rect legs
use — raises `TracerArrayConversionError` on the Delaunay family under jit, so the
Split variant is mandatory; `_inference_cli.delaunay_regularization()` already
resolves it with the production coefficients.

## Scope

1. `--mesh {rect,delaunay}` + `--mesh-pixels N` on the inference CLI, a `variant`
   segment in the results path, the output `path_prefix` and the target id, and
   `variant`/`mesh`/`mesh_pixels`/`regularization` in the result payload
   (`SCHEMA_VERSION` 1 -> 2, readers tolerate v1).
2. A `scripts/imaging/slam/hst_delaunay.py` leaf so the wall-gate **cell id**
   (`imaging/slam/hst_delaunay`) is distinct from the rectangular cell's — a
   1250-vertex Delaunay chain is a different cost profile and must never share a
   rate row.
3. Move the four completed base rows under `slam_base/` and **commit** them (the
   first real results in this repo); the truncated `__rate_probe_342695` row is
   not committed; `build_readme.py` skips rows whose `status` is not `complete`.
4. Two A100 submits (`submit_slam_delaunay1250_hst_jax_gpu_{dense,sparse}`,
   `--array=0-1`, 12 h containment, `source: unmeasured probe-first: yes` — the
   base run's walls are not citable across the mesh boundary).
5. A Cortex task `slam_hst_delaunay_1250`, the two arrays submitted on RAL, job
   ids recorded. The session ends at submission; the pull and the judgment happen
   on a later `/cortex` check-in.

## Out of scope

- The four CPU legs of the base run (still awaiting the human's OK).
- Filling `wall/rates.py` with the now-measurable A100 rates for
  `imaging/slam/hst` from the completed base rows — worth doing, but it changes
  the base submits' wall basis and belongs in its own prompt.
