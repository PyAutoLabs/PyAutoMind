# Setup-first profiling: dashboard, evidence catalogue, scripts and assistant

Type: feature
Target: pyautopulse
Repos: PyAutoPulse, autolens_profiling, PyAutoBrain, autolens_assistant
Difficulty: too-large
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-05

## Intent and authorization

The human approved the full direction after a read-only investigation. Implement
the complete architecture, including large-scale restructuring where justified;
do not reduce this to dashboard cosmetics. Source implementation has not begun.
Deliver through bounded dependent tasks (one task/issue/PR per repo phase), not
one oversized cross-repository PR. This draft holds the common design and issue
plan; split into phase prompts at registration, preserving this request.

Affected repos: @PyAutoPulse (primary), @autolens_profiling,
@PyAutoBrain (profiling conductor compatibility), @autolens_assistant (consumer).
Classification: workspace/organ development; no scientific library API changes.

## High-level plan

1. Define stable setup identities and an evidence catalogue shared by dashboards
   and assistants, retaining the project's ownership of scientific meaning.
2. Publish runtime, breakdown, compilation, memory, hazards and recommendations
   through a versioned project interface; explicitly identify selected reference
   records and gaps instead of treating latest as accepted.
3. Rebuild Pulse and the project dashboard around project → dataset → model →
   instrument/configuration navigation with the shared Heart-style theme.
4. Reorganize active profiling entry points into dataset/model/measurement
   folders, updating drivers, HPC commands, CI, documentation and Brain readers.
5. Add setup-oriented wiki summaries and assistant lookup guidance; retain
   cross-cutting campaign histories and original result provenance.
6. Define a reproducible baseline campaign and its acceptance/coverage report.
   Actual bulk measurement and scientific acceptance remain a later campaign:
   the human requested a baseline when the time is right, not immediately.

Tier: judge — merge mode: human /prm.

## Detailed implementation and issue plan

### Phase 1: Pulse contract reader (PyAutoPulse) — COMPLETE

Merged 2026-10-05: https://github.com/PyAutoLabs/PyAutoPulse/pull/11.
Record: `complete/2026/10/profiling-setup-contract.md`. Reader v2 is available;
the live registry stays v1 until the browser consumer migration. Phase 2 and project Phase 3a are merged; Pulse Phase 3b is PR #13.

Suggested issue: `feat: accept setup-based profiling evidence`
Suggested branch: `feature/profiling-setup-contract`

- Extend `pulse/summary.py`, `REFERENCE.md`, and contract fixtures/tests with a
  new version for setup-oriented multi-axis evidence. Continue accepting v1
  during migration; deploy the reader before the new producer.
- Separate setup identity (dataset family, model family, instrument, exact
  dataset/configuration identity) from measurement identity (axis, method,
  hardware, backend, precision, measured revision, run ID).
- Include explicit units, statistic/repetitions where available, configuration
  dimensions, evidence anchors, validation status, missing-data reasons,
  recommendations and their applicability. Preserve captured commit semantics.
- Keep runtime seconds, compile seconds, component timings, host memory and
  VRAM as different typed metrics. A component is never a full likelihood;
  device total/allocated memory is not inferred to be peak process VRAM.
- Selection belongs to the project: a reference maps each setup/metric to a
  specific record. Expose absent/unreviewed evidence honestly. Do not silently
  join different solvers, regularizations, revisions or hardware configurations.
- Test v1/v2 coexistence, unknown versions, empty projects, invalid references,
  units, non-finite values, unsafe evidence paths, duplicate IDs and mismatches.

### Phase 2: Project catalogue and complete exporter (autolens_profiling) — COMPLETE

Merged 2026-10-05: https://github.com/PyAutoLabs/autolens_profiling/pull/377.
Record: `complete/2026/10/profiling-setup-catalogue.md`. Companion v2 catalogue
and lazy evidence shards are available; existing v1 consumers remain supported.


Suggested issue: `feat: publish a complete profiling setup catalogue`
Suggested branch: `feature/profiling-setup-catalogue`

