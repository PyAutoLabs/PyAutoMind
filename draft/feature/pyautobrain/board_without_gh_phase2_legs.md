# Board phase 2: the remaining four legs onto the seam

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- dashboard
- mind-workflow
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-27
Parent: draft/feature/pyautobrain/board_without_gh.md
After: complete/2026/08/board-github-data-seam.md (phase 1 shipped 2026-08-27, PyAutoBrain#303 — this is unblocked)

Phase 2: port the four legs phase 1 did not cover onto the seam it built (`--github-data`; the contract is `PyAutoBrain/board/AGENTS.md` → "Reading the board in a remote session") —
`versions: no stamps resolved` (`bin/version_drift.sh`), `community: scan
unavailable (exit 4)` (`agents/conductors/community/_community.py`), `resume:
pending-release PR search failed`, and `upkeep: open-issue count unavailable`.

Two of these live in scripts rather than in `_board.py`, so the phase's real
question is whether each script grows its own `--github-data` seam or whether
the board gathers on their behalf. Answer it in the phase-1 contract's terms;
do not invent a second shape.

## Done when

A remote render reports **zero** unread legs, or names each remaining one with
a reason that is not "no `gh`" — the parent prompt's headline criterion.
