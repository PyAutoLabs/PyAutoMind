# Complete profiling navigation and useful dashboard output

Type: feature
Target: autolens_profiling
Repos: autolens_profiling, PyAutoPulse
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07
Status: plan approved; Phase A implemented, awaiting Heart acknowledgement to ship

## Phase progress

Human approved the concrete plan with "ok go". Phase A is issue
https://github.com/PyAutoLabs/autolens_profiling/issues/387; active prompt:
active/profiling_dashboard_completion.md. Implementation and validation complete;
shipping awaits the exact Heart YELLOW acknowledgement recorded there. Phases B/C
remain pending. No merge, deployment, scientific campaign or Fable review occurred.

## Current direction

The human superseded the Fable handoff with: "just go without fable not worth the faff on this on".
Proceed with the current Codex session; no Fable review is required or claimed.
The review and plan below supersede the earlier handoff request retained as history.

## Direct review and implementation plan — 2026-10-07

Real Chromium checks of BOTH live sites reproduced the same default MGE/HST
problem without console or failed-request errors: a breakdown-only archive run
is selected, the runtime panel opens with no measurements, and the breakdown
panel containing all nine displayed metrics is collapsed. There are six
imaging/MGE/HST shards containing runtime measurements and 47 HST run choices.
Screenshots are local scratch at tmp/profiling-browser/{project,pulse}-mge.png.
This is a verified presentation defect, not an absent-result or deployment diagnosis.

Another confirmed defect is in both browsers' advice() handling: unbound findings
are filtered by '/<dataset>/' in their evidence path. All twelve exported findings
point to results/hazards/hazards_index.json; consequently none passes an imaging
filter. Empty exact-setup hazard bindings and this discovery bug are separate.

Requirement assessment:

| Requirement | Delivered | Remaining |
|---|---|---|
| Dataset/model source organization | 80 canonical script/helper moves | Remove compatibility hierarchy after caller audit; migrate stale docs |
| Dataset/model/instrument browsing | Working on both live sites | Useful overview before choosing an individual archive row |
| Runtime/breakdown/compile/memory visibility | Typed records and verified shards | Axis/device availability, useful defaults, populated panels visible |
| Hazards beside relevant likelihoods | Detectors and archived findings | Explicit discovery mapping, fix hidden unbound findings, justified exact bindings |
| Exact provenance and qualification | Preserved | Keep throughout UI changes; unknown compatibility stays unknown |
| Fresh accepted baseline | Readiness specification only | Remains a separate campaign, not required to expose existing evidence |

Classification: workspace/organ feature plus corrective UI changes; no library
API or scientific numerical changes. Brain feature routing recommended phasing;
the phases below replace its generic automatic stubs with task-specific scope.

### Phase A: useful project dashboard (autolens_profiling)

Suggested branch: feature/profiling-dashboard-completion.

1. Add a model/instrument overview in catalogue/browser.js and browser.css.
   Enumerate available measurement axes and recorded devices from evidence_shards;
   show counts and labelled run choices before asking users to choose one exact
   historical configuration. Keep unknown devices explicit. Preserve exact-run
   deep links, URL history and lazy hash-verified loading.
2. Make initial selection prefer available runtime evidence deterministically,
   retaining explicit reference preferences within that axis; never rank by
   speed or pretend that reference candidates are scientifically accepted.
   Open a populated panel if the chosen evidence lacks runtime. Clearly
   distinguish 'absent in this run; other runs available' from no recorded
   evidence anywhere in this model/instrument scope. Other axes should be
   directly reachable without hunting through dozens of opaque run options.
3. Fix hazard discovery using explicit registry metadata in catalogue/registry.json
   and scripts/misc/tooling/build_catalogue.py, not filename substring guesses.
   Separate related/unverified findings from exact version-qualified bindings.
   Audit raw findings before adding any exact binding; no required binding count
   if historical evidence cannot establish exact applicability. Expose shared
   component findings under an explicit shared scope rather than every model.
4. Update catalogue/README.md and generated setup wiki/dashboard via their
   builders. Preserve v2 identity/provenance semantics; any additive discovery
   metadata must be optional for existing consumers. Do not fuse historical rows.
5. Extend scripts/misc/test/browser_setup_page.cjs and relevant catalogue/UI
   tests with MGE and rectangular examples that lack reference candidates,
   axis navigation, visible values, related hazards, unknown metadata, failed
   loads, keyboard/history and responsive checks. Retain raw-result hashes.

### Phase B: finish source/documentation consolidation (autolens_profiling)

Suggested branch: feature/profiling-layout-completion; follows Phase A.

1. Audit all 80 legacy routes and active callers in project scripts, HPC, CI,
   tests, README/wiki, Brain profiling and assistant lookup. Preserve historical
   result/provenance text; update current usage guidance.
2. Retire thin wrapper files and obsolete measurement-first directories once
   their active callers use canonical paths. Keep legacy aliases in
   catalogue/script_routes.json for historical identity/output mapping.
   Change _script_routes.load_routes so aliases need not exist on disk;
   remove wrapper execution support only after import/caller audit proves safe.
3. Move model-specific hazard documentation beside mge/ and rectangular/;
   retain shared detector/framework documentation in misc/hazards and deliberately
   document dataset-free component probes. Do not duplicate scientific bodies.
4. Update tests/migration docs, run routing/import/HPC dry-run checks plus
   appropriate full lint/tooling checks, and prove archived results unchanged.

### Phase C: matching Pulse experience (PyAutoPulse)

Suggested branch: feature/profiling-browser-completion.

Coordinate/serialize with active dashboard-checkin-prompts (Brain #484), which
claims Pulse. Do not edit its worktree or claim Pulse concurrently without human
coordination. Once available, adapt pulse/setup_browser.{js,css,py} to Phase A's
overview, selection, populated-panel and hazard-discovery behavior, preserving
captured commit/shard validation and unrelated check-in wording. Validate with
Pulse's contract and real browser tests; regenerate via its own renderer.

### Acceptance and delivery

- Imaging MGE/HST and rectangular/HST show available measurements immediately;
  runtime, breakdown, compilation and memory evidence is reachable by named axis.
- Device, precision, scientific configuration, software and measurement method
  remain visible per run; incompatible runs are never presented as one benchmark.
- Related hazards are discoverable with explicit applicability qualifications;
  unbound does not become 'safe', and dataset-free findings are not misassigned.
- Both browsers pass real-data desktop/mobile, keyboard, deep-link, corrupt-shard
  and missing-data checks; generated artifacts match their builders.
- Current source/doc navigation uses dataset/model folders, active callers work,
  and archived results/provenance are unchanged.
- One issue/PR per bounded phase; repeat readiness at shipping. Source completion
  is distinct from publication. Recheck live pages after an authorized merge and
  deployment, without timers or background watchers.

Tier: judge — merge mode: human /prm.

Survey: profiling main fef5f28 matches fetched origin/main, no other worktrees,
only untracked dataset/abell_1201/ (preserve). Pulse main bfff2c8 matches fetched
origin/main, clean; existing feature/dashboard-checkin-prompts worktree/claim.
No implementation issue or worktree yet. Heart entry remains YELLOW; full feed
saved locally at tmp/profiling-completion-heart.txt. Read current ship gates later.

## Earlier Fable handoff (historical context)

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
