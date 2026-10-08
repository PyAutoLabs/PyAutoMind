# Active Tasks

## search-ext-b1-registration
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/492
- issued: 2026-10-07
- prompt: active/search_extensibility_b1_registration.md
- epic: search-extensibility (phase B1 registration)
- session: Claude CLI (Fable 5.1, /start_dev); https://claude.ai/code/session_01QJmrnXNQdq6HSruUt3MqVW
- status: workspace-shipped, awaiting-merge — 5/7 MERGED 2026-10-07 by human /prm (autofit_inference#1, autofit_profiling#1, Mind#493 ba34fdb5, Cortex#60, Pulse#33); OPEN: Heart#292 (red on the pre-existing Brain#499 markdown-link test break — bug draft draft/bug/pyautoheart/dashboard_markdown_link_test_broken_by_brain_499.md) and .github#34 (no CI configured; needs the human's explicit merge OK). RAL clones pulled. Resume: fix the Heart bug → re-run #292 → /prm both → close-out
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b1-registration
- repos:
  - autofit_inference: feature/search-ext-b1-registration
  - autofit_profiling: feature/search-ext-b1-registration
  - PyAutoMind: feature/search-ext-b1-registration (coordination authorised by the human 2026-10-07 with mind-dashboard-simplify #491: repos.yaml, ROUTING.md, epics.md only)
  - PyAutoHeart: feature/search-ext-b1-registration
  - PyAutoCortex: feature/search-ext-b1-registration
  - PyAutoPulse: feature/search-ext-b1-registration
- tier: judge (human /prm)
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/1
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/1
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/493
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/292
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/60
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/33
- workspace-pr: https://github.com/PyAutoLabs/.github/pull/34
- heart-ack: manifest drift: workspace checkouts (manifest ↔ disk) — 2 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source — acknowledged by the human 2026-10-07 at ship
- summary: minimal lint-green skeletons for both new fit repos; Mind repos.yaml rows + repos_sync --write; Heart excluded; Cortex planned row; Pulse task adoption (no registry rows at B1); org profile rows; RAL clones. Clears Heart manifest-drift YELLOW.
