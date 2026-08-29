## overflow-flood-refs-smc-cell
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/196
- completed: 2026-08-29
- library-pr: autolens_profiling#197 (merged f284f246f -> main)
- what shipped: (1) record corrections — 341908_5 made 90,000 Nautilus calls / 29 bounds / maxL 30,701.3 and was killed by a finite log_l overflow flood (up to 3e+303) from the λ⁴ Adapt coefficient, not a thrash (PROGRAMME ×3, targets/REFS_V1_HARVEST, DECISIONS +2 entries incl. the library stack boundary; knn ref −480 nat = same pathology); (2) `_setup._free_adapt_split(cap=1e4)` → `al.reg.AdaptSplitPower` with LogUniform(1e-6,1e4) coefficients for knn / slam_source_pix_nn / delaunay_adapt_split → 8 new target_ids (knn_fp64 ccafb8b191bc, slam_source_pix_nn_fp64 ad291b57fc62, …); legacy rows NOT restamped (they ran λ⁴ — the boundary is the point); (3) `PYTHONUNBUFFERED=1` in activate.sh SLURM block; (4) slogdet A/B submit `submit_search_nautilus_slogdet_ab_imaging_slam_source_pix_nn_a100_hst_fp64` via `build_ab_for_cell`; (5) SMC cell — `build_smc` (af.SMC) + `SAMPLER_BUILDERS`, leaf `scripts/imaging/searches/smc/mge.py`, `SEARCHES_SMC_*` README block, probe submit `submit_search_smc_imaging_mge_a100_hst_fp64_probe` (mala_warm, hmc_warm, mala_cold; warm = `prior_scaled` diagonal at the Prodigy MAP because the 16-sample source is below af.SMC's 2·n_dim=30 covariance floor — cannot test H6.1 anisotropy; Nautilus-sourced warm start owed), PROGRAMME Phase 7 in flight; (6) BONUS: `log_det_method` was absent from four of five sampler identifiers → a slogdet A/B would run once and report twice (RAL 340576's nested-path defect); shared `_samplers.log_det_arm_tag`, env-override-only so no recorded path moves (test-pinned).
- validation: pytest 293 (+37); ruff/format; build_readme --check; check_submits --check 55/0; SMC leaf smoked in test mode; identifiers verified to change for refs 5/6/7 (no resume collision); lint CI green on both commits.
- heart-ack: shipped + merged under human-authorised YELLOW ("prm", 2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source". Unrelated.
- next: HPCPullPyAuto (Fit b70cf7fc3 / Array 302d5df32 / Galaxy 2ee44d507 / Lens af514d179) then `sbatch --array=5,6,7 --requeue …refs_v1_array.sh`, `sbatch --requeue …slogdet_ab…slam_source_pix_nn…`, `sbatch --requeue …smc…probe` (~8 tasks, ~30 GPU-h); harvest = later session. Pre-existing: slam_source_pix_nn NaN at the PYAUTO_TEST_MODE=2 point (same on main).

## Original prompt

# Refs 5,6 unblock, overflow-flood record correction, slogdet A/B, SMC cell + A100 probe

Type: feature
Epic: inference-programme
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- inference
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-29
Issued: 2026-08-29

## Original request (verbatim)

> do the 5 things above listed and make sure we have some SMC runs going soon

## Context

Wave B of the overflow-flood fix wave (plan `glowing-puzzling-nova`). Wave A
merged three library changes this workspace now builds on:

- **PyAutoFit** `Fitness` magnitude guard — `general.test.log_likelihood_ceiling`
  (default `1e20`) rejects implausibly large finite log-likelihoods.
- **PyAutoFit** `af.SMC` — blackjax adaptive-tempered SMC with `mala`/`hmc`
  inner kernels, `SamplesSMC` carrying `log_evidence`, `lambda_list`,
  `acceptance_rate_list`, `ess_list`.
- **PyAutoArray** `al.reg.AdaptSplitPower(inner_coefficient, outer_coefficient,
  signal_scale, power=1.0)` — the squared-once Adapt sibling; `power` is a
  `Constant` in the priors and is never sampled.

RAL pilot 341908_5 (`slam_source_pix_nn`, free `AdaptSplit` on DelaunayNN) was
ledgered as "0 Nautilus calls in 6 h / thrashes". The checkpoint.hdf5 diagnosis
(2026-08-29) says otherwise: **90,000 likelihood calls, 29 bounds,
explored=FALSE, maxL 30,701.3, 0.239 s/eval, MaxRSS 3.66 GB, TIMEOUT at 6 h**.
Zero NaN and zero -inf; finite `log_l` up to **3e+303** in shells 14/23/24/26/28,
`shell_log_l` up to 1e56 with `shell_n_eff` ~ 1. The job was killed by a
**likelihood-overflow flood**, not by thrashing: `Adapt*` squares the
coefficient twice (lambda^4), the regularization matrix goes non-PD from
c ~ 1e4 under `LogUniform(1e-6, 1e6)`, fp64 Cholesky returns finite garbage,
`Fitness` passed it through and Nautilus accepted it as the best point, so
`f_live` could never terminate. The `.out` froze at `Calls | 0` because stdout
was block-buffered. The knn reference row's -480-nat deficit is the same
pathology.

## Goal

1. **Record corrections.** `PROGRAMME.md:37,:992`, `targets/REFS_V1_HARVEST.md:12,128`
   corrected in place with a "corrected 2026-08-29" note; a NEW dated
   `DECISIONS.md` entry (append-only) that supersedes the 2026-08-27 block,
   links Wave A's PyAutoFit/PyAutoArray changes, and marks the **library stack
   boundary** — post-Wave-A Adapt coefficients are not comparable with pre-Wave-A
   rows, and the knn reference row must be re-run.
2. **Switch the free-AdaptSplit targets to `al.reg.AdaptSplitPower` + prior cap.**
   A `_setup.py` helper returning `af.Model(al.reg.AdaptSplitPower)` with
   `inner/outer_coefficient = af.LogUniformPrior(1e-6, 1e4)`, used by
   `_knn_model`, `_slam_source_pix_nn_model` and `_delaunay_adapt_split_model`
   so their documented parameter-identity survives. `target_id`s change;
   re-stamp affected recorded rows with `restamp_target_block.py`.
   `slam_source_pix_nn`'s free `signal_scale` is left as is.
3. **Unbuffered stdout.** `export PYTHONUNBUFFERED=1` in `activate.sh` under the
   existing `$SLURM_JOB_ID` block, covering all submits at once.
4. **slogdet A/B on `slam_source_pix_nn`** — a 2-arm submit through
   `_setup.build_ab_for_cell(..., log_det_methods=("cholesky", "slogdet"))`,
   Nautilus `n_live=300`, `--time=8:00:00`, WALL-BASIS `unmeasured / probe-first`.
5. **Refs 5,6 resubmit** on the post-Wave-A stack, plus a re-run of the `knn`
   reference row (its row is suspect for the same reason).
6. **SMC cell.** `build_smc` in `scripts/misc/searches/_samplers.py` wrapping
   `af.SMC` (+ a `SAMPLER_BUILDERS` row), leaf
   `scripts/imaging/searches/smc/mge.py`, a `SEARCHES_SMC_*` env block in
   `scripts/misc/searches/README.md`, and an A100 probe submit with
   `mala_warm` / `hmc_warm` / `mala_cold` arms warm-started from the existing
   RAL Prodigy MAP fit. PROGRAMME Phase 7 row -> "in flight".

Item 7 of the plan (the RAL sbatch submits) is **not** part of this task: the PR
must merge and `HPCPullPyAuto` must run on RAL first.

## Out of scope

The factor-2 `Adapt` scatter asymmetry (filed separately); pinning
`signal_scale` on `slam_source_pix_nn`; harvesting any Wave-B run.
