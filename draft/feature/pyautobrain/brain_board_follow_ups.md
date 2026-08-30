# Brain board follow-ups: what real mornings surface

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- dashboard
- mind-workflow
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-23

The living catch-all for Brain-board gaps found by actually using it as the
morning door. Two rounds already shipped from this prompt (2026-08-23, both
via branch `claude/pyautobrain-dashboard-o33z4r`):

- **Round 1** (PyAutoBrain#254 + the boards-footer arc): README dashboard
  paragraph, per-conversation community chips, the cross-board footer on all
  six boards, the Brain row on the organism router.
- **Round 2** (readiness/devbox/trend arc, with PyAutoHeart#160 publishing
  `board.json`): the Readiness & release section consumes the Heart's
  structured blockers verbatim (their own `/bug` prompts as chips) plus the
  Hands headline; ⏸ blocked-gate annotations render inline; `board publish`
  (morning.sh's last step) pushes the dev-box observation — hygiene pre-scan
  rows + worktree state, age-stamped, stale at 48h, dropped at 7d; the
  autonomy log's tail renders as a section; the header carries the
  self-carrying "N need you" trend sparkline.

Remaining candidates — pick up only when a real morning shows the need:

1. **Cloud-safe hygiene sensors in CI** — some hygiene modes (dep-cap drift,
   optdeps/extras) could run in brain_board.yml against fresh checkouts,
   making those rows live rather than devbox-stamped. Only worth it if the
   devbox stamp proves too stale in practice.
2. **Sweep lists single-sourced** — `bin/overnight_status.sh` and
   `bin/version_drift.sh` read `config/policy.yaml board:` instead of their
   own copies (the keep-in-step comments then come out).
3. **Whatever a week of mornings surfaces** — append here before starting.

Filed separately, because it is not a nit: **`board_without_gh.md`** — the
eleven legs that read GitHub through `gh api` are dark in a remote session,
which has no `gh`. A mobile morning is mostly blind until that is closed.
