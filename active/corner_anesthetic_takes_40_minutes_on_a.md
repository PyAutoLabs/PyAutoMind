# corner_anesthetic takes 40+ minutes on a 20-parameter model (HowToLens ch2 tutorial 2)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- HowToLens
- workspaces
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1760
Issued: 2026-11-06
Consequence: glance
Witness: `aplt.corner_anesthetic(samples=result.samples)` on the HowToLens chapter 2 tutorial 2 result (20 free parameters, 14,534 weighted Nautilus samples) completes in under 60 s on the laptop CPU.
Review-minutes: 3
Unattended: ready

Found 2026-11-06 while working on HowToLens#130 (stored tutorial results).

## Symptom
HowToLens `scripts/chapter_2_lens_modeling/tutorial_2_practicalities.py` line 453, `aplt.corner_anesthetic(samples=result.samples)`, ran for more than 44 minutes without finishing in a real (non-test-mode) run, then again for several minutes when the fit was loaded from disk ("Fit Already Completed"). It is not deadlocked: faulthandler dumps 60 s apart show progress in different frames. Line 472 (`latent=True`) follows and is likely similar.

## Stack (faulthandler, repeated)
tutorial_2_practicalities.py:453 → autofit/non_linear/plot/plot_util.py:112/121 wrapper → autofit/non_linear/plot/nest_plotters.py:140 corner_anesthetic → anesthetic/samples.py:478 plot_2d → pandas plotting core.py:773 _adorn_subplots → tools.py:422 handle_shared_axes → tools.py:336 _remove_labels_from_axis → matplotlib axis.get_minorticklabels → _update_ticks → ticker tick_values.

## Cause (hypothesis)
20 parameters → 20×20 = 400 axes from `make_2d_axes`; anesthetic's default kinds put 2D KDE contours on 190 lower panels over 14.5k weighted samples, and pandas' shared-axis label pass walks tick locators on all 400 axes. Cost scales ~quadratically with parameter count.

## Fix options
- Tutorial side: plot a parameter subset (e.g. mass model only) — anesthetic `make_2d_axes` takes the column list.
- Library side: in `corner_anesthetic`, cap the default number of parameters drawn and/or default to cheaper kinds (hist diagonal, scatter/hist_2d lower) above N parameters; thin to equal-weight samples before KDE.
- Measure where the time actually goes (KDE vs pandas label pass) before choosing.

## Notes
Affects every HowTo reader regardless of stored results (HowToLens#130 ships thin samples, which also helps, but does not fix the library default). Check other `corner_anesthetic` call sites in HowToLens ch4 tutorial 2, chapter_optional/tutorial_searches, workspaces.

<!-- formalised by the Intake (Conception) Agent on 2026-11-06 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/corner_bug.md -->
