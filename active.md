# Active Tasks

## euclid-cpu-two-stage-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49
- prompt: active/cpu_vis_lp_jax_vis_pix_numba_submission.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01BhD2t684rJZi1tT34u2KgR
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/euclid-cpu-two-stage-route
- repos:
  - euclid_strong_lens_modeling_pipeline (feature/euclid-cpu-two-stage-route)
- epic: euclid-dr1-prep (Mind phase 4; gates PyAutoCortex phases/euclid/dr1_prelim_10_lens_science_run)

## silence-colab-cli-message
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/156
- prompt: active/silence_the_non_colab_setup_colab_message.md
- issued: 2026-08-31
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/157
- session: web-github (batch 2026-08-31-pm member autonerves-colab-silence, --auto)
- repos:
  - PyAutoNerves: feature/silence-colab-cli-message
- heart-ack:
  - manifest drift: local checkout origins — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - CI status unavailable for all 6 libraries and 11 workspaces (web container: Heart's ci_status.sh shells to gh, which does not exist here — measurement blindness, not a measured red)

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

## image-source-mappings-p2
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/719
- prompt: active/mappings_shape_solver_fit_subplot.md
- issued: 2026-09-02
- session: claude --resume 7ac5cc85-dfd9-41e2-a4bd-725f33f0f24f
- status: library-shipped (PR-A #518 → PR-B, awaiting /prm)
- library-pr: PyAutoArray https://github.com/PyAutoLabs/PyAutoArray/pull/518
- library-pr: PyAutoLens https://github.com/PyAutoLabs/PyAutoLens/pull/720
- epic: image-source-mappings (phase 2 + 2a — ledger draft/feature/autoarray/image_source_mappings_epic.md; opened 2026-09-02 by user decision ahead of the PyAutoArray release that gated it)
- heart-ack:
  - "PyAutoArray: open PR 10d old"
  - "release validation incomplete: no rehearsal for current source"
- worktree: ~/Code/PyAutoLabs-wt/image-source-mappings-p2
- parallel-claim: PyAutoArray — numba-vs-jax-sparse holds a read-only research claim on main (no branch, no worktree); file sets disjoint
- repos:
  - PyAutoArray: feature/image-source-mappings-p2
  - PyAutoLens: feature/image-source-mappings-p2
- summary: |
    Phase 2 of image-source-mappings. PR-A (PyAutoArray, phase 2a): Shape.contains / Shape.boundary on
    autoarray/structures/triangles/shape.py. PR-B (PyAutoLens): ShapeSolver validation suite + audit fixes,
    ShapeSolver.image_regions_from / mapping_from, autolens/lens/mappings.py (fit-level mappings, brightest
    multiple-image positions in arcsec + pixels, per-image magnification), subplot_mappings(fit), plots.yaml wiring.
    Fable session; execution delegated to Opus. Library-first: PR-A merges before PR-B (PyAutoLens PR CI is source-installed
    against PyAutoArray main).

## numpy-deflections-p2
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/596
- prompt: active/numpy_deflections_p2_mge_wofz.md
- issued: 2026-09-02
- session: claude --resume d3971bba-0e8d-4c4f-bc59-7808e6bfa6cd
- status: shipped, awaiting-merge (merge order PyAutoGalaxy#597 → autolens_profiling#212)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/212
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/597
- epic: numpy-deflections-cpu (phase 2 — ledger draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md)
- worktree: ~/Code/PyAutoLabs-wt/numpy-deflections-p2
- heart-ack:
  - PyAutoArray: open PR 10d old
  - release validation incomplete: no rehearsal for current source
- repos:
  - PyAutoGalaxy: feature/numpy-deflections-p2
  - autolens_profiling: feature/numpy-deflections-p2
- summary: |
    Phase 2 of numpy-deflections-cpu: scipy.special.wofz on the numpy branch of the MGE
    Faddeeva, Gaussian.wofz deduped onto MGEDecomposer.wofz, numpy-only spherical MGE branch
    (removes the q=0.9999 clamp bias), exact exp_term mask; cache lever dropped (0.3 %).
    Re-pin of dark/stellar lens cells with mpmath provenance. Targets re-scoped to measured
    ceilings (gNFW ~2.3x, gNFWSph ~59x, Gaussian sph ~16x). Fable session; execution → Opus.

## ep-laplace-hessian
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1561
- prompt: active/ep_laplace_covariance_and_failed_update_projection.md
- issued: 2026-09-02
- status: library-dev
- epic: graphical-ep (fix wave 3/3: D1 #1558, D4/D5 #1560 merged → D2/D3; the phase-2 mechanism; ledger draft/research/graphical_ep/ep_campaign.md)
- worktree: ~/Code/PyAutoLabs-wt/ep-laplace-hessian
- parallel-claim: PyAutoFit also claimed by resampling-info-summary-section (web session, no worktree, disjoint files). Own worktree from origin/main 9eb808522.
- heart-ack:
  - PyAutoArray: open PR 10d old
  - release validation incomplete: no rehearsal for current source
- repos:
  - PyAutoFit: feature/ep-laplace-hessian
- summary: |
    D2: real Hessian at the Laplace mode (central FD of the tilted gradient,
    full inverse, marginal blocks; BAD_PROJECTION skip on non-concave/boundary
    modes; refine_state accumulates, n_refine=0 allowed). D3: failed line search
    returns last_dist with updated=False; precision guard before the divide;
    always-skipping factors reported stale. Acceptance: analytic_gaussian.py leg A
    mu std -> 4.11, bit-identical across prior ids, 0 BAD_PROJECTION on leg A.
    Fable session; implementation delegated to a Fable subagent.
