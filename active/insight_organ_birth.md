# PyAutoInsight: inference campaigns and evidence organ

Type: feature
Target: @PyAutoInsight
Repos:
- PyAutoInsight
- autolens_inference
- PyAutoMind
- PyAutoBrain
Consequence: judge
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-10-04
Issued: 2026-10-04
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/1

## Human request

"Build the inference organ end to end, following everything we implemented for PyAutoPulse on 2–3 October 2026, including its latest campaign control room and task migration. This is an implementation request, not just a scoping exercise."

"The outcome should be one dashboard and one ongoing chat through which I can manage all inference campaigns, see updates, direct individual campaigns and suggest ideas."

Name chosen: PyAutoInsight, organ key insight. User created public repository.
Current Heart override: "I authorize on red and repo made, continue" (2026-10-04).

## Delivery contract

Follow Insight#1. Preserve Pulse's current control-room design/order: editable
copyable all-campaign prompt; active campaign table; open tasks; evidence below.
Project-owned inference-summary@1 exporter reads actual results including failed,
stopped, incomplete, archived and diagnostic-missing runs, with exact provenance,
parent/stage identity and separately defined timing clocks. Never sum overlapping
stages or infer scientific success from process completion. Raw samples remain
project-owned and availability unknown unless verified.

Insight owns registry resolved through Mind identities, schema reader, one-commit
ingest receipts, last-good snapshots, campaign/task intent and durable check-ins.
Cortex owns science runs/observations/human conclusions. Mind retains bounded PR
lifecycle and claims. No new inference conductor or retired programme evidence.

Audit all pending Mind sources; migration preserves bytes/hashes/source commit,
priorities/decisions/blockers/issues and duplicate scheduling removal. Destination
must merge before Mind source removal. Regenerate canonical body maps/adapters,
Brain cockpit, public hub/org lists. Include producer dispatch sender and verify
published receipt against successful publication revision. Full CI, tests, review
and required authorisations before merge. No compute or release authorised.

## Validation / resumability

Implementation in feature/insight-producer, feature/insight-control-room and
feature/insight-integration across affected repos. Missing scientific local deps
must be covered by exact-head full CI, never a fabricated local pass.

## Exact published Heart RED reason set acknowledged at entry

```text
release validation FAILED (stage integrate)
PyAutoHeart/workflows/Release Integrate: failure
PyAutoArray/Tests: red
PyAutoArray/Tests: red
PyAutoFit/Tests: red
autofit_workspace_test/Smoke Tests: red
autogalaxy_workspace_test/Smoke Tests: red
autolens_workspace_test/Smoke Tests: red
CI wall-clock: 26 gates · slowest PyAutoBrain Nightly Release 83m · 1 slowed · 6 hang events
Release readiness: release validation FAILED (stage integrate)
PyAutoCTI/test_autocti/extract/two_d/parallel/test_parallel_fpr.py::test__estimate_capture: red
PyAutoNerves/test_autonerves/test_fitsable.py::test__output_to_fits: red
Unit-test timing: 3 test regressions (>3× baseline), 1 slow (>1.5×)
autolens_test: red
Release validation: NOT release_ready — v2026.10.3.1.dev79901 profile=release (2026-10-03T07:43:31+00:00)
validation_report/stages/integrate: fail
autolens_assistant: red
autolens_profiling: red
autolens_workspace_test: red
Worktree drift: 0 orphan / 0 missing / 4 dirty
euclid_strong_lens_modeling_pipeline: red
```

## Shipping checkpoint — 2026-10-04

- Organ: https://github.com/PyAutoLabs/PyAutoInsight/pull/2; 77 tests,
  lint and hosted Dashboard Refresh pass. No check-in stamped by refresh.
- Producer: https://github.com/PyAutoLabs/autolens_inference/pull/18;
  full hosted lint workflow passes, including scientific simulator/SLaM smoke.
- Registration: https://github.com/PyAutoLabs/PyAutoMind/pull/471.
- Integration: Brain #460, hub #28, .github #31, Scientist #41,
  Cortex #56, Pulse #8, Memory #114, Eyes #15, Ears #8,
  Heart #273, Hands #296, Nerves #183, Gut #20.
  All triggered integration PR workflows passed at their published heads.
- Destination contains eight campaigns and six frozen source task records;
  Mind source originals remain until the destination is merged.
- Captured producer evidence: feature/insight-producer commit
  9c362a7a298238d766f61e812c694813e94830d1 (56 records, 15 parent runs).
  This is explicitly branch evidence, not a verified main publication.
- Remaining gated sequence: explicit human merge command under AUTONOMY.md
  RED development override; merge destination/registration/integrations and
  producer; hash-checked Mind source cleanup and generated ledger round-trip;
  verify actual producer publication dispatch, expected receipt revision and
  published GitHub Pages; then lifecycle close-out. No merge or deployment
  verification has been claimed. Browser visual check remains outstanding;
  editable-copy native/fallback behavior is covered by executable Node tests.