- Add a documented, versioned setup registry and stdlib loader under the
  project tooling; distinguish display labels from stable semantic IDs and
  script paths. Include all scientific script families, library components and
  experimental/off-grid work without exposing tooling folders as datasets.
- Extend `scripts/misc/tooling/build_dashboard.py` or factor its scan into
  reusable catalogue/export modules. Read existing runtime, breakdown, compile,
  VRAM, streaming and hazard evidence through explicit adapters.
- Catalogue experimental controls separately from representative results.
  Never promote legacy results to accepted reference evidence automatically.
- Export configuration including image shape/masked pixels, source dimensions,
  PSF, oversampling, regularization, solver/preloads, N_vis, transformer and
  precision where applicable; unknown legacy metadata stays null with reason.
- Preserve original result paths and values. Historical evidence must not be
  renamed/relabelled as though it was measured by the new source layout.
- Derive coverage from the declared setup matrix, including not measured,
  unusable, failed and inapplicable states; do not invent zero timings.
- Wire deterministic generation and validation into existing lint/Pages checks.
  Test real representative record shapes plus adversarial incompatibilities.

### Phase 3: Scientist-facing browsing (separate project and Pulse PRs)

Project Phase 3a merged: autolens_profiling#379; record `complete/2026/10/profiling-setup-page.md`.
Pulse branch:
`feature/profiling-setup-browser` (Pulse).

- Reuse `PyAutoBrain/board/_theme.py`, including its existing Pulse SVG hero,
  responsive width, typography and controls; adjust deployment dependencies
  only as required to load that shared theme.
- In `pulse/board.py`, use Heart-style copy actions with expandable prompts,
  label the check-in `Profiling Check In`, integrate last-reviewed metadata,
  retain the campaigns table with individual accessible links/icons, and avoid
  cramped wrapping. Keep open tasks reachable inside the appropriate campaign.
- Replace the global wall of comparisons/evidence with project → dataset →
  model disclosures. Model detail uses instrument/config selectors and updates
  all values, charts and configuration metadata consistently.
- The project `dashboard/index.html` generator presents the same setup model.
  Prefer one exported data contract and shared conventions; do not maintain
  separately curated scientific summaries on the two sites.
- Provide URL state/deep links, browser back/forward, keyboard navigation,
  labelled selectors, sensible empty states and a no-JS evidence fallback.
- Show exact timings and linear-scale charts by default, separate device panels
  where useful, with optional log scale. Clearly distinguish single-call
  latency from batch throughput, compile/setup from steady state, and the
  instrumented breakdown from the full compiled likelihood.
- Place evidence links at the bottom of each setup under a disclosure; retain
  a concise visible qualification indicator and expand its reasons on demand.
- Remove temporal charts and drift-led navigation from the default view.
  Preserve history, revisions, existing pins and provenance for later use;
  no change to Heart drift policy or claim of a newly accepted baseline.
- Verify desktop/narrow/mobile rendering, table wrapping, every selector,
  direct links, mismatched evidence, missing devices, and local/GPU/A100 labels
  using the actual hardware records rather than assumed three-way coverage.

### Phase 4: Source taxonomy and orchestration (project, then Brain)

Suggested branches: `feature/profiling-model-layout` (project),
`feature/profiling-catalogue-routing` (Brain).

- Inventory every active script and its callers before moving it. Target
  `scripts/<dataset>/<model>/<measurement>.py`, including imaging and
  interferometer MGE/Delaunay/rectangular families; explicitly map point-source,
  cluster, multi-dataset and datacube cases. Keep dataset-independent component
  work under `scripts/lens/` and shared machinery under a documented common
  location. Use catalogue aliases for legacy `pixelization` naming.
- Preserve numerical bodies, CLI arguments and result destinations. Update
  cross-script imports, runtime sweep path resolution, compile mappings, HPC
  submission scripts, smoke commands, READMEs and checks. Retain thin old-path
  wrappers during a documented compatibility window; never duplicate science.
