## pix-gradient-slogdet-revalidation
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/112
- completed: 2026-07-22
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/114
- summary: |
    **NEGATIVE RESULT — `slogdet` does NOT reopen the pixelized gradient landscape.**
    Phase-2 validation tail of the pix-NaN lineage (localisation #104/PR#105 → fix
    PyAutoArray#392 → fitness-guard contract PyAutoFit#1391). Strict A/B: same
    script, same seed (0), 16 starts x 150 steps x adam@1e-2, one env var
    (`PIX_LOGDET`) apart, back-to-back in one SLURM job (RAL 330953, 1d07h31m).

    | | cholesky | slogdet |
    |---|---|---|
    | BEST log L | -31452.97 | -31448.10 |
    | best r_E | 1.4016 | 1.4017 |
    | plateau at | step 25 | step 25 |
    | starts alive @150 | 0/16 | 0/16 |
    | loop seconds | 43354 | 67973 (1.57x slower) |

    Delta 4.87 (0.015%) on an objective ~190k below the +17419 Nautilus bar. Both
    arms stall at the identical step, plateau at the identical value, lose every
    start. So #104 correctly localised *where* the first NaN enters, but removing
    that NaN source does not restore search progress — the #100/#101 walls are not
    (just) the non-PD Cholesky, and the log-det formulation is not the fix.

    TWO PHASE-2 POINTERS (written into searches_minimal/pix_nonfinite_findings.md):
    (1) **The stall is not the deaths** — both arms plateau at step 25 while starts
    keep dying out to step 149, so progress stops long before the population is
    exhausted: a descent-direction problem, not domain exhaustion.
    (2) **The basin is reachable but non-finite** — in both arms exactly one start
    lands at r_E ~1.42-1.45 (inside both truth 1.6 and Nautilus-mode 1.31
    tolerances) and reports log L = -inf there. That is what to localise next.
    Several starts also finish log L = nan / r_E = nan (params themselves went
    NaN), which optax.apply_if_finite latching does not prevent. The #104 "Open
    question" candidates are untouched and stay open (920x920 reduced matrix =
    900 mesh pixels + 20 unregularized MGE amplitudes may not leave a clean
    Laplacian; disconnected mesh pixels; `unique_indices=True` scatter promise in
    constant.py:55-58).

    KEY REFRAME (user's): this never needed the A100. It is a gradient-FINITENESS
    question, not a throughput one — the only hard requirement is memory (MaxRSS
    41.5 GB). The `gpu` partition was starved for days (one node down*, the other's
    4 A100s held by another user's multi-day jobs; est. start ~3 days out), so the
    A/B was re-cut onto the idle `ral` CPU partition (~900 GB / 252-CPU nodes,
    27-day walltime) where it scheduled instantly. New reusable
    `searches_minimal/pix_slogdet_ab_cpu.sbatch`. GPU job 330921 cancelled. CPU
    cost: 288s/step cholesky vs 458s/step slogdet, ~2.7 of 32 cores actually busy
    (XLA-CPU does not parallelize the 920x920 linalg well).

    BLOCKER CLEARED EN ROUTE (was blocking ALL HPC work, not just this task): the
    RAL PyAuto stack was half-migrated by the autoconf→autonerves rename —
    `autoarray` was on `autonerves` but PyAutoFit main still imported `autoconf`,
    and there was NO PyAutoNerves checkout at all, so nothing imported. Root cause:
    `HPCPullPyAuto` (~/.bashrc) only ever pulled PyAutoConf/Fit/Array/Galaxy/Lens
    and never knew about PyAutoNerves. Fixed: cloned PyAutoNerves onto RAL,
    replaced the stale RAL activate.sh (repo copy already listed PyAutoNerves),
    patched the HPCPullPyAuto repo list, pulled all 5 mains.

    SHIP NOTE: merged with human authorization while Heart was RED on "release
    validation FAILED (stage integrate)" — stale evidence (validation run
    2026-07-21T19:05Z predates the unblock-release-validation fixes that merged
    2026-07-22 20:19-20:57Z). This PR touches only HPC-only experiment scripts +
    markdown in a developer repo, so it cannot affect release validation.

    FOLLOW-UP: phase 2 should localise why the objective is non-finite *inside* the
    correct basin (pointer 2), and why best log L stops improving at step 25 while
    starts remain alive (pointer 1) — not the log-det.

## Original prompt

# Re-validate the pixelized gradient landscape after the slogdet fix

Type: experiment
Target: autolens
Repos:
- @autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: high

## Original request (verbatim)

> /start_dev draft/bug/autoarray/pixelized_likelihood_nonfinite_regions.md —
> localise-the-NaN (highest leverage; the death-point coordinates to replay are
> preserved in searches_minimal/lr_free_results/) use the right brain agent

## Standing state (why this is now validation, not localisation)

The "localise the NaN" bug the request names is **already shipped** (all merged
2026-07-17), so localisation is done and there is nothing left to localise:

- Phase 1 localisation — `complete/2026/07/pix-nonfinite-localisation.md`
  (autolens_workspace_developer#104 / PR#105). NaN pinned to ONE site,
  `AbstractInversion.log_det_regularization_matrix_term`
  (`autoarray/inversion/inversion/abstract.py:734-764`), the
  `log(diag(cholesky(H)))` of the reduced reg matrix. Prime suspect was wrong.
- Phase 2 fix — `complete/2026/07/gradient-safe-logdet.md` (PyAutoArray#391 /
  PR#392). Added `Settings.log_det_method`: default `"cholesky"` (byte-identical),
  opt-in `"slogdet"` (finite + differentiable where the Cholesky NaNs). Applies to
  BOTH evidence log-det terms via `_log_det_symmetric_from`.
- Sibling — `complete/2026/07/fitness-nan-guard-contract.md` (PyAutoFit#1391 /
  PR#1392). Pinned the contract that `Fitness.call`'s `xp.where` guard protects the
  VALUE, never the GRADIENT (`0*NaN=NaN` on the tape); a jax.grad consumer must
  avoid producing the NaN, not mask it.

What is NOT yet proven: that turning the shipped `log_det_method="slogdet"` ON
actually **reopens the pixelized gradient landscape** — i.e. that the hard
non-finite walls #100/#101 found by elimination are gone in a real multi-start
run, not just at the isolated probe points.

## Task

Re-run the pixelized multi-start gradient landscape with the shipped fix enabled
and produce an evidence-backed verdict on whether the walls are gone.

1. Enable the fix in the pix harness (`searches_minimal/pix_multi_start.py`,
   `pix_lr_free.py`): build `al.SettingsInversion(log_det_method="slogdet")` and
   thread it into `build_analysis` (currently uses config-default settings). Keep
   a cholesky-baseline toggle so the two are directly comparable.
2. Replay against the recorded baseline in `searches_minimal/lr_free_results/`
   (`pix_death_report_330592.txt`, `pix_lr_free_comparison.txt`) — the same broad
   starts that all died within ~25–50 steps.
3. Measure: fraction of broad starts that now survive to a finite optimum, step at
   which any residual death occurs, and whether the step-0 finite-loss/NaN-grad
   class is cured (the fitness-guard contract predicts it is, since slogdet stops
   producing the NaN upstream of the where).
4. Verdict: walls gone (landscape now gradient-navigable) / partially cured /
   still walled — and if residual walls remain, WHICH site (re-probe with
   `probe_nonfinite_pix.py`).

Deliverable: a findings record under `searches_minimal/` (extend
`pix_nonfinite_findings.md`) + the harness change committed; no library edits (the
library fix is already merged). If the landscape opens up, this unblocks every
gradient consumer (multi-start MAP, HMC/NUTS, MCLMC, SVGD) on the pix problem.

## Reproduction traps (durable — from phase 1)

- Will NOT run locally: one point's `value_and_grad` needs 10.90 GiB; a
  15GB/6GB-VRAM laptop OOMs on CPU and GPU. Use RAL A100
  (`probe_nonfinite.sbatch`, `--partition=gpu --mem=64gb`, ~5 min).
- Recorded death points reproduce nothing — `pix_lr_free.py:206-208` stores
  LAST-FINITE params (finite by construction). Use the seed-0 rejected draws that
  `pix_lr_free.py:124-130` silently discards (draws 12 and 35 of 90).
- A forward-only probe misses the step-0 deaths (finite value, NaN gradient) — the
  backward walk localises them.
- autoarray wrappers need `.array` before `jnp.sum` under a tracer.

## Not in scope

The withdrawn `draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md` (proposed
changing the DEFAULT log-det — the adversarial review ruled that out, C4: current
lam-dependence correct to machine precision). This experiment only toggles the
already-shipped opt-in.
