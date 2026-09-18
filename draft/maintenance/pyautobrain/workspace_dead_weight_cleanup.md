# Workspace dead-weight cleanup and autolens_jax_joss local removal

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- autolens_assistant
- autofit_assistant
- autolens_inference
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `ls -a` at the workspace root lists none of .agents, .codex, .git, scrap.py, root.log or .pr-body-*.md; `git -C <repo> worktree list` reports no .worktrees/ entry for any repo; autolens_jax_joss is absent from disk while `git ls-remote https://github.com/PyAutoLabs/autolens_jax_joss` still returns 6bce65e; and `python3 -c "import autolens, autofit, autoarray, autogalaxy"` still resolves from the flat checkouts.
Review-minutes: 5
Unattended: safe

Phase 1b of the PyAutoLabs workspace regroup. Changes NO directory layout and touches no organ
logic - pure deletion of material already proven dead. Sibling task: workspace-location-contracts.

## Scope

1. Delete root dead weight: .agents/ (10 symlinks, ALL already dangling — targets PyAutoPrompt/ and
   admin_jammy/, neither of which exists); .codex/ (empty since 2026-05-13); the root .git/ stub
   (contains only an empty info/ dir — it is why git commands at the root fail "not a git repository"
   and why `codex exec` refuses to start without --skip-git-repo-check); scrap.py (contains the
   truncated non-parsing line "import numpy as"); root.log (0 bytes); the 4 .pr-body-*.md drafts from
   2026-09-14; .pytest_cache/; .ruff_cache/.
2. Prune stale references to repos that no longer exist: ~45 .idea/PyAutoLabs.iml entries (z_projects/*,
   z_projects_complete/*, PyAutoConf, PyAutoBuild, PyAutoPulse, PyAutoPrompt, autolens_base_project —
   all confirmed absent from disk; note vcs.xml by contrast is current, all 39 mappings resolve); the
   admin_jammy and z_projects/euclid rows in the root AGENTS.md; and the 2 stale
   .claude/settings.json additionalDirectories (./PyAutoConf, ./autolens_base_project).
3. Remove the two .worktrees/ trees (74M: howtofit-mode, scientific-workflow-language). Verified: NO
   unpushed commits in any member of either tree. Judge three untracked items first —
   autolens_assistant/scripts/cluster_model_composition.py,
   autofit_assistant/scripts/compose_model_gaussians_exponentials.py, and
   autolens_inference/results/slam/imaging/hst/delaunay_1250/ plus
   .../slam_base/hpc_a100_jax_gpu_dense_fp64__rate_probe_342695/ (these look like real A100 run output —
   preserve them before removing the tree). Use `git worktree remove` / prune, not rm -rf, so each
   repo's admin metadata is updated. This also removes ~80 worktree paths from the phase-3 migration.
4. Remove the autolens_jax_joss LOCAL checkout. Verified safe 2026-09-18: clean tracked and untracked
   status, no stashes, only local branch main, no commit on any branch absent from a remote-tracking
   ref, and local HEAD == origin/main == refs/heads/main == 6bce65e47a9e2a789b7ee83ee805abd755e1b945
   (remote reached directly). 4.5M. Lost: gitignored dataset/ (re-fetchable from autolens_workspace),
   results/quick/ (throwaway quick-mode runs) and three __pycache__ trees. The committed results/*.json
   and RESULTS.md are pushed. It is the only checkout absent from PyAutoMind/repos.yaml.
   Clean up alongside: the .idea/vcs.xml:34 mapping; the exclusion comment at
   PyAutoBrain/bin/clean_slate.sh:72; the two .worktrees/*/autolens_jax_joss copies (removed by item 3);
   the now-moot open drafts draft/maintenance/pyautomind/autolens_jax_joss_manifest_gap.md and
   draft/feature/autolens_jax_joss/autolens_jax_joss_benchmark_repo.md; and the autolens_jax_joss row in
   draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md.

## Explicitly out of scope

Deleting or archiving the autolens_jax_joss GitHub repo. The remote stays. It is the citable artefact
behind the JOSS paper's benchmark claims, is linked from autolens_workspace/scripts/weak/start_here.py:309,
and mgl-slam-batch-home.md:19 flags its benchmarks as possibly pinned to published JOSS numbers.
Deleting it would break a published paper's reproducibility path. Leave complete/** history and the
autolens_workspace source comments as they are — they reference the GitHub repo, which survives.
