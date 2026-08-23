# status.sh --repos sources a file that no longer exists

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Filed: 2026-08-19 (backfilled from git)

Found by the 2026-08-19 readability-pass census (#248).
@PyAutoMind/scripts/status.sh's `--repos` branch does
`source scripts/pyauto_status.sh`, and that file does not exist in `scripts/`
— `bash scripts/status.sh --repos` fails. `skills/OWNERSHIP.md` records that
`pyauto-status` was retired into the `$health status` leg (PyAutoHeart), so
the branch is probably vestigial.

Decide and fix: either delete the `--repos` branch (and any docs offering it),
or repoint it at the Heart-owned replacement. Check the callers first
(Brain `wake_up.md`, `nightly.sh`, `bin/overnight_status.sh`; Heart `tick.sh`,
`ci_status.sh`, `heart-health.yml`) to confirm none of them pass `--repos`.
