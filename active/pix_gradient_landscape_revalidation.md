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
