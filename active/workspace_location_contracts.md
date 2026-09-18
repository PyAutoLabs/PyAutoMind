# Workspace location contracts: one resolver for root, repo, main and task checkouts

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a pytest fixture builds a nested workspace (lens/PyAutoLens beside a flat PyAutoBrain) and asserts the resolver returns the TRUE root, not the family directory, for both the Python and the shell entry point; and repos_sync.py --check exits non-zero when a manifest-declared repo's directory is absent (today it passes silently, checking nothing).
Review-minutes: 25
Unattended: needs-slicing
Issued: 2026-09-18

Phase 1a of the PyAutoLabs workspace regroup. Changes NO directory layout.

## Why

The workspace root has 45 entries and is hard to navigate. The human approved (2026-09-18, in chat)
regrouping the science repos into per-family subfolders `lens/ galaxy/ fit/ cti/ reduce/`, leaving the
8 organs plus PyAutoArray, PyAutoScientist and pyautolabs.github.io flat at root. Lowercase family
names were chosen because none collides with an importable package name; the human explicitly rejected
naming a group after its library (PyAutoLens/PyAutoLens) because $ROOT/PyAutoLens would still resolve
to an existing directory after the move, converting loud failures into silent wrong-path ones.

Three read-only sweeps plus an independent Codex (gpt-6-astra) review, all 2026-09-18, established
that the blocking problem is not the move — it is that the organism has no single answer to where
anything is. Six organs disagree TODAY: PyAutoHeart/heart/_common.sh:31 hardcodes $HOME/Code/PyAutoLabs;
PyAutoHeart/heart/dashboard.py:171 and PyAutoHands/autohands/board.py:56 fall back to ~/Code (not
~/Code/PyAutoLabs); PyAutoHeart/heart/checks/worktree_drift.py:46 tests `_p3.name == "PyAutoLabs"`;
PyAutoHands/autohands/run_all.py:37 and PyAutoMind/scripts/spawn.py:507 use fixed parents[N]. Only
PyAutoBrain uses the canonical _pyauto_root pair, and that pair decides the root by probing for a
sibling organ directory (agents/_pyauto_root.py:59) without checking it is a checkout.

## Scope

1. Define four SEPARATE concepts and one API, rather than one conflated "root":
   workspace-root discovery / repo identity / main-checkout location / task-checkout location.
   This separation is the review's central recommendation: the dangerous end state is "organs resolve
   by sibling arithmetic, science resolves through a manifest". Placement must be a location property,
   not a second classification system. Note PyAutoArray stays flat but is a library, not an organ.
2. Add a `.pyauto-root` marker file at the workspace root and make root discovery walk up to it instead
   of probing SIBLING_ORGANS. Model it on autolens_profiling's profiling_root(), which already walks up
   to a ruff.toml marker and is the one layout-independent path helper in the workspace. Keep
   $PYAUTO_ROOT as an override but validate it (today _pyauto_root.py:76 bypasses every check, so a
   wrong value exported by a hook is accepted silently).
3. Make PyAutoHeart, PyAutoHands and PyAutoMind consume that single resolver instead of their six
   private answers.
4. Make the drift check work in BOTH directions, folding in the separately-filed
   `draft/maintenance/pyautomind/autolens_jax_joss_manifest_gap.md` (retire it on merge):
   - declared-but-missing is silently SKIPPED at repos_sync.py:882 (CLAUDE pointer checks),
     :1318 (origin checks) and :1607 (codex hook checks) — after any move these would pass while
     checking nothing. A successful check that means reduced coverage is the failure to remove.
   - on-disk-but-undeclared is SILENCE: repos_sync walks the manifest and asks whether each entry is
     present, so it structurally cannot see a checkout absent from repos.yaml. That is the
     manifest_gap defect, and it survived the removal of its example (autolens_jax_joss).
   Note the two are independent of presence on disk: admin_jammy is a genuine manifest entry that is
   deliberately never cloned, so "missing" must be expressible as intentional rather than as drift.
5. Record the inventory the later phases need, as committed data rather than a one-off sweep:
   existing worktrees, dependency symlinks, and runtime import locations.


## Not in this phase

The physical move, the repos.yaml `path:` field, the ~12 root enumerators, worktree.sh, the
smoke_install.sh flat pip chain, and the IDE/PYTHONPATH/symlink migration are phases 2 and 3. Do not
introduce a universal `root / manifest.path` rule here: the review's named ordering hazard is that such
a rule breaks CI immediately (whose trees are legitimately flat) and misroutes task worktrees later.
The fan-out that CONSUMES this resolver is phase 2:
`draft/maintenance/pyautobrain/workspace_resolver_fanout.md` — the 37-copy session-start hook,
the 14 run_smoke/retime PyAutoHands joins, and the 7 hardcoded absolute paths. It cannot land
first and is mechanical once this phase exists.

The dead-weight cleanup was the sibling task workspace-dead-weight-cleanup, SHIPPED
2026-09-18 (PyAutoBrain#390, PyAutoMind#413) — record
`complete/2026/09/workspace-dead-weight-cleanup.md`. Two findings from it land here:
the `.worktrees/` trees it removed are ~80 paths this phase no longer has to migrate, and
its `autolens_jax_joss_manifest_gap` sibling is the MIRROR of scope item 4 — `repos_sync.py`
is blind in both directions (declared-but-missing is skipped; on-disk-but-undeclared is
silence). Fix both together.
