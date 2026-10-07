# Complete profiling navigation and useful dashboard output

Type: feature
Target: autolens_profiling
Repos: autolens_profiling, PyAutoPulse
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07
Status: pre-implementation review requested from Fable

## Next action: Fable review

Review the process, previous work and remaining work before implementation.
This packet was prepared by a GPT-6 session; no Fable review has occurred.
The human explicitly selected a handoff to Fable rather than a substitute reviewer.
Do not start source changes or dispatch profiling jobs during this review.

Read workspace AGENTS.md and the relevant repository instructions. Review the
original intent against the delivered user experience, not just phase completion
records or passing contract tests. Verify the evidence below independently.
Return a concise assessment, concrete remaining scope, a phased implementation
plan, and observable acceptance criteria. Identify what requires new measurements
versus what existing evidence can already support. Do not broaden into unrelated work.

Primary implementation candidate: @autolens_profiling; consumer changes may
require @PyAutoPulse. Brain/assistant callers require an audit before removing
compatibility paths; add implementation repos only when that audit requires it.
Use start-dev after the review and the applicable plan approval. No issue,
worktree, implementation branch, merge or publication has been created for this task.

## Original requests (verbatim)

We rrecently did a lot of work restructing autolens_profiling in order to improve its dashboard. First, I think there are aspects of the refacotr which are incomplete, for example there is still a "hazards" folder with mge / pixelization stuff in, but all hazards stuff should be specific to each likleihod function. Same for imaging/likelihood_runtime and imaging_likelihood_breakdown and similar packages, It feels like the refactor only got half way through?

ok yeah then lets continue, and before we start review the process, previous work and remaining work with Fable. Also, the dashboard does not contain any of the expected output and information att he moment, so maybe it never fully finished and got ot that?

Review-routing answer: Prepare a review handoff for Fable

## Previous work to inspect

Mind records under complete/2026/10/:

- profiling-setup-redesign.md: original full request, architecture and six-phase plan.
- profiling-setup-contract.md and profiling-setup-catalogue.md: transport and adapters.
- profiling-setup-page.md and profiling-setup-browser.md: project/Pulse browser scope.
- profiling-model-layout.md and profiling-catalogue-routing.md: source migration and callers.
- profiling-setup-wiki.md and profiling-setup-advice.md: documentation and assistant.
- profiling-baseline-readiness.md and profiling-baseline-campaign.md: later measurement boundary.

The parent says all six approved implementation phases merged on 2026-10-06.
Actual baseline collection, scientific acceptance and temporal charts were
explicitly deferred. That does not establish that the existing evidence is
presented usefully. Separate delivered phase scope from original product intent.

## Evidence gathered on 2026-10-07

Checkout anchors (recheck before proceeding):

- lens/autolens_profiling main: fef5f28da520df4a357805647cb0f093d5b22583.
- organs/PyAutoPulse main: bfff2c8f86c69eaf0fa575872b5614a7d748e4aa.
- Profiling has untracked dataset/abell_1201/; preserve it.
- Mind active.md claims PyAutoPulse and PyAutoBrain for dashboard-checkin-prompts,
  Brain issue #484, feature/dashboard-checkin-prompts. Its stated scope is
  approved check-in wording, not restructuring. Coordinate before claiming either.
- Heart entry: YELLOW — Release YELLOW; monitoring RED, 39/100, 154 unresolved,
  updated 17h ago. This is a transient observation; re-read at workflow gates.

### Source layout

Phase 4 moved 80 scientific scripts/helpers and retained thin compatibility
wrappers by explicit design. All Python files in these old imaging directories
are wrappers calling _script_routes.run_legacy:

- scripts/imaging/hazards/: 2 wrappers.
- scripts/imaging/likelihood_runtime/: 8 wrappers.
- scripts/imaging/likelihood_breakdown/: 23 wrappers.

Examples: hazards/pixelization.py routes to rectangular/hazards.py;
hazards/mge_nnls_capture.py routes to mge/hazards_nnls_capture.py.
See catalogue/script_routes.json, catalogue/migration.md and _script_routes.py.
The loader currently requires both legacy and canonical files to exist; wrapper
retirement therefore needs routing-contract and test changes, not just deletions.

