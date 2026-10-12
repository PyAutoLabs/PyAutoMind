# Shipped: record-preserving Scientist runtime upgrades

Completed: 2026-10-12
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/75
PR: https://github.com/PyAutoLabs/PyAutoScientist/pull/76 (MERGED)
Merge: 9eb3bafd672ed313be8da9548db87bf707625c56

Implemented private exact-revision Scientist/Brain runtime selection with preview/apply initialization, upgrade and rollback, plus a check/render launcher. Validates prepared clean local checkout pairs against existing configuration offline; retains one previous pair and verifies declared protected records. Rollback uses current records, never replaces them with old copies. Includes the starter-linked upgrade/recovery guide.

Validation: 142 Python and 7 Node tests passed, including synthetic preservation/failure cases and real owner-validator upgrade/recovery. Exact-head GitHub Board tests run 38268112457 and its tests job passed; GitHub reported clean mergeability. Feature head c7e04e0c9932e82797d7548f323d61d8d53301d5 is an ancestor of origin/main. Heart at ship was STALE solely for missing current-source release rehearsal; no readiness rerun at merge.

Limits: trusted candidate Python executes; fingerprints detect drift and are not a sandbox or backup. Protection is limited to declared paths. Retained checkout pairs and launcher are needed for recovery. This covers the minimal Scientist + Brain runtime, not environment/package or owner-organ upgrades, arbitrary schema downgrades, hosted rollout, or real collaborator acceptance. Those acceptance milestones remain separate. No independent review claimed.

Local test logs and readiness evidence retained under tmp/scientist-record-preserving-upgrade/.

## Original prompt

# Pin, upgrade and recover an independent Scientist runtime

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoScientist
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: active
Issued: 2026-10-12
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/75

## Original request

do next task

## Context

Bounded implementation of `scientist_record_preserving_upgrades.md`, following
Scientist PR#74 and Broca PR#19. Independent config and organ data already live
outside framework checkouts. @PyAutoScientist owns this local runtime selection
helper; Brain is a pinned dependency, not an implementation target. Hosted pilot
acceptance remains separately recorded and is not claimed by upgrade tests.

## High-level plan

- Record the chosen Scientist and Brain checkout paths and exact Git revisions in
  a private instance runtime manifest.
- Preview an upgrade to an already prepared second pair, validate compatibility
  with existing configuration offline, then explicitly apply the selection.
- Preserve the previous selection for recovery; rollback changes framework choice,
  never restores old user configuration over newer records.
- Demonstrate upgrade, failed upgrade and recovery with unchanged project, task,
  research and Broca records in an independently named synthetic instance.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

1. Add `scripts/instance_runtime.py` with initialize, upgrade, rollback and check
   commands. Initialize/upgrade/rollback preview by default and require --apply
   to write. The manifest is separate from instance.json and references the
   canonical map and profile rather than copying them. Record exact Scientist/Brain
   revisions, current selection and one previous selection. Reject dirty tracked
   code, invalid identities/paths and changed inputs before atomic replacement.
2. Require already prepared local Git checkouts and resolve exact commits; no
   fetch, pull, checkout, reset, environment installation or network calls. Both
   framework pairs remain available so switching does not mutate shared checkouts.
   A selected revision mismatch fails closed until deliberately reviewed.
3. Use the selected pair's existing --check-instance validator in a subprocess
   with explicit PYAUTO_BRAIN and profile/map paths. Bound execution, disable
   bytecode writes, report validation failure and retain the current manifest.
   Record-preservation checks cover the instance files and explicitly supplied
   record directories, with documented treatment of Git internals and symlinks.
   These checks detect drift; they are not a sandbox for untrusted framework code.
4. Provide a launcher/check path that actually uses the manifest's selected
   Scientist/Brain pair. The manifest must influence execution, not be decorative
   version metadata. Keep normal feed-fetching render an explicit user action;
   upgrade and rollback validation remain offline. The same launcher can select
   the old pair after recovery, without changing instance/profile/project records.
5. Rollback validates the previous pair against current configuration before
   switching. If newer configuration is incompatible, report it and leave the
   selection and records alone. Explain manual recovery from retained checkouts
   and the original manifest if the launcher itself becomes unusable. Do not
   promise arbitrary schema downgrade or conflict-free framework updates.
6. Add `tests/test_instance_runtime.py`: synthetic local Git pairs, exact pin
   checks, successful upgrade/rollback, invalid candidate, missing previous pair,
   incompatible current config, concurrent-input change and write-failure cases.
   Hash fixture instance/Mind/research/Broca files before and after. Validate with
   real current owner scripts as well as fault-injection fixtures.
7. Add an upgrade guide and update STARTER.md with registration of existing
   instances, preview/apply, fresh-chat resumption, selected-pair invocation and
   recovery. Keep paths/manifests private; no publication-bundle inclusion.

## Acceptance and limits

One Scientist PR. Framework selection and recovery are implemented for the minimal
Scientist + Brain runtime only; no package/environment upgrades, owner-organ code
upgrades, schema migration, hosted rollout or collaborator access. Existing
instance and owner records are reused and preserved. Record hashes are evidence
for the declared protected paths, not an assertion about every file on the host.

Scientist main is clean at 396f3e0; no active claim. The old DNA worktree is clean
and already contained in main; leave it untouched. Proposed branch:
`feature/scientist-record-preserving-upgrade`, bundle under `.worktrees/`.
Route start_workspace -> ship_workspace. Heart STALE only for missing current-source
release rehearsal; no RED or YELLOW reasons. Plan awaits explicit approval.

Plan approved by user: "go", 2026-10-12.

## Implementation handoff — 2026-10-12

PR https://github.com/PyAutoLabs/PyAutoScientist/pull/76 at c7e04e0 on
feature/scientist-record-preserving-upgrade; task bundle under .worktrees/.
instance_runtime.py implements preview/apply initialize/upgrade/rollback and a
check/render launcher selecting exact Scientist/Brain revisions. Only the private
manifest is intentionally updated; candidate validation is offline, rollback uses
current configuration, and protected records are checked without restoring old data.
Pairs must be local clean Git roots. No fetch/pull/reset or environment changes.

142 Python + 7 Node PASS; real owner validator rerun after shallow-CI adaptation
PASS; project/lifecycle checks and author review PASS. Evidence: bundle pytest.log,
node.log, real-runtime-test.log and readiness.json. Heart STALE only for absent
current-source release rehearsal. No independent review claimed.

Boundaries: trusted candidate Python is executed; fingerprints detect drift, not
sandbox or backup it. Protected paths are explicit, Git metadata excluded, symlinks
refused. Retain both checkout pairs and a known-good launcher for recovery.
Next: human /prm, then update programme milestones; hosted and collaborator
acceptance remain unproven and owner-organ/environment upgrades remain separate.
