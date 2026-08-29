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
