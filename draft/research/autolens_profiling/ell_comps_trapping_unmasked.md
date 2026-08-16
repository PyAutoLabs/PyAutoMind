# The `ell_comps` trapping was masked, not cleared — characterise it now it is visible

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Filed 2026-08-16. This is **follow-up (2)** owed by the `mge-lane-death` task
(`active/mge_lane_death.md`, autolens_profiling#128), which recorded it as out
of its own boundary. Follow-up (1) is
`complete/2026/08/prior-support-clipper.md` (shipped 2026-08-16 as
PyAutoFit#1477).

## What changed

The `mge-lane-death` investigation reported that the `ell_comps` plateau was
**cleared** as a suspect for the MGE cell: the trapped-lane counter read
`n_constrained_lane_steps = 0`, and a positive control confirmed the detector
was genuinely watching rather than silently absent.

That zero was correctly measured and wrongly interpreted. It meant *"nothing got
that far"* — lanes died of prior-exit first, at a mean death step of ~43 of 150.
The trapping was **masked behind a larger failure mode**, not absent.

With the prior deaths removed (the diagnostic arm that neutered
`log_prior_list_from_vector` to zeros), the constrained count is **667 of 2400
lane-steps — 27.79%**.

So PyAutoFit#1475 / PyAutoGalaxy#572's trapped-lane counter is measuring a
**live failure mode on this cell**. Lanes stop being dead and start being
**stuck**. That is an improvement — a stuck lane still has a finite figure of
merit and can still be the best-fit — but it is not a solved cell, and it is the
next thing in the way.

## Why this needs its own task

It is a different mechanism from the prior-exit death, with a different fix
space, and it lands in a different place:

- **Prior exit** is a *support* problem — the lane leaves the box, `log_prior`
  is `-inf`, the objective is non-finite. Fixed by projection (the `Clipper`).
- **`ell_comps` trapping** is a *gradient* problem — the lane is finite and
  differentiable, but sits above the `ELL_COMPS_MAGNITUDE_CLAMP` (`0.999`)
  saturation, where the radial derivative is exactly zero and the flat figure of
  merit **reads as convergence**. Projection does not help: the lane is not
  outside anything it declares.

The clamp/guard annulus documented in `complete/2026/08/frozen-lane-counter.md`
is directly relevant — the clamp saturates at `0.999` while `validate_ell_comps`
only rejects at `1.0`, and the region between is reachable and valid-by-the-guard.

## Sequencing — this runs after the Clipper

**The 27.79% is not a citable production number.** It was measured on a
*diagnostic* arm with the prior term neutered to zeros, which is not a
configuration anyone would run — it removes the prior from the objective
entirely, so the MAP being sought is not the declared one. It establishes that
the trapping is *there and large*, and nothing more.

The real measurement is on a **clipped** run, where lanes survive under the
declared prior. So this task runs on top of phase 1
(shipped: `complete/2026/08/prior-support-clipper.md`) and can share arms with phase
2 (`draft/feature/autofit/clipper_validation_campaign.md`), which already
records `n_constrained_lane_steps` per arm. **Do not re-derive the diagnostic-arm
number; measure the clipped one.**

## Questions to answer, in order

1. **How big is it under clipping?** `n_constrained_lane_steps` and the count of
   lanes *ending* trapped, on the `ClipperPriorBox` arm, at ≥2 seeds. This is
   the number that decides whether anything further is warranted.
2. **Do trapped lanes cost the answer?** A trapped lane is not a dead lane — it
   has a finite fom. Compare best-fit log-likelihood against the Nautilus truth
   bar (`results/searches/nautilus/imaging/mge/hst/hpc_a100_fp64.json`,
   `max_log_likelihood = 31786.782462488976`) with trapped lanes included versus
   excluded. If the best fit never comes from a trapped lane and the answer is
   already at the bar, this is a *budget* problem, not a *correctness* one, and
   should be reported as such.
3. **Where do they enter the plateau — and is it the corner region?** The corner
   (both components inside `(-1, 1)` with magnitude above 1) is the region a
   prior-limit detector provably cannot see, which is why the declared-constraint
   detector exists. Clipping is a per-parameter box projection, so it **cannot**
   keep a lane out of the corner either. Confirm whether clipped lanes are
   arriving there specifically — that is the case where the two mechanisms
   interact and the `Clipper` is structurally the wrong tool.
4. **Only then, the fix space.** Candidates, none pre-selected: a
   `ClipperEllComps`-style projection onto the declared model constraint rather
   than the prior box (which would make the constraint protocol a `Clipper`
   strategy, and is the tidy outcome if question 3 says corner); momentum reset
   on trapped lanes; resurrection targeted at trapped rather than dead lanes; or
   reparameterisation of `ell_comps`. **Do not open this until 1-3 are answered.**

## What would say "leave it alone"

Write these down before running, and report them honestly:

- Trapping is small under clipping (≪ 27.79%) → the diagnostic arm exaggerated
  it, because removing the prior let lanes wander into regions the real prior
  forbids. Close the question with the measurement recorded.
- Best-fit logL reaches the Nautilus bar regardless of trapped-lane count →
  wasted compute only, no correctness impact. Report as a budget finding and stop.
- Trapped lanes are all in the annulus below magnitude `1.0` rather than the
  corner → the existing guard/clamp threshold drift is the whole story, and it
  is a PyAutoGalaxy threshold decision, not a search-side task.

## Traps inherited (all paid for already)

- **Grade on the alive/trapped-versus-step curve, not the percentage.** These
  counters are **survival integrals** — a trapped lane keeps counting on every
  subsequent step, so the same curve reports a larger share at a larger budget.
  Verified exactly for the death counter (`sum(150 - k_i) = 14*150 - 654 =
  1446`). Two arms at different budgets cannot be compared on the scalar.
- **`0` and `null` are different findings.** Read counters with `.get()`; a
  `null` means the search never wrote the key — broken plumbing, not a clean
  cell. This task exists *because* a `0` was over-read once; do not repeat it in
  the other direction.
- **A zero can mean "nothing got that far".** The lesson of this whole task.
  Before reporting any counter as clean, confirm the lanes actually reached the
  regime the counter watches.
- **A crashed run poisons the next run of the same `name`** — see
  `draft/bug/autofit/crashed_run_poisons_resume.md`. Delete `output/<name>/`
  between arms or use unique names, and assert the recorded step count equals
  `n_steps` before believing any counter.
- All #128 numbers are **float32 CPU, single seed**. Expect movement on fp64 and
  do not call a difference a regression without checking precision first.

## Deliberately out of scope

- The prior-support fix itself (shipped —
  `complete/2026/08/prior-support-clipper.md`) and its validation
  campaign (`clipper_validation_campaign.md`).
- Changing `ELL_COMPS_MAGNITUDE_CLAMP` or the `validate_ell_comps` guard
  threshold. The drift between them is documented in
  `complete/2026/08/frozen-lane-counter.md`; moving either shifts geometry for
  every elliptical profile in PyAutoGalaxy and needs its own task with its own
  justification.
- Changing `resurrect` defaults — it would shift every stored multi-start
  benchmark.
