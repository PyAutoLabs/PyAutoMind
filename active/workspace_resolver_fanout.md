# Workspace resolver fan-out: the hook, the smoke shims and the hardcoded paths

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoMind
- PyAutoReduce
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: with a nested workspace fixture the regenerated session-start hook resolves the TRUE root rather than the family directory and fans out over every manifest repo rather than one family; `git grep -c 'WORKSPACE_ROOT="$(dirname "$REPO_DIR")"'` returns 0 across all repos after propagation; and no tracked Python file in PyAutoReduce or PyAutoArray matches `Code/PyAutoLabs`.
Review-minutes: 25
Unattended: needs-slicing
Issued: 2026-09-18
Unblocked: phase 1a SHIPPED 2026-09-18 (PyAutoBrain#392, PyAutoHeart#232, PyAutoHands#283, PyAutoMind#414) — record complete/2026/09/workspace-location-contracts.md. The resolver this consumes is on main: `_pyauto_root` resolves by `.pyauto-root` marker with the sibling-organ probe demoted to a fallback, and exports PYAUTO_ROOT_REASON / PYAUTO_ROOT_MARKER for shell callers. NOTE the limitation this phase inherits: step 3 is still wrong for a NESTED workspace with no marker (pinned by a test, deliberately, to protect the remote single-repo case), so the marker is the only thing protecting a regrouped tree.

Phase 2 of the PyAutoLabs workspace regroup. Changes NO directory layout. Mechanical fan-out that
CONSUMES the single resolver phase 1a introduces, so it cannot land before it.

## Scope

1. **The session-start hook — 1 source, 37 generated copies.**
   `PyAutoMind/policy/session_start_hook.sh:72` is `WORKSPACE_ROOT="$(dirname "$REPO_DIR")"`. Verified
   2026-09-18: exactly 37 copies exist, all byte-identical (single md5 dbcdbbde9ef3b44f54cbb1dca94fbf95),
   and all 37 carry that line. Give it the phase-1a marker walk and regenerate via
   `repos_sync.py --write`.
   Correct severity, which an early survey overstated: the hook exits at :47 unless
   CLAUDE_CODE_REMOTE=true, so it never runs in a local CLI session. It is a remote/web-session defect,
   not a local one — real, but not the dominant local risk.
   Fixing root discovery is NOT sufficient on its own: the one-level fan-out must move too —
   :426 (the ensure_full_clone unshallow loop), :470 (install_workspace_settings, which would write a
   bogus .claude/ root INTO a family directory, every guard passing), and :564 (the PYAUTO_ROOT export,
   which poisons every downstream consumer). Coverage exists in PyAutoMind/tests/test_session_bootstrap.py
   and tests/test_session_hook_sync.py.

2. Renumbered — the smoke shims moved OUT of this task. They are
   `draft/maintenance/pyautobrain/workspace_smoke_shim_bootstrap.md`: 12 repos, no propagation
   mechanism, and the 12 files are NOT copies (12 distinct checksums, 5 shape-classes). That task
   carries the prior question of whether 12 divergent copies of one bootstrap should exist at all.

3. **The 7 tracked Python files that hardcode an absolute workspace path.**
   Only one is a genuine cross-repo reference and the only one a regroup actually breaks:
   `PyAutoReduce/scripts/reduce_cosmos_web_ring.py:34` ->
   `/home/jammy/Code/PyAutoLabs/autolens_assistant/dataset/imaging/cosmos_web_ring/wavebands`.
   Also `PyAutoReduce/prototypes/` starred_vs_epsf_m92.py:30, starred_vs_epsf_omegacen.py:26,
   starred_vs_epsf_comparison.py:31, starred_epsf_spike.py:38 (all
   `Path.home()/"Code/PyAutoLabs/PyAutoReduce/scripts/output"`), and
   `PyAutoArray/files/ghost_peak_experiment.py:39`, `pca_rotation_experiment.py:28`
   (`~/Code/PyAutoLabs-wt/` inside docstrings).
   This corrects an earlier sweep that reported ZERO such files; an independent Codex review found them.

## Not in this phase

The physical move, the repos.yaml `path:` field, the ~12 root enumerators, worktree.sh and the
IDE/PYTHONPATH/symlink migration are phase 3. Also deferred there: the `smoke_install.sh` flat
`pip install ./PyAutoFit ./PyAutoArray ...` chain, which PyAutoHeart runs LOCALLY via
`heart/smoke.py:313` with `cwd=organism_root` (`smoke.py:229` builds `organism_root / repo` the same
way) — it is a shared CI+local script whose two callers would need different layouts, which is exactly
the ordering hazard the Codex review named. Do not introduce a universal `root / manifest.path` rule
before that is resolved.
