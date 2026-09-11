## model-figures-renderer
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1613 (closed completed 2026-09-11)
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1614 (merged)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/152 (merged)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1614
- epic: model-figures — phase 2 of 6 shipped; phase 3 (`draft/feature/autolens/model_figures_3_lens_cookbook.md`) and phase 4 (`draft/feature/autofit/model_figures_4_graphical_plates.md`) are now unblocked
- session: local-dev, Fable architect session; implementation, tests, docs, ship and workspace legs delegated to five Opus subagents (worktree `~/Code/PyAutoLabs-wt/model-figures-renderer`, parallel-claim waiver vs `remove-parallel-ep-optimiser` #1612, disjoint files)
- summary: |
    New package `autofit/model_figure/` draws the phase-1 `GraphSpec` as a
    pure-matplotlib containment figure, exposed as
    `af.ModelPlotter(model, analysis=None, solved_paths=()).figure(path=None,
    filename="model", format="show|png|svg|pdf", detail="names|priors",
    collapse=True, max_depth=None, show_fixed=True, width=14.0)`. Three
    layers: `presentation.py` (no matplotlib: cards, name-first pills with
    states free/fixed/fixed-varies/relation/solved/missing/folded, sharing as
    a blue badge — `shared across group` on the owner, `↗ owner` on
    references — plates badged `N components` with the `0 - 29`
    representative key and the `repeats` line, `2D` tags, mixed tuples
    expanded, `redshift = 0.5` subtitle, `assert …` constraints, one-line
    legend, defined-count footer), `layout.py` (Agg text measurement, fixed
    font sizes, padding shrinking per level, pill flow-wrap, top-level cards
    wrapped at the width budget in declaration order, a right-hand gutter for
    orthogonal links anchored on the top-level card edge, `LayoutTree.to_dict`
    as the determinism artefact) and `render.py` (FancyBboxPatch cards/pills,
    dashed plates and solved pills, dashed-orange unfilled constraint boxes,
    `save` mirroring `output_figure`). Per-search: `DirectoryPaths._save_model_info`
    writes `model.png` beside `model.info` when the NEW `output.yaml` key
    `model_figure` is true — read strictly via `_model_figure_enabled()`
    (absent → off; `should_output` would fall back to `default: true`), skipped
    under `PYAUTO_SKIP_VISUALIZATION`, any exception logged and swallowed.
    Key added as `false` to the library default, `test_autofit/config` and
    `autofit_workspace/config`. Evidence: 11 PNGs + `make_figures.py` under
    `docs/images/model_figures/`, embedded in `docs/cookbooks/{model,
    multi_level_model,multiple_datasets}.md`. Workspace: nine
    `af.ModelPlotter(...).figure()` calls with map/legend prose in the three
    cookbooks, notebooks regenerated, config key.
- tests: 85 new — `test_autofit/model_figure/` 76 (vocabulary rules, width budget, fixed text size across cases, declaration order, determinism of the layout dict across builds and a subprocess plus PNG bytes in-process, file output, matplotlib import purity) + `test_autofit/non_linear/paths/test_model_figure_output.py` 9 (config gate true/false/absent, test-mode skip, renderer failure swallowed). Full `test_autofit` 2714 passed serially; black + pyflakes clean; Sphinx warnings 30 = baseline. CI green on docs, 3.12, 3.13, no-jax; workspace smoke 3.12/3.13 + navigator green on the same-named library branch.
- acceptance: |
    (a) simple lens 839×584 px, 6 model cards in `model.info` order; (b) MGE
    2×30 + pixelized 1121×976, 11 components, two `30 components` plates split
    on `ell_comps`, `centre` owner `shared across group`, `areas_factor ·
    missing`, footer `16 unique sampled scalars · 63 fixed leaf slots · 6
    shared priors · 1 missing · 2 plates standing for 60 components`; (e)
    group scale 1042×886, one `8 components` plate with `centre · fixed,
    varies by member` and `independent` priors. Max width 1121 px ≤ 1400 cap;
    identical font sizes across the toy Gaussian and group-scale layouts.
    Composite (shared + relation `sigma = a.sigma * 2.0` + `assert a.sigma >
    5.0`) renders all three encodings. These are the phase-1 structural
    doubles; phase 3 re-renders the real PyAutoLens models.
- traps: |
    - `should_output(name)` falls back to `output.yaml` `default:` on a
      missing key, and every workspace sets `default: true` — a new
      opt-in key must be read strictly or it silently switches on in the
      ~15 configs that lack it.
    - The PyAuto API-gate hook blocks one-liners naming `af.ModelPlotter` /
      `autofit.model_figure` as "not in installed stack" until the canonical
      checkout carries it; `PYAUTO_SKIP_API_GATE=1` for branch-only symbols.
    - `pyauto-heart smoke` grades against the canonical checkout, so a
      workspace script using an unreleased library symbol must be run headless
      from the task worktree (activate.sh) instead; workspace CI checks out the
      same-named library branch and is fine.
    - `graph_spec` names relation/assertion operands by the compound prior's
      own slot path (`b.sigma.self`); the presentation layer rewrites them via
      the `ParamRow.occurrences` map so pills read `a.sigma`. `PlateInfo.repeats`
      never says "independent" — derived from free unshared rows in an N-plate.
    - `ParamRow` carries no prior parameters (only `prior_cls_name`), so
      `detail="priors"` reads `Prior.parameter_string` from the model via
      `prior_summaries(model)`.
    - The group-scale double has no `missing` row; `Hilbert.areas_factor` lives
      in the MGE double. The epic brief's case (e) wording was off.
    - `ledger_merge.py classify --base origin/main` hangs; pass explicit paths.
    - The test-mode env var is `PYAUTO_SKIP_VISUALIZATION`, not
      `PYAUTOFIT_TEST_MODE`.
- notes: |
    Deviations from the prompt, all recorded on the issue: plate cards are
    titled by class name only (the member index is meaningless); reference
    badges are relative (`↗ 0.centre`) with the full path kept on the link
    key; links are dropped above `Style.max_links=12` in favour of labelled
    references (expanded MGE has 118); a `folded` pill state carries
    `max_depth`; `Card` has no constraints field (`Constraint.key` names the
    owning card); empty cards read `no parameters`. `figure()` follows
    autofit's `output_figure` convention (`path` = directory, `format`), not
    the prompt's sketch. No `model.figure()` alias. Four pre-existing
    `` `Gaussian`'s `` possessives in `multi_level_model.py` left untouched.
    Follow-ups worth filing: sweep those possessives; add a `GraphSpec` /
    `ModelPlotter` entry to `docs/api/` (none lists plot helpers today).

## Original prompt

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
Issued: 2026-09-11

**Phase 1 shipped 2026-09-11** — `complete/2026/09/model-figures-graph-spec.md` (PyAutoFit#1606 merged); this phase is unblocked.
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
