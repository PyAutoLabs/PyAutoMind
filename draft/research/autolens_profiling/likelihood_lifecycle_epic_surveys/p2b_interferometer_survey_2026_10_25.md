# Likelihood lifecycle 2b — interferometer campaign: survey and draft plan

Read-only survey, 2026-10-25, autolens_profiling main `29caed89`, PyAutoArray tags 2026.10.23.1 / 2026.10.25.1.
Nothing was edited, pushed, submitted or SSH'd. Paths below are relative to `lens/autolens_profiling` unless prefixed.

## 0. Headline findings (read first)

1. **No DFT cell is planned.** `_dft` and `_streaming` are `regime_only_suffixes` (`catalogue/provisional_designations.json:30-33`, read at `scripts/misc/tooling/catalogue_lifecycle.py:270-272`), so the 84 planned cells contain only `_nufft` (dense) and `_wtilde` (sparse) setups. The prompt's "NUFFT and DFT" overstates the scope. DFT would mean adding cells (ruling R2).
2. **Planned instruments come from the registry**, not from §3.3: `catalogue/registry.json:139-170` declares `interferometer/mge/sma` and `{rectangular, delaunay} × {sma, alma, alma_high, jvla}`. There are no sdp81 cells and no MGE cells above sma, although committed rows exist for them.
3. **Dense pixelized NUFFT is infeasible above sma in the library at either tag.** `TransformerNUFFT.transform_mapping_matrix` sends every column through one batched `nufft2d2` (PyAutoArray@2026.10.23.1 `autoarray/operators/transformer.py:601`). For MGE-20 that call already asks 61.4 GiB at alma, 300 GiB at alma_high and 1.46 TiB at jvla (`wiki/campaigns/interferometer/interferometer_likelihood_decision_matrix_2026_09.md:283`), and the pixelized source has about 1,280 columns. T alone (N_vis × S × 16 B) is 20.5 GB at alma, 102 GB at alma_high and 512 GB at jvla. The decision matrix already rules "Meshes on the A100: always W~, never dense" (`…decision_matrix_2026_09.md:37-40`). 24 of the 32 dense pixelized cells can't be measured on the production route (ruling R1).
4. **The 2a "production model" machinery is imaging-only.** `standard_size_preset` raises for anything except `delaunay_numba`/`pixelization_numba` (`_production_config.py:577-578`), `numpy_dense_reference` is built on `AnalysisImaging` (`_production_config.py:1365-1383`), and no interferometer preset exists (`preset_for` → KeyError, `_production_config.py:536-545`). The interferometer cells today run different models per script (see §2).
5. **The interferometer pixelized breakdown harnesses predate 2x and 1B.** `scripts/misc/likelihood_breakdown/interferometer_pixelized{,_numpy}.py` write no `resources` block (no `cpus_per_eval` / `peak_rss_gb`, only `peak_rss_mb` in a summary at `:1019`), no `fit.png` and no `parity.json`. **No interferometer numba runtime script exists** (`scripts/interferometer/{rectangular,delaunay}/` hold only `likelihood_breakdown_numba.py`).
6. **Keep pin 2026.10.23.1.** The only library change to 2026.10.25.1 relevant here is PyAutoArray#654/#655 (finufft on the NumPy path). It does not touch the per-call likelihood of any planned cell: JAX uses nufftax, and the numba W~ path never calls the transformer per evaluation. A 10.25.1 row would also make all 104 2a rows `stale`, because the catalogue pin is the newest record pin (`scripts/misc/tooling/coverage_matrix.py:14-17`). Ruling R5 has the details and one cost.
7. **jvla has never been measured on CPU** (`…decision_matrix_2026_09.md:287`). Every CPU jvla number is a projection, so batch 0 is essential.

## 1. The 84-cell work list

Source: `dashboard/coverage.json` (`likelihood` starts `interferometer/`). Coverage today: **83 missing, 1 stale** (the mge/sma `jax_gpu_dense_fp64_nufft [breakdown]` row from 2026.8.17.1). 20 of the missing cells are covered only by `size_fallback` rows at Delaunay 1500 / rect 39², all breakdowns from 2026.8.17.1.