- Validate all dispatch paths without submitting jobs, import smoke affected
  script families, and run existing relevant tooling/unit tests and lint.
  Freeze/check existing result content and numerical configuration defaults.
- In `PyAutoBrain/agents/conductors/profiling/`, replace fragile source-layout
  assumptions (including AST lookup of sweep `CELLS` where appropriate) with
  the published/local catalogue reader, preserving dry-run behavior, bounded
  CPU policies and existing compatibility until the producer is available.
- Update only affected Brain skill/agent documentation and tests; do not change
  the ownership boundaries between Brain, Pulse, Cortex, Mind and projects.

### Phase 5: Wiki and assistant consumption (separate project/assistant PRs)

Suggested branches: `feature/profiling-setup-wiki` (project),
`feature/profiling-setup-advice` (assistant).

- Add per-setup wiki navigation generated/validated against the catalogue;
  connect selected evidence, hazards, supported recommendations, scripts and
  relevant campaigns. Retain `wiki/campaigns/` journals as single authoritative
  cross-cutting narratives. Extend `check_wiki.py` and documentation contracts.
- Structure existing interferometer decision-matrix recommendations with
  applicability bounds, measured revision, acceptance caveats and evidence.
  Do not extrapolate an accepted NUFFT choice to unmeasured configurations.
- Add an assistant skill and relevant routing links to query the catalogue by
  dataset size, masked pixels, source resolution, PSF, precision and hardware.
  Report exact match / approximate analogue / no applicable evidence, explain
  confidence and limitations, and cite concrete records.
- Distinguish per-likelihood timing from estimated total fit time; any fit-time
  calculation states assumed evaluation count, concurrency, setup/compilation
  and overhead. No general calibrated predictor without supporting data.
- Add lookup/contract tests for applicable, incompatible and absent evidence;
  verify assistant examples resolve against the exported fixture/catalogue.

### Phase 6: Baseline readiness (Pulse task and project specification)

- Record a dedicated baseline campaign in Pulse's campaign/task ownership and
  its executable configuration matrix/specification in the project.
- Specify revisions, exact setups, reference hardware/thread settings, host
  load bounds, timing synchronization/warmup/repetitions, compile-cache states,
  memory methodology and correctness witnesses. Include missing cells and CPU
  usability exclusions; CPU arrays obey the `ral` partition rule.
- Provide dry-run enumeration and acceptance report generation; no bulk runs,
  overwriting baseline pins, or scientific acceptance during this refactor.
- A later approved campaign collects and accepts the new baseline. Temporal
  dashboards remain a later feature, while metadata required for them survives.

## Current branch survey and checkpoint

All four implementation checkouts are on main and match fetched origin/main.
PyAutoPulse and PyAutoBrain are clean. autolens_profiling has untracked
`dataset/abell_1201/`; autolens_assistant has that dataset plus untracked
`scripts/cluster_model_composition.py`. Preserve these in canonical checkouts;
implementation uses isolated worktrees under the workspace `.worktrees/`.

Recent local branches:
- Pulse: main only.
- Profiling: main, feature/interferometer-streaming-scaling,
  feature/critical-curves-dispatch-audit, feature/pointsolver-extent-sanity-check,
  codex/abell-1201-data.
- Assistant: main, feature/benchmark-positions-inference,
  chore/session-start-hook-regen, bench/bootstrap-smoke-stage-b,
  feature/abell-1201-point-mass.
- Brain: main, feature/tiered-auto-merge, feature/abell-1201-point-mass,
  feature/cortex-may-submit, claude/pyauto-cti-ci-phase-5-n4idom.

Coordination authorized by the human on 2026-10-05, including removal of the
merged streaming worktree. Its phase is recorded in
`complete/2026/10/interferometer-streaming-scaling.md`; ignored files were
archived and verified before removal. The old calibration answer remains
unknown and no shadow-row outcome was invented.

Heart at entry: STALE — Release STALE; monitoring RED · 45/100 · 125 unresolved
(updated 21h ago). Entry helper exits 1; planning allowed. Re-read at shipping.

