# autocti_workspace imaging_ci/modeling/start_here.py: the slowest smoke script in the organism (61 s)

Type: test
Target: autocti_workspace
Repos:
- autocti_workspace
- PyAutoCTI
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-09-06

Split out of phase 8 (autolens_workspace#536) because it is the one script on a
different stack (PyAutoCTI + arcticpy). The ingested record (PyAutoHeart
`timings/scripts/autocti_workspace.jsonl`, run 33908175450, py3.12) puts
`imaging_ci/modeling/start_here.py` at **61.0 s** — the slowest smoke script
anywhere — with `dataset_1d/modeling/start_here.py` 17.0 s and
`dataset_1d/modeling/features/species_x3.py` 15.9 s behind it; the repo's three
gate entries total 93.9 s at a 17 s median, against a 5-7 s floor everywhere
else. The legacy digest (PyAutoHeart `timings/legacy_round_2026-09.md` §3) names
it as the one genuine per-script bottleneck on the user-facing surface.

Ask: diagnose where the 61 s goes under the smoke profile (arcticpy clocking at
full size under `PYAUTO_SMALL_DATASETS`? a real search the TEST_MODE bypass does
not reach? plot/output work the skip variables miss?), then fix it the phase-8
way — shared machinery (autonerves cap helper, profile override) first, script
content last and conservative, never the tutorial prose. CI is the acceptance;
record the before/after rows in the epic ledger.

<!-- was a member of the ci-timing-fast-tests epic (retired COMPLETE 2026-09-06, ledger complete/archive/epics/ci_timing_fast_tests_epic.md); now ordinary backlog -->