Per (likelihood × instrument), each with runtime + breakdown:

| likelihood | instruments | `hpc_ral_cpu` setups (class) | `hpc_a100` setups (class) | cells |
|---|---|---|---|---|
| interferometer/mge | sma | `jax_cpu_dense_fp64_nufft` (opt) | `jax_gpu_dense_fp64_nufft` (opt) | 4 |
| interferometer/rectangular | sma, alma, alma_high, jvla | `numba_cpu_sparse_fp64_wtilde` (opt), `jax_cpu_sparse_fp64_wtilde` (sec), `jax_cpu_dense_fp64_nufft` (sec) | `jax_gpu_sparse_fp64_wtilde` (opt), `jax_gpu_dense_fp64_nufft` (sec) | 40 |
| interferometer/delaunay | sma, alma, alma_high, jvla | same | same | 40 |

**Per host:** RAL CPU **50** (sma 14 = 12 + 2 mge; alma 12; alma_high 12; jvla 12). A100 **34** (sma 10; alma 8; alma_high 8; jvla 8). By class: 36 optimal, 48 secondary. There is no `jax_cpu_*@hpc_a100` leg (unlike 2a), so the A100 jobs run GPU legs only.

Instrument geometry (`instruments/interferometer.py:39-101`, 3.5″ mask):

| inst | pixel | grid | masked px (≈π(3.5/ps)²) | mask extent / padded W~ FFT | N_vis | NUFFT chunk |
|---|---|---|---|---|---|---|
| sma | 0.1″ | 256² | ~3.8k | 70² / 140² | 190 | none |
| alma | 0.05″ | 800² | ~15.4k | 140² / 280² | 1.0e6 | none |
| alma_high | 0.025″ | 800² | ~61.6k | 280² / 560² | 5.0e6 | 1e6 |
| jvla | 0.01″ | 800² | ~384.9k | 700² / 1400² | 2.5e7 | 1e6 |

**Feasibility of the 32 dense pixelized cells (S ≈ 1,280):**

| inst | T = N_vis·S·16 B | A100 dense | RAL CPU dense |
|---|---|---|---|
| sma | 3.9 MB (one-shot grid 1280×512²×16 ≈ 5.4 GB) | feasible (library path) | feasible |
| alma | 20.5 GB; one-shot gather ≈ 61 GiB × 64 | library OOM; the chunked arm OOM'd at 50 cols (decision matrix :98-115); fits only with ≤5-column chunks | library infeasible; chunked arm ≈ 1,280 × ~0.65 s ≈ 14 min/call |
| alma_high | 102 GB | infeasible (> 80 GB) | chunked only; ~1 h/call, ≥256 GB `--mem` |
| jvla | 512 GB | infeasible | infeasible (T + copies > 921 GB node) |

## 2. Gaps that need code before runs (PR A)

