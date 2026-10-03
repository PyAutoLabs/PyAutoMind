# Assistant feedback distribution

Completed 2026-10-03 under explicit human "Merge and continue" authorization.

Merged PyAutoBrain#458 (f00437d), autolens_assistant#149 (1098c8a),
autofit_assistant#53 (a52bdba), autogalaxy_assistant#32 (a3973a5),
autocti_assistant#34 (6db8840). All nine CI jobs passed on the exact heads;
all five published heads verified ancestors of main. Issue autolens_assistant#148 closed.

Canonical standalone feedback generator and clone-sync classification now ship
with Brain. All four assistants expose their own Claude/Codex discovery adapters
and embedded portable report template/invitation. User reviews and submits;
no telemetry, private-history retrieval, automatic posting or science-code change.

Validation: 1168 Brain tests, 67 focused tests after boundary correction,
four discovery/generation checks, two synthetic drafting checks. CI caught a
hard-coded reference in a new test; corrected to cover every configured
reference, then all tests and tenant firewall passed in both Python CI legs.

Whole-programme Heart RED development override remains; merge authorized
separately this turn, no release. Standalone local clones retained. Phase 5
follow-through remains separate work; no source release obligation created.

## Original prompt

# Distribute portable feedback to assistants

Type: feature
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Epic: community-organ-birth
Filed: 2026-10-03
Issued: 2026-10-03
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/148

Original request: "OK do thr next stuff" followed by "@GitHub".
Continue accepted programme phase4 after Ears listening reliability merged.

Ship /feedback in @autolens_assistant through its real flat-skill/discovery
mechanism, and propagate generic content to @autofit_assistant,
@autogalaxy_assistant and @autocti_assistant using @PyAutoBrain clone sync.
Keep Brain's existing report template/invitation canonical: generate one
standalone flat skill embedding those resources with correct local anchors.
Classify generic feedback paths in the template boundary; regenerate each
assistant's own Claude/Codex adapters. Verify actual standalone discovery and
no dependence on a Brain checkout during use. No telemetry, automatic posting,
private-history search or new category. Human reviews and submits to Discussions.

Test deterministic generation, generic partition/sync, adapter links and a
synthetic quick/retrospective drafting scenario. Preserve domain-specific
content and existing safety/session-start instructions. Tier judge: source PRs
await human /prm. Whole-programme development authorization continues; no release.


## PR handoff
- PyAutoBrain: https://github.com/PyAutoLabs/PyAutoBrain/pull/458 — 88a74af965565a5d7ae85f1b29a8642fd9d18268
- autolens_assistant: https://github.com/PyAutoLabs/autolens_assistant/pull/149 — 27b56371b48c30e701fbc81c0eb08bd3e80700d6
- autofit_assistant: https://github.com/PyAutoLabs/autofit_assistant/pull/53 — 6567be938666f64d06cf52b9b1fa9aa0b817c47b
- autogalaxy_assistant: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/32 — ea0ff9ca905282c5832a5bfc9e7a989ca23d7617
- autocti_assistant: https://github.com/PyAutoLabs/autocti_assistant/pull/34 — 4870e1f9a4ca5ae862175bf725d9c3fc7f5686d6

Validation: 1,168 Brain tests passed; 67 focused tests passed after the final boundary correction; all four assistant discovery and canonical-generation checks passed. Both synthetic drafting checks passed. The existing bundled autofit Gaussian/Colab examples needed explicit domain classification to complete its boundary; no example code changed. Source PRs await human /prm, Brain first; task remains open.

Recorded Heart RED reasons (development authorization only):
```
  [red] release validation FAILED (stage integrate)
  [red] PyAutoHeart/workflows/Release Integrate: failure
  [red] PyAutoArray/Tests: red
  [red] PyAutoArray/Tests: red
  [red] PyAutoFit/Tests: red
  [red] autofit_workspace_test/Smoke Tests: red
  [red] autogalaxy_workspace_test/Smoke Tests: red
  [red] autolens_workspace_test/Smoke Tests: red
  [red] CI wall-clock: 26 gates · slowest PyAutoBrain Nightly Release 83m · 1 slowed · 6 hang events
  [red] Release readiness: release validation FAILED (stage integrate)
  [red] PyAutoCTI/test_autocti/extract/two_d/parallel/test_parallel_fpr.py::test__estimate_capture: red
  [red] PyAutoNerves/test_autonerves/test_fitsable.py::test__output_to_fits: red
  [red] Unit-test timing: 3 test regressions (>3× baseline), 1 slow (>1.5×)
  [red] autolens_test: red
  [red] Release validation: NOT release_ready — v2026.10.3.1.dev79901 profile=release (2026-10-03T07:43:31+00:00)
  [red] validation_report/stages/integrate: fail
  [red] autolens_assistant: red
  [red] autolens_profiling: red
  [red] autolens_workspace_test: red
  [red] Worktree drift: 0 orphan / 0 missing / 4 dirty
  [red] euclid_strong_lens_modeling_pipeline: red
```

CI follow-up: tenant-firewall reference-name finding corrected by testing every configured reference; three feedback tests and tenant firewall pass locally. Brain CI rerun pending; assistant checks green.
