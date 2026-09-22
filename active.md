# Active Tasks

## abell-1201-point-mass
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/133
- issued: 2026-09-22
- prompt: active/add_an_abell_1201_central_point_mass.md
- session: Codex (session ID unavailable)
- status: awaiting-input
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/abell-1201-point-mass
- repos:
  - autolens_assistant: feature/abell-1201-point-mass
- summary: Human approved plan and branch on 2026-09-22. Inspect supplied F390W/F814W data, obtain mask/contaminant confirmation before composing fit, freeze baseline and point-mass inference, add benchmark and website image. Full-run compute budget and scientific inputs remain checkpoints. Heart RED is not overridden.
- resume: Human approved existing contaminant-removal images and exact processed ~4 arcsec boundary. prepare_dataset.py successfully loads both cleaned image/noise pairs with identical 31417-pixel support and PSF sums 1; no fit run. Inspection/presentation/preparation scripts locally committed. Pre-removal originals explicitly deferred by human on 2026-09-22; use available images for presentation, retain/disclose cut-out, no inpainting. Await baseline/prior/reference specification and run budget; units/redistribution still to confirm. Previews under scripts/scratch/abell_1201. Issue #133 has progress. Assistant branch local/unpushed; Heart RED not overridden. Originals untouched.

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

## inspection-missing-assets
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/100
- issued: 2026-09-22
- prompt: active/inspection_missing_assets.md
- session: Codex (session ID unavailable)
- status: awaiting-input
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inspection-missing-assets
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/inspection-missing-assets
- summary: PAUSED at explicit user request (going offline). Local implementation on approved branch; 241 fast tests passed/10 fitting tests deselected. Independent review FINDINGS: collector validates existence only, stale multi-wavelength PNG on incomplete refresh, stale Witt-Wynne CSV/in on skip. No deployment/jobs; Heart RED not overridden.
- resume: Fix the three independent review findings documented in active/inspection_missing_assets.md and issue #100; update staged .scratch/deploy overlay, rerun affected tests and independent review, then address Heart shipping gate. User plan remains approved; wait for user to resume. Science dirt/data untouched.
