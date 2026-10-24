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
