# Active Tasks

## release-smoke-env-declarations
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/272
- issued: 2026-08-31
- status: library-dev
- location: web-github (batch 2026-08-31-pm member release-smoke-env, --auto, effective level supervised)
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - PyAutoHands: feature/release-smoke-env-declarations
- summary: |
    release.yml run_smoke_tests replaces its bash loop with the canonical
    env-aware runner (autohands/run_python.py --list smoke_tests.txt
    --report-dir), so in-file __Env__ declarations govern release smoke runs
    and witt_wynne.py (ENV: full_datasets) stops failing every LIVE release.
    Plan on the issue; option 1 of the prompt (no autolens_workspace change).

## subhalo-followup-adapt-split-rectangular
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
