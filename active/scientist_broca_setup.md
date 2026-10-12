# Resumable local Broca setup for an independent Scientist

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoBroca
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: active
Issued: 2026-10-12
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/16

## Original request

WE have been doing work on making PYAutoScientist useful generally, can we continue that where we left it

## Recovered handoff

Continue `scientist_optional_organ_activation.md`. Starter conversational acceptance,
validated organ connections and Broca's live feed acceptance are complete. The next
bounded slice is owner-specific resumable setup. @PyAutoBroca owns implementation;
reuse @PyAutoScientist's existing connection validator without changing its contract.

## Proposed scope

Add an offline preview/apply setup command for an independently named, user-owned
Broca data directory. Initialize empty configuration and required state through
Broca-owned schemas, without copying maintainer measurements. Persist enough local
setup information to inspect and resume an interrupted setup; refuse conflicting
files and preserve existing records. Validate canonical repository identity and
explicit Pages location. Reuse existing check/render/state validation to produce a
local board and feed with truthful empty/unknown evidence. Explain the subsequent
publication and Scientist connection steps in a fresh-chat handoff.

No remote creation, publishing, schedules, assistant evaluation, Scientist lifecycle
UI, upgrades or collaborator access in this slice. Actual activation remains pending
until the existing public-feed connection gate succeeds.

## Approved implementation plan

- `broca/setup.py` (new): prepare a deterministic file plan; validate identity using
  the supplied canonical map; implement apply/resume with conflict detection and
  preservation of user changes. Track setup artifacts only, not a second task ledger.
- `broca/__main__.py`: expose setup preview/apply and owner validation through the
  existing CLI, allowing setup before `assistants.json` exists.
- Reuse `broca/collect.py`, `broca/records.py` and `broca/state.py` schema/validation
  owners; change them only if required to support truthful empty initial state.
- `tests/test_setup.py` (new): empty destination, interrupted resume, identical retry,
  conflicting configuration, invalid identity and byte-preserved existing records;
  integration check/render/feed validation for a differently named synthetic instance.
- `README.md` and a concise setup guide: explain preview/apply/resume, fresh-chat
  recovery and the explicit publication/connection boundary.

Route: start_workspace -> ship_workspace. Proposed branch:
`feature/scientist-broca-setup`. One implementation PR in Broca; human /prm.
Heart door on 2026-10-12: STALE (exit 1), planning permitted; ship gate remains due.

## Implementation handoff — 2026-10-12

Implementation is complete in `.worktrees/scientist-broca-setup/PyAutoBroca`,
branch `feature/scientist-broca-setup`, based on 0204cd5; changes remain uncommitted
because the refreshed Heart verdict is RED. New setup command validates identity,
previews/applies empty data, resumes interruptions without replacing files, and
writes a private fresh-chat handoff. Four initial files; no fabricated receipt or
resource inventory. Existing Scientist connection remains unchanged.

49 tests pass; owner check validates 4 assistants/18 records; saved board and feed
render successfully. Author review and diff check pass; no independent review
claimed. Logs and drafted PR body are in the task bundle parent (`pytest.log`,
`readiness.json`, `pr-body.md`). Exact RED reasons are recorded in active.md.
Next: live task-specific development override, four-sink recording, commit/push/PR.
No merge or publication authority. After merge, continue optional-organ publication
and lifecycle scope, then upgrades and collaborator acceptance.

## PR opened — 2026-10-12

User authorized the task-specific development override: "I authroize, go".
Recorded in issue comment, PR body, active.md and autonomy_log.md.
Commit 04660f4 pushed; PR https://github.com/PyAutoLabs/PyAutoBroca/pull/17 is open.
Earlier uncommitted/awaiting-override statements are superseded. Validation remains
49 tests plus existing owner check/render PASS. Next: human /prm with required
checks green; no merge or release authority carried by this development override.
