# Audit HowTo tutorials for missing setup_notebook() line

Type: bug
Target: HowToFit
Repos:
- @HowToFit
- @HowToGalaxy
- @HowToLens
- @autofit_workspace
- @autogalaxy_workspace
- @autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Discovered during the batch-2b markdown rollout ([[markdown-example-renderings]]).
Several HowTo tutorials are missing the standard
`# from autoconf import setup_notebook; setup_notebook()` line that every other
workspace/tutorial script carries (it chdir's to the workspace root + enables
inline plotting). Without it, a tutorial that loads data via a relative path
(or runs a simulator subprocess) FAILS when executed by nbconvert (which runs
with CWD = the notebook's own directory), and only works interactively if the
user happens to launch jupyter from the repo root.

Confirmed missing in chapter_1_introduction alone: HowToFit start_here.py +
tutorial_1_models.py; HowToGalaxy tutorial_4_methods.py; (HowToGalaxy
tutorial_3_fitting.py + HowToLens tutorial_7_fitting.py were fixed in batch 2b's
PRs since they blocked rendering). The 3 still-missing pass today only because
they don't load data by relative path.

Fix: audit ALL chapters of all three HowTo repos (and re-check the workspaces)
for scripts lacking the setup_notebook line; add it right after the opening
docstring, matching the sibling convention; regenerate the affected notebooks.
Low-risk boilerplate consistency fix.

## Audit result (2026-08-18)

Every `.py` under `scripts/` — plus each HowTo repo's root `start_here.py` — was checked in the
three HowTo repos and all five user-facing workspaces. 39 scripts were missing the line:

| Repo | Missing | Notes |
|---|---|---|
| HowToFit | 3 | `chapter_1_introduction/{start_here,tutorial_1_models}.py`, root `start_here.py` |
| HowToGalaxy | 2 | `chapter_2_modeling/tutorial_8_need_for_speed.py`, root `start_here.py` |
| HowToLens | 6 | `chapter_2_lens_modeling/{tutorial_8_need_for_speed,tutorial_11_slam}.py`, `chapter_3_pixelizations/tutorial_9_model_fit.py`, `simulator/{lens_x2,lens_x3}.py`, root `start_here.py` |
| autofit_workspace | 1 | `overview/overview_3_statistical_methods.py` |
| autogalaxy_workspace | 5 | under `guides/`, `imaging/data_preparation/`, `interferometer/` |
| autolens_workspace | 22 | mostly `cluster/*`, `guides/*` and feature `simulator.py` scripts |
| autocti_workspace | 0 | clean |

`tutorial_4_methods.py` in HowToGalaxy, named in the original report, already carries the line —
it was fixed before this audit ran.

The omissions are not a deliberate per-subtree policy: they sit alongside siblings in the same
directory that do carry the line (e.g. `autolens_workspace/scripts/cluster/` has 6 without and 5
with).

The two genuinely load-bearing cases are `HowToLens/scripts/simulator/lens_x{2,3}.py`, which write
to a relative `dataset/` path; the rest are prose-only or import-only scripts that pass today for
the reason the report gives.

**Out of scope, deliberately:** `autoreduce_workspace` has 30 scripts and none carry the line, but
it has no `notebooks/` directory — the convention does not apply there yet. Same for every
`*_workspace_test` and `*_workspace_developer` repo (checked by tree listing; none generates
notebooks).

**Placement:** after the module docstring, or after the `from auto* import jax_wrapper` line where
a script has one. One outlier — `autolens_workspace/scripts/guides/units/mass_to_light_ratio_units.py`
opens on imports rather than a docstring, so the line went at the top of the file.

**Notebooks:** patched by hand to the exact shape PyAutoHands emits (uncommented, same cell,
`json.dumps(nb, indent=1)` round-trips byte-identically), because the generator is not available in
a cloud session. A real `generate.py` run should be a no-op on these — confirm before merging.

Branch `claude/howto-setup-notebook-audit-dm2j9e` in all six repos. Not merged, no PRs opened.
