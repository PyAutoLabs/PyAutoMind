# Organ-named dashboard prompt headings

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/479
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/481
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/14
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/286
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/302
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/117
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/16
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/7
- workspace-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/187
- workspace-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/23
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/19
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/44

All eleven PRs merged with every CI run and matrix job green (22 jobs). Per-repository git ancestry proves every task branch is contained in origin/main. Brain merged first, then consumers tested against the merged helper. The human acknowledged the named Heart YELLOW reason set and explicitly authorized /prm on 2026-10-06.

All thirteen dashboards now have source support for their approved concise action headings with only the organ name bold. Shared escaped heading markup and responsive typography preserve domain prompts, copy controls and work links; explanatory panel subtitles are absent. Brain's long task labels fit 320px columns. Consumer-generated pages refreshed where tracked.

Validation: all affected suites; strict docs; 104 rendered board/viewport/theme cases at 320/375/768/1440px without horizontal overflow; 14 clipboard/layout cases plus denial, budget, isolation and pending-edit witnesses. Eyes checked all 265 PNG URLs, 265 preserved copy payloads and 554 preserved links. Hands/Memory/Nerves/Gut payloads and links identical on the same input snapshots. The local Brain grouped-path fixture required inherited overrides removed; its rerun and both complete remote Python matrices pass.

This completes only the organ-named heading phase. The parent standardize_dashboard_orchestration_prompt_panel.md retains broader orchestration adoption and generated standards-discovery work; do not retire that parent on heading evidence.

Publication: previously merged prose cleanups Hands#301, Eyes#18 and Insight#6 are now verified live; removed prose absent on all three sites. All thirteen live Pages dashboards verified with exact approved text and only the organ name in strong emphasis on 2026-10-06. Successful manual refresh jobs: Cortex 37468432096; Heart 37468435968; Hands 37468440200; Nerves 37468444594; Gut 37468449113; Scientist 37468453423. Other boards published through their normal merge-triggered workflows. Evidence and screenshots remain in tmp/organ-prompt-headings/ (not committed).

Reconciliation: retained the broader orchestration/standards parent, appended the heading completion link, and cleared the sizing-none-triage-rules blocker. Intake flagged unrelated batch_slice.md on resemblance only; retained, with follow-up `/intake reconcile draft/feature/pyautobrain`. No irreplaceable ignored data products in the task worktrees; synthetic fixtures retained under tmp/organ-prompt-headings/.

## Original prompt

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

## Implementation checkpoint — 2026-10-06

Eleven local commits complete; awaiting Heart YELLOW acknowledgement before source push and PR creation. No merge or release authorization. The shared Brain PR must merge before consumer CI is rerun against Brain main. Validation and prepared PR descriptions: `tmp/organ-prompt-headings/`.

- PyAutoBrain: `9afc57e7f87ab9ab362ef11cdda1f552fdd9a28e`
- PyAutoEars: `56a9907bb946d7578ff05e06bdd53870e67bd307`
- PyAutoHeart: `7567628d6564ab27e24dca01a72903d03474a4c1`
- PyAutoHands: `edded79105d1ba88deb25f7ffaf0fdec722ce53d`
- PyAutoMemory: `aacd6a92598847fbe791f6288771bb650567e689`
- PyAutoPulse: `2a1b694de5c75e0096838ed34fc24eae7201c297`
- PyAutoInsight: `a6a9681161fef508f099c768f783192ace347c33`
- PyAutoNerves: `89c7d748899eb7eed6231cbc15d6ac512e828c1f`
- PyAutoGut: `ca019d84644f8916956c92abb773b79869f4785d`
- PyAutoEyes: `78d141a507bb347d3dd5af96d8f2ce7102fe3674`
- PyAutoScientist: `bd898e1d76a89a1c0b4c8203919bd2517a98a1ad`

Validation: all consumer suites passed; Brain 1232 passed plus one grouped-path fixture rerun passed with inherited environment overrides removed (all four grouped tests pass). Strict docs, 104 browser layouts, 14 shared copy cases, owner data/link invariance and Eyes 265 live PNG URLs pass.

Publication: Hands later run 37437902439 succeeded and removed prose is absent live. Eyes 37363681281 and Insight 37363693166 remain failed latest publication runs; old prose remains live. No deployments initiated.
