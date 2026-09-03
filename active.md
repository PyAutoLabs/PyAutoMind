# Active Tasks

## batch-status-box
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/341
- prompt: active/batch_board.md
- issued: 2026-09-02
- session: claude --resume session_01VsKeuX83FNGjLqs2axLHeR
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/batch-status-box
- repos:
  - PyAutoBrain: feature/batch-status-box
  - PyAutoCortex: feature/batch-status-box
  - PyAutoMind: feature/batch-status-box
- epic: two-slot-batching (phase 6; parent draft/feature/pyautomind/two_slot_batching_epic.md)

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

## over-sample-snr-double-division
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/523
- prompt: active/over_sample_snr_double_division.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01UpLMvgejg1kNXbG3P789wy
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/over-sample-snr-double-division
- repos:
  - autolens_workspace (feature/over-sample-snr-double-division)
  - autolens_workspace_test (feature/over-sample-snr-double-division)
  - autolens_assistant (feature/over-sample-snr-double-division)

## image-source-mappings-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/525
- prompt: active/mappings_guide_and_tutorial_rewrite.md
- issued: 2026-09-03
- session: claude --resume 7edd9743-c486-48ec-be0a-9f184a4898d4
- status: workspace-dev
- epic: image-source-mappings (phase 3 — ledger draft/feature/autoarray/image_source_mappings_epic.md; opened 2026-09-03 by user decision ahead of the PyAutoArray/PyAutoLens releases that gated it; every PR carries pending-release)
- heart-ack:
  - "release validation FAILED (stage integrate)"
  - "PyAutoArray: open PR 11d old"
- worktree: ~/Code/PyAutoLabs-wt/image-source-mappings-p3
- parallel-claim: autolens_workspace — over-sample-snr-double-division (#523) in its own worktree; touches SLaM scripts, guides/advanced/over_sampling.py and guides/modeling/slam_start_here.py only; file sets disjoint
- repos:
  - autolens_workspace: feature/image-source-mappings-p3
  - HowToLens: feature/image-source-mappings-p3
  - HowToGalaxy: feature/image-source-mappings-p3
  - autogalaxy_workspace: feature/image-source-mappings-p3
- summary: |
    Phase 3 of image-source-mappings (workspace). New guide autolens_workspace/scripts/guides/mappings.py
    (point → parametric region → pixelized region mappings with the 0.2/0.5/0.8 clump threshold demo,
    subplot_mappings, 4MOST brightest-position recipe with guide-level astropy WCS, magnification per image);
    HowToLens/HowToGalaxy tutorial_2_mappers rewritten to draw polygons via mapper.mappings_from + regions=,
    BUGGY line dropped; dead slim_indexes_for_pix_indexes sections in the pixelization delaunay.py /
    likelihood_function.py scripts fixed; prose + total_mappings_pixels config sweep. One issue, four PRs,
    one worktree. Fable session; execution delegated to Opus (subagent A guide, subagent B tutorials/dead sections).
