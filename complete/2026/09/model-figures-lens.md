## model-figures-lens
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/736 (closed completed 2026-09-11)
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1615 (merged)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/550 (merged)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/616 (merged)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/737 (merged)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/541 (merged)
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/240 (merged)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1615
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/550
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/616
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/737
- epic: model-figures — phase 3 of 6 shipped; phase 4 (`draft/feature/autofit/model_figures_4_graphical_plates.md`) unblocked; phase 5 after 4; phase 6 after 3 and 4
- session: local-dev, Fable architect session; five Opus legs (PyAutoFit protocol; lens semantics + renders + docs; library gates + 4 PRs; workspace cookbooks; workspace ship); worktree `~/Code/PyAutoLabs-wt/model-figures-lens` over six repos on one branch name so `lib-tests.yml` resolved the sibling branches; parallel-claim waiver vs `remove-parallel-ep-optimiser` (#1612)
- summary: |
    PyAutoFit cannot know which lens parameters a fit solves rather than
    samples, and phase 2's `solved_paths=` could only re-tag rows that exist.
    `graph_spec` now reads a class attribute `__solved_parameters__` from a
    model's `cls` (the same probe shape as `__exclude_identifier_fields__`)
    and appends a `solved` row per declared name that is not a slot
    (provenance `solved-by-fit`, `in_model_info=False`), re-tagging one that
    is; `solved_paths=` is additive (unmatched → synthesised on the owner,
    never ignored); rule R7 drops `af.Model(cls)` for any int/float subclass
    so a free `Redshift` is a pill on its galaxy card; `counts["solved"]`,
    `name · solved` pill text and a footer phrase. Declared on
    `LightProfileLinear` (`intensity`), `PointSolved` (`centre`),
    `aa.Pixelization` (`reconstruction`); `Basis` declares nothing (members
    carry the solved amplitudes). Real-class acceptance in
    `test_autolens/model_figure` (simple lens; MGE 2×30 linear Gaussians +
    Delaunay/ConstantSplit source; group scale with eight synthetic centres)
    and `test_autogalaxy/profiles/test_model_figure_semantics.py`. Docs:
    both `model_cookbook.md` pages re-synced to their scripts with a figure
    per stage, PyAutoLens gains `## Solved Parameters` and `## Reading the
    Figure` (correspondence contract, plate-vs-model.info grouping, tint =
    nesting depth, decorative); `overview_3_features.md` MGE / pixelization /
    point figures. Workspaces: figures at every `model.info` stage of both
    modeling cookbooks, Redshift Free builds its model, new Solved
    Parameters stage, `source.effective_radius` typo fixed, notebooks
    regenerated, `model_figure: false` in both `config/output.yaml`.
- tests: PyAutoFit +18 (graph_spec 66, model_figure 80; full 2732); PyAutoGalaxy +12; PyAutoLens +19; full suites PyAutoArray 1512, PyAutoGalaxy 1207, PyAutoLens 646+1 xfail; black clean; Sphinx 110 ≤ 134 (lens), 95 ≤ 105 (galaxy). CI green on all four libraries (3.12/3.13/no-jax/docs) and both workspaces (smoke 3.12/3.13, navigator, size guard).
- acceptance: |
    MGE + pixelized on real classes (1323×945 px): 11 model cards, two
    `30 components` plates split on `ell_comps`, `centre` owner `shared
    across group`, `intensity · solved` on every member, `reconstruction ·
    solved`, `areas_factor · missing`, 6 shared priors, 61 solved, 14 unique
    sampled scalars (epic target 16 was measured on the phase-1 double whose
    source was a Sersic; the real pixelized source has 1). Group scale: one
    `8 components` plate, `centre · fixed, varies by member`, `sigma`
    independent. Simple lens: six cards in `model.info` order. Max PNG width
    1323 ≤ 1400.
- traps: |
    - `solved_paths` was a re-tagger only; a path absent from `__dict__` was
      silently ignored — the protocol is additive for exactly that reason.
    - `Model.constructor_argument_names` filtered only `self`; a class with a
      custom `__new__(cls, …)` (`ag.Redshift`) leaked `cls` as a parameter and
      overwrote `Model.cls` with a ConfigException, so `af.Model(al.Redshift)`
      never worked (the cookbook built it but never printed). Fixed in #1615.
    - Prompt facts stale vs the stack: `Pixelization(mesh, regularization)` is
      two-deep (image meshes are instances built before the fit);
      `areas_factor` lives on `Delaunay/DelaunayNN/KNN` meshes, not `Hilbert`;
      no `Voronoi` mesh; `AdaptSplit`, not `AdaptiveBrightnessSplit`.
    - `af.Model(al.mesh.Delaunay)` is not "three missing rows": `pixels` is an
      R7 fixed row from its `int` annotation, `zeroed_pixels` takes its
      default; only `areas_factor` is `ConfigException`/missing under the
      library's null `priors/mesh/delaunay.yaml`. autolens_workspace pins it
      to a constant 0.5, so the same code drawn from the workspace shows a
      fixed pill (docs page says so).
    - `af.Model.from_json` writes zero-free-parameter components back as
      instances (Delaunay mesh, PointSolved galaxy) — filed
      `draft/bug/autofit/model_from_json_drops_zero_free_parameter_components.md`.
    - A relation on one tuple component is carried by the spec but not drawn
      on the tuple pill — filed
      `draft/feature/autofit/model_figure_tuple_component_relations.md`.
    - Lens latent keys are bare names, so `analysis=` latents land on the root
      card; dotted keys are a possible follow-up.
    - The lens cookbook had 7 `print(model.info)` (6 distinct + JSON reload)
      and no MGE/pixelization/point stage; the Solved Parameters stage was
      added for the semantics this phase exists for.
    - `pyauto-heart smoke` grades the canonical checkout, so workspace scripts
      using unreleased symbols are run headless from the worktree instead;
      workspace CI checks out the same-named library branches.
    - Heart YELLOW (autolens workspace validation, profiling drift, no
      rehearsal) acknowledged by the human for phase 2 the same day; the
      identical reason set was carried for this ship.
- notes: |
    Scope widened from the prompt's four repos to six (PyAutoFit +
    PyAutoArray) — recorded on the issue and in the approved plan. `Basis`
    deliberately declares no solved amplitude (review caveat resolved
    empirically: it has no model-level amplitude). `docs/images/` was not
    created; each repo's live `docs/<section>/images/<page>/` convention was
    used. Flipping `model_figure` to default-true remains a separate human
    decision (ledger). PyAutoGalaxy's `autofit>=` floor was not bumped; the
    class attributes are harmless on older PyAutoFit.

