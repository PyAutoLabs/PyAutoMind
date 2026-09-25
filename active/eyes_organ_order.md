# Canonical organ order — Eyes after Memory, before Heart

Type: maintenance
Target: PyAutoEyes
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
- pyautolabs.github.io
- PyAutoScientist
- PyAutoCortex
- PyAutoNerves
- PyAutoGut
Difficulty: small
Autonomy: supervised
Priority: high
Lane: local-dev
Status: draft
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check` organism-map/organ-table legs OK with Eyes between Memory and Heart in every generated block; grep of SIBLING_ORGANS lists in Brain/Heart/Hands shows the same order.
Epic: pyautoeyes-birth
Filed: 2026-09-25

## Request (verbatim)

> I just applied the patch, but I dont think Eyes belong after Gut, I think
> they belong after Memory before Heart which should be the canonical order

## Context

Phase 0 of `pyautoeyes-birth` (`complete/2026/09/pyautoeyes-birth-organ-row.md`,
PyAutoMind#437) appended Eyes after Gut everywhere. The human ruled on
2026-09-25 that the canonical organ order is:

**Brain, Mind, Cortex, Memory, Eyes, Heart, Hands, Nerves, Gut**

## Files to reorder (the phase-0 touch list)

- **PyAutoMind**: `repos.yaml` (move the Eyes row between Memory and Heart);
  `policy/session_start_hook.sh` directory chains.
- **PyAutoBrain**: `agents/_pyauto_root.py` `SIBLING_ORGANS`;
  `bin/_pyauto_root.sh`; the `ORGANISM.md` table; `docs/concepts/organism.md`;
  the `docs/index.md` toctree; the `README.md` organ list.
- **PyAutoHeart**: `heart/_workspace.py` and `heart/_workspace.sh`.
- **PyAutoHands**: `autohands/_workspace.py`.
- **pyautolabs.github.io**: the `index.html` blurb.
- Then run `repos_sync.py --write` to regenerate the map blocks (Brain, Cortex,
  Nerves and Gut `AGENTS.md`), the Scientist README and the root routing table.
  The `.github` org-profile table is a human edit.
- The `organs/AGENTS.md` root file is unversioned, so edit it by hand.

## Note for later phases

The phase-2 items (the `policy.yaml` boards and `_theme.py`) must use the new
order when they land.
