## cti-database-examples-drift
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/121
- completed: 2026-11-05
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/122
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/42

Merged 2026-11-05 by glance-tier auto-merge (plan approved by the human): PyAutoCTI#122 (804ddebd), then autocti_workspace#42. Issue #121 closed. cti-upkeep phase 3.

Library:
- `CTIAgg` (`aggregator/cti.py::_cti_from`) returns a list with one CTI per dataset for FactorGraphModel fits, and a single CTI otherwise. This is a human-approved API decision.
- Second bug found in the same function: `object_via_gen_from` ignored its `instance`, so PDF draws and above-weight samples all returned the max-likelihood CTI. The existing all_above_weight test asserted 10.0 for both samples, which was only true because of the bug; it now expects 1.0, 10.0.
- `_cti_list_from` is shared from `aggregator/abstract.py`.

Workspace:
- database/examples/samples.py and models.py handle the per-dataset entries.
- The `with_paths` example is switched off (human decision) pending the PyAutoFit bug `draft/bug/autofit/samples_with_paths_shared_prior_factor_graph.md`.
- results/examples/samples.py returns errors with `as_instance=False`; as an instance they broke the ordered-timescale assertion under a real sampler.
- 3 scripts joined `smoke_tests.txt`.

Evidence:
- 2 new tests, both failing on main.
- `test_autocti` 279 passed (serial).
- All 9 dataset_1d results/database scripts pass.
- Smoke 6/6 under profile_smoke and profile_release, and in CI on 3.12 and 3.13.
- Independent review (separate model): FINDINGS, LOW only. Docstrings fixed (95997885); smoke-adding models.py declined (unit test covers it, rubric counts smoke growth as a defect); issue link declined.

PyAutoCTI#122 carries the GitHub `pending-release` label.

## Original prompt

# autocti_workspace: the dataset_1d results/database example scripts have drifted

Type: bug
Target: autocti_workspace
Repos:
- autocti
- autocti_workspace
Themes:
- cti
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `scripts/dataset_1d/advanced/database/examples/samples.py` and `scripts/dataset_1d/results/examples/samples.py` run end-to-end against the installed autocti (FactorGraphModel instance structure, live plot API), and a minimal smoke workflow runs them in CI.
Review-minutes: 3
Unattended: ready
Epic: cti-upkeep
Phase: 3
Issued: 2026-11-05
Filed: 2026-08-19 (backfilled from git)

<!-- re-homed from draft/triage/ to draft/bug/autocti_workspace/ at the witness-campaign close-out, 2026-09-17: two concrete sites, a bug not a triage -->
<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from user-intake -->
