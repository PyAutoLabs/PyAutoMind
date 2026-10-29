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
