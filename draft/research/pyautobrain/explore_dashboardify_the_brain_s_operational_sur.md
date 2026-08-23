# Explore: dashboardify the Brain's operational surfaces with pasteable conductor prompts

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-19 (backfilled from git)

Explore: dashboardify the Brain's operational surfaces with pasteable conductor prompts

Exploratory research, deliberately unscoped — a plan-and-consider investigation, not an implementation task. Investigate giving the organism's operational routines dashboard-style surfaces with copy-for-Claude pasteable prompts, extending the one-tap pattern beyond tasks. Two axes to consider together:

1. Conductor shortcuts. A surface carrying pasteable prompts for the recurring @PyAutoBrain conductor runs — /health, /hygiene, /community (the ears) and maybe others — each shortcut paired with a short description of what that run looks like and produces: the same kind of orientation the /wake_up skill already assembles each morning. In effect this dashboardifies wake_up a bit further, if it is not already: is the right shape one operational page the morning routine reads and links, or per-conductor sections?

2. Standardised metric dashboards. Recurring health/hygiene measurements — profiling workspace timings, library import times, slow tests/scripts, and the other standardised checks the Heart and hygiene sweeps already produce — considered as candidates for small generated dashboards, each with a claude-pasteable prompt to investigate or refresh the numbers.

Deliverable: an investigation write-up reviewed with a human — inventory which conductor runs and which standardised metrics exist, which genuinely benefit from a phone-readable surface versus staying CLI output, how this relates to the one-tap dashboard rollout (Heart board shipped — complete/2026/08/actionable-health-board.md; remaining surfaces in draft/feature/pyautobrain/one_tap_dashboard_more_surfaces.md) and to /wake_up, and which candidates (if any) earn their own feature prompts. Recommending only a subset, or none, is a valid outcome. Supervision required: this shapes the command surface humans drive.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from user-intake -->

---

**2026-08-23 — investigation resolved; implementation begun.** The human
unparked this with direction: build the PyAutoBrain dashboard, move the
/wake_up routine onto it, make it the morning starting point, and run the
local repo sync as a terminal command. The write-up this prompt asked for is
[`docs/pyautobrain/brain_board_assessment.md`](../../../docs/pyautobrain/brain_board_assessment.md)
(inventory of wake_up's legs and where each landed, what was deliberately NOT
dashboarded, architecture on the sibling-board pattern). Implementation on
PyAutoBrain branch `claude/pyautobrain-dashboard-o33z4r`
(`board/_board.py` + `brain_board.yml` + `bin/morning.sh` + wake_up repoint).
