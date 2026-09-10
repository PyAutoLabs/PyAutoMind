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

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/0797ba95-88e6-4a0d-a71a-b75f4417dc2c/scratchpad/item1.md -->
