# Active Tasks

## search-ext-a1-declare-gate
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1674
- issued: 2026-10-08
- prompt: active/search_extensibility_a1_declare_gate_registry.md
- epic: search-extensibility (phase A1)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-shipped + workspace-shipped, awaiting-merge — 4 PRs opened 2026-10-08 under --auto (decide-and-flag, `decision-taken` on #1675); merge PyAutoFit#1675 first, the three docs PRs after RTD latest rebuilds
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1675
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/778
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/653
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/116
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1675
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/778
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/653
- validation: 3409 passed / 2 skipped / 9 xfailed; nojax 1192 passed; Sphinx 30 warnings = baseline in full and emulated-minimal envs; downstream suites green; afT BlackJAXNUTS/MultiStartAdam accuracy asserts fail identically on main
- decision-taken: factor-graph backend rules (use_jax=None derives from factors; agreement check after the test-mode bypass; gradient_mode disagreement → reverse); judgement values for status/warm_start/resumable/batched listed in the PR
- autonomy: --auto launch 2026-10-08 ("do A1 and B2 auto"); effective supervised (feature@large); ship checkpoint = decide-and-flag; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a1-declare-gate
- repos:
  - PyAutoFit: feature/search-ext-a1-declare-gate
  - PyAutoLens: feature/search-ext-a1-declare-gate
  - PyAutoGalaxy: feature/search-ext-a1-declare-gate
  - PyAutoCTI: feature/search-ext-a1-declare-gate
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## search-ext-b2-harness
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/2
- issued: 2026-10-08
- prompt: active/search_extensibility_b2_harness_protocol.md
- epic: search-extensibility (phase B2)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: workspace-shipped, awaiting-merge — autofit_inference#3 opened 2026-10-08 under --auto (decide-and-flag, `decision-taken`); first run of lint.yml + witness.yml on GitHub pending
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/3
- validation: 46 tests; ruff clean; build_readme/export/WALL --check pass; local witness run accepted; Insight check --offline validates the fixture; numpy Nautilus reference ×3 agrees to 0.019 nat / 0.015σ; DynestyStatic ln Z scatters 2.3 nat at default walks=5 (limitation, pilot item); JAX Nautilus refs and separated refs pending → B3
- decision-taken: constant-likelihood validation rerun at n_live=2000 after n_live=500 measured −1.972 outside the ±0.1 window; both attempts kept
- autonomy: --auto launch 2026-10-08; effective supervised (feature@large); ship checkpoint = decide-and-flag; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b2-harness
- repos:
  - autofit_inference: feature/search-ext-b2-harness
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## board-one-click-update
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/504
- issued: 2026-10-08
- prompt: active/board_one_click_update.md
- session: Codex CLI, session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-one-click-update
- repos:
  - PyAutoBrain: feature/board-one-click-update
- tier: judge (human /prm)
- approval: user approved shared authenticated Update service with "ok do it"
- next: awaiting hosting preference after explaining setup; local service prototype preserved, shared button integration and shipping incomplete

## pyautobroca-assistant-management
- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/1
- issued: 2026-10-08
- prompt: active/assistant-management-organ.md
- session: Codex CLI (GPT-6), session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautobroca-assistant-management
- approval: user approved Broca and execution; explicitly allowed coordinated Brain/Mind changes preserving other tasks
- tier: judge (human /prm)
- repos:
  - PyAutoBroca: feature/pyautobroca-assistant-management
  - PyAutoBrain: feature/pyautobroca-assistant-management
  - PyAutoMind: feature/pyautobroca-assistant-management

- validation: Broca 18 passed; Brain 1252 passed; Mind 696 passed; ten browser checks passed
- artifact: .worktrees/pyautobroca-assistant-management/PyAutoBroca/dashboard.html
- evidence: 14 historical AutoLens benchmark runs and four maintenance inventory records; no new paid benchmark campaign
- heart: YELLOW; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- heart-stale: release validation incomplete: no rehearsal for current source
- next: human /prm in order Mind #495 → Brain #511 → Broca #2; recheck exact-head CI after dependencies land, then regenerate other-organ instruction surfaces

- heart-ack: user explicitly acknowledged exact YELLOW manifest-drift reason and authorized PR publication on 2026-10-08; no merge/release authority
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/495
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/511
- library-pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/2
- heads: Mind 11196551; Brain 0b4471de; Broca 296225e
- limits: private local board; no Pages deployment or scheduled refresh; no new response-quality campaign; raw historical transcripts remain in original sources
