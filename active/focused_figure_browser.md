# Simplify the PyAutoEyes dashboard and browse one figure at a time

Target: @PyAutoEyes
Type: feature
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/25

Retain a compact overview, use library → dataset → figure navigation, and display
one selected figure prominently inside the dashboard with its critique actions.
Use PyAutoPulse and PyAutoInsight Results sections as read-only navigation references;
only PyAutoEyes implementation is in scope.

## Approved plan — 2026-10-08

- Use library names alone (PyAutoLens, PyAutoGalaxy, etc.) throughout visible navigation.
- Reduce the overview to Library, Figures, Rendered with (version only), and
  Freshness (Current/Behind/Ahead/Unknown); keep open critiques inside their library section.
- Expand a library to choose a dataset, then select a figure from a labelled
  dropdown. Show one large selected image and its suggestion/review actions.
- Load only selected images; offer accessible in-page enlargement with close,
  Escape and focus restoration, plus loading and failure feedback.
- Remove visible survey summaries, repeated stack/date prose and repository/manifest
  boilerplate. Preserve machine-readable evidence and counts consumed by Brain.
- Verify browser interactions, responsive layout, renderer contracts and generated outputs.

Tier: undeclared — merge mode: human /prm.

### Implementation details

Primary repository: PyAutoEyes. Brain classified this as medium, direct, library
workflow (start_library → ship_library). Pulse and Insight require no edits.

1. `eyes/board.py::render_html`: retain stable instance anchors, shared theme
   `section_layout` disclosures and orchestration panel. Simplify table headers/rows
   and instance headings. Nest dataset disclosures under library disclosures; each
   dataset gets a labelled figure select and a single image viewer. Selecting a
   figure updates its image, accessible label, review copy payload and suggestion
   URL atomically. Keep critique ownership in the project repo.
2. `eyes/board.py::CSS` and `JS`: replace thumbnail-grid styling with a responsive
   image viewer and in-page enlarge control/dialog; constrain long names and use
   shared sizing tokens. Assign image sources only when needed, and handle load
   failures without navigating off the dashboard. Keyboard and touch controls
   must remain usable inside the cockpit iframe. Provide usable no-JS figure links.
3. Add a presentation-only compact freshness formatter; preserve InstanceView
   freshness calculation and state-feed semantics. `render_markdown` gets matching
   concise labels/text while retaining instance/context markers, leading counts
   and a complete figure index. Keep survey collection/carry-forward intact.
4. `tests/test_board.py`: update old grid/raw-link expectations; cover selection
   metadata, safe escaping, unique control identifiers, empty/unavailable manifests,
   concise status labels and preserved context/state contracts. Run repository
   Ruff, pytest, board generation and manifest checks. Browser-check real loaded
   images, selection/action matching, enlargement/close/Escape/focus, clipboard,
   navigation anchors, failure states and no whole-page overflow at 390, 768,
   820, 1024 and 1440px in light/dark modes.
5. Regenerate `dashboard.html` and `dashboard.md` with `bin/pyauto-eyes board`;
   include any legitimately changed generated feeds. Update guidance describing
   the old thumbnail behavior if needed. Ship a reviewable PR through ship_library.

### Initial branch survey

- PyAutoEyes root: `/home/jammy/Code/PyAutoLabs/organs/PyAutoEyes`; branch `main`.
  Untracked `dataset/`, `output/`, `scripts/` exist; preserve them. Only local branch
  is main. Conflict guard returned clear; no matching active task found.
- Mind root: `/home/jammy/Code/PyAutoLabs/organs/PyAutoMind`; branch `main`.
- Proposed branch: `feature/eyes-focused-figure-browser`.
- Planned worktree: workspace-local `.worktrees/eyes-focused-figure-browser/`,
  respecting the workspace path boundary. Create after plan approval/registration.
- Entry Heart status: STALE; release STALE, monitoring RED. Reassess at ship gate.
- Next step: obtain plan approval, then create the issue and register/setup the worktree.

## Original user request (verbatim)

PyAutoEyes dashboard: lens - PyAutoLens -> PyAutoLens, same for Galaxy

The table at the top is good but its a bit cluttered or too much informaiton or hard to read, can we simplify?
In "Rendered with" we only need version numbers so for example "	autolens " is removed. Freshness can be more
concise (I think it dusplicates inform with Rendered with?) Survey feels like it could be removeD?

I thikn we should click "lens PyAutoLEns" to get a drop down menu of datasets (E.g. imaigng, interferometer),
which we rthen click to reveal all images. This will reduce information being over the top at beginning and user
navigates based on their choices ot know whats happening. Similar design in PyAutoPulse and PyAutoInight Results tabs.

Stuff like this is too much info and I wont read it "Rendered with autolens 2026.8.17.1, autogalaxy 2026.8.17.1, autoarray 2026.8.17.1, autofit 2026.8.17.1; generated 2026-09-28."

at the moment clicking an image takes you to raw githubcontent which then takes a while to load and moves you off the dashboard.
I want to be able to click an image to bring it up but can it be more seamless and integrated in the dashboard set up?
I can imagine that after clikcing imaging as a drop down, instead of seeing all images at oncde its a drop down menu
and we choose one at a time which then displays in the dashboard large (with its suggest an improvement) prompt
also there. I Will really look at one image at a time so why display them all in a grid?

Remove this: Figures from PyAutoLabs/autolens_visualization, manifest gallery/viz_manifest.yaml, re-rendered on pyautolens-release.

Survey (Brain Eyes conductor, local checkout): 40 PNGs on disk (imaging 22, interferometer 18); gaps none; orphans none; stale renders none.

## Implementation handoff — 2026-10-08

- Approved plan implemented in `.worktrees/eyes-focused-figure-browser/PyAutoEyes`,
  branch `feature/eyes-focused-figure-browser`; changes are not committed/pushed yet.
- Compact four-column overview, concise library/status labels, dataset disclosures,
  one selected image with matching critique actions, and accessible enlargement.
  Hidden survey/context/state contracts remain intact. Generated HTML/Markdown updated.
- Ruff and all 87 pytest tests pass. Live check passed all 265 image URLs, manifest
  digests and Brain state schema. Twelve Chromium cases passed: five
  widths in both themes plus phone/desktop iframe views, four real PNGs, clipboard,
  keyboard, failure/retry and response races. Fixed modal Tab/Shift+Tab containment
  in iframe; Escape restores image focus. Evidence: repo `.scratch/` logs/screenshots.
- Heart YELLOW: `manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.
  Specific mismatch: unregistered `COWLS_COSMOS_Web_Lens_Survey` checkout.
- Stale reason: `release validation incomplete: no rehearsal for current source`.
- Ship requires human acknowledgement of this current YELLOW warning under
  ship_library step 3. PR draft is `.scratch/pr-body.md`; no merge authority.
- No scientific workspace API changes; downstream surface is the board/cockpit.

Implementation and all applicable local checks complete. Next action: human acknowledgement of the exact Heart YELLOW reason above, then commit/push and open the prepared PR. No source changes have been committed, pushed or published.

## Ship authorization — 2026-10-08

Human: "yes I authorize and prm". Acknowledges the exact Heart YELLOW manifest-drift reason recorded above and authorizes commit/push, PR creation and merge after all CI passes. PR: https://github.com/PyAutoLabs/PyAutoEyes/pull/26; commit b10afdd. Local validation unchanged and passing.
