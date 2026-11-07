# The looks-shipped guard's flags were 32 of 33 false: tighten its evidence

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: PR open — awaiting human /prm
Consequence: judge
Witness: Run against the PyAutoMind tree as it stood before PyAutoMind#545 (125caf48e), with the same organism checkouts, `intake looks-shipped` flags only `draft/maintenance/ci/wiki_currency_check_version_gate.md` (the one true positive, shipped as autocti_assistant#26), down from 33. Hermetic tests in `tests/test_intake_looks_shipped.py` reproduce each false-positive shape and the true-positive shape, and the Brain suite passes.
Review-minutes: 10
Filed: 2026-11-07
Issued: 2026-11-07
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/598

Original request (2026-11-07, after answering all 33 flags in PyAutoMind#545 and #546): "Yeah do that now filendraft and do it". This replies to the proposal to tighten the guard, for example by ignoring a draft's own filing commit and requiring the evidence to show what the Witness asks for.

## What was seen

The daily close-out guard (`agents/conductors/intake/_shipped.py`, run by PyAutoMind's `looks_shipped.yml`) flagged 33 open drafts as "looks shipped". Every flag was checked against current main of the repos it cited. One had shipped. The other 32 were false, and they fell into these shapes:

- **witness-exists, "changed by" (about 21 flags).** The Witness names a class, function or test file that already existed when the draft was filed: the class the bug lives in (`FitInterferometer`, `LensCalc`, `AnalysisInterferometer`, …) or the test file a new case would join (`test_presentation`, `test_result`, …). Any later edit to it counted as evidence.
- **witness-exists, "added by" a same-named definition (about 5).** A second `def` with the same name appeared elsewhere, for example `log_likelihood_function` in `interpolator/covariance.py` or `source_plane_mesh_grid` in a mock. That counted as the witness arriving.
- **Same-day filing commits.** Leg (i) used `--since=<Filed>T00:00`, so the commit that motivated the draft, made earlier on the filing day, counted against it (`production_standard_data`, the Sibson regression test, …).
- **commit-names-draft through a code subject (7).** A `fix(build):`/`feat:`/`docs:` commit whose body names the draft it filed as follow-up ("…; remove once the cost is found (draft/….md)") qualified because the subject was code-like, even with no ship word on the line.
- **Three-word slugs (2).** `jax_zero_contour` is a package name, and `group_los_halos` matched "group, LOS halos" in prose.
- **A campaign map (1).** `lenstwin_epic`: each shipped phase added real new classes, but the map itself never ships.

## Ask

Tighten the evidence without losing true positives, and keep every flag a fact a human can re-check:

1. Witness leg: the named thing must have had **no definition anywhere on main at the draft's filing moment** and have one now. Use the precise filing commit time, not the day.
2. Commit/PR leg: the line that names the draft must itself carry a ship word, matched as a whole word, or be the PR-merge line for the draft's branch. A code-style subject no longer lends the claim.
3. Bare slugs must be more distinctive: 4 or more words and at least 20 characters.
4. Skip `Status: campaign map` drafts.
5. Measure before and after on the real tree.
