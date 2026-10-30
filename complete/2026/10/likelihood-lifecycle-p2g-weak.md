# Likelihood lifecycle phase 2g: weak lensing — campaign setup shipped (RAL not run)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/476 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/477 DRAFT (7f7e7e8f) — D1–D10 await human
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/477 MERGED 2026-10-29 864202d7 (human /prm)
- planner-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/481 MERGED 2026-10-29 (settles D5)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2g_weak_runs.md (closed 2026-10-30: complete/2026/10/likelihood-lifecycle-p2g-weak-runs.md)
- merged: 2026-10-29

## Shipped — scope: campaign setup only

Recorded as **campaign setup shipped**. No RAL batch ran; the batch-0 go, RAL batches and PR B are re-filed as the remainder draft.

- `scripts/misc/simulators/weak.py` (the workspace/visualization `simple` catalogue, reproduced exactly), `scripts/misc/likelihood_breakdown/weak_standard.py`, and `scripts/weak/isothermal/likelihood_{runtime,breakdown}.py` (rows with provenance and resources, parity.json, fit.png).
- Registry cell `weak/isothermal/simple` and the `weak` family; `weak_p2g.py` + tests + `submit_campaign_p2g_*` (batch 0 runnable with provisional walls; batch 1 guarded).
- Wiki: `wiki/campaigns/weak/likelihood_lifecycle_p2g.md` (rule, expected verdict, D1–D10).
- Laptop: runtime 48 s, breakdown 38 s, parity `match` (|Δ| 2.3e-10 at |log L| 84.87); JIT steady median 1.04 ms, vmap 0.47 ms per point.
- **D5 settled** by #481 (human "fix the planner gap"): GPU setups are planned only on `hpc_a100`, so the 2 unrunnable `jax_gpu_dense_fp64@hpc_ral_cpu` cells are no longer planned.

Open at close-out: D1–D4, D6–D10 (in the remainder draft). The `e- s^-1` chi-squared colour-bar label is a library plotting quirk to raise with Eyes.

## Original prompt

# Likelihood lifecycle phase 2g: profiling campaign — weak lensing: **new** profiling scripts and planned cells

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

Phase 2 sub-issue 2g of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: weak lensing: **new** profiling scripts and planned cells.

The only dataset type with no image-plane fit; design the runtime and breakdown cells first (judgment fork → human).

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
