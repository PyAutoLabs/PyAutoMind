# Publish Broca's shared organ state feed

Type: feature
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
