# Model figures phase 2 — matplotlib renderer

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
Themes:
- visualization
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: ready
Epic: model-figures
Phase: 2
Filed: 2026-09-10

**Blocked by phase 1** — `draft/feature/autofit/model_figures_1_graph_spec.md`.
(Kept out of the `Blocked-by:` header deliberately: that key is graded against
GitHub refs and cannot name a Mind prompt path.)

Phase 2 of the `model-figures` epic. Ledger (brief, full design record, full
independent review): `draft/feature/autofit/model_figures_epic.md`. This phase
draws the figure, in pure matplotlib, over the phase-1 spec.

## The renderer

A `MatplotlibRenderer` consuming the phase-1 `GraphSpec`. **Zero new
dependencies.** graphviz is explicitly *not* adopted: the `dot` binary is absent
locally, on the GitHub `ubuntu-24.04` runner and often on Colab, is not
pip-installable, and its rank layout is wasted on a containment figure. (Phase 5
may revisit it for the edge-heavy EP graph; phases 2–4 may not.)

Containment layout:

- **Measure bottom-up, place top-down.** Measure text with
  `Text.get_window_extent` — the prototype's width *estimator* was 11 % short on
  bold headers and the figure clipped.
- **A width budget that wraps.** Top-level frames wrap onto new rows when the
  budget is exhausted; the un-budgeted group-scale figure came out 3574 px wide.
- **Declaration order beats packing.** Never reorder children to fill space —
  the prototype floated `shear` above `mass` while `model.info` says
  `bulge, mass, shear`, forcing the reader to choose between reading across and
  reading down.
- **Fixed text size; collapse, never shrink.** Scalability comes from collapsing
  content, not from scaling the whole figure down. Padding *decreases* per
  nesting level. At most **three tint levels** — boundaries, indentation and
  labels carry hierarchy; tint only assists.
- Outputs **PNG and SVG** (PDF if free).

## Visual vocabulary (v2, as amended by the review)

Name-first pills inside white component cards. States must stay mutually
distinguishable: `free`, `fixed`, `shared`, `relation`, `solved`, `drawn`,
`missing`, `observed`.

- **free** → white pill, name only.
- **fixed** → grey pill. **Shown by default** (review point 4): fixed values
  explain model structure, especially fixed centres and widths. Hiding them is
  allowed but must print a **visible hidden-count** ("63 fixed parameters
  hidden").
- **shared is a property, not a state** (review point 3): a shared prior is
  still sampled, so it stays a **white pill** plus a **small blue badge** and a
  link to its owner. The owner's badge reads **"shared across group"** — never
  `×30`, which means something else.
- **plate badge reads "N components"** (`30 components`), because `×30` on a
  plate and `×30` on a parameter meant two different things and newcomers could
  not tell them apart.
- **per-member constant** reads **"fixed · varies by member"** — a single grey
  pill otherwise suggests one common fixed value.
- **independent repeated priors** are marked as such (distinct prior objects,
  identical configuration) and never confused with sharing.
- **solved** → dashed pill, with legend wording **"solved during fitting"** (not
  "solved", which reads as a completed fit or a known answer). Emitted only from
  verified domain semantics, which arrive in phase 3.
- **missing** → its own state for unset required configuration (`areas_factor`).
  Absence from the picture is not acceptable; it reads as absence from the model.
- **2-D cue on tuples** — `centre` and `ell_comps` each conceal two scalars, so
  a small `2D` annotation explains why counting pills does not reproduce the
  footer count. Partially fixed or partially shared tuples expand or show a
  mixed state.
- **relation** → the pill shows its **defining expression** (`= sigma × 2`).
  Prior limits are optional detail; the expression is central and is the one
  permitted piece of numeric detail on the map.
- **assertion** → a **compact constraint label carrying both operand paths**,
  visually distinct from dependency arrows. Long orange routes past several
  junctions are not acceptable.
- **redshift exception** → when fixed, render as `redshift = 0.5` under the
  galaxy header. A *free* redshift keeps the ordinary sampled-parameter pill.
- A **one-line legend** (the prototype's universal legend was disproportionate),
  and a footer with **defined counts**: prefer "16 unique sampled scalars" over
  an unexplained "16 free"; state whether "shared" counts unique shared
  variables or repeated references, and whether totals include hidden elements.

Minor fixes carried from the review: give cross-links a dedicated gutter (the
blue connector grazed a plate boundary); remove redundant outer framing that
adds no branching information; strengthen contrast on tiny muted labels and
footers; explain class-family header colours or keep them strictly decorative
(phase 3 decides); drop the short header stems, which read as partial wiring
when enclosure already shows ownership.

## API

Proposed, mirroring the `*Plotter` convention used across the organism:

    af.ModelPlotter(model).figure(
        path=None, detail="names"|"priors", collapse=True,
        max_depth=None, show_fixed=True,
    )

`detail="names"` is the default map; `detail="priors"` adds the legend's
content onto the map for a single-component read. `max_depth` folds a subtree
into one row (`… N components / M priors`); `collapse=False` expands plates.
A `model.figure()` alias may be added at plan time if the human prefers it —
this is design open decision 1 and is **not** settled; raise it in the plan.

## Per-search output

Write `model.png` beside `model.info` via `DirectoryPaths._save_model_info`,
gated behind a **NEW** `output.yaml` key **`model_figure`**, default **false**.

**Do not reuse `model_graph`.** That key was deliberately set default-false on
2026-05-15 (`complete/2026/05/disable-model-graph.md`, PyAutoFit#1264) to stop an
empty file being written for every non-graphical fit, and it gates the
*graphical-model text* `model.graph` / `graph_info`, not any image. See the
ledger's "Trap" section. `model_figure` stays false until the phase-3 acceptance
renders pass; adding it means adding `model_figure: false` to every workspace
`config/output.yaml`, as the 2026-05 task had to.

Leave `af.VisualiseGraph` (pyvis) in place as the interactive HTML extra. It may
later be reimplemented over the spec or deprecated; not in this phase.

## Documentation deliverables

- Figures in the PyAutoFit cookbooks: `autofit_workspace/scripts/cookbooks/model.py`,
  `multi_level_model.py`, `multiple_datasets.py`.
- Docs pages `@PyAutoFit/docs/cookbooks/*.md`, with the PNGs committed under
  `docs/images/` and referenced by raw URL — the pattern `overview_3_features.md`
  already uses.

## Acceptance

1. The **three lens acceptance figures** render truthfully and their renders are
   **committed as evidence**: (a) simple lens; (b) MGE 2×30 + pixelized — 11
   components, two ×30 plates split on `ell_comps`, footer "16 unique sampled
   scalars"; (e) group scale — fixed per-galaxy centre tuples rendered, unset
   `areas_factor` in the `missing` state.
2. The **toy Gaussian** from the PyAutoFit cookbooks renders.
3. A **shared / relation / assertion composite** model renders with all three
   encodings simultaneously legible.
4. Deterministic output: same model → same figure, twice.
5. No figure exceeds the width budget; text size is unchanged between the
   smallest and largest acceptance case.
