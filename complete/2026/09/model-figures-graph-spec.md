## model-figures-graph-spec
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1605 (closed completed 2026-09-11)
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1606 (merged)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1606
- epic: model-figures — phase 1 of 6 shipped; phase 2 (`draft/feature/autofit/model_figures_2_renderer.md`) is now unblocked
- session: web-github (session clone of PyAutoFit, no task worktree; issue, PR and merge driven through the GitHub MCP surface; implementation delegated to two Opus subagents from a Fable session)
- summary: |
    New `autofit/graph_spec.py` — the pure semantic layer of the model-figures
    epic. `GraphSpec.from_model(model, analysis=None, collapse=True,
    solved_paths=())` turns any `AbstractPriorModel` into frozen, JSON-stable
    dataclasses: `ComponentNode`s in declaration order (the walk order of
    `path_instance_tuples_for_class(..., ignore_children=True)`, i.e.
    `model.info`'s parameter-detail section — the structural summary was
    rejected because `find_groups(limit=0)` reorders it), one `ParamRow` per
    parameter slot carrying independent properties (sampling
    `free|fixed|solved|missing`, sharing as prior id + path occurrences,
    dimensionality with per-slot tuple components so partial fixes/shares are a
    mixed state, provenance with relation expressions built from a symbol
    table), `SharedEdge` / `RelationEdge` / `AssertionEdge`, a `model.info`
    path index and reconciling counts. Sibling `Model`s collapse into plates by
    R1 (class tree + prior configuration, ignoring prior id / `_label` /
    constant values) and R2 (split by cross-member shared priors) under the
    review's safety condition; plates group over the existing `find_groups`
    and the path index records where the figure's partition is finer than
    `model.info`'s. Exported as `af.GraphSpec` / `af.graph_spec_from`. No
    matplotlib import (asserted), `af.VisualiseGraph` untouched, no new deps
    or config keys.
