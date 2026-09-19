# Infrastructure checkouts grouped under organs

Completed the approved two-phase migration: infrastructure compatibility first,
then journaled relocation of the eight organs and PyAutoScientist into `organs/`.
PyAutoArray and the public hub remain at the workspace root; science families
retain their existing grouped locations. The root marker and activation entrypoint
remain at the outer workspace root. No GitHub repository identity changed.

## Delivery

- PyAutoBrain#398 and #399: manifest bootstrap, shared lookup consumers, command
  guidance, activation and journaled physical/worktree repair.
- PyAutoMind#420: manifest placement, root/bootstrap/spawn discovery, generated
  smoke and session hooks. PyAutoMind#421 removes a satellite-specific probe from the canonical hook.
- PyAutoHeart#234/#235 and PyAutoHands#285/#286: grouped root and command consumers, explicit
  lookup failure propagation, duplicate Brain rejection and standalone CLI import.
- PyAutoMemory#100 and PyAutoScientist#29: grouped Brain theme discovery.
- PyAutoCortex#40: correct local lens-family science paths and generated dashboards.

Mind's canonical smoke propagation delivered all twelve generated bootstrap blocks
directly to main. The twelve duplicate migration PRs were closed after byte-for-byte
comparison against the delivered main commits, and their redundant CI cancelled.
Receipt `.migration/organs/bootstrap-delivery.json` records every PR and commit.
They were superseded, not merged; no pending CI is represented as green.
Canonical session hook propagation also completed, including the firewall correction.
Scientist deliberately has no PR CI; its eight local tests and independent review passed.

## Validation

Full local suites passed: Brain959, Mind573, Heart1032, Hands461, Memory210,
Scientist8 and Cortex63. Focused review regressions passed, including six real-Git
migration tests. Applicable infrastructure PR workflows and matrix legs passed.
Independent reviews found and repaired direct-script import, shell error propagation,
duplicate checkout and activation-scope issues; final source review CLEAN.

Physical cutover: nine repos moved,81 symlinks repaired,17 local configuration files
updated. Journal verification preserved directory device/inode,HEAD and full
porcelain status for every moved repo. All39 canonical branch names and dirty/
untracked states matched the pre-cutover inventory. Imports6/6, deployed smoke
bootstraps12/12, Git checkouts/worktrees77/77, manifest38/38 and generated hooks37/37
passed; all drift/firewall checks passed. Root and task activation overrides passed.
The standard installer refreshed skill links. Hook propagation run35440020980
succeeded after the final canonical hook correction.

## Preservation and repair

The final inventory compares directory identity, HEADs and dirty/untracked statuses
across the move. Existing results, datasets and other tasks' worktrees are preserved.
The Cortex checkin branch retains its name. The pre-existing Mind draft deletion
`draft/maintenance/pyautobrain/workspace_resolver_fanout.md` is preserved and excluded
from migration commits. No remote HPC checkout or job was changed.

A post-science-migration Cortex pull had recreated a results-only flat
`autolens_inference/` using its stale project map. All22 result files matched the
canonical `lens/autolens_inference/`; the entire recreated folder, including its
nonidentical `.cortex/pull.json`, was preserved by rename under
`.migration/organs/recovered-autolens_inference/`. Cortex's project paths are now fixed.

For existing shells run `source /home/jammy/Code/PyAutoLabs/activate.sh`; restart
agent sessions to reload installed skill links. Existing generated task activation
files select their own organ paths after canonical activation; user-authored and
symlinked activation files are left alone.

Local receipts and the reversible cutover journal live at `.migration/organs/`,
outside every moved checkout. All ignored task files were archived with verified SHA-256 receipts before cleanup.
Task completion releases this task's claims and
removes only its temporary worktrees after preserving their evidence. Branch refs
for superseded generated commits remain recoverable; their exact file content is
already present on main via canonical propagation.

## Original prompt

# Group the infrastructure checkouts under organs

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoHands
- PyAutoCortex
- PyAutoMemory
- PyAutoNerves
- PyAutoGut
- PyAutoScientist
Difficulty: large
Autonomy: supervised
Consequence: judge
Status: approved — human said “ok go” after the two-phase plan
Filed: 2026-09-19
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/397
Witness: Flat and grouped infrastructure resolve identical repository identities; all 38 manifest checkouts, twelve smoke bootstraps, imports, commands and retained Git worktrees pass after the move, preserving untracked and ignored data.

## Original request

how complex would it be from here to take the final step and also make an organs folder for PyAutoScientist and others?

Approval: ok go

## Approved plan

Phase 1: make infrastructure discovery work with flat and organs/ layouts; merge and validate. Phase 2: move the eight organs and PyAutoScientist with the existing journal, repair links, and repeat imports, worktree and coverage checks. Keep PyAutoArray, the public hub, root marker and activation entrypoint at root. Preserve existing user changes, results and other tasks.

## Detailed implementation

- Brain agents/_repo_paths.py: bootstrap Mind manifest discovery independently of the manifest, support flat and one-family placement, reject ambiguities; package_paths uses the same discovery. Root resolution retains marker-first semantics.
- Brain launchers, resolver loaders, agents, board, worktree and migration helpers: replace root/organ joins with shared lookup; locate Brain itself without circular dependency, preserve flat CI and task bundles.
- Mind scripts/repos_sync.py, session_bootstrap.sh, policy/smoke_bootstrap.py and propagation: locate Brain and Mind after nesting, add organs paths for nine repos, regenerate the twelve deployed smoke shim blocks.
- Heart and Hands root/resolver loaders and organ consumers: support grouped infrastructure, keep standalone/flat fallback; inspect Cortex, Memory, Nerves, Gut and Scientist for consumed fixed sibling paths and fix only actual callers.
- Focused flat/grouped/missing/ambiguous tests, organ suites and independent review. Merge tested source PRs, then refresh canonical repos.
- Fresh inventory; move nine real checkout directories without cleaning, repair retained Git worktrees, symlinks, root activation, local IDE/hook config and installed skill links. Journal must survive moving Mind and preserve rollback.
- Validate manifest 38/38, actual smoke bootstrap 12/12, imports, commands and retained worktrees. Record completion and remove only this task worktrees.

Suggested branch: feature/workspace-organs-regroup
