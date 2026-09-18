## profiling-contracts
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/284
- completed: 2026-09-18
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/285
- merge: f0d73171d2aad13c79471fce454a9cb801d2060e
- summary: Fixed-light cells reject unknown flags and invalid counts/budgets; CPU comparison rows reset and validate their timed streams. Current campaign summaries clarify CPU closure, phase-7 shelving, corrected GPU budgets/attribution and the unversioned bridge-control limitation.

## Validation and authorization

CI run35366185667 on head45b3701 passed its full lint/test/link/smoke workflow,
every job and step green. Local63 affected tests and12 changed-cell smokes
passed; independent Sol review CLEAN. All task branch commits proven ancestors
of origin/main. No benchmarks, solver/default changes or result regeneration.

User explicitly authorized separate-worktree coordination with GPU phase2,
then task-specific development shipping under Heart RED:
`release validation FAILED (stage integrate)`; YELLOW:
`manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.
Live user `ok merge and wrap up` separately authorized merge/close-out.
No release authorization or claim that Heart is healthy.

GPU phase2 remains separate; preserve its extra CLI declarations when integrating
the one-line final-parser change. Historical lever3 bridge control was not
available locally and no replacement was fabricated. Pending library release
obligations remain in the CPU phase3 completion record.

## Cleanup

Removed task worktree via worktree_remove after releasing its Mind claim.
Only disposable Python/pytest/Ruff caches were present; no research data products.
Local task branch removed after ancestry proof. Dashboard regenerated with the
completion record; folder reconciliation found no suspects.

## Original prompt

# Harden profiling experiment contracts and current result summaries

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: human-required
Filed: 2026-09-18
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/284

## Original user request (verbatim)

> ok I agree with that implement the changes and improve the repo :)

The user approved the preceding read-only review's two recommendations:
validate experiment options and matched draw streams, and make corrected
findings/current campaign state discoverable with durable supporting evidence.

## High-level plan

- Reject unconsumed command-line options at the fixed-light cells' final parsing
  boundary while preserving intentional shared/cell-specific staged parsing.
- Validate resolved experiment settings and matched CPU timing streams before
  reporting comparisons; preserve the already-correct phase-5/6 protocols.
- Add short superseding notices for corrected GPU headlines and shelved CPU
  follow-ups; correct the stale GPU phase-2 epic pointer from the active ledger.
- Preserve any recoverable bridge evidence that supports the CPU cumulative
  headline, labelled as a control-only record from an incomplete A/B job.
- Run focused contract tests and required repo checks, then ship a reviewable PR.

## Detailed plan

Classification: standalone workspace work in @autolens_profiling. Mind owns
the accompanying prompt, registry and epic-state correction. No library change.
Suggested branch: feature/profiling-contracts.

1. `_profile_cli.py`: expose unconsumed options to an explicit final cell-parser
   boundary (or compose the parsers), reject unknown flags and abbreviations there.
   Retain existing staged parsing for unrelated callers; do not broadly migrate
   the repository. Inspect fixed-light cell flags before wiring the boundary.
2. `scripts/imaging/likelihood_breakdown/fixed_light*.py`: adopt the boundary in
   the relevant existing CPU/GPU fixed-light cells; validate positive counts and
   experiment identities. Preserve the GPU phase-2 owner's unmerged batching
   implementation and coordinate the minimal trace-cell parser edit explicitly.
3. `fixed_light_numba.py`: inspect phase-4b timing-stream alignment, generalize
   only where comparisons can still drift after unequal warm-up lengths, and
   record/assert the matched stream metadata. Do not change solver or memo policy.
4. `scripts/misc/test/`: add focused regression coverage for misspelled flags,
   valid mixed shared/local flags, legacy compatibility and stream mismatch.
   Tests must avoid executing likelihood benchmarks or generating result data.
5. `results/notes/` and `results/README.md`: concise current-summary pointers,
   explicit budget-2 versus budget-7 correction, single-call versus batch scope,
   CPU epic closure/phase-7 shelving, and separate pending-library-release state.
   Retain historical measurements and add notices rather than rewriting history.
6. Inspect tracked evidence and permitted existing artifacts for job343355's
   control bridge. Commit it only if provenance can be verified; otherwise
   disclose the reproducibility limit and avoid claiming it was recovered.
   Use the existing source/job sidecar convention, not a new schema framework.
7. Validate focused tests, Ruff lint/format, changed-cell import smokes and README
   idempotence; independent review and Heart gate before ship-workspace.

## Branch survey and authorization

User approved the two changes in this session. autolens_profiling main is clean
but eight commits behind origin/main; create the worktree from fetched origin/main.
PyAutoMind main was clean and fast-forwarded to 93dcc34e.
The conflict guard reports hst-gpu-residue-p2 still claims autolens_profiling.
Coordination approved 2026-09-18: user replied "Yes, coordinate in a separate worktree".
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-contracts.
Preserve GPU phase-2 implementation; coordinate only the parser boundary.

## Scope exclusions

No new benchmarks, issues for further research, library defaults, solver changes,
memo/order research, phase-7 revival, broad audit, result-schema migration or
general harness rewrite. No merge/release authorized by this task.

## Implementation checkpoint — 2026-09-18

Implemented in /home/jammy/Code/PyAutoLabs/.worktrees/profiling-contracts/autolens_profiling,
branch feature/profiling-contracts, staged and not committed pending Heart override.
Strict final shared/local parser in 12 fixed-light cells; invalid counts/budget
lists rejected; numba rows reset/validate their timed streams. Current-summary
page and nine superseding notices preserve CPU closure, phase-7 shelving,
corrected GPU headlines and the unversioned bridge-control limitation. No new
benchmarks, library changes or result artifacts. Mind epic pointer corrected.

Validation: full suite initially 646 passed, 5 skipped and one stale AST helper-name
reference; that test was updated. Final affected rerun: 63 passed (33 contract tests
plus 30 CPU tests), five pre-existing fixture warnings. Twelve changed-cell import
smokes pass. Ruff check/format, README idempotence, submit wall contracts, diff
whitespace and 57 local Markdown links pass. Actual CLI rejections checked for
unknown flags, zero threads, mixed precision, dataset mismatch and unsupported
vmap-batch on the old trace cell. Independent Sol review: CLEAN, including actual
phase-2 parser compatibility and per-claim dispositions.

Heart verdict: RED `release validation FAILED (stage integrate)`;
YELLOW `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.
Live user authorized task-specific development shipping: "Yes, ship this development PR".
Authorization: commit, push, PR-open only; no merge or release.
Recorded on issue #284, PR draft, active.md and autonomy_log.md.
PR body draft: PyAutoMind/tmp/profiling-contracts-pr.md.

## PR opened

https://github.com/PyAutoLabs/autolens_profiling/pull/285 at 45b3701, pending-release.
Task-specific override recorded in all four sinks. No merge/release performed.
