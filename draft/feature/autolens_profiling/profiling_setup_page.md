# Browse profiling by dataset, model and instrument

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-05

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
