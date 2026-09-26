## modelplotter-figure-draws-twice
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1622 (closed completed 2026-09-14)
- completed: 2026-09-14
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1623 (merged `6fd754bc691b94f95a2d02db55173315f73d0f11`)
- session: web-github (claude.ai/code), session clone at `/home/user/pyautofit`, no task worktree; branch `claude/howtofit-modelplotter-duplicate-eqr6gk`. Reported by the human from a HowToFit tutorial run in Google Colab, then intake → start_dev → ship_library → prm in the one session.
- summary: |
    `af.ModelPlotter(model).figure()` drew every model **twice** in a notebook.
    `model_figure/render.py:save()` did two displaying things on its default
    `format="show"` path: it called `plt.show()`, which the inline backend
    publishes as a `display_data` PNG, and then *returned* the `Figure` — which
    IPython's registered `image/png` formatter renders a second time as the
    cell's `execute_result`, because every tutorial cell ends on that call.

    The show path now shows, closes and returns `None`. That is not a new
    convention: `autofit/non_linear/plot/plot_util.py:output_figure`, which
    `save()`'s own docstring says it mirrors, returns nothing and always closes.
    Returning the `Figure` was the deviation, and the missing `plt.close` was a
    second, quieter defect in the same branch — under a non-inline backend a
    shown figure was never closed, so a script drawing a model per stage leaked
    them.

    `EPPlotter` imports the same `save`, so it was fixed and guarded in the same
    change. Every other format (`png`/`svg`/`pdf`/`None`) still returns the
    `Figure`, leaving the one in-tree caller — `non_linear/paths/directory.py`,
    `format="png"` — untouched.

    **Behavioural API change:** `ModelPlotter.figure()` and `EPPlotter.figure()`
    return `None` when `format="show"` (the default) instead of the `Figure`.
    No migration: across HowToFit, autofit_workspace and autolens_workspace all
    153 `ModelPlotter`/`EPPlotter` call sites are bare statements and not one
    binds the return value, so the workspaces needed no change — this was a
    library-only fix for a bug that looked like a workspace one.
- traps: |
    **The test suite pinned the bug.** `test_show_returns_a_figure_and_writes_nothing`
    asserted `figure is not None` on the show path, so the defect was not an
    oversight the tests would have caught — it was the contract they enforced.
    Fixing it meant rewriting that test, and the rewrite
    (`test_show_returns_nothing_so_a_notebook_draws_it_once`) carries the
    *reason* in its name and docstring so it is not "corrected" back.

    **Don't assert `plt.get_fignums() == []`.** The first version of both new
    tests did, and both failed: other tests in the same process leave figures
    open (the `format=None` acceptances hand the figure to the caller by
    design). Compare against the set of figure numbers open *before* the call
    instead — the claim is "this call left nothing behind", not "the process has
    no figures".

    **`pytest -n auto` is broken in this repo**, unrelated to this task:
    `test_autofit/mapper/prior/test_prior_properties.py` parametrises over
    objects whose ids embed `repr` memory addresses, so xdist workers collect
    different test ids and error with "Different tests were collected between
    gw0 and gw2". Run the suite serially (~105s) or that is what you get. Worth
    an `ids=` fix on that parametrize one day.
- notes: |
    **The witness was checked for real, twice.** The prompt's witness — "a
    notebook cell whose only content is `af.ModelPlotter(model).figure()`
    produces exactly one `image/png` output" — was run with `nbclient` against
    the unpatched and the patched library: 2 outputs (`display_data` +
    `execute_result`) before, 1 (`display_data`) after. It is deliberately not
    in the suite: executing a real kernel per assertion is a slow test for a
    branch the unit tests pin exactly. The two committed regression tests were
    each verified failing on the unpatched tree.

    **Diagnosis order that worked**, for the next notebook-rendering bug: read
    the plotter's `save`/output helper first (the double-display is nearly
    always show-plus-return), then reproduce with `nbclient` rather than
    reasoning about IPython's formatter registration from memory — executing a
    two-cell notebook and counting `image/png` outputs took one command and
    settled it.

    Heart was not available in this session (PyAutoHeart is not one of the four
    organs a web session holds), so per the ship-gate fallback the per-repo
    suite stood in for the readiness verdict: `pytest test_autofit/ -x`,
    2796 passed / 45 skipped. CI then went 4/4 green on `be80052`
    (`unittest` 3.12, 3.13, nojax; `docs-build`).

## Original prompt

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
Issued: 2026-09-14

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
