# Organ-named dashboard prompt headings

Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/479
Type: feature
Target: PyAutoBrain
Consequence: judge
Autonomy: supervised
Difficulty: large

## Overview
Apply the approved organ-named prompt headings across all 13 dashboards, retaining existing payloads, copy controls and work links. Parent initiative: PyAutoMind/draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md. Prior Brain blockers #469–#472 are closed and claims cleared.

## Plan
- Add shared, safely escaped heading markup and responsive single-line typography; bold only the organ name.
- Adopt in Brain/Mind/Cortex and ten other dashboard owners, preserving prompt/copy semantics and GitHub work links. Remove explanatory subtitles.
- Validate rendered desktop/mobile layouts, no horizontal overflow, copy behavior and owner suites; open one PR per affected repository.

Tier: judge — merge mode: human /prm

## Detailed implementation plan
Brain board/_theme.py: provide canonical organ heading helper and sizing; use it in orchestration_panel and the Brain, intake/Mind and Cortex renderers; document the contract in docs/board-orchestration.md.
Owner renderers: Ears ears/board.py and presentation.py; Heart heart/dashboard.py; Hands autohands/board.py; Memory scripts/board.py; Pulse pulse/campaigns.py; Insight insight/campaigns.py; Nerves scripts/board.py; Gut scripts/board.py; Eyes eyes/board.py; Scientist board renderer. Reuse the shared helper without changing prompts or per-board workflows. Regenerate tracked owner outputs when required. Test headline escaping and rendering, preserve copy payloads, check 320/375/768/1440px geometry and representative copy actions.

Branch survey: all eleven owner repos on main; clean except unrelated untracked Eyes dataset/, output/, scripts/ directories, preserved in canonical checkout. Separate clean worktrees created at .worktrees/organ-prompt-headings/<Repo> on feature/organ-prompt-headings. Brain owns Mind/Cortex rendering, so these do not require source claims in Mind/Cortex.

## Approved wording and original request
 — requested 2026-10-05

Replace generic panel headings with concise action sentences containing the organ name in bold. No explanatory subtitle. Cover all dashboards and validate mobile/desktop line length without horizontal overflow. Mind quoted subtitle is absent from the live HTML as verified during this request. Wording approved in session; user then instructed “ok go”: Brain — Plan your next move with your Brain; Mind — Put your Mind to work; Cortex — Explore science with your Cortex; Ears — Use your Ears to hear the community; Heart — Keep your Heart healthy; Hands — Ship with your Hands; Memory — Build your Memory; Pulse — Check your Pulse; Insight — Find your next Insight; Nerves — Check your Nerves for config drift; Gut — Clear out your Gut; Eyes — Review figures with your Eyes; Scientist — Work with your Scientist.

Original request (verbatim):

At the top of mind "Plan and coordinate devleopment" button is good, remove the text "Review the task queue, choose
priorities and carry accepted work through the development workflow." as this again is just elling me what I aleady know.
instead of "Plan and coordinate development" be more direct what the prompt does or link it to Mind. It could
be "Do some tasks on you Mind". For ears it could be One chat. The whole
community. -> "Use your Ears to listen to the community". I want each setense to be concise, span one line, but use the
organ name to remind us where we are. The organ name should be in bold.   Then do this across all dashboards, thinking carefully aobut how the organ name makes its way into the text.

Heading implementation checkpoint — 2026-10-05: wording approved, including “Explore science with your **Cortex**”. Entry Heart verdict STALE (PyAutoNerves rehearsal source drift). Worktree conflict guard blocks PyAutoBrain: active issues #469/#470/#471/#472 (worktree-sh-root-activate-clobber, unregistered-worktree-guard, cortex-find-script-symlink, intake-declared-header-fields). No source edited or worktree created. Git fetch is unavailable in this restricted session (github.com DNS resolution failure); this checkpoint is local, not pushed. Resume the approved heading work after the Brain claims clear; do not ask for wording approval again.

Resume verification — 2026-10-06: GitHub access restored; fetched Mind before editing and preserved all five saved local files. Issues #469–#472 remain OPEN; current active.md and worktree_check_conflict confirm all four Brain claims. Heading implementation remains blocked; approved wording persists. Heart entry reports STALE (release STALE, monitoring RED). Publication verification: Hands run 37363739823, Eyes run 37363681281 and Insight run 37363693166 all completed with failure and cancelled deployment jobs. No later publication runs were present. Live Pages HTML still contains the removed Hands relationship paragraph, Eyes introduction/tutorial and Insight check-in/ledger guidance. The merged prose cleanup is not yet live; verification did not rerun deployments.
