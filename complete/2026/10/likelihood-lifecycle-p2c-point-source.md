# Likelihood lifecycle phase 2c: point-source campaign (complete)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/472 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/480 DRAFT (PR B, 2bca9d15; base p2b branch) — 15/15 legs, 10/10 cells current, parity all match; runtime cell plain vs solved + GPU-on-ral planner gap await human
- pr-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/480 MERGED 2026-10-29 8620ec48 (human /prm)
- planner-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/481 MERGED 2026-10-29 c932b669 (merged into #480)
- rerun: quiet-node rerun of the 2 solved RAL CPU runtime legs (human 2026-10-29 "do the reruns now") RAL 413267 [0-1%2] --exclusive, chained before the 2b rerun; branch feature/likelihood-lifecycle-p2c-quiet-rerun eb8b3237 (no PR yet); RAL profiling/autolens_profiling_p2c_rerun → output/p2c_quiet/; log scratch/p2_quiet_rerun_submit.log; ingest after
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2bc_quiet_rerun_ingest.md (quiet-rerun ingest, shared with 2b)
- merged: 2026-10-29

## Shipped

Phase 2c profiled `point_source_image/image_plane` and `point_source_source/source_plane` (instrument `simple`) on pin 2026.10.25.1.

- **#480** carries the campaign commits (manifest `point_source_p2c.py`, submits, harness gaps) and PR B rows. RAL 413192 (ral CPU, 6 legs) + 413193 (A100, 9 legs): 15/15 legs exit 0, `revisions OK` on every one. Point source 10/10 current; parity 53 → 58 `match` of 110 planned setup cells, 0 `diverged`. Coverage (220-cell plan) after: 116 current / 1 stale / 103 missing.

## Human rulings 2026-10-29

- **"Switch 2c to Solved":** the published runtime cell is the Solved likelihood (`FitPositionsImagePairAllSolved` / `FitPositionsSourceSolved` with `PointSolved`). Plain rows moved to `experiments/plain_runtime/` (unpublished comparison); the work list and submits now run `likelihood_runtime_solved.py` as the runtime cell. No number changed.
- **Dashboard refusal guard, option A:** host-change refusals are allowed when there is no carried endpoint (a fresh host-change refusal is not a carry regression); landed on main with tests.
- **"Fix the planner gap":** #481 merged in; the two `source_plane jax_gpu_na_fp64@hpc_ral_cpu` cells are no longer planned.

Per-call (single-jit median, ms, published = solved): image plane A100 `jax_gpu_na_fp64` 0.847, RAL `jax_cpu` 1.556; source plane RAL `jax_cpu` 0.156, A100 `jax_gpu` 0.262 / `jax_cpu` 0.265. Verdict: the pre-registered rule is met. Flagged for phase 3: the source-plane A100 GPU number rose 0.233 → 0.262 ms (+12 %), and jax_gpu vs jax_cpu on hpc_a100 is not separated by the evidence.

In flight at close-out: the quiet-node rerun of the 2 solved RAL CPU runtime legs (see `rerun:` above); ingest is the remainder draft.

## Original prompt

# Likelihood lifecycle phase 2c: profiling campaign — point_source_image/image_plane and point_source_source/source_plane (12 planned cells)

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

Phase 2 sub-issue 2c of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: point_source_image/image_plane and point_source_source/source_plane (12 planned cells).

Point-source runtime scripts honour `--output-path` since autolens_profiling#455.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
