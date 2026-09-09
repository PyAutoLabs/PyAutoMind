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
