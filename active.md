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

## analytic-gaussian-benchmark
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91
- prompt: active/analytic_gaussian_benchmark.md
- issued: 2026-09-02
- status: pr-open, awaiting-merge (CI running; merge via /prm)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/92
- heart-ack:
  - PyAutoArray: open PR 10d old
  - release validation incomplete: no rehearsal for current source
- epic: graphical-ep (phase 1 — the keystone; ledger draft/research/graphical_ep/ep_campaign.md)
- worktree: ~/Code/PyAutoLabs-wt/analytic-gaussian-benchmark
- repos:
  - autofit_workspace_test: feature/analytic-gaussian-benchmark
- summary: |
    Closed-form conjugate hierarchical Gaussian benchmark (known-scatter leg
    analytic, unknown-scatter leg exact by quadrature) vs a minimal hand-rolled
    EP vs autofit EP (Laplace) and graphical joint fit; prior-family sweep and
    the phase-2 collapse configuration. Home autofit_workspace_test/scripts/
    graphical/ (analytic_*.py); analytic_gaussian.py curated into the smoke
    gate. PyAutoFit read-only (claimed by two other tasks); defects file as
    bug prompts. Fable session; execution delegated to Fable subagents.

## numpy-deflections-p1
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/514
- prompt: active/numpy_deflections_p1_sph_decorator_tracer.md
- issued: 2026-09-02
- session: claude --resume d3971bba-0e8d-4c4f-bc59-7808e6bfa6cd
- status: library-dev
- epic: numpy-deflections-cpu (phase 1 — ledger draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md)
- worktree: ~/Code/PyAutoLabs-wt/numpy-deflections-p1
- heart-ack:
  - PyAutoArray: open PR 10d old
  - release validation incomplete: no rehearsal for current source
- parallel-claim: PyAutoArray — numba-vs-jax-sparse holds a read-only research claim on main (no branch, no worktree); file sets disjoint, own worktree approved by the human 2026-09-02
- repos:
  - PyAutoArray: feature/numpy-deflections-p1
  - PyAutoGalaxy: feature/numpy-deflections-p1
  - PyAutoLens: feature/numpy-deflections-p1
  - autolens_profiling: feature/numpy-deflections-p1
- summary: |
    Phase 1 of numpy-deflections-cpu: land autolens_profiling/scripts/lens/deflections/
    (nine numpy mass-profile deflection cells, hst + euclid, pins), commit the baseline,
    then the two zero-numerics levers — GridMaker.via_grid_2d no longer fires
    Grid2D.over_sampled on *Sph calls (+ sub-size-1 short-circuit) and the tracer /
    galaxy double trace at sub-size 1. Fable session; execution delegated to Opus.

## image-source-mappings-p1
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/515
- prompt: active/mappings_regions_clumps_subplot.md
- issued: 2026-09-02
- session: claude --resume e962a3a7-cee9-4168-93a5-e7067699f2d7
- status: library-dev
- epic: image-source-mappings (phase 1 — ledger draft/feature/autoarray/image_source_mappings_epic.md)
- worktree: ~/Code/PyAutoLabs-wt/image-source-mappings-p1
- parallel-claim: PyAutoArray — numpy-deflections-p1 (#514) holds it in its own worktree; file sets disjoint (this task: autoarray/inversion/, autoarray/plot/, config/visualize/; theirs: grid over-sampling decorator + tracer path); own worktree approved by the human 2026-09-02
- repos:
  - PyAutoArray: feature/image-source-mappings-p1
- summary: |
    Phase 1 of image-source-mappings: new autoarray/inversion/mappings/ package
    (Mapping / ImageRegion result objects, mesh-graph connected components, image-plane
    regions from the mapping matrix, arcsec boundary polygons), Inversion.source_clumps_from
    + mappings_from, Mapper.mappings_from, a regions= overlay on plot_array /
    plot_inversion_reconstruction, and subplot_mappings rewritten as the one-look 2x2
    mapping figure. Fable session; execution delegated to Opus.

## adapt-image-snr-cap
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/521
- prompt: active/adapt_image_snr_cap.md
- issued: 2026-09-02
- session: claude-code-cli (Fable architect, Opus execution)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/adapt-image-snr-cap
- repos:
  - autolens_workspace: feature/adapt-image-snr-cap
  - autolens_assistant: feature/adapt-image-snr-cap