| # | Gap | Evidence | Fix |
|---|---|---|---|
| A1 | **The interferometer cells don't share a model.** JAX runtime Delaunay: Hilbert 1500, `weight_power=1.0, floor=0.0`, `zeroed_pixels=0`, `ConstantSplit(1.0)`. JAX runtime rect: 32², `Constant(1.0)`. Harnesses: Delaunay 1500 `AdaptSplit(0.1,10,0.1)`, rect 39² `Constant`. | `scripts/interferometer/delaunay/likelihood_runtime.py:158,298,335-337`; `rectangular/likelihood_runtime.py:121,269-270`; `scripts/misc/likelihood_breakdown/interferometer_pixelized.py:460-509` | Add an interferometer standard preset to `_production_config.py`, borrowing hst `source_pix[2]`: Delaunay 1250 Hilbert (wp 3.5, floor 0.01) + 30 zeroed edge points, `AdaptSplit`; rect `RectangularBilinearAdaptImage` 35² + `reg.Adapt` with production weight priors (`_production_config.py:373-415`). No lens light, over-sampling or positions, which the interferometer has none of. The adapt image is the truth lensed source (`_adapt_image_util.py`), with no S/N cap (R3). Wire `--standard-size` into both JAX runtime scripts, both harnesses and the new numba runtime, so every setup of a likelihood × instrument evaluates one likelihood (2a ruling N1). |
| A2 | **No numba runtime script** | only `likelihood_breakdown_numba.py` exists | New `scripts/interferometer/{rectangular,delaunay}/likelihood_runtime_numba.py`, mirroring `scripts/imaging/*/likelihood_runtime_numba.py`: threads pinned to 1, warm iid median and cold evals, through the library's `FitInterferometer(xp=np)` default route. Add `catalogue/script_routes.json` entries and WALL-BASIS gate cells. |
| A3 | **The numba arm forces direct_conv** (`--numba-gate` default 1e9) instead of the production cost-model route | `delaunay/likelihood_breakdown_numba.py:31`; `interferometer_pixelized_numpy.py:24,202`; Pulse `decisions/interferometer-route-gate-cost-model.md` | The headline `numba_cpu_sparse_fp64_wtilde` should measure the packaged default (cost model; at jvla it will pick FFT). Keep both arms in the breakdown, record the chosen route, and cap `--n-instances` at jvla (R4). |
| A4 | **No dense breakdown row.** The JAX harness puts the dense arm inside the *sparse* row as `dense_steps`, so it can never fill a `jax_*_dense_fp64_nufft [breakdown]` path. It is also off above `--dense-max-vis` 200,000 (`interferometer_pixelized.py:128,172-177,1364`). | — | Add a `--dense` primary mode that writes the dense arm as its own row at the `_nufft` setup path. Run the JAX runtime script's dense leg (no `--sparse`) only where R1 keeps it. |
| A5 | **No `resources` / `fit.png` / `parity.json` in the pixelized harnesses** | grep: `resources_dict` and `render_fit_png` absent from `interferometer_pixelized{,_numpy}.py`; only `peak_rss_mb` (`:1019`) | Call `_profile_cli.resources_dict` (numba: `cpus_per_eval` 1; JAX CPU: NPROC; GPU: one device), `render_fit_png(..., dataset_type="interferometer")` (supported, `_profile_cli.py:1284,1300-1303`) and the parity writer. Check that the mge runtime/breakdown already carry resources; the runtime scripts call `render_fit_png`. |
| A6 | **The parity reference is imaging-only** (`AnalysisImaging`) | `_production_config.py:1365-1383` | Add an interferometer reference: eager NumPy **dense** `AnalysisInterferometer(use_jax=False)` with no sparse operator, independent of W~. At sma use the library path. At alma, alma_high and jvla the library dense path is infeasible (§1), so add a **visibility-chunked dense reference** that accumulates `F = Σ Tₖᵀ N⁻¹ Tₖ` and `D` over visibility chunks (memory O(S² + chunk·S)). Compute it **once per (instrument, mesh, instance)** in a reference task and cache it for every setup's `parity.json` (R6 for cost; R7 for tolerance). |
| A7 | **The generator is imaging-shaped**: `"imaging"` literals, `SETUPS`, `masked_pixels × 1340` memory model, and `jax_cpu@a100` folded into GPU jobs | `scripts/misc/campaigns/imaging_p2a.py:46-72,165-224,230-300` | Factor the submit rendering (`render`, `_wall_rows`, `_bash_array`, the pin/import guard, `prepare_dataset` lock, walls.tsv) into `campaigns/_common.py`, with `imaging_p2a.py --check` byte-identical. Then add `campaigns/interferometer_p2b.py` with its own task table, flags, an N_vis-aware memory model (A8) and tests. Run `wall/check_submits.py --check`. |
| A8 | **Memory model per instrument** | §1 tables | Batch-0 `--mem`, as a declared estimate. **RAL:** sma 32 GB; alma 32 GB; alma_high 64 GB; jvla 128 GB (L = 384,852 × 1,280 × 8 B = 3.9 GB, dataset ≈ 1.2 GB, nufftax CPU prep chunks ≈ 2.7 GB, JAX CPU W~ FFT batches, compile temps). The chunked dense reference task: alma 64 GB, alma_high/jvla 64 GB with 2.5e5-vis chunks. **A100:** one GPU, `--mem` 64 GB host; jvla W~ ≈ 7.7 GB/replica (`scripts/misc/vram/config.py:106`). Batch 1 takes sacct MaxRSS × 1.5 rounded up, as in 2a. |
| A9 | **jvla dataset and caches** | not in the local `dataset/interferometer/` | `prepare_dataset` simulates jvla once per instrument under the lock (25M vis, about 0.8 GB FITS), writes `lensed_source.fits`, and pre-builds the W~ preload cache (`--preload-cache on`) so legs don't race. |
| A10 | **Designation and coverage changes**, only if R1 (dense regime) or R2 (DFT) is ruled | `provisional_designations.json`, `build_catalogue.py:1270-1287` | Regenerate `catalogue.json` → `coverage.{json,md}`; `build_catalogue --check --validate-with ../PyAutoPulse`. |

