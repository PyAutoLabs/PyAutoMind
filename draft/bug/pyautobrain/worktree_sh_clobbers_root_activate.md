# worktree.sh bundle creation clobbers the unversioned root activate.sh

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Lane: local-dev
Status: formalised
Consequence: notify
Witness: after creating a new task bundle with `worktree_create`, `~/Code/PyAutoLabs/activate.sh` is byte-identical to before, and `ls -l ~/Code/PyAutoLabs-wt/*/activate.sh` shows every bundle's activate.sh as a real file (no symlink to the root)
Review-minutes: 0
Unattended: ready

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

<!-- formalised by the Intake (Conception) Agent on 2026-09-27 from file:../worktree_sh_clobbers_root_activate.md -->
