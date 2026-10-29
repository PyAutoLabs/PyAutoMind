# Likelihood lifecycle phase 2d: multi_galaxy + group — decisions, RAL batches and PR B

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
Filed: 2026-10-29

- batch0: NOT SUBMITTED (2026-10-29). Decisions adopted: human "ok can we do all that now then" adopted every drafted option (2d D1-D11; D12 already decided); recorded docs-only in autolens_profiling#485 (open, human /prm). The batch-0 go was given but HELD: the RAL venv /mnt/ral/jnightin/PyAuto/PyAuto (activated by every submit, CPU and A100) carries jax/jaxlib 0.10.2, which the pin 2026.10.25.1's PyAutoNerves excludes (Heart#274), so rows would not match the pin's dependency floor (human's call). The human then said not to start anything new on RAL that evening. Prepared but unused: detached checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main 32c0becd (log /mnt/ral/jnightin/scratch/p2dg_checkout.log); guarded submit script draft (not on RAL) in the session scratchpad.
- Status: split out of `likelihood-lifecycle-p2d-galaxy-group` at close-out 2026-10-29 — the campaign setup shipped (autolens_profiling#484, PyAutoPulse#81), recorded in `complete/2026/10/likelihood-lifecycle-p2d-galaxy-group.md`; this is what remains. No RAL batch has run.
- Shipped setup: `cell_builders/galaxy_group.py`, `likelihood_breakdown/galaxy_group_standard.py`, 20 cell scripts under `scripts/{multi_galaxy,group}/{mge,rectangular,delaunay}/`, 48 planned cells (20 `hpc_ral_cpu`, 28 `hpc_a100`), `scripts/misc/campaigns/multi_galaxy_group_p2d.py` + `submit_campaign_p2d_*`, pages `wiki/campaigns/{multi_galaxy,group}/likelihood_lifecycle_p2d.md`.

## What remains

1. The human reviews the open decisions below (campaign page has the full table with reasons and alternatives) and rules on each.
2. **Batch-0 go** from the human (none given: "leave this as something I then review before we do RAL runs"). Then run batch 0 from a private RAL checkout at pin 2026.10.25.1 (or whatever pin the human sets).
3. Walls commit: fill `BATCH0_WALLS` / `BATCH0_PEAK_RSS_KIB`, set `WALL_BASIS_STATUS="measured"`, re-render the submits (multi_galaxy_group_p2d.py `--write`).
4. **Batch-1 go**, then batch 1.
5. PR B: copy the complete cells into `results/`, regenerate catalogue / coverage / dashboard, record the verdict on the campaign page(s), refetch the Pulse receipt.

## Open decisions (drafted in #484; human rules)

| | Decision (draft) |
|---|---|
| D1 | Variants `mge`, `rectangular`, `delaunay` for both types (no `delaunay_nn`, no `sersic`). |
| D2 | One instrument per type: multi_galaxy at `hst`, group at `euclid`, instrument-preset PSF. |
| D3 | Datasets mirror the workspace simulators; masks 3.0" and 7.5"; the multi_galaxy extra galaxy is noise-scaled inside 0.9". |
| D4 | Model: the workspace modeling MGE model; group extra galaxies `dPIEMassSph` (sigma free); narrow Gaussian priors on the truth. |
| D5 | Pixelized source: the hst production preset at the standard size, as imaging; no positions penalty. |
| D6 | Setups and hosts: §3.3 "as imaging", verbatim. |
| D7 | Instance is iid draw 0; parity vs the eager NumPy dense reference at 1e-4 × \|ref\|. |
| D8 | A100 vmap batch 16 pixelized / 64 MGE, halving on OOM; CPU capped at 3. |
| D9 | Batch 0 = every group leg (24); batch 1 = all 48 cells with walls from batch 0. |
| D10 | Breakdowns use a generic stage walk of `AnalysisImaging.fit_from` (JAX prefixes / numba lazy stages). |
| D11 | Walls and memory provisional: batch 0 4:00:00 and 32 GB per task; batch 1 refuses until measured. |

**Decided — D12 (human 2026-10-29):** keep `--xla_cpu_multi_thread_eigen=false` for every JAX cell (jaxlib 0.11.2 XLA:CPU deadlock). Rows record it in `device.xla_flags` / `configuration.xla_cpu_workaround`; they are not like-for-like with the 2a/2b JAX CPU rows. Knowledge: PyAutoPulse `knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md` and `decisions/xla-cpu-deadlock-eigen-workaround.md` (PyAutoPulse#81). Whether the deadlock fires on a 236-core RAL node is untested.

## Also open
- A JAX upstream issue for the deadlock (the exported module reproduces it).
- Workspace bug: the multi_galaxy simulator's `mask_extra_galaxies` inversion (campaign page).
- Not run locally: any GPU leg, any run on the pin, non-`--fast` repeat counts.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
