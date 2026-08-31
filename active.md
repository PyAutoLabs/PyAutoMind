# Active Tasks

## multistart-quick-update-wiring
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1552
- issued: 2026-08-31
- status: awaiting-input
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1552#issuecomment-5483342883
- location: web-github (batch 2026-08-31-pm member autofit-multistart-iterations,
  supervised --auto)
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - PyAutoFit: feature/multistart-quick-update-wiring
- summary: |
    Phase 1 (library) of the MultiStart* dead-kwarg bug: wire real quick updates
    into AbstractMultiStartGradient's host-side step loop (unit = gradient
    steps), forward iterations_per_quick_update / background_quick_update /
    live_visual_update into the Fitness so LiveDisplay/BackgroundQuickUpdate
    ride the standard path, make the startup message unit-honest, remove the
    EXEMPT entry in test_quick_update_wiring.py, and cover with a step-loop
    driving test. Phase 2 (autolens_workspace prose retune + AST guard) follows
    once the semantics land — file it at close-out. Sibling batch member
    autofit-prodigy-49 touches the same wiring and merges first; re-validate on
    the moved main at review.
    DONE (2026-08-31): implemented + full suite green (2334 pass serial),
    branch feature/multistart-quick-update-wiring pushed (94a658b32), no PR —
    parked at ship sign-off per the supervised contract; the question comment
    carries the gate evidence, unit decision, sibling merge-order note, the
    phase-2 filing ask, and the test-file JAX-policy deviation. On sign-off:
    open the PR with pending-release, then file the phase-2 workspace prompt.
- issue: none — science project (no GitHub home; not in repos.yaml); review via the
  next batch packet per the science-run review workflow (batches/reviews/2026-08-31-am.md)
- issued: 2026-08-31
- status: science-run (supervised --auto; human-dispatched from the 2026-08-31-am
  batch review's queued tweaks)
- location: cli-in-progress
- repos:
  - subhalo_validation (local, /mnt/c/Users/Jammy/Science/subhalo_validation, branch main — no worktree; project has no remote)
- summary: |
    Three actions from the 2026-08-31-am review rulings (project state.md "Next
    session — 2026-08-31" items 2–4), in order:
    1. `_adapt_split_fix` rerun — source_pix[1] on pl_eff_1_outer with AdaptSplit
       replacing ConstantSplit at pix[1], output suffix `_adapt_split_fix`; run only
       through source_pix[1], NO later stages chained — human inspects first.
       Scope the reg swap as an explicit knob/variant, not a silent default change
       to the delaunay_adapt_split recipe.
    2. Disable subhalo[2] (single-plane refine) for future runs — subhalo[1] grid
       detection suffices; keep visibly commented for a paper-run re-enable.
    3. RectangularBilinear runs (rectangular_adapt recipe, job A reloads / job B
       fresh via hpc/run_chain.sh) for the two successful lenses: pl_sersic_0 +
       whichever pl_eff of 342027_1/_2 lands cleanly — confirm from pulled witness
       JSONs before submitting; if pl_eff is still running/undetermined, submit
       pl_sersic_0 and park the pl_eff member as a recorded follow-up.
    Constraints: two-job JAX/numba split mandatory; RAL CPU partition `ral`; submit
    from hpc/batch_cpu; size --time from measured stage costs (grid ≈29h of ≈34h);
    commit edits locally on main; journal run rows + rewrite wiki/project/state.md.
    Pulled outputs land at the next batch collect (runs outlast this session).
