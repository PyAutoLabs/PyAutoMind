# Likelihood lifecycle phase 2g: weak lensing — decisions, RAL batches and PR B

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
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-29

- batch0: SUBMITTED 2026-10-29 20:27 GMT from /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main ad103340 (#486 XLA:CPU workaround merged fe81b1f4, #485 decisions merged ad103340), pin 2026.10.25.1, guarded detached script /mnt/ral/jnightin/scratch/p2dg_batch0_submit.sh (log p2dg_batch0_submit.log, marker P2DGBATCH0SUBMITDONE; guards: venv jax/jaxlib 0.11.2, HEAD == SHA, clean tree, pin tags, flag in all 9 submits, no output/*_batch0). ENV CHANGE: the shared RAL venv /mnt/ral/jnightin/PyAuto/PyAuto was upgraded jax/jaxlib/jax-cuda12-plugin/jax-cuda12-pjrt 0.10.2 -> 0.11.2 (human 2026-10-29, 'Upgrade the shared venv'; log scratch/jax0112_upgrade.log, freezes scratch/pyauto_venv_freeze_{before,after}_jax0112_20261029.txt; only the 4 jax packages changed; pip check: only anesthetic numpy<2 and ipython psutil>=7, unrelated to jax). FLAG: every JAX_PLATFORMS=cpu leg runs with --xla_cpu_multi_thread_eigen=false appended to XLA_FLAGS (shared preamble, #486; human option 'All JAX CPU legs'), GPU legs never; rows record it in device.xla_flags. The A100 legs are the first GPU test of jax 0.11.2 on RAL. Rows: output/p2g_batch0/. All 9 submits: RAL CPU p2d 413272, p2e 413273, p2f 413274, p2f references 413292, p2g 413293; A100 p2d 413294, p2e 413295, p2f 413296, p2g 413297. This campaign: 413293 [0-1%8] 1:30:00 RAL CPU + 413297 1:30:00 A100 (one job). At 20:40 the early tasks had completed exit 0 with no FAILED/Traceback/REFUSING in the .out files; NEXT: sacct all, walls.tsv, parity, walls commit, batch 1 (human go).
- batch0 earlier hold (2026-10-29, superseded by the line above): Decisions adopted: human "ok can we do all that now then" adopted every drafted option (2g D1-D4, D6-D10; D9 = batch-0 rows are the campaign rows, no batch 1; D5 settled by #481); recorded docs-only in autolens_profiling#485 (open, human /prm). The batch-0 go was given but HELD: the RAL venv /mnt/ral/jnightin/PyAuto/PyAuto (activated by every submit, CPU and A100) carries jax/jaxlib 0.10.2, which the pin 2026.10.25.1's PyAutoNerves excludes (Heart#274), so rows would not match the pin's dependency floor (human's call). The human then said not to start anything new on RAL that evening. Prepared but unused: detached checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ main 32c0becd (log /mnt/ral/jnightin/scratch/p2dg_checkout.log); guarded submit script draft (not on RAL) in the session scratchpad.
- Status: split out of `likelihood-lifecycle-p2g-weak` at close-out 2026-10-29 — the campaign setup shipped (autolens_profiling#477), recorded in `complete/2026/10/likelihood-lifecycle-p2g-weak.md`; this is what remains. No RAL batch has run.
- Shipped setup: `scripts/misc/simulators/weak.py`, `likelihood_breakdown/weak_standard.py`, `scripts/weak/isothermal/likelihood_{runtime,breakdown}.py`, registry cell `weak/isothermal/simple`, `scripts/misc/campaigns/weak_p2g.py` + `submit_campaign_p2g_*`; page `wiki/campaigns/weak/likelihood_lifecycle_p2g.md`.

## What remains

1. The human reviews the open decisions below (campaign page has the full table with reasons and alternatives) and rules on each.
2. **Batch-0 go** from the human (none given: "leave this as something I then review before we do RAL runs"). Then run batch 0 from a private RAL checkout at pin 2026.10.25.1 (or whatever pin the human sets).
3. Walls commit: fill `BATCH0_WALLS` / `BATCH0_PEAK_RSS_KIB`, set `WALL_BASIS_STATUS="measured"`, re-render the submits (weak_p2g.py `--write`).
4. **Batch-1 go**, then batch 1.
5. PR B: copy the complete cells into `results/`, regenerate catalogue / coverage / dashboard, record the verdict on the campaign page(s), refetch the Pulse receipt.

## Open decisions (drafted in #477; human rules)

- **D1, one evaluation:** `AnalysisWeak.log_likelihood_function(instance)` — tracer, model shear at N positions via the `LensCalc` Hessian (JAX `jacfwd`), chi-squared over 2N components plus noise normalization.
- **D2, naming:** likelihood `weak/isothermal`, instrument `simple`.
- **D3, standard size:** 1500 galaxies (3000 shear components), the `simple` catalogue (50"–200" annulus, ~46 galaxies/arcmin², sigma 0.25).
- **D4, setups and hosts:** the §3.3 weak row: `jax_cpu_dense_fp64` (provisional optimal) and `jax_gpu_dense_fp64` (secondary); `jax_cpu@hpc_a100` runs on the A100 node's CPU inside the GPU job.
- **D5 — settled** by autolens_profiling#481 (human 2026-10-29 "fix the planner gap"): GPU setups are planned only on `hpc_a100`, so the 2 `jax_gpu_dense_fp64@hpc_ral_cpu` cells are gone. Re-check the plan count after the merge.
- **D6, setup spelling:** `_dense_` as §3.3 writes it (alternative `_na_`, as point sources use).
- **D7, parity:** vs eager NumPy `FitWeak` (finite-difference Hessian), tolerance 1e-4 × |ref| (laptop agreement 2.7e-12 relative).
- **D8, what is timed:** runtime = JIT steady median + vmap per call at batch 32; breakdown = `model_shear`, `likelihood_from_shear` + a deflections reference.
- **D9, batch plan:** batch 0 = all runnable legs; proposal: accept its rows as the campaign's rows and skip batch 1.
- **D10, fit figure:** `subplot_fit_weak` as `fit.png` (chi-squared colour bar reads `e- s^-1`, a library plotting quirk to raise with Eyes).

## Also
- No RAL dry run of the submits was done; the A100 GPU leg (`JAX_PLATFORMS=cuda,cpu`) is untested locally.
- Check whether 2d's jaxlib 0.11.2 XLA:CPU deadlock (D12 there) affects the weak JAX CPU cells before batch 0.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
