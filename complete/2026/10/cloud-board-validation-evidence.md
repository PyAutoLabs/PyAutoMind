# Cloud board validation evidence

Merged https://github.com/PyAutoLabs/PyAutoHeart/pull/264 at 0bff26a3b391dccf70ae969ab590478d2995f881 on 2026-10-01. Closes https://github.com/PyAutoLabs/PyAutoHeart/issues/263.

The daily cloud board now reads smoke results and collects matching rehearsal/integration artifacts through the canonical validator. The collector preserves producer timestamps, run identity, attempt and SHA, adverse conclusions and incomplete evidence. No readiness thresholds, weights, skips or local tick behavior changed.

Validation: 1139 full-suite tests passed; 40 focused tests passed after the last two edge cases. Tenant firewall and whitespace checks passed. Real artifact collection in isolated state yielded GREEN/100 without changing live state. Every exact-head GitHub run was checked: Heart Tests 36917011559 succeeded on both Python 3.12 and 3.13. Human prm authorized merge and closeout.

Implementation is merged. Cloud-board deployment verification is a separate action, not claimed here. No package release dependency. Artifacts and logs remain in the session .heart-evidence directory outside the task bundle. The task bundle contains only clean tracked work plus reproducible pytest/Python caches, so normal cleanup is safe.

## Original prompt

# Ingest authoritative validation evidence into the cloud Heart board
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/263
Issued: 2026-10-01
Type: bug
Difficulty: medium
Autonomy: human-required

## Original request
> do it

This accepts the preceding next step: route the published-board evidence-propagation discrepancy through the bug workflow and plan artifact ingestion for the cloud board.

## Evidence
@PyAutoHeart local readiness is GREEN/100 after rehearsal 36895121274 (2026.10.1.1.dev79601), integration 36899858987 (719 pass, 82 skip, zero failures/timeouts, install A-F pass), and smoke 36909756099 (1405 pass,122 skip). Published board.json remains STALE/65 at 2026-10-01T15:31:24Z with three evidence gaps.
The heart-health workflow runs CI/performance checks but neither test_run nor release_run. publish exports local sections, not authoritative release/install sidecars. release_run consumes integration-only evidence and correctly leaves validation incomplete without the rehearsal. validate currently dates an ingest at now; cloud repeated ingestion must not refresh evidence age.

## Scope and proposed plan
Single owner: PyAutoHeart infrastructure. No thresholds, weights, skip policies or release gate changes. No source, publication or deployment before plan approval.
1. Wire the existing smoke reader into cloud health before aggregation, retaining measured artifact counts and adverse-run semantics.
2. Add bounded read-only collection of matching rehearsal and integration artifacts. Resolve the rehearsal producer from configured body-map identity, never a hard-coded tenant or synthesized run ID. Require exact version agreement, successful producer evidence, release profile and complete source SHAs; preserve installation evidence through validate. Prefer explicit provenance linkage where available. Missing/expired/mismatched artifacts stay incomplete; latest failed runs remain failures and must not fall back to an older pass.
3. Use producer evidence timestamps for freshness on every fresh cloud environment; do not re-date old success. Preserve existing local-fresher and adverse-evidence behavior. Feed the canonical validator/readiness functions, not a second verdict implementation.
4. Add regression coverage for complete matched evidence, absent rehearsal, version mismatch, unsuccessful/cancelled/pending producers, expired artifacts, source movement, missing SHAs, freshness and repeated ingestion, and workflow ordering. Run targeted tests followed by the Heart suite.
5. Validate a cloud-equivalent isolated state directory against recorded artifacts and compare its authoritative readiness with the local reference. Ship a reviewable PR; merge/publication are later explicit steps.

## Branch survey
Canonical Heart: clean main; no active PyAutoHeart claim. Canonical Mind belongs to another session and is preserved. Planning ledger uses isolated codex/cloud-board-validation-evidence. Proposed source branch feature/cloud-board-validation-evidence from current origin/main.

## Candidate files
.github/workflows/heart-health.yml; heart/checks/release_run.py (or a focused artifact-collection helper); heart/validate.py only if required for evidence timestamp preservation; relevant release-run, validator and workflow wiring tests; docs/internals.md for the evidence path.
