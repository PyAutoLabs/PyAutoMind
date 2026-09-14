The per-figure reading commentary that phase 6 of the `model-figures` epic rolled out
beside every `af.ModelPlotter` figure is gone. The human's verdict (2026-09-14): it is
information overload, and the figure should be self-explanatory. Every opener block —
opener sentence, map/legend paragraph, and all file-specific paragraphs after it —
now reads exactly:

> The same model can also be visualized as a figure, making its structure easier to
> understand at a glance.
>
> The figure shows how the model is organized: which parameters belong to each
> component, and whether they are free, fixed, shared, linked by an expression, solved
> during the fit, or not configured. `model.info` provides the corresponding numerical
> details, including the prior assigned to each free parameter and the value of each
> fixed parameter.

## Shipped

29 source files and 21 regenerated notebooks across six repos: PyAutoFit#1627,
PyAutoGalaxy#617, PyAutoLens#738 (docs only), autofit_workspace#158 (11 scripts),
HowToFit#56 (9 tutorials), autogalaxy_workspace#241 (1 script). All six branches
verified merged into `origin/main` with `git branch -r --merged`, not by PR state alone.

A second pass, approved mid-run, stripped the same figure-rendering vocabulary (pills,
plates, badges, greyed, footer counts) from the shorter notes at later figure sites —
35 notes rewritten across 14 scripts, 1 deleted outright, plus 7 `.md` pages.

## Kept deliberately

- **15 teaching sentences** that had been mixed into figure commentary, each reworded to
  stand alone: parameter-space dimensionality in three HowToFit tutorials, the
  multi-level hierarchy rationale, the shared-`centre`-makes-it-graphical point, the
  linear-profile `intensity` fact in autogalaxy_workspace.
- **The EP factor-graph blocks.** Box / pill / edge is standard probabilistic-graphical-
  model notation, and the state overlay reports per-factor update counts, update age and
  status — information `graph.info` does not provide. Not the redundancy being removed.
- **Image `:alt:` text** and `make_figures.py` generator docstrings: describing how a
  figure looks is the purpose of alt text, and stripping it would degrade screen-reader
  accessibility.
- In `PyAutoGalaxy` and `PyAutoLens` `model_cookbook.md` the solved/unconfigured material
  was **rewritten, not deleted** — a linear profile's `intensity` is solved by the
  inversion, a `Basis` owns no amplitude of its own, `areas_factor` has no configured
  prior so the model cannot be fitted until one is supplied. The `## Reading the Figure`
  section went, along with the cross-reference that pointed at it.

## Traps worth keeping

- **A line-based grep undercounts the census.** The `**map**` token wraps across a line
  break in two HowToFit tutorials, and `tutorial_4_hierachical_models.py` had a
  first-figure block with no map/legend paragraph at all. Use a whitespace-flattened
  per-file search, and match on the `**map**` paragraph rather than the opener — there
  are ~16 opener variants.
- **The recorded sphinx baselines are stale.** PyAutoGalaxy records 105 and PyAutoLens
  134; `main` itself builds 102 and 131 in this environment. The change was verified
  30/102/131 against same-env `main` builds, not against the recorded numbers.
- **`worktree_check_conflict` returned a false clean** when passed all six repos in one
  call, and fired on three of them when called one repo at a time. Loop and call it per
  repo. The claim it fired on (`howtofit-mode`, one uncommitted `README.md` per repo)
  was provably disjoint and waived; it merged during the run, so the waiver is now moot.
- `HowToFit/scripts/chapter_1_introduction/tutorial_1_models.py` is **no longer CRLF** —
  it is pure LF. A prior session's note said otherwise.

## Gate

