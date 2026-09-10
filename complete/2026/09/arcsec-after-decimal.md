## arcsec-after-decimal
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/546
- completed: 2026-09-10
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/547
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/612
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/547
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/612
- summary:
  - `arcsec_after_decimal` is now a per-call keyword on `plot_array`, `plot_grid`
    and `plot_inversion_reconstruction`, forwarded through `apply_extent` to
    `_arcsec_labels`. `True` forces the symbol-over-decimal form (`3.″8`),
    `False` forces the suffix form (`3.8"`), `None` (the default) reads the
    `ticks.symbol_over_decimal` config flag. PyAutoGalaxy's `plot_array` wrapper
    forwards it too, which is what makes `aplt.plot_array(...,
    arcsec_after_decimal=True)` work for lens users; PyAutoLens needed no change
    because it re-exports autogalaxy's function.
  - **Most of the filed prompt had already shipped.** The formatter and the
    `ticks.symbol_over_decimal` config flag were already in `main`, with four
    tests covering all four cases the prompt asked for, and the prompt had never
    been retired to `complete/` — so it kept rendering as pickable backlog
    claiming the whole feature, and the `visualization` bundle picked it on that
    basis. Only the per-call override actually remained. `Difficulty:` was
    corrected `large` → `medium` at issue time and the prompt body carries a
    dated scope correction.
  - **Follow-up worth running: `pyauto-brain intake reconcile` across the wider
    backlog.** Nothing suggests this prompt was the only one shipped-but-not-
    retired, and the failure is invisible by construction — the dashboard renders
    such a prompt faithfully and no workflow can tell the difference.
  - Trade-off recorded: the public API name (`arcsec_after_decimal`) deliberately
    differs from the config key and internal helpers (`symbol_over_decimal`). The
    config key already shipped and is documented in `general.yaml`, so renaming it
    would break anyone who had set it. The two are bridged at each public
    function's `apply_extent` call rather than unified.
  - Gate: `pyauto-heart` is unreachable from a remote web session, so
    `ship_library`'s documented fallback (per-repo pytest) was used —
    `test_autoarray/plot` 35 passed (33 in `test_utils`, = 30 baseline + 3 new);
    PyAutoGalaxy related plot tests 22 passed. The wider `test_autoarray` run
    showed 1408 passed / 8 failed, and all 8 were proven pre-existing by
    re-running them in a detached worktree at the pristine branch point
    `35aa681f`, where they fail identically — `No module named 'numba'` in the
    container, all under `test_autoarray/inversion/`, which the diff does not
    touch. CI (which has numba) was green on every leg: PyAutoArray 3/3,
    PyAutoGalaxy 4/4.
  - Both PRs were opened directly rather than through `/ship_library`, so they did
    not carry the `pending-release` label at PR-open; it was applied during this
    close-out so the release chain is intact.
  - Bundle context: this was one of three members of the `visualization` bundle,
    and the only one that shipped. `research/autolens/quick_update_plotting_cost.md`
    was dropped (its deliverable is a measured breakdown needing a quiet box, which
    a shared container cannot be) and annotated with what a static pass found.
    `docs/workspaces/plot_coverage_followups.md` was dropped and split into four
    prompts — it was a container of four independent items that said "do not
    bulk-issue them as a series" and carried no `Type:`/`Autonomy:` header, which
    AUTONOMY.md reads as `human-required`.

## Original prompt

# Claude Development Prompt: Arcsecond Tick Label Decimal Placement

Type: feature
Target: PyAutoArray
Themes:
- visualization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: issued 2026-09-09 — PyAutoArray#546 (re-scoped; see the correction below)
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-05-14 (backfilled from git)
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/546

You are working in the PyAutoLens / PyAutoArray plotting codebase.

## Goal

Add a boolean option to the plotting API that changes arcsecond tick labels from the current format:

```text
0.45"
-2.2"
3.1"
```

to:

```text
0."45
-2."2
3."1
```

This should be implemented inside the plotting source code, not by user scripts editing Matplotlib tick labels after a figure has been drawn.

## Requirements

- Add a clearly named boolean option, for example `arcsec_after_decimal`, defaulting to `False` so existing plots are unchanged.
- The option should be available from high-level plotting functions such as `autolens.plot.plot_array(...)`.
- When enabled, only labels that are already formatted as arcseconds should change.
- Preserve all existing tick locations, precision choices, rotation, font size, and other style settings.
- Do not change colorbars or non-arcsecond axis labels.
- Add focused tests or examples covering:
  - default behavior remains `0.45"`;
  - enabled behavior becomes `0."45`;
  - negative values become `-2."2`;
  - integer-like labels without a decimal either remain unchanged or use a documented behavior.

## Suggested Implementation Direction

Find where axis tick labels are formatted in the AutoArray / PyAutoLens plotting stack. Start from:

- `autolens.plot.plot_array(...)`
- `autoarray.plot.plot_array(...)`
- the axis / tick helper functions used by `autoarray.plot.utils`
- any config-driven tick-label formatter that appends the arcsecond symbol

Implement this as close as possible to the tick-label formatter that appends `"`, rather than modifying labels after plotting. Ideally the formatter should receive the boolean and place the arcsecond marker either at the end or immediately after the decimal point.

## Acceptance Criteria

This example should work without post-processing:

```python
import autolens.plot as aplt

aplt.plot_array(
    array=array,
    title="VIS Data",
    arcsec_after_decimal=True,
)
```

and should produce axis labels like:

```text
-2."2   0."45   3."1
```

The same call without `arcsec_after_decimal=True` should preserve the current default labels.

## Notes

This request comes from paper-figure generation, where editing Matplotlib labels after `aplt.plot_array` works but creates fragile layout and whitespace side effects. The source-level option should keep normal PyAutoLens layout behavior intact.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## Scope correction 2026-09-09 — most of this already shipped

Re-read against `main` before issuing. The **formatting** half of this prompt is
already implemented and tested:

- `autoarray/plot/utils.py:1109` `_arcsec_labels` renders the double-prime over
  the decimal point (`3.″8`), driven by `ticks.symbol_over_decimal` in
  `autoarray/config/visualize/general.yaml:26` (default `false`).
- `test_autoarray/plot/test_utils.py:19-90` already covers all four of the test
  cases this prompt asks for: default `0.45"`, enabled `0."45`, negative, and
  the integer-like case (documented as a bare `3″`).

It shipped without this prompt being retired to `complete/`, so the prompt kept
rendering as pickable backlog claiming the whole feature. `Difficulty:` lowered
`large` → `medium` accordingly.

**What actually remained**, and what PyAutoArray#546 covers: the switch is
**global config only**, so the Acceptance Criteria call above —
`aplt.plot_array(array=array, arcsec_after_decimal=True)` — still does not
work. A caller wanting this for one figure has to mutate `conf.instance` and
restore it, which is the fragile stateful pattern the Notes section was filed to
remove. #546 threads a per-call `arcsec_after_decimal` override through
`plot_array` → `apply_extent` → `_arcsec_labels` in PyAutoArray, and forwards it
through PyAutoGalaxy's `plot_array` wrapper (which has an explicit keyword
signature and no `**kwargs`). PyAutoLens needs no change — it re-exports
autogalaxy's function.
