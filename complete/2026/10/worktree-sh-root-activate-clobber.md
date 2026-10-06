## worktree-sh-root-activate-clobber
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/469
- completed: 2026-10-06
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/473
- bundle: pyautobrain-worktree-guards

Merged PyAutoBrain#473 (9b73033) into main 2026-10-06 via /prm (tier `notify`; PyAutoBrain has no PR test CI, gate was the local full Brain suite). Issue #469 closed.

worktree_create no longer symlinks the names it writes itself (activate.sh, root marker) into a bundle and removes any pre-existing link before writing activate.sh, so a new bundle cannot clobber the unversioned workspace-root file or retarget other bundles. Adds opt-in worktree_repair_activate (bundle paths only). New tests/test_worktree_activate.py (4, hermetic); full suite 1199 passed; new tests red on unfixed code first.

No workspace impact (Brain tooling only); no pending-release obligation.

## Original prompt

# worktree.sh bundle creation clobbers the unversioned root activate.sh

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: medium
Lane: local-dev
Status: formalised
Consequence: notify
Witness: hermetic test — a fabricated PYAUTO_MAIN (tmp dir) containing a root `activate.sh` with known bytes; after `worktree_create <task>` the root `activate.sh` is byte-identical to before and the bundle's `activate.sh` is a regular file (not a symlink) holding the per-task PYTHONPATH; the test never touches the real workspace root
Review-minutes: 0
Unattended: ready
Updated: 2026-09-28
Issued: 2026-10-05

## Bug

`organs/PyAutoBrain/bin/worktree.sh` bundle creation clobbers the unversioned root
`~/Code/PyAutoLabs/activate.sh`.

The loop at lines ~181-187 (`for entry in "$PYAUTO_MAIN"/*` … `ln -s "$entry" "$root/$name"`)
symlinks every non-repo top-level entry of the workspace root into the bundle, including
`activate.sh`. Line ~195, `worktree_activate_script "$task" > "$root/activate.sh"`, then
writes through that symlink into the root file.

## Effect

- Every new bundle rewrites the root activate.sh to point at itself.
- Every earlier bundle whose activate.sh is that symlink silently switches its env to the
  newest bundle. 10 bundles were affected on 2026-09-27: eyes-organ-order,
  mass-field-{chaining-helper,inference-sim,profiling-live,reduce,sibling-sweep},
  multistart-cpu-memory-probe, point-source-cpu-p4, point-source-source-plane-p2b (already
  hand-repaired to a real file), remove-empty-modeling-headings.
- The canonical root template is `organs/PyAutoBrain/bin/regroup_workspace.py:193-205`
  (the root file was restored from it on 2026-09-27).

## Fix

- Exclude `activate.sh` (and any other file worktree.sh later writes into the bundle root)
  from the symlink loop, or `rm -f "$root/activate.sh"` before writing so the write never
  follows a symlink.
- Add a test: creating a bundle leaves the root activate.sh byte-identical, and the bundle's
  activate.sh is a regular file.
- Optional one-shot repair: convert existing bundle activate.sh symlinks into regenerated
  real files (`worktree_activate_script <task>`).

## Witness

`ls -l ~/Code/PyAutoLabs-wt/*/activate.sh` currently shows symlinks → the root activate.sh.

## Recurrence 2026-09-28

1. **Recurred today** for task `autolens-visualization-rebirth`: the root activate.sh (restored
   on 2026-09-27) was again overwritten with that task's per-task PYTHONPATH file, and the new
   bundle got a symlink instead of its own activate.sh.
2. **Origin of the root file:** the 2026-09-18 root backup has no `activate.sh`, so the root
   file was itself created by an earlier run of this same defect. This explains the standing
   memory that "root activate.sh points PYTHONPATH at a stale library worktree".
3. **Witness is hermetic:** test against a fabricated `PYAUTO_MAIN` with a root `activate.sh`,
   never the real `~/Code/PyAutoLabs` (see header Witness). Check `organs/PyAutoBrain/tests`
   for existing worktree.sh tests and extend them.
4. **The helper must never touch the root.** The auto-mode classifier treats restoring the
   unversioned root file as irreversible, so the fix is purely preventive: skip `activate.sh`
   (and generally any name `worktree_create` itself writes) in the sibling loop, and
   `rm -f "$root/activate.sh"` (removing any symlink) before writing it. Any repair of existing
   bundle symlinks acts on bundle paths only.
5. **Priority raised normal → medium** on the recurrence.

<!-- formalised by the Intake (Conception) Agent on 2026-09-27 from file:../worktree_sh_clobbers_root_activate.md -->
