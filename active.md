# Active Tasks

## autofit-prodigy-49
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1553
- prompt: active/multistartprodigy_stops_at_49_steps_when_iterati.md
- issued: 2026-08-31
- status: library-shipped, awaiting-merge (--auto safe; batch 2026-08-31-pm member autofit-prodigy-49)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1555
- location: web-github (remote session clone; no task worktree)
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - PyAutoFit (branch feature/multistart-quick-update-49-steps)
- summary: |
    Investigated: MultiStartProdigy cannot stop at a quick-update boundary — the
    multi-start step loop never reads iterations_per_quick_update and the
    convergence gate (min_steps=100) plus the n_steps ceiling are the only stop
    paths (empirically confirmed: cadence=50, n_steps=120 runs 120/120). The
    reported "49 steps" is search.summary's `Total Samples = 49` line
    (1 best + n_starts=48 per-start finals) misread as a step count. Fix:
    report Total Steps / Stop Reason in the multi-start search.summary block,
    disambiguate the Total Samples line, and pin the non-termination with an
    end-to-end MultiStartProdigy regression test (the prompt's Witness).
    PR #1555 CI green on head 2629933cc; merge serially before
    autofit-multistart-iterations per the batch record.

## organ-board-github-link
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/325
- prompt: active/github_page_link_in_every_organ_board.md
- issued: 2026-08-31
- session: claude-code-remote (batch 2026-08-31-pm member organ-board-github-link, web-github)
- status: pr-open (all five legs of the autonomous-ship gate passed 2026-08-31; merge is the human's)
- branch: feature/organ-board-github-link
- prs:
  - https://github.com/PyAutoLabs/PyAutoBrain/pull/326
  - https://github.com/PyAutoLabs/PyAutoHeart/pull/194
  - https://github.com/PyAutoLabs/PyAutoHands/pull/273
  - https://github.com/PyAutoLabs/PyAutoMemory/pull/77
  - https://github.com/PyAutoLabs/PyAutoScientist/pull/25
- repos:
  - PyAutoBrain
  - PyAutoHeart
  - PyAutoHands
  - PyAutoMemory
  - PyAutoScientist
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)

## resampling-info-summary-section
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1551
- prompt: active/add_resampling_info_section_to_the_bottom.md
- issued: 2026-08-31
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1554
- batch: 2026-08-31-pm — member autofit-resampling-info, --auto; effective level
  supervised (= min(header safe, bug work-type cap)); shipped via decide-and-flag
  (one flagged decision: PR-open instead of park at ship sign-off — see PR body)
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - PyAutoFit: feature/resampling-info-summary-section

## numba-vs-jax-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/513
- prompt: active/numba_solve_vs_jax_sparse_operator.md
- issued: 2026-08-31
- status: awaiting-input (verdict posted 2026-08-31; judge-tier research — parks
  for human review per the supervised contract; sign-off retires via close-out,
  a failed review files an ordinary /intake follow-up)
- question: https://github.com/PyAutoLabs/PyAutoArray/issues/513#issuecomment-5483142802
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - PyAutoArray: main (read-only — research verdict, no branch)
- summary: |
    Is the numba CPU positive-only solve the same linear algebra as the JAX
    sparse-operator mode? Characterise the shipped numba lineage (#498/#501
    warm-start memo, #505/#507 curvature-F work, SparseLinAlgImagingNumba
    preload) against the JAX ImagingSparseOperator + jaxnnls PDIP path; assess
    GPU-portability of the numba levers; verdict unify/port/keep posted on the
    issue. Judge-tier: verdict parks for human review, no decide-and-flag.

## subhalo-followup-adapt-split-rectangular
- prompt: active/follow_up_wave_adapt_split_and_rectangular.md
- issue: none — science project (no GitHub home; not in repos.yaml); review via the
  next batch packet per the science-run review workflow (batches/reviews/2026-08-31-am.md)
- prompt: active/follow_up_wave_adapt_split_and_rectangular.md
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

## memory-queue-filing-gate
- prompt: active/repair_queue_automation_filing_gate.md
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/75
- issued: 2026-08-31
- status: ship — PR open (PyAutoMemory#76, decision-taken; --auto, effective supervised, batch 2026-08-31-pm; merge + close-out re-drive human)
- location: web-github
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)
- repos:
  - pyautomemory (branch feature/memory-queue-filing-gate — web-github session clone, no worktree)
- summary: |
    Repair the PyAutoMemory queue automation (#69/#71/#72 stuck since
    2026-08-28): add the PyAutoBrain sibling checkout to queue_filing.yml
    (gate hard-broken since dcd1e2c, 2026-08-24), make queue_actions.yml's
    push retry conflict-proof (fetch + reset --hard + re-run the idempotent
    action script instead of rebase-and-discard), and add an if: failure()
    report step so a failed run comments on its issue instead of silence.
    Close-out post-merge (human): re-apply labels on #69/#71/#72; Witness =
    green queue_filing.yml run on #71 that opens a filing PR.
