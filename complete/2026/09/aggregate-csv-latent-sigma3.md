## aggregate-csv-latent-sigma3
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1597
- completed: 2026-09-10
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1598 (merge 68d43b0f)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1598
- summary: |
    `AggregateCSV` wrote wrong numbers for two column kinds and hid a third failure. `Row.values_at_sigma_3_kwargs`
    read `latent_summary.values_at_sigma_1`, so every latent `*_3_sigma` column carried the 1-sigma values (shipped
    into the June 2026 Euclid DR1 prelim catalogue); `Row.max_likelihood_kwargs` seeded from `median_pdf_sample`,
    so a `MaxLogLikelihood` model-parameter column was the median; `Column.value` swallowed every KeyError into
    None. Both reads fixed. An argument that resolves in neither the samples-summary nor the latent-summary
    keyspace now logs one warning per column (naming it and the first ten available arguments), and
    `AggregateCSV(aggregator, strict=True)` raises a KeyError instead (`Row.known_paths` is the union of the four
    kwargs keyspaces). The eight tautological `x == "a" or "b"` assertions in `test_aggregate_csv.py` are replaced
    with exact values; regression tests cover each defect; the fixture's max-likelihood `centre_0` now differs
    from the median so the max_lh test means something. 2511 passed serially; CI green on 3.12/3.13/nojax/docs.
- trap: |
    The new keyspace check evaluates all four kwargs dicts, and the base `Samples.summary()` (a search with no
    PDF) leaves `median_pdf_sample` and both `values_at_sigma_*` as None — the plan's version would have raised
    AttributeError where a Median-only column used to work. Caught in diff review; `Row` now treats a missing
    sample or sigma dict as an empty contribution, with a stub-result unit test.
- notes: |
    web-github session (no worktree, no gh, no Heart): PyAutoFit was attached mid-session with add_repo and the
    fix pushed on the session's `claude/` branch; pytest was the ship gate. `Autonomy: supervised` on an
    interactive launch with nobody present — ship sign-off taken and flagged in the PR body (decide-and-flag),
    merge left to the human, who typed /prm. Serial full-suite run: `-n auto` trips a pre-existing xdist
    collection mismatch in `test_prior_properties.py` (memory-address parametrize ids), unrelated.
    Release note: catalogues built with latent 3-sigma or max-likelihood columns must be regenerated once the
    release ships — `draft/bug/euclid/catalogue_latent_prefix_blank_columns.md` carries that follow-up.
    Shadow row: not applicable (`Consequence: judge`).

## Original prompt

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
Issued: 2026-09-10

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
