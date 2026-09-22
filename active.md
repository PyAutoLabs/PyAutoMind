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
- summary: Approved Abell 1201 preparation/smoke implementation; full posterior budget and science validation remain checkpoints. Development-only Heart RED override and public processed-data redistribution authorised on 2026-09-22. Shipping stopped at failed clone-boundary check; no assistant push or PR.
- heart-red-override:
  - authorization: User "continue i suthorize" in direct response to development-only shipping override for issue #133; no release, merge, posterior run or CI bypass.
  - red-reasons: "release validation FAILED (stage integrate)"
  - passed: 129 tests at refreshed head 79854cc; refreshed data preparation, finite coarse likelihood smoke and freeze-check pass.
  - blocked: clone-boundary check rejects scripts/abell_1201/README.md as unclassified; override cannot bypass this failure. Requires coordinated assistant template-policy and Brain clone-profile classification.
- latest-shipping-attempt: Local head 79854cc records user permission ("yeah do it") to publish supplied processed data with Nightingale et al. (2023)/HST credit. No assistant push or PR; earlier resume below is the pre-override checkpoint.
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
## vis-lp-inspection-bundle
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/102
- issued: 2026-09-22
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Plan approved. Issue #102 filed. Implement and test in the isolated workspace, then ship and refresh the existing catalogue without rerunning fits.
