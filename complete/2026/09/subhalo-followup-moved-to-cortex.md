- issue: none — the science project has no GitHub home (not in repos.yaml); no issue was ever opened
- completed: 2026-09-01
- classification: research (subhalo_validation) — a science follow-up wave, closed by MIGRATION not by delivery
- summary: |
    The subhalo-validation follow-up wave — the three actions the human ruled in the
    2026-08-31-am batch review (`batches/reviews/2026-08-31-am.md`) and dispatched the same
    day as RAL jobs 342093_0 (the `_adapt_split_fix` source_pix[1] rerun of pl_eff_1_outer
    with AdaptSplit replacing ConstantSplit), 342094_0 and 342095_0 (the RectangularBilinear
    `rectangular_adapt` chain on pl_sersic_0) — has **moved to the Cortex** as
    `PyAutoCortex/phases/subhalo_validation/delaunay_adapt_split_pl_eff_1_outer.md` and
    `PyAutoCortex/phases/subhalo_validation/rectangular_adapt_pl_sersic_0.md`, alongside the
    two lens phases carrying the accepted and awaiting-ruling results
    (`delaunay_adapt_split_pl_sersic_0`, `delaunay_adapt_split_pl_eff_0`). No GitHub issue
    ever existed for this work, so nothing is closed on a tracker; the record simply changes
    organ. All four witnesses have landed. The rulings of record are **R-20260831-06**
    (pl_sersic_0 accepted) and **R-20260831-07** (pl_eff leave-to-finish), both held in the
    Cortex; the two runs dispatched by this wave (342093_0 and 342095_0) are awaiting the
    human's ruling and no ruling has been invented for them here. This record exists so the
    Mind's history of the wave stays readable after the prompt was removed in the Cortex
    phase-4 migration (PyAutoMind#383).

## Original prompt

# Subhalo validation follow-up wave: AdaptSplit fix, no subhalo[2], RectangularBilinear runs

Type: research
Target: subhalo_validation
Repos:
- subhalo_validation
Themes:
- pixelization
- hpc-gpu
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Lane: local-dev
Filed: 2026-08-31
Issued: 2026-08-31

From the 2026-08-31-am batch review (packet `batches/packets/2026-08-31-am.html`,
members `subhalo-pl_sersic_0-342027_0` accept / `subhalo-pl_eff-342027_12`
leave-to-finish). Project: `/mnt/c/Users/Jammy/Science/subhalo_validation` (read its
`AGENTS.md` and `wiki/project/state.md` first). Human note, verbatim:

"""
2) The pl_eff_1_outer_no_subhalo task did not get a good result, the outer source
galaxy messed up the solution. I think the issue is that source_pix[1] used
ConstantSplit, not AdaptSplit, so can you rerun source_pix[1] on this lens with a
suffix "_adapt_split_fix" and I will inspect the result.

We dont need subhalo[2] for these currently, knowing if theres a detection in
subhalo[1] is sufficent so dont run subhalo[2] for future runs.

Lets also do a RectangularBilinear run for the two successful lenses in the next
batch / task.
"""

Three actions, in order:

1. **`_adapt_split_fix` rerun.** Rerun `source_pix[1]` on `pl_eff_1_outer` with the
   output suffix `_adapt_split_fix`, swapping the stage's `ConstantSplit`
   regularization for `AdaptSplit` (root-cause hypothesis: ConstantSplit at pix[1]
   let the outer source component corrupt the solution). Deliverable is the run plus
   pulled outputs — **the human inspects the result before anything further**; do not
   chain later stages onto it.
2. **Disable `subhalo[2]`** (the single-plane refine) in the pipeline for future
   runs — `subhalo[1]`'s grid detection answer is sufficient for this project. Keep
   the change visible/commented so it can be re-enabled for a science paper run.
3. **RectangularBilinear runs** for the two successful lenses via the
   `rectangular_adapt` recipe — the mesh/regularization comparison rows in
   `wiki/project/results_summary.md`. "Two successful" = `pl_sersic_0` plus
   whichever of the `pl_eff` lenses lands cleanly from 342027 (confirm from the
   pulled witness JSONs before submitting).

Constraints from the project (see state.md): two-job JAX/numba split is mandatory;
RAL CPU partition is `ral`; submit from the project's `hpc/batch_cpu`; `hpc/sync
pull` now fetches `results/`. Record measured stage costs (grid ≈ 29 h of ≈ 34 h)
when sizing `--time`.
