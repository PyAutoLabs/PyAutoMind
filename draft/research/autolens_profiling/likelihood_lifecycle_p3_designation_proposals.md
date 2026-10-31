# Likelihood lifecycle phase 3: designation proposals for the completed campaigns (2a imaging, 2b interferometer, 2c point source) — DRAFT for the human

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
- dashboard
Difficulty: large
Autonomy: human-required
Priority: high
Status: draft proposals for the human — never issued itself; no Pulse decision record exists or is implied, and `catalogue/provisional_designations.json` is unchanged. The phase 3 prompt (filed after the "campaigns complete" gate) cites this file
Consequence: judge
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-29

Written 2026-10-29 (Opus 5.5) from autolens_profiling `main` at 32c0becd (`dashboard/catalogue.json` generated 2026-10-29T09:46:25Z, `dashboard/coverage.json`, `catalogue/provisional_designations.json`, `catalogue/reference_hosts.json`, and the campaign pages below) and PyAutoPulse `main` at 4a4bdee (`decisions/README.md` "Designation decisions", `REFERENCE.md`, `pulse/decisions.py`). No repo code was changed, no decision recorded, no compute submitted.

## Re-derivation 2026-10-31 on the day-zero catalogue (supersedes Appendix A for the record step)

Re-derived from autolens_profiling PR #496 head `c218a428` (`dashboard/catalogue.json`). That is main after #494 (the quiet reruns) plus every 2a–2c JAX row on jax/jaxlib 0.11.2, which is the catalogue main will hold once #496 merges. It covers all seven campaigns (2a–2g) on the axis the human fixed on 2026-10-30:
- **Q1/Q3:** rank by projected calls/s per node within each hardware class. A setup separates when the winner beats the runner-up by more than the larger recorded p10–p90 spread, or by more than the 9 % arm-to-arm noise when no spread is recorded.
- **Q2/Q11:** `gpu_a100` means GPU setups only, with GPU-only secondaries.
- **Q5:** interferometer is designated by `standard`, with an instrument-keyed rule.
- **Q10:** untested branches are named in the rule.

The generator scripts are `designate.py` and `appendix_b.py` (session scratch, reproduced in the PR that records the decisions). Every entry passes `pulse.decisions._designation`.

**Result: 40 likelihood × hardware-class groups. 39 can be designated (21 separated, 18 uncontested) and 1 holds.**

- **Hold:** `datacube/delaunay` `gpu_a100`. At sma, `jax_gpu_sparse_fp64_wtilde` 3.46 against `jax_gpu_dense_fp64_nufft` 3.37 calls/s/node is 1.03×, inside the 9 % tolerance; alma and alma_high measured only W~ sparse. It keeps its §3.3 provisional label.
- **Changed since 2026-10-29:**
  1. `interferometer/delaunay` `cpu_many_core`, jvla: the old **HOLD (25 %) now separates.** Numba is 1.22 against JAX 0.564 calls/s/node (2.17×). The quiet rerun sped numba up (0.87×) and jax 0.11.2 plus the eigen flag slowed JAX CPU W~ down (1.50×).
  2. `point_source_source/source_plane` `gpu_a100`: the old draft proposed the node CPU (`jax_cpu_na_fp64`). Under Q2 it is `jax_gpu_na_fp64`. This follows the ruling, not new data.
  3. The interferometer ids are now `…-standard-…` instead of the n_vis bins (Q5). The optimal setup is the same in every old bin.
- **Unchanged:** every 2a and 2c proposal keeps its optimal setup.
- **The JAX CPU slowdown flips nothing.** Every CPU group with a numba setup was already numba, by 2.2–35× per node. JAX-only CPU groups (MGE, point source, cluster, weak) are uncontested.
- **New groups (2d–2g):**
  - group, multi_galaxy and multi_dataset follow imaging: numba on CPU, `jax_gpu_dense_fp64` on the A100, all separated.
  - datacube on CPU: numba W~, separated.
  - cluster and weak: uncontested JAX.
- **Caveats:**
  - imaging/rectangular euclid numba has no MaxRSS (sacct missed the task), so it has no projection; that instrument is ranked per call (numba 3.22× JAX).
  - Uncontested groups rest on one measured setup.
  - Projections are upper bounds: η = 1.0, declared and unmeasured until phase 4. Every record says `basis: projected` in its prose (Q4 option a).

**For the human (the record step):** approve the 39, or name the ones to hold, and confirm the datacube A100 hold. On approval the conductor writes the 39 `decisions/<id>.md` and `decisions.yaml` rows in PyAutoPulse, then the producers re-declare `class: optimal` + `decision_id` on the cited rows (autolens_profiling), and `pyauto-pulse check` must resolve them.

## What this is, and what it is not

The epic's rule (ledger Summary; report §3.2) is that an optimal setup is always a Pulse `designation` decision made by the human, never inferred. Phase 3 (ledger card; report §4 "Phase 3") must produce: a pinned released tag with every Optimal/Secondary cell measured on it, `day_zero` stamped, a Pulse `day_zero` snapshot, **one `designation` decision per likelihood × hardware class (the conductor drafts, the human records)**, `wiki/campaigns/<dataset_type>/<variant>/day_zero.md` decision-rule notes, the Pulse `setup-baseline` campaign adopted and closed with its 1,044-slot manifest replaced, no `not_measured` Optimal cell on Coverage, and the `runtime_estimates` export. Phase 3 is gated on the human's "campaigns complete" confirmation, which has not happened (2d–2g have not run on RAL).

This file is the "conductor drafts" part for the three campaigns that are complete. For each likelihood × hardware class it gives the §3.3 provisional setups, the measured evidence, a proposed optimal and secondary, a one-line reason, whether it confirms or overturns §3.3, and the caveats that could change the call. Appendix A holds each proposal as a draft `decisions.yaml` entry in the shape `decisions/README.md` specifies; all 26 pass `pulse.decisions._designation` (run against PyAutoPulse `pulse/decisions.py`, identical to `main`). They are drafts: the `date` is a placeholder for the human's decision date, and nothing is in any index.

Sources:

