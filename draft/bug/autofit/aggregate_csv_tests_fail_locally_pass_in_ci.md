# test_aggregate_csv: five tests fail locally on main while CI is green

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- aggregator
- tests
Difficulty: small
Autonomy: supervised
Priority: low
Consequence: notify
Witness: `python -m pytest test_autofit/aggregator/summary_files/test_aggregate_csv.py -q` passes on the local WSL checkout of `main` (currently 5 failed / 2557 passed / 2 skipped for the full suite) and the cause is recorded — either the test is made order-independent or the environment difference is named.
Filed: 2026-09-10

Observed 2026-09-10 while gating a docs-only PyAutoFit branch (start-here-mode,
autofit_assistant#38): the full suite in a fresh task worktree branched from
`0280983a8` gives `5 failed, 2557 passed, 2 skipped`, all five in
@PyAutoFit/test_autofit/aggregator/summary_files/test_aggregate_csv.py:

- `test_add_column`, `test_use_max_log_likelihood`, `test_add_named_column`,
  `test_add_latent_column`, `test_max_log_likelihood_differs_from_median`

`test_add_column` fails with `assert '-5.0' == '-1.0'` on
`dicts[0]["galaxies_lens_bulge_centre_centre_0"]` — the aggregator finds
"2 search_outputs" and the first row is the other search. The same test fails
identically on the canonical `PyAutoFit` checkout of `main`; the GitHub
`Tests` workflow on the same SHA is green. No untracked/ignored residue in
`test_autofit/aggregator/` (only `__pycache__`). Hypothesis (unverified): the
row order of the aggregated searches depends on directory-listing order, which
differs between the WSL filesystem and the CI runner; the test should sort or
key rows by search name rather than index into `dicts[0]`.
