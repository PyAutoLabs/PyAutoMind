# Heart Health rerun cannot publish after main advances

Type: bug
Target: PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-10-25

## Evidence and reproduction

Authorized health refresh reran the cloud collector job of run 40181167884. Attempt 2, job 121239368620, collected current data, rendered the board and passed cockpit schema validation, then failed Commit the README block + today's timing record at 2026-10-25T17:30:22Z: main -> main rejected (fetch first). Pages job 121239552700 skipped. The old run checks out its historical SHA; main already contains the first attempt's generated commit. No fresh board was published; latest observed board remains 2026-10-25T09:34:29.845384+00:00 (342 findings, incomplete RED).

## Recovery and repair scope

Immediate recovery: dispatch a NEW Heart Health workflow on current main; do not retry the stale run or force-push. The connector exposes job reruns but not new workflow dispatch; browser fallback is signed out. No new workflow dispatched from this session.

Investigate a tested, non-destructive writeback policy for stale re-runs and main advances. Preserve current-main source and append-only timing records, including deduplication and conflict handling. Never force-push, overwrite another writer, lower scores, or silently publish invalid evidence. Add a regression witness using a bare remote advanced after checkout. Check current claims and use start-dev before implementation. Do not repurpose release workflows as health collectors.

## Separate release-validation limitation

Brain release validate --ref main --json stopped at local preflight: PyAutoNerves session clone still on feature/colab-finufft-bootstrap with two uncommitted files, plus unknown library CI. The fix is already merged upstream; this is a local clone-state blocker, not evidence the fix failed. Preserve that patch, use verified clean current-main source and authoritative CI, then follow release conductor TestPyPI rehearsal/integration with explicit rehearsal mode and matching candidate commit SHAs. Do not rerun old install evidence against old wheels or publish PyPI. No rehearsal was dispatched.
