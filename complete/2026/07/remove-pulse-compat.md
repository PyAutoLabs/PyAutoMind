## remove-pulse-compat
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/20
- completed: 2026-07-06
- repos: PyAutoHeart, PyAutoBrain, PyAutoBuild, admin_jammy
- branch: feature/remove-pulse-compat (PyAutoBrain PR #13, squash-merged); other repos shipped earlier via #113 / #573 and prior PyAutoHeart shim removal
- validation:
  - `pyauto-brain help` renders after shim removal (exit 0)
  - Copilot review on PR #13: reviewed all files, no comments
  - grep: no stale `pyauto-pulse`/`pyauto-agent` shim claims or live invocations remain
- notes: |
    Final cleanup of the PyAutoPulse→PyAutoHeart and PyAutoAgent→PyAutoBrain
    renames. PyAutoHeart's `pyauto-pulse` shim, PyAutoBuild's autobuild CLI
    (#113), and the five library CI workflows (#573) were already migrated;
    admin_jammy had no pulse refs. This task removed PyAutoBrain's dead
    `pyauto-agent` shim (zero live callers) and corrected the docs / capability
    audits that still claimed the shims were retained (BUILD/HEART "drift" note
    flipped YELLOW→GREEN now that PyAutoBuild is fully renamed). Also refreshed
    ~/.bashrc onto PyAutoHeart / `pyauto-heart`.
    Deferred: the PyAutoBrain GitHub About still reads "gates on PyAutoPulse" —
    belongs to autoprompt/update_renamed_repo_abouts.md, not this task.

## Original prompt

# Remove PyAutoPulse Compatibility Names

## Original Request

We renamed PyAutoPulse to PyAutoHeart, but the folder still has PyAutoPulse and there is PyautoHeart/autopulse, is it safe to remove these pulse things and if so do it

## Notes

- Remove the old top-level `PyAutoPulse` symlink if it is only an alias to `PyAutoHeart`.
- Remove tracked `pulse` / `pyautopulse` compatibility wrappers from `PyAutoHeart`.
- Update packaging and tests to use canonical `heart` / `pyautoheart` paths only.
