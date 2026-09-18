# Workspace location contracts: one resolver for root, repo, main and task checkouts

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoHands
- PyAutoArray
- PyAutoReduce
- HowToFit
- HowToGalaxy
- HowToLens
- autocti_workspace
- autocti_workspace_test
- autofit_workspace
- autofit_workspace_test
- autogalaxy_workspace
- autogalaxy_workspace_test
- autolens_workspace
- autolens_workspace_test
- euclid_strong_lens_modeling_pipeline
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a pytest fixture builds a nested workspace (lens/PyAutoLens beside a flat PyAutoBrain) and asserts the resolver returns the TRUE root, not the family directory, for both the Python and the shell entry point; and repos_sync.py --check exits non-zero when a manifest-declared repo's directory is absent (today it passes silently, checking nothing).
Review-minutes: 25
Unattended: needs-slicing

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
4. Give the session-start hook the same marker walk: PyAutoMind/policy/session_start_hook.sh is the one
   source, generated into 37 byte-identical per-repo copies (verified: 37 files, single md5
   dbcdbbde9ef3b44f54cbb1dca94fbf95, all 37 carrying `WORKSPACE_ROOT="$(dirname "$REPO_DIR")"` at :72).
   Correct severity: the hook exits at :47 unless CLAUDE_CODE_REMOTE=true, so it affects remote/web
   sessions only, never a local CLI session. Its one-level fan-out (:426 unshallow loop, :470
   install_workspace_settings, :564 PYAUTO_ROOT export) must be fixed too — fixing root discovery while
   leaving the fan-out at one level still omits every nested science repo. Covered by
   PyAutoMind/tests/test_session_bootstrap.py and tests/test_session_hook_sync.py.
5. Give the same marker walk to the 14 files joining `WORKSPACE.parent / "PyAutoHands"` (12
   .github/scripts/run_smoke.py plus autolens_workspace_test and autogalaxy_workspace_test retime.py).
   Breaks loudly but mis-diagnosed as "No module named build_util"; bypassed in CI because the reusable
   workflow supplies Hands on PYTHONPATH.
6. Fix the 7 tracked Python files that hardcode an absolute workspace path. One is a genuine cross-repo
   reference and the only one the regroup would actually break:
   PyAutoReduce/scripts/reduce_cosmos_web_ring.py:34 -> /home/jammy/Code/PyAutoLabs/autolens_assistant/
   dataset/imaging/cosmos_web_ring/wavebands. Also PyAutoReduce/prototypes/starred_vs_epsf_m92.py:30,
   starred_vs_epsf_omegacen.py:26, starred_vs_epsf_comparison.py:31, starred_epsf_spike.py:38 (all
   Path.home()/"Code/PyAutoLabs/PyAutoReduce/scripts/output") and PyAutoArray/files/
   ghost_peak_experiment.py:39, pca_rotation_experiment.py:28 (~/Code/PyAutoLabs-wt/ in docstrings).
   This corrects an earlier sweep that reported zero such files.
7. Make "declared in the manifest but missing on disk" an ERROR rather than a skip. repos_sync.py:882
   (CLAUDE pointer checks), :1318 (origin checks) and :1607 (codex hook checks) all skip a repo whose
   directory is absent, so after any move they would pass while silently checking nothing. A successful
   check that means reduced coverage is the failure mode to remove.
8. Record the inventory the later phases need, as committed data rather than a one-off sweep: existing
   worktrees, dependency symlinks, and runtime import locations.

## Not in this phase

The physical move, the repos.yaml `path:` field, the ~12 root enumerators, worktree.sh, the
smoke_install.sh flat pip chain, and the IDE/PYTHONPATH/symlink migration are phases 2 and 3. Do not
introduce a universal `root / manifest.path` rule here: the review's named ordering hazard is that such
a rule breaks CI immediately (whose trees are legitimately flat) and misroutes task worktrees later.
The dead-weight cleanup is the sibling task workspace-dead-weight-cleanup.
