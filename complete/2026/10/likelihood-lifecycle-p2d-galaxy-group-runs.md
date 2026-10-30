# Likelihood lifecycle phase 2d: multi_galaxy + group — batch 0 + batch 1 run, 48 rows committed (campaign complete)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/473 (closed 2026-10-29 at setup)
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/487 MERGED 2026-10-30 6203903c (human /prm) — walls from batch 0, 2d driver GPU-flag fix
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/489 MERGED 2026-10-30 e6942fe3 (human /prm) — PR B
- merged: 2026-10-30

## Shipped

Batch 0 (RAL 413272, A100 413294, 2026-10-29; 24 group legs, all exit 0, 12/12 witnesses match) set
batch 1's walls (#487). Batch 1 (RAL 413445/413446, A100 413453/413454, 2026-10-30, from the RAL
checkout autolens_profiling_p2dg at 830314e9) all exit 0; PR B #489 copied the 48 rows into
`results/{multi_galaxy,group}/`: 24/24 witnesses match, coverage 182 -> 230 of 272, 0 stale.

Verdict: rule met. `jax_gpu_dense_fp64@hpc_a100` fastest per call (MGE ~7 ms; pixelized 38-56 ms);
`numba_cpu_sparse_fp64` the RAL CPU pixelized route (0.80-1.10 s vs JAX CPU 3.7-6.0 s). The
expectation "group slower than multi_galaxy for every setup" fails for the numba pixelized cells.
Fit figure note: multi_galaxy MGE shows a ~14 sigma ring residual at iid draw 0 (parametric source).

Human decisions this session (2026-10-30): loaded RAL nodes accepted (no quiet gate); the 2d driver
keeps the eigen flag off GPU legs (#487); wait for RAL and ship one complete PR B per campaign.

## Original prompt

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

- batch1: SUBMITTED 2026-10-30 ~10:50 UTC (human go: "fix the 2d driver then submit batch 1") from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg detached at 830314e9 (#487 head; #487 MERGED 6203903c). Batch 0 DONE: all legs exit 0, every witness match; walls commit autolens_profiling#487 merged 2026-10-30 (WALL_BASIS_STATUS=measured). Human 2026-10-30: loaded RAL nodes accepted (batch-0 RAL rows loadavg 95-109; no quiet gate). 2d driver now keeps the eigen flag off GPU legs (#487). This campaign: RAL 413445 (multi_galaxy) + 413446 (group) [0-9%16] 0:30:00 16 GB; A100 413453 (multi_galaxy) + 413454 (group), one job each 1:00:00 16 GB. NEXT: verify batch 1 (sacct, walls.tsv, parity), then PR B.
- batch1 check 2026-10-30 11:45 UTC: A100 413453/413454 COMPLETED exit 0 (22:46, 26:28): 28 legs, 20 GPU rows flag-free, 8 node-CPU rows flagged, 14/14 witnesses match; every row final at the pin, profiling_revision 830314e9. RAL arrays 413445-413452 PENDING (Priority; ral full, estimated start 2026-10-30 23:19). Human 2026-10-30: wait for RAL, then one complete PR B per campaign (no partial A100-only PR).
- pr-b 2026-10-30: batch 1 complete (every RAL and A100 leg exit 0); PR B autolens_profiling#489 (48 rows, 24/24 match; coverage 182 -> 230). Merge order #489, #490, #491 (human /prm); then close this draft.
- batch0: SUBMITTED 2026-10-29 20:27 GMT from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main ad103340 (#486 XLA:CPU workaround merged fe81b1f4, #485 decisions merged ad103340), pin 2026.10.25.1, guarded detached script /mnt/ral/jnightin/scratch/p2dg_batch0_submit.sh (log p2dg_batch0_submit.log, marker P2DGBATCH0SUBMITDONE; guards: venv jax/jaxlib 0.11.2, HEAD == SHA, clean tree, pin tags, flag in all 9 submits, no output/*_batch0). ENV CHANGE: the shared RAL venv /mnt/ral/jnightin/PyAuto/PyAuto was upgraded jax/jaxlib/jax-cuda12-plugin/jax-cuda12-pjrt 0.10.2 -> 0.11.2 (human 2026-10-29, 'Upgrade the shared venv'; log scratch/jax0112_upgrade.log, freezes scratch/pyauto_venv_freeze_{before,after}_jax0112_20261029.txt; only the 4 jax packages changed; pip check: only anesthetic numpy<2 and ipython psutil>=7, unrelated to jax). FLAG: every JAX_PLATFORMS=cpu leg runs with --xla_cpu_multi_thread_eigen=false appended to XLA_FLAGS (shared preamble, #486; human option 'All JAX CPU legs'), GPU legs never; rows record it in device.xla_flags. The A100 legs are the first GPU test of jax 0.11.2 on RAL. Rows: output/p2d_batch0/. All 9 submits: RAL CPU p2d 413272, p2e 413273, p2f 413274, p2f references 413292, p2g 413293; A100 p2d 413294, p2e 413295, p2f 413296, p2g 413297. This campaign: 413272 [0-9%8] 4:00:00 RAL CPU + 413294 [0-13%2] 4:00:00 A100. At 20:40 the early tasks had completed exit 0 with no FAILED/Traceback/REFUSING in the .out files; NEXT: sacct all, walls.tsv, parity, walls commit, batch 1 (human go).
- batch0 earlier hold (2026-10-29, superseded by the line above): Decisions adopted: human "ok can we do all that now then" adopted every drafted option (2d D1-D11; D12 already decided); recorded docs-only in autolens_profiling#485 (open, human /prm). The batch-0 go was given but HELD: the RAL venv /mnt/ral/jnightin/PyAuto/PyAuto (activated by every submit, CPU and A100) carries jax/jaxlib 0.10.2, which the pin 2026.10.25.1's PyAutoNerves excludes (Heart#274), so rows would not match the pin's dependency floor (human's call). The human then said not to start anything new on RAL that evening. Prepared but unused: detached checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main 32c0becd (log /mnt/ral/jnightin/scratch/p2dg_checkout.log); guarded submit script draft (not on RAL) in the session scratchpad.
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
