# Likelihood lifecycle phase 2f: multi_dataset + datacube — campaign setup shipped (RAL not run)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/475 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/479 MERGED 2026-10-29 a36f4818 (human /prm)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2f_dataset_datacube_runs.md
- merged: 2026-10-29

## Shipped — scope: campaign setup only

Recorded as **campaign setup shipped**. No RAL batch ran; the batch-0 go, RAL batches and PR B are re-filed as the remainder draft.

- `scripts/misc/likelihood_breakdown/datacube_standard.py` (2b's interferometer standard cell in 34 channels, `FactorGraphModel` of `AnalysisInterferometer(shared_preloads=True)`; JAX W~/dense runtime, numba runtime, lead-channel breakdown projected to the cube, cube parity reference derived from 2b's chunked dense reference, finalise pass).
- `scripts/misc/likelihood_breakdown/multi_dataset_standard.py` (2a's hst Delaunay cell in 2 datasets; JAX/numba runtime, breakdown, parity = sum of 2a's dense reference per dataset).
- Datacube cell scripts gain `--standard-size`; new datacube numba runtime/breakdown and `parity_reference.py`; new multi_dataset runtime/breakdown (JAX + numba). Routes registered.
- `multi_dataset_datacube_p2f.py` + tests + `submit_campaign_p2f_*` (batch 0 runnable with declared guesses; batch 1 refuses while provisional). `_common.py` unchanged.
- D1 (draft) applied as its own commit in `catalogue/provisional_designations.json`: dense datacube NUFFT at sma only, 40 → 32 planned cells (RAL 18, A100 14).
- Wiki: `wiki/campaigns/{datacube,multi_dataset}/likelihood_lifecycle_p2f.md`.
- Laptop smokes (datacube sma at 4 channels; multi_dataset hst numba) wrote rows with parity `match`; the datacube JAX dense breakdown did not complete on the laptop (swap).

Open at close-out: D1–D9 (in the remainder draft).

## Original prompt

# Likelihood lifecycle phase 2f: profiling campaign — multi_dataset and datacube/delaunay (40 planned cells)

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

Phase 2 sub-issue 2f of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: multi_dataset and datacube/delaunay (40 planned cells).



## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
