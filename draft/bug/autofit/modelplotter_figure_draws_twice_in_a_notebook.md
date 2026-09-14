# ModelPlotter.figure() draws twice in a notebook

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
- autolens_workspace
- HowToFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a notebook cell whose only content is `af.ModelPlotter(model).figure()`, executed with nbclient, produces exactly one `image/png` output (today it produces two).
Review-minutes: 3
Unattended: ready

Reported from a HowToFit tutorial run in a Google Colab notebook: the model figure
drawn by `af.ModelPlotter` appears twice, one identical image directly below the
other.

Cause, confirmed by reading the source and reproducing it. `autofit/model_figure/render.py:save()`
does two things on the default `format="show"` path:

    if format == "show":
        plt.show()      # (1) inline backend emits the figure as `display_data`
        return figure   # (2) IPython's PNG formatter for `Figure` emits it again

`plt.show()` under the inline backend (Colab's default) publishes the figure as a
`display_data` message. `figure()` then returns the matplotlib `Figure`, and because
the tutorial cells end on that call, IPython's registered `image/png` formatter for
`Figure` renders the very same figure a second time as the cell's `execute_result`.
Reproduced with nbclient on a cell shaped exactly like the tutorial ones: two outputs,
`display_data['image/png']` and `execute_result['image/png']`.

Every cell whose last expression is a `ModelPlotter` call is affected, i.e. all the
model-figure cells the model-figures rollout added: HowToFit chapter_1 tutorials 1, 3,
4, 7 and the optional Bayesian-formalism tutorial, chapter_advanced tutorials 2, 3, 4,
5, and the equivalent cells across autofit_workspace and autolens_workspace. Scripts
run outside a notebook are unaffected (nothing echoes the return value there).

Secondary defect in the same branch: `format="show"` never calls `plt.close(figure)`,
unlike every other branch of `save()`. Under a non-inline backend the figures stay
open, so a script that draws a model per stage leaks them.

Fix: the `format="show"` path should not hand a renderable `Figure` back to the
notebook. Returning `None` there is the simplest and matches what the caller can do
with it (nothing — it has already been shown); closing the figure on that path too
fixes the leak. `ModelPlotter.figure()`'s docstring ("Returns: The matplotlib Figure")
and any caller that relies on the return value need checking first —
`autofit/non_linear/paths/directory.py:519` calls it with `format="png"`, which is
unaffected. Guard it with a regression test at the level the Witness states.

<!-- formalised by the Intake (Conception) Agent on 2026-09-14 from file:/tmp/claude-0/-home-user/04e7e446-3395-5345-aae5-0d280360eef1/scratchpad/intake_modelplotter.md -->
