# Likelihood lifecycle phase 2e: cluster — batch 0 + batch 1 run, 10 rows committed (campaign complete)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/474 (closed 2026-10-29 at setup)
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/487 MERGED 2026-10-30 6203903c (human /prm) — walls from batch 0, 2d driver GPU-flag fix
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/490 MERGED 2026-10-30 a91fad39 (human /prm) — PR B
- merged: 2026-10-30

## Shipped

Batch 0 (RAL 413273, A100 413295; 4 image-plane legs, exit 0, 2/2 match) set the walls (#487).
Batch 1 (RAL 413447, A100 job 413455, 2026-10-30) all exit 0; PR B #490 copied the 10 rows (4 image
plane, 6 source plane) into `results/cluster/`: 5/5 witnesses match, coverage 230 -> 240.

Verdict: rule met on both pages. Image plane: A100 2.32 ms vs RAL CPU 5.71 ms per call, solved and
plain headlines the same order, ~105 s lower+compile per pipeline. Source plane: 0.51-0.82 ms, one
order below the image plane (not two); the A100 node's CPU beats its GPU per single call.

## Original prompt

# Likelihood lifecycle phase 2e: cluster — decisions, RAL batches and PR B

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

- batch1: SUBMITTED 2026-10-30 ~10:50 UTC (human go: "fix the 2d driver then submit batch 1") from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg detached at 830314e9 (#487 head; #487 MERGED 6203903c). Batch 0 DONE: all legs exit 0, every witness match; walls commit autolens_profiling#487 merged 2026-10-30 (WALL_BASIS_STATUS=measured). Human 2026-10-30: loaded RAL nodes accepted (batch-0 RAL rows loadavg 95-109; no quiet gate). 2d driver now keeps the eigen flag off GPU legs (#487). This campaign: RAL 413447 [0-3%8] 0:30:00 32 GB; A100 413455 1:00:00 32 GB. NEXT: verify batch 1 (sacct, walls.tsv, parity), then PR B.
- batch1 check 2026-10-30 11:45 UTC: A100 413455 COMPLETED exit 0 (11:33): 6 legs, 3/3 witnesses match; every row final at the pin, profiling_revision 830314e9. RAL arrays 413445-413452 PENDING (Priority; ral full, estimated start 2026-10-30 23:19). Human 2026-10-30: wait for RAL, then one complete PR B per campaign (no partial A100-only PR).
- pr-b 2026-10-30: batch 1 complete (every RAL and A100 leg exit 0); PR B autolens_profiling#490 stacked on #489 (10 rows, 5/5 match; coverage 230 -> 240). Merge order #489, #490, #491 (human /prm); then close this draft.
- batch0: SUBMITTED 2026-10-29 20:27 GMT from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main ad103340 (#486 XLA:CPU workaround merged fe81b1f4, #485 decisions merged ad103340), pin 2026.10.25.1, guarded detached script /mnt/ral/jnightin/scratch/p2dg_batch0_submit.sh (log p2dg_batch0_submit.log, marker P2DGBATCH0SUBMITDONE; guards: venv jax/jaxlib 0.11.2, HEAD == SHA, clean tree, pin tags, flag in all 9 submits, no output/*_batch0). ENV CHANGE: the shared RAL venv /mnt/ral/jnightin/PyAuto/PyAuto was upgraded jax/jaxlib/jax-cuda12-plugin/jax-cuda12-pjrt 0.10.2 -> 0.11.2 (human 2026-10-29, 'Upgrade the shared venv'; log scratch/jax0112_upgrade.log, freezes scratch/pyauto_venv_freeze_{before,after}_jax0112_20261029.txt; only the 4 jax packages changed; pip check: only anesthetic numpy<2 and ipython psutil>=7, unrelated to jax). FLAG: every JAX_PLATFORMS=cpu leg runs with --xla_cpu_multi_thread_eigen=false appended to XLA_FLAGS (shared preamble, #486; human option 'All JAX CPU legs'), GPU legs never; rows record it in device.xla_flags. The A100 legs are the first GPU test of jax 0.11.2 on RAL. Rows: output/p2e_batch0/. All 9 submits: RAL CPU p2d 413272, p2e 413273, p2f 413274, p2f references 413292, p2g 413293; A100 p2d 413294, p2e 413295, p2f 413296, p2g 413297. This campaign: 413273 [0-1%8] 2:30:00 RAL CPU + 413295 [0-1%2] 2:30:00 A100. At 20:40 the early tasks had completed exit 0 with no FAILED/Traceback/REFUSING in the .out files; NEXT: sacct all, walls.tsv, parity, walls commit, batch 1 (human go).
- batch0 earlier hold (2026-10-29, superseded by the line above): Decisions adopted: human "ok can we do all that now then" adopted every drafted option (2e D1, D2, D5, D6; D3/D4 already decided); recorded docs-only in autolens_profiling#485 (open, human /prm). The batch-0 go was given but HELD: the RAL venv /mnt/ral/jnightin/PyAuto/PyAuto (activated by every submit, CPU and A100) carries jax/jaxlib 0.10.2, which the pin 2026.10.25.1's PyAutoNerves excludes (Heart#274), so rows would not match the pin's dependency floor (human's call). The human then said not to start anything new on RAL that evening. Prepared but unused: detached checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main 32c0becd (log /mnt/ral/jnightin/scratch/p2dg_checkout.log); guarded submit script draft (not on RAL) in the session scratchpad.
- Status: split out of `likelihood-lifecycle-p2e-cluster` at close-out 2026-10-29 — the campaign setup shipped (autolens_profiling#478), recorded in `complete/2026/10/likelihood-lifecycle-p2e-cluster.md`; this is what remains. No RAL batch has run.
- Shipped setup: `scripts/cluster/{image_plane,source_plane}/likelihood_runtime.py` on `likelihood_breakdown/cluster_standard.py`, solved-headline breakdowns, `scripts/misc/campaigns/cluster_p2e.py` + 4 `submit_campaign_p2e_*` submits, `cluster/source_plane` planned; 10 cluster cells (image_plane 4, source_plane 6; 4 RAL CPU, 6 A100); pages `wiki/campaigns/cluster/{image_plane,source_plane}/likelihood_lifecycle_p2e.md`.

## What remains

1. The human reviews the open decisions below (campaign page has the full table with reasons and alternatives) and rules on each.
2. **Batch-0 go** from the human (none given: "leave this as something I then review before we do RAL runs"). Then run batch 0 from a private RAL checkout at pin 2026.10.25.1 (or whatever pin the human sets).
3. Walls commit: fill `BATCH0_WALLS` / `BATCH0_PEAK_RSS_KIB`, set `WALL_BASIS_STATUS="measured"`, re-render the submits (cluster_p2e.py `--write`).
4. **Batch-1 go**, then batch 1.
5. PR B: copy the complete cells into `results/`, regenerate catalogue / coverage / dashboard, record the verdict on the campaign page(s), refetch the Pulse receipt.

## Open decisions (drafted in #478; human rules)

| | Decision (draft) | Alternative |
|---|---|---|
| D1 | Standard image-plane cell uses the workspace cluster PointSolver kept by the `cluster-pointsolver-speed` epic: 100×100 @ 1.0″, precision 0.001, `magnification_threshold` 0.1, `residual_threshold` 10, all passed explicitly. | The historic 200×200 @ 0.7″, precision 0.01 solver |
| D2 | Plan `cluster/source_plane` by analogy with point_source_source (registry cell `cluster/source_plane/unspecified`, 6 coverage cells since #481). | Leave it unplanned; re-measure as unplanned rows only |
| D5 | Batch 0 = the 4 image-plane legs; batch 1 = all 10 legs with walls from batch 0. | Skip batch 0 (`P2E_ALLOW_PROVISIONAL_WALL=1`) |
| D6 | Parity witness from the runtime script only, default 1e-4 tolerance; vmap batch declared (CPU 3, GPU 16) since the vram table has no cluster entry. | Tighter tolerance, or a `--vmap-probe` run first |

**Decided:** D3 (human 2026-10-29) — the headline is the solved class (`FitPositionsImagePairRepeatSolved` / `FitPositionsSourceSolved`); plain is a sub-row. D4 — settled by autolens_profiling#481 (GPU setups planned only on GPU hosts).

## Also
- The legacy `results/breakdown/cluster/` rows become superseded once new rows land. The committed cluster/source_plane rows predate PyAutoLens bdb44a87c and must be re-measured.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
