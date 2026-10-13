# Starter organ navigation

Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/77
Difficulty: medium
Consequence: judge

## Original user request

I think it would be nice to have thew bar with all the icons (e.g. Scientist, Brain, Mind) which I currently use for navigation to be at the top in the place they appear normally. You should be able to click them and navigate to each board, but if they are not active it should just contain text explaining what the organ does, along with a copyable prompt to set it up with with AI. This would be the same text as under "Dashboards" but it helps build in the navigation early. Use ientical text for now, we will refine and update it as we go

## Scope

@PyAutoScientist: give opt-in independent instance previews persistent top organ navigation matching the existing pyautolabs.github.io cockpit icon/label order and placement. Scientist opens the overview. Explicitly connected organs open their configured boards; unconnected/setup-incomplete organs open an explanatory view with byte-identical existing Dashboards description and setup/resume prompt, with a copy control. Keep navigation visible, support direct links, Back/Forward and keyboard/mobile use. Do not connect or fetch inactive organs, or send independent users to maintainer boards. Reuse content from one owner-controlled source rather than duplicate prose.

Regenerate empty and connected PyAutoEmbryo static demos and tester download after source changes are accepted. Current deployment clone: organs/PyAutoMind/tmp/pyautoembryo-tryout-2026-10-13/PyAutoEmbryo-pages, main. Existing cockpit is a read-only visual reference; no main cockpit changes planned.

## Proposed implementation and validation

- scripts/organism_board.py and scripts/overview.js: instance-only shell/navigation; shared inactive-organ content payload used by both Dashboards and organ view; active-board URLs only from validated profile.
- Reuse Brain registry/icon conventions and existing cockpit navigation appearance; preserve normal Scientist rendering without an instance.
- Focused tests under tests/: available/setup/connected/paused routing, exact content parity, escaping and no inactive network requests.
- Browser checks: empty and example-connected profiles, desktop/mobile, keyboard, copy prompts, deep links and Back/Forward. Connected-board tests use local synthetic targets.
- Plan approved by human; isolated worktree created. Tier judge; source merge by human /prm. No science or collection.

## Implementation handoff — 2026-10-13

- Source PR: https://github.com/PyAutoLabs/PyAutoScientist/pull/78; commit `ba97db9881d784ecf01fe8ac974f73a1e34b63a9`.
- Worktree `.worktrees/starter-organ-navigation/PyAutoScientist`, branch `feature/starter-organ-navigation`, clean.
- Added instance_navigation.py/.js; integrated shared inactive content into organism_board.py; updated STARTER.md; added renderer and browser regression coverage.
- 146 Python tests, 7 Node checks, 30 browser cases passed. Browser covers five widths/light-dark, exact clipboard text, zero inactive requests, configured/paused destinations, history/focus and banner clearance; no-JS text checked. Independent review not claimed.
- Logs/screenshots/generated demos: `organs/PyAutoMind/tmp/starter-organ-navigation/`; Python/Node logs at `organs/PyAutoMind/tmp/starter-organ-navigation-{tests,node}.log`.
- Heart STALE: `release validation incomplete: no rehearsal for current source`; no red/yellow reasons. Development PR permitted; no release readiness claimed.
- Source CI was in progress when judged. Judge tier requires human /prm.
- Generated `pages-candidate/` contains index, connected/empty pages, README and refreshed ZIP. `publication-candidate.json` records hashes and destination checkout. Live site remains at the initial published preview.
- Next: merge #78 once exact-head CI is green; publish these artifacts to PyAutoLabs/PyAutoEmbryo using the already authorized static-only Pages route, then verify live navigation and ZIP. Existing static publication exception is recorded; do not run science/activate organs.
