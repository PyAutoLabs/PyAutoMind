Phase 2a of the likelihood-lifecycle epic profiled every imaging likelihood (mge, rectangular, delaunay, delaunay_nn) at the standard production size on tag 2026.10.23.1, across RAL CPU and A100 setups, and committed the rows with parity witnesses.

- **PR A #457:** standard-size cells matching production subhalo_validation (Delaunay 1250 Hilbert + 30 edge, rectangular `RectangularBilinearAdaptImage` 35², over-sampling cut on the uncapped S/N map), parity.json (eager NumPy dense reference), generated submits with a tag/import guard.
- **Batch 0** (timing arm; RAL 412877 + 412884; reruns 412911 + 412915): 32/34. Four breakdown-script bugs fixed in **#458**. The ao `jax_gpu_dense` breakdowns (delaunay and rectangular) run out of A100 memory on the 384,753×1,280 fp64 blurred mapping matrix; HUMAN RULING: recorded limitation, not rerun.
- **#459:** guard test only. The suspected pix_sizes omission in the interferometer/datacube scripts was a false alarm; the library leaves those curvature triplets unmasked too.
- **#460:** batch-1 `--time`/`--mem` from measured walls and MaxRSS (1.25× + 15 min, 32 GB floor).
- **Batch 1** (RAL 412923–412926 + A100 412927, 412943–412945): 104/106, the 2 limitations.
- **PR B #461:** 104 rows (53 cells), 13 superseded rows → history/, parity 53/53 match. Coverage across 246 planned went from 2/6/238 to 104/7/135 (current/stale/missing). New catalogue/release_revisions.json: tag source checkouts stamp 2026.8.17.1, so release_pin comes from an exact library-SHA match. Wiki page `wiki/campaigns/imaging/likelihood_lifecycle_p2a.md`.
- **PyAutoPulse#75:** lens receipt 679 records at eef5edfe; `hst_mge_cpu_pilot` superseded by the 2a mge/hst CPU cell (human 2026-10-25); autolens_profiling#415 closed.

Per-call evidence: `jax_gpu_dense@a100` is fastest per call everywhere (ao: mge 19 ms, rectangular 311 ms, delaunay 367 ms; numba CPU 8.7–10 s). OPEN for phase 3, raised by the human: numba CPU runs one process per core under Nautilus multiprocessing, so designations must compare node throughput, not single-call latency. Follow-up being planned.

Private RAL checkouts kept for 2b–2g: /mnt/ral/jnightin/profiling/PyAuto_2026.10.23.1 (libraries) and /mnt/ral/jnightin/profiling/autolens_profiling_p2a.

## Original prompt

# Likelihood lifecycle phase 2a: profiling campaign — imaging/{mge, rectangular, delaunay, delaunay_nn} (106 planned cells)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the coverage matrix shows zero missing and zero stale cells for class ∈ {optimal, secondary} × measurement ∈ {runtime, breakdown} for this campaign's likelihoods; every new current cell carries fit.png, provenance and parity.json; `build_catalogue --check --validate-with ../PyAutoPulse` valid at @3; the campaign wiki page records the pre-registered rule and verdict
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24
Issued: 2026-10-24
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456

Phase 2 sub-issue 2a of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: imaging/{mge, rectangular, delaunay, delaunay_nn} (106 planned cells).

Size: the 2026-10-17 imaging results are at Delaunay 1500 / rectangular 39², not the standard size, so every cell is re-measured at 1250 / 35². That reuse is no longer possible, and the ledger card's "reuse" line is superseded by the size ruling. **First, add the missing `parity.json` writer** (#451 defined only the format): each cell computes its log-likelihood against a named reference and writes `parity.json` beside the row. Adopts Pulse `hst_mge_cpu_pilot`.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).

## Plan approved 2026-10-24 (human), with rulings
- **Pinned tag: 2026.10.23.1** (the latest PyPI release), shared by every phase-2 sub-issue. Rows on other likelihoods go stale and are re-measured in 2b–2g.
- **Standard Delaunay = 1250 Hilbert + 30 edge (1280 recorded).** Rows record `source_pixels_requested: 1250` beside the actual count, and the size rule matches on the requested count. Rectangular = 35².
- **PR A (code, laptop):**
  - `--source-pixels` in the 3 JAX runtime scripts (hard-coded 1500 / 39² today) and the numba scripts (presets; jwst/ao have none); a `--standard-size` flag.
  - A `parity.json` writer: an in-process eager NumPy reference on the same inputs and size, absolute tolerance 1e-4·|ref| (1e-3 mixed).
  - New submits: a RAL CPU array on `--partition=ral` for the 44 CPU cells, plus one `--gres=gpu:1` A100 job per instrument. The 18 `jax_cpu_sparse`@`hpc_a100` cells run inside those GPU jobs. Each submit gets a WALL-BASIS block.
- **Batch 0 (human go):** one short timing arm per new submit kind, to set `--time` from measurement.
- **Batch 1 (human go):** all 106 cells from a private RAL checkout at the pinned tag.
- **PR B:** commit the rows, regenerate the catalogue and coverage, write the campaign wiki page (pre-registered rule: every cell current with parity `match`; any divergence blocks that setup), refetch Pulse, and adopt and close Pulse `hst_mge_cpu_pilot`.
- Tier: judge, merge by human `/prm`. Starts after autolens_profiling#455 merges.

## Rulings during PR A review (human, 2026-10-24)
- **N1, align JAX to production:** under `--standard-size`, every pixelized JAX cell (rectangular, delaunay, delaunay_nn) uses the same production model as the numba cells of that likelihood × instrument: mesh (Delaunay 1250 + 30 edge; rectangular 35²), MGE, adapt weights, regularisation, and the HST preset borrowed for jwst/ao. Optimal and secondary then measure the same likelihood.
- **(c), parity reference:** JAX sparse cells use the independent eager NumPy dense-mapping reference, the same as the numba cells.
- **Fixes:** the delaunay_nn numba witness is not_applicable; batch 1 writes to a scratch tree and PR B copies complete rows; RAL `--mem` is sized per instrument.
- **Re-review ruling (human, 2026-10-24): match real production.** Under `--standard-size`, both setups measure the actual production pipeline (subhalo_validation): rectangular uses `RectangularBilinearAdaptImage`, and the over-sampling cut thresholds the uncapped S/N map, as production does. The legacy numba preset deviated on both points; runs without the flag and their pins are unchanged, and a follow-up will fix the legacy preset. B1 fixed: the MGE breakdown ignored `--instrument`. The PR B wiki notes that euclid's positions penalty is untimed in JAX breakdowns.
