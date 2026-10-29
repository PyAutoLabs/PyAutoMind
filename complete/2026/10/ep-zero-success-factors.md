Phase of the graphical-ep EP campaign (PyAutoInsight `tasks/ep_campaign.md`), the first finding of the analytic_gaussian wave-1 ruling R-20260910-04: 19/400 seed-legs ended with a factor that never recorded a SUCCESS update.

**Diagnosis (two findings, two causes).** The NO_CHANGE-only PriorFactor (leg A seed 140 and 12 leg-B seeds) is a converged update: the factor's Laplace optimiser met its gradient tolerance at the start point (`iter=0`, posterior mean of mu within 2e-3 of the prior mean), the projection was accepted and the message updated (N(50, 22.4) → N(49.9994, 10.0)), and the posterior matches the closed form to a = 5e-5, b = 2e-5. The library's STALE tracking never flagged it; the conflation lived in the ensemble witness's criterion 6 (SUCCESS-only count). The BAD_PROJECTION-only HierarchicalFactor (6 leg-B seeds) is the #1405 Laplace-on-scatter state, cured by `LaplaceOptimiser(projection="moments")` (#1656): seeds 29 and 71 re-run under moments give HierarchicalFactor SUCCESS 28 and 23, no STALE.

**Shipped.** PyAutoFit#1712 (merge abb8bfacb): `optimise_quasi_newton` reports a zero-iteration successful convergence as `updated=True` (flag stays NO_CHANGE), docstrings on `StatusFlag.NO_CHANGE` and the EP stale tracking, two tests in `test_factor_failure_recovery.py` (one red→green). No EP update maths, projection or Laplace numerics changed; repro numerics bit-identical. autofit_workspace_test#115 (merge 97cb781): seed-140 leg A EP-only leg in `scripts/graphical/analytic_gaussian.py` (closed-form parity rows incl. widths, flag health, STALE absent; +2 s; passes against released PyAutoFit too). PyAutoCortex#75 (open, human merge): criterion 6 amended to count SUCCESS or NO_CHANGE as a completed update. PyAutoInsight#38 (open, human merge): ledger reconciliation as companion file `tasks/ep_campaign_state_2026-10-23.md` (the byte-pinned `ep_campaign.md` re-pin is the human's call).

**Witness.** Science sidecar criterion satisfied by the amendment branch of the Witness line (criterion 6 amended with the reason) plus the workspace regression; `ensemble_seed.py:160 any_factor_never_succeeded` change (count SUCCESS+NO_CHANGE) handed to the human as a diff — science checkout is outside the workspace.

**Gate at ship.** tests 3561 passed / 1 skipped / 1 xfailed (`test_autofit`), smoke `analytic_gaussian.py` PARITY 49/49 in 158 s, Heart YELLOW (manifest drift 1 mismatch; PyAutoLens release validation stale) acknowledged by the human, witness passed. CI: PyAutoFit docs/generated-search-docs/unittest 3.12/3.13/nojax all success; autofit_workspace_test smoke 3.12/3.13 success.

**Side finding (unfiled).** Seed 29 leg B under moments still misses the sigma cell (a 0.225 / b 0.416 vs 0.15 / 0.25) while sigma stays inside [q05, q95].

