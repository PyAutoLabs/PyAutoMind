# Starter organ navigation

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
- Plan/worktree approval still pending. Tier judge; source merge by human /prm. No science or collection.
