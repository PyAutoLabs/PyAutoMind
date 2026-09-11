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