**Remaining in the epic.** `draft/bug/autofit/nan_in_ep_evidence_accumulation_invalid_value.md` (medium), `draft/bug/autofit/ep_moments_loggaussian_transformed_scatter.md` (small, overlaps #1498/#1331), `draft/feature/autofit/ep_lbfgs_jax.md`; the four Cortex RAL reruns are human-gated.


## Original prompt

# EP factors end the run with zero SUCCESS updates on the exactly-Gaussian leg A of analytic_gaussian (seed 140) and on 18/200 leg-B seeds

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `python3 scripts/ensemble_seed.py --seed 140 --legs a --columns ep` in `analytic_gaussian` writes a sidecar whose `legs.A.info["ep stale"]` is False and in whose `legs.A.info["ep flags"]` every factor has SUCCESS >= 1 — or, if a zero-SUCCESS factor is ruled legitimate, criterion 6 is amended with the reason; plus a regression in `autofit_workspace_test/scripts/graphical/` that pins the leg-A case.
Review-minutes: 3
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-10
Issued: 2026-10-23

## Why

Criterion 6 of the pre-registered witness of the science task
`PyAutoCortex/tasks/analytic_gaussian/ensemble_parity.md` ("no seed in which any factor ends the
run with zero SUCCESS updates") missed: **19 of 400 seed-legs** recorded at least one factor that
finished the EP run having never once been updated successfully — the STALE state PyAutoFit
#1562 / #1574 / #1576 / #1580 taught the library to report.

Ruled 2026-09-10 as `PyAutoCortex/rulings/2026/09/R-20260910-04.md` (accept with findings).

Affected seeds, from the 200-seed N=5 ensemble (RAL job 342413_[0-199], autofit 2026.8.17.1):

- **leg B** (`sigma ~ TruncatedGaussian(10, 5, 0, 100)`): seeds 29, 38, 44, 52, 62, 71, 75, 83,
  90, 106, 133, 138, 147, 149, 152, 160, 178, 193
- **leg A** (`sigma = 10` fixed): seed **140**

Leg A is the damning one. It is a linear-Gaussian graph — `mu ~ N(50, 10^2)`,
`x_i | mu ~ N(mu, 10^2)`, `y_ij | x_i ~ N(x_i, s_i^2)` — on which Laplace EP is exact by
construction, and criterion 3 confirms it: autofit EP recovers leg A 200/200 with worst
`a = 0.001`. A factor that never takes an update on a graph where every projection is available
in closed form is a library defect, not a model limitation.

The sidecars show two distinct shapes:

- a `PriorFactor*` that ends with only `NO_CHANGE` (leg A seed 140: `PriorFactor5 {NO_CHANGE: 2}`;
  most leg-B seeds, e.g. 38/44/52/62 `PriorFactor17 {NO_CHANGE: 3}`)
- a `HierarchicalFactor1` that ends with only `BAD_PROJECTION` and never a SUCCESS
  (leg B seeds 29, 71, 106, 152, 178, 193 — e.g. `{BAD_PROJECTION: 15}`, `{BAD_PROJECTION: 20}`)

Whether those are one defect or two is part of the question.

## Repro

Science project `analytic_gaussian` at `/mnt/c/Users/Jammy/Science/analytic_gaussian`
(git main, no remote), results committed at `b44390d`:

```
cd /mnt/c/Users/Jammy/Science/analytic_gaussian
python3 scripts/ensemble_seed.py --seed 140 --legs a --columns ep
```

and read the EP flag fields of the sidecar it writes — in
`results/ens_n5/seed_0140.json` they are `legs.A.info["ep flags"]`
(a `{factor_name: {FLAG: count}}` map) and the derived boolean `legs.A.info["ep stale"]`.
The witness scripts are borrowed verbatim from
`autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit}.py` @ `165a19e`.

## Ask

- Which factor is it, on which update, and **why** does it never succeed — is the projection
  rejected, is the update a no-op because the message is already the cavity, or is the factor
  never visited?
- Are the `NO_CHANGE`-only `PriorFactor` case and the `BAD_PROJECTION`-only `HierarchicalFactor`
  case the same defect or two?
- Fix it, or explain why a zero-SUCCESS factor is legitimate on an exactly-Gaussian graph — and
  if it is legitimate, criterion 6 is what has to change, with the reason recorded.
- Add a regression to `autofit_workspace_test/scripts/graphical/` that pins the leg-A seed-140
  case: on the exactly-Gaussian leg every factor ends with at least one SUCCESS update.

## Lineage

- PyAutoFit#1405 — still open, the Laplace-on-scatter collapse basin
- PyAutoFit#1580 — merged, the most recent STALE-reporting fix; this evidence is from a mirror
  that contains it (RAL PyAutoFit `66f9f8d5d` contains `08207bad0`)
- `PyAutoCortex/rulings/2026/09/R-20260910-04.md` — the ruling
- 2026-09-30: `LaplaceOptimiser(projection="moments")` (PyAutoFit#1656, record `complete/2026/09/ep-moment-projection.md`) gives 3/3 HierarchicalFactor SUCCESS on the tight toy (50, 50.5, 49.5) where the default mode path gives 0 (all BAD_PROJECTION); the `BAD_PROJECTION`-only `HierarchicalFactor` case may be cured under `projection="moments"` — re-check seed 140 / the 18 leg-B seeds with it before fixing the mode path

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/0797ba95-88e6-4a0d-a71a-b75f4417dc2c/scratchpad/item1.md -->
