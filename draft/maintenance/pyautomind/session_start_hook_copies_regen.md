# Regenerate the 28 drifted `.claude/hooks/session-start.sh` copies after the organ-order change

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Status: draft
Consequence: glance
Witness: `python3 scripts/repos_sync.py --check` reports 0 mismatches on its hooks leg.
Filed: 2026-09-29

## The finding

`repos_sync.py --check` reports 28 `.claude/hooks/session-start.sh`
mismatches across the organism. They differ only in the `holds_an_organ`
check order and are left over from the organ-order change (Mind#439,
`4cde3d30`), which updated the canonical hook without re-propagating every
copy. Surfaced while shipping PyAutoEyes phase 3 (PyAutoMind#452).

## Fix

One sweep PR set regenerating the hook copies from the canonical source via
`repos_sync.py --write` (one PR per affected repo). The
`.github/profile/README.md` row is human-only — hand that patch to the human.
