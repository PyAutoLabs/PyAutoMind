- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/232
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/233
- scope: **whole prompt** — all five Delaunay-family cells re-based, both schemes pinned per cell,
  provenance key added, and the A/B priced on the A100. The `autolens_workspace_test` scope note
  resolved to no change: `scripts/imaging/jax_likelihood/delaunay.py` there already uses
  `AdaptSplit`, so no pin needed flipping. The follow-up below is a new lever the measurement
  exposed, not unshipped scope.

### What shipped

Every `autolens_profiling` Delaunay-family likelihood cell measured
`al.reg.ConstantSplit(coefficient=1.0)`, while production (the Euclid pipeline, the SLaM
pipelines) pairs Delaunay meshes with `al.reg.AdaptSplit`. The profiled rows were therefore not
the regularization production actually pays for.

- **A shared `--regularization {adapt_split,constant_split}` flag and a
  `delaunay_regularization()` helper in `_profile_cli.py`.** Five cells now default to
  `AdaptSplit(inner=0.1, outer=10.0, signal_scale=0.1)`:
  `likelihood_breakdown/delaunay{,_nn}.py` and
  `likelihood_runtime/delaunay{,_nn,_numba}.py`. `constant_split` still reproduces the historical
  scheme exactly, so the old rows stay comparable.
- **The adapt image is wired into every `AdaptImages` *and* into the cells' directly built
  interpolators** (`adapt_data=adapt_image` on the `_INTERPOLATOR_CLS` constructions). Without
  that second half `pixel_signals_from` receives `adapt_data=None`; the first local run is what
  caught it.
- **Per-scheme pins in every cell**, with the `ConstantSplit` values re-verified through the new
  always-on adapt-image wiring — DelaunayNN reproduced `29144.581943564488` to the last digit,
  which is what keeps the historical rows citable.
- **A `regularization` provenance key** next to `sibson` in every result JSON.
- **8 new A100 submits** under `hpc/batch_gpu/` (`submit_{breakdown,runtime}_imaging_delaunay{,_nn}_a100_hst_fp64_{adapt,constant}_split`),
  written without the retired `--exclude=euclid-ral-gpu-1` MIG block.