- tests: 52 new in `test_autofit/graph_spec/` — the 18-construct catalogue, collapse rules, determinism (byte-identical `to_dict()` across runs and id resets, in-process and across processes), a matplotlib-purity subprocess check, and the three lens acceptance models as structural doubles. CI green on 3.12 / 3.13 / no-jax / docs.
- acceptance: |
    The lens acceptance cases are structural doubles of today's
    autolens_workspace scripts (autofit may not import autolens). (b) MGE 2×30
    + pixelized source meets every epic invariant: 11 boxes, two ×30 plates
    split on `ell_comps` (never one ×60), shared multiplicities
    60/60/30/30/30/30, 16 unique sampled scalars, `areas_factor` in the
    `missing` state, per-Gaussian `sigma` recorded as `varies_by_member`.
    (a) simple lens: 8 raw nodes → 6 boxes in declaration order (17 rows vs the
    epic's 13 — redshift and intensity rows counted). (e) group scale: today's
    `group/modeling.py` composition with 8 extra galaxies is far smaller than
    the prototype's model (33 raw nodes vs 166, 0 shared priors vs 22), so its
    numeric counts are pinned as measured with `# epic target` comments; the
    structural invariant holds (8 galaxies → one plate `0 - 7`, per-galaxy
    fixed `centre` tuples present and `varies_by_member`). Phase 3 re-runs the
    assertions on the real classes in PyAutoLens.
- traps: |
    - Rows are read from each component's `__dict__` directly, not from the
      `direct_*` properties: those cannot see raw instance leaves, lose
      declaration order once merged, and carry the known `Constant`
      double-count.
    - `all_paths_prior_tuples` reports a relation operand at a second path
      inside the `CompoundPrior` (`('centre','self')`); `occurrences` keeps it
      literally but `direct_occurrences` drives `shared`, `SharedEdge`, the
      shared count and R2 — a relation operand is related, not shared.
    - `obj_id` is the `ModelObject` id counter, not `id(obj)`; `model.copy()`
      preserves `.id`, so two independently freed copies share an `obj_id`.
    - A `None` attribute (`Basis(regularization=None)`) is not a slot —
      `model.info` prints nothing for it — so it emits no row.
    - `Model(int)` with no leaf is an explicit added annotation
      (`in_model_info=False`); with a prior/constant/ConfigException it is a
      free/fixed/missing row on its owner (R7).
    - `Hilbert.areas_factor` no longer exists in autoarray; the double keeps it
      because it is the epic's `missing` case. Today's `Delaunay` takes no
      `pixels`, so the "12 before R7" `Model(int)` node is absent.
    - `ComponentNode` keeps rows and children as separate ordered fields, so a
      row declared after a child model renders before it — a phase-2 renderer
      concern.
    - xdist collection is nondeterministic in `test_autofit` (pre-existing);
      run the suite serially. `TestEmceeContainment` failed once on a full run
      and passed on re-run (stochastic).
- notes: |
    Plan approved 2026-09-10; issue #1605 carries the two-level plan. Phase 1
    left `user-prior`, `assertion`, `hierarchical-draw` and `observed`
    provenance kinds reserved and documented; `solved` is carried via
    `solved_paths=` for phase 3's domain rules.

## Original prompt

# Model figures phase 1 — semantic extraction

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
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
Phase: 1
Filed: 2026-09-10
Issued: 2026-09-10

Phase 1 of the `model-figures` epic. Ledger (read it for the brief, the visual
vocabulary, the full design record and the independent review):
`draft/feature/autofit/model_figures_epic.md`. This phase draws nothing — it
builds the pure semantic layer everything later renders over.

## What to build

A new module `@PyAutoFit/autofit/graph_spec.py` — **pure extraction, no
drawing, no matplotlib import**, no dependency beyond `autofit/mapper/`. It
turns any `af.AbstractPriorModel` (and, in phase 4, a `FactorGraphModel`) into
a **nesting tree**:

- `ComponentNode{path, name, cls_name, obj_id, rows, children, multiplicity}` —
  one node per `Model` / `Collection` / `GlobalPriorModel`. `path` is the full
  tuple path in the model; `obj_id` is the Python object identity (this is how a
  component shared across datasets is detected: the same `obj.id` at several
  paths).
- `ParamRow` — one row per *parameter slot*, carrying **separate properties, not
  one exclusive `kind`** (see below).
- Edge records: `SharedEdge`, `RelationEdge`, `AssertionEdge`.

The three-layer split is a hard requirement of the review: **semantic
extraction** (this phase) / presentation transformation (grouping, omission,
ordering, detail level) / layout and rendering (phase 2). Nothing in this
module may know about pixels, fonts or colours.

### `ParamRow` is a bag of properties, not a single kind

The original design proposed `kind ∈ free|fixed|relation|instance|pointer`. The
review rejected that as too exclusive — a shared prior is *still sampled*, a
tuple is *still free*. Model each of these independently:

| Property | Values | Source |
|---|---|---|
| **sampling status** | `free` \| `fixed` \| `solved` \| `missing` | `free` = a `Prior` in the tree; `fixed` = a `Constant`; `solved` = a quantity the fit determines but that is absent from the model (linear light profile `intensity`, pixelization pixels, `al.ps.PointSolved` centre) — phase 3 supplies the domain rules, phase 1 only carries the field; `missing` = a required configuration value that is unset (e.g. `areas_factor`), which must never look like absence from the model. |
| **sharing** | prior identity (`prior.id`) + the **list of path occurrences** | keep occurrences separately from object identity — the review is explicit that a shared prior is a property of a *sampled* row, not a separate state. |
| **dimensionality** | scalar \| 2-D tuple (and the component scalars it holds) | so pill counts reconcile with the footer's "16 unique sampled scalars". A partially fixed or partially shared tuple must be representable as a mixed state, not flattened. |
| **provenance** | `config-default` \| `user-prior` (best effort) \| `relation(expression)` \| `assertion(operands)` \| `hierarchical-draw` \| `observed` | relations carry their **defining expression** (`= sigma × 2`); assertions carry **both operand paths**; a hierarchical draw is `centre_i` "drawn from", **never** a sharing marker; observed data gets its own encoding, distinct from `fixed`. |

`name` is the exact attribute spelling, preserved verbatim. Full paths stay on
the record even when the renderer shows only the name.

### Ordering

**Declaration order is preserved end to end.** The review's point 4: in the
prototype `shear` floated above `mass` because the layout was free-form
masonry, while `model.info` orders `bulge, mass, shear`. The spec emits
children and rows in declaration order and the renderer is forbidden from
reordering them for packing. `model.info` itself uses different orders in its
structural summary versus its parameter-detail section — pick one, document the
choice in the module docstring, and be consistent.

### Collapse rules R1/R2, with the safety condition

- **R1 soft plate.** Sibling `Model`s collapse into one plate when their class
  tree *and prior configuration* match — **ignoring prior identity, prior
  `_label`, and constant values**.
- **R2 shared split.** Split a plate by the partition its **cross-member** shared
  priors induce. A prior appearing in *every* member (the MGE centre) does not
  discriminate; one appearing in a *subset* (basis-0's `ell_comps`) does, giving
  `Gaussian ×30` + `Gaussian ×30`. A prior shared only *inside* one member never
  splits the plate — without this qualifier the 8 extra galaxies of the group
  model fall back to 8 separate boxes.
- **Safety condition (Codex review point 7, mandatory).** A plate must preserve
  **sharing, relations, assertions and exceptions** across its members, not
  merely class tree + prior configuration. A repeated component is not
  necessarily an independent statistical replicate. Any member that differs in
  any of those four respects leaves the plate and is drawn on its own. The spec
  records **what the plate repeats**, as a field, so the renderer can say it.

Reuse — do not re-invent — **`find_groups` in
`@PyAutoFit/autofit/mapper/prior_model/representative.py`**. It is the collapse
primitive `model.info` already uses to print `0 - 29` / `30 - 59`, and the
figure must group over it rather than inventing a second, divergent notion of
sameness. Where the figure's partition is necessarily *finer* than
`find_groups`' (the figure partitions by component, `model.info` groups per
parameter), record the mapping rather than hiding it — phase 3 documents it.

### The `model.info` correspondence contract

Not "line for line". The contract, in the module docstring and in the tests:

> Every displayed model element resolves to its corresponding path or grouped
> paths in `model.info`; every omission and every added annotation (`solved`,
> `missing`) is explicit.

Emit a lightweight **path index** alongside the spec so a static PNG stays
navigable: element → path(s) in `model.info`.

## Verified extraction primitives (DESIGN §5, all executed)

- `path_instance_tuples_for_class((Model, Collection), ignore_children=False)` —
  the component nodes.
- `path_priors_tuples` — free parameter slots.
- `all_paths_prior_tuples` — groups a prior with **all** its paths; this is the
  sharing detector.
- `path_instance_tuples_for_class((Constant, float), ignore_class=Prior)` —
  fixed leaves.
- `path_instance_tuples_for_class((CompoundPrior, ModifiedPrior))` — relations.
- `gathered_assertions()` — assertions (a **method**, while `assertions` is a
  property; easy to mis-call).
- `find_groups` (`mapper/prior_model/representative.py`) — the collapse.

## Traps for the implementer (DESIGN §6, all verified by execution)

- `TuplePrior` **is not** an `AbstractPriorModel`: any walk over
  `direct_prior_tuples` + `direct_prior_model_tuples` silently loses every tuple
  parameter — i.e. every `centre` in every lens model.
- `CompoundPrior` / `ComparisonAssertion` **are** `AbstractPriorModel`s with
  `cls = float`, so they masquerade as components and must be filtered out of
  the component walk. Their operand names come from a stack-frame
  `retrieve_name()` (`cp._left_name` / `cp._right_name`), which is why the names
  are `sm`, `sc`, `x` in a hand-built relation but `self`/`other` when built by
  `ArithmeticMixin.__add__`.
- `repr()` of a `CompoundPrior` subclass without `__str__` **recurses forever**
  (`compound.py:88`). Never `repr` in a label path. (Filed separately as
  `draft/bug/autofit/assertion_repr_recurses_forever.md`.)
- Prior `_label` carries a per-instance counter (`einstein_radius2` vs
  `einstein_radius4`), which defeats naive equality when detecting plates.
- `fgm.graph` rebuilds on every access and renames `PriorFactor`s — cache it.
  `factor.name` is not unique across `_HierarchicalFactor`s; use
  `factor.name_for_variable(v)`, never `variable.label`. (Phase 4 leans on this;
  phase 1 only needs the tree.)
- `with_free_parameters` does **not** exist on the installed `af.Model`; the live
  multi-dataset idiom is `model.copy()` + `af.AnalysisFactor` +
  `af.FactorGraphModel`.
- `Model(int)` wrappers (e.g. `Delaunay.pixels`) need special-casing: plain
  int/float attributes are rows on their owner, never components.
- Fixed **tuple** constants inside a plate produced *no row at all* in the
  prototype (the extra-galaxy centres vanished). This is an acceptance case, not
  a nice-to-have — their absence reads as absence from the model.

## Tests — the 18-construct catalogue

One test per construct, each asserting the extracted spec, not a picture:

1. `af.Model(Cls)` with default priors.
2. Overridden prior (`m.centre = af.UniformPrior(...)`) — *indistinguishable*
   from (1) without a config diff; assert that, and record it as a known gap.
3. Fixed float (`m.centre = 0.0`, `af.Model(Cls, centre=0.0)`) → wrapped in
   `Constant`, absent from `prior_tuples`, present in `model.info`.
4. Shared prior (`m.a.x = m.b.x`) — the same `Prior` object at two paths.
5. Relation (`m.centre = m.norm + m.sigma`) → a `SumPrior` / `CompoundPrior`
   with `cls == float`; assert the expression string and both operands.
6. Assertion (`m.add_assertion(m.sigma > 5.0)`) — in `model._assertions`, not in
   the tree and **not in `model.info`**.
7. Tuple parameter → `TuplePrior` holding `centre_0`, `centre_1`; paths are
   `('centre','centre_0')`; one row with a 2-D cue.
8. `af.Collection(a=…, b=…)` — children as named attributes.
9. `af.Collection([m0, m1, m2])` — children named `"0"`, `"1"`, `"2"`.
10. Nested Collections.
11. Multi-level `af.Model(Cls, gaussian_list=[Model, Model])` — the list becomes
    a child `Collection` at `('gaussian_list',)`.
12. Instance leaf (`af.Collection(a=Model, b=instance)`) — a raw Python object
    with an injected `id`; `model.info` shows `Gaussian (N=0)`.
13. `af.Model(function)` — `model.cls` is the function, so `cls.__name__` works;
    note that config priors crash (filed as
    `draft/bug/autofit/model_function_cannot_resolve_config_priors.md`), so the
    test supplies explicit priors.
14. `af.Array(shape=…, prior=…)` — flat priors `prior_0_0`, `prior_0_1`, … plus
    `shape` / `indices` noise attributes that need a skip-list.
15. `FactorGraphModel.global_prior_model`, fully shared — all children the
    **same object** (`id == 1` for all three).
16. Per-dataset free parameters (`model.copy()` + reassignment) — shared params
    keep one `prior.id`, free ones get new ids.
17. Cross-dataset relation (`sigma = sm*x + sc`) — nested
    `SumPrior(MultiplePrior(sm, x), sc)`; assert the operand-name provenance.
18. Latent variables — **not part of the model at all**; they live on
    `Analysis.Latent` (`autofit/non_linear/analysis/latent.py`), and
    `Latent.keys(analysis)` returns dot-separated names (`"gaussian.fwhm"`).
    The spec must accept an optional `analysis=` and attach derived rows;
    without it, assert they are simply absent.

## Acceptance — the three lens models

Beyond the catalogue, the spec must be asserted against the real lens models.
These are the epic's acceptance cases and the review moved them **into the
phase 1–2 gate** rather than leaving them to phase 3:

- **(a) simple lens** — Sersic + Isothermal + ExternalShear + Sersic source.
  8 raw nodes / 48 info lines → 6 component boxes, 13 rows.
- **(b) MGE 2×30 + pixelized source** — 73 raw nodes / 178 info lines. Must
  yield **11 components** (12 before R7 drops the `Model(int)`), **two ×30
  plates split on `ell_comps`** (never one merged ×60), 6 shared priors with
  multiplicities 60, 60, 30, 30, 30, 30, and **16 unique sampled scalars**.
- **(e) group scale, 8 extra galaxies** — 166 raw nodes / 418 info lines → 15
  components (16 before R7), 41 unique sampled scalars, 22 shared priors, 291
  fixed leaf slots. Must render **fixed per-galaxy centre tuples** (the
  prototype dropped them) and an unset **`areas_factor` in the `missing`
  state** — not "solved", not absent.

Determinism is part of acceptance: run each extraction twice and assert
byte-identical spec output, including ordering.

## Out of scope

Drawing anything (phase 2), lens domain semantics (phase 3), plates over a
factor graph (phase 4), EP overlays (phase 5). `af.VisualiseGraph` (pyvis)
stays exactly where it is — do not touch or delete it in this phase.