Heart was YELLOW at ship time with nine pre-existing reasons — workspace validation
3 failed (cloud#34824535982), two manifest drifts vs `repos.yaml`, five profiling
drifts, and a stale "no rehearsal for current source". None touches a file this work
changes; the human acknowledged them explicitly. 18/18 runnable scripts exit 0, with
`searches/start_point.py`, `features/expectation_propagation.py` and HowToFit
`tutorial_5_expectation_propagation.py` edited but not runnable per `no_run.yaml`.

The same standard was applied to autolens_workspace and HowToLens under
autolens_workspace#542 (phase 6b wave 2), which shipped separately.

## Original prompt

# Model figure prose: replace the map/legend block with two short paragraphs

Type: docs
Target: workspaces
Repos:
- autofit_workspace
- HowToFit
- autogalaxy_workspace
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
Themes:
- visualization
- notebooks
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: model-figures
Phase: 6-prose
Filed: 2026-09-14
Issued: 2026-09-14

## Request (verbatim)

> Replace this text everywhere:
>
> The same model can also be drawn as a figure, which shows its structure at a glance.
>
> The figure is the **map** and `model.info` is the **legend**. The map shows the shape of the model: which component
> owns which parameter, and what state every parameter is in (free, fixed, shared with another component, related to
> one by an expression, solved during the fit or missing from your configuration). The legend gives the numbers: the
> prior on every parameter and the value of every fixed one.
>
> WITH:
>
> The same model can also be visualized as a figure, making its structure easier to understand at a glance.
>
> The figure shows how the model is organized: which parameters belong to each component, and whether they are free,
> fixed, shared, linked by an expression, solved during the fit, or not configured. model.info provides the corresponding
> numerical details, including the prior assigned to each free parameter and the value of each fixed parameter.
>
> Also remove all text and paragraphs after this one, for example:
>
> "The map here is the two planes of the lens system: the `lens · Galaxy` card subtitled `redshift = 0.5` holding
> `bulge · Sersic`, `mass · Isothermal` and `shear · ExternalShear`, and the `source · Galaxy` card subtitled
> `redshift = 1.0` holding `bulge · SersicCore`. `centre` and `ell_comps` are badged `2D` because each is a tuple of
> two free parameters, and the greyed `radius_break`, `gamma` and `alpha` pills on the source are fixed values, which
> is the difference between the footer's count of sampled scalars and the number of pills drawn."
>
> Imo, this is informaiton overload and the figure should be self explantory. Do this across all repos, HowTo's etc.
> This is prob gonna over a lot of scripts, HowTo, workspaces etc

## Context

Phase 6 of the `model-figures` epic rolled `af.ModelPlotter(model).figure()` out beside every bare
`print(model.info)`, and every first site in a script carries a map/legend opener plus one paragraph of
figure-specific reading commentary. The human's verdict (2026-09-14) is that the per-figure commentary is
information overload: the figure should be self-explanatory, so every block collapses to two fixed paragraphs.

Census (read-only, 2026-09-14) — 141 landed blocks across 8 repos:

| Repo | `.py` | `.ipynb` | `.md` |
|---|---|---|---|
| autolens_workspace | 44 | 44 | — |
| autofit_workspace | 11 | 11 | — |
| HowToFit | 6 | 6 | — |
| HowToLens | 6 | 6 | — |
| autogalaxy_workspace | 1 | 1 | — |
| PyAutoFit / PyAutoGalaxy / PyAutoLens (docs) | — | — | 3 / 1 / 1 |

**This prompt covers the six unclaimed repos only** (41 files). `autolens_workspace` and `HowToLens` (100 files)
are claimed by the in-flight task `model-figures-rollout-lens` (autolens_workspace#542, wave 2 stalled with 13
uncommitted blocks and ~53 sites unwritten); the human's decision is that those are handled by resuming that task
with the new standard, not by a parallel claim here.

## Replacement text (canonical, `model.info` backticked per the human's confirmation)

```
The same model can also be visualized as a figure, making its structure easier to understand at a glance.

The figure shows how the model is organized: which parameters belong to each component, and whether they are free,
fixed, shared, linked by an expression, solved during the fit, or not configured. `model.info` provides the
corresponding numerical details, including the prior assigned to each free parameter and the value of each fixed
parameter.
```

## Scope

Every `.py` block is structurally uniform (verified across all 88 landed script blocks): a column-0 `"""` opens,
at most three lines of opener prose follow, then the `The figure is the **map**` paragraph, then file-specific
trailing prose, then `"""`, then a `*Plotter(...).figure()` call. No block contains a `__Section__` header and no
block is followed by anything other than a plotter call, so the replacement is scriptable: from the docstring
opener through the line before the closing `"""`, substitute the canonical text.

Opener variants that must all be caught (the block is identified by the `**map**` paragraph, not the opener):

- `The same model can also be drawn as a figure, which shows its structure at a glance.`
- `The same model can also be drawn as a figure, via af.ModelPlotter.`
- `We can also draw the model, via af.ModelPlotter.` / `...this global model...` / `...a loaded model...`
- `The same model can also be drawn, via af.ModelPlotter.` / `As in tutorial 1, the model can also be drawn...`
- the long HowToFit / HowToLens "two views of the same model ... division of labour" variants
- one-off openers in HowToLens chapter 4 (`Drawing the model shows the multi-galaxy regime at a glance.`, etc.)

Out of scope:

- **Later short figure sites** — the one-to-three-line "map unchanged, legend moved" notes at the second and third
  figure in a script. The human quoted only the opener block.
- `autolens_workspace`, `HowToLens` (the resumed `model-figures-rollout-lens` task).

Library-docs `.md` handling (human-confirmed assumptions):

- Replace the map/legend paragraph with the canonical text and delete the figure-reading commentary that follows it,
  stopping at the next markdown heading.
- **Delete** the "how to read the figure" contract sections in `PyAutoGalaxy/docs/general/model_cookbook.md` and
  `PyAutoLens/docs/general/model_cookbook.md` (the explicit map-to-`model.info` contract, the nesting-tint note,
  the plate-badge-vs-shared-badge note) — the same overload in reference form.
- **Keep** the `Setting model_figure: true in a workspace's config/output.yaml` sentence in
  `PyAutoFit/docs/cookbooks/model.md` — setup information, not figure commentary.
- `PyAutoFit/docs/cookbooks/multiple_datasets.md` keeps its `{image}` directive and the `af.ModelPlotter(...)` code
  fence; only the prose is replaced.

## Verification

- Coverage grep: zero occurrences of `is the **map**`, `is its **legend**` or `drawn as a figure` remain in the six
  repos; the canonical first sentence occurs once per previously-matching file.
- Notebooks are **regenerated**, never text-edited:
  `PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py <key>` from each workspace root;
  commit only the touched twins (plus `llms-full.txt` / `workspace_index.json` if rewritten); `check_navigator.py` OK.
- Every touched script runs headless from its repo root under the smoke env profile
  (`PYAUTO_TEST_MODE=1 PYAUTO_SKIP_FIT_OUTPUT=1 PYAUTO_SKIP_VISUALIZATION=1 PYAUTO_SKIP_CHECKS=1
  PYAUTO_SKIP_API_GATE=1 MPLBACKEND=Agg`, worktree `activate.sh` sourced), exit 0, no traceback.
- `HowToFit/scripts/chapter_1_introduction/tutorial_1_models.py` is CRLF — preserve its line endings.
  `config/priors/*.yaml` are CRLF in these repos — do not touch them.
- Library repos are docs-only: sphinx warning count must equal the baseline built on `main` in the same env.

## Ship

`ship_workspace` for autofit_workspace, HowToFit, autogalaxy_workspace; `ship_library` for PyAutoFit, PyAutoGalaxy,
PyAutoLens (docs-only, pending-release). PR body `## Scripts Changed` by folder; no `## API Changes`.
