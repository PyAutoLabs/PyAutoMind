# corner_anesthetic takes 40+ minutes on a 20-parameter model

Merged 2026-11-09 in PyAutoFit#1761 (`bdb7af0e9`), issue PyAutoFit#1760.


## What shipped

A 20-parameter `corner_anesthetic` plot now takes ~25–32 s, down from 40+ min. Witness: the real HowToLens ch2 tutorial 2 model, 14,534 weighted samples, 23.6–31.9 s over five runs (target < 60 s).

- **pandas label pass:** pandas' shared-axis label pass (n⁴) now runs once after the last panel instead of after every panel. Each diagonal twin axis gets its parent's x range back afterwards, which fixes a shifted last 1D curve the review found.
- **Unlabelled samples:** samples are built without labelled columns (anesthetic copied them for every panel), and the labels are re-applied to the axes.
- **Compact style above `max_detailed_parameters` (10):** 2D histograms instead of KDE contours, and no upper triangle. A caller's `kind` / `kinds` / `upper` wins.
- **Single render:** `output_figure` saves via the figure, because `plt.savefig` re-rendered via `draw_idle`.
- **`max_parameters_search` (30):** a search skips the full corner plot above it. The log says whether per-component plots are made instead.
- **End of fit only:** weighted and chain searches make their corner plots once the fit completes (`PosteriorDefaults.plots_during_fit`). Point searches' progress plots still update during the fit. The human asked for this on 2026-11-06.

Seeded full, repeated-label, subset, latent and 12-parameter compact plots are pixel-identical to the pre-change `main`.

## Root cause

Before 2026-10-04 this plot never drew for models with two same-named components: repeated LaTeX labels made anesthetic raise `KeyError`, which `@log_plot_exception` swallowed. 9db2921aa fixed the keys and exposed the n⁴ pandas cost. The 10-28 pandas 3 upgrade is not the cause.

## Gates

- **Unit tests:** the full suite passes apart from the pre-existing Zeus conformance failure, which also fails on main.
- **Smoke:** 160/160 across the six workspaces.
- **Independent review:** FINDINGS (twin-axis shift, misleading skip log), fixed in 1607eeefe, re-review CLEAN.
- **Heart:** RED, not caused by this branch (Galaxy/Lens inversion test failures and others). The human authorized the development-only override, recorded in all four sinks.
- **CI:** Tests 3/3 green. The Docs run never started its jobs on 3 attempts ("workflow file issue"); docs-build passed in attempt 2 and generated-search-docs passes locally. The human chose to merge.

## Follow-ups

- **HowToLens#130** (howtolens-stored-results) was blocked on this. The library fix is enough; the tutorial needs no change.
- **Docs CI:** the Docs workflow's startup failures on PR events are worth a look if they recur.

## Original prompt

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
