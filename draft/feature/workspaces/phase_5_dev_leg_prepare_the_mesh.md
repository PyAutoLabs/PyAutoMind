# Phase 5 dev leg: prepare the mesh gradient-search array for PositionsLH…

Type: feature
Target: workspaces
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: jax-inference-profiling

Phase 5 dev leg: prepare the mesh gradient-search array for PositionsLH at factor 1e5 / threshold auto — verify the multi_start_prodigy leaf scripts honour SEARCHES_POSITIONS / _THRESHOLD / _FACTOR through _setup.py, add a `submit_search_multi_start_prodigy_phase5_positions_array.sh` under hpc/batch_gpu/ (cells × seeds per Cortex phase 16), include the one-cell Nautilus tauto0.2 f1e5 control task, and dry-run one task with AUTOLENS_PROFILING_SMOKE=1. No submission — dispatch is a Cortex phase-16 act after phase 12 is ruled.

Gate: this prompt is gated on PyAutoCortex phase 16
(`phases/inference_programme/phase5_mesh_gradient_positions_on.md`, state `planned`)
having been READ BY THE HUMAN — the array's cells, arms and seeds come from that
phase's dispatch plan, and it also records two open questions the array's shape
depends on (there is no `multi_start_prodigy_autoconv` leaf for any mesh cell, and
no measured step rate for any mesh cell at 256 lanes, so a probe arm precedes the
sizing). Not a `Blocked-by:` — a Cortex phase is not a GitHub ref.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from user-intake -->

## Widened 2026-09-02 (human decision)

Everything above stands verbatim; this section adds to it. PyAutoCortex phase 16
(`phases/inference_programme/phase5_mesh_gradient_positions_on.md`) was widened on the
same date and this dev leg is the half that has to land first.

### (a) Every Phase 5 gradient arm is the Gate B1 config `multi_start_prodigy_autoconv`

The human's call closes phase 16's open item 3 ("a decision on `autoconv`"): auto-convergence
is **ON for every arm**, at the Gate B1 settings — `check_for_convergence=True, window=50,
rtol=1e-4, atol=1e-3, min_steps=100` (`scripts/misc/searches/_samplers.py`, `_MULTI_START_AUTOCONV`
and `_convergence()`, lines ~746-790). Phase 5 therefore *is* the Gate B pt 1 config and does
not have to caveat itself as a fixed-step surrogate. The consequence is seven new leaves:

```
scripts/imaging/searches/multi_start_prodigy_autoconv/{pixelization,knn,delaunay_matern,
                                                       delaunay,delaunay_nn,
                                                       slam_source_pix,slam_source_pix_nn}.py
```

Each mirrors `multi_start_prodigy_autoconv/mge.py`: the same `_profiling_root()` preamble and a
single `run_search(sampler="multi_start_prodigy_autoconv", dataset_class="imaging",
model_type="<cell>", default_instrument="hst")` call. Nothing else belongs in a leaf — the
per-lane best records (`lane_best_params` / `lane_best_foms` / `lane_best_steps`), `stop_reason`,
and the `SEARCHES_POSITIONS` / `_THRESHOLD` / `_FACTOR` plumbing are properties of `_runner.py`
and `_setup.build_for_cell`, which are **sampler-agnostic** (`_runner.py:783`,
`is_multi_start = sampler in _MULTI_START_CLASSES`; `_setup.py:161-300`, `build_for_cell` takes
no sampler argument at all).

**What was verified in the code, per cell** (read, not assumed):

