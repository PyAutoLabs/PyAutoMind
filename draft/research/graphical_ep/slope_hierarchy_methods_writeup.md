# slope_hierarchy: methods write-up (NUTS headline, EP cautionary)

Type: docs
Target: graphical_ep
Repos:
- slope_hierarchy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Model: Opus (narrative/scientific prose — see feedback_tutorial_prose_opus)

## Context

`slope_hierarchy` (private, Jammy2211/slope_hierarchy#1, external checkout
`/mnt/c/Users/Jammy/Science/slope_hierarchy`) answered all four of its goals and
was wrapped up on 2026-07-22 with every result committed. `paper/figures/` and
`paper/tables/` exist but are **empty** — nothing has been written yet.

## What there is to write about

The project has an unusually clean methods story, because the negative result is
sharp and fully diagnosed rather than hand-waved:

1. **Goal 1 — JAX-gradient NUTS works.** BlackJAX NUTS on the joint factor graph
   recovers the parent mean 2.028 [2.000, 2.063] and scatter 0.143 [0.117, 0.185]
   against truth (2.0, 0.1). This is the headline method.
2. **Goal 2 — EP recovers the mean but not the scatter.** Converged EP gives mean
   2.051 (agrees with NUTS) but scatter 0.026 — ~4× low — with errors ~1000× too
   tight. Crucially this was separated from two innocent explanations before
   being called a failure mode: the **projection bug** (real, found here, fixed
   in PyAutoFit#1383) and **under-convergence** (the round-1 `max_steps=5` value
   of 0.004 was a badly under-converged snapshot; the true fixed point is 0.026,
   reached at `max_steps=12` and flat for the last ~2 sweeps).
3. **Goal 3 — the RAL HPC pipeline** works end to end.
4. **Goal 4 — the 2026-07 EP diagnostics wave** (PyAutoFit#1330/#1335) was
   exercised in anger and **caught a real projection bug**, shipped as
   PyAutoFit#1383. That is the strongest possible endorsement of the diagnostics:
   they found a defect in the framework that ran them.
5. **The generalisation.** A follow-up CPU toy (PyAutoFit#1405) proved the
   scatter pathology is a **framework property, not a property of this problem** —
   it reproduces off-boundary (parent σ=10) and off-lensing, as *stochastic
   instability* across identical runs: 70% recover / 7% collapse / 23% crash.
   The honest methods claim is therefore about EP-for-scale-hyperparameters in
   general, not about N=5 strong lenses.

## The claim to land

**Use a joint gradient sampler (NUTS) for a hierarchical scale hyperparameter;
EP is fast and correct for the parent mean but over-confident and
variance-shrinking on the scatter.** Say plainly that the failure is stochastic
(a basin, entered ~7% of the time on a clean toy) rather than a fixed bias — a
reader who runs EP once and recovers the truth has not disproved this.

## Scope decision to make first

Two honest shapes, and this should be settled before drafting:
- a **methods note / project write-up** in `paper/` for internal use and to
  ground the PyAutoFit issues; or
- a **publishable short paper**, which realistically wants the N=25–50 scale-up
  (`slope_hierarchy_n25_scale_up.md`) first, since N=5 is thin for a headline
  parity claim.

Prefer the note unless the scale-up has already run — the note costs a session
and preserves everything; the paper does not.

## Deliverable

Prose + figures/tables committed under `paper/`, with figures regenerated from
the committed `results/` JSONs (do not hand-copy numbers — they are all in
`results/*.json` and `results/ep_history_n5_maxsteps12/parent_trajectory.csv`).
Repo is private and personal — keep it out of public repos
(`feedback_pyautopaper_personal_repo`).

<!-- filed 2026-07-22 when the slope-hierarchy task was wrapped up. -->
