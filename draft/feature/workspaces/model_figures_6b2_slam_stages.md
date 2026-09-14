# Model figures phase 6b2 — the model figure in SLaM pipeline stages (decision first)

Type: feature
Target: workspaces
Repos:
- autolens_workspace
Themes:
- visualization
- notebooks
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: needs-decision
Epic: model-figures
Phase: 6b2
Filed: 2026-09-13

The SLaM half of the rollout map's "(b) PyAutoLens surfaces" bullet, cut out of phase 6b
and deferred on 2026-09-13 so that cut could ship the 147 ordinary script/tutorial sites
without waiting on a design question.

## The finding (census, 2026-09-13)

`autolens_workspace` has **41 SLaM-style scripts** carrying roughly **200 inline stage
`def`s** (`def source_lp[_1]`, `def source_pix`, `def light_lp`, `def mass_total`, …), and
**not one of them prints `model.info`** — the 6b coverage grep therefore finds nothing to
sit beside. The canonical copy is `scripts/guides/modeling/slam_start_here.py`; the rest
are variants of it under the SLaM feature/dataset folders. No SLaM script is in the smoke
allowlist, so none has CI coverage today: any change here is verified by headless runs alone.

## The decision to take before starting

1. **Inline figures.** Put `af.ModelPlotter(model).figure()` inside every stage function,
   between `model = af.Collection(...)` and `return search.fit(...)`, with the prose
   standard 6b actually SHIPPED — the canonical two paragraphs at a script's first figure
   site and a short model-fact note at later ones, with no figure-rendering vocabulary
   (pills, plates, badges, greyed, footer counts). Take it from
   `complete/2026/09/model-figures-rollout-lens.md`, NOT from the "Pattern" section of
   the 6b prompt folded into that record, which describes the map/legend reading retired
   on 2026-09-14. ~200 edit sites across 41 scripts, all verified by headless runs only (no CI
   leg will catch a regression), and every SLaM run then renders up to a dozen figures
   inline.
2. **Config flag.** Flip `model_figure: true` in `autolens_workspace/config/output.yaml`
   so every search writes `model.png` beside `model.info` in its own output folder — SLaM
   stages included, with no script edits at all. This changes the output of **every** fit
   run from the workspace, not just SLaM.

Option (ii) is also the phase-3 question left open — whether `model_figure` stays opt-in
until the acceptance renders pass — so deciding it here settles both.

Nothing is started until a human picks. Once picked, the work is mechanical: the 6b pattern
and verification recipe apply unchanged, minus the CI legs SLaM does not have.