- Campaign pages (autolens_profiling 32c0becd): imaging [`wiki/campaigns/imaging/likelihood_lifecycle_p2a.md`](https://github.com/PyAutoLabs/autolens_profiling/blob/32c0becd/wiki/campaigns/imaging/likelihood_lifecycle_p2a.md) (#461, #467; 106/106 current); interferometer [`wiki/campaigns/interferometer/likelihood_lifecycle_p2b.md`](https://github.com/PyAutoLabs/autolens_profiling/blob/32c0becd/wiki/campaigns/interferometer/likelihood_lifecycle_p2b.md) (#471, #483; 60/60); point source [`wiki/campaigns/point_source_source/source_plane/likelihood_lifecycle_p2c.md`](https://github.com/PyAutoLabs/autolens_profiling/blob/32c0becd/wiki/campaigns/point_source_source/source_plane/likelihood_lifecycle_p2c.md) and its [image-plane twin](https://github.com/PyAutoLabs/autolens_profiling/blob/32c0becd/wiki/campaigns/point_source_image/image_plane/likelihood_lifecycle_p2c.md) (#480; 10/10; human ruling: the published runtime is the Solved likelihood).
- Node throughput: phase 2x (#463, #465, PyAutoPulse#77), the `projected_node_throughput` block on every runtime record.
- Every current runtime row of these likelihoods is on `release_pin` 2026.10.25.1 (imaging rows measured on 2026.10.23.1 and carried by the declared `carry_forward`, #466/#467).

## The comparison axis (pre-registered by the report; restated, not chosen here)

The report's "Amendment 2026-10-25: node throughput" (human-approved) fixes the axis before the data: keep **separate** Optimal GPU and Optimal CPU designations; within each, **rank by projected throughput on the named hardware budget (calls per second per node)**, with per-call latency only as secondary evidence; designations made before phase 4 carry `basis: projected` and are revisited when phase 4 measures the parallel efficiency η. The proposals below follow that axis and say where the per-call axis would give a different answer. Two gaps the report leaves open are questions for the human (Q2, Q4): whether a GPU node's "hardware budget" includes its 124 CPU cores, and where `basis: projected` goes, since the Pulse designation schema refuses any field it does not list.

Mapping used: host class `hpc_a100` (RAL gpu node, 4 × A100 80GB PCIe, 124 cores, 885 GB) → `hardware_class: gpu_a100`; `hpc_ral_cpu` (RAL ral node, declared 236 cores, 921 GB) → `cpu_many_core` (`catalogue/reference_hosts.json`). `laptop` has no current evidence (R7: laptop rows are never current), so no laptop proposal is made (Q6).

## How to read the evidence tables

- **Headline per call**, by the basis the campaign pages define: JAX `single-jit median` (median of individually timed calls after the warm calls; 200 calls in 2a/2c), or `single-jit block mean †` where the leg recorded only the one-block mean (catalogue `metric: single_jit_block` on a JAX row); numba `warm iid median` (median over seeded iid draws after the compile: 16 in 2a; 16/16/6/1 at sma/alma/alma_high/jvla in 2b, per the 2b page). For 2b numba rows the forced `direct_conv` and NumPy FFT route arms are shown beside the cost-model pick (2b ruling R4).
- **p10–p90**: the single-jit spread recorded in the row (`full_pipeline_single_jit_p{10,90}_ms`); absent on † rows and numba rows.
- **vmap per call [batch]**: batch time / batch size at the batch the script chose. It is the per-call source of every JAX row's projection (`per_call_source: vmap.per_call`); numba's is the warm iid median.
- **Projected calls/s per node**: `projected_node_throughput.hosts[0]` — workers = min(cores / cores per call, node memory / peak RSS), or one per GPU, × η (declared 1.0, an upper bound, unmeasured) / per-call time; each row projected only onto the node class it was measured on (#464). Not modelled: Nautilus `n_batch`, shared memory bandwidth.
- **Peak RSS** is the row's (2b/2c) or the sacct backfill's (2a: exact per RAL leg; the multi-leg A100 job's peak, an upper bound, on A100).
- **Parity** is the cell's witness status from the catalogue's `parity_witnesses` (all 88 cell witnesses here — 53 imaging, 30 interferometer, 5 point source — `match`; 0 `diverged`).
- **Rounding**: one rule for every number below, applied to the record value: per-call times to 4 significant figures (integers with separators from 1,000 ms), projections and RSS to 3 significant figures. The campaign pages round some values one digit differently (e.g. 0.1986 ms prints as 0.20 on the 2a page and 0.1986 here); the record id is the source.
- **Record ids are path-hashed** (2b page, Journal 2026-10-29): when the quiet-rerun ingest replaces a RAL CPU row in place, the same id will name the new row. Re-resolve every evidence id at the freeze commit before recording a decision.

## Cross-cutting caveats (referenced as C1–C9 below)

- **C1 RAL CPU load.** 2a RAL CPU rows: load average 8.6–37 at write (2a page). 2b: every RAL CPU row started at a 1-minute load of 45–72 on euclid-ral-compute-1 (2b page, "Load"). 2c: the two solved RAL CPU runtime rows started at 33.4 on euclid-ral-compute-10-5 (2c page). All are refused as dashboard trend points (cap 8) but stay `current`. The quiet reruns RAL 413267 (2c, 2 legs) and 413268–413271 (2b, 38 legs) are queued (`likelihood_lifecycle_p2bc_quiet_rerun_ingest.md`; their state was not checked from this session, RAL is not mounted here), so **every 2b and 2c RAL CPU number may move**. The 2a RAL CPU rows are **not** in the rerun.
- **C2 A100 host.** Every A100 runtime row here ran on euclid-ral-gpu-1; the release sweep pins euclid-ral-gpu-2 (`hpc/release_sweep.conf`), so they are flagged off-host on the run-time dashboard. Comparisons inside `gpu_a100` are all on gpu-1, so they are like-for-like with each other. A100 load at write: 9–13 (2a), 1–7 (2b), ≤ 2.5 (2c).
- **C3 Close calls.** Where two setups sit inside each other's p10–p90, or within a few per cent with no spread recorded, the evidence does not separate them; each is named where it occurs.
- **C4 jax version and the XLA:CPU deadlock.** Every current 2a/2b/2c row records `jax`/`jaxlib` **0.10.2** (`identity.software`; checked in the raw rows) and `XLA_FLAGS` without `--xla_cpu_multi_thread_eigen=false`. The jaxlib 0.11.2 XLA:CPU deadlock (PyAutoPulse `knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md`; decision `xla-cpu-deadlock-eigen-workaround`, D12) was found on 0.11.2 and is untested for these executables. But tag 2026.10.25.1's PyAutoNerves declares `jax>=0.7.0,<0.12.0,!=0.10.*,!=0.11.0` ("CPU batched LAPACK can deadlock in 0.10.x / 0.11.0 (Heart#274)", commit 249ba9e, 2026-10-04): **the JAX evidence was measured on a jax the pinned tag excludes**, while the superseded 2026.10.17.1 point-source rows recorded jaxlib 0.11.2 and the 2d–2g legs will run on 0.11.2 with the D12 flag (+25 % per call on laptop group/mge against the deadlocking default; within ~15 % on pixelized cells). A 2a/2b/2c JAX CPU row is therefore not like-for-like with a 2d–2g JAX CPU row on two axes (jax version, eigen flag). Numba rows (numba 0.65.1) are not affected by the jax version. This is Q7 and the largest open item for the freeze.
- **C5 Mixed precision** is `experimental` everywhere (R4; footnote to §3.3). No mixed-precision row exists in 2a–2c, so no proposal names one.
- **C6 Per call vs per node.** Within one hardware class the two axes agree everywhere except: imaging/delaunay euclid on RAL (per-call tie), interferometer pixelized alma_high and jvla on RAL (JAX CPU faster per call, numba ahead per node), and point-source source plane on the A100 node (per-call tie, CPU cores ahead per node). Across classes (which hardware a fit should request), a ral node is projected ahead of a 4×A100 node for interferometer pixelized at sma and alma but behind it at alma_high and jvla (2b headline), and ahead on hst Delaunay imaging but behind on ao (2a). That cross-class choice is phase 5's (`setup="auto"` when both are present), not a designation; it is stated here because it is the same axis question.
- **C7 JAX CPU cores per call.** Every JAX CPU row ran with 8 threads (`cpus_per_eval` 8), so a ral node projects 29 JAX CPU workers against 236 numba workers. A JAX CPU leg with fewer threads per call was never measured, so the per-node rank of JAX CPU against numba is conditional on that thread count.
- **C8 Projection source.** Projections use vmap per call, which on some rows is slower than the single-jit median (e.g. interferometer rectangular alma A100: vmap 51.22 ms [3] against single-jit 36.01 ms; interferometer/mge sma RAL: 112.5 against 90.63 ms). No within-class ordering below changes if the single-jit median is used instead.
- **C9 Phase 4.** η is declared 1.0 (upper bound). The CPU projections (hundreds of workers sharing memory bandwidth) are the most optimistic (2a page). Phase 4 measures η per setup and host; any designation here is `basis: projected` until then (report amendment).

## Evidence (current runtime rows; size-variant 28² rows excluded)

The four `size_variant` rows at hst rectangular 784 source pixels (`source_pixels_784/`, autolens_profiling#468, the rect28 rows for autolens_inference) are current but not the standard size, so they are not evidence for a standard-regime designation.

### Evidence: imaging/delaunay

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| euclid | `jax_cpu_sparse_fp64` @ A100 node | 1,146, single-jit median | 1,127–1,169 | 857.4 [3] | 8 | 1.91 | 17.5 (15, cores) | match | `lifecycle/a9e102b324300939da14` |
| euclid | `jax_gpu_dense_fp64` @ A100 node | 44.73, single-jit median | 44.24–45.63 | 14.80 [64] | 8 | 1.91 | 270 (4, gpus) | match | `lifecycle/c07af59a8d393975dd28` |
| euclid | `jax_gpu_sparse_fp64` @ A100 node | 46.85, single-jit median | 46.67–47.30 | 18.16 [64] | 8 | 1.91 | 220 (4, gpus) | match | `lifecycle/371f67d50254479493ee` |
| euclid | `jax_cpu_sparse_fp64` @ RAL | 1,122, single-jit median | 1,100–1,165 | 826.6 [3] | 8 | 1.74 | 35.1 (29, cores) | match | `lifecycle/b202eb6f7da58a38882f` |
| euclid | `numba_cpu_sparse_fp64` @ RAL | 820.0, numba warm iid median | — | — | 1 | 0.551 | 288 (236, cores) | match | `lifecycle/5556ca430bc180c2d536` |
| hst | `jax_cpu_sparse_fp64` @ A100 node | 2,562, single-jit block mean † | — | 2,110 [3] | 8 | 10.7 | 7.11 (15, cores) | match | `lifecycle/0f45aa8eb79d60157031` |
| hst | `jax_gpu_dense_fp64` @ A100 node | 59.58, single-jit median | 59.19–60.42 | 35.05 [16] | 8 | 10.7 | 114 (4, gpus) | match | `lifecycle/73c19173fcc983318b61` |
| hst | `jax_gpu_sparse_fp64` @ A100 node | 76.23, single-jit median | 75.45–76.79 | 47.93 [16] | 8 | 10.7 | 83.5 (4, gpus) | match | `lifecycle/12c678df16e04f4f9011` |
| hst | `jax_cpu_sparse_fp64` @ RAL | 2,221, single-jit block mean † | — | 1,895 [3] | 8 | 3.20 | 15.3 (29, cores) | match | `lifecycle/06a9dad80c65ecd81c6c` |
| hst | `numba_cpu_sparse_fp64` @ RAL | 951.7, numba warm iid median | — | — | 1 | 0.854 | 248 (236, cores) | match | `lifecycle/321ec1f6f2a5955a9a20` |
| jwst | `jax_cpu_sparse_fp64` @ A100 node | 5,086, single-jit block mean † | — | 4,686 [3] | 8 | 7.38 | 3.20 (15, cores) | match | `lifecycle/97d2ae3cab5f9bbc9d8f` |
| jwst | `jax_gpu_dense_fp64` @ A100 node | 88.63, single-jit median | 87.74–90.16 | 72.29 [8] | 8 | 7.38 | 55.3 (4, gpus) | match | `lifecycle/12348bea7be2ca70cffb` |
| jwst | `jax_gpu_sparse_fp64` @ A100 node | 124.2, single-jit median | 124.0–124.6 | 108.1 [8] | 8 | 7.38 | 37.0 (4, gpus) | match | `lifecycle/d34ebb3d52e02dfb8b16` |
| jwst | `jax_cpu_sparse_fp64` @ RAL | 4,759, single-jit block mean † | — | 4,361 [3] | 8 | 5.58 | 6.65 (29, cores) | match | `lifecycle/b5b87c504713b9831857` |
| jwst | `numba_cpu_sparse_fp64` @ RAL | 1,745, numba warm iid median | — | — | 1 | 1.98 | 135 (236, cores) | match | `lifecycle/d93b4dad29e8a0f77987` |
| ao | `jax_cpu_sparse_fp64` @ A100 node | 56,742, single-jit block mean † | — | 57,179 [1] | 8 | 39.8 | 0.262 (15, cores) | match | `lifecycle/780ad479b1fe66279696` |
| ao | `jax_gpu_dense_fp64` @ A100 node | 368.2, single-jit median | 363.9–371.5 | 366.9 [1] | 8 | 39.8 | 10.9 (4, gpus) | match | `lifecycle/fa028d54604cd08d3555` |
| ao | `jax_gpu_sparse_fp64` @ A100 node | 886.7, single-jit median | 885.9–887.5 | 935.3 [1] | 8 | 39.8 | 4.28 (4, gpus) | match | `lifecycle/99d7c3c7623e3d43d059` |
| ao | `jax_cpu_sparse_fp64` @ RAL | 56,746, single-jit block mean † | — | 55,292 [1] | 8 | 19.5 | 0.524 (29, cores) | match | `lifecycle/e08b7a6ff7b9daea8790` |
| ao | `numba_cpu_sparse_fp64` @ RAL | 8,671, numba warm iid median | — | — | 1 | 23.0 | 4.61 (40, memory) | match | `lifecycle/1f22a4a5fcd73276ec53` |

### Evidence: imaging/delaunay_nn

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| hst | `jax_cpu_sparse_fp64` @ A100 node | 6,250, single-jit block mean † | — | 6,235 [3] | 8 | 10.7 | 2.41 (15, cores) | match | `lifecycle/cbc5540f3214caf61aba` |
| hst | `jax_gpu_dense_fp64` @ A100 node | 89.59, single-jit median | 89.50–89.82 | 42.74 [16] | 8 | 10.7 | 93.6 (4, gpus) | match | `lifecycle/c661098ad46c65fa59b2` |
| hst | `jax_gpu_sparse_fp64` @ A100 node | 1,201, single-jit median | 1,200–1,201 | 1,149 [16] | 8 | 10.7 | 3.48 (4, gpus) | match | `lifecycle/70bcae3ab1c4777651f0` |
| hst | `jax_cpu_sparse_fp64` @ RAL | 6,831, single-jit block mean † | — | 6,427 [3] | 8 | 10.8 | 4.51 (29, cores) | match | `lifecycle/1ae46b0872f10459a7c4` |
| hst | `numba_cpu_sparse_fp64` @ RAL | 1,295, numba warm iid median | — | — | 1 | 0.831 | 182 (236, cores) | match | `lifecycle/05dde64a0eb7fdd0c4a1` |

### Evidence: imaging/mge

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| euclid | `jax_gpu_dense_fp64` @ A100 node | 5.916, single-jit median | 5.729–6.194 | 0.1986 [64] | 8 | 1.91 | 20,100 (4, gpus) | match | `lifecycle/770dce7d7db7a1fc3b53` |
| euclid | `jax_cpu_dense_fp64` @ RAL | 7.896, single-jit median | 7.535–8.377 | 6.797 [3] | 8 | — | not projected (no peak RSS) | match | `lifecycle/190ebc582d9aba9aaa9c` |
| hst | `jax_gpu_dense_fp64` @ A100 node | 6.285, single-jit median | 6.250–6.337 | 0.4116 [64] | 8 | 10.7 | 9,720 (4, gpus) | match | `lifecycle/8a475e9abd97a8c4a1c0` |
| hst | `jax_cpu_dense_fp64` @ RAL | 21.22, single-jit median | 19.55–22.43 | 14.39 [3] | 8 | — | not projected (no peak RSS) | match | `lifecycle/54979849c807d452c510` |
| jwst | `jax_gpu_dense_fp64` @ A100 node | 7.000, single-jit median | 6.933–7.354 | 0.9966 [64] | 8 | 7.38 | 4,010 (4, gpus) | match | `lifecycle/0756e600e86d7ae6a462` |
| jwst | `jax_cpu_dense_fp64` @ RAL | 50.25, single-jit median | 45.86–59.97 | 41.55 [3] | 8 | 1.29 | 698 (29, cores) | match | `lifecycle/4baa9bc04c8d24a713b6` |
| ao | `jax_gpu_dense_fp64` @ A100 node | 15.73, single-jit median | 15.68–15.78 | 18.98 [3] | 8 | 39.8 | 211 (4, gpus) | match | `lifecycle/4b514c4262172f610fee` |
| ao | `jax_cpu_dense_fp64` @ RAL | 388.9, single-jit median | 347.7–444.2 | 329.7 [3] | 8 | 3.49 | 88.0 (29, cores) | match | `lifecycle/3216ffc143645fb46c72` |

### Evidence: imaging/rectangular

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| euclid | `jax_cpu_sparse_fp64` @ A100 node | 827.4, single-jit median | 810.4–859.4 | 633.8 [3] | 8 | 1.91 | 23.7 (15, cores) | match | `lifecycle/9e4861d45b9802a91868` |
| euclid | `jax_gpu_dense_fp64` @ A100 node | 29.83, single-jit median | 29.19–30.50 | 7.926 [64] | 8 | 1.91 | 505 (4, gpus) | match | `lifecycle/456f7d65babc5524183a` |
| euclid | `jax_gpu_sparse_fp64` @ A100 node | 34.68, single-jit median | 34.62–34.86 | 13.19 [64] | 8 | 1.91 | 303 (4, gpus) | match | `lifecycle/bc5ed323618c58fc7682` |
| euclid | `jax_cpu_sparse_fp64` @ RAL | 858.5, single-jit median | 772.5–942.2 | 683.0 [3] | 8 | 1.91 | 42.5 (29, cores) | match | `lifecycle/4c53e409a27040f5d6a4` |
| euclid | `numba_cpu_sparse_fp64` @ RAL | 282.5, numba warm iid median | — | — | 1 | — | not projected (no peak RSS) | match | `lifecycle/6060fdcfa2e5a4a0c168` |
| hst | `jax_cpu_sparse_fp64` @ A100 node | 1,968, single-jit median | 1,946–2,009 | 1,709 [3] | 8 | 10.7 | 8.78 (15, cores) | match | `lifecycle/22c24ae6e2c83dc51d89` |
| hst | `jax_gpu_dense_fp64` @ A100 node | 40.66, single-jit median | 40.59–40.77 | 25.50 [16] | 8 | 10.7 | 157 (4, gpus) | match | `lifecycle/42f6a707360ce63b8150` |
| hst | `jax_gpu_sparse_fp64` @ A100 node | 61.55, single-jit median | 61.50–61.67 | 41.19 [16] | 8 | 10.7 | 97.1 (4, gpus) | match | `lifecycle/cc3f3365b6ac65388a93` |
| hst | `jax_cpu_sparse_fp64` @ RAL | 2,155, single-jit block mean † | — | 2,029 [3] | 8 | 3.15 | 14.3 (29, cores) | match | `lifecycle/2b5e34f509175fd4d030` |
| hst | `numba_cpu_sparse_fp64` @ RAL | 696.7, numba warm iid median | — | — | 1 | 1.02 | 339 (236, cores) | match | `lifecycle/b62534053c00fb102bf4` |
| jwst | `jax_cpu_sparse_fp64` @ A100 node | 4,141, single-jit block mean † | — | 3,940 [3] | 8 | 7.38 | 3.81 (15, cores) | match | `lifecycle/cfba00e49ad2fb8681cb` |
| jwst | `jax_gpu_dense_fp64` @ A100 node | 66.30, single-jit median | 65.77–66.77 | 62.84 [8] | 8 | 7.38 | 63.6 (4, gpus) | match | `lifecycle/ec69a200557ea8212e5e` |
| jwst | `jax_gpu_sparse_fp64` @ A100 node | 116.8, single-jit median | 116.7–117.6 | 107.5 [8] | 8 | 7.38 | 37.2 (4, gpus) | match | `lifecycle/bdffd9d6d157b3b66435` |
| jwst | `jax_cpu_sparse_fp64` @ RAL | 4,453, single-jit block mean † | — | 4,210 [3] | 8 | 5.38 | 6.89 (29, cores) | match | `lifecycle/9bb2e30e94491253641b` |
| jwst | `numba_cpu_sparse_fp64` @ RAL | 1,688, numba warm iid median | — | — | 1 | 1.98 | 140 (236, cores) | match | `lifecycle/304ac75d242dcbc2c22f` |
| ao | `jax_cpu_sparse_fp64` @ A100 node | 50,291, single-jit block mean † | — | 50,843 [1] | 8 | 39.8 | 0.295 (15, cores) | match | `lifecycle/3617cdce4ec7d5357c4f` |
| ao | `jax_gpu_dense_fp64` @ A100 node | 309.6, single-jit median | 308.6–310.9 | 310.8 [1] | 8 | 39.8 | 12.9 (4, gpus) | match | `lifecycle/d570569f32c953038fde` |
| ao | `jax_gpu_sparse_fp64` @ A100 node | 968.4, single-jit median | 967.2–969.4 | 1,053 [1] | 8 | 39.8 | 3.80 (4, gpus) | match | `lifecycle/46db4990a22e25aee123` |
| ao | `jax_cpu_sparse_fp64` @ RAL | 50,877, single-jit block mean † | — | 48,794 [1] | 8 | 22.3 | 0.594 (29, cores) | match | `lifecycle/d7020017fca2249bf32b` |
| ao | `numba_cpu_sparse_fp64` @ RAL | 9,982, numba warm iid median | — | — | 1 | 28.0 | 3.21 (32, memory) | match | `lifecycle/403420f8debaaa38956c` |

### Evidence: interferometer/delaunay

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| sma | `jax_gpu_dense_fp64_nufft` @ A100 node | 55.86, single-jit median | 55.76–56.23 | 55.77 [1] | 8 | 5.00 | 71.7 (4, gpus) | match | `lifecycle/ff5c53947f845ee5f2d8` |
| sma | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 27.49, single-jit median | 27.39–27.69 | 12.09 [64] | 8 | 1.68 | 331 (4, gpus) | match | `lifecycle/742eaf1292ed737e591e` |
| sma | `jax_cpu_dense_fp64_nufft` @ RAL | 6,411, single-jit block mean † | — | 5,702 [3] | 8 | 33.0 | 4.74 (27, memory) | match | `lifecycle/284efdc05b70e06e060a` |
| sma | `jax_cpu_sparse_fp64_wtilde` @ RAL | 1,169, single-jit median | 1,001–1,298 | 859.2 [3] | 8 | 1.32 | 33.8 (29, cores) | match | `lifecycle/00838694b2c3c955a644` |
| sma | `numba_cpu_sparse_fp64_wtilde` @ RAL | 335.1, numba warm iid median (route arms: direct_conv 338.4, NumPy FFT 1,166) | — | — | 1 | 0.853 | 704 (236, cores) | match | `lifecycle/b2d01ef74bf71e49d774` |
| alma | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 40.26, single-jit median | 40.02–41.05 | 22.65 [64] | 8 | 2.53 | 177 (4, gpus) | match | `lifecycle/8dada4df3a4ed30d1721` |
| alma | `jax_cpu_sparse_fp64_wtilde` @ RAL | 2,845, single-jit block mean † | — | 2,712 [3] | 8 | 2.39 | 10.7 (29, cores) | match | `lifecycle/60747d6f7a1867da50c9` |
| alma | `numba_cpu_sparse_fp64_wtilde` @ RAL | 823.6, numba warm iid median (route arms: direct_conv 817.9, NumPy FFT 3,052) | — | — | 1 | 1.55 | 286 (236, cores) | match | `lifecycle/5e9d64046821795b4651` |
| alma_high | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 82.48, single-jit median | 82.36–82.80 | 68.81 [16] | 8 | 4.16 | 58.1 (4, gpus) | match | `lifecycle/ba12584bdfe8c2e16f30` |
| alma_high | `jax_cpu_sparse_fp64_wtilde` @ RAL | 9,692, single-jit block mean † | — | 8,500 [3] | 8 | 9.31 | 3.41 (29, cores) | match | `lifecycle/d54c6814c51c381564cf` |
| alma_high | `numba_cpu_sparse_fp64_wtilde` @ RAL | 11,301, numba warm iid median (route arms: direct_conv 8,777, NumPy FFT 11,267) | — | — | 1 | 2.36 | 20.9 (236, cores) | match | `lifecycle/bfe464d85eab437c56be` |
| jvla | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 440.2, single-jit median | 440.0–440.7 | 459.4 [3] | 8 | 14.3 | 8.71 (4, gpus) | match | `lifecycle/3c33efbabefe647c901b` |
| jvla | `jax_cpu_sparse_fp64_wtilde` @ RAL | 34,832, single-jit block mean † | — | 34,209 [3] | 8 | 23.0 | 0.848 (29, cores) | match | `lifecycle/757d2c2d7167cdef0457` |
| jvla | `numba_cpu_sparse_fp64_wtilde` @ RAL | 73,492, numba warm iid median (route arms: direct_conv 315,196, NumPy FFT 77,134) | — | — | 1 | 11.7 | 1.06 (78, memory) | match | `lifecycle/e63a97d451e1633c91aa` |

### Evidence: interferometer/mge

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| sma | `jax_gpu_dense_fp64_nufft` @ A100 node | 3.718, single-jit median | 3.670–3.797 | 0.5729 [64] | 8 | 1.57 | 6,980 (4, gpus) | match | `lifecycle/4c9e3b4239cc98b8a7ff` |
| sma | `jax_cpu_dense_fp64_nufft` @ RAL | 90.63, single-jit median | 71.48–125.1 | 112.5 [3] | 8 | 1.30 | 258 (29, cores) | match | `lifecycle/02e5496a9c9da3407d87` |

### Evidence: interferometer/rectangular

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| sma | `jax_gpu_dense_fp64_nufft` @ A100 node | 50.06, single-jit median | 50.00–50.33 | 50.13 [1] | 8 | 4.78 | 79.8 (4, gpus) | match | `lifecycle/e44acbf15a2387706fa1` |
| sma | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 22.95, single-jit median | 22.87–23.04 | 7.191 [64] | 8 | 1.65 | 556 (4, gpus) | match | `lifecycle/a39d6114339d546f6bd6` |
| sma | `jax_cpu_dense_fp64_nufft` @ RAL | 3,781, single-jit block mean † | — | 3,488 [3] | 8 | 31.6 | 8.31 (29, cores) | match | `lifecycle/0cec032ed12d6d948802` |
| sma | `jax_cpu_sparse_fp64_wtilde` @ RAL | 856.0, single-jit median | 756.5–970.7 | 757.7 [3] | 8 | 1.33 | 38.3 (29, cores) | match | `lifecycle/29d350ddd936276d4121` |
| sma | `numba_cpu_sparse_fp64_wtilde` @ RAL | 287.3, numba warm iid median (route arms: direct_conv 301.3, NumPy FFT 1,040) | — | — | 1 | 0.826 | 822 (236, cores) | match | `lifecycle/0e27b1175ce084dff51e` |
| alma | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 36.01, single-jit median | 35.95–36.23 | 51.22 [3] | 8 | 1.42 | 78.1 (4, gpus) | match | `lifecycle/fe32c3ee13ad9afc455c` |
| alma | `jax_cpu_sparse_fp64_wtilde` @ RAL | 2,907, single-jit block mean † | — | 2,796 [3] | 8 | 2.35 | 10.4 (29, cores) | match | `lifecycle/41fd14e1f19bad947f24` |
| alma | `numba_cpu_sparse_fp64_wtilde` @ RAL | 897.9, numba warm iid median (route arms: direct_conv 887.8, NumPy FFT 1,960) | — | — | 1 | 0.927 | 263 (236, cores) | match | `lifecycle/4663f221c8c3ce49b76f` |
| alma_high | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 73.70, single-jit median | 73.66–73.96 | 86.62 [3] | 8 | 4.14 | 46.2 (4, gpus) | match | `lifecycle/2ab9504c46bb8170ba54` |
| alma_high | `jax_cpu_sparse_fp64_wtilde` @ RAL | 8,731, single-jit block mean † | — | 9,809 [3] | 8 | 9.45 | 2.96 (29, cores) | match | `lifecycle/fe0f252f68dcc26d7d13` |
| alma_high | `numba_cpu_sparse_fp64_wtilde` @ RAL | 17,723, numba warm iid median (route arms: direct_conv 16,789, NumPy FFT 16,328) | — | — | 1 | 2.32 | 13.3 (236, cores) | match | `lifecycle/d79f1b94f4b03452d745` |
| jvla | `jax_gpu_sparse_fp64_wtilde` @ A100 node | 437.8, single-jit median | 437.7–438.1 | 450.6 [3] | 8 | 14.2 | 8.88 (4, gpus) | match | `lifecycle/220d076d8421130e83cf` |
| jvla | `jax_cpu_sparse_fp64_wtilde` @ RAL | 58,366, single-jit block mean † | — | 58,633 [3] | 8 | 22.4 | 0.495 (29, cores) | match | `lifecycle/99c70939e335d08c4cff` |
| jvla | `numba_cpu_sparse_fp64_wtilde` @ RAL | 71,933, numba warm iid median (route arms: direct_conv 437,013, NumPy FFT 70,490) | — | — | 1 | 10.9 | 1.17 (84, memory) | match | `lifecycle/15aded078686cdf03ff5` |

### Evidence: point_source_image/image_plane

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| simple | `jax_gpu_na_fp64` @ A100 node | 0.8472, single-jit median | 0.8334–0.9058 | 0.4055 [3] | 8 | 1.18 | 9,860 (4, gpus) | match | `lifecycle/6282556b81be530f7bce` |
| simple | `jax_cpu_na_fp64` @ RAL | 1.556, single-jit median | 1.466–1.910 | 1.097 [3] | 8 | 1.06 | 26,400 (29, cores) | match | `lifecycle/6cbf08c848ae6cdb820f` |

### Evidence: point_source_source/source_plane

| instrument | setup @ host | headline per call (ms), basis | p10–p90 (ms) | vmap per call (ms) [batch] | cores/call | peak RSS (GB) | projected calls/s per node (workers, bound) | parity | runtime record |
|---|---|---|---|---|---|---|---|---|---|
| simple | `jax_cpu_na_fp64` @ A100 node | 0.2653, single-jit median | 0.2377–0.3155 | 0.1107 [3] | 8 | 0.577 | 136,000 (15, cores) | match | `lifecycle/c2bfeea342f97959dc7c` |
| simple | `jax_gpu_na_fp64` @ A100 node | 0.2617, single-jit median | 0.2531–0.2827 | 0.1087 [3] | 8 | 0.689 | 36,800 (4, gpus) | match | `lifecycle/fcb319f0f24b8cc9fd37` |
| simple | `jax_cpu_na_fp64` @ RAL | 0.1557, single-jit median | 0.1356–0.2076 | 0.06085 [3] | 8 | 0.573 | 476,000 (29, cores) | match | `lifecycle/61082dc032d7280b3bd1` |

## Proposals

Each block: §3.3 provisional (report §3.3 text, and its machine reading in `catalogue/provisional_designations.json` `tables`) → evidence (the table rows above) → proposed optimal / secondary → reason → confirms or overturns → caveats. "Uncontested" means only one setup was planned and measured on that hardware class: the evidence confirms it runs, matches parity and what it costs, but compares it with nothing. "Does not separate" means two measured setups are inside each other's spread or within the noise named.

### imaging/mge (regime `standard`; instruments euclid, hst, jwst, ao)

| | `gpu_a100` | `cpu_many_core` |
|---|---|---|
| §3.3 provisional | optimal `jax_gpu_dense_fp64`; secondary — | optimal `jax_cpu_dense_fp64`; secondary — |
| Evidence | only setup measured on the node: vmap per call 0.1986 [64] / 0.4116 [64] / 0.9966 [64] / 18.98 [3] ms (euclid/hst/jwst/ao); single-jit 5.916 / 6.285 / 7.000 / 15.73 ms; parity match ×4 | only setup measured: vmap per call 6.797 / 14.39 / 41.55 / 329.7 ms [3]; single-jit 7.896 / 21.22 / 50.25 / 388.9 ms; euclid and hst rows have no peak RSS, so not projected; parity match ×4 |
| **Proposed** | optimal `jax_gpu_dense_fp64`; secondary [] | optimal `jax_cpu_dense_fp64`; secondary [] |
| Reason | the only planned GPU setup; runs every instrument, ao in 15.73 ms | the only planned CPU setup for a parametric source |
| Verdict | **confirms (uncontested)** | **confirms (uncontested)** |
| Caveats | C2; C4 (GPU rows on jax 0.10.2); the node-CPU arm was not measured (Q2), though on its own ral node `jax_cpu_dense_fp64` projects 698 calls/s (jwst) and 88.0 (ao) against the gpu node's 4,010 and 211, so a whole ral node is behind | C1 (2a load 8.6–37; not in the quiet rerun); C4 (no eigen flag; D12 measured +25 % on laptop group/mge); C7 |

### imaging/rectangular, imaging/delaunay, imaging/delaunay_nn (regime `standard`)

**`gpu_a100`** — §3.3: optimal `jax_gpu_dense_fp64` ("`jax_gpu_sparse_fp64` secondary until the light_fixed divergence is explained"); machine-reading secondary [`jax_cpu_sparse_fp64`, `jax_gpu_sparse_fp64`].

| Likelihood | dense vs sparse, vmap per call (ms) euclid / hst / jwst / ao | single-jit p10–p90 overlap? | Per node |
|---|---|---|---|
| rectangular | 7.926 vs 13.19 / 25.50 vs 41.19 / 62.84 vs 107.5 / 310.8 vs 1,053 | no, on any instrument | same order (one process per GPU each): 505 vs 303 … 12.9 vs 3.80 calls/s |
| delaunay | 14.80 vs 18.16 / 35.05 vs 47.93 / 72.29 vs 108.1 / 366.9 vs 935.3 | no; closest euclid 44.24–45.63 vs 46.67–47.30 ms | 270 vs 220 … 10.9 vs 4.28 |
| delaunay_nn (hst only) | 42.74 vs 1,149 | no | 93.6 vs 3.48 |

`jax_cpu_sparse_fp64` on the gpu node's CPU is 1–2 orders slower than either GPU setup on every cell (e.g. hst Delaunay vmap 2,110 ms [3], 7.11 calls/s per node). Parity match on all 27 cells.

- **Proposed:** optimal `jax_gpu_dense_fp64`; secondary [`jax_gpu_sparse_fp64`, `jax_cpu_sparse_fp64`], for each of the three likelihoods.
- **Reason:** dense is fastest per call and per node on every instrument, separated beyond the spread.
- **Verdict:** **confirms** §3.3 (optimal and secondary).
- **Caveats:** C2; C4 (GPU rows on jax 0.10.2; a jaxlib change could move GPU numbers, untested). Q2: numba was never measured on the gpu node's 124 cores. On its own ral node numba projects 248 calls/s on hst Delaunay against 114 for the gpu node's GPUs (2a page), so on a per-node axis that counts the GPU node's cores the CPU arm could matter, and there is no row to say. The 2026-10-18 `jax_gpu_sparse_fp64` light_fixed divergence blocks only an Optimal designation of that setup (ledger, phase 4 card). delaunay_nn `jax_gpu_sparse_fp64` at 1,149 ms against 42.74 ms dense is flagged on the 2a page ("worth a look in phase 3"); it does not change the order. ao A100 peak RSS (39.8 GB) is the multi-leg job's peak, an upper bound.

**`cpu_many_core`** — §3.3: optimal `numba_cpu_sparse_fp64` "+ cores"; secondary `jax_cpu_sparse_fp64` (numba dense dropped 2026-10-18); rule branches on "cores ≥ threshold (phase 4 efficiency curve); source pixels".

| Likelihood | numba vs JAX CPU sparse, per node (calls/s) euclid / hst / jwst / ao | per call (ms): numba warm iid median vs JAX vmap [3] or [1] |
|---|---|---|
| rectangular | numba not projected (no peak RSS) vs 42.5 / 339 vs 14.3 / 140 vs 6.89 / 3.21 (32 workers, memory) vs 0.594 | 282.5 vs 683.0 / 696.7 vs 2,029 / 1,688 vs 4,210 / 9,982 vs 48,794 |
| delaunay | 288 vs 35.1 / 248 vs 15.3 / 135 vs 6.65 / 4.61 (40, memory) vs 0.524 | **820.0 vs 826.6** / 951.7 vs 1,895 / 1,745 vs 4,361 / 8,671 vs 55,292 |
| delaunay_nn (hst) | 182 vs 4.51 | 1,295 vs 6,427 |

- **Proposed:** optimal `numba_cpu_sparse_fp64`; secondary [`jax_cpu_sparse_fp64`], each likelihood.
- **Reason:** numba is ahead per node on every projected cell (5× to 40×) at one core per call. Per call it is ahead everywhere except euclid Delaunay, where the two tie (0.8 %).
- **Verdict:** **confirms** §3.3. The "+ cores" threshold cannot be written yet (phase 4). The draft rule says workers are capped by node memory over peak RSS, which binds at ao (32 and 40 workers).
- **Caveats:** C1 (2a RAL load 8.6–37; not in the quiet rerun); C4 (JAX CPU side only); C7; C9. euclid rectangular numba has no peak RSS, so its per-node figure is missing (per call it is 2.4× ahead at 1/8 the cores). The §3.3 laptop optimal for pixelized imaging (`jax_cpu_dense_fp64`) was never measured on any host.

### interferometer/mge (sma only; 190 visibilities → regime `n_vis_lt_1e5`)

| | `gpu_a100` | `cpu_many_core` |
|---|---|---|
| §3.3 provisional | `jax_gpu_dense_fp64_<dft\|nufft>` by the `n_vis × n_pix` crossover ≈ 1e7; secondary — | `jax_cpu_dense_fp64_<dft\|nufft>`; secondary — |
| Evidence | `jax_gpu_dense_fp64_nufft` single-jit 3.718 ms (3.670–3.797), vmap 0.5729 [64]; parity match | `jax_cpu_dense_fp64_nufft` single-jit 90.63 ms (71.48–125.1), vmap 112.5 [3]; 258 calls/s per node; parity match |
| **Proposed** | optimal `jax_gpu_dense_fp64_nufft`; secondary [] — regime `n_vis_lt_1e5` only | optimal `jax_cpu_dense_fp64_nufft`; secondary [] — `n_vis_lt_1e5` only |
| Reason | the only measured setup | the only measured setup |
| Verdict | **confirms the NUFFT half (uncontested); the DFT branch is untested** (2b R2: no DFT cells), so the evidence does not separate DFT from NUFFT; no MGE row above sma (R9), so no proposal for the other regimes | same |
| Caveats | sma here has 190 visibilities at σ = 1000 (2b caveats), a small regime anchor; C2; C4 | C1 (2b load 45–72; rerun 413268); C4; C7 |

### interferometer/rectangular, interferometer/delaunay

Regimes as `provisional_designations.json` names them, read from each row's `configuration.visibilities`: sma 190 → `n_vis_lt_1e5`; alma 1,000,000 and alma_high 5,000,000 → `n_vis_1e5_1e7`; jvla 25,000,000 → `n_vis_ge_1e7`. Note: every catalogue record carries `regime: standard`. Designating by n_vis regime needs the producer to emit these regimes (Q5).

**`gpu_a100`** — §3.3: optimal `jax_gpu_sparse_fp64_wtilde`, `streaming` at `n_vis ≥ 1e7`; secondary "dense routes" (machine reading: `jax_gpu_dense_fp64_{dft,nufft}`).

| Regime | Evidence (rectangular; delaunay) | Proposed optimal / secondary | Verdict |
|---|---|---|---|
| `n_vis_lt_1e5` (sma) | W~ vmap 7.191 [64] vs dense NUFFT 50.13 [1] ms; single-jit 22.95 (22.87–23.04) vs 50.06 (50.00–50.33); per node 556 vs 79.8. Delaunay 12.09 [64] vs 55.77 [1]; 27.49 (27.39–27.69) vs 55.86 (55.76–56.23); 331 vs 71.7 | `jax_gpu_sparse_fp64_wtilde` / [`jax_gpu_dense_fp64_nufft`] | **confirms** (DFT secondary untested, R2) |
| `n_vis_1e5_1e7` (alma, alma_high) | W~ only: rectangular single-jit 36.01 / 73.70 ms; delaunay 40.26 / 82.48 ms. The dense route cannot form its mapping matrix above sma (R1(a): 20.5 GB at alma, 102 GB at alma_high) | `jax_gpu_sparse_fp64_wtilde` / [] | **confirms optimal (uncontested); overturns the provisional secondary**: no dense route runs in this regime |
| `n_vis_ge_1e7` (jvla) | W~ only: rectangular 437.8 ms (437.7–438.1), delaunay 440.2 ms (440.0–440.7), peak 14.2 / 14.3 GB on one A100 | `jax_gpu_sparse_fp64_wtilde` / [] | **departs from §3.3 by absence, not by measurement**: §3.3 names `streaming` here and streaming was not measured, so W~ vs streaming does not separate (Q10) |

Caveats (all regimes): C2; C4.

**`cpu_many_core`** — §3.3: "per the interferometer decision matrix: numba direct_conv vs FFT cost model (symmetric gate 0.7); `streaming` at large n_vis"; machine reading optimal `numba_cpu_sparse_fp64_wtilde`, secondary [`jax_cpu_dense_fp64_{dft,nufft}`, `jax_cpu_sparse_fp64_wtilde`].

| Regime | Per node, numba vs JAX CPU W~ (calls/s) rectangular; delaunay | Per call (ms), numba pick vs JAX CPU W~ vmap [3] | Proposed optimal / secondary | Verdict |
|---|---|---|---|---|
| `n_vis_lt_1e5` (sma) | 822 vs 38.3 (dense NUFFT 8.31); 704 vs 33.8 (dense 4.74) | 287.3 vs 757.7; 335.1 vs 859.2 (cost model picked direct_conv; forced arms 301.3 / 338.4) | `numba_cpu_sparse_fp64_wtilde` / [`jax_cpu_sparse_fp64_wtilde`, `jax_cpu_dense_fp64_nufft`] | **confirms** (DFT untested) |
| `n_vis_1e5_1e7` (alma, alma_high) | alma 263 vs 10.4, alma_high 13.3 vs 2.96; alma 286 vs 10.7, alma_high 20.9 vs 3.41 | alma 897.9 vs 2,796 and 823.6 vs 2,712 (numba ahead); **alma_high 17,723 vs 9,809 and 11,301 vs 8,500 (JAX CPU ahead per call)** | `numba_cpu_sparse_fp64_wtilde` / [`jax_cpu_sparse_fp64_wtilde`] | **confirms on the per-node axis**; on a per-call axis the regime would split between 1e6 and 5e6 visibilities (C6) |
| `n_vis_ge_1e7` (jvla) | rectangular 1.17 (84 workers, memory) vs 0.495 — separated (2.4×); **delaunay 1.06 (78, memory) vs 0.848 — 25 %** | 71,933 vs 58,633; 73,492 vs 34,209 (JAX CPU ahead per call) | rectangular: `numba_cpu_sparse_fp64_wtilde` / [`jax_cpu_sparse_fp64_wtilde`]. **delaunay: does not separate** (hold; §3.3's numba stands as provisional) | rectangular **confirms** per node; delaunay: no call. The 25 % margin rests on one numba warm draw at jvla and two loaded-node rows (C1), with η unmeasured and JAX CPU fixed at 8 threads (C7) |

- **The cost-model miss (2b page "The numba route").** At delaunay alma_high the cost model picked the NumPy FFT route (11,301 ms) but the forced `direct_conv` arm ran in 8,777 ms (22 % faster), on 6 warm draws on a loaded node. On the same node, two arms of one route differ by up to 9 % (rectangular alma_high: FFT pick 17,723 ms against forced FFT 16,328 ms). The miss is larger than that, but it is still thin evidence. It does not change the setup_id (both routes are inside `numba_cpu_sparse_fp64_wtilde`), and the per-node rank holds on either route. On the per-call axis, `direct_conv` would bring numba level with JAX CPU W~ (8,777 against 8,500 ms), which then does not separate. The fix belongs to the route-gate decision (PyAutoPulse `interferometer-route-gate-cost-model`, `direct-conv-symmetric-gate`), not to the designation. The draft rule says "route chosen by the packaged cost model" so a gate change does not reopen the designation.
- **Caveats:** C1 (every 2b RAL CPU row; quiet reruns 413268–413271 queued); C4 (JAX CPU side); C7; C9. Streaming on CPU was not measured.

### point_source_image/image_plane (instrument `simple`; regime `standard`)

| | `gpu_a100` | `cpu_many_core` |
|---|---|---|
| §3.3 provisional | optimal `jax_gpu_na_fp64` (§3.3 writes `jax_gpu_dense_fp64`; R1 machine reading `_na_`); secondary — | optimal `jax_cpu_na_fp64`; secondary — |
| Evidence (Solved likelihood, human ruling 2026-10-29) | single-jit 0.8472 ms (0.8334–0.9058), vmap 0.4055 [3]; 9,860 calls/s per node; parity match | single-jit 1.556 ms (1.466–1.910), vmap 1.097 [3]; 26,400 calls/s per ral node; parity match |
| **Proposed** | optimal `jax_gpu_na_fp64`; secondary [] | optimal `jax_cpu_na_fp64`; secondary [] |
| Reason | the only setup planned on the gpu node; faster per call than RAL CPU (0.8472 against 1.556 ms) | the only setup planned |
| Verdict | **confirms (uncontested)** on the per-call axis. On the per-node axis it is open: `jax_cpu_na_fp64@hpc_a100` was not planned for the image plane, and on its own ral node `jax_cpu_na_fp64` projects 26,400 calls/s against the gpu node's 9,860, so the node-CPU arm could win on a gpu node (Q2). Not separable without that row | **confirms (uncontested)** |
| Caveats | C2; C4 | C1 (load 33.4 at import; rerun 413267); C4; C7. The plain likelihood (`experiments/plain_runtime/`) is within 4 % of the solved one on every setup (2c page) |

### point_source_source/source_plane (instrument `simple`; regime `standard`)

| | `gpu_a100` | `cpu_many_core` |
|---|---|---|
| §3.3 provisional | optimal `jax_cpu_na_fp64` ("cheap; GPU warm-up dominates"); secondary `jax_gpu_na_fp64` | optimal `jax_cpu_na_fp64`; secondary `jax_gpu_na_fp64` (host-agnostic Secondary column; a GPU setup on a GPU-less host, D2 / #481) |
| Evidence | node CPU `jax_cpu_na_fp64` single-jit 0.2653 ms (0.2377–0.3155), vmap 0.1107 [3], **136,000 calls/s per node (15 workers × 8 cores)**; GPU `jax_gpu_na_fp64` 0.2617 ms (0.2531–0.2827), vmap 0.1087 [3], **36,800 (4 GPUs)**; breakdown fused solved 0.261 vs 0.250 ms (2c page); parity match ×2 | `jax_cpu_na_fp64` single-jit 0.1557 ms (0.1356–0.2076), vmap 0.06085 [3]; 476,000 calls/s per ral node; parity match |
| **Proposed** | optimal `jax_cpu_na_fp64`; secondary [`jax_gpu_na_fp64`] | optimal `jax_cpu_na_fp64`; secondary [] |
| Reason | per call the two **do not separate** (1.4 % apart, inside each other's p10–p90; GPU ahead by ≤ 4 % in both scripts); per node the CPU cores project 3.7× the GPUs | the only setup runnable on the host |
| Verdict | **confirms §3.3 on the per-node axis only**; on the per-call axis the evidence does not separate them (the 2c page verdict) | **confirms the optimal; overturns the secondary** (no GPU on the host; #481 already stopped planning it) |
| Caveats | C2; C4; C9 (15 JAX workers on a 124-core node at η = 1, `n_batch` not modelled); the A100 GPU per call rose 12 % against 2026.10.17.1 (0.233 → 0.262 ms), not investigated (2c page). The proposal depends on Q1 (axis) and Q2 (GPU node's CPU cores counted) | C1 (load 33.4; rerun 413267); C4; C7 |

## Summary

| Likelihood | Regime | `gpu_a100` proposed optimal / secondary | vs §3.3 | `cpu_many_core` proposed optimal / secondary | vs §3.3 |
|---|---|---|---|---|---|
| imaging/mge | standard | `jax_gpu_dense_fp64` / — | confirms (uncontested) | `jax_cpu_dense_fp64` / — | confirms (uncontested) |
| imaging/rectangular | standard | `jax_gpu_dense_fp64` / `jax_gpu_sparse_fp64`, `jax_cpu_sparse_fp64` | confirms | `numba_cpu_sparse_fp64` / `jax_cpu_sparse_fp64` | confirms |
| imaging/delaunay | standard | same as rectangular | confirms | same as rectangular | confirms (per-call tie at euclid) |
| imaging/delaunay_nn | standard (hst) | same as rectangular | confirms | same as rectangular | confirms |
| interferometer/mge | n_vis_lt_1e5 (sma) | `jax_gpu_dense_fp64_nufft` / — | confirms NUFFT; DFT untested | `jax_cpu_dense_fp64_nufft` / — | confirms NUFFT; DFT untested |
| interferometer/{rectangular, delaunay} | n_vis_lt_1e5 (sma) | `jax_gpu_sparse_fp64_wtilde` / `jax_gpu_dense_fp64_nufft` | confirms | `numba_cpu_sparse_fp64_wtilde` / `jax_cpu_sparse_fp64_wtilde`, `jax_cpu_dense_fp64_nufft` | confirms |
| interferometer/{rectangular, delaunay} | n_vis_1e5_1e7 (alma, alma_high) | `jax_gpu_sparse_fp64_wtilde` / — | confirms optimal; overturns secondary (dense cannot run) | `numba_cpu_sparse_fp64_wtilde` / `jax_cpu_sparse_fp64_wtilde` | confirms per node (per call splits) |
| interferometer/rectangular | n_vis_ge_1e7 (jvla) | `jax_gpu_sparse_fp64_wtilde` / — | streaming untested (Q10) | `numba_cpu_sparse_fp64_wtilde` / `jax_cpu_sparse_fp64_wtilde` | confirms per node |
| interferometer/delaunay | n_vis_ge_1e7 (jvla) | `jax_gpu_sparse_fp64_wtilde` / — | streaming untested (Q10) | **does not separate** (numba 1.06 vs JAX 0.848 calls/s) | hold |
| point_source_image/image_plane | standard | `jax_gpu_na_fp64` / — | confirms per call; per node open (Q2) | `jax_cpu_na_fp64` / — | confirms (uncontested) |
| point_source_source/source_plane | standard | `jax_cpu_na_fp64` / `jax_gpu_na_fp64` | confirms per node; per call does not separate | `jax_cpu_na_fp64` / — | confirms optimal; overturns secondary |

26 proposals (Appendix A): 25 with a proposed optimal, 1 hold. None overturns a §3.3 **optimal** on measured evidence. The departures are three dropped secondaries that cannot run (dense interferometer above sma ×2 likelihoods; GPU on a GPU-less host) and §3.3 branches that were never measured (interferometer DFT, GPU streaming at n_vis ≥ 1e7, every laptop cell).

## Human rulings (2026-10-30, chat, after the "campaigns complete" gate)

- **Q1 + Q3 — adopted as recommended:** rank by projected calls/s per node within each hardware class, per call as secondary evidence; record a designation only where setups separate beyond the recorded spread (or the arm-to-arm noise), otherwise keep the §3.3 provisional label with no decision.
- **Q2 — A100s only:** `gpu_a100` designations are GPU setups; the node's CPU stays a measured secondary where it exists. No node-CPU rows are added.
- **Q7 — re-measure the 2a–2c JAX rows:** day zero is one environment (jax/jaxlib 0.11.2, `--xla_cpu_multi_thread_eigen=false` on CPU legs). Every 2a/2b/2c JAX row (CPU and GPU) is re-measured; numba rows are carried. The 2b/2c quiet reruns (RAL 413319–413323, on 0.11.2 with the flag) already cover the 2b/2c RAL CPU legs; the remainder is every 2a JAX leg and the 2b/2c A100 JAX legs.
- **Q8 — freeze on 2026.10.25.1:** every row is on it; no carry.
- **Q9 — settled by the human's 2026-10-30 ruling on loaded RAL nodes** ("ignore loaded node stuff for now"): the 2a RAL CPU rows are accepted.
- Q4, Q5, Q6, Q10, Q11: the recommended handling in this file stands unless the human says otherwise ((a) `basis: projected` in the decision prose; designate interferometer by `standard` with an instrument-keyed rule unless the producer emits n_vis regimes; laptop undesignated; untested branches named in the rule; GPU-class secondaries GPU-only per Q2).

## Questions for the human

- **Q1 — Axis.** The report amendment (2026-10-25) pre-registered per-node projected throughput within each hardware class, with per call as secondary evidence. Confirm it for the records. It decides four proposals: interferometer pixelized alma_high and jvla on RAL (numba per node, JAX CPU per call), euclid Delaunay imaging on RAL (per-call tie), and the source-plane A100 node (per-call tie, CPU cores 3.7× per node).
- **Q2 — What a GPU node's budget includes.** Does `gpu_a100` mean "use the A100s" or "use the gpu node": 4 GPUs plus 124 cores? Source plane measured the node CPU (D2) and the proposal there rests on it. Image-plane point source, imaging pixelized (numba) and interferometer were never measured on the gpu node's CPU, and on their own ral nodes those CPU setups project ahead of the gpu node on several cells (point source 26,400 vs 9,860; hst Delaunay 248 vs 114). If the node counts, those arms need rows before the GPU designations are final. Rows are not projected across machines (human 2026-10-25).
- **Q3 — Close calls.** Proposed handling: record a designation only where the setups separate on the chosen axis beyond the recorded p10–p90 (or, with no spread recorded, beyond the arm-to-arm noise seen on the same node, about 9 % for 2b numba). Otherwise record "does not separate" and keep the §3.3 provisional label without a decision. Current cases: interferometer/delaunay jvla on RAL per node (25 %; hold), source plane on the A100 node per call (1.4 %), and euclid Delaunay imaging on RAL per call (0.8 %).
- **Q4 — `basis: projected`.** The amendment says pre-phase-4 designations carry `basis: projected`. Pulse's `decisions.yaml` refuses any field outside `id, title, date, url, kind` plus the eight designation fields (`pulse/decisions.py`). Options: (a) say it in the canonical `decisions/<id>.md` and the `rule` sentence; (b) a Pulse change adding `basis`. The appendix assumes (a).
- **Q5 — Interferometer regimes.** Every catalogue record says `regime: standard`. Designate interferometer by the n_vis regimes in `provisional_designations.json` (needs the producer to emit `regime` per record, and a decision on where alma_high at 5e6 sits), or by `standard` with an instrument-keyed rule?
- **Q6 — Laptop.** No laptop evidence can be current (R7), and a designation needs non-empty `evidence`. Leave `laptop` undesignated at day zero, or record §3.3's laptop column citing the CPU-node rows?
- **Q7 — The jax environment (C4).** The 2a/2b/2c JAX rows ran on jax/jaxlib 0.10.2, which tag 2026.10.25.1 excludes (`!=0.10.*`, Heart#274). 2d–2g will run on 0.11.2 with the D12 eigen flag. Freeze the 0.10.2 rows as day zero, or re-measure every JAX row (CPU and GPU) on 0.11.2 with the flag so day zero is one environment? Numba rows are unaffected.
- **Q8 — Which tag phase 3 freezes on.** See the next section.
- **Q9 — 2a RAL CPU rows.** They ran at load 8.6–37 and are not in the quiet rerun. Accept them, or rerun them quiet?
- **Q10 — Untested §3.3 branches.** Interferometer MGE DFT (R2: no DFT cells), GPU `streaming` at n_vis ≥ 1e7, CPU streaming. Record designations without them, with the branch named as untested in the rule, or measure first?
- **Q11 — Secondary lists.** Is `jax_cpu_sparse_fp64` (the gpu node's CPU) a useful secondary for imaging on `gpu_a100`, as §3.3's host-agnostic column implies, or should a GPU-class secondary be GPU-only?

## Release interaction (the tag phase 3 freezes on)

Every proposal rests on rows published at 2026.10.25.1 (imaging measured on 2026.10.23.1 and carried by `catalogue/release_revisions.json`, human ruling 2026-10-26, #466). Phase 3 must freeze on a released tag (ledger orchestration step 7). Two facts:

1. **A release after the pin already exists:** 2026.10.26.1 (all five libraries tagged 2026-10-25/26; PyAutoNerves 2026.10.25.1 = 2026.10.26.1 = `main` = ec8b5c1). The release the human is planning now would come after it.
2. **Likelihood-path commits since 2026.10.25.1** (`git log 2026.10.25.1..origin/main`, fetched 2026-10-29; "[26.1]" = already in 2026.10.26.1):

| Repo | Commit | What | Touches a 2a–2c cell's per-call path? |
|---|---|---|---|
| PyAutoArray | 71a3ef49 [26.1] | matrix-free interferometer route, `Settings(interferometer_route="matrix_free")`; `inversion/inversion/factory.py` gains an opt-in branch, `inversion/interferometer/matrix_free.py` new | No by default: the branch fires only when the setting is `"matrix_free"` (2b's matrix-free experiment, never current). It is an edit to the pixelized interferometer factory, so re-run the 2b parity smokes before carrying |
| PyAutoArray | 171eacca [26.1] | config leaf comments | No (comment-only; values unchanged in `general.yaml`) |
| PyAutoArray | cd26722b | introductory four-panel imaging plot | No (plotting) |
| PyAutoGalaxy | 499827fe [26.1] | `PowerLaw` JAX unit-vector transform | No: the standard cells use `Isothermal` + `ExternalShear` (`_production_config.py`; point-source scripts `Isothermal`). `PowerLaw` appears only in fixed-light and experiment scripts |
| PyAutoGalaxy | 36ec41b2 [26.1] | `MassSheet` JAX deflections | No (not in the standard cells) |
| PyAutoGalaxy | 9be12cae [26.1] | reject singular isothermal dipole multipoles (`power_law_multipole.py`) | No (not in the standard cells) |
| PyAutoGalaxy | 0fee6daf [26.1] | `SersicCoreSph` mass-to-light ratio | No |
| PyAutoGalaxy | eaf12527, ac1adc08, 6c0fac8f [26.1] | latent ("derived") parameter declarations (`convert.py`; `ExternalShear` +3 lines of declarations) | No per-call change expected (declarations for corner plots) |
| PyAutoGalaxy | acfc61ad | gNFW convergence integral tabulated instead of per-point `quad` (perf) | No for 2a–2c; a 2d–2g cell using gNFW would change (the profiling scripts reference `NFWSph`, `NFWMCRLudlowSph`, not gNFW) |
| PyAutoGalaxy | f539aca7 | `mass_integral` length-1 radius fix (Einstein radius, angular mass) | No (not called in a likelihood) |
| PyAutoGalaxy | 6879610f, abcb81b8, 22f849c9 | aperture mass, `MassBudget` (lenstwin), plots | No |
| PyAutoLens | f6800bb50, 9541c87bb | `al.twins` (lenstwin) | No (new package) |
| PyAutoLens | 8cff95d5f [26.1], a0666e7ef, 05f0a776d, 1d430dcd9 | config comments, cluster/intro plots, point-dataset tests | No |
| PyAutoFit | 00a153ceb [26.1] | config leaf comments | No |
| PyAutoNerves | — | no commits | — |

Dependencies: no `pyproject.toml` change to jax, jaxlib or numba floors since the pin. The only change is PyAutoGalaxy's `autofit>=2026.10.23.1` floor. Non-comment config diffs in `general.yaml` / `non_linear.yaml`: none.

**The agent's reading for the human:** a release cut from today's mains changes no per-call likelihood of a 2a–2c standard cell. The one likelihood-adjacent edit is the opt-in branch in the interferometer inversion factory. The options:

- (a) **Freeze on 2026.10.25.1.** Valid as a released tag, but the day-zero pin is then older than the library users install.
- (b) **Carry the 2a–2c rows to the new tag** under the existing `carry_forward` rule (the #466 precedent: re-stamp, don't rerun), after the 2b parity smokes pass on the new tag.
- (c) **Re-measure on the new tag.**

The tag diff alone does not justify (c). The environment does: C4/Q7 (the rows ran on jax 0.10.2, which the tag excludes) is independent of which tag is chosen. If the human wants one environment for 2a–2g, (c) for the JAX rows (with numba rows carried) is the consistent choice, and it could share RAL time with the 2d–2g batches. Whatever is chosen, 2d–2g should run on the tag phase 3 will freeze on, so they need no carry.

## What phase 3 still needs (checklist)

From 2d–2g and phase 2:

- [ ] 2d multi_galaxy + group, 2e cluster, 2f multi_dataset + datacube, 2g weak: decision reviews, batch-0 goes, RAL batches, PR B, campaign pages with verdicts (`likelihood_lifecycle_p2{d_galaxy_group,e_cluster,f_dataset_datacube,g_weak}_runs.md`). Coverage today: 272 planned, 176 current, 96 missing (`dashboard/coverage.md`, 2026-10-29T09:46:25Z), the 96 all theirs.
- [ ] Their evidence for the "as imaging" / "as interferometer" / "as point source" inheritance in §3.3 (multi_galaxy, group, multi_dataset → imaging; datacube → interferometer per channel; cluster → point source × n_sources; weak → `jax_cpu_dense_fp64` with a GPU secondary): their designations are drafted after their campaigns, like these.
- [x] Quiet-rerun ingest — DONE 2026-10-31, autolens_profiling#494, record `complete/2026/10/likelihood-lifecycle-p2bc-quiet-ingest.md` (was RAL 413267–413271 → 413319–413323): replaces 38 2b and 2 2c RAL CPU rows. Then re-check every `cpu_many_core` interferometer and point-source proposal above, especially the interferometer/delaunay jvla hold and the alma_high per-call flip, and re-resolve evidence ids (path-hashed).
- [ ] The human's "campaigns complete" confirmation (the phase 3 gate).

Human decisions before records (this file's questions): Q1 axis; Q2 GPU-node budget (and, if the node counts, node-CPU rows for image-plane point source, imaging pixelized numba and interferometer); Q3 close-call rule; Q4 where `basis: projected` lives; Q5 interferometer regimes; Q6 laptop; Q7 jax environment; Q8 tag; Q9 2a RAL load; Q10 untested branches; Q11 secondary lists.

Phase 3 deliverables themselves (ledger card; report §4):

- [ ] Pin the released tag; re-measure (or carry, by ruling) every Optimal/Secondary cell not on it; stamp `day_zero`; Pulse snapshot `day_zero`.
- [ ] The designation records: one canonical `decisions/<id>.md` per likelihood × regime × hardware class plus its `decisions.yaml` row (human-recorded; Appendix A is the draft). Then producers re-declare `class: optimal` + `decision_id` on the cited rows, and `pyauto-pulse check` resolves them.
- [ ] `catalogue/provisional_designations.json` replaced or retired in favour of the records (it must agree with them, and phase 5's library rule table is generated from and tested against them).
- [ ] `wiki/campaigns/<dataset_type>/<variant>/day_zero.md` per likelihood, with rules in dataset-property terms.
- [ ] Pulse `setup-baseline` campaign adopted and closed, its 1,044-slot manifest replaced (R10).
- [ ] Coverage shows no `not_measured` Optimal cell; the `runtime_estimates` export exists (for 5E).

## Appendix A — draft `decisions.yaml` entries (NOT published, NOT indexed)

Generated from `dashboard/catalogue.json` at autolens_profiling 32c0becd. Each entry was checked with `pulse.decisions._designation` (PyAutoPulse `pulse/decisions.py`, identical to `main` 4a4bdee). `evidence` lists, per instrument and setup measured on that host class, the runtime record id followed by its parity record id. `date` is a placeholder for the human's decision date, quoted as a string when recorded. The `# separation:` comment above each entry is this draft's label on the pre-registered per-node axis (see the Proposals for where the per-call axis differs), not a field. The `hold` entry must not be recorded as written. Ids follow the README template `<likelihood>-<regime>-<hardware-class>` in kebab case. Re-resolve every id at the freeze commit (path-hashed ids; quiet-rerun ingest).

```yaml
# separation: uncontested
- id: imaging-mge-standard-gpu-a100
  title: 'Designation: imaging/mge standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-mge-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/mge
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: []
  evidence: [lifecycle/770dce7d7db7a1fc3b53, lifecycle/2d7064bb66242f2ca6cc, lifecycle/8a475e9abd97a8c4a1c0, lifecycle/4e93e744f3e1295b3c8d, lifecycle/0756e600e86d7ae6a462, lifecycle/a58929ead49f62c064da, lifecycle/4b514c4262172f610fee, lifecycle/eb44c9d7e6987735cdd1]
  rule: Any imaging dataset fitted with a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: imaging-mge-standard-cpu-many-core
  title: 'Designation: imaging/mge standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-mge-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/mge
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64
  secondary: []
  evidence: [lifecycle/190ebc582d9aba9aaa9c, lifecycle/acf067a34aa2005d1b11, lifecycle/54979849c807d452c510, lifecycle/d2aece86956eba227ada, lifecycle/4baa9bc04c8d24a713b6, lifecycle/2cf94e6d7d8231a57c92, lifecycle/3216ffc143645fb46c72, lifecycle/a37560173314cc078894]
  rule: Any imaging dataset fitted with a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64.
  supersedes: null
# separation: separated
- id: imaging-rectangular-standard-gpu-a100
  title: 'Designation: imaging/rectangular standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-rectangular-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/rectangular
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64, jax_cpu_sparse_fp64]
  evidence: [lifecycle/9e4861d45b9802a91868, lifecycle/eb746ec4a8c1668c7a40, lifecycle/456f7d65babc5524183a, lifecycle/a429326f9f33ea12e6b8, lifecycle/bc5ed323618c58fc7682, lifecycle/688c98aeb69ac24ea6f3, lifecycle/22c24ae6e2c83dc51d89, lifecycle/0b43689b6e8f601ade78, lifecycle/42f6a707360ce63b8150, lifecycle/51cd6f8ab1edb2761cb8, lifecycle/cc3f3365b6ac65388a93, lifecycle/d1a3e06d7571bd6b5eba, lifecycle/cfba00e49ad2fb8681cb, lifecycle/72add1d2a2a70bb1304c, lifecycle/ec69a200557ea8212e5e, lifecycle/76d01fc60350dd469eed, lifecycle/bdffd9d6d157b3b66435, lifecycle/df1e242101ab32dea573, lifecycle/3617cdce4ec7d5357c4f, lifecycle/48ae4d8138f5bb99846a, lifecycle/d570569f32c953038fde, lifecycle/32ca51df82e1724685ab, lifecycle/46db4990a22e25aee123, lifecycle/67787bf45d6bb0b3aa42]
  rule: Any imaging dataset with a rectangular pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: imaging-rectangular-standard-cpu-many-core
  title: 'Designation: imaging/rectangular standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-rectangular-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/rectangular
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/4c53e409a27040f5d6a4, lifecycle/39a0a9b81376f2be8446, lifecycle/6060fdcfa2e5a4a0c168, lifecycle/ae663292d53c60a65c62, lifecycle/2b5e34f509175fd4d030, lifecycle/ee2df565d3603ba2bbd3, lifecycle/b62534053c00fb102bf4, lifecycle/8db1316c3491c8569223, lifecycle/9bb2e30e94491253641b, lifecycle/dd67472c35e8ed230b03, lifecycle/304ac75d242dcbc2c22f, lifecycle/0de8cf81e718d21ee2aa, lifecycle/d7020017fca2249bf32b, lifecycle/e44433f6b0bb6fbb1519, lifecycle/403420f8debaaa38956c, lifecycle/a721c437cf9355984ca5]
  rule: Any imaging dataset with a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS).
  supersedes: null
# separation: separated
- id: imaging-delaunay-standard-gpu-a100
  title: 'Designation: imaging/delaunay standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64, jax_cpu_sparse_fp64]
  evidence: [lifecycle/a9e102b324300939da14, lifecycle/1c09fadde930b03b7518, lifecycle/c07af59a8d393975dd28, lifecycle/f706db5c42869fee8ea5, lifecycle/371f67d50254479493ee, lifecycle/b72ae27c889b5f309c7d, lifecycle/0f45aa8eb79d60157031, lifecycle/d8087ff55a7a9c1902cc, lifecycle/73c19173fcc983318b61, lifecycle/dbb5a42b977bbac7679e, lifecycle/12c678df16e04f4f9011, lifecycle/720a326dbad29c263006, lifecycle/97d2ae3cab5f9bbc9d8f, lifecycle/e0e005616c964f881ccd, lifecycle/12348bea7be2ca70cffb, lifecycle/ff61f1cb7a87d8382b9a, lifecycle/d34ebb3d52e02dfb8b16, lifecycle/5f300473b328b24bac66, lifecycle/780ad479b1fe66279696, lifecycle/afc236d86c1d2fad6db9, lifecycle/fa028d54604cd08d3555, lifecycle/9b34de15d3aca2deb34c, lifecycle/99d7c3c7623e3d43d059, lifecycle/93f7eea188801e17127a]
  rule: Any imaging dataset with a Delaunay pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: imaging-delaunay-standard-cpu-many-core
  title: 'Designation: imaging/delaunay standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/b202eb6f7da58a38882f, lifecycle/095071358666d6efbc20, lifecycle/5556ca430bc180c2d536, lifecycle/99cf9f43e4608fb548ea, lifecycle/06a9dad80c65ecd81c6c, lifecycle/51b8245cf58b86533327, lifecycle/321ec1f6f2a5955a9a20, lifecycle/3c0e90f2b30d48843af2, lifecycle/b5b87c504713b9831857, lifecycle/489bebc145a525eab14d, lifecycle/d93b4dad29e8a0f77987, lifecycle/e3b1cad17937b4c1f9dc, lifecycle/e08b7a6ff7b9daea8790, lifecycle/e77729fc4ba5d235e1b0, lifecycle/1f22a4a5fcd73276ec53, lifecycle/572824ce3cc75acae94b]
  rule: Any imaging dataset with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS).
  supersedes: null
# separation: separated
- id: imaging-delaunay-nn-standard-gpu-a100
  title: 'Designation: imaging/delaunay_nn standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-nn-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/delaunay_nn
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64, jax_cpu_sparse_fp64]
  evidence: [lifecycle/cbc5540f3214caf61aba, lifecycle/5033bab3983481d5c826, lifecycle/c661098ad46c65fa59b2, lifecycle/2461a4934062a3be2dc9, lifecycle/70bcae3ab1c4777651f0, lifecycle/5082531d009e61e07a7d]
  rule: Any imaging dataset with a Delaunay natural-neighbour source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: separated
- id: imaging-delaunay-nn-standard-cpu-many-core
  title: 'Designation: imaging/delaunay_nn standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-nn-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/delaunay_nn
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/1ae46b0872f10459a7c4, lifecycle/2e8ae296db66eeaf44a7, lifecycle/05dde64a0eb7fdd0c4a1, lifecycle/22e86297033ff62cf19e]
  rule: Any imaging dataset with a Delaunay natural-neighbour source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core.
  supersedes: null
# separation: uncontested
- id: interferometer-mge-n-vis-lt-1e5-gpu-a100
  title: 'Designation: interferometer/mge n_vis_lt_1e5 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-mge-n-vis-lt-1e5-gpu-a100.md
  kind: designation
  likelihood: interferometer/mge
  regime: n_vis_lt_1e5
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64_nufft
  secondary: []
  evidence: [lifecycle/4c9e3b4239cc98b8a7ff, lifecycle/6cfb178c7acab8b84e63]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64_nufft.
  supersedes: null
# separation: uncontested
- id: interferometer-mge-n-vis-lt-1e5-cpu-many-core
  title: 'Designation: interferometer/mge n_vis_lt_1e5 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-mge-n-vis-lt-1e5-cpu-many-core.md
  kind: designation
  likelihood: interferometer/mge
  regime: n_vis_lt_1e5
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64_nufft
  secondary: []
  evidence: [lifecycle/02e5496a9c9da3407d87, lifecycle/9a3e014c9053e1d98114]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64_nufft.
  supersedes: null
# separation: separated
- id: interferometer-rectangular-n-vis-lt-1e5-gpu-a100
  title: 'Designation: interferometer/rectangular n_vis_lt_1e5 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-lt-1e5-gpu-a100.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_lt_1e5
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: [jax_gpu_dense_fp64_nufft]
  evidence: [lifecycle/e44acbf15a2387706fa1, lifecycle/18947283f540e425ae11, lifecycle/a39d6114339d546f6bd6, lifecycle/e98a8f4000e25e6d9f35]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a rectangular pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde, falling back to jax_gpu_dense_fp64_nufft.
  supersedes: null
# separation: uncontested
- id: interferometer-rectangular-n-vis-1e5-1e7-gpu-a100
  title: 'Designation: interferometer/rectangular n_vis_1e5_1e7 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-1e5-1e7-gpu-a100.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_1e5_1e7
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: []
  evidence: [lifecycle/fe32c3ee13ad9afc455c, lifecycle/94c8f316ca657a6536ad, lifecycle/2ab9504c46bb8170ba54, lifecycle/1aafc8c30c529ae51479]
  rule: An interferometer dataset with 1e5 to 1e7 visibilities and a rectangular pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde (the dense route cannot form its mapping matrix above 1e5 visibilities).
  supersedes: null
# separation: uncontested
- id: interferometer-rectangular-n-vis-ge-1e7-gpu-a100
  title: 'Designation: interferometer/rectangular n_vis_ge_1e7 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-ge-1e7-gpu-a100.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_ge_1e7
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: []
  evidence: [lifecycle/220d076d8421130e83cf, lifecycle/7aad4d80e0298f32687c]
  rule: An interferometer dataset with at least 1e7 visibilities and a rectangular pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde (streaming not measured).
  supersedes: null
# separation: separated
- id: interferometer-rectangular-n-vis-lt-1e5-cpu-many-core
  title: 'Designation: interferometer/rectangular n_vis_lt_1e5 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-lt-1e5-cpu-many-core.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_lt_1e5
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde, jax_cpu_dense_fp64_nufft]
  evidence: [lifecycle/0cec032ed12d6d948802, lifecycle/ad305d23a04bd7700b82, lifecycle/29d350ddd936276d4121, lifecycle/f90468fb8090019a8659, lifecycle/0e27b1175ce084dff51e, lifecycle/f8de59681124b4e117d2]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core, with the curvature route chosen by the packaged cost model.
  supersedes: null
# separation: separated
- id: interferometer-rectangular-n-vis-1e5-1e7-cpu-many-core
  title: 'Designation: interferometer/rectangular n_vis_1e5_1e7 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-1e5-1e7-cpu-many-core.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_1e5_1e7
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/41fd14e1f19bad947f24, lifecycle/5772383ee5a1c474afff, lifecycle/4663f221c8c3ce49b76f, lifecycle/85d104c103a554b56afa, lifecycle/fe0f252f68dcc26d7d13, lifecycle/7f44ae97f7ce3ccc7864, lifecycle/d79f1b94f4b03452d745, lifecycle/af1beefd41024500ad13]
  rule: An interferometer dataset with 1e5 to 1e7 visibilities and a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core, with the curvature route chosen by the packaged cost model.
  supersedes: null
# separation: separated
- id: interferometer-rectangular-n-vis-ge-1e7-cpu-many-core
  title: 'Designation: interferometer/rectangular n_vis_ge_1e7 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-n-vis-ge-1e7-cpu-many-core.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: n_vis_ge_1e7
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/99c70939e335d08c4cff, lifecycle/8aeeeff35ca0d5d5b855, lifecycle/15aded078686cdf03ff5, lifecycle/598903fd79ec17f4328f]
  rule: An interferometer dataset with at least 1e7 visibilities and a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, with workers capped by node memory over peak RSS.
  supersedes: null
# separation: separated
- id: interferometer-delaunay-n-vis-lt-1e5-gpu-a100
  title: 'Designation: interferometer/delaunay n_vis_lt_1e5 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-lt-1e5-gpu-a100.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_lt_1e5
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: [jax_gpu_dense_fp64_nufft]
  evidence: [lifecycle/ff5c53947f845ee5f2d8, lifecycle/7babc936c9e3d3d61400, lifecycle/742eaf1292ed737e591e, lifecycle/f0257d6c38e984e02a27]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a delaunay pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde, falling back to jax_gpu_dense_fp64_nufft.
  supersedes: null
# separation: uncontested
- id: interferometer-delaunay-n-vis-1e5-1e7-gpu-a100
  title: 'Designation: interferometer/delaunay n_vis_1e5_1e7 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-1e5-1e7-gpu-a100.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_1e5_1e7
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: []
  evidence: [lifecycle/8dada4df3a4ed30d1721, lifecycle/3604b6b6097ea2ead0a3, lifecycle/ba12584bdfe8c2e16f30, lifecycle/d1bef0d03e8078e165cf]
  rule: An interferometer dataset with 1e5 to 1e7 visibilities and a delaunay pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde (the dense route cannot form its mapping matrix above 1e5 visibilities).
  supersedes: null
# separation: uncontested
- id: interferometer-delaunay-n-vis-ge-1e7-gpu-a100
  title: 'Designation: interferometer/delaunay n_vis_ge_1e7 gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-ge-1e7-gpu-a100.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_ge_1e7
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: []
  evidence: [lifecycle/3c33efbabefe647c901b, lifecycle/20d0956c95b461dbae98]
  rule: An interferometer dataset with at least 1e7 visibilities and a delaunay pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde (streaming not measured).
  supersedes: null
# separation: separated
- id: interferometer-delaunay-n-vis-lt-1e5-cpu-many-core
  title: 'Designation: interferometer/delaunay n_vis_lt_1e5 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-lt-1e5-cpu-many-core.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_lt_1e5
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde, jax_cpu_dense_fp64_nufft]
  evidence: [lifecycle/284efdc05b70e06e060a, lifecycle/56f48185c11f75209119, lifecycle/00838694b2c3c955a644, lifecycle/a152a69dfb443926581d, lifecycle/b2d01ef74bf71e49d774, lifecycle/ea2702adb920859138bf]
  rule: An interferometer dataset with fewer than 1e5 visibilities and a delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core, with the curvature route chosen by the packaged cost model.
  supersedes: null
# separation: separated
- id: interferometer-delaunay-n-vis-1e5-1e7-cpu-many-core
  title: 'Designation: interferometer/delaunay n_vis_1e5_1e7 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-1e5-1e7-cpu-many-core.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_1e5_1e7
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/60747d6f7a1867da50c9, lifecycle/72fa1f4145e1b837daad, lifecycle/5e9d64046821795b4651, lifecycle/52f7465981114aecc98d, lifecycle/d54c6814c51c381564cf, lifecycle/ebd642f6c596e964cea9, lifecycle/bfe464d85eab437c56be, lifecycle/2790184b43d78bf4da78]
  rule: An interferometer dataset with 1e5 to 1e7 visibilities and a delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core, with the curvature route chosen by the packaged cost model.
  supersedes: null
# separation: HOLD - does not separate; do not record as written
- id: interferometer-delaunay-n-vis-ge-1e7-cpu-many-core
  title: 'Designation: interferometer/delaunay n_vis_ge_1e7 cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-n-vis-ge-1e7-cpu-many-core.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: n_vis_ge_1e7
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/757d2c2d7167cdef0457, lifecycle/b9bd70be62ec18cf0a02, lifecycle/e63a97d451e1633c91aa, lifecycle/bb2f3d9734b53f7fca77]
  rule: An interferometer dataset with at least 1e7 visibilities and a delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, with workers capped by node memory over peak RSS.
  supersedes: null
# separation: uncontested
- id: point-source-image-image-plane-standard-gpu-a100
  title: 'Designation: point_source_image/image_plane standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-image-image-plane-standard-gpu-a100.md
  kind: designation
  likelihood: point_source_image/image_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_na_fp64
  secondary: []
  evidence: [lifecycle/6282556b81be530f7bce, lifecycle/f4dfadf54484b22e9f69]
  rule: A galaxy-scale point-source dataset fitted in the image plane on an A100 node uses jax_gpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: point-source-image-image-plane-standard-cpu-many-core
  title: 'Designation: point_source_image/image_plane standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-image-image-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: point_source_image/image_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/6cbf08c848ae6cdb820f, lifecycle/a884951a80a697791744]
  rule: A galaxy-scale point-source dataset fitted in the image plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
# separation: per-node only
- id: point-source-source-source-plane-standard-gpu-a100
  title: 'Designation: point_source_source/source_plane standard gpu_a100'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-source-source-plane-standard-gpu-a100.md
  kind: designation
  likelihood: point_source_source/source_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_cpu_na_fp64
  secondary: [jax_gpu_na_fp64]
  evidence: [lifecycle/c2bfeea342f97959dc7c, lifecycle/5e68a4c3f41437c52c70, lifecycle/fcb319f0f24b8cc9fd37, lifecycle/403a31905c1445a750ba]
  rule: A galaxy-scale point-source dataset fitted in the source plane on an A100 node uses jax_cpu_na_fp64 on the node CPU cores, not the GPUs.
  supersedes: null
# separation: uncontested
- id: point-source-source-source-plane-standard-cpu-many-core
  title: 'Designation: point_source_source/source_plane standard cpu_many_core'
  date: YYYY-MM-DD
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-source-source-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: point_source_source/source_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/61082dc032d7280b3bd1, lifecycle/fa18efad842f4cc9fa73]
  rule: A galaxy-scale point-source dataset fitted in the source plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
```

## Appendix B — re-derived 2026-10-31 on the day-zero catalogue (PR #496 head c218a428; NOT published)

```yaml
# separation: uncontested
- id: cluster-image-plane-standard-cpu-many-core
  title: 'Designation: cluster/image_plane standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/cluster-image-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: cluster/image_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/86d6277f36e3c8ec1d2f, lifecycle/0533eec58c25ebd8637b]
  rule: A cluster-scale point-source dataset fitted in the image plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: cluster-image-plane-standard-gpu-a100
  title: 'Designation: cluster/image_plane standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/cluster-image-plane-standard-gpu-a100.md
  kind: designation
  likelihood: cluster/image_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_na_fp64
  secondary: []
  evidence: [lifecycle/d92190013ae10eaa21f6, lifecycle/7e5edbcfcccee90b11b5]
  rule: A cluster-scale point-source dataset fitted in the image plane on an A100 node uses jax_gpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: cluster-source-plane-standard-cpu-many-core
  title: 'Designation: cluster/source_plane standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/cluster-source-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: cluster/source_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/004001caf29a727421e0, lifecycle/8909566077ecf0ba922a]
  rule: A cluster-scale point-source dataset fitted in the source plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: cluster-source-plane-standard-gpu-a100
  title: 'Designation: cluster/source_plane standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/cluster-source-plane-standard-gpu-a100.md
  kind: designation
  likelihood: cluster/source_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_na_fp64
  secondary: []
  evidence: [lifecycle/02df871c3e8378b505ca, lifecycle/34d551d02bba3ac253a1]
  rule: A cluster-scale point-source dataset fitted in the source plane on an A100 node uses jax_gpu_na_fp64.
  supersedes: null
# separation: separated
- id: datacube-delaunay-standard-cpu-many-core
  title: 'Designation: datacube/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/datacube-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: datacube/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/8e374ab509e7626573da, lifecycle/b767269193c94e381a30, lifecycle/5800a501664b981824d4, lifecycle/821bc78b048e1ae58e0a, lifecycle/6669e2835516e93361f1, lifecycle/3339ddf063b8cf824048, lifecycle/3ea56488a996d6f0ffd1, lifecycle/ffa08d2b2e0136acbb7d, lifecycle/84cc85952546c05eabe2, lifecycle/803151df21c7de55861a, lifecycle/649dfad640b1afce5631, lifecycle/8f9413a9807f794ae36e, lifecycle/5b411896dcf5b1cc5853, lifecycle/cdcbd9feaefdff4aba33]
  rule: A datacube (interferometer channels fitted together) with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64_wtilde.
  supersedes: null
# separation: does not separate  — HOLD: does not separate; do not record as written
- id: datacube-delaunay-standard-gpu-a100
  title: 'Designation: datacube/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/datacube-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: datacube/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: [jax_gpu_dense_fp64_nufft]
  evidence: [lifecycle/c3ed1c5a8847d28eb792, lifecycle/7c22bd05b2e6a332c05f, lifecycle/5ddc372d7a91e6f979a8, lifecycle/9779431a4492758cb70b, lifecycle/b62555fd25c854bfdf3d, lifecycle/bb703db94dff9a1c1ff7, lifecycle/5a76ad3529beab044b72, lifecycle/2dd892f07fead03714bf]
  rule: A datacube (interferometer channels fitted together) with a Delaunay pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde, falling back to jax_gpu_dense_fp64_nufft.
  supersedes: null
# separation: separated
- id: group-delaunay-standard-cpu-many-core
  title: 'Designation: group/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: group/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/f4474b23fc3ee5d4b43f, lifecycle/3312f41b04546c2ef2b6, lifecycle/22696238c7226a6971dd, lifecycle/15ff2e809477e969c467]
  rule: A group-scale imaging dataset with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: group-delaunay-standard-gpu-a100
  title: 'Designation: group/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: group/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/826e517e5786c2398767, lifecycle/4d43ba6e6f51755c0a00, lifecycle/af408d3bf87b7b904f2d, lifecycle/a99fbbd0cb8f8eaedcc4]
  rule: A group-scale imaging dataset with a Delaunay pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: uncontested
- id: group-mge-standard-cpu-many-core
  title: 'Designation: group/mge standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-mge-standard-cpu-many-core.md
  kind: designation
  likelihood: group/mge
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64
  secondary: []
  evidence: [lifecycle/eb438402eb57e940aa63, lifecycle/5637649f49871e13e428]
  rule: A group-scale imaging dataset with a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: group-mge-standard-gpu-a100
  title: 'Designation: group/mge standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-mge-standard-gpu-a100.md
  kind: designation
  likelihood: group/mge
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: []
  evidence: [lifecycle/c631285eca889fc2c2c4, lifecycle/883d959ca124d30992b1]
  rule: A group-scale imaging dataset with a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: separated
- id: group-rectangular-standard-cpu-many-core
  title: 'Designation: group/rectangular standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-rectangular-standard-cpu-many-core.md
  kind: designation
  likelihood: group/rectangular
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/acba8d20547d37e8f89c, lifecycle/6e8c2db0c3afbfa0112f, lifecycle/a393fa2e139fd0560564, lifecycle/d1eb8e9cc712b7a123b0]
  rule: A group-scale imaging dataset with a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: group-rectangular-standard-gpu-a100
  title: 'Designation: group/rectangular standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/group-rectangular-standard-gpu-a100.md
  kind: designation
  likelihood: group/rectangular
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/506bcbce87ad6c020945, lifecycle/e69558ac3425ca0f7c32, lifecycle/34335ddd284ac5077dc2, lifecycle/1fd3b971b77882c2ec7f]
  rule: A group-scale imaging dataset with a rectangular pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: imaging-delaunay-standard-cpu-many-core
  title: 'Designation: imaging/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/e08b7a6ff7b9daea8790, lifecycle/e77729fc4ba5d235e1b0, lifecycle/1f22a4a5fcd73276ec53, lifecycle/572824ce3cc75acae94b, lifecycle/b202eb6f7da58a38882f, lifecycle/095071358666d6efbc20, lifecycle/5556ca430bc180c2d536, lifecycle/99cf9f43e4608fb548ea, lifecycle/06a9dad80c65ecd81c6c, lifecycle/51b8245cf58b86533327, lifecycle/321ec1f6f2a5955a9a20, lifecycle/3c0e90f2b30d48843af2, lifecycle/b5b87c504713b9831857, lifecycle/489bebc145a525eab14d, lifecycle/d93b4dad29e8a0f77987, lifecycle/e3b1cad17937b4c1f9dc]
  rule: Any imaging dataset with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS).
  supersedes: null
# separation: separated
- id: imaging-delaunay-standard-gpu-a100
  title: 'Designation: imaging/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/fa028d54604cd08d3555, lifecycle/9b34de15d3aca2deb34c, lifecycle/99d7c3c7623e3d43d059, lifecycle/93f7eea188801e17127a, lifecycle/c07af59a8d393975dd28, lifecycle/f706db5c42869fee8ea5, lifecycle/371f67d50254479493ee, lifecycle/b72ae27c889b5f309c7d, lifecycle/73c19173fcc983318b61, lifecycle/dbb5a42b977bbac7679e, lifecycle/12c678df16e04f4f9011, lifecycle/720a326dbad29c263006, lifecycle/12348bea7be2ca70cffb, lifecycle/ff61f1cb7a87d8382b9a, lifecycle/d34ebb3d52e02dfb8b16, lifecycle/5f300473b328b24bac66]
  rule: Any imaging dataset with a Delaunay pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: imaging-delaunay-nn-standard-cpu-many-core
  title: 'Designation: imaging/delaunay_nn standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-nn-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/delaunay_nn
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/1ae46b0872f10459a7c4, lifecycle/2e8ae296db66eeaf44a7, lifecycle/05dde64a0eb7fdd0c4a1, lifecycle/22e86297033ff62cf19e]
  rule: Any imaging dataset with a Delaunay natural-neighbour source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core.
  supersedes: null
# separation: separated
- id: imaging-delaunay-nn-standard-gpu-a100
  title: 'Designation: imaging/delaunay_nn standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-delaunay-nn-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/delaunay_nn
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/c661098ad46c65fa59b2, lifecycle/2461a4934062a3be2dc9, lifecycle/70bcae3ab1c4777651f0, lifecycle/5082531d009e61e07a7d]
  rule: Any imaging dataset with a Delaunay natural-neighbour source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: imaging-mge-standard-cpu-many-core
  title: 'Designation: imaging/mge standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-mge-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/mge
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64
  secondary: []
  evidence: [lifecycle/3216ffc143645fb46c72, lifecycle/a37560173314cc078894, lifecycle/190ebc582d9aba9aaa9c, lifecycle/acf067a34aa2005d1b11, lifecycle/54979849c807d452c510, lifecycle/d2aece86956eba227ada, lifecycle/4baa9bc04c8d24a713b6, lifecycle/2cf94e6d7d8231a57c92]
  rule: Any imaging dataset fitted with a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: imaging-mge-standard-gpu-a100
  title: 'Designation: imaging/mge standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-mge-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/mge
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: []
  evidence: [lifecycle/4b514c4262172f610fee, lifecycle/eb44c9d7e6987735cdd1, lifecycle/770dce7d7db7a1fc3b53, lifecycle/2d7064bb66242f2ca6cc, lifecycle/8a475e9abd97a8c4a1c0, lifecycle/4e93e744f3e1295b3c8d, lifecycle/0756e600e86d7ae6a462, lifecycle/a58929ead49f62c064da]
  rule: Any imaging dataset fitted with a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: separated
- id: imaging-rectangular-standard-cpu-many-core
  title: 'Designation: imaging/rectangular standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-rectangular-standard-cpu-many-core.md
  kind: designation
  likelihood: imaging/rectangular
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/d7020017fca2249bf32b, lifecycle/e44433f6b0bb6fbb1519, lifecycle/403420f8debaaa38956c, lifecycle/a721c437cf9355984ca5, lifecycle/4c53e409a27040f5d6a4, lifecycle/39a0a9b81376f2be8446, lifecycle/6060fdcfa2e5a4a0c168, lifecycle/ae663292d53c60a65c62, lifecycle/2b5e34f509175fd4d030, lifecycle/ee2df565d3603ba2bbd3, lifecycle/b62534053c00fb102bf4, lifecycle/9e90c7a031fd6370f9af, lifecycle/9bb2e30e94491253641b, lifecycle/dd67472c35e8ed230b03, lifecycle/304ac75d242dcbc2c22f, lifecycle/0de8cf81e718d21ee2aa]
  rule: Any imaging dataset with a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS).
  supersedes: null
# separation: separated
- id: imaging-rectangular-standard-gpu-a100
  title: 'Designation: imaging/rectangular standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/imaging-rectangular-standard-gpu-a100.md
  kind: designation
  likelihood: imaging/rectangular
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/d570569f32c953038fde, lifecycle/32ca51df82e1724685ab, lifecycle/46db4990a22e25aee123, lifecycle/67787bf45d6bb0b3aa42, lifecycle/456f7d65babc5524183a, lifecycle/a429326f9f33ea12e6b8, lifecycle/bc5ed323618c58fc7682, lifecycle/688c98aeb69ac24ea6f3, lifecycle/42f6a707360ce63b8150, lifecycle/9bbfceb21916e4329a0a, lifecycle/cc3f3365b6ac65388a93, lifecycle/27f711205e5a76c127cb, lifecycle/ec69a200557ea8212e5e, lifecycle/76d01fc60350dd469eed, lifecycle/bdffd9d6d157b3b66435, lifecycle/df1e242101ab32dea573]
  rule: Any imaging dataset with a rectangular pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: interferometer-delaunay-standard-cpu-many-core
  title: 'Designation: interferometer/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/60747d6f7a1867da50c9, lifecycle/72fa1f4145e1b837daad, lifecycle/5e9d64046821795b4651, lifecycle/52f7465981114aecc98d, lifecycle/d54c6814c51c381564cf, lifecycle/ebd642f6c596e964cea9, lifecycle/bfe464d85eab437c56be, lifecycle/2790184b43d78bf4da78, lifecycle/757d2c2d7167cdef0457, lifecycle/b9bd70be62ec18cf0a02, lifecycle/e63a97d451e1633c91aa, lifecycle/bb2f3d9734b53f7fca77, lifecycle/284efdc05b70e06e060a, lifecycle/56f48185c11f75209119, lifecycle/00838694b2c3c955a644, lifecycle/a152a69dfb443926581d, lifecycle/b2d01ef74bf71e49d774, lifecycle/ea2702adb920859138bf]
  rule: Any interferometer dataset with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64_wtilde. Untested: CPU streaming and the MGE DFT route.
  supersedes: null
# separation: separated
- id: interferometer-delaunay-standard-gpu-a100
  title: 'Designation: interferometer/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: interferometer/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: [jax_gpu_dense_fp64_nufft]
  evidence: [lifecycle/8dada4df3a4ed30d1721, lifecycle/3604b6b6097ea2ead0a3, lifecycle/ba12584bdfe8c2e16f30, lifecycle/d1bef0d03e8078e165cf, lifecycle/3c33efbabefe647c901b, lifecycle/20d0956c95b461dbae98, lifecycle/ff5c53947f845ee5f2d8, lifecycle/7babc936c9e3d3d61400, lifecycle/742eaf1292ed737e591e, lifecycle/f0257d6c38e984e02a27]
  rule: Any interferometer dataset with a Delaunay pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde, falling back to jax_gpu_dense_fp64_nufft. Untested: the GPU streaming route (measured up to jvla, 2.5e7 visibilities, on W~ sparse).
  supersedes: null
# separation: uncontested
- id: interferometer-mge-standard-cpu-many-core
  title: 'Designation: interferometer/mge standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-mge-standard-cpu-many-core.md
  kind: designation
  likelihood: interferometer/mge
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64_nufft
  secondary: []
  evidence: [lifecycle/02e5496a9c9da3407d87, lifecycle/9a3e014c9053e1d98114]
  rule: Any interferometer dataset with a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64_nufft. Untested: CPU streaming and the MGE DFT route.
  supersedes: null
# separation: uncontested
- id: interferometer-mge-standard-gpu-a100
  title: 'Designation: interferometer/mge standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-mge-standard-gpu-a100.md
  kind: designation
  likelihood: interferometer/mge
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64_nufft
  secondary: []
  evidence: [lifecycle/4c9e3b4239cc98b8a7ff, lifecycle/6cfb178c7acab8b84e63]
  rule: Any interferometer dataset with a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64_nufft. Untested: the GPU streaming route (measured up to jvla, 2.5e7 visibilities, on W~ sparse).
  supersedes: null
# separation: separated
- id: interferometer-rectangular-standard-cpu-many-core
  title: 'Designation: interferometer/rectangular standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-standard-cpu-many-core.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64_wtilde
  secondary: [jax_cpu_sparse_fp64_wtilde]
  evidence: [lifecycle/41fd14e1f19bad947f24, lifecycle/5772383ee5a1c474afff, lifecycle/4663f221c8c3ce49b76f, lifecycle/85d104c103a554b56afa, lifecycle/fe0f252f68dcc26d7d13, lifecycle/7f44ae97f7ce3ccc7864, lifecycle/d79f1b94f4b03452d745, lifecycle/af1beefd41024500ad13, lifecycle/99c70939e335d08c4cff, lifecycle/8aeeeff35ca0d5d5b855, lifecycle/15aded078686cdf03ff5, lifecycle/598903fd79ec17f4328f, lifecycle/0cec032ed12d6d948802, lifecycle/ad305d23a04bd7700b82, lifecycle/29d350ddd936276d4121, lifecycle/f90468fb8090019a8659, lifecycle/0e27b1175ce084dff51e, lifecycle/f8de59681124b4e117d2]
  rule: Any interferometer dataset with a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64_wtilde, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64_wtilde. Untested: CPU streaming and the MGE DFT route.
  supersedes: null
# separation: separated
- id: interferometer-rectangular-standard-gpu-a100
  title: 'Designation: interferometer/rectangular standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-rectangular-standard-gpu-a100.md
  kind: designation
  likelihood: interferometer/rectangular
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_sparse_fp64_wtilde
  secondary: [jax_gpu_dense_fp64_nufft]
  evidence: [lifecycle/fe32c3ee13ad9afc455c, lifecycle/94c8f316ca657a6536ad, lifecycle/2ab9504c46bb8170ba54, lifecycle/1aafc8c30c529ae51479, lifecycle/220d076d8421130e83cf, lifecycle/7aad4d80e0298f32687c, lifecycle/e44acbf15a2387706fa1, lifecycle/18947283f540e425ae11, lifecycle/a39d6114339d546f6bd6, lifecycle/e98a8f4000e25e6d9f35]
  rule: Any interferometer dataset with a rectangular pixelized source on an A100 node uses jax_gpu_sparse_fp64_wtilde, falling back to jax_gpu_dense_fp64_nufft. Untested: the GPU streaming route (measured up to jvla, 2.5e7 visibilities, on W~ sparse).
  supersedes: null
# separation: separated
- id: multi-dataset-delaunay-standard-cpu-many-core
  title: 'Designation: multi_dataset/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-dataset-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: multi_dataset/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/f1dc379c56f5c2c7f32d, lifecycle/41ebc7e42114bbb5173a, lifecycle/f57f23fc63823bcdf1bc, lifecycle/d0be4a7b3506be7b53e9]
  rule: A multi-dataset imaging fit (several datasets fitted together) with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: multi-dataset-delaunay-standard-gpu-a100
  title: 'Designation: multi_dataset/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-dataset-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: multi_dataset/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/b5dea27fcaf8b14ec9bb, lifecycle/0a0078bdc1dee2e7f555, lifecycle/b14372bc431d168fa7ff, lifecycle/74d94bd622ecce0679fe]
  rule: A multi-dataset imaging fit (several datasets fitted together) with a Delaunay pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: multi-galaxy-delaunay-standard-cpu-many-core
  title: 'Designation: multi_galaxy/delaunay standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-delaunay-standard-cpu-many-core.md
  kind: designation
  likelihood: multi_galaxy/delaunay
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/d3102456687aef830651, lifecycle/844f80aec856dd9e86ff, lifecycle/fc2096cb1c848e64b674, lifecycle/ba7ba9f1625678852fd7]
  rule: A multi-galaxy imaging dataset with a Delaunay pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: multi-galaxy-delaunay-standard-gpu-a100
  title: 'Designation: multi_galaxy/delaunay standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-delaunay-standard-gpu-a100.md
  kind: designation
  likelihood: multi_galaxy/delaunay
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/5a510cca4fff0c0d5b58, lifecycle/dfd272620e2836754417, lifecycle/ec0a8fbc9c4e2d8b587e, lifecycle/633b3471528047682453]
  rule: A multi-galaxy imaging dataset with a Delaunay pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: uncontested
- id: multi-galaxy-mge-standard-cpu-many-core
  title: 'Designation: multi_galaxy/mge standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-mge-standard-cpu-many-core.md
  kind: designation
  likelihood: multi_galaxy/mge
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64
  secondary: []
  evidence: [lifecycle/2ee75bc51ab781c2df4e, lifecycle/9edfaee55c6a1193e6f4]
  rule: A multi-galaxy imaging dataset with a parametric (MGE) source on a many-core CPU node with no GPU uses jax_cpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: multi-galaxy-mge-standard-gpu-a100
  title: 'Designation: multi_galaxy/mge standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-mge-standard-gpu-a100.md
  kind: designation
  likelihood: multi_galaxy/mge
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: []
  evidence: [lifecycle/ad7e6ff9cd88a460649a, lifecycle/9068d8507411cfbcf803]
  rule: A multi-galaxy imaging dataset with a parametric (MGE) source on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
# separation: separated
- id: multi-galaxy-rectangular-standard-cpu-many-core
  title: 'Designation: multi_galaxy/rectangular standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-rectangular-standard-cpu-many-core.md
  kind: designation
  likelihood: multi_galaxy/rectangular
  regime: standard
  hardware_class: cpu_many_core
  optimal: numba_cpu_sparse_fp64
  secondary: [jax_cpu_sparse_fp64]
  evidence: [lifecycle/51f5d0ecf49223f09154, lifecycle/d7185e051ab18a8d35e1, lifecycle/a3ef052bb150d3365992, lifecycle/b7ba7f751e33237bf6a3]
  rule: A multi-galaxy imaging dataset with a rectangular pixelized source on a many-core CPU node with no GPU uses numba_cpu_sparse_fp64, one serial likelihood per core (workers capped by node memory over peak RSS), falling back to jax_cpu_sparse_fp64.
  supersedes: null
# separation: separated
- id: multi-galaxy-rectangular-standard-gpu-a100
  title: 'Designation: multi_galaxy/rectangular standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/multi-galaxy-rectangular-standard-gpu-a100.md
  kind: designation
  likelihood: multi_galaxy/rectangular
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: [jax_gpu_sparse_fp64]
  evidence: [lifecycle/6d59cdcd3eb1e4abf967, lifecycle/e291f6a166388b23e52f, lifecycle/f6d5339ad2b2bd8b790b, lifecycle/dd733151c3847dd9349f]
  rule: A multi-galaxy imaging dataset with a rectangular pixelized source on an A100 node uses jax_gpu_dense_fp64, falling back to jax_gpu_sparse_fp64.
  supersedes: null
# separation: uncontested
- id: point-source-image-image-plane-standard-cpu-many-core
  title: 'Designation: point_source_image/image_plane standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-image-image-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: point_source_image/image_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/6cbf08c848ae6cdb820f, lifecycle/a884951a80a697791744]
  rule: A galaxy-scale point-source dataset fitted in the image plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: point-source-image-image-plane-standard-gpu-a100
  title: 'Designation: point_source_image/image_plane standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-image-image-plane-standard-gpu-a100.md
  kind: designation
  likelihood: point_source_image/image_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_na_fp64
  secondary: []
  evidence: [lifecycle/6282556b81be530f7bce, lifecycle/f4dfadf54484b22e9f69]
  rule: A galaxy-scale point-source dataset fitted in the image plane on an A100 node uses jax_gpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: point-source-source-source-plane-standard-cpu-many-core
  title: 'Designation: point_source_source/source_plane standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-source-source-plane-standard-cpu-many-core.md
  kind: designation
  likelihood: point_source_source/source_plane
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_na_fp64
  secondary: []
  evidence: [lifecycle/61082dc032d7280b3bd1, lifecycle/fa18efad842f4cc9fa73]
  rule: A galaxy-scale point-source dataset fitted in the source plane on a many-core CPU node with no GPU uses jax_cpu_na_fp64.
  supersedes: null
# separation: uncontested  — CHANGED from 2026-10-29 (was jax_cpu_na_fp64)
- id: point-source-source-source-plane-standard-gpu-a100
  title: 'Designation: point_source_source/source_plane standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/point-source-source-source-plane-standard-gpu-a100.md
  kind: designation
  likelihood: point_source_source/source_plane
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_na_fp64
  secondary: []
  evidence: [lifecycle/fcb319f0f24b8cc9fd37, lifecycle/403a31905c1445a750ba]
  rule: A galaxy-scale point-source dataset fitted in the source plane on an A100 node uses jax_gpu_na_fp64.
  supersedes: null
# separation: uncontested
- id: weak-isothermal-standard-cpu-many-core
  title: 'Designation: weak/isothermal standard cpu_many_core'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/weak-isothermal-standard-cpu-many-core.md
  kind: designation
  likelihood: weak/isothermal
  regime: standard
  hardware_class: cpu_many_core
  optimal: jax_cpu_dense_fp64
  secondary: []
  evidence: [lifecycle/03601d3a29aca4f5c389, lifecycle/7f6973aafe0b068ba1ab]
  rule: A weak-lensing shear dataset with an isothermal lens on a many-core CPU node with no GPU uses jax_cpu_dense_fp64.
  supersedes: null
# separation: uncontested
- id: weak-isothermal-standard-gpu-a100
  title: 'Designation: weak/isothermal standard gpu_a100'
  date: 'YYYY-MM-DD'
  url: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/weak-isothermal-standard-gpu-a100.md
  kind: designation
  likelihood: weak/isothermal
  regime: standard
  hardware_class: gpu_a100
  optimal: jax_gpu_dense_fp64
  secondary: []
  evidence: [lifecycle/fbd315b1a0e03f308c76, lifecycle/bfd2db209cd80e6a6354]
  rule: A weak-lensing shear dataset with an isothermal lens on an A100 node uses jax_gpu_dense_fp64.
  supersedes: null
```
