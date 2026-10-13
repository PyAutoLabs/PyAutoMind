# Match the independent starter to the cockpit shell

Difficulty: medium
Consequence: judge

## Original user request

Can we make it look the same as my cockpit, so it should have the PyAutoLabs / Cockpit link but say MyScientist / Cockpit, the icons should now have a scroll bar, it should have the same bar and format at the top but instead of YELLOW it should just be a greyed out button and say a word to imply its awaiting work   and also have the Scientist board Reload / New tablt thing.

## High-level plan

- Match the existing cockpit's three-row shell: identity/status, horizontally scrollable icons, selected-board toolbar.
- Show MyScientist / Cockpit for the demo, derived from instance-owned identity. Use a grey disabled IDLE status button for this starter shell, meaning awaiting work, not a health verdict.
- Keep a visible horizontal scrollbar/scroll affordance for organ navigation; preserve touch and keyboard access and the existing organ order.
- Add the selected board name plus Reload / New tab controls. Connected organs target their configured board; Scientist and inactive-organ views remain local. Keep descriptions and setup prompts unchanged.
- Preserve the familiar full-width shell and independent board-content scrolling, and verify desktop/mobile, light/dark, deep links/history, reload/new-tab destinations and clipboard behavior.
- Prepare regenerated PyAutoEmbryo pages and tester download. Tier: judge — merge mode: human /prm before publishing.

## Detailed implementation plan

@PyAutoScientist is the sole source repository. Use pyautolabs.github.io/cockpit/index.html as the read-only appearance/interaction reference; do not change the existing cockpit. Extend scripts/instance_navigation.py/.js and the instance-only wrapper in scripts/organism_board.py. Scope shell CSS to independent profiles and preserve unprofiled rendering. Keep configurable identity/destinations and inactive-feed isolation.

Add focused coverage in tests/test_instance_navigation.py and tests/navigation_browser.cjs for the three-row order, IDLE label, horizontal scrolling, selected-board toolbar, reload destination, new-tab destination, history, no unexpected external requests, and no overlap/whole-page overflow. Update STARTER.md only for the new shell/control behavior.

Survey: Scientist main is clean at 921d4ef; no active claim. Old unregistered DNA worktree remains untouched. Proposed branch feature/starter-cockpit-shell; proposed worktree .worktrees/starter-cockpit-shell. Live demo: https://pyautolabs.github.io/PyAutoEmbryo/ (publication clone in organs/PyAutoMind/tmp/pyautoembryo-tryout-2026-10-13/PyAutoEmbryo-pages).

Plan approval pending. No source edits yet.