| new autoconv leaf | closer template | what it needs |
|---|---|---|
| `pixelization.py` | `multi_start_prodigy/pixelization.py` | straight copy; per-cell knob rows already exist |
| `knn.py` | `multi_start_prodigy/knn.py` | straight copy; per-cell knob rows already exist |
| `delaunay_matern.py` | `multi_start_prodigy/delaunay.py` (whose `model_type` is `delaunay_matern`) | straight copy. **Name it for the cell, not the file it came from** — the fixed-step leaf's filename/`model_type` mismatch is exactly the trap phase 16's cells table had to spell out |
| `delaunay.py` (plain) | `nautilus/delaunay.py` (only source of the `model_type` spelling) | new cell for MultiStart; needs the knob rows below |
| `delaunay_nn.py` | `nautilus/delaunay_nn.py` | new cell for MultiStart; knob rows below; see the lane-mortality note |
| `slam_source_pix.py` | `nautilus/slam_source_pix.py` | new cell for MultiStart; knob rows below |
| `slam_source_pix_nn.py` | `nautilus/slam_source_pix_nn.py` | new cell for MultiStart; knob rows below; see the lane-mortality and NaN-wall notes |

**`_setup.build_for_cell` needs no work for any of these cells.** All seven `model_type`s are
already registered (`_setup.py:85-100`, `_PIX_MODEL_TYPES`), dispatched in `_build_model`
(`_setup.py:842-853` → `_delaunay_nn_model` / `_slam_source_pix_model` /
`_slam_source_pix_nn_model`), given Hilbert-mesh adapt images through `_DELAUNAY_FAMILY`
(`_setup.py:102-109`, `_adapt_images_for` at `_setup.py:1950`), and covered by the positions
plumbing (`imaging` is in `_POSITIONS_SUPPORTED_DATASET_CLASSES`, `_setup.py:991`). Better:
`_setup.py:282-293` already applies SLaM's own **auto** threshold convention to
`slam_source_pix` / `slam_source_pix_nn` when positions are on and `SEARCHES_POSITIONS_THRESHOLD`
is unset — i.e. the `tauto` arm shape phase 5 wants comes for free on exactly those two cells,
and an explicit `SEARCHES_POSITIONS_THRESHOLD` in the submit script **suppresses** it. Target ids
are sampler-independent (`_targets.py:433`), so the positions-on target rows the witness
recomputes against already exist for all seven cells.

**The one real source change is in `_samplers.py`, not `_setup.py`.** The per-cell MultiStart
knob tables carry rows only for `imaging:pixelization`, `imaging:knn`, `imaging:delaunay_matern`
(and `group`):

- `_MULTI_START_N_STARTS_BY_CELL` — `_samplers.py:361-367`
- `_MULTI_START_BATCH_BY_CELL` — `_samplers.py:381-386`
- `_MULTI_START_N_STEPS_BY_CELL` — `_samplers.py:416-422`

For `delaunay`, `delaunay_nn`, `slam_source_pix` and `slam_source_pix_nn` an un-overridden
MultiStart run therefore resolves to the module defaults: `n_starts=64`, `n_steps=300`, and
`batch_size=None`. The last is the dangerous one — `batch_size=None` on a *pixelized* cell is
precisely the unbatched jvp fusion the comment at `_samplers.py:368-380` calls the ~58 GB
allocation, and says is **not optional** on pixelized cells; `n_steps=300` would additionally be
the budget artefact the same file warns about at `_samplers.py:411-415`. The array's env vars
(`SEARCHES_N_STARTS` / `_N_STEPS` / `_BATCH_SIZE`) would mask all three, but a bare leaf run and
the `AUTOLENS_PROFILING_SMOKE=1` dry-run would not. So: **add the four missing rows to each of
the three tables** (`batch_size=4`, `n_steps=3000`, `n_starts=16` for symmetry with the other
mesh cells) as part of this dev leg, with a comment naming Phase 5. That is twelve dict entries,
not a refactor.

Two science risks to carry into the leaf docstrings rather than discover on the A100:

- **Lane mortality on the DelaunayNN cells.** `_targets.py:170-180` records the W4 broad-draw
  verification: `delaunay` 8/8 finite, `delaunay_nn` 3/8 finite (3/8 NaN, 2/8 FitException),
  `slam_source_pix_nn` 1/8 finite (2/8 NaN, 5/8 FitException). A 256-lane *broad-start* search is
  the configuration most exposed to that, so the leaves should say so and the arms should expect
  a materially lower live-lane count than on `knn`.