catalogue/README.md says removal follows an explicit decision after Brain and
assistant migration, with no automatic expiry. scripts/imaging/hazards/README.md
still describes that old directory as the fixture home; scripts/misc/hazards/README.md
still directs dataset fixtures to scripts/<dataset>/hazards/.
Shared detectors and dataset-free component/matrix probes need a deliberate home;
do not indiscriminately duplicate them into every likelihood directory.

### Dashboard and evidence

Fetched https://pyautolabs.github.io/autolens_profiling/index.html and catalogue.json
with Python urllib: both byte-identical to the current local dashboard files.
One imaging/Delaunay/HST reference shard was also live and byte-identical.
This rules out a stale project deployment for those files at inspection time;
it does not prove all browser interactions or the live Pulse deployment work.
The web tool could not access the page, and no browser execution was performed.
Node is available, but Playwright was not resolvable in the current environment.

Local dashboard/catalogue.json contains:

- 540 setups: 508 legacy_or_experimental, 3 reference_candidate, 29 planned_baseline.
- 508 shards containing 20,709 metric records; 112 records in the root index.
- 435 planned measurement slots. These are deliberately unmeasured placeholders.
- 0 setup-bound hazards and 12 unbound_findings; catalogue/registry.json has
  hazard_bindings: []. Applicability must be established, never guessed from names.
- Imaging MGE: 56 setups, no reference candidates. Imaging rectangular: 102
  setups, no reference candidates. Imaging Delaunay: 100 setups, two HST candidates.

The exporter explicitly isolates legacy setup identities to individual source
rows because metadata is insufficient for cross-file joins (build_catalogue.py).
Both project catalogue/browser.js and Pulse pulse/*js select one such setup/run
at a time. Panels say 'Not measured for this configuration' for axes absent
from that selected run. Only the runtime panel initially opens. This can conceal
relevant evidence under other run selections; it is not proof that data is absent.
Some shards do contain multiple axes: 92 have runtime/breakdown/compile/memory.
Do not claim every shard is single-axis or that the dashboard has no numbers.

Existing browser tests include numeric visibility and equality to the selected
shard, navigation/history, corruption/error handling and empty baseline states.
Review why these tests can pass while the intended scientist-facing overview
remains unsatisfactory; do not dismiss prior validation as nonexistent.

## Questions Fable must resolve

1. Which original requirements were fulfilled, narrowed, deferred or omitted?
   In particular: likelihood/instrument overview with runtime by device,
   breakdown, compilation, memory, hazards and configuration details.
2. Is the reported emptiness an interaction/rendering bug, poor defaults and
   discoverability, source-row fragmentation, missing adapters, genuine missing
   measurements, or several of these? Inspect both live dashboards with a browser.
3. How should related evidence be browsed together without pretending different
   runs, revisions or configurations are equivalent? Consider a model/instrument
   overview with explicitly separate runs and compatibility labels; determine
   whether exact setup identity and evidence-run identity need separating further.
4. What existing hazards can be bound with evidence, what remains unbound, and
   how can shared component findings remain discoverable without false applicability?
5. Can the compatibility hierarchy now be retired? Audit active callers across
   scripts, HPC, CI, docs, Brain and assistant; preserve historical provenance.
6. What completion criteria should replace 'all phase PRs merged'? Specify
   representative real-data browser journeys, displayed values and units, device
   distinctions, hazard coverage, understandable gaps, and published-site checks.

## Constraints and expected return

Preserve scientific bodies/defaults and archived result paths/content. Do not
silently join incompatible measurements, accept archive records as baselines,
invent GPU VRAM from host RSS, dispatch CPU/GPU runs, or restore temporal charts.
Review may recommend a later campaign but must not use one to avoid displaying
existing useful evidence. Generated dashboards/wiki must come from their builders.

Return findings with file/line evidence, a requirement-to-delivery gap table,
prioritized bounded tasks (one issue/PR per repo phase), and explicit acceptance
criteria. Explain any scientific ambiguities that require human decisions.
Tier: judge — merge mode: human /prm.