The conceptual and detailed plan, branch proposal and coordination are approved
by the human (2026-10-05). Phase 1 has now shipped and merged (record above); remaining phases have not
been implemented, and no compute has been dispatched.

## Original request (verbatim)

The first dashboard is okay but leaves a lot to be desired, it has way too much information, the information is
spread out everywhere and its a nightmare and headache to navigate. Here are suggestiosn:

- Make format match size of other boards (e.g. PyAutoHeart) and try make the image at the top exactly the same style
as dashboards like heart, it currently has no image.
- For the bug prompt at the top, match Heart's style for "Fix Heart Systematically" where its a clickable button
and a drop down to see the full propmt.
- Make "Check in on all profiling work" something more concise "Profiling Check In"
- Make this text more integrated it takes up a whole line "Last check-in: not recorded yet. Ledger dates are review dates, not measurement freshness."
- Campaigns dashboard and table is good make sure with narrower size it doesnt have text double column and put individual clickable
icons for easch. 

- Here is where things have way too much information. After the table, we should have an interface of lcickable drop
downs which takes us to what we need. So, the first clickable dropdown should be autolens, so we are looking
at autolens project profiling stuff. Once we click it, we should see all options in the scritps folder (e.g. imaging, interferometer),
meaning we as a user have just chosen our dataset, more intuitive. I think for imaging and interferometer the next
click should be the type of likelihood function we want to look at results for (e.g. delaunay, rectangular, mge). This
would then bring up all relevent information for that setup, for example if I click delaunay I can see its overall likelihood run time
on CPU, GPU, I can see its breakdown on all 3,I can see informaiton on its compile time, I can see information on its hazards
and everything else. I can imagine that instrument type (e.g. HST, EUcid) is a small drop down box which I can click betwen which live
"updates" the values and graphs displayed to me. It is far more intuitive for a scientisit to pick dataset type, model type, and then
look at results then what is there now. For each set of options, I can imagine at the bottom under the info it then links to all the
"profiling evidnece links" which at the moment just complete overwhelmes and clutters the dashboard and is completely useless cause
its too dense to navigate. These pages should also display key information about the profiling run time (e.g. number of source pixels, PSF size)
for each setup.

At this point, one is left wondering if we need a huge _profiling refactor, as the above design would be scripts/imaging/delaunay/likelihood_breakdown.py (for example)
whereas currently we have scripts/imaging/likelihood_breakdown/delaunay.py. I think this would be a big endeavor, but I think it would be worth it
as it means in the long term the repo navgiation matches what to me feels most intuitive. This is also closer to how autolens_workspace is packaged
with features in dediciated folders. I suspect this would then lead a redesign and refactor of the research wikis, campaigns etc, but I think this makes
obvious sense as a large scale refactor. Give me your opinion after reseaerching this.

The other long term goal of _profiling repos is for the autolens_assistant (or other assistant) to read them and give the user a recommended setup
in terms of settings (E.g. which NUFFT to use for their interferometr dataset) and an estimate of run time. I think that having the structure above
is probably more conducive for this, as the assistant will know what its dataset and setup is and then just need to find the right folder
on the repo, and can access all the key information within (e.g. likelihood time, breakdown time, compile time, VRAM use, etc.).

https://pyautolabs.github.io/autolens_profiling/ is nice, but getting to this information via clickable routing like described above makes it alot
more interpretable as the user has chosen what information to get to before reading it. Having the y axis log is tircky as graphs are hard to read.

I think we should drop temporal information for now, for example in these graphs. Its a good idea and something we should add back in, but 
I think we want a working clear useable dashboard that is representative of the current results and then we can work in how we manage and display
temporal stuff. The currently temporal stuff also uses results I'm not convinced are entireliy reliable so I think we will want to do a
"baseline" campaign when the time is right.

## Follow-up authorization (verbatim)

It soundsl ike we are in agreement, and we should do this maximally now to pay off in the long term even if it is large scale refactors :)
