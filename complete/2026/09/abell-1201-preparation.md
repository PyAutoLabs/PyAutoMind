## abell-1201-preparation
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/133 (open for remaining scientific work)
- completed: 2026-09-22
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/134
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/414
- summary: Preparation phase only. Cleaned data with provenance/permission, exact processed 4 arcsec mask, power-law + shear + point-mass model, setup benchmark, separate RGB and guarded future posterior driver merged. Brain clone classification repaired. No posterior fit or scientific mass validation performed.

User invoked `$prm`, authorising these merges separately from the development-only Heart RED override. All exact-head Actions runs completed successfully: Brain Tests (Python 3.12, 3.13), assistant clone-boundary and wiki-currency (four jobs across three runs). Both PRs were CLEAN/MERGEABLE. Brain merged first at a4d67367ee787ecf9b5c829b720a142b2f4e18ad; assistant at 2865c59dbc1c2622c49f15326177b34a8cb63341. Both local heads proved ancestors of origin/main after fetching.

Local validation: 129 assistant tests, 56 clone tests, data preparation, finite coarse likelihood, freeze-check and clone boundary passed. Heart remains RED: `release validation FAILED (stage integrate)`. No release or CI bypass.

The larger science task remains active at `active/add_an_abell_1201_central_point_mass.md`: agree full-run budget, run/validate inference and calibrate the full-fit benchmark. Issue #133 intentionally stays open. Repository claims released; worktree retained for continuation and its 4.2 MB of ignored Abell plots/reports. No data deleted.
