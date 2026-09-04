# gradient-slam-baseline dev leg: the `mass_pix` target, its drivers and a gradient-cost probe

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- pixelization
- jax-gradient
- profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Witness: `mass_pix` builds on CPU with exactly 7 free parameters and one forward eval returns a finite log-likelihood; the probe script runs and prints a forward/grad ratio and an FD table
Review-minutes: 20
Unattended: ready
Filed: 2026-09-04
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/218 (opened 2026-09-04 as a Cortex gate ref; reuse in start_dev — never open a second)

Build the **`mass_pix`** profiling target — a SLaM `mass[1]`-shaped cell: lens light fixed
to the simulator truth, source mesh and regularization fixed at certified values, **only
mass + shear free (7 parameters)** — plus its two search drivers, a gradient-cost probe
script and the HPC submit scripts the science phases will use. **No submission**: dispatch
is a PyAutoCortex act, and phase 20 is gated on this prompt's issue.

This is the development half of the Cortex epic **`gradient-slam-baseline`**, born
2026-09-04 from the retired `jax-inference-profiling` programme. Read its ledger first —
`@autolens_profiling/results/notes/gradient_slam/LEDGER.md` — which carries the question,
the inherited citable evidence, the exact fixed values with their provenance, and the four
Cortex phases (20–23) this leg unblocks.

## Why

**No gradient-search run exists on any rectangular mesh target, anywhere.** MGE Prodigy is
done and citable; the only rectangular kernel-CDF gradient cost datum is a CPU one (the
~17× `value_and_grad`-over-forward anomaly of autolens_workspace_developer#117,
`searches_minimal/pix_prodigy_findings.md`), never re-measured on an A100. And the existing
`slam_source_pix*` targets are not the right shape to ask on: they free the lens light, the
mesh weights and every regularization parameter at once, which no SLaM stage does. This
prompt builds the cell that is the right shape.

## What to build

### 1. The model — `@autolens_profiling/scripts/misc/searches/_setup.py`

Add `_mass_pix_model`, alongside `_pixelization_model` (~line 1307) and
`_slam_source_pix_model` (~line 1394), which are the two closest templates.

- **Lens `bulge`** — the `Sersic` **instance** from
  `@autolens_profiling/dataset/imaging/hst/tracer.json` (galaxy 0, `bulge`): `intensity`
  2.0, `effective_radius` 0.6, `sersic_index` 3.0, `ell_comps` (0.0526, 0.0), `centre`
  (0.0, 0.0). **Load it from the file — do not retype the numbers.** The file is the
  provenance.
- **Lens `mass` and `shear`** — free, with the registry priors the other cells use:
  `Isothermal` (5) + `ExternalShear` (2) = **7 free parameters**.
- **Source** — instances, not models: `al.mesh.RectangularRTUAdaptImage` with
  `shape=_PIXELIZATION_MESH_SHAPE` ((39, 39)), `weight_power` **0.001**, `weight_floor`
  **0.248**; `al.reg.Adapt` with `inner_coefficient` **0.140**, `outer_coefficient`
  **226.169**, `signal_scale` **0.004**. Carry a provenance comment naming the certified
  `slam_source_pix_pos_fp64` reference: PyAutoCortex R-20260902-01, RAL job 342091 task t4,
  run identifier `4323a2ffcb3e50a71f229e46032d9e95`.
- Add the cell to **`_PIX_MODEL_TYPES`** so `use_border_relocator` follows it, exactly as
  the other mesh cells do.

### 2. The target — `@autolens_profiling/scripts/misc/searches/_targets.py`

Register model type `mass_pix`, giving the usual family `mass_pix[_pos]_{fp64,mp}`, so
`target_id` and `priors_ref` stamp on every result row. Positions convention: threshold
`auto` (resolving to 0.2), matching every certified mesh reference.

### 3. Per-cell sampler knobs — `@autolens_profiling/scripts/misc/searches/_samplers.py`

Rows for `imaging:mass_pix` in `_MULTI_START_N_STARTS_BY_CELL` (**16**),
`_MULTI_START_BATCH_BY_CELL` (**4**) and `_MULTI_START_N_STEPS_BY_CELL` (**3000**), and the
Nautilus `n_live` fiducial **150** (the reference arms run at 300, i.e. 2× the fiducial, as
every `InferenceRefs_v1` row does).

### 4. The drivers

Mirroring `@autolens_profiling/scripts/imaging/searches/nautilus/pixelization.py` and
`@autolens_profiling/scripts/imaging/searches/multi_start_prodigy_autoconv/pixelization.py`
— the same `_profiling_root()` preamble and a single `run_search(...)` call, nothing else:

- `scripts/imaging/searches/nautilus/mass_pix.py`
- `scripts/imaging/searches/multi_start_prodigy_autoconv/mass_pix.py`

### 5. The gradient probe — `scripts/misc/searches/probe_mass_pix_gradient.py`

Forward vs `value_and_grad` timing (ms/eval each, plus their ratio), jit compile time for
each, and a **strict finite-difference check on all 7 free parameters**. Follow the
FD-certification pattern of
`@autolens_workspace_test/scripts/imaging/jax_grad/pixelization.py`. This script is what
Cortex phase 20 runs.

### 6. HPC submits — `@autolens_profiling/hpc/batch_gpu/`

One per science phase, each with a **`WALL-BASIS`** block naming the measurement its wall
budget comes from (measured on this cell, never transferred from another):

- **P1** (Cortex phase 20) — the probe, one task.
- **P2** (Cortex phase 21) — Nautilus, two arms: `pos_tauto0.2_f1e8` and
  `pos_tauto0.2_f1e5`, n_live 300, seed 0, fp64.
- **P3** (Cortex phase 22) — `multi_start_prodigy_autoconv`, `pos_tauto0.2_f1e5`, seeds 0–4
  as an array 0–4.

**Write the P1 submit now; write P2's and P3's `WALL-BASIS` blocks after phase 20 rules** —
their wall basis is P1's measurement, which does not exist yet.

### 7. Bookkeeping

- Regenerate `@autolens_profiling/results/notes/inference/targets/TOLERANCES.md` so the new
  target's tolerances are listed.
- A CPU smoke of the model build: `JAX_PLATFORMS=cpu`, build the cell, assert **7** free
  parameters, run **one** forward eval and assert it is finite. No fit, no sampler.

## Out of scope

No RAL submission (that is a Cortex act, after this PR merges). No library code in
PyAutoArray / PyAutoGalaxy / PyAutoLens. No changes to the retired programme's ledgers, to
`output/legacy*` trees, or to the `slam_source_pix*` targets — they stay certified as
targets and are simply not what this epic runs on. The reg-free and MGE-at-ML lens-light
variants are the epic's unfiled work-up queue and are not built here.
