Phase 1b of the workspace regroup. Cleared provably-dead workspace-root material and
removed the `autolens_jax_joss` local checkout. No directory layout changed.

## What shipped

**Versioned** — the two merged PRs are small by design:

- `PyAutoBrain/bin/clean_slate.sh` — the `DATASET_REPOS` exclusion comment no longer
  implies a local `autolens_jax_joss` checkout, while keeping the record of why it was
  excluded. No behaviour change; it was never in that array.
- `PyAutoMind/repos.yaml` — the `euclid_strong_lens_modeling_pipeline` role text routed
  readers away from `z_projects/euclid`, a directory that no longer exists. Rewritten and
  the workspace-root `AGENTS.md` routing table regenerated via `repos_sync.py --write`.
- Three prompts re-pointed (see "Drafts kept" below).

**Unversioned** — the bulk of the task. The workspace root is not a git repo, so git holds
none of this and there was no rollback; everything was archived first to
`~/Code/PyAutoLabs-backups/root-unversioned-2026-09-18.tar.gz` (29 entries, 5.7 KB).

- `.worktrees/` removed, 74M -> 0: 8 real worktrees via `git worktree remove` + `prune`,
  then ~81 symlinks. All 8 task branches verified at 0 commits absent from a remote. Only
  genuine loss: `autofit_workspace/test-results/` (24 KB smoke artefact).
- `autolens_jax_joss` local checkout removed (4.5M) after re-confirming `ls-remote` parity
  at `6bce65e` immediately before deletion. **The GitHub remote is deliberately retained** —
  it is the citable artefact behind the JOSS paper's benchmark claims and is linked from
  `autolens_workspace/scripts/weak/start_here.py:309`.
- Root dead weight deleted: `.agents/` (10 symlinks, every one already dangling — they
  targeted `PyAutoPrompt/` and `admin_jammy/`, neither on disk), `.codex/` (empty since
  2026-05-13), `scrap.py` (contained only the non-parsing line `import numpy as`),
  `root.log` (0 bytes), four spent `.pr-body-*.md`, `.pytest_cache/`, `.ruff_cache/`.
- Stale references pruned: 44 dead `.idea/PyAutoLabs.iml` entries, the `.idea/vcs.xml`
  jax_joss mapping, 2 dead `.claude/settings.json` `additionalDirectories`.

Root entry count: 45 -> 42 visible, 59 -> 47 with dotfiles. The navigation win is modest by
design — this task cleared dead weight only; the regroup itself is what takes the root to ~16.

## Three deviations from the approved plan

1. **The root `.git/` stub was kept.** The plan's rationale for deleting it was wrong: git
   and `codex exec` fail at the workspace root because there is *no repo*, not because of
   the stub, and removing it changes only the error text. It also turned out to hold a live
   `claude-code-runtime` exclude file. Deleting a harness-managed directory for a benefit
   that does not exist is pure risk. (Verified no parent of the workspace is a git repo, so
   removing it would not have caused git to operate on an ancestor either.)
2. **The `.idea` prune was nearly destructive and was corrected mid-flight.** Dropping every
   entry whose path is absent removed 53 entries — including 9 `excludeFolder` rules for
   `output/`, `.venv/` and `notebooks/` dirs that simply do not exist *right now* and are
   recreated by runs, which would have let the IDE index large output trees later. The step-0
   archive was restored and the correct rule applied: drop an entry only when its **repo** is
   gone (44 entries across 7 repos: z_projects, z_projects_complete, PyAutoConf, PyAutoBuild,
   PyAutoPulse, PyAutoPrompt, autolens_base_project). The archive earned its keep within ten
   minutes of being written.
3. **Neither jax_joss draft was retired**, though both were filed as "now-moot". See below.

## Drafts kept, not retired

- `draft/maintenance/pyautomind/autolens_jax_joss_manifest_gap.md` — its motivating example
  is gone, but its defect stands: `repos_sync.py --check` drift-checks **manifest -> disk
  only**, so a checkout absent from `repos.yaml` is silence rather than a failure. Annotated,
  including the point that presence on disk and presence in the manifest are independent
  (`admin_jammy` is manifest-listed and has never been cloned). This is the **mirror** of an
  item in `draft/maintenance/pyautobrain/workspace_location_contracts.md`, which makes
  *declared-but-missing* an error (`repos_sync.py:882,1318,1607` skip it today). The check is
  blind in both directions and the two should be fixed together.
- `draft/feature/autolens_jax_joss/autolens_jax_joss_benchmark_repo.md` — the repo now exists
  on GitHub at `6bce65e` with benchmark scripts, committed `results/*.json` and a `RESULTS.md`,
  last science commit "complete first A100 sweep — 8 benchmarks + imaging Nautilus comparison".
  So it looks **shipped** rather than moot — but that was not verified, so it is flagged for
  the intake reconcile procedure rather than archived. Verification now needs a clone.
- `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md` — its 7
  jax_joss benchmark files still need the flat-`fields=` migration but are no longer locally
  sweepable; that member now needs a fresh clone or a PR against the remote.

## Corrections to the filed prompt

The prompt called the `admin_jammy` row in the root `AGENTS.md` stale. It is not —
`Jammy2211/admin_jammy` is a genuine body-map repo that simply is not cloned locally. Only the
`z_projects/euclid` reference was dead, and since that table is generated between `repos_sync`
markers the fix belonged in `repos.yaml`, not in `AGENTS.md`.

## Witness

- `ls -a` at the workspace root: all 12 targeted entries gone
- `git worktree list` per repo: 0 repos still registering a `.worktrees/` entry
- `git ls-remote .../autolens_jax_joss` still returns `6bce65e` with the checkout absent
- `import autolens, autofit, autoarray, autogalaxy, autonerves` all resolve from the flat checkouts
- `repos_sync.py --check` exit 0, all 8 checks (incl. "37 of 37 checked out, 2 excluded")
- `intake dashboard --check` — "are current"
- `bash -n clean_slate.sh`; XML validity of `.iml` and `vcs.xml`; JSON validity of `settings.json`;
  all 4 hook command paths and `BASH_ENV` re-verified to resolve

## Not touched

The 11 live `PyAutoLabs-wt` task worktrees; `scrap.md`, `tmp/`, `.git-salvage/`; the three
canonical untracked files Heart reports as drift (two assistant scripts and the
`autolens_inference` A100 results) — those appeared inside `.worktrees/` only through symlinks
and were never at risk. Five stale PyAutoMind worktrees remain in other sessions' `/tmp`
scratchpads; they survived `prune`, so those directories still exist and belong to other sessions.

## Follow-on

Phase 1a is `draft/maintenance/pyautobrain/workspace_location_contracts.md` — the resolver work,
which is the real prerequisite for moving anything. Phase 3 (the physical regroup into
`lens/ galaxy/ fit/ cti/ reduce/`, organs staying flat) waits for the in-flight tasks to clear
the PyAutoGalaxy + PyAutoLens release gate.

## Original prompt

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
Issued: 2026-09-18

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
