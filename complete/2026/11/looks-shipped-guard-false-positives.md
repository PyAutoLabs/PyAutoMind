# looks-shipped guard flags only real evidence (33 → 1)

Completed: 2026-11-07
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/598
PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/599
Merge: 6d2caced343dc0c7e5f3106ba8807ce9d4026644

The `intake looks-shipped` close-out guard (`agents/conductors/intake/_shipped.py`) now needs evidence that a draft's work arrived, not just that something it names was touched:

- **Witness leg:** a name in the Witness counts only if it had no definition anywhere on main at the draft's filing moment (`defined_at` / `added_since`, which replace `changed_since`).
- **Filing moment:** `filed_at()` is the add commit on the `Filed:` day, read without `--follow`, because rename detection follows a sibling draft's history.
- **Commit/PR leg:** the naming line needs a whole-word ship word (`_SHIP_RE`), or must be the PR-merge line for the draft's branch. A code-style subject no longer lends the claim, and `add` is no longer a ship word.
- **Slugs:** bare slugs need 4+ words and 20+ characters.
- **Campaign maps:** `Status: campaign map` drafts are skipped.

Witness: on PyAutoMind `125caf48e` (before PyAutoMind#545) with the same 21 organism checkouts, flags went from 33 to 1. The remaining one is the true positive, `wiki_currency_check_version_gate` (autocti_assistant#26). A second hermetic fixture in `tests/test_intake_looks_shipped.py` pins each false-positive shape and the true positive.

Validation: Brain Tests passed on 3.12 and 3.13 at `441b452`. The first CI run failed the tenant-firewall step because a fixture merge line used the real org name; that was fixed before merge. The skill line-count step reports over-budget skills, but it is report-only and the overage predates this PR. Full suite: 1643 passed, 1 skipped.

Known trade-offs: a fix that lands the same day but *before* its draft is filed is not flagged, and "adds X (draft path)" without a ship word no longer counts.

Human `/prm` authorized the merge. Every claimed branch is contained in origin/main, and the issue is closed. There are no release obligations (PyAutoBrain is not in the published set).

## Original prompt

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
