# Group the local science checkouts by project family

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoHands
Difficulty: large
Autonomy: supervised
Consequence: judge
Priority: high
Status: planned — implementation approval requested 2026-09-19
Filed: 2026-09-19
Witness: the same repository identities resolve in a flat CI fixture, a grouped canonical fixture and a flat task bundle; after the local move all 38 declared checkouts remain covered, library imports originate at the intended checkouts, all 12 smoke bootstraps import Hands, and every retained Git worktree remains usable.

## Original request

We have been doing work to move sall the folders in PyAutoLabs into sub folder per project, find the work andcontinue it now it should be unblocked (or if PRs need merging to unblock you can merge them now as gatres removed)

## Existing decisions and completed prerequisites

The user approved the family layout on 2026-09-18: `lens/`, `galaxy/`,
`fit/`, `cti/`, `reduce/`. Keep the eight organs, PyAutoArray,
PyAutoScientist and pyautolabs.github.io at the root. Repo identity and
GitHub names do not change. See the September completion records:
`workspace-location-contracts.md`, `workspace-resolver-fanout.md`,
`workspace-smoke-shim-bootstrap.md`, `workspace-dead-weight-cleanup.md`.

The release-held blockers are now merged under the user's current grant:
autolens_workspace#562 (`89b910dd`) and autolens_workspace_test#322
(`279a69d4`), all current-head CI green. Both upstream library PRs #742/#744
were already merged. Their tasks are closed and claims released; records
`mass-field-workspace-sweep.md` and `mass-field-flat-sweep.md` carry the receipts.

## Implementation plan

1. Add one repository-location API to Brain, alongside the existing root
   resolver, with Python and shell entry points. Keep workspace root, repo
   identity, canonical checkout and task checkout distinct. Read placement
   from Mind's body map; prefer a real checkout in the supplied context so
   flat CI and flat task bundles remain valid. Reject unsafe manifest paths,
   ambiguous checkouts and missing required repos. Never treat an ordinary
   directory named after a repo as proof of checkout identity.
2. Add explicit family `path:` metadata to `PyAutoMind/repos.yaml` and teach
   `scripts/repos_sync.py`, `scripts/session_bootstrap.sh`, generated routing
   documentation and `scripts/smoke_bootstrap_sync.py` to use the shared
   lookup. Preserve both directions of disk/manifest drift checking and
   complete coverage. Stage the metadata/physical cutover so a missing nested
   path cannot silently shrink the inspected set.
3. Update Brain's `bin/worktree.sh`, `bin/install.sh`, `bin/morning.sh`,
   `agents/_common.sh`, and actual checkout enumerators in hygiene, review,
   clone and batch. Audit callers before replacing joins: many root/filename
   expressions refer to results or internal files rather than repositories.
   New task bundles stay flat and use canonical lookup for their dependency
   symlinks. Update Heart's `heart/_workspace.py`, `heart/smoke.py`, checkout
   checks and local install-chain paths; update Hands' `_workspace.py` and
   local build callers. CI still supports a flat sibling checkout layout.
4. Before moving, save a local migration inventory of canonical locations,
   HEADs, statuses, linked worktrees, symlinks and import origins. Map each
   science repo to its family (Euclid assistant/pipeline and lens profiling/
   inference belong under lens). Keep `.github` at root as the declared
   unmapped checkout. Use reversible directory renames; preserve untracked
   and ignored content. Repair Git worktree administration, dependency
   symlinks and workspace-owned activation/IDE path configuration using the
   recorded old-to-new mapping. Do not change HPC checkouts or submit jobs.
5. Validate the infrastructure before and after cutover: flat/grouped/bundle
   fixtures, missing/duplicate identities, manifest coverage, actual Git
   worktree usability, actual library import locations, all twelve smoke
   bootstrap imports, and Brain/Heart/Hands command entry points. Compare
   pre/post HEADs and dirty-file inventories. Roll back the local renames and
   recorded link changes if post-move validation fails. Run relevant organ
   suites, independent review and ship workflow; merge ready PRs under the
   user's current authorization and record the completed cutover in Mind.

## Survey and preservation requirements

Suggested branch: `feature/workspace-family-regroup`.
Suggested task bundle: `PyAutoLabs-wt/workspace-family-regroup` via the standard
worktree helper after approval. Final scope follows the caller audit.

All 38 canonical checkouts were on main at the 2026-09-19 survey. Brain,
Heart and Hands were clean. Mind has a pre-existing deleted
`draft/maintenance/pyautobrain/workspace_resolver_fanout.md`; preserve it and
exclude it from unrelated commits. Heart/Hands reported behind their fetched
main refs and must be fetched/fast-forwarded before setup.

Preserve untracked files in autofit_assistant
(`scripts/compose_model_gaussians_exponentials.py`), autolens_assistant
(`scripts/cluster_model_composition.py`) and autolens_inference (two results
trees). Do not clean any checkout as part of this migration.

Existing linked worktrees exist for Brain, Mind, Cortex, Array, the two lens
workspaces, the Euclid pipeline and profiling. Several contain unfinished or
parked work. The merged mass-field bundle is intentionally retained: its two
repos contain 17 MB + 3.5 MB of ignored outputs and 23 MB + 4.8 MB of datasets.
Repair retained worktrees; deletion is not a prerequisite for grouping.

The original phase-3 implementation was never registered as an active task;
this prompt captures the remaining work rather than reopening completed
resolver/bootstrap tasks. Layout approval is recorded, but the new code and
cutover plan was presented for explicit approval before source edits.
