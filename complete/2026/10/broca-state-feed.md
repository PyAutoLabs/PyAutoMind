# Broca shared state feed

- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/14
- shipped: 2026-10-11
- epic: scientist-adoption-pilot
- pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/15

Human /prm authorized merge and full close-out. Head 43d0201c69e438f99f8a0b50081227620bb998d1 merged at 0204cd5ab943d7079667d9def193c92b57b21cf9; ancestry proven. Exact-head CI: Tests push 38172423590 and PR 38172433146 passed; Pages 38172433318 build passed, deployment intentionally skipped on PR (not a test). No pending/failing test legs.

Broca now publishes Brain's shared state contract from saved receipts/records. Explicit canonical publishing identity, configurable URL, assistant-free communication configuration, separate collection/evaluation clocks, conservative same-day outcomes and validity bounded by passing-evaluation deadlines. Guides/workspaces are inventory, not quality results. No source copying, collection, execution or evidence rewrite. Local 34 tests; saved-data check/shared validator and Scientist integration passed. Independent re-review CLEAN after expiry regression fix.

Published successfully by Pages run 38172715636 at the exact merge SHA (build and deploy passed). Real https://pyautolabs.github.io/PyAutoBroca/state.json returned 200 and passed the shared validator. Scientist's actual HTTPS connection helper applied to a new synthetic Mira profile; identical retry was a no-op, collection/rendering succeeded and the research note remained unchanged. No live Scientist user configuration was modified. Status remains red from saved evidence and updated remains 2026-10-08T12:58:48+00:00; deployment did not freshen or clear it.

Evidence archived under tmp/broca-state-feed/, including live-state.json, verify_live.py, live-scientist fixture/HTML and local test/artifact logs. Heart ship gate was STALE only (no current-source rehearsal); no software release claimed. Next epic phase: resumable optional-organ provisioning/owner validation, then record-preserving upgrades and real collaborator acceptance. Connection publication prerequisite is complete.

## Original prompt

# Publish Broca's shared organ state feed

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/14
Target: PyAutoBroca
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge
Priority: high

## Original request

> ok great, conitnue work

Follow-up discovered while implementing Scientist#71 / PR#72. Keep this within the existing adoption epic and Broca expanded communication/documentation scope.

## Observed prerequisite gap

On 2026-10-11, the configured public Broca dashboard https://pyautolabs.github.io/PyAutoBroca/ returns HTTP 200; state.json beneath it returns HTTP 404. Current main 1282e85 renders site/index.html through broca/board.py; Pages uploads site/, and source inspection finds no shared state producer. Scientist's existing collector and new validated connector require the shared Brain state contract. The connector correctly leaves an unconfigured profile unchanged.

## Next bounded implementation

@PyAutoBroca should publish a minimal accurate state.json alongside its HTML using Brain's shared state builder/validator. Derive summary and collection dates from owner records; do not confuse render time with evidence collection, invent scientific/assistant quality verdicts, or mark inventory as validation. Preserve project source ownership and the broad guides/workspaces/docs/tutorials scope, with assistants separate. Include configurable canonical repo identity and Pages location so independently named instances work; inspect existing config before adding a new surface. Reuse existing Pages artifact workflow. Test empty, stale/missing and malformed evidence, renamed identities and artifact contents; after authorized publication verify Scientist's declared-identity/location connection against the real feed. No recollection, assistant execution, external messages, project cloning or full-roadmap dependency.

Use start-dev to inspect current work and produce one bounded issue/branch/PR. This record claims no repo and starts no publication. After this prerequisite, continue resumable optional-organ provisioning and owner validation; the published feed alone is not a full activation workflow.

Current authorization: "ok do that" — implement the feed prerequisite through the existing judge-tier PR workflow.
