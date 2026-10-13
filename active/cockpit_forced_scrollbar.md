# Remove forced cockpit scrollbar
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/81
Difficulty: small
Consequence: judge

## Original request
The icon scrolling left right bar is still there, I dont want a scroll and the PyAuto one does not have it

## Correction to approved cockpit-matching work
@PyAutoScientist scripts/instance_navigation.py constrains .nav-scroll to 1160px and forces overflow-x:scroll, unlike the original pyautolabs.github.io cockpit. Remove the width cap, forced scrollbar and custom scrollbar rules; use the original full-width overflow-x:auto behavior. At desktop width all icons should fit with no scrollbar/hint; retain the reference cockpit narrow-screen accessibility. Existing header, toolbar and content are unchanged.

Update tests/navigation_browser.cjs to assert width-dependent overflow and auto behavior. Verify desktop shows all icons without horizontal scrolling and mobile retains access as in the reference. Prepare regenerated Embryo artifacts. Suggested branch feature/cockpit-overflow-fix. Single clean Scientist main checkout, no active claim; old DNA worktree untouched. This is an explicitly requested correction to the already approved cockpit parity scope. Tier judge; human /prm before merge/publication.
