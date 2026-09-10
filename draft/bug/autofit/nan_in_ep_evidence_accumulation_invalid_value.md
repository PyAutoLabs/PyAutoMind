# NaN in EP evidence accumulation: `invalid value encountered in add` in ep_mean_field.py on analytic_gaussian seeds 25 and 172

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: `python3 scripts/ensemble_seed.py --seed 25 --columns ep` and the same for seed 172 complete with no `RuntimeWarning` from `ep_mean_field.py`, and the EP evidence they record is finite — or the non-finite term is raised/logged with the variable named rather than warned-and-summed, with a regression in `autofit_workspace_test/scripts/graphical/` asserting the EP evidence of a converged fit is finite.
Review-minutes: 3
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-10

## Why

Two seeds of the 200-seed N=5 ensemble behind
`PyAutoCortex/tasks/analytic_gaussian/ensemble_parity.md` (RAL job 342413_[0-199],
autofit 2026.8.17.1) emitted a numpy warning from the EP evidence accumulator, repeatedly.
Verbatim from `hpc/batch_cpu/error/error.342413_25.err` (line 1, repeated 7x in that file and
10x in `error.342413_172.err`):

```
/mnt/ral/jnightin/PyAuto/PyAutoFit/autofit/graphical/expectation_propagation/ep_mean_field.py:336: RuntimeWarning: invalid value encountered in add
  return factor_evidence + sum(variable_evidence.values())
```

`invalid value encountered in add` is numpy's NaN-producing-add: at least one term of
`factor_evidence` or of `variable_evidence.values()` is non-finite (NaN, or a ±inf pair), and
the library warns and keeps going, folding the result into the EP evidence readout.

This is a **separate symptom** from the zero-SUCCESS stale-factor finding of the same ruling:
neither seed 25 nor seed 172 appears in that finding's 19 stale seed-legs, and both seeds'
parity results are otherwise fine — they are not among the outliers on any row. So the evidence
accumulator is going non-finite on runs that otherwise look healthy, which is exactly the case a
warning is least likely to be noticed in.

Ruled 2026-09-10 as `PyAutoCortex/rulings/2026/09/R-20260910-04.md` (accept with findings).

## Repro

Science project `analytic_gaussian` at `/mnt/c/Users/Jammy/Science/analytic_gaussian`
(git main, no remote), results committed at `b44390d`:

```
cd /mnt/c/Users/Jammy/Science/analytic_gaussian
python3 scripts/ensemble_seed.py --seed 25 --columns ep
python3 scripts/ensemble_seed.py --seed 172 --columns ep
```

Run them with `python3 -W error::RuntimeWarning` (or `np.seterr(invalid="raise")`) to get the
traceback at the moment the term goes non-finite. The witness scripts are borrowed verbatim from
`autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit}.py` @ `165a19e`;
the per-seed sidecars are `results/ens_n5/seed_0025.json` and `seed_0172.json`.

## Ask

- **Where does the non-finite variable evidence come from?** Which variable's
  `variable_evidence` entry is NaN/inf, and what makes it so — a degenerate (zero- or
  negative-variance) message, a log of a non-positive normalisation, an inf−inf cancellation?
- **Should this warn and continue at all?** Decide between guarding it (skip / clamp the term
  with a named reason), raising it (a non-finite evidence is a broken fit and should say so), or
  logging it with the offending variable named. Warn-and-sum is the one option that leaves no
  usable trace in a batch run — the only reason it was caught here is that SLURM kept the
  `.err` files.
- **Does it bias the EP evidence readout?** If the accumulated evidence is used for
  convergence, model comparison or the reported `log_evidence`, a silently-NaN term is a
  correctness problem, not cosmetic. Say which, with the evidence for it.
- Add the regression named in the Witness above.

## Lineage

- `PyAutoCortex/rulings/2026/09/R-20260910-04.md` — the ruling that surfaced it
- PyAutoFit#1405 — the open Laplace-on-scatter collapse basin (leg B's known bias); this is not
  that, but the same EP path

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/0797ba95-88e6-4a0d-a71a-b75f4417dc2c/scratchpad/item2.md -->
