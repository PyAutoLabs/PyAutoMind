Shipped as autolens_inference#6 (merged `ee31deb`), issue #5 closed.

## What shipped

The HST SLaM cell gained a **run-variant** level. Every leg used to land in
`results/slam/imaging/hst/<config_name>/`, and `build_readme.py` groups rows
into a parity row by the payload's `target` — so a second experiment on the
same cell would have shared both the directory and the parity group, claiming
to be the same run under a different backend. The 28x28 rectangular
workspace-default run is now the variant `slam_base`; the mesh under test is
`delaunay_1250`.

- `--mesh {rect,delaunay}` / `--mesh-pixels N`, threaded into the results path,
  the output `path_prefix`, the target id (`hst/slam5_<variant>/seed<n>` for
  anything but the base, which keeps `hst/slam5/seed<n>`) and the payload
  (schema v2; v1 rows still render).
- The Delaunay route as production builds it: a Hilbert image mesh draws 1250
  vertices from the S/N-capped source adapt image (weight power 3.5, floor
  0.01), a 30-point circle edge ring is appended, and
  `al.mesh.Delaunay(pixels=1250, zeroed_pixels=30, areas_factor=0.5)` pairs
  with the `al.reg.AdaptSplit` **class**. `total_pixels == pixels +
  zeroed_pixels`, so the ring size and `zeroed_pixels` are one number written
  twice. The whole recipe is recorded in every row.
- A `scripts/imaging/slam/hst_delaunay.py` leaf, so the wall gate's cell id —
  and therefore the rate key — is `imaging/slam/hst_delaunay`.
- Two A100 submits (`jax_gpu` x {dense, sparse}, seeds 0-1, 24 h containment,
  96 gb, 8 CPUs), `source: unmeasured  probe-first: yes`.
- **The four completed A100 base rows**, committed under `slam_base/` — the
  first real results this repo holds — with the README tables regenerated.
  `build_readme.py` now skips rows whose `status` is not `complete`.

## What the pre-submission smoke caught

Three defects, each worth an A100 slot, none of which a rectangular leg hits:
the mesh must be a plain **instance** (an `af.Model` leaves `areas_factor` free
and this repo has no prior config for it); it does **not place its own
vertices** (without an image-plane mesh grid via `adapt_images` the
pixelization cannot be built); and at `--cores 2` the fit **deadlocks** — 22
minutes, every thread in `futex_wait`, zero CPU, while a heartbeat thread
printed "still compiling". The mesh reaches qhull through a
`jax.pure_callback`, so the fit calls back into the host while an XLA
computation is in flight, and a pool narrower than the callback depth hangs.
Hence 8 CPUs on the submits, and a fourth commit taking the CI witness leg off
`--cores 2`.

Measured: `source_pix[1]` compile is ~25 min (dense) / ~34 min (sparse) on the
small euclid cell against seconds for the rectangular legs — which is why the
containment went 12 h to 24 h. Peak RSS 9.3 GB dense / 6.5 GB sparse, inverting
the base run's ordering, which is why both legs request 96 gb.

## Runs

A100 arrays **343143** (dense) and **343145** (sparse), seeds 0-1, submitted
2026-09-15 from the feature branch on the RAL clone. The Cortex ledger
`projects/autolens_inference.md` carries them as open runs; they are judged on
a `/cortex` check-in, not here.

## Findings for whoever reads the comparison

1. On the base row, dense and sparse agree at the same seed to 0.00-0.04σ
   (seed 0) and 0.3-0.6σ (seed 1), while **seeds of the same leg disagree by up
   to 0.93σ and 2.9-3.4 nats**. The `slam_hst_base` witness bands (2 nats, 0.2σ,
   σ-ratio [0.8, 1.25]) are tighter than Nautilus's own seed reproducibility on
   this cell. Any variant comparison must be seed-paired, and the bands
   themselves want rewriting before the CPU legs run.
2. `source_pix[2]` carries 3 free parameters on the Delaunay branch against the
   rectangular branch's 5 (the rectangular image mesh leaves
   `weight_power`/`weight_floor` free; the Hilbert weights are pinned at the
   production values). This is Delaunay-as-production-runs-it versus the
   rectangular default, not a controlled single-variable swap.
3. Sparse costs ~1.5x dense on the A100 for the rectangular base chain and buys
   nothing measurable.

## Left open, deliberately

The four CPU legs of `slam_hst_base` still await the human's OK; `wall/rates.py`
still carries no a100 row although the four completed base rows can now supply
one.

## Original prompt

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
