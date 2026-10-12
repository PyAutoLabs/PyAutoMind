# Independent Broca publication bundle

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoBroca
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: active
Issued: 2026-10-12
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/18

## Original request

ok do next task

The user then said "conitnue" in response to the task-specific Heart RED
planning checkpoint. Current reasons: `PyAutoFit: 1 commit(s) behind origin`,
`PyAutoGalaxy: 1 commit(s) behind origin`, `PyAutoLens: 1 commit(s) behind origin`.
This permits continuing planning; the new detailed plan awaits approval.

## Context

Continue `scientist_optional_organ_activation.md` after
`complete/2026/10/scientist-broca-setup.md` (Broca PR#17). Local setup and an
existing public feed connection are proven. Independent publication needs a
portable destination that does not copy the maintainer checkout or private setup
manifest. @PyAutoBroca is the only implementation target. Scientist's existing
connection helper is reused without changing it.

## High-level plan

- Prepare a standalone publication directory from the independent instance's saved
  evidence, with canonical repository identity and explicit Pages URL.
- Include only reviewed HTML/feed and a minimal Pages workflow; retain setup paths,
  source records and private handoff files in the local data directory.
- Make the board work link point to the configured independent repository.
- Validate the bundle and document deployment plus the existing Scientist
  connection check using a differently named synthetic instance.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

1. Add `broca/publication.py` and a `publication` subcommand in
   `broca/__main__.py`. Require explicit canonical map/key, Pages URL, Brain path
   and new output destination. Preview by default; apply creates a new directory
   with `site/index.html`, `site/state.json` and `.github/workflows/pages.yml`.
   Validate owner records/receipts and shared state before writing. Refuse existing
   or symlink output destinations; rebuild to a new directory for review rather
   than overwriting a publication checkout. No git/network operations.
2. Reuse `broca/board.py` and `broca/state.py` producers. Add explicit repository
   identity to the renderer's work destination, preserving the live default for
   existing callers. Keep names and URLs escaped; do not infer identity by suffix.
3. The generated Pages workflow uploads only `site/`, has minimal permissions,
   validates the expected two-file artifact, and deploys only for the intended
   default branch or an explicit dispatch. No framework checkout, collection,
   evaluation, schedules or private data directory is needed by the publisher.
4. Add `tests/test_publication.py`: preview has no writes; malformed identity,
   bad owner evidence and unsafe destinations fail; exact output allowlist excludes
   setup paths and records; identity-specific links and feed agree; source hashes
   remain unchanged. Check workflow semantics using the existing workflow tests'
   conventions. Run full Broca suite and existing check/render smoke.
5. Extend `docs/setup.md` and add a publication guide: inspect bundle, choose public
   destination and default branch, enable Pages via Actions, verify deployed HTTPS
   feed, then run Scientist connect_organ preview/apply. Document that HTML content
   still needs a visibility review; an artifact allowlist is not a privacy scanner.

## Boundaries and acceptance

One Broca PR. No actual repository creation, upload or deployment in this slice:
the independent destination/owner has not been supplied. No claim of live independent
activation from local tests. Pause/needs-attention controls, record-preserving
upgrades and collaborator validation remain later milestones. Publishing the bundle
requires a concrete destination and reviewed content; the existing PyAutoLabs Pages
workflow stays unchanged.

Branch survey: Broca clean main at f6e04b0; no conflicting active claim or linked
worktree. Proposed branch `feature/scientist-broca-publication`; task bundle under
`.worktrees/scientist-broca-publication`. Route start_workspace -> ship_workspace.

Plan approved: "yeah I approve, go" (2026-10-12).

## Implementation handoff — 2026-10-12

PR https://github.com/PyAutoLabs/PyAutoBroca/pull/19 opened at 3c387cc on
feature/scientist-broca-publication, under .worktrees/scientist-broca-publication.
Publication preview/apply creates exactly HTML/feed/workflow, validates owner state,
refuses unsafe/existing destinations, and uses explicit canonical board work links.
Generated workflow validates two-file site membership and publishing identity before
upload, with default-branch deployment guard. Existing live publishing workflow is
unchanged. 64 tests pass; owner check (4 assistants/18 records), board/feed render
and author diff review pass. Logs: task bundle pytest.log and readiness.json.
Task-specific RED authorization and unchanged reasons recorded in four sinks.
No independent review claimed; no real destination chosen or deployed.
Next: human /prm, then select independent deployment destination or continue the
remaining activation-state work. Upgrade and collaborator milestones stay separate.
