# Active Tasks

## sersic-variants
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/74
- issued: 2026-09-12
- prompt: active/sersic_variants_prior_edge.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: paused
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/75
- note: "PR #75 was closed unmerged at the maintainer's request on 2026-09-18. The feature branch, issue #74, prompt and worktree are retained for possible later recovery or selective reuse. Its previous overlap with sed-chain-cpu-route is no longer live because PR #70 merged the CPU-route change."
- summary: |
    --variant for the Sersic stage: four variants (baseline, wide_n,
    central_noise, sersic_point) on the same 100 euclid_sersics core lenses, to
    explain the lens-light Sersic index pile-up at the n = 5 prior edge. The
    inline model block in fit_sersic is extracted into a pure sersic_model_from
    helper; variant=None stays byte-for-byte today's behaviour and any other
    variant writes to unique_tag sersic_lens_model_<variant>. util gains a pure
    Gaussian noise-inflation helper (A = 9, sigma = 0.17") plus a keyword-only
    noise_inflation on load_vis_dataset, and parse_fit_args(with_variant=True).
    New hpc/batch_cpu/submit_sersic_variants runs the four variants sequentially
    inside one array task per lens, because all four restore the same vis_lp zip
    and PyAutoFit's restore() deletes it. Science-clone submit and the analysis
    script (PR 2) are follow-ups.

## sersic-variants-analysis
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/76
- issued: 2026-09-12
- prompt: active/sersic_variants_analysis.md
- session: https://claude.ai/code/session_01LfJojDFow4pxPzuwRHqMt2 (web-github resume 2026-09-17; planned 2026-09-12 in session_01KTGhZacWuxrxYkXXWXJbBx)
- status: workspace-dev
- worktree: n/a — web-github session clone (/home/user/euclid_strong_lens_modeling_pipeline); the local ~/Code/PyAutoLabs-wt/sersic-variants-analysis worktree named on 2026-09-12 never pushed feature/sersic-variants-analysis, so the branch of record is the session's
- repos:
  - euclid_strong_lens_modeling_pipeline: claude/sersic-variants-analysis-3iqibr
- resume: "IMPLEMENTED 2026-09-17 (web-github; Fable planned, Opus executed): claude/sersic-variants-analysis-3iqibr pushed at 480c107 — scripts/analysis/{sersic_variants.py,README.md,__init__.py}, tests/test_sersic_variants_analysis.py (8 tests), one config/build/no_run.yaml entry. Verified locally: the new tests + test_repo_invariants + test_compare_catalogues, 26 passed; the rest of the fast suite needs astropy/autolens (absent in the container) — CI runs it. FLAGGED on issue #76 comment 5715176814: the W1-W4 thresholds are transcribed into the module's WITNESSES constant (plan page rev 3 unreachable from the session) and need the human's confirmation. NEXT = /ship_workspace (PR) then /prm; nothing here imports --variant, so PR #75's merge order is not a gate."
- note: "The earlier conflict survey named sed-chain-cpu-route PR #70 and sersic-variants PR #75. PR #70 merged on 2026-09-18 and PR #75 was closed unmerged at the maintainer's request; neither branch's file set intersects this task, which adds only scripts/analysis/**, tests/test_sersic_variants_analysis.py and one config/build/no_run.yaml entry."
- summary: |
    PR 2 of the euclid_sersics variants work: scripts/analysis/sersic_variants.py
    reads the four lens_sersic_<variant>.csv scrapes that PR #75's --variant
    produces and emits the per-variant comparison production needs - N, median n,
    fractions above 4.5/4.9/9.5 (and 5.0 for wide_n), paired dn and dR_eff against
    baseline with 16-84 % bands, June-vs-baseline dn from sample/lens_map.csv, and
    the four witness readings W1-W4 printed as numbers beside their pre-registered
    thresholds, never as a verdict word. Four-panel shared-bin histogram PNG plus a
    markdown report. Pure functions split from the CLI; a synthetic four-CSV
    fixture with a variant missing two tiles pins the inner join and its reporting.

## hst-gpu-residue-p2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/273
- issued: 2026-09-16
- prompt: active/hst_gpu_residue_p2_vmap_vs_jit_and_batched_callback.md
- session: claude --resume 51243072-d1a4-437b-b5a6-edf3bff12db4
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hst-gpu-residue-p2
- repos:
  - autolens_profiling: feature/hst-gpu-residue-p2
- parallel-claim: "autolens_profiling was also claimed by fixed-light-numba-levers (#267, COMPLETE 2026-09-16, merged and closed out; worktree removed): its files are fixed_light_numba*, fixed_light_numpy_solvers.py, the lever submits/results and fixed_lens_light_levers_2026_09.md; this task touches fixed_light_trace.py, a new host_callback_probe.py, library_solver_injection.py, a new vmap submit + results + note — disjoint, own worktree beside it exactly as phase 1 (#268) did."
- note: "Phase 2 of hst-gpu-non-solver-residue, STEP 1 ONLY (matched vmap-vs-jit A100 experiment + policy; PyAutoArray batch-aware callback deferred to phase 2b via /intake if the numbers warrant). Fable session plans, Opus executes. A100 submit -> wait -> harvest is a human resume point. Heart RED (install verify testpypi F; release integrate) at start; PR-open needs the human's ack. Phase-1 worktree ~/Code/PyAutoLabs-wt/hst-gpu-residue-p1 still awaits the human's cleanup (3 untracked .err -> worktree_remove -> branch -d)."
- hpc: "A100 array 343376 tasks 0-4 SUBMITTED 2026-09-17 00:10 BST from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 @ bf52147 (B16 distinct fb-on / B16 fb-off / B8 / B4 / B16 identical control); all 5 RUNNING on euclid-ral-gpu-1/2 at submit. HUMAN RESUME POINT: when done, harvest = commit the 5 results/breakdown/imaging/fixed_light_trace_delaunay_vmap*_hpc_a100_fp64_*.{json,png} in the RAL worktree, fetch locally (git fetch euclid_jump:/mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 feature/hst-gpu-residue-p2), check AUTOTUNE_ENTRIES count=0 + unjoined 0 + lane pins PASS in hpc/batch_gpu/output/output.343376_*.out, then Phase C (note + errata + README + ship). Phase A on the issue: #273 comment 2026-09-17."

## grid-offset-prior
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/88
- issued: 2026-09-17
- prompt: active/datasetmodel_grid_offset_prior_0_2_clips.md
- session: claude --resume 7bff8610-4b84-413a-a994-d72484c4c14c
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/grid-offset-prior
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/grid-offset-prior
- note: "The 2026-09-17 conflict survey named five claims. Since then sed-chain-cpu-route PR #70 merged and sersic-variants PR #75 closed unmerged; sersic-variants-analysis #76, simulator-from-result-linear #77 (parked) and witt-wynne-catalogue #84 remain relevant. Code file sets are disjoint except catalogue/README.md shares one hunk with witt-wynne-catalogue."
- note: "PAUSED 2026-09-17 17:10 BST, resumable. DONE on feature/grid-offset-prior (3 local commits d50eb52 prior ±0.5\" / 3563a98 prior_edge_y-x columns + header pin + tests / e58a1be README + eight producers; 208 fast tests green; NOT pushed, no PR). Witness done: sep1 Tile102008165 nir_j x 0.1906 [.., 0.2000] flagged → 0.2727 [0.167, 0.387] unflagged under ±0.5"; nir_h of that tile spins in Nautilus exploration (second case of 343381_8). RESUME: cd ~/Code/PyAutoLabs-wt/grid-offset-prior/euclid_strong_lens_modeling_pipeline; source ../activate.sh; pytest tests -q; /ship_workspace (Heart RED release-side → human ack); /prm; README one-hunk overlap with witt-wynne-catalogue #84. Full state on issue #88 comment."

## oneshot-benchmark-harness
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/126
- issued: 2026-09-17
- prompt: active/oneshot_benchmark_harness.md
- session: claude --resume session_01YTzjiXh2fLocc6dNqLQ66d
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/380
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/127
- autonomy: supervised (header; launched on the human's "Go / continue" in-session — plan on the issue, shipped to PR-open 2026-09-17, merge is human; Brain PR first, it is the assistant PR's `Brain-ref:`)
- location: web-github (session clones /home/user/autolens_assistant + /home/user/PyAutoBrain, no task worktree)
- worktree: n/a — web-github session clones
- repos:
- note: "PyAutoBrain PR #380 and autolens_assistant PR #127 merged; issue #126 is closed. Both repo claims are released. The entry remains active only for the first real headless runs noted below; do not fully close it as part of codex-hook-parity."
- summary: |
    One-shot, machine-scored assistant benchmarks: headless `benchmark.py run`
    (harnesses.yaml adapters, private workdir without benchmarks/truth, compute
    shims), computed-score contract (common gates × card metrics → score.json,
    RESULTS.md medians), prompt freeze (prompt_sha256 + VERSIONS.lock), first
    one-shot card `oneshot-smoke`, 2026-07 cards retired to prompts/conversational/,
    Brain clone VALIDATION_PLAN/partition update. Cards
    benchmark_positions_initialised_inference / benchmark_forward_model_consistency
    stay in draft/, Blocked-by this task. Real headless runs need a laptop with
    the agents installed — the human's first step after merge.

## community-surface-brain
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/405
- issued: 2026-09-19
- prompt: active/community-surface-brain.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/406
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/406
- validation: 72 community/board tests passed; independent review CLEAN.
- next: Review required GitHub checks, then human merge via /prm.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoBrain: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-policy
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/426
- issued: 2026-09-19
- prompt: active/community-surface-policy.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/427
- pending-release: PyAutoMind@https://github.com/PyAutoLabs/PyAutoMind/pull/427
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Review required GitHub checks, then human merge via /prm.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoMind: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-pyautolens
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/746
- issued: 2026-09-19
- prompt: active/community-surface-pyautolens.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/747
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/747
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoLens: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-pyautogalaxy
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/626
- issued: 2026-09-19
- prompt: active/community-surface-pyautogalaxy.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/627
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/627
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoGalaxy: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-pyautofit
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1639
- issued: 2026-09-19
- prompt: active/community-surface-pyautofit.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1640
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1640
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoFit: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-pyautoarray
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/562
- issued: 2026-09-19
- prompt: active/community-surface-pyautoarray.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/563
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/563
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - PyAutoArray: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-autolens-workspace
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/569
- issued: 2026-09-19
- prompt: active/community-surface-autolens-workspace.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/570
- pending-release: autolens_workspace@https://github.com/PyAutoLabs/autolens_workspace/pull/570
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - autolens_workspace: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-autogalaxy-workspace
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/247
- issued: 2026-09-19
- prompt: active/community-surface-autogalaxy-workspace.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/248
- pending-release: autogalaxy_workspace@https://github.com/PyAutoLabs/autogalaxy_workspace/pull/248
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - autogalaxy_workspace: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-autofit-workspace
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/161
- issued: 2026-09-19
- prompt: active/community-surface-autofit-workspace.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/162
- pending-release: autofit_workspace@https://github.com/PyAutoLabs/autofit_workspace/pull/162
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - autofit_workspace: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-website
- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/8
- issued: 2026-09-19
- prompt: active/community-surface-website.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/9
- pending-release: pyautolabs.github.io@https://github.com/PyAutoLabs/pyautolabs.github.io/pull/9
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Review required GitHub checks, then human merge via /prm.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - pyautolabs.github.io: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.

## community-surface-profile
- issue: https://github.com/PyAutoLabs/.github/issues/15
- issued: 2026-09-19
- prompt: active/community-surface-profile.md
- session: Codex (session ID unavailable)
- status: awaiting-input, PR-open
- workspace-pr: https://github.com/PyAutoLabs/.github/pull/16
- pending-release: .github@https://github.com/PyAutoLabs/.github/pull/16
- validation: Documentation/template checks passed; independent review CLEAN.
- next: Human configures answerable Proposals (slug proposals), then mark draft ready and review CI.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-surface
- repos:
  - .github: feature/community-surface
- note: Approved community-surface plan; shared worktree bundle, separate issue and PR per repository. No library API changes.
