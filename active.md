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
- resume: Preparation/smoke checkpoint complete at local assistant commit 9251b40; 129 tests passed. Approved F390W power-law + shear + point mass, nuisance parameters fitted, cleaned inputs with exact processed 4 arcsec support (31417 pixels). Bundled data manifest, separate RGB, setup-only benchmark card/scorer, model builder and opt-in future posterior driver prepared. Finite 12x12-source likelihood smoke passed; no posterior or headless benchmark run authorised/executed. Pre-removal originals deferred; retain/disclose cut-out, no inpainting. Await full-run budget and scientific calibration; units/redistribution still to confirm before publication. Assistant branch local/unpushed: Heart RED, release validation FAILED (stage integrate), no override. Issue #133 tracks progress; artifacts under scripts/scratch/abell_1201. Originals untouched.

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
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inspection-missing-assets
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/inspection-missing-assets
- summary: PR #101 open at 3e5357d; Heart development override authorized and recorded. 249 fast tests/26 regressions, catalogue smoke and independent review CLEAN. Eleven tooling files deployed with checksum guards; catalogue-only RAL job 350452 submitted; product verification pending.
- resume: Check RAL job 350452, verify bundle using .scratch/verify_bundle.py against .scratch/ral-before-products.json, report FITS/CSV/PNG counts and skips. PR #101 merge remains human. Existing science dirt/data preserved.
- heart-red-override: |
    User: "Authorize issue #100 development override". Heart RED: `release validation FAILED (stage integrate)`. 249 fast tests, 26 targeted regressions, ten-stage catalogue smoke, Ruff/format/diff checks PASS; independent Sol review CLEAN. Commit/push/pending-release PR only; deployment/catalogue rerun separately authorized by approved plan. No merge or release.
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/101
- catalogue-job: 350452
