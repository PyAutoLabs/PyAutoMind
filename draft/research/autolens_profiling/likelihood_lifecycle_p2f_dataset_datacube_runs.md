# Likelihood lifecycle phase 2f: multi_dataset + datacube — decisions, RAL batches and PR B

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

- batch1: SUBMITTED 2026-10-30 ~10:50 UTC (human go: "fix the 2d driver then submit batch 1") from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg detached at 830314e9 (#487 head; #487 MERGED 6203903c). Batch 0 DONE: all legs exit 0, every witness match; walls commit autolens_profiling#487 merged 2026-10-30 (WALL_BASIS_STATUS=measured). Human 2026-10-30: loaded RAL nodes accepted (batch-0 RAL rows loadavg 95-109; no quiet gate). 2d driver now keeps the eigen flag off GPU legs (#487). This campaign: RAL 413448 (multi_dataset hst), 413449/413450/413451 (datacube alma/alma_high/sma), references 413452; A100 413456 (multi_dataset), 413457/413458/413459 (datacube alma/alma_high/sma). NEXT: verify batch 1 (sacct, walls.tsv, parity), then PR B.
- batch1 check 2026-10-30 11:45 UTC: A100 413456-413459 COMPLETED exit 0: 14 legs, 5 witnesses match, 2 not_assessed (datacube alma, awaiting the RAL reference 413452); every row final at the pin, profiling_revision 830314e9. RAL arrays 413445-413452 PENDING (Priority; ral full, estimated start 2026-10-30 23:19). Human 2026-10-30: wait for RAL, then one complete PR B per campaign (no partial A100-only PR).
- batch0: SUBMITTED 2026-10-29 20:27 GMT from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main ad103340 (#486 XLA:CPU workaround merged fe81b1f4, #485 decisions merged ad103340), pin 2026.10.25.1, guarded detached script /mnt/ral/jnightin/scratch/p2dg_batch0_submit.sh (log p2dg_batch0_submit.log, marker P2DGBATCH0SUBMITDONE; guards: venv jax/jaxlib 0.11.2, HEAD == SHA, clean tree, pin tags, flag in all 9 submits, no output/*_batch0). ENV CHANGE: the shared RAL venv /mnt/ral/jnightin/PyAuto/PyAuto was upgraded jax/jaxlib/jax-cuda12-plugin/jax-cuda12-pjrt 0.10.2 -> 0.11.2 (human 2026-10-29, 'Upgrade the shared venv'; log scratch/jax0112_upgrade.log, freezes scratch/pyauto_venv_freeze_{before,after}_jax0112_20261029.txt; only the 4 jax packages changed; pip check: only anesthetic numpy<2 and ipython psutil>=7, unrelated to jax). FLAG: every JAX_PLATFORMS=cpu leg runs with --xla_cpu_multi_thread_eigen=false appended to XLA_FLAGS (shared preamble, #486; human option 'All JAX CPU legs'), GPU legs never; rows record it in device.xla_flags. The A100 legs are the first GPU test of jax 0.11.2 on RAL. Rows: output/p2f_batch0/. All 9 submits: RAL CPU p2d 413272, p2e 413273, p2f 413274, p2f references 413292, p2g 413293; A100 p2d 413294, p2e 413295, p2f 413296, p2g 413297. This campaign: 413274 [0-9%8] 12:00:00 RAL CPU + 413292 [0%8] 12:00:00 references + 413296 [0-9%2] 6:00:00 A100. At 20:40 the early tasks had completed exit 0 with no FAILED/Traceback/REFUSING in the .out files; NEXT: sacct all, walls.tsv, parity, walls commit, batch 1 (human go).
- batch0 earlier hold (2026-10-29, superseded by the line above): Decisions adopted: human "ok can we do all that now then" adopted every drafted option (2f D1-D9 incl. 34 channels; batch 0 to include the optional alma_high reference); recorded docs-only in autolens_profiling#485 (open, human /prm). The batch-0 go was given but HELD: the RAL venv /mnt/ral/jnightin/PyAuto/PyAuto (activated by every submit, CPU and A100) carries jax/jaxlib 0.10.2, which the pin 2026.10.25.1's PyAutoNerves excludes (Heart#274), so rows would not match the pin's dependency floor (human's call). The human then said not to start anything new on RAL that evening. Prepared but unused: detached checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main 32c0becd (log /mnt/ral/jnightin/scratch/p2dg_checkout.log); guarded submit script draft (not on RAL) in the session scratchpad.
- Status: split out of `likelihood-lifecycle-p2f-dataset-datacube` at close-out 2026-10-29 — the campaign setup shipped (autolens_profiling#479), recorded in `complete/2026/10/likelihood-lifecycle-p2f-dataset-datacube.md`; this is what remains. No RAL batch has run.
- Shipped setup: `likelihood_breakdown/datacube_standard.py`, `likelihood_breakdown/multi_dataset_standard.py`, datacube `--standard-size` + numba runtime/breakdown + `parity_reference.py`, new multi_dataset runtime/breakdown scripts, `scripts/misc/campaigns/multi_dataset_datacube_p2f.py` + `submit_campaign_p2f_*`; 32 planned cells (RAL 18, A100 14); pages `wiki/campaigns/{datacube,multi_dataset}/likelihood_lifecycle_p2f.md`.

## What remains

1. The human reviews the open decisions below (campaign page has the full table with reasons and alternatives) and rules on each.
2. **Batch-0 go** from the human (none given: "leave this as something I then review before we do RAL runs"). Then run batch 0 from a private RAL checkout at pin 2026.10.25.1 (or whatever pin the human sets).
3. Walls commit: fill `BATCH0_WALLS` / `BATCH0_PEAK_RSS_KIB`, set `WALL_BASIS_STATUS="measured"`, re-render the submits (multi_dataset_datacube_p2f.py `--write`).
4. **Batch-1 go**, then batch 1.
5. PR B: copy the complete cells into `results/`, regenerate catalogue / coverage / dashboard, record the verdict on the campaign page(s), refetch the Pulse receipt.

## Open decisions (drafted in #479; human rules)

| | Decision (draft) |
|---|---|
| D1 | Dense datacube NUFFT (`jax_{cpu,gpu}_dense_fp64_nufft`) planned at sma only (2b's R1(a)): 40 → 32 cells. Applied as its own commit in `catalogue/provisional_designations.json` (revert = that commit + regen). |
| D2 | Cube = 34 channels of 2b's delaunay standard cell; shared uv / noise / mask / adapt image / lens; channel visibilities × a_c (Gaussian line, a_0 = 1, a_33 = 0.15); `shared_preloads=True`. |
| D3 | Datacube parity: cube reference derived from 2b's chunked dense reference terms; in-process at sma, 2b's `output/p2b_references/` cache above sma, else `parity_reference.py`. Tolerance 1e-8 × \|ref\|. |
| D4 | Datacube breakdown = 2b breakdown of the lead channel; shared steps once + the rest ×34 → `total_step_by_step_cube`. |
| D5 | Datacube numba runtime: packaged cost-model route only (forced arms off by default). |
| D6 | multi_dataset = 2a's hst cell in 2 datasets, data and noise ×1 and ×0.5 (same S/N), `shared_preloads=False`. |
| D7 | multi_dataset breakdown = 2a imaging breakdown of dataset 0, total ×2. |
| D8 | multi_dataset parity = sum of 2a's eager NumPy dense reference per dataset, tol 1e-4 × \|ref\|. |
| D9 | Batch 0 = alma_high for datacube W~/numba, sma for dense, all 10 multi_dataset legs (hst only). |

## Also
- Batch 0: 21 tasks (RAL 10 at 12:00:00 / 128 GB est., A100 10 at 6:00:00 / 64 GB est., optional alma_high reference). Batch 1: 34 tasks (32 cell legs + 2 references).
- Not run locally: the datacube JAX dense breakdown (laptop swap), any alma/alma_high leg, any GPU leg, 34-channel cubes.
- The alma/alma_high datacube witnesses reuse 2b's delaunay references if they are in the submitting checkout's `output/p2b_references/`; otherwise the 2f reference tasks compute them.
- Check whether 2d's jaxlib 0.11.2 XLA:CPU deadlock (D12 there) affects these JAX CPU cells before batch 0.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
