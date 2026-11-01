## cloud-validation-rehearsal-clock-skew
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/321
- completed: 2026-11-01
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/322
- Found in a `/health` dashboard review. The board was STALE ("release validation incomplete: no rehearsal for current source") although integrate 41291876649 passed for v2026.11.1.1.dev85301. Cause: GitHub reported PyAutoHands rehearsal run 41290559836's `created_at` (09:50:55Z) an hour after its own `updated_at` (09:09:27Z) on US DST-end day, and `collect()`'s `created > integrate start` prefilter dropped it.
- Fix: `_effective_created(run)` = min(created_at, updated_at); used for the prefilter and for the report timestamp. Identity checks and `matching_rehearsal`'s `produced <= start` guard unchanged.
- Trap: GitHub run and job `started_at`/`created_at` can be skewed relative to `updated_at`/`completed_at`; order runs by completion stamps.
- The live verdict clears only once a Heart Health tick re-collects. This merge does not itself refresh the board.

## Original prompt

# Cloud validation discards a matching rehearsal when GitHub reports a skewed run `created_at`

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Themes:
- release-validation
- heart
Difficulty: easy
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-01
Consequence: glance
Witness: a `heart/checks/cloud_validation.collect()` test with injected `fetch`/`get_artifact` reproduces run 41290559836's timestamps (`created_at` 09:50:55Z, `updated_at` 09:09:27Z) against an integrate starting 09:09:36Z: it matches the rehearsal (`rehearsal_matched: true`) and the report is not stamped later than the integrate start; a rehearsal whose jobs genuinely completed after the integrate started is still rejected.
Review-minutes: 10

Source: `/health` dashboard review, 2026-11-01 (claude.ai/code session).

## Why

On 2026-11-01 (US DST-end day) the published board went STALE with
"release validation incomplete: no rehearsal for current source", and
`validation_report:coverage` read "incomplete — no rehearsal evidence —
v2026.11.1.1.dev85301", although the nightly chain had produced a valid pair:

- PyAutoHands `release.yml` run 41290559836 (rehearsal, run 853 →
  `v2026.11.1.1.dev85301`): API reports `created_at` / `run_started_at`
  2026-11-01T09:50:55Z but `updated_at` 09:09:27Z. Its jobs report
  `started_at` 09:51:10Z and `completed_at` 09:00:08–09:09:20Z — every
  start stamp is one hour late; the run really finished at 09:09:27Z.
- PyAutoHeart Release Integrate 41291876649 started 09:09:36Z and passed.

`collect()` prefilters candidates with `created > observed → continue`, so
the skewed `created_at` (09:50:55 > 09:09:36) discarded the rehearsal before
`matching_rehearsal()` (version, run_id, run_attempt, build_sha,
`produced <= start`) was ever consulted. The release verdict stayed STALE for a
genuinely validated source. Re-running the chain clears it only by luck of
timestamps; the gate should not depend on GitHub's start stamps being sane.

Re-read the API timestamps of runs 41290559836 and 41291876649 before acting —
GitHub may have corrected them.

## What

- Order candidates by when the producer *finished*, not by `created_at`: the
  existing `produced = updated_at <= integration start` check in
  `matching_rehearsal()` is the real ordering guard. Treat a run whose
  `created_at` is later than its `updated_at` as clock-skewed (use the earlier
  of the two, or drop the `created > observed` prefilter and rely on
  `produced <= start`).
- Do not let `observed = min(observed, created)` stamp the report from a skewed
  `created_at`.
- Keep every identity check (version, mode, index, run_id, run_attempt,
  build_sha, completed status) unchanged; never accept a rehearsal that really
  completed after the integrate started.
- Regression tests via `collect()`'s injectable `fetch` / `get_artifact`.

Never clear the verdict by editing evidence or thresholds; the fix is to the
collector's time ordering only.
