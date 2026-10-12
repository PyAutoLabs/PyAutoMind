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
