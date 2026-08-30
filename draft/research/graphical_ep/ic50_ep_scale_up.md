# IC50 use case: EP end-to-end with existing derived-variable handling

Type: research
Target: graphical_ep
Repos:
- PyAutoFit
- ic50_workspace
Themes:
- graphical-ep
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: graphical-ep
Phase: 4
Campaign: research/graphical_ep/ep_campaign.md (Phase 4)
Filed: 2026-08-19 (backfilled from git)

## Context

The IC50 cancer use case (external checkout
`/mnt/c/Users/Jammy/Science/ic50_workspace`, non-standard layout; scientific
context and run help in https://github.com/Jammy2211/ic50_assistant) is the
scale target: the end goal is graphical + EP fits at 10 000+ datasets, with a
clear demonstration that EP matches the graphical joint fit at small N before
anyone trusts it at large N.

The final model has a **derived variable**: the per-dataset factor results
inform the priors on the global model. This is currently implemented through
the declarative framework; prior GitHub discussion covers moving it into the
lower-level EP framework.

## Scope decision (made at intake, 2026-08-19)

**Use the derived-variable handling exactly as it exists.** Formalising
derived variables as a first-class EP/API concept is explicitly out of scope
here — do not let it derail the runs. If the existing handling blocks an EP
fit outright, record the blocker and route it as its own prompt; do not
redesign inline.

## The work

1. **Get an EP fit running end-to-end** on the real IC50 model, derived
   variable and all, at small N. Companion prompt
   `feature/autofit/ep_lbfgs_jax.md` (swap DynestyStatic → LBFGS/JAX for the
   simple 3-parameter factor fits) is the speed lever for the per-factor
   fits; it can land before or alongside this and stays its own PR.
2. **EP-vs-graphical parity at small N** — same model both ways, compare
   parameter means and errors (the standard strategy). This is the
   trust-building deliverable.
3. **Scale ladder** — grow N stepwise toward 10k, recording wall time, memory
   and disk at each rung. Expect the per-factor fits to be fast and the
   autofit wrapper overhead to dominate — that evidence feeds the
   EP-profiling epic (`research/autofit/autofit_profiling_bootstrap.md`)
   rather than being fixed inline here.

## Acceptance

- One committed parity table (EP vs graphical, means ± errors) at small N.
- EP runs at the largest N reached, with per-rung timings committed.
- Any derived-variable or scaling blocker recorded as its own filed prompt,
  not patched ad hoc.
