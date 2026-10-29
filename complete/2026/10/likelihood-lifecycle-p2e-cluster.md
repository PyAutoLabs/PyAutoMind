# Likelihood lifecycle phase 2e: cluster — campaign setup shipped (RAL not run)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/474 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/478 DRAFT (2bf2f53a) — D1–D6 await human
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/478 MERGED 2026-10-29 741ca9a8 (human /prm)
- planner-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/481 MERGED 2026-10-29 (settles D4)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2e_cluster_runs.md
- merged: 2026-10-29

## Shipped — scope: campaign setup only

Recorded as **campaign setup shipped**. No RAL batch ran; the batch-0 go, RAL batches and PR B are re-filed as the remainder draft.

- Runtime cells `scripts/cluster/{image_plane,source_plane}/likelihood_runtime.py` on the shared driver `scripts/misc/likelihood_breakdown/cluster_standard.py` (eager NumPy reference, JIT timings, steady median, vmap, parity.json, fit.png); breakdowns decompose the solved headline with the plain class as a sub-row.
- `scripts/misc/campaigns/cluster_p2e.py` + tests + 4 submits (`submit_campaign_p2e_*`, batch 1 guarded while `WALL_BASIS_STATUS=provisional`).
- Registry plans `cluster/source_plane` (D2, draft). Coverage plans 10 cluster cells (image_plane 4, source_plane 6), all submitted: 4 RAL CPU, 6 A100.
- Wiki: `wiki/campaigns/cluster/{image_plane,source_plane}/likelihood_lifecycle_p2e.md`.
- Laptop smokes (solved headline) all wrote rows with parity `match`.
- **D3 decided (human 2026-10-29):** "the cluster default setup should use solved as I think it does on the workspace" — solved headline (`FitPositionsImagePairRepeatSolved` / `FitPositionsSourceSolved`).
- **D4 settled** by #481 (human "fix the planner gap").

Open at close-out: D1, D2, D5, D6 (in the remainder draft). The `results/breakdown/cluster/` legacy rows become superseded once new rows land.

## Original prompt

# Likelihood lifecycle phase 2e: profiling campaign — cluster/image_plane and cluster/source_plane (4+ planned cells, `regime: standard`)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
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
Issued: 2026-10-28

Phase 2 sub-issue 2e of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: cluster/image_plane and cluster/source_plane (4+ planned cells, `regime: standard`).

**Re-measure cluster/source_plane:** the committed rows predate PyAutoLens bdb44a87c (2026-10-21, `FitPositionsSource` now uses the Jacobian precision tensor and a model-independent noise term); the breakdown script was re-derived in autolens_profiling#455.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
