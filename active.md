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

## euclid-single-rgb-vis-lp
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/98
- issued: 2026-09-20
- prompt: active/single_rgb_dr1_vis_lp_pilot.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/99
- heart-red-override: User authorized issue #98 development override in this session: "Authorize issue #98 development override" in response to commit, push, pending-release PR, and RAL deployment for this branch. Heart RED: `release validation FAILED (stage integrate)`. Final branch gates: 223 fast tests passed (10 deselected); 37 focused tests passed; Euclid smoke 9/9 passed; Ruff check/format and diff check passed; real DR1 JPG rendered to two-panel `rgb.png`; review faculty surface at f28e3cf judged CLEAN. Development shipping only; no merge or release.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/euclid-single-rgb-vis-lp
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-single-rgb-vis-lp

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
