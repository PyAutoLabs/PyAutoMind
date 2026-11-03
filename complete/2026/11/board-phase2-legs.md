- summary: board phase 2. Three of the four legs the prompt named (versions, community, resume) had been retired from `collect()` in 41ec5c5 after filing, so no script needed its own seam. Upkeep, the last GitHub leg, gets `open_issues_endpoint(org)` — both its `gh api` path (dev-box path unchanged) and its `--github-data` key. Contract (board/AGENTS.md) and gatherer skill (skills/board/board.md, which still asked for retired overnight runs) updated.
- decision: human 2026-11-03 accepts upkeep reading "open-issue count unavailable" in a remote session (no org-wide issue search on the MCP surface).
- pr: PyAutoBrain#564; issue PyAutoBrain#562.
- witness: PASS — fixture tests: injected data → zero unread legs; injected null → "upkeep: open-issue count unavailable", never 0.

## Original prompt

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
Consequence: notify
Witness: A remote render with `--github-data` reports zero unread legs across versions, community, resume and upkeep, or names each remaining one with a reason other than "no gh", pinned by a fixture-driven test; the dev-box `gh` path is unchanged.
Review-minutes: 0
Unattended: ready
Filed: 2026-08-27
Issued: 2026-11-03
Parent: complete/archive/epics/board_without_gh.md (umbrella archived 2026-09-17; this prompt carries its headline criterion)
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