## 3. Human rulings needed (with recommendations)

- **R1. Dense pixelized NUFFT above sma (24 cells).** Options:
  - (a) Add a regime rule (like `_dft`) so dense pixelized `_nufft` is planned only at N_vis < 1e5 (sma). Planned interferometer cells go 84 → **60** (RAL 38, A100 22).
  - (b) Keep the cells and record them as limitations: fail-fast legs, as with 2a's two ao OOMs.
  - (c) Measure the chunked, non-library arm where it fits: A100 alma at ≤5-column chunks; CPU alma and alma_high. This measures a route the library does not run.
  
  **Recommend (a)**, plus one alma A100/CPU frontier probe written to `experiments/` as evidence. It matches decision-matrix rule 2 and keeps "missing" meaningful.
- **R2. DFT.** No DFT cell is planned. **Recommend** no new planned cells. Optionally run mge/sma `--use-dft` (`scripts/interferometer/mge/likelihood_runtime.py:122`) as an `experiments/` row, since sma at 190 vis is the one in-regime instrument.
- **R3. The "production model" for the interferometer.** No interferometer production preset or pipeline exists in subhalo_validation/euclid. **Recommend** the hst `source_pix[2]` mesh and regularisation at the standard size: Delaunay 1250 + 30 edge with AdaptSplit, rect 35² `RectangularBilinearAdaptImage` + Adapt. This matches the workspace interferometer SLaM (`autolens_workspace/scripts/interferometer/features/pixelization/slam.py:592-603`; `delaunay.py:217`). Use the truth lensed-source adapt image (as 2a's truth tracer stand-in) with no S/N cap. MGE stays MGE-20, unchanged.
- **R4. The numba headline route and iid count.** **Recommend** the packaged cost-model route as the headline, with the forced direct_conv and NumPy FFT arms kept as sub-rows. Use `--n-instances` 20 for sma/alma, 10 for alma_high and 5 for jvla: the projected jvla direct_conv is about 540 s/call against about 60–100 s for FFT.
- **R5. Pin.** **Recommend keeping 2026.10.23.1.**
  - The library diff to 10.25.1 is finufft on the NumPy path only (`git log 2026.10.23.1..2026.10.25.1`: PyAutoArray 157e210c, 3f3c8619; Fit, Galaxy and Lens changes are unrelated).
  - Per-call timings of the planned cells are unchanged.
  - A 10.25.1 row would stale every 2a row (`coverage_matrix.py:14-17`).
  - The RAL shared venv probably lacks `finufft` and must not be changed, because euclid_dr1 uses it.
  - Cost: the eager dense references run nufftax on CPU, about 25–35× slower than finufft (Aris memory, RAL 412863). That makes the jvla reference roughly 6–10 h, done once.
  - Phase 3 day-zero re-pins anyway.
- **R6. The parity reference at jvla.** **Recommend** the visibility-chunked eager dense reference (A6) as one dedicated RAL task per mesh, about 6–10 h at 64 GB. Fallback if refused: eager NumPy W~ via the FFT route (`interferometer_route` forced), labelled `reference: numpy_wtilde_fft` with a limitation. It is independent of JAX and numba but not of the W~ algebra.
- **R7. Parity tolerance.** The 2a gate is 1e-4·|ref| (1e-3 mp). At |logL| ≈ 3.0e8 (jvla) that is about 30,000 nats, which proves nothing; existing W~ vs dense agreement is ≤1e-6 nats at sma, and GPU vs CPU 8.7e-7 at alma. **Recommend 1e-8·|ref|** fp64 for the interferometer (≈3 nats jvla, 0.12 alma, 3e-5 sma), keeping 1e-3 for mp. Alternatively keep 1e-4 for uniformity and pre-register the 1e-8 bound as the wiki verdict.
- **R8. Batch-0 bounding cells.** **Recommend** jvla for every sparse and numba setup, since it has the largest mask and N_vis and was never measured on CPU. Under R1(a), add sma for every dense setup and mge:
  - RAL 14: jvla numba ×4, jvla jax_cpu sparse ×4, sma jax_cpu dense ×4, mge sma ×2.
  - A100 10: jvla gpu sparse ×4, sma gpu dense ×4, mge sma ×2.
  - Optionally the 2 jvla dense-reference tasks, so their wall is measured.
- **R9. Instrument scope.** Planned = registry (no sdp81; mge sma only). **Recommend** no change: mge alma+ dense OOMs, and the mge W~ route isn't a §3.3 setup.
- **R10. Heart RED.** Each PR needs a per-task RED override, as for 2x.

## 4. Plan

**High level**
1. Rulings R1–R9. The coverage matrix then fixes the work list (84, or 60 under R1a).
2. PR A (laptop code): interferometer standard preset, the numba runtime scripts, the dense breakdown mode, resources/fit.png/parity in the harnesses, the chunked dense reference, and the `interferometer_p2b.py` generator with shared submit code.
3. Batch 0 (human go): the bounding cells on RAL `ral` + A100 `--gres`, into a gitignored `output/p2b_batch0/`.
4. A follow-up PR sets batch-1 `--time`/`--mem` from batch-0 walls and MaxRSS, plus any harness fixes (2a needed #458/#460).
5. Batch 1 (human go): all cells into the scratch `output/p2b_batch1/results/`.
6. PR B: copy only complete rows; supersede the old ones; regenerate catalogue and coverage; write the wiki page; refetch Pulse.

**Detailed**

- **PR A** (branch `feature/likelihood-lifecycle-p2b-…`; tier judge, human `/prm`):
  1. `_production_config.py`: `interferometer_standard_preset(mesh, instrument)` (A1/R3), and `interferometer_dense_reference(...)`, visibility-chunked (A6).
  2. JAX runtime ×2: `--standard-size`, a dense leg without `--sparse` (sma only under R1a), resources (already present), `parity.json`.
  3. Harnesses: `--standard-size`, `--dense` primary mode (A4), resources, fit.png, parity, and the R4 numba route and instance cap.
  4. New `likelihood_runtime_numba.py` ×2, plus routes.
  5. mge runtime/breakdown: parity writer (eager NumPy dense at sma).
  6. `campaigns/_common.py` + `interferometer_p2b.py`:
     - tasks, flags, `--config-name` `hpc_ral_cpu_fp64` / `hpc_a100_fp64`;
     - per-instrument RAL arrays on `--partition=ral` and per-instrument A100 jobs with `--gres=gpu:1`;
     - batch-0 submits with WALL-BASIS `source: unmeasured`;
     - a reference-task submit;
     - the guards from 2a: pin 2026.10.23.1, `PYAUTO_PRIVATE_BASE`, a `library_revisions` check, `walls.tsv` START/WALL.
  7. Tests: generator, standard-preset equality between JAX and numba, parity writer, and a smoke run on sma at the laptop size.
  8. If R1(a): edit the designations and regenerate the catalogue and coverage.
  9. Witness: `imaging_p2a.py --check` unchanged, `interferometer_p2b.py --check`, `wall/check_submits.py --check`, pytest, ruff, `build_catalogue --check --validate-with ../PyAutoPulse`.
- **Batch 0** (human go): a new private RAL checkout of autolens_profiling at the PR A merge (do not reuse the dirty p2a tree), with the libraries from `/mnt/ral/jnightin/profiling/PyAuto_2026.10.23.1`.
  - Pre-flight: `pip freeze` floors on the shared venv (nufftax ≥ 0.6.1, jax and jaxlib match the laptop); dataset prep for jvla.
  - Submit the RAL `ral` array (14) and the A100 array `%2` (10), plus optionally the 2 jvla reference tasks.
  - Declared guesses: RAL `--time` 12:00:00 (jvla numba breakdown ≈ 4–6 h projected); A100 6:00:00.
- **Wall/mem PR**: `BATCH0_WALLS` and the MaxRSS peaks go into the generator; batch-1 `--time` = 1.25 × basis leg + 15 min, rounded to 30 min, and `--mem` = the next step ≥ 1.5 × peak with a 32 GB floor. Any limitation found in batch 0 is recorded as a human ruling, like 2a's ao OOMs.
- **Batch 1** (human go):
  - RAL: 4 per-instrument arrays (sma 14, alma/alma_high/jvla 12 each; or 8 each under R1a).
  - A100: 4 per-instrument jobs (sma 10; others 8, or 4 under R1a).
  - Reference tasks: 2 per instrument above sma (rect, delaunay), unless they are already in batch 0.
- **PR B**:
  - Copy only complete cells: final row, `fit.png`, `parity.json` with `parity_witness.py --check` passing, and `library_revisions` matching the pin.
  - Move the 20 size_fallback rows and the stale mge row to `history/<pin>_<date>/`.
  - Regenerate the catalogue, dashboard and coverage; the target is zero missing or stale for this campaign.
  - Wiki page `wiki/campaigns/interferometer/likelihood_lifecycle_p2b.md`. Pre-registered rule: every cell current, with parity `match` at the R7 tolerance; any divergence blocks that setup. Expected verdict: W~ is optimal on both hosts, with a cost-model FFT pick at jvla CPU. Results are framed as projected node throughput, never as a latency-only "GPU N× faster".
  - Refetch the PyAutoPulse lens receipt (Pulse PR, `pyauto-pulse check`). There is no Pulse task to adopt; the `interferometer` campaign is parked at knowledge-complete.

## 5. Risks

- **OOM.**
  - A100 dense at alma and above (certain); the R1 ruling removes or labels it.
  - The JAX CPU W~ jvla compile temps are unmeasured, so start at 128 GB.
  - The chunked dense reference at jvla needs the chunk sized below 64 GB.
  - The old sma JAX cell hit 14.6 GB RSS from the one-shot dense transform (`interferometer_pixelized.py` docstring).
- **Wall.** jvla CPU is unmeasured. Projections: numba direct_conv ≈ 540 s/call, FFT ≈ 60–100 s, JAX CPU W~ ≈ 50–70 s; a 20-instance breakdown could exceed 12 h, hence R4's caps and batch 0. The nufftax CPU prep at 25M vis adds minutes, plus the preload build.
- **numba fork segfault** (Aris, RAL 412871–74). It does not apply to these single-process legs. It matters for phase 4 multi-worker runs: an interferometer parent never calls numba before the fork. Note it on the wiki page; no action in 2b.
- **finufft availability.** It is not needed at the 10.23.1 pin. If the human picks 10.25.1, the shared venv must not be modified (euclid_dr1): use a private overlay. Without finufft the NumPy path falls back to nufftax with a warning, which is a reproducibility hazard.
- **RAL dependency drift.** The venv once held nufftax 0.4.0 against a ≥ 0.6.1 floor, which caused a GPU fp32 Pallas precision loss (memory `feedback_ral_sync_check_misses_dependency_floors_nufftax`). Pre-flight `pip freeze` on the venv.
- **Delaunay bistability.** About 1e-8 relative logL jitter between the scipy and JAX walks (`delaunay/likelihood_breakdown_numba.py` pinned note). It sits inside R7's 1e-8·|ref|, but tight at sma; record the absolute delta.
- **Coverage churn.** R1(a) changes `planned_cells` and the Pulse coverage expectation, so the catalogue must regenerate and validate in PR A, not PR B.
- **Shared RAL.** Never touch euclid_dr1 jobs; CPU only on `ral`; private checkouts only (never HPCPullPyAuto the shared mirror).
