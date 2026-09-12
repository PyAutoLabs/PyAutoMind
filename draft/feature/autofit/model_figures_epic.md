# Model figures — structure-first model visualisation

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoLens
- PyAutoGalaxy
- autofit_workspace
- autolens_workspace
- autogalaxy_workspace
- HowToFit
Themes:
- visualization
- graphical-ep
Difficulty: too-large
Autonomy: human-required
Priority: normal
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 30
Unattended: needs-slicing
Epic: model-figures
Filed: 2026-09-10

## Brief

PyAutoFit can print a model but cannot draw one. `model.info` is exhaustive and
linear — 178 lines for an MGE + pixelized lens, 418 for a group-scale model —
and the only existing figure, `af.VisualiseGraph` (networkx + pyvis), draws one
node per parameter with no collapse, drops every tuple prior, and is invisible
to fixed values, instances and assertions; its per-search hook is commented out.
The model the user builds is a nested container structure — galaxies inside
collections, profiles inside galaxies, bases inside profiles — and that is
exactly the fact neither surface shows. The reference point is
[caskade's beginner guide](https://caskade.readthedocs.io/en/latest/notebooks/BeginnersGuide.html),
whose ~30-line graphviz figure gets the *idea* right (white = free, grey =
fixed, arrow = link) and the *scale* wrong: it has no collapse of any kind and
would not survive a PyAutoLens model.

The user's framing settles what the figure is for: **the figure is the MAP, and
`model.info` is the LEGEND**. So the figure is *structure-first and names-only*
— nesting drawn by containment (a component's children sit inside its box, no
parent→child edges), parameters drawn as pills carrying their name and their
state (free / fixed / shared / solved / drawn / missing / observed), repeated
siblings collapsed into plates, and edges reserved for the three facts a linear
dump cannot show: sharing, relations and assertions. Prior distributions,
limits and values are the legend's job, not the map's. It renders in pure
matplotlib by containment layout — **no graphviz**: the `dot` binary is absent
here, on the GitHub `ubuntu-24.04` runner and often on Colab, is not
pip-installable, and its rank layout is wasted on a containment figure (the one
place it is allowed back in is the phase-5 EP factor graph, where edges
dominate). A matplotlib prototype has already reproduced every predicted count:
the MGE 2×30 + pixelized model collapses from 73 nodes / 178 info lines to 11
component boxes; group scale (8 extra galaxies) from 166 nodes / 418 lines to
15. Once the cookbooks carry figures, **phase 6 rolls the figure out
across every example, tutorial and sibling project** — cookbooks first, then
every workspace, HowTo chapter and downstream pipeline that prints
`model.info`.

## End goals (acceptance for the epic as a whole)

1. **The three lens acceptance figures render truthfully**, and their renders
   are committed as evidence:
   - (a) simple lens — Sersic + Isothermal + shear + Sersic source;
   - (b) MGE 2×30 + pixelized source — must yield **11 component boxes**, **two
     ×30 plates split on `ell_comps`** (not one merged ×60), and a footer
     reading **16 unique sampled scalars**;
   - (e) group scale — 8 extra galaxies, each with **fixed per-galaxy centre
     tuples** that still render a row, and an unset `areas_factor` shown in the
     **missing** state (never silently absent, and never mislabelled "solved").
2. **Both cookbooks carry figures.** PyAutoFit's `model.py`,
   `multi_level_model.py` and `multiple_datasets.py` cookbooks and their docs
   pages; PyAutoLens' `guides/modeling/cookbook.py` (6 `model.info` stages) and
   `docs/general/model_cookbook.md`.
3. **Both "not implemented yet" placeholders are filled**:
   `autofit_workspace/scripts/features/graphical_models.py` ("This is what our
   factor graph looks like:" followed by nothing) and HowToFit
   `chapter_graphical_models` tutorial 2 ("visualization of graphs not
   implemented yet").
4. **An EP view exists**: an explicit factor graph, plate-grouped, overlaid with
   factor status, update age and confirmed reverted updates, written as
   `graph_model.png` beside `graph.info` and `graph_state.png` on the
   `visualise_interval` tick.
5. Per-search `model.png` output ships **opt-in** and only flips to a default
   once goal 1 passes.

## Phases

Issue ONE at a time through `/start_dev`. Order: 1 → 2 → 3; 4 after 2; 5 after 4;
6 after 3 and 4.

| # | Phase | Prompt | State |
|---|-------|--------|-------|
| 1 | Semantic extraction — `autofit/graph_spec.py` + the 18-construct catalogue | `complete/2026/09/model-figures-graph-spec.md` | shipped 2026-09-11 (PyAutoFit#1606) |
| 2 | matplotlib containment renderer, `af.ModelPlotter` API, per-search `model.png`, PyAutoFit cookbook figures | `complete/2026/09/model-figures-renderer.md` | shipped 2026-09-11 (PyAutoFit#1614, autofit_workspace#152) |
| 3 | Lens domain semantics + PyAutoLens/PyAutoGalaxy cookbook figures | `complete/2026/09/model-figures-lens.md` | shipped 2026-09-11 (PyAutoFit#1615, PyAutoArray#550, PyAutoGalaxy#616, PyAutoLens#737, autolens_workspace#541, autogalaxy_workspace#240) |
| 4 | Plate-notation graphical-model figure; fill the two placeholders | `complete/2026/09/model-figures-graphical.md` | shipped 2026-09-12 (PyAutoFit#1617, autofit_workspace#153, HowToFit#51) |
| 5 | EP factor-graph view with convergence/reversion overlay | `draft/feature/autofit/model_figures_5_ep_view.md` | filed 2026-09-10 |
| 6 | Rollout — the figure beside every `model.info` in every example, tutorial and sibling project | `draft/feature/workspaces/model_figures_6_rollout.md` | filed 2026-09-10 |

## Trap — do NOT reuse the `model_graph` config key

`output.yaml` already has a key named `model_graph`. It is **not** free, and it
is **not** about a figure:

- It was deliberately set **default `false`** on 2026-05-15 — record
  `complete/2026/05/disable-model-graph.md`, PyAutoFit#1264 — precisely to stop
  an empty file being written for every non-graphical fit.
- It gates the **graphical-model text dump** `model.graph` (`graph_info`) in
  `_save_model_info`, not any image. Flipping it to `true` to make the new
  figure appear would re-open the 2026-05 bug and write graph text for every
  fit.

The per-search figure therefore needs **its own key** — proposed `model_figure`
— which stays **`false` until the phase-3 acceptance renders pass** (Codex
review point 10; this is also the resolution of design open decision 2). Adding
it means adding `model_figure: false` to every workspace `config/output.yaml`
too, exactly as the 2026-05 task had to.

## Sibling bug prompts (standalone, NOT epic members)

Four PyAutoFit defects were found by execution while researching this design.
They are small, independent and worth fixing whether or not the epic proceeds:

- `draft/bug/autofit/assertion_repr_recurses_forever.md` — **already filed
  2026-09-10** (`CompoundPrior.__repr__` → `str(self)` → `__repr__` → …). Do not
  re-file it.
- `draft/bug/autofit/add_assertion_name_silently_dropped.md`
- `draft/bug/autofit/direct_instance_tuples_double_counts_constants.md`
- `draft/bug/autofit/model_function_cannot_resolve_config_priors.md`

## Provenance

Research and a throwaway matplotlib prototype were done in a **Fable session on
2026-09-10** (five legs: A caskade + comparable libraries, B PyAutoFit DAG
extraction, C PyAutoLens models, D graphical models + EP, E the prototype).
The prototype code was deliberately throwaway and is **not preserved** — every
number it produced that matters is written into the design record below. The
design page rendered for the human is the artifact
`https://claude.ai/code/artifact/c0a01490-ddcc-4959-88f1-94e651618b28`.
The two sections that follow are the full, verbatim design record and the full,
verbatim independent review, pasted here so nothing survives only in an
ephemeral scratchpad. Heading levels are demoted two steps; the text is
otherwise unedited.

## Design record (2026-09-10)

### PyAutoFit model figures — design (2026-09-10)

Research legs: A (caskade + libraries), B (PyAutoFit DAG extraction), C (PyAutoLens
models), D (graphical models + EP), E (matplotlib prototype). Reports and the
prototype live beside this file (`A_*.md … D_*.md`, `../proto/`).

#### 1. Verdict

- caskade's figure is ~30 lines of python-`graphviz`: one node per module
  (ellipse) and per parameter (box). **White box = free, grey box = fixed,
  grey right-arrow = linked/pointer.** It has no collapse of any kind, so it
  would not survive a PyAutoLens model.
- PyAutoFit's `af.VisualiseGraph` (networkx + pyvis HTML) has correctness bugs,
  not only clutter: tuple priors (every `centre`) are dropped or orphaned,
  fixed values / instances / assertions are invisible, node identity *is* the
  label string (ids + prior limits baked in), no depth limit or collapse. The
  hook that would write it per search (`directory.py:368`) is commented out.
- `model.info` already contains the collapse primitive: `find_groups` in
  `mapper/prior_model/representative.py` prints `0 - 29`, `30 - 59`. The figure
  renders over that grouping rather than re-inventing it.
- A one-vocabulary design (component box + parameter rows, plates for repeated
  siblings, edges only for shared/relation/assertion) was prototyped in pure
  matplotlib and reproduces every predicted count: MGE 2×30 + pixelized source
  goes from 73 nodes / 178 info lines to **11 boxes**; group scale (8 extra
  galaxies) from 166 nodes / 418 lines to **15 boxes**.

#### 2. Visual vocabulary (one, at every scale)

| Element | Drawn as |
|---|---|
| `Model` component | Box: header strip `attr · ClassName` (`lens.bulge · Sersic`), one row per parameter. Sub-components nested *inside* the box (containment, no parent→child edges). |
| `Collection` | Labelled frame (`galaxies`), nested for nested collections. |
| free prior | White row `name   U(0, 100)` / `N(0.5, 0.1)` / `LogU(1e-6, 1e6)` / `TN(0, 0.3)`. |
| tuple prior | One row `centre (y,x)   U(-0.1, 0.1)`. |
| fixed constant | Grey row `sigma   3`. |
| shared prior | Row lives in the first owner with chip `⇄ ×N`; every other occurrence is a grey pointer row `centre   ⇄ g0.centre` plus a dashed blue edge to the owner. |
| relation (`CompoundPrior`) | Cream row `sigma   = sigma * 2`, orange edge to operand. |
| assertion | Dashed orange edge labelled `assert <`. |
| linear profile / Basis / pixelization | Italic header tag `linear · intensity solved`, `source pixels solved`. |
| repeated siblings (plate) | One box inside a dashed frame with badge `×30`; rows annotate `⇄ ×30` (one prior for all), `×8 independent` (distinct priors, same config), `0.01 → 3 (30, fixed)` (constant varying per member). |
| root | Footer chip `N = 16 free · 62 fixed · 6 shared` from model-level counts, so hidden constants are still counted. |

Palette is near-monochrome; blue = shared-prior edges, orange = relation/assertion.

#### 3. Collapsing rules (validated on lens models a, b, e)

R1 soft plate: siblings matching on class tree + prior *configuration* (ignore
prior identity, `_label`, constant values). R2 split a plate only by
cross-member shared priors (MGE basis 0 vs basis 1 `ell_comps`). R3 tuple row.
R4 fixed rows; constants varying across plate members → one range row. R5
shared drawn once + pointers. R6 linear/solved tag. R7 scalar attrs and
`Model(int)` are rows never boxes. R8 collections are frames. R9 dataset plate
for `FactorGraphModel`. R10 chained state `fixed ← source_lp[1]` (needs
provenance not on the model; deferred). R11 assertions as edges.

Zoom: `max_depth` folds a subtree into one row `… N components / M priors`;
`collapse=False` expands plates; `show_fixed=False` hides grey rows.

#### 4. Graphical models and EP

- Model figure = **plate notation**: shared prior box above, dashed plate
  `dataset i = 1…N` with one collapsed component box (pointer row `⇄ shared`
  or `◂ drawn N(50,30)`), shaded `data_i` node; hierarchical factor as a
  hyper-parameter box above with one arrow `centre_i ~ N(mean, sigma)`.
  Plates are *inferred* (declarative variables have `plates=()`): group
  `graph.analysis_factors` by prior-model isomorphism, then per path shared /
  plated / drawn.
- EP figure = explicit **factor graph**, plate-grouped, with overlays from
  `EPHistory` / `FactorHistory` / `Status` / `EPDiagnostics`: factor fill =
  converged/working/stale, KL sparkline, variable `mean ± std`, dashed red edge
  for `Status.changed[v] is False` (the README §3.5 silent-reversion failure).
  Files: `graph_model.png` beside `graph.info`, `graph_state.png` on the
  `visualise_interval` tick.
- Existing holes to fill: `autofit_workspace/scripts/features/graphical_models.py`
  ("This is what our factor graph looks like:" then nothing) and HowToFit
  chapter_graphical_models tutorial_2 ("visualization of graphs not implemented
  yet").

#### 5. Architecture

1. `autofit/graph_spec.py` — pure extraction, no drawing: a **nesting tree**
   (`ComponentNode{path, name, cls_name, obj_id, rows, children, multiplicity}`,
   `ParamRow{name, kind ∈ free|fixed|relation|instance|pointer, summary,
   prior_id}`) plus `SharedEdge / RelationEdge / AssertionEdge`. Primitives
   (verified): `path_instance_tuples_for_class((Model, Collection),
   ignore_children=False)`, `path_priors_tuples`, `all_paths_prior_tuples`,
   `path_instance_tuples_for_class((Constant, float), ignore_class=Prior)`,
   `path_instance_tuples_for_class((CompoundPrior, ModifiedPrior))`,
   `gathered_assertions()`, `find_groups`.
2. `MatplotlibRenderer` — containment layout (measure bottom-up, place
   top-down), zero new deps. **Primary and, for phases 1–4, only renderer.**
   graphviz is *not* adopted: the `dot` binary is absent here, on the GitHub
   ubuntu-24.04 runner and often on Colab, is not pip-installable, and dot's
   rank layout is wasted on a containment figure. Revisit only for the EP
   factor graph (many edges) in phase 5.
3. `af.VisualiseGraph` (pyvis) stays as the interactive HTML extra, reimplemented
   over the spec or deprecated.
4. Output: `model.png` beside `model.info` via `DirectoryPaths._save_model_info`,
   config-gated by the existing `output.yaml` `model_graph` key.

Production must-fixes learnt from the prototype: measure text with
`Text.get_window_extent` (estimator was 11 % short on bold headers); width
budget that wraps top-level frames (group-scale figure is 3574 px wide);
fixed *tuple* constants inside a plate render no row (extra-galaxy centres);
`Model(int)` wrappers (`Delaunay.pixels`) need special-casing.

#### 6. Traps for the implementer (all verified by execution)

- `TuplePrior` is not an `AbstractPriorModel`: any walk over
  `direct_prior_tuples` + `direct_prior_model_tuples` silently loses every tuple
  parameter.
- `CompoundPrior` / `ComparisonAssertion` *are* `AbstractPriorModel`s with
  `cls = float`, so they masquerade as components; operand names come from a
  stack-frame `retrieve_name()`.
- `repr()` of a `CompoundPrior` subclass without `__str__` recurses forever
  (`compound.py:88`). Never repr in a label path.
- Prior `_label` carries a per-instance counter (`einstein_radius2`), which
  defeats naive equality when detecting plates.
- `fgm.graph` rebuilds on every access and renames `PriorFactor`s; cache it.
  `factor.name` is not unique across `_HierarchicalFactor`s; use
  `factor.name_for_variable(v)`, never `variable.label`.
- `with_free_parameters` does not exist on installed `af.Model`; the live
  multi-dataset idiom is `model.copy()` + `af.AnalysisFactor` /
  `af.FactorGraphModel`.

#### 7. Proposed epic (PyAutoMind)

| Phase | Repo | Deliverable |
|---|---|---|
| 1 | PyAutoFit | `graph_spec.py` extractor + tests over the 18-construct catalogue (B §2) |
| 2 | PyAutoFit | matplotlib renderer, rules R1–R8/R11, `model.png` per search, `af.ModelPlotter`-style API; PyAutoFit cookbook figures (`model.py`, `multi_level_model.py`, `multiple_datasets.py`) + docs PNGs |
| 3 | PyAutoLens (+Galaxy) | validate on the five lens models, fixed-tuple plate row, width wrapping, `linear`/`solved` tags; lens cookbook + `model_cookbook.md` figures |
| 4 | PyAutoFit + workspaces | plate-notation `plot_factor_graph`; fill the two "not implemented yet" placeholders; HowToFit chapter |
| 5 | PyAutoFit | EP factor-graph view with convergence/reversion overlay, `graph_state.png` |

Side bug prompts (PyAutoFit): `CompoundPrior.__repr__` recursion;
`add_assertion(name=)` silently dropped; `direct_instance_tuples` double-counts
`Constant`s; `af.Model(function)` cannot resolve config priors.

#### 8. Open decisions for the human

1. API name: `af.ModelPlotter(model).figure()` (mirrors `aplt.*Plotter`) vs
   `model.plot()` / `af.plot_model(model)`.
2. Should `model.png` be written per search by default (flip `output.yaml`
   `model_graph` to true) or stay opt-in?
3. Fixed rows: shown grey by default (cookbooks) — hide by default in the
   per-search file?
4. File the epic now via `/intake`, or iterate on the prototype figures first?

#### 9. Independent review (Codex gpt-6-astra, 2026-09-10) — final say

Verdict: **ADOPT WITH CHANGES** — adopt the v2 containment layout and
name-first pills; do not ship the semantic encoding unchanged. Full text in
`codex_review.md`. Adopted changes, in the reviewer's priority order:

1. **Fix misleading states first.** Hierarchical draws are not shared: A_08's
   `⇄ centre` becomes `centre_i` with a "drawn" annotation and the parent arrow
   ends on that pill. `Delaunay.pixels` must render as `areas_factor` in a
   distinct *missing-configuration* state. States to keep distinguishable:
   free, fixed, shared, relation, solved, drawn, missing, observed.
2. **Separate repetition from sharing.** Plate badge reads `30 components`;
   a group-shared parameter carries a badge `shared across group`, not `×30`;
   a per-member constant reads `fixed · varies by member`; independent repeated
   priors are marked as such.
3. **Sharing is a property, not a state.** A shared prior is still sampled: white
   pill + small blue badge/link, never a separate "shared" fill. Tuples get a
   `2D` cue so pill counts reconcile with the footer; relations show their
   defining expression (`= sigma × 2`) as the one permitted piece of detail;
   assertions get a compact label with both operands.
4. **Fixed parameters shown by default** (they explain structure; hiding must
   print a hidden-count). Redshift gets a presentation exception:
   `redshift = 0.5` under the galaxy header when fixed.
5. **Contract wording.** Not "line for line": *every displayed element resolves
   to a path or grouped paths in `model.info`; every omission or added
   annotation (solved, missing) is explicit.* The figure's plates are the
   component partition induced by all cross-member shared priors; `model.info`
   groups per parameter (`0 - 59` for centre) and may be coarser — document it.
   Visual order = declaration order (fix the masonry putting `shear` above
   `mass`); footer counts get definitions (`16 unique sampled scalars`).
6. **Scalability.** Keep text size fixed and collapse content, never shrink the
   figure; reduce padding per nesting level; fewer tint levels (A_06 has too
   many); overview + selected-subtree exports with the same vocabulary; PNG +
   SVG/PDF.
7. **R1/R2 safety condition.** A plate must preserve sharing, relations,
   assertions and exceptions across members, not only class tree + prior
   configuration; say what the plate repeats.
8. **Graphical/EP.** Separation of model view vs EP factor graph approved.
   Observed data gets its own encoding (not "fixed"); hyper-parameters counted
   separately. EP overlay starts with factor status, update age and confirmed
   reverted updates (use the `reverted_variables` set, not `Status.changed is
   False`); message precision only with defined handling of signed/invalid site
   precisions; collapsed plates show aggregates plus exceptional members.
9. **Architecture.** matplotlib containment approved as initial renderer; keep
   three layers (semantic extraction / presentation transformation /
   layout-rendering); `ParamRow.kind` becomes separate properties (sampling
   status, sharing, dimensionality, provenance). One renderer for small and
   large; caskade mode optional polish.
10. **Phasing revised.** Large-model correctness (fixed tuples, missing
    configuration, deterministic order, width bounds) moves into the phase 1–2
    gate with A_04–A_06 as acceptance cases; **per-search `model.png` stays
    opt-in until they pass** (resolves open decision 2); phase 3 = lens docs on
    already-correct rendering; phase 4 = shared-vs-hierarchical teaching
    examples; phase 5 = EP with layout engine still open.

Resolved decisions: fixed pills shown by default (3); per-search output opt-in
until acceptance cases pass (2). Still open: API name (1); file the epic now (4).

## Independent review (Codex gpt-6-astra, 2026-09-10)

#### Verdict

**ADOPT WITH CHANGES.** Adopt style A’s containment layout and name-first presentation. Do **not** ship the current semantic encoding unchanged.

A_04 makes component ownership much easier to see than the v1 table. A_05 keeps the MGE basis recognisable without drawing 60 Gaussians. C_05 demonstrates why a conventional tree is a poor default for this model.

The remaining problems are substantive: some symbols imply the wrong statistical relationship, aggregation hides meaningful differences, and the promised `model.info` correspondence is not yet reliable.

#### Top 5 changes (ordered)

1. **Correct misleading parameter states before polishing layout.**  
   In **A_08**, `⇄ centre` says “same parameter across datasets,” whereas the hierarchical arrow says “distinct centres drawn from a common distribution.” Remove the shared symbol; label it `centre_i` with a distinct “drawn” annotation. In **A_05**, replace solved `Delaunay.pixels` with the actual `areas_factor` and its **missing configuration** state. Missing, fixed, derived, and solved must remain distinguishable.

2. **Separate repetition from sharing.**  
   In **A_05**, the plate’s `×30` means 30 components, while `centre ×30` means reuse of a parameter. Newcomers cannot infer that distinction. Use **“30 components”** on the plate and **“shared across group”** on the parameter. Distinguish independent repeated priors explicitly. For grey `sigma`, say **“fixed; varies by member”**—the current pill can suggest one common fixed value.

3. **Make the `model.info` correspondence an explicit mapping contract.**  
   Preserve exact attribute names and full paths internally, with a lightweight path index for static output. In A_05, the displayed two Gaussian groups map to a **single `0 - 59` centre block**, two ellipticity blocks, and individual sigma blocks. This is a many-to-many mapping, not line-for-line correspondence. Solved annotations absent from `model.info` need to be identified as additional information.

4. **Replace unrestricted masonry with predictable reading order and bounded detail.**  
   In **A_05**, `shear` sits above `mass`; the structural `model.info` summary orders `bulge, mass, shear`. The reader must choose between reading across and reading down. Use stable ordered columns or rows, then collapse detail to fit. Provide a readable overview plus component detail views for A_06; fitting the width of a laptop is not the same as fitting its screen.

5. **Move large-model correctness into the first release gate.**  
   Fixed tuples, missing parameters, tuple sharing, grouping fidelity, and width limits cannot wait until phase 3: they determine whether phase 2’s automatically saved figure is truthful. Make A_04–A_06 acceptance cases for extraction and the first renderer. Keep automatic per-search output opt-in until those cases pass.

#### Encoding critique

**Keep the white component cards.** In A_02 they clearly separate the two Gaussians; in A_04 they distinguish light, mass, and shear without a forest of ownership arrows. The name-only pills are considerably calmer than v1’s tables.

Several refinements are necessary:

- **“Free” and “shared” are not mutually exclusive states.** A shared prior can still be sampled. Represent sampling status and sharing as separate properties, even if sharing uses a small blue badge.
- **“Solved” needs qualification.** A dashed `intensity` pill may suggest a completed fit or a known answer. Use legend wording such as “solved during fitting,” and emit it only from verified domain semantics. In A_05, `Basis.intensity` alongside member intensities risks implying an additional solved amplitude.
- **Relations need their defining expression.** In A_02, orange `ƒ sigma` identifies a relation but does not explain it. An optional-detail policy is appropriate for prior limits; the defining expression of a dependency is more central.
- **Assertions need unambiguous operands.** A_02’s `assert <` and long orange routes require tracing several nearby junctions. Show a compact constraint label containing both operand paths. Distinguish constraint edges from dependency arrows.
- **Tuple pills need a dimension cue.** A_04’s `centre` and `ell_comps` each conceal two scalar parameters. A small “2D” annotation explains why counting pills does not reproduce “19 free.” Partially fixed or partially shared tuples must expand or show a mixed state.

**Show fixed parameters by default.** They explain model structure, especially fixed centres and widths. Offer explicit omission with a visible hidden-count summary. A_06’s missing extra-galaxy centres is misleading because their absence can look like absence from the model.

**Redshift deserves a presentation convenience, not a different semantic rule.** A compact `redshift = 0.5` beneath `lens · Galaxy` is useful orientation and worth an exception to the no-numbers preference. A free redshift must retain the ordinary sampled-parameter encoding.

#### Scalability

A_06 demonstrates successful **structural compression**, but not yet successful **reading at screen size**. Its small text, tall page, and repeated padding demand scrolling or zooming.

Recommended defaults:

- Remove redundant outer framing where it adds no branching information.
- Reduce padding progressively through nested containers.
- Keep text size stable; collapse content instead of shrinking the entire figure.
- Offer overview and selected-subtree exports with the same vocabulary.
- Reserve gutters for cross-links and use labelled references when links become numerous.

The nested tints are readable in A_04, but A_06 asks the reader to distinguish too many nearly identical background levels. Let boundaries, indentation, and labels carry hierarchy; tint should assist.

R1/R2 also need a stronger safety condition: grouping must preserve **sharing, relations, assertions, and exceptions**, not merely matching component trees and prior configurations. A repeated component is not necessarily an independent statistical replicate. State what the plate repeats.

#### model.info contract

The right promise is:

> Every displayed model element resolves to its corresponding path or grouped paths in `model.info`; every omission or added annotation is explicit.

The README’s stronger “line for line” claim does not hold:

- **A_04:** `centre` represents a parent block and two scalar leaves; solved `intensity` is absent from the supplied dump.
- **A_05:** figure group boundaries differ from the text’s centre grouping.
- **A_05:** mass parameter order differs from the grouped dump.
- **A_05:** the mesh name/state is wrong; missing Hilbert configuration fields are also absent from the picture.

Choose and document whether visual order follows the structural summary or parameter-detail section; the supplied dump itself uses different orders.

Keep exact attribute spelling visible. Full paths should be available through a static companion index and, later, selection or hover. A PNG must remain navigable without hover.

The footer also needs a count definition. Prefer **“16 unique sampled scalars”** over unexplained “16 free”; define whether “shared” counts unique shared variables or repeated references. State when totals include hidden elements.

#### Graphical/EP

**Approve the separation between a teaching-oriented model view and an explicit EP factor graph.** They answer different questions.

For **A_08**:

- Connect the parent distribution to `centre_i`, rather than ending the arrow at the dataset frame.
- Replace the shared marker with a hierarchical-draw annotation.
- Give observed data an explicit observed encoding; fixed model constants and observations are different concepts.
- Include the two free hyperparameters in the accounting, separately from the three parameters per dataset.

Plate inference must inspect actual sharing and hierarchical membership. Matching model shape does not establish identical priors, analyses, or conditional independence.

For EP, start with **factor status, update age, and confirmed rejected/reverted updates**. Add sparklines and posterior summaries as optional detail. Do not label `Status.changed[v] is False` as “reverted” unless its semantics establish rejection; “unchanged” and “reverted” require different explanations.

Likewise, message precision should not be presented casually as “how strongly this factor constrains the variable.” Such a display needs defined handling of signed or invalid site precisions.

At large dataset counts, show status aggregates and exceptional members, with individual factor access. A collapsed plate must not conceal failures behind an average.

#### Architecture & phasing

**Approve matplotlib containment as the initial renderer.** It matches the chosen layout, supports static exports, and avoids an unnecessary external layout dependency. C_05 supports this choice for these models; it does not prove every possible tree layout fails.

Keep three separate layers:

1. **Semantic extraction:** paths, identity, parameter states, relationships, provenance.
2. **Presentation transformation:** grouping, omission, ordering, detail level.
3. **Layout/rendering:** measurement, placement, routing, drawing.

The proposed `ParamRow.kind` is too exclusive: sharing, dimensionality, and sampling status are separate properties. The specification also needs explicit missing, solved, hierarchical-draw, and observed states. Preserve path occurrences separately from object identity.

Revise the phases:

- **Before phase 1:** reconcile DESIGN.md’s v1 table vocabulary with the v2 pills and settle semantic/count definitions.
- **Phases 1–2:** include large-model correctness, deterministic order, fixed tuples, missing configuration, and bounded layouts.
- **Phase 3:** domain documentation and examples, building on already-correct rendering.
- **Phase 4:** shared-versus-hierarchical teaching examples.
- **Phase 5:** EP diagnostics, with layout-engine choice still open.

Prefer one consistent renderer for small and large models; a separate caskade mode is optional polish. PNG plus SVG/PDF export would serve both search output and documentation.

#### Minor nits

- A_02 uses orange semantics absent from its legend.
- A_01’s universal legend is disproportionately large and its canvas has unnecessary empty space.
- A_06’s empty Hilbert card needs an explicit explanation.
- A_05’s blue connector grazes the plate boundary; give it a dedicated gutter.
- Tiny muted labels and footers need stronger contrast at intended display size.
- Explain class-family header colours, or keep them strictly decorative.
- Remove the short header stems if enclosure already makes ownership clear; they currently resemble partial wiring.
- Renumber panel titles consistently: the supplied sequence jumps between `(a)`, `(b)`, and `(e)`.