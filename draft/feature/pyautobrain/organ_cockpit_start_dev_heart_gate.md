# Organ cockpit: start_dev refuses or warns on the Heart feed before development starts

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: notify
Witness: with a fixture RED feed the helper exits 2 and prints the reasons; start_dev.md, start_bundle.md and route.md each reference the step; a start_dev run in the session shows the Heart line before the plan.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-26
Epic: organ-cockpit

The cockpit and the Heart ntfy alert direct attention to a RED Heart; the human's stated rule is 'fix Heart before doing development'. Today nothing enforces it at the start of a task: the Heart gate is only consulted at ship time (ship_library / ship_workspace step 3). This prompt moves a light version of the gate to the front door.

1. A small stdlib helper in PyAutoBrain (bin/heart_feed.py or agents/faculties/vitals): read https://pyautolabs.github.io/PyAutoHeart/state.json (fallback: the local canonical PyAutoHeart state via pyauto-heart readiness --json when offline), print status, headline, updated age and the red/yellow items; exit codes 0 green, 1 yellow/stale, 2 red, 3 grey/unreachable. Never triggers a Heart tick (fast, read-only).
2. skills/start_dev/start_dev.md gains step 0a 'Heart at the door': run the helper; GREEN → continue; YELLOW/STALE → print the reasons and continue (acknowledgement is asked at ship, unchanged); RED → stop before planning and report the verbatim reasons; the human may invoke the existing AUTONOMY.md 'Human override for Heart RED (development only)' to proceed, recorded on the issue as today; GREY/unreachable → say so and continue. Under --auto RED parks the run before any issue is opened. Mirror the step in skills/start_bundle and skills/route (they enter development too).
3. Tests: the helper against fixture feeds (each status + unreachable) and a skill-seam test that the three skill files name the step.

Out of scope: changing ship-time gating; the vitals faculty's tick; Heart internals.

Witness: with a fixture RED feed the helper exits 2 and prints the reasons; start_dev.md, start_bundle.md and route.md each reference the step; a start_dev run in the session shows the Heart line before the plan.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
