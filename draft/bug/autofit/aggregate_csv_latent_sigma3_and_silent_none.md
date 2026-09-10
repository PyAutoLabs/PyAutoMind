# `aggregate_csv`: latent 3-sigma bounds are the 1-sigma values, max_lh is the median, unresolvable arguments are silent

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on the `aggregate_csv` test fixture a latent's `*_lower_3_sigma` differs from `*_lower_1_sigma`, a MaxLogLikelihood model-parameter column differs from its Median column, an argument matching neither keyspace emits exactly one warning and raises under `strict=True`, and no assertion of the form `x == "a" or "b"` remains in `test_aggregate_csv.py`.
Review-minutes: 25
Unattended: ready
Filed: 2026-09-10

## Symptom

In PyAutoFit `aggregate_csv`, latent 3-sigma bounds silently carry the 1-sigma values,
max-likelihood model-parameter columns are the median, unresolvable arguments are silent, and the
tests are vacuous.

1. `autofit/aggregator/summary/aggregate_csv/row.py:102` `values_at_sigma_3_kwargs` reads
   `latent_summary.values_at_sigma_1` (since 1a62a78c7, 2025-04-09), so every latent
   `*_lower_3_sigma` / `*_upper_3_sigma` column equals its 1-sigma column: already shipped in the
   June 2026 DR1 prelim catalogue (2990/2990 `lens_mass.csv` rows, 22815/22815 `magnitudes.csv`
   rows) and reproduced on the 342398 rebuild 10/10, while the model-parameter control differs.
2. `row.py:64` `max_likelihood_kwargs` seeds from `samples_summary.median_pdf_sample.kwargs`
   instead of `max_log_likelihood_sample.kwargs`, so a MaxLogLikelihood model-parameter column is
   the median (the latent half at `row.py:68` is correct).
3. `column.py:63-96` `Column.value` returns None on KeyError for all four value types with no
   warning, so a renamed latent or a typo is indistinguishable from a missing value; this hid the
   euclid pipeline's stale `latent.` prefix from June to September.
4. `test_autofit/aggregator/summary_files/test_aggregate_csv.py` asserts `x == "a" or "b"`
   (always truthy) about eight times, and its fixture latent is named `latent.value`, which made
   the prefix look sanctioned.

## Do

1. The two one-liners (1) and (2).
2. A `logger.warning` once per column when an argument matches neither the samples-summary nor the
   latent-summary keyspace, plus an opt-in `strict=True` on `AggregateCSV` that raises.
3. Replace the tautological assertions.
4. Add regression tests that a latent's 1-sigma and 3-sigma bounds differ, that max-likelihood
   differs from the median, and that an unresolvable argument warns.

## Release note

This changes published numbers: the June DR1 prelim catalogue's latent 3-sigma columns need
regenerating.

Related: `complete/2026/09/catalogue-latent-prefix-blank.md` (the stale `latent.` prefix
this silence hid) and `draft/bug/autolens/vis_lp_mge_stage_writes_no_latents.md` (the vis_lp stage
that writes no latents at all).
