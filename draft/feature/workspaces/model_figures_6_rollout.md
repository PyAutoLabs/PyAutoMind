# Model figures phase 6 — roll the figure out across every example and tutorial

Type: feature
Target: workspaces
Repos:
- autofit_workspace
- autolens_workspace
- autogalaxy_workspace
- HowToFit
- HowToLens
- HowToGalaxy
- autocti_workspace
- euclid_strong_lens_modeling_pipeline
- PyAutoFit
- PyAutoLens
- PyAutoGalaxy
Themes:
- visualization
- notebooks
- docs-hub
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: needs-slicing
Epic: model-figures
Phase: 6
Filed: 2026-09-10

**Phase 3 shipped 2026-09-11** — `complete/2026/09/model-figures-lens.md`; still blocked by phase 4 (`draft/feature/autofit/model_figures_4_graphical_plates.md`)
— and, for the graphical-model tutorials only, **by phase 4**
(`draft/feature/autofit/model_figures_4_graphical_plates.md`).
(Deliberately not in a `Blocked-by:` header: that key is graded against GitHub
refs and cannot name a Mind prompt path.)

Phase 6 of the `model-figures` epic. Ledger (brief, design record, independent
review): `draft/feature/autofit/model_figures_epic.md`. Phases 2 and 3 put the
figure into the two cookbooks; phase 6 is the **rollout**.

## Goal

Every script and tutorial that composes a model and prints `model.info` also
**shows the model figure** — structure view, default settings — immediately
beside that print, so the figure becomes the standard first look at a model
across the organism: read the map, then the legend. Docs pages that show
`model.info` output embed the committed PNGs alongside it.

## Ordering — issue ONE sub-task at a time

This prompt is a rollout map, not a single issue. At pick-up, cut **one**
sub-task from the list below and run it through `/start_dev`; never bulk-issue
the set, and never bundle two repos' rollouts into one PR.

- **(a) PyAutoFit surfaces** — `autofit_workspace` cookbooks and `features/`,
  the `howtofit` scripts and the HowToFit chapters. The graphical-models
  chapter waits for phase 4.
- **(b) PyAutoLens surfaces** — `guides/modeling/cookbook.py` (phase 3 already
  did this; verify only), `imaging/modeling/*` and `features/*` (MGE,
  pixelization, point source, multi-dataset), `slam_start_here.py` and the SLaM
  pipelines, and the HowToLens chapters that compose models.
- **(c) PyAutoGalaxy surfaces** — `autogalaxy_workspace` plus HowToGalaxy.
- **(d) Sibling projects** — `autocti_workspace` / PyAutoCTI docs, and the
  model-composition points in `euclid_strong_lens_modeling_pipeline`.
- **(e) RTD docs** — the PyAutoFit / PyAutoGalaxy / PyAutoLens documentation
  pages that print `model.info` output.

## Mechanics

- The call sits **next to each `print(model.info)`**, using the API settled in
  phase 2 — provisionally `af.ModelPlotter(model).figure()`. If phase 2 named it
  otherwise, that name wins; do not invent a second spelling here.
- In **generated notebooks** the figure renders inline and commits **no asset**.
- In **docs pages** the PNG is committed under that repo's `docs/images/` and
  referenced by raw URL, as `overview_3_features.md` already does.
- **Regenerate notebooks** per each workspace's own convention — the regen
  command differs per repo; use that repo's, not another's.
- **Smoke CI must stay green.** The figure call has to be cheap and must never
  raise inside a script. Any guard belongs **in the library**, once — never a
  `try/except` copied into every script.
- **SLaM pipelines**: one figure per stage, wherever that stage writes
  `model.info`.

## Acceptance

- A grep for `model.info` across the listed repos finds a figure call beside
  every occurrence. Explicit exceptions, excluded by design (code-heavy,
  doc-light): `*_workspace_test`, `*_workspace_developer`, the profiling repos,
  and the assistant workspaces.
- Notebooks regenerated in every touched workspace.
- All workspace smoke CI green.
- Docs build clean in each of PyAutoFit, PyAutoGalaxy and PyAutoLens.

## Note on model split

Any **tutorial prose** written or revised in this rollout stays Opus-or-above
per the tutorial-prose split in `PyAutoBrain/skills/WORKFLOW.md`. The figure
call itself is mechanical and delegates normally.
