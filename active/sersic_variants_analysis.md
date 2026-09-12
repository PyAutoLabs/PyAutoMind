# Per-variant comparison of the four Sersic scrapes (`scripts/analysis/sersic_variants.py`)

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Difficulty: easy
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: four synthetic scrapes in, per-variant fractions + paired medians + W1-W4 readings out, with the inner-join losses named
Review-minutes: 15
Filed: 2026-09-12
Issued: 2026-09-12

User request (verbatim, 2026-09-12):

"""
Do the next lot of sersics i think we can do each batch of 100 at the same time and
then we'll have the info we need to decide what to do in production
"""

This prompt is the **"info we need"** half of that request. The running half —
`--variant` for the Sersic stage and the 100-task array that produces the four
result trees — is PR #75 on issue #74 (`sersic-variants`). Nothing here touches
its files.

## Context

The `euclid_sersics` project exists to explain why the lens-light Sersic index
piles up at the prior edge `n = 5` in the June catalogue (67 % of the core 100
lenses sit above 4.5). Four variants — `baseline`, `wide_n`, `central_noise`,
`sersic_point` — are being run on the *same* 100 lenses, each writing
`sersic_lens_model_<variant>/vis`, each scraped by
`catalogue/scripts/lens_sersic.py --unique_tag sersic_lens_model_<variant>` into
its own `lens_sersic.csv`.

Four CSVs of 100 rows each are not an answer. What production needs is the
pairwise comparison: how the `n` distribution moves per variant, how each lens
moves against its own `baseline` fit, and how `baseline` compares to the June
number the pile-up was first seen in. Doing that by hand in a notebook, four
times, is how a comparison stops being reproducible.

## Deliverable

`scripts/analysis/sersic_variants.py`, plus `scripts/analysis/README.md` and
`scripts/analysis/__init__.py`:

1. **Inputs** — a directory holding the four scrapes as
   `lens_sersic_<variant>.csv`, and an optional `--lens-map sample/lens_map.csv`
   (the science clone's map: `euclid_object_id,sep1_tile,batch_zip,
   offset_arcsec,total_valid_votes,june_sersic_index`) joined on
   `sep1_tile == lens_name` for the June `n` per lens.
2. **Outputs** — a stdout table, a markdown report and a four-panel PNG under
   `--out`: per-variant N, median `n`, fractions `n > 4.5 / 4.9 / 9.5` (and
   `> 5.0` for `wide_n`, whose prior edge moved), paired `Δn` and `ΔR_eff`
   against `baseline` (median and the 16-84 % band), June-vs-`baseline` `Δn`
   when the map is given, and the four witness readings W1-W4 printed as
   **numbers beside their pre-registered thresholds** — never as a verdict word.
   Histograms share bins 0.5-10 with the 0.8 / 5.0 config limits marked.
3. **Pure functions** (`load_variants`, `summarise`, `paired_deltas`,
   `witness_table`) separated from the CLI, so the tests need no result tree.
4. **`tests/test_sersic_variants_analysis.py`** — a synthetic four-CSV fixture
   in the style of `tests/test_compare_catalogues.py`, asserting the fractions,
   the paired medians, that the lens set is an **inner** join and the dropped
   lenses are named, and that the CLI writes both the markdown and the PNG.

Not in scope: extending `catalogue/scripts/lens_sersic.py`. It scrapes the six
Sersic parameters and nothing else, so the `sersic_point` nucleus flux fraction
is not available from these CSVs and the report says so rather than inventing it.

## Verification

`pytest -q -m "not slow" tests` green; the script runs end to end on the
synthetic fixture and writes both artefacts; no PyAuto library import, so it
stays in the fast suite.
