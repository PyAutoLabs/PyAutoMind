Shipped in PyAutoBrain#619 (closes PyAutoBrain#618), merged 2026-11-13 by the human's `/prm`.

`<Science>/STATE.md` is now its own table-only render (`render_science_state`) instead of a byte copy of `dashboard.md`: a title line (generated date, last check-in, Pages link, do-not-edit), then `## Active (N)`, `## Dormant (N)`, `## Planned (N)` only when any, `## Retired (N)`. Active/Dormant/Planned: Project · Where · Now · Runs · Last update; Retired: Project · Where · Note · Last update. Where is relative to the Science root or `Code/…` under the workspace root; Now/Note are the first sentence capped at 120 chars (human's choice), Note without its `previously:` history.

Tests: tests/test_cortex_conductor.py 104 passed. The first PR head failed CI's tenant-firewall check (instance names `PyAutoFit`, `autofit_inference` in two test fixtures); fixed with neutral fixture names before merge.

Shipped under the Heart RED development override (recorded on the issue, the PR, active.md and autonomy_log.md 2026-11-13); Heart remains RED for release purposes.

## Original prompt

# STATE.md as status tables, not a copy of the board

Targets: @PyAutoBrain
Type: feature
Filed: 2026-11-13
Issued: 2026-11-13
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/618
Consequence: judge

Verbatim user request (2026-11-13): "STATE.md is a bit too not human readable, I want it to be a quick "check in on projects via a table" vibe and not incude things like the whole check in prompt you might copy from the dashboard. Professional/tasks.md serves this function a lot better, it is just tables under each group I can quickly eyeball with the stuff i need to look at less (e.g. Done) at the bottom."

Layout approved from a mockup; Now = "First sentence, max 120". Heart RED override authorized in the same answer ("Override both").

Tier: judge — merge mode: human /prm
