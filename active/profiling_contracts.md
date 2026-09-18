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