- **Canonical row semantics changed, no history destroyed.** `breakdown/imaging/delaunay{,_nn}_hpc_a100_fp64.*`
  and the matching runtime rows now mean **AdaptSplit**; the previous canonical ConstantSplit rows
  were `git mv`-ed to `..._hpc_a100_fp64_constant_split_2026_09_05.*` (pre-#537, not on this
  note's scale), and the 2026-09-08 same-node controls are `..._hpc_a100_fp64_constant_split.*`.
  `results/README.md` records both conventions.
- **Regenerated README dashboards** (`results/README.md` plus the generated `README.md` and
  `scripts/misc/likelihood_breakdown/README.md`) — `build_readme.py --check` is a lint step, so
  new results rows are a RED until the dashboards are regenerated.
- The full note: `autolens_profiling/results/notes/delaunay_adapt_split_regularization.md`.

Coefficients are deliberately **not** the constructor defaults: `AdaptSplit()` is
`inner = outer = 1.0`, and `adapt_regularization_weights_from` returns `outer` everywhere when
`inner == outer`, so the default degenerates to `ConstantSplit(1.0)` — the pins would not move and
the A/B would prove nothing. `0.1 / 10.0 / 0.1` are the production-shaped values already used
in-repo by `likelihood_breakdown/delaunay_numba_nnls_iterations.py`.

**No library change.** The dependency (PyAutoArray #537, the split-stencil compaction) was already
merged and present in the shared RAL install (`47a00e8c`), so the library-first merge gate was
trivially satisfied — there was no upstream PR to wait on.

### The numbers (A100 `euclid-ral-gpu-2`, jobs 342340–342347, one node, one window)

Per likelihood call at `vmap` 16 — the citable column:

| Quantity | ConstantSplit | AdaptSplit | Δ |
|---|---:|---:|---:|
| DelaunayNN `params→H` prefix | 7.250 ms | **7.277 ms** | +0.4 % |
| DelaunayNN whole likelihood | 40.92 ms | 45.76 ms | +11.8 % |
| Delaunay whole likelihood | 39.68 ms | 42.47 ms | +7.0 % |

**The AdaptSplit assembly is free** — PyAutoArray #537's split-stencil compaction survives the
regularization change intact. What AdaptSplit costs sits **downstream in the NNLS reconstruction**,
not in `H`: `reconstruction_positive_only_from` on the JAX path is `jax_nnls.solve_nnls_primal`, a
primal-dual `lax.while_loop` capped at `max_iter = 50` that under `vmap` runs until the slowest
lane converges. AdaptSplit's per-pixel weights span two decades (`inner 0.1` … `outer 10.0`) where
ConstantSplit's are flat, so `F + H` is worse conditioned and the loop takes more trips. That is a
finding about the **production configuration**, not a regression introduced here — production
already pays it; the profiling rows now show it.

AdaptSplit moves the log evidence by a real margin (+44.1 nats Delaunay, +204.3 DelaunayNN), so
the per-scheme pins genuinely discriminate the schemes rather than duplicating each other.

### Witness verdict — met

The pre-registered witness asked that every re-based cell carry a new `EXPECTED_LOG_EVIDENCE_HST`
pin passing on both legs, and that the AdaptSplit `params→H` prefix on the DelaunayNN cell sit
within ~1 ms/call at `vmap` 16 of the ConstantSplit row in
`results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_assembly.json`.

Both met. **All 8 A100 pins PASSED** (max drift 3.3e-10 relative; the runtime legs report
`pinned_drift: []`), and the prefix is **7.277 vs 7.250 ms/call — a 0.027 ms gap against a ~1 ms
allowance**.

### Verification

- **Local CPU, eager**: all five cells × both schemes run this session, every run `EXIT 0`; every
  `constant_split` control reproduced its pre-change pin, and the new `adapt_split` pins were taken
  from those first eager runs.
- **A100**: 8 legs (342340–342347) all `COMPLETED`, 0 `Traceback`, 0 float32 truncation warnings,
  all 8 JSONs written, all 8 pins PASSED.
- **Ship re-validation**: `likelihood_runtime/delaunay_numba.py --regularization adapt_split`
  (euclid) `EXIT 0`, pinned-value check PASSED (5579.104036561175 vs pin 5579.104036561161),
  `regularization` key present in the JSON.
- `ruff check .` clean; `ruff format --check .` — 212 files already formatted.
- **CI**: `lint` green on `e21c4d9` (the single gate on this repo — build_readme `--check`,
  check_submits, pytest, lychee, smoke in one job).

### Caveat

The **unbatched** rows carry a systematic ~+5 ms offset on the AdaptSplit legs in a block that
contains no regularization work at all (`Inversion setup`, steps 5–8), while the same block at
`vmap` 16 is flat to 0.1 %. The AdaptSplit leg was the first job of each pair and **no
reversed-order repeat was run**, so a first-job-on-node warm-up cannot be excluded. **Read the
`vmap` 16 columns as the citable numbers**; treat unbatched deltas below ~5 ms as noise on this
session.

### Follow-ups

- **The NNLS iteration count under adaptive regularization is now the largest mesh-agnostic lever
  on the Delaunay-family likelihood.** AdaptSplit costs +7 % (Delaunay) to +11.8 % (DelaunayNN) of
  a whole evaluation, and all of it is `solve_nnls_primal` taking more trips round its
  `lax.while_loop` because `F + H` is worse conditioned — not mesh work, not assembly work. Warm
  starts, preconditioning on the adapt weights, or a per-lane convergence exit are the obvious
  candidates. **Described, not filed** — it wants costing against the post-#537 figures first.
- **The cavity early exit (Phase B of the DelaunayNN Phase A prompt) stays deferred**, as it was at
  the #537 close-out. Still unfiled.
- **`build_readme.py --check`'s error text names a stale path** — it tells you to run
  `scripts/build_readme.py`, but the real script is `scripts/misc/tooling/build_readme.py`. A
  one-line fix in the generator's message, worth doing next time that file is open.

### Traps worth remembering

- **`AdaptSplit()`'s constructor defaults are `ConstantSplit(1.0)` in disguise.** `inner = outer = 1.0`
  makes `adapt_regularization_weights_from` return `outer` everywhere, so an A/B against the
  defaults measures nothing and the pins do not move. Pick production-shaped coefficients
  deliberately.
- **An adapt image has to reach two places, not one.** Wiring it into `AdaptImages` is not enough
  in cells that also build their interpolator directly: without `adapt_data=` on that
  construction, `pixel_signals_from` silently gets `adapt_data=None`. The first local run caught
  it here; nothing in the API complains.
- **Adding files under `results/` is a lint failure until the README dashboards are regenerated.**
  `build_readme.py --check` is a step of the single `lint` job on this repo, so new result rows
  turn CI RED with no other symptom. Regenerate in the same commit. (This close-out's first `/prm`
  pass stopped exactly there.)

### Heart

- heart-ack: 2026-09-08 in-session, YELLOW — "workspace validation not passing (5 failed, 2
  timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens
  scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more); release
  validation incomplete: no rehearsal for current source — both organism-scope, neither names
  autolens_profiling"

### Notes

- Workspace-only task: no library PR, so no `pending-release:` obligation outlives this record.
- `autolens_profiling` was under a three-way parallel claim (`retire-gpu1-mig-exclusion` #220,
  `interferometer-preload-cpu` #229); file sets were verified disjoint at claim time and no
  conflict materialised.
- CI at close-out: `lint` green on `e21c4d9` (1 run, 1 job). The first `/prm` pass stopped on a RED
  `lint` at `203d5f4` — `build_readme.py --check` would have rewritten `README.md` and
  `scripts/misc/likelihood_breakdown/README.md`; regenerating them and pushing produced `e21c4d9`.
  No freeze window open.

## Original prompt

# Re-base the Delaunay profiling cells on AdaptSplit regularization

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- profiling
- regularization
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: every re-based cell has a new EXPECTED_LOG_EVIDENCE_HST pin that passes on both legs, and the AdaptSplit params->H prefix on the DelaunayNN cell is within ~1 ms/call at vmap 16 of the ConstantSplit row in results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_assembly.json
Review-minutes: 20
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-08

## Original request (verbatim)

> I think this should use AdaptSplit like regular delaunay albeit its good we sped up ConstantSplit

## Why

Every autolens_profiling likelihood cell for the Delaunay family measures
`al.reg.ConstantSplit(coefficient=1.0)`:

- `scripts/imaging/likelihood_breakdown/delaunay.py`
- `scripts/imaging/likelihood_breakdown/delaunay_nn.py`
- `scripts/imaging/likelihood_runtime/delaunay.py`
- `scripts/imaging/likelihood_runtime/delaunay_nn.py`
- `scripts/imaging/likelihood_runtime/delaunay_numba.py`

Production pipelines pair Delaunay with `al.reg.AdaptSplit` — see
`euclid_strong_lens_modeling_pipeline/scripts/initial_lens_model.py` and the
SLaM pipelines. So the profiled numbers are not the regularization production
runs actually pay for.

## Task

Re-base those cells on `AdaptSplit`, taking the adapt image from the cell's
existing adapt-image path — the same one the `Hilbert` mesh already uses — so
the Delaunay and DelaunayNN cells profile what production runs.

`AdaptSplit` shares `pixel_splitted_regularization_matrix_from` with
`ConstantSplit`, so the PyAutoArray #537 compaction (assembly 10.03 -> 0.84
ms/call at vmap 16) carries over; the only extra cost is the per-pixel adapt
weights.

Expect the log-evidence pins (`EXPECTED_LOG_EVIDENCE_HST` in each script) to
change, so each cell needs a fresh pin measured on the A100 with a same-node
control (ConstantSplit) vs feature (AdaptSplit) pair, per the protocol in
`results/notes/delaunay_nn_constant_split_assembly.md`.

Keep ConstantSplit available behind a `--regularization` CLI flag or config key
if that is cheap — the historical rows are ConstantSplit and must stay
comparable. The default flips to AdaptSplit.

Record which regularization every result JSON was measured with: a
`regularization` key next to the existing `sibson` key.

## Scope note

autolens_workspace_test is in scope only if a jax_assertions pin needs the same
flip — check `scripts/imaging/jax_likelihood/delaunay.py` there, which already
uses AdaptSplit per the PyAutoArray #537 ship notes.

## Witness

- Every re-based cell has a new pin that passes on both legs.
- The AdaptSplit params->H prefix on the DelaunayNN cell is within ~1 ms/call at
  vmap 16 of the ConstantSplit row in
  `results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_assembly.json` — i.e. the
  compaction gain survives the regularization change.

## Related

- `complete/2026/09/delaunay-nn-constant-split-assembly.md`
- PyAutoArray #536, PyAutoArray #537
- `autolens_profiling/results/notes/delaunay_nn_constant_split_assembly.md`

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 -->