- **The reg/jit constraint is already baked in and must not be "fixed".** `_setup.py:1505-1520`
  records that `al.reg.Adapt` cannot be traced under `jax.jit` on the Delaunay family
  (`TracerArrayConversionError` via `regularization/adapt.py` → `mesh_geometry/delaunay.py` →
  qhull; it killed RAL 340210 tasks 5 and 6 in ~52 s), which is why `slam_source_pix_nn` uses
  `AdaptSplit` and `delaunay_nn` uses `ConstantSplit`; `slam_source_pix`'s `reg.Adapt` is
  jit-safe only because the rectangular family has analytic neighbours. `AdaptSplit` on a
  Delaunay-family mesh is also the documented NaN wall (`_setup.py:1535+`). None of this blocks a
  gradient leaf — it is why the models are shaped as they are — but a leaf must not "helpfully"
  swap a regularization to match a sibling cell.

`scripts/misc/searches/sweep.py`'s `CELLS` list (`sweep.py:82-129`) is a sweep-driver
convenience, not a registry: the existing mesh `multi_start_prodigy` leaves are absent from it
too, so adding the new cells there is optional and out of scope unless the sweep is wanted.

### (b) The array: 41 tasks, plus a per-cell step-rate probe set

`hpc/batch_gpu/submit_search_multi_start_prodigy_phase5_positions_array.sh` covers phase 16's
widened dispatch plan:

- **primary** — 7 cells × seeds 0-4 = **35 tasks**, `pos_tauto0.2_f1e5`, `MultiStartProdigy`
  n=256, `prior_box`, `scaler=none`, autoconv, `batch_size=4`, fp64, viz off;
- **bridge** — `knn` only, seeds 0-4, `pos_t0.3_f1e5` = **5 tasks**;
- **control** — Nautilus `knn`, seed 0, `pos_tauto0.2_f1e5`, n_live 2× fiducial (300), fp64,
  `--config-name hpc_a100_fp64_ref` = **1 task**.

**41 tasks, `--array=0-40`**, one task per arm/seed, `--requeue` for the `_gpu_preflight.sh` MIG
bounce, `--time` 8:00 per task.

Separately — and this is what the human runs **first** — a **per-cell step-rate probe set**: one
short truncated arm per in-scope cell (7 tasks) at the dispatch lane tier, whose measured s/step
goes into `scripts/misc/wall/rates.py` with its job id before the real array is sized. Today
`rates.py` holds only 16-lane / `batch_size=4` mesh rows (`knn` 2.20 s/step,
`delaunay_adapt_split` 4.85 s/step) and nothing at all for five of the seven cells, and
`wall/check_submits.py` requires the submit's `WALL-BASIS` block to cite `source: rates`. Quoting
a rate across a configuration is what killed RAL 340576, so the probe set ships as its own submit
script (or an `--array` subset flag on the same one) and the 41-task array is not submitted until
its rows land. **No submission from this dev leg either way** — dispatch is an act of phase 16.

### (c) DelaunayNN is a named deliverable

`delaunay_nn` (and, for the SLaM pair, `slam_source_pix_nn`) is not an optional extra: phase 5's
**H5.2 DelaunayNN / kernel-CDF ranking cannot be answered without it**, and it has a *ruled*
positions-on Nautilus bar to score against (`delaunay_nn_pos` 31,351.39, R-20260902-01). A
version of this dev leg that lands the three phase-12 cells and skips DelaunayNN does not unblock
phase 16. `delaunay_adapt_split` stays out of scope — it has no reference row of any kind.

### Difficulty

**Still `medium`.** The seven leaves are five-line `run_search(...)` copies, `build_for_cell`
needs no change for any cell (verified above), and the only source edit is twelve dict rows in
`_samplers.py`. The remaining work — the 41-task submit script, the probe-set submit, the
`rates.py` rows and one `AUTOLENS_PROFILING_SMOKE=1` dry-run — is submit-script work of the kind
this repo already has many examples of. It would only be `large` if the SLaM cells needed real
`_setup` work, and they do not.
