# Brain board follow-ups: round out the morning surface

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-23

Follow-up features for the Brain board (shipped from
`claude/pyautobrain-dashboard-o33z4r`; design record in
`docs/pyautobrain/brain_board_assessment.md`). The human reviewed the first
render: "sample looks great, maybe missing some features — we can do those in
follow up." Candidates, most valuable first; ship as separate small PRs or one
pass, human's call at start_dev:

1. **Umbrella router card** — the PyAutoScientist organism board consumes the
   new `brain | N need you / clear to work` badge.json like the other boards'
   headlines, and links the Brain board from its where-to-work-next banner.
2. **Single source for the sweep lists** — `bin/overnight_status.sh` and
   `bin/version_drift.sh` read `config/policy.yaml board:` (overnight_jobs /
   version_stamps) instead of carrying their own copies; the keep-in-step
   comments then come out.
3. **Devbox-published local metrics** — the Heart's `pyauto-heart publish`
   pattern applied to the board's local-only blind spots (hygiene headline,
   worktrees with unpushed commits), age-stamped "observed Nh ago on the dev
   box" and expiring, so the cloud render can show them honestly.
4. **Anything the human names from using the live board** — a week of real
   mornings will surface the actual gaps; fold those in here before starting.

Not in scope: the full issue_cleanup audit half on the board (stays
confirmation-gated in its own door), and auto-anything — every chip keeps
routing through the human-gated doors.
