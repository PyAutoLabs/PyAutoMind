## eyes-organ-order
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/439
- completed: 2026-09-28
- epic: pyautoeyes-birth
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/449
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/427
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/241
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/291
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/46
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/177
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/13
- library-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/35
- pending-release: PyAutoMind@https://github.com/PyAutoLabs/PyAutoMind/pull/449
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/427
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/241
- pending-release: PyAutoHands@https://github.com/PyAutoLabs/PyAutoHands/pull/291
- pending-release: PyAutoCortex@https://github.com/PyAutoLabs/PyAutoCortex/pull/46
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/177
- pending-release: PyAutoGut@https://github.com/PyAutoLabs/PyAutoGut/pull/13
- pending-release: PyAutoScientist@https://github.com/PyAutoLabs/PyAutoScientist/pull/35

Phase 0 of `pyautoeyes-birth` (PyAutoMind#437) had put Eyes after Gut. The human ruled
on 2026-09-25 that the canonical organ order is **Brain, Mind, Cortex, Memory, Eyes,
Heart, Hands, Nerves, Gut**. This task moved Eyes to that position everywhere the
order is written down:

- the `repos.yaml` body map and the session-start hook's directory chains (Mind);
- `SIBLING_ORGANS` in Brain, Heart and Hands, `_pyauto_root.sh`, `ORGANISM.md`, and the Brain docs and README;
- the generated organism-map blocks in Cortex, Nerves, Gut and the Scientist README (`repos_sync.py --write`).

## Notes

- **`pyautolabs.github.io` had no diff** after the rebase onto main, so it had no PR.
- **Human-only work still to do: the `.github` org-profile README.** The patches are kept at
  `tmp/handover/eyes-organ-order/order-dotgithub.patch` and
  `map-block-dotgithub-post449.patch` (paths relative to the workspace root).
- **Merge collision.** Mind#449 and Mind#447 both touched the PyAutoEyes block of
  `repos.yaml`: #449 moved the row and #447 rewrote its role. Whichever merged second was
  rebased to keep the #447 strings at the #449 position. The post-merge map-block regen then
  landed as PyAutoCortex#47.
- **Hook propagation.** The #449 merge push event did not trigger `session_hook_propagate`.
  It was dispatched by hand as run 36479476721, which concluded `failure`. It pushed
  `session-start.sh` to the other in-scope repos, but the PyAutoCortex push was rejected
  (`fetch first`) because it raced the PyAutoCortex#47 merge. PyAutoCortex main still holds
  the previous hook copy until the workflow is re-dispatched.

## Original prompt

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
Issued: 2026-09-25
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
