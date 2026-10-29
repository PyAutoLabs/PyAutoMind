# Likelihood lifecycle phase 2d: multi_galaxy + group — campaign setup shipped (RAL not run)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/473 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/484 DRAFT (caa46fad) — D1–D12 await human; D12 = XLA:CPU deadlock workaround (jaxlib 0.11.2); #481 merged in, 2d stays 48
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/484 MERGED 2026-10-29 d0481695 (human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/81 MERGED 2026-10-29 6f847287 (XLA:CPU deadlock knowledge page + eigen-workaround decision record + board lists every knowledge page)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2d_galaxy_group_runs.md
- merged: 2026-10-29

## Shipped — scope: campaign setup only

Recorded as **campaign setup shipped**. The human held 2d for review before any RAL run, so no batch ran and no measured row landed; the batch-0 go, RAL batches and PR B are re-filed as the remainder draft.

- `scripts/misc/cell_builders/galaxy_group.py` (datasets from the workspace simulators, workspace MGE model with narrow truth priors, hst production pixelization at the standard size, seeded iid stream) and the shared driver `scripts/misc/likelihood_breakdown/galaxy_group_standard.py` (JAX runtime/breakdown via seven jitted `fit_from` prefixes, numba runtime and eager stage-walk breakdown, parity.json + fit.png).
- 20 cell scripts under `scripts/{multi_galaxy,group}/{mge,rectangular,delaunay}/`; 48 planned cells (20 `hpc_ral_cpu`, 28 `hpc_a100`); `multi_galaxy_group_p2d.py` + tests + `submit_campaign_p2d_*` (batch 0 = every group leg; batch 1 refuses to run while `WALL_BASIS_STATUS=provisional`).
- Wiki: `wiki/campaigns/multi_galaxy/likelihood_lifecycle_p2d.md` (D1–D12) and `wiki/campaigns/group/likelihood_lifecycle_p2d.md`.
- Laptop smoke: all 28 scripts rc 0 with parity `match` (local mains, not the pin).
- **D12 decided (human 2026-10-29):** "keep the workaround which ensures we retain the fastest run times and make sure this knowledge is retained in Pulse for going forward" — every JAX leg appends `--xla_cpu_multi_thread_eigen=false` (jaxlib 0.11.2 XLA:CPU deadlock in `CpuPjRtRawLoadedExecutable::Execute`; minimal repro with no PyAuto code). Knowledge + decision kept in PyAutoPulse#81.

Open at close-out: D1–D11 (in the remainder draft); a JAX upstream issue for the deadlock; the multi_galaxy simulator's `mask_extra_galaxies` inversion (workspace bug, campaign page).

## Original prompt

# Likelihood lifecycle phase 2d: profiling campaign — multi_galaxy and group: **new** profiling scripts (runtime and breakdown) and their planned cells (`regime: standard` only)

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
Issued: 2026-10-28

Phase 2 sub-issue 2d of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: multi_galaxy and group: **new** profiling scripts (runtime and breakdown) and their planned cells (`regime: standard` only).

Scripts mirror the autolens_visualization producers and the workspace simulators; add the planned cells to `catalogue/registry.json`, and the §3.3 rows if missing (judgment fork → human).

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