## Original prompt

# Model figures phase 3 — lens semantics and cookbooks

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- autolens_workspace
- autogalaxy_workspace
Themes:
- visualization
- mge
- pixelization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: model-figures
Phase: 3
Filed: 2026-09-10
Issued: 2026-09-11

**Phase 2 shipped 2026-09-11** — `complete/2026/09/model-figures-renderer.md` (PyAutoFit#1614 merged, autofit_workspace#152 merged); this phase is unblocked.
(Deliberately not in a `Blocked-by:` header: that key is graded against GitHub
refs and cannot name a Mind prompt path.)

Phase 3 of the `model-figures` epic. Ledger (brief, full design record, full
independent review): `draft/feature/autofit/model_figures_epic.md`. By this
phase the renderer is already correct on the acceptance models; phase 3 supplies
the **lens domain semantics** it renders and puts the figures into the lens
documentation.

## Domain semantics hooks

PyAutoFit cannot know which parameters a lens fit solves rather than samples.
Supply that from PyAutoGalaxy / PyAutoLens as data the phase-1 spec consumes —
a registry or a small protocol, **not** hard-coded class-name strings inside
PyAutoFit:

- **Linear light profiles** (`al.lp_linear.*`) and **`al.lp_basis.Basis`** —
  `intensity` is **absent from the model entirely**; it is solved by the
  inversion. It must be emitted as a `solved` pill with the legend wording
  "solved during fitting", or the figure silently misreports the profile as
  having no amplitude. Beware the review's caveat: a `Basis.intensity` drawn
  alongside member intensities risks implying an *additional* solved amplitude —
  decide and document where it belongs.
- **Pixelization** — the source pixels are solved; `al.Pixelization` is a
  3-deep chain (`image_mesh` / `mesh` / `regularization`) whose only free
  parameters are the regularization coefficients. `mesh_shape` and `pixels` are
  plain scalar attributes, not priors: rows on their owner, never boxes.
- **`al.ps.PointSolved`** — zero parameters; the centre is solved analytically.
  `al.ps.Point` has two. Without the annotation the box looks empty and wrong.
- **`areas_factor`** — the `missing` state. It is unset configuration, not a
  solved quantity and not an absent one. This is an explicit review finding
  (the prototype labelled a `Delaunay.pixels` pill "solved" when the real gap
  was `areas_factor`) and it is an epic acceptance case.
- **Redshift** — fixed redshift renders as `redshift = 0.5` under the galaxy
  header (a presentation convenience, not a different semantic rule); a free
  redshift (`af.Model(al.Redshift)`) keeps the ordinary sampled pill.

## Class-family header tint — decide it here

The review's nit: either **explain** class-family header colours (light / mass /
pixelization) in the legend, or keep them **strictly decorative** and say so.
Do not ship an unexplained semantic-looking encoding. Whichever way it goes,
record the decision in the docs page.

## Documentation deliverables

- `autolens_workspace/scripts/guides/modeling/cookbook.py` — 442 lines with **6
  `model.info` stages**; each gains its figure.
- `@PyAutoLens/docs/general/model_cookbook.md` and
  `@PyAutoLens/docs/overview/overview_3_features.md` — PNGs committed under
  `docs/images/` and referenced by raw URL, matching the existing pattern.
- The equivalent PyAutoGalaxy / `autogalaxy_workspace` cookbook stages where
  they mirror the lens ones.

## Document the plate-vs-`model.info` grouping difference

This is the one place the promised correspondence is genuinely many-to-many and
it must be written down for readers, not papered over:

> The figure partitions **by component**: the MGE model shows two `30 components`
> plates, split because each basis holds its own `ell_comps` pair. `model.info`
> groups **per parameter**: it prints a single `0 - 59` block for `centre`
> spanning both figure plates, two separate ellipticity blocks, and individual
> `sigma` blocks.

The contract that does hold, and which the docs should state: every displayed
element resolves to a path or grouped paths in `model.info`; every omission and
every added annotation (`solved`, `missing`) is explicit. Solved annotations
have no counterpart in `model.info` at all and must be identified as additional
information.

## Acceptance

- The three lens acceptance figures from the ledger render truthfully with lens
  semantics attached, and the renders are committed.
- All 6 cookbook stages carry a figure; the docs pages build with the images.
- Once these pass, the per-search `output.yaml` key `model_figure` (phase 2) may
  be proposed for default-`true` — a **separate human decision**, recorded in
  the ledger, not taken inside this phase.
