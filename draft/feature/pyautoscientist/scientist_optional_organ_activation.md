# Progressive optional organ activation

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoScientist
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: needs-slicing

Parent: `collaborator_led_pyautoscientist_adoption_pilot.md`.

After minimal starter: stable capability IDs and explicit configured locations, available/setup-incomplete/active/paused/needs-attention states. Prove one organ end to end with resumable setup, validation and honest absent versus stale evidence.

Start-dev must inspect current implementation and produce a bounded one-task/one-PR plan before execution. This is a next-step record, not an active repo claim.

## Agreed discoverability direction — 2026-10-11

Show relevant unconfigured project capabilities as grey available-to-add entries, including tutorials, workspace, assistant, workspace_test, profiling, inference and visualization. Clicking explains the purpose and offers a setup prompt; once created and validated, the entry becomes a normal repository link. Distinguish available-to-add, setup-incomplete and connected. Unavailable evidence for a connected resource must not make it appear uninstalled. Use stable capability IDs with configurable suggested names such as yourproject_workspace and yourproject_inference; suffixes are naming hints, never identity inference. Reuse the organ-linked resource cards shipped in Scientist PR #58. Implement with starter/optional-organ setup, not as a claim that missing repositories already exist.

## Discovery slice — 2026-10-11

`complete/2026/10/scientist-available-resources.md` (Scientist#67) implements the explicit available-to-add project-resource presentation contract and differently named offline example. It does not activate organs. Next: complete starter handoff validation, then select one organ for resumable setup and prove its evidence path; follow with record-preserving upgrades/rollback and collaborator acceptance.

## Validated connection slice — 2026-10-11

Starter conversational acceptance is merged (Mind#503). `complete/2026/10/scientist-organ-connection.md`, Scientist#71 / merged PR#72, adds preview/validate/apply for an already prepared public organ, with retry/no-op semantics and record preservation. 113 Python and 7 JS tests pass; independent review CLEAN. Fixture Broca connection/rendering and subsequent unavailable evidence are covered. This is the connection boundary, not full provisioning or activation state management.

The live Broca board is HTTP 200 but state.json is HTTP 404 (2026-10-11); its current Pages artifact contains only HTML. The new helper correctly refuses connection without changing the profile. Next prerequisite: `complete/2026/10/broca-state-feed.md`, keeping evidence ownership and communication scope in Broca. Then exercise a real validated feed connection, followed by resumable owner setup/provisioning and pause/needs-attention presentation. Keep record-preserving upgrades and actual collaborator validation separate.

## Broca feed implementation ready — 2026-10-11

Broca#14 / PR#15 (`complete/2026/10/broca-state-feed.md`) adds the missing shared state producer and site artifact. Explicit canonical publishing identity/custom Pages URL support independent naming; empty assistant configuration works. Saved collection/evaluation timestamps and their separate deadlines are retained; a newer collection cannot extend a passing evaluation. 34 tests pass, actual saved evidence renders/validates, and Scientist accepts/connects/renders the generated feed through local fixture transport. Independent re-review CLEAN.

Await human merge, then verify existing Pages deployment and the real HTTPS feed before claiming live connection acceptance. Publication is authorized by the user's request, but this judge-tier implementation still requires /prm. Next remains real endpoint connection acceptance, then resumable organ provisioning/owner validation and record-preserving upgrades.

## Broca feed live acceptance complete — 2026-10-11

Broca#15 merged and issue#14 closed; `complete/2026/10/broca-state-feed.md` records the result. Pages run 38172715636 built/deployed exact merge 0204cd5. The real HTTPS state.json returns 200 and validates; Scientist successfully connected, retried without changes and rendered it using a new synthetic profile with records preserved. Earlier missing-feed and pending-publication statements above are historical and superseded. Existing red evidence and October 8 collection time remain unchanged.

The published-feed/validated-connection prerequisite is complete. Next: resumable optional-organ provisioning and owner-specific setup validation, then record-preserving upgrades and actual collaborator acceptance. No real collaborator access or full activation workflow is implied.

## Resumable local Broca setup merged — 2026-10-12

`complete/2026/10/scientist-broca-setup.md` records Broca#16 / merged PR#17.
A differently named instance can preview/apply empty local Broca data, resume
interrupted file creation, refuse conflicting files and validate its owner feed.
49 tests and all applicable exact-head CI passed. Local setup retains unknown
evidence honestly and provides a private fresh-chat handoff. No remote provisioning,
publication, pause controls or full activation certification is implied.

Next: independent organ publication/activation and lifecycle presentation; reuse the
existing validated HTTPS-feed connection helper. Record-preserving upgrades and
actual collaborator acceptance remain their separate milestones.

## Independent publication preparation merged — 2026-10-12

`complete/2026/10/scientist-broca-publication.md` records Broca#18 / merged PR#19.
The publication command prepares only HTML/feed/Pages workflow in a new directory,
with explicit independent identity and validated owner state. 64 local tests and
all applicable exact-head CI passed. The workflow validates artifact membership
and destination identity; deployment remains an explicit adopter action.

No new repository or live independent endpoint was created. A destination means
the adopter-owned repository serving their public board/feed; PyAutoLabs' existing
host remains available. Select a real hosted pilot destination when appropriate.
Next implementation can cover remaining activation/pause/needs-attention
presentation; record-preserving upgrades and collaborator validation remain separate.

## Observation lifecycle merged — 2026-10-12

`complete/2026/10/scientist-organ-lifecycle.md` records Scientist#73 / merged PR#74.
Available catalogue, setup-incomplete entries, validated connection promotion and
pause/resume of Scientist observation are implemented. Pending/paused organs make
no server/browser feed requests; cached evidence cannot revive them. Owner jobs
remain untouched. 126 Python, 7 Node and five browser cases passed; exact-head CI
passed. Profile changes require rendering/publishing and reloading the page.

The previously pending observation-lifecycle implementation is complete. Full live
independent-organ acceptance is still unproven: select an adopter/synthetic hosting
destination and exercise publication through connection/resume when appropriate.
Record-preserving upgrades/recovery and actual collaborator acceptance remain their
separate programme milestones; no collaborator access or live deployment is implied.
