# TruncatedNormalMessage.log_partition underflows to -inf when the support lies far in one tail (EP evidence +inf on analytic_gaussian seeds 25/172)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: `TruncatedNormalMessage(mean=-7374.18, sigma=384.36, lower_limit=0, upper_limit=100).log_partition()` returns a finite value within 1e-9 of the `scipy.special.log_ndtr`-based reference (log Z ≈ -187.93, full log-partition ≈ 2.07) instead of -inf; `python3 scripts/ensemble_seed.py --seed 25 --columns ep` in `analytic_gaussian` (mode projection) records a finite EP `log_evidence` on every step and `ep_diagnostics.results` carries no `evidence_nonfinite:` line; the posterior rows stay bit-identical to `results/ens_n5/seed_0025.json`.
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-10-23
Parent: PyAutoFit#1713 (reporting fix: NaN evidence named once per fit)

## Why

PyAutoFit#1713 diagnosed the `invalid value encountered in add` warnings of the analytic_gaussian
wave-1 ensemble (seeds 25 and 172): the variable evidence of the hierarchical scatter `sigma`
goes `+inf` on sweep 4 because one `HierarchicalFactor` member sends it an accepted
`TruncatedNormalMessage` with mean -7374.18 and sigma 384.36 on [0, 100] — its support sits
about 19.2–19.4 sigma above the mean. `TruncatedNormalMessage.log_partition`
(`autofit/messages/truncated_normal.py:58–64`) computes `log(Φ(b) − Φ(a))` directly, which is
`1 − 1 = 0` in float64, so the log-partition is -inf; the true value is finite (log Z ≈ -187.93).
Every adjacent factor term then becomes -inf and `inf + (-inf)` is NaN.

#1713 made the library report this by name and return an explicit NaN, which is the right
behaviour for a non-finite term. This prompt is the cure of the term itself. It is **message
arithmetic**, which the human's 2026-10-23 instruction ("EP is trusted — don't break it") puts
under human review, hence `Consequence: judge` and `Autonomy: supervised`.

The moments projection does not produce this message; only the mode projection does. The fit's
posterior is unaffected either way (bit-identical sidecars), so this is a readout-only defect.

## Ask

- Make `log_partition` tail-stable: compute `log(Φ(b) − Φ(a))` via `scipy.special.log_ndtr`
  (and its complement for the upper tail) with a log-diff-exp, matching the existing value to
  1e-12 in the well-conditioned regime and staying finite in either tail. Check the JAX path
  (`xp`) has an equivalent (`jax.scipy.special.log_ndtr`).
- Decide, separately and explicitly, whether a message centred ~19 sigma outside its own
  support should be accepted from the mode projection at all (projection scope — document the
  decision, do not change the projection in this task).
- Regression: a unit test on the message with the production numbers above, and the
  analytic_gaussian seed-25 mode-projection leg of `autofit_workspace_test/scripts/graphical/analytic_gaussian.py`
  (added by #1713) then asserts a finite evidence rather than "finite or named NaN".

## Lineage

- PyAutoFit#1713 — the reporting fix and the diagnosis (sweep 4, step 39/40)
- PyAutoFit#1405 — the Laplace-on-scatter state this message is a symptom of under the mode path
- PyAutoFit#1656 — moments projection (does not produce the message)
- `PyAutoCortex/rulings/2026/09/R-20260910-04.md` — the ruling that surfaced the warnings
