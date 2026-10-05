# Profiling project setup browser

Merged autolens_profiling#379 (4832679a61121291ea581c61f3f187b9cf3e6776), closes #378. Exact head e84086ae00129e9af4c2fbd0df47024e377622b1 passed lint run37298134702, all jobs successful. User explicitly authorized prm on 2026-10-05.

Project page now routes dataset/model/instrument/configuration to exact captured profiling evidence, with shared theme, linear metric groups and collapsed qualification/evidence. Catalogue descriptors make source configurations readable. Original measurements/v1 payloads unchanged; archives remain unreviewed. No baseline execution or acceptance.

Validation: 1061 full tests (5 skipped), 48 final focused tests, Chromium desktop/mobile/history/failure/keyboard checks, seven smokes, Ruff/metadata/Pulse contracts, inline code/visual review. Heart RED override recorded at ship; release remains blocked by `release validation FAILED (stage integrate)`.

Parent Phase 3a complete. Pulse front-page consumer is separate #12; source taxonomy and Brain routing follow in Phase 4.

## Original prompt

# Browse profiling by dataset, model and instrument

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-05
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/378

Primary repo: @autolens_profiling
Classification: standalone workspace; no library API changes.
Branch: feature/profiling-setup-page
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 3.
Dependency: autolens_profiling#377 catalogue producer; merge before starting source edits.

## Approved high-level plan

1. Replace the project's temporal-first page with dataset/model disclosures and
   instrument/configuration selectors backed by the v2 catalogue.
2. Show exact runtime, breakdown, compile and memory values with linear charts,
   visible qualification and unknown coverage; reveal supporting evidence last.
3. Match the shared Heart-family theme, including Pulse SVG hero and board width.
4. Support deep links, browser history, accessible controls and no-JS evidence.
5. Validate interactions and desktop/mobile rendering, then ship a project PR.
   The separate Pulse front-page migration follows this project PR.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

- Add scripts/misc/tooling/setup_page.py and browser assets under catalogue/;
  build_dashboard.py renders the new index from the v2 index and assets.
  Preserve v1 data contracts, archived results, comparison pins and drift logic;
  remove temporal graphs from the default human-facing page only.
- Import the actual shared PyAutoBrain/board/_theme.py through resolved checkout
  paths; CI and build jobs that regenerate the page must check out Brain.
  Fail with an actionable message if the shared theme cannot be found; no silent
  duplicated theme. The shared Pulse icon needs no new raster asset.
- Navigation: project autolens → all dataset families and script categories →
  model → labelled instrument and exact source-row configuration selectors.
  Show expected baseline cells alongside archive candidates; never stitch
  source-isolated legacy setups into a synthetic CPU/GPU comparison.
- Fetch only the chosen setup shard, verify declared hash/count/setup/record IDs,
  guard stale asynchronous responses, and provide actionable load/error states.
  Escape evidence metadata; resolve source links against the publication's
  captured repository revision. Metric units/axes and uncertainty remain intact.
- Display numeric values and linear relative bars within compatible unit/axis
  panels. Separate first-call/batched/single-call metrics and component breakdown;
  do not rank incompatible records or promote an unreviewed result.
- Render configuration metadata (including source pixels/PSF and unknown reasons),
  qualification disclosure, scoped advice, static-estimate distinction and an
  evidence disclosure below the results. No global wall of evidence links.
- Hash URL state and history restore dataset/model/instrument/setup choices.
  Native disclosures/selects and status announcements support keyboard use;
  no-JS fallback exposes setup/source links without remote scripting.
- Test output escaping, unchanged v1 semantics, missing devices, empty/error states,
  navigation/filter consistency, late-response races, exact shard integrity,
  deep-link back/forward and responsive overflow. Use the installed browser
  harness if available; run appropriate Python suite and repository checks.
- Follow-up Pulse PR reuses this browser's contract/conventions, changes campaign
  controls, narrows the layout and switches its registered summary to v2.

## Authorization and original request

The parent Phase 3 plan is already approved. The current live instruction
continues into this phase after the Phase 2 merge; no bulk profiling authorized.

Original request (verbatim):

$prm and continue

## Branch survey and routing

2026-10-05: canonical autolens_profiling main at merged catalogue dcfa056e;
only pre-existing untracked dataset/abell_1201, preserved. No open PRs or active
repo claims. Historical worktrees are out of scope. Workspace-only classification
confirmed by Brain feature decision; generic API-risk heuristic is not a library
scope. Phase 3 is already split into project then Pulse as the parent approved.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-page.

## Implementation checkpoint — 2026-10-05

The project browser is implemented in its worktree. `setup_page.py` uses the real
shared Brain theme and binds the catalogue by SHA-256. `catalogue/browser.js/css`
provide dataset/model disclosures, instrument/exact-configuration selectors,
record-derived labels, lazy verified shards, stale-response protection, deep-link
history, stale-link refusal, native keyboard controls and no-JS evidence. Navigation
collapses to the selected path. Runtime is first; remaining axes, configuration,
qualification, hazards and evidence expand on demand. Single-call, per-replica
batch and batch-wall bars have separate groups. Numeric labels are readable with
exact values preserved in qualification details and original evidence.

Only root catalogue descriptors were added (actual axes/devices/precisions for
labels). All measurement shards, results and v1 JSON feeds are unchanged. CI and
profile generation check out Brain for the theme. CI adds pinned Playwright 1.63.0
and the actual browser test; no profiling/compute is dispatched.

Validation: 1061 full tests passed, 5 skipped (18 warnings); 48 final targeted
Python tests after descriptors changed. Final Chromium suite passes navigation,
selected values, history/deep links, stale-link refusal, keyboard, four widths
320/390/768/1280, dark mode, corrupted shard/retry, delayed responses, missing root
catalogue and no-JS fallback. Mobile and desktop screenshots visually reviewed.
Seven existing section smokes pass. Ruff, README/wiki/results/wall checks and
idempotent page/catalogue generation pass; Pulse validates all index/shards.
Inline code/visual review only; no independent-review claim.

PR description prepared at `.worktrees/profiling-setup-page/phase3-pr-body.md`;
previews and logs are in that task root. Browser tests stop their own servers;
the temporary manual HTTP server was terminated. The shared browser test tooling
is under `.worktrees/profiling-browser-tools` for reuse by the Pulse phase.

Heart still reports RED `release validation FAILED (stage integrate)`; #378 needs
its own live shipping override after this evidence. The phase2 #376 override was
recorded and exhausted by the successful #377 merge/close-out. No #378 source
commit, push, PR or merge yet. Next after project shipping: separate Pulse front
page task per approved parent Phase 3, then later model-first script migration.
