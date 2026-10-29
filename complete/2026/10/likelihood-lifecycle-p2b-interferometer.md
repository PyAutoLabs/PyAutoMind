# Likelihood lifecycle phase 2b: interferometer standard-size campaign (complete)

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469 (closed 2026-10-29)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/471 MERGED 2026-10-29 5e30a537 on the human's explicit "merge them if possible" (CI green, CLEAN); task stays open for PR B (#483 DRAFT)
- pr-b: https://github.com/PyAutoLabs/autolens_profiling/pull/483 DRAFT 2026-10-29 (af93f46f; branch feature/likelihood-lifecycle-p2b-results, base the p2b branch; batch 1 72/73 legs, 60/60 cells current, 30/30 parity match; matrix-free alma 192x192 TIMEOUT recorded missing per human ruling 2026-10-29; worktree ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2b-results; human review → /prm after #471)
- pr-b-merged: https://github.com/PyAutoLabs/autolens_profiling/pull/483 MERGED 2026-10-29 32c0becd (human /prm)
- planner-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/481 MERGED 2026-10-29 c932b669 (GPU setups planned only on GPU hosts; human "fix the planner gap"; no Mind task of its own)
- rerun: quiet-node rerun of the 38 batch-1 RAL CPU legs (human 2026-10-29 "do the reruns now") RAL sma 413268 [0-13%2], alma 413269, alma_high 413270, jvla 413271 [0-7%2], --exclusive, chained afterany behind 2c 413267 (<=2 nodes); branch feature/likelihood-lifecycle-p2b-quiet-rerun bd0dca1d (no PR yet); RAL profiling/autolens_profiling_p2b_rerun → output/p2b_quiet/; quiet = loadavg_at_import[0] <= 8; ingest after
- remainder: draft/research/autolens_profiling/likelihood_lifecycle_p2bc_quiet_rerun_ingest.md (quiet-rerun ingest, shared with 2c)
- merged: 2026-10-29

## Shipped

Phase 2b profiled interferometer/{mge, rectangular, delaunay} at the standard size (Delaunay 1250 + 30 edge, rectangular 35²) on pin 2026.10.25.1, from the private RAL checkout.

- **PR A #471:** R3 standard cells, R4 numba cost-model headline (forced routes as sub-rows), `--dense` breakdown mode, resources / fit.png / parity.json in every harness, visibility-chunked eager NumPy dense reference (R6/R7, tolerance 1e-8·|ref| fp64), R1(a)/R2 planned cells (interferometer 84 → 60), `campaigns/_common.py` + `interferometer_p2b.py` generator (imaging_p2a byte-identical), matrix-free experiment harness (`experiments/`/`scans/` only), campaign page `wiki/campaigns/interferometer/likelihood_lifecycle_p2b.md`.
- **Batch 0** from dff89226 (human go 2026-10-27), then **batch 1** (RAL 413146/413158/413159/413160, references 413161, A100 413162–413165, matrix-free 413191) from 80bbb028.
- **PR B #483:** 72/73 legs landed; 60 cell rows (30 cells, each with fit.png + parity.json), 6 references, 6/7 matrix-free experiment rows, 21 rows superseded into history/. Parity 30/30 `match`. Interferometer 60/60 current; coverage (222-cell plan) 106/7/109 → 166/6/50 current/stale/missing.
- **Missing by human ruling 2026-10-29 ("go ahead with cell missing"):** matrix-free alma 192² scan leg 413191_6 TIMEOUT at 12:00:29 (dense_fft comparison arm at 36,864 source pixels). Experiment leg, not a coverage cell; recorded in `BATCH1_LIMITATIONS`, the campaigns README and the campaign page; not resubmitted.
- **#481 planner fix** (human 2026-10-29 "fix the planner gap"): `gpu_hosts: ["hpc_a100"]`; GPU setups planned only on GPU hosts (222 → 220 cells).

Verdict: the pre-registered rule is met. W~ beats dense NUFFT wherever both ran (sma). Flagged for phase 3: at delaunay alma_high forced `direct_conv` (8.8 s) beats the cost model's NumPy FFT pick (11.3 s). Per node, a ral node leads a 4×A100 node at sma/alma and trails at alma_high/jvla.

In flight at close-out: the quiet-node rerun of the 38 batch-1 RAL CPU legs (see `rerun:` above). Its branch changes the shared `scripts/misc/campaigns/_common.py` (quiet-node gate, `--exclusive`) and needs its own review; ingest is the remainder draft.

## Original prompt

# Likelihood lifecycle phase 2b: profiling campaign — interferometer/{mge, rectangular, delaunay} (84 planned cells), including the sparse W~ (`_wtilde`) and dense routes

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
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469
Consequence: judge
Witness: the coverage matrix shows zero missing and zero stale cells for class ∈ {optimal, secondary} × measurement ∈ {runtime, breakdown} for this campaign's likelihoods; every new current cell carries fit.png, provenance and parity.json; `build_catalogue --check --validate-with ../PyAutoPulse` valid at @3; the campaign wiki page records the pre-registered rule and verdict
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24

Phase 2 sub-issue 2b of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: interferometer/{mge, rectangular, delaunay} (84 planned cells), including the sparse W~ (`_wtilde`) and dense routes.

Sparse and dense, NUFFT and DFT, as in the §3.3 table.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).

## Human rulings (2026-10-25/26) and approved plan
- R1(a) dense pixelized NUFFT planned only at sma (84 → 60 cells); R2 no DFT cells; R3 hst source_pix[2] presets at the standard size (Delaunay 1250 + 30 edge AdaptSplit; rect 35² RectangularBilinearAdaptImage + Adapt; truth lensed-source adapt image, no S/N cap; MGE-20 unchanged); R4 numba headline = packaged cost-model route, forced routes as sub-rows, --n-instances 20/20/10/5 (sma/alma/alma_high/jvla); R6 visibility-chunked eager dense parity reference, one RAL task per mesh above sma; R7 parity tolerance 1e-8·|ref| fp64 (1e-3 mp); R8 batch-0 bounding cells (RAL 14 + A100 10 + optional jvla reference tasks); R9 registry instruments.
- R5 CHANGED by human 2026-10-26: pin **2026.10.25.1** (private RAL checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1).
- Human 2026-10-26: "install finufft on RAL" (the 10.25.1 NumPy NUFFT path uses finufft).
- Human 2026-10-26: matrix-free (PyAutoArray#658, merged after 10.25.1) → `numpy_cpu_matrixfree` rectangular runtime as experiments/ rows on all 4 instruments at 35² plus a mesh scan at alma (64², 128², 192²) in scans/, from a private RAL checkout at exact main SHAs (labelled unreleased), never current; log-evidence agreement vs the dense reference recorded.
- Human 2026-10-26: "make sure we have checks all the different variants with sparse, dense, but also ... matrix free sparse".
- Heart RED override: live human 2026-10-26 "Yes, authorise for 2b" (PRs + planned RAL batches).
- Plan approved: "rest sounds good". PR A = presets, numba runtime scripts, --dense breakdown mode, resources/fit.png/parity in harnesses, chunked dense reference, campaigns/_common.py + interferometer_p2b.py (imaging_p2a --check byte-identical), matrix-free experiment harness, tests, R1 designation/coverage regen. Then batch 0 → walls PR → batch 1 → PR B (survey §4).
- Queued behind rectangular-28sq-profiling-rows (both edit _production_config.py) — start PR A from main after that merges.
