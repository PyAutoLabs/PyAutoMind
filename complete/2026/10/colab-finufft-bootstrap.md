# Colab finufft bootstrap — source merged

- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/204
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/205
- merged: 2026-10-25, ec8b5c1e5f17ac03ac5246b5fbc322624a6cd3f6
- authorization: Human “I approve” for corrective PR, then “Prm I authorize” for merge and close-out.
- corrective-red: install verification FAILED (testpypi; checks F)
- authorization-record: https://github.com/PyAutoLabs/PyAutoNerves/issues/204#issuecomment-6399922959

## Delivered

Array-based Colab project stacks explicitly install finufft>=2.4.0 with --no-deps. Fit-only stacks are unchanged. Six parametrized command tests cover all supported projects. No API signatures or notebook call sites change.

## Verification

Before source correction the new witness failed for four Array projects and passed for the two Fit projects. Patched Nerves suite: 258 passed, one existing sibling-dependent skip. Existing Array CPU NUFFT parity: seven passed. Both head workflow runs completed successfully; all four jobs passed (Python 3.12, Python 3.13, no-JAX, Colab gate). PR head 90bd238356203233ab766976306865999a247ad6 is an ancestor of main. Source merged unchanged; issue closed as completed.

## Remaining release evidence

Source completion is not release readiness. The pending-release obligation above remains. Fresh candidate wheels and install/integration validation must reconcile verify_install:F:, release:a13bfd6326c80cc0 and release:151bc7341455ff32 plus linked coverage/validation IDs. Published Heart RED is not cleared by this merge. No release or rehearsal performed. No authoritative dev-box freeze flag was available on this surface.

## Cleanup

This task used a session clone, not a managed task worktree. Recoverable session files are retained; no canonical checkout, ignored data or unrelated work was removed.

## Original prompt

# Install finufft in Array-based Colab bootstraps

Type: bug
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: easy
Autonomy: supervised
Consequence: judge
Priority: high
Status: formalised
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/204
Issued: 2026-10-25

@PyAutoNerves

## Original request

Human follow-up, 2026-10-25: "Yep do all that"

This approves the health-review worklist, including investigation and repair of
the release blocker `verify_install:F`. Publication, merges and destructive
cleanup remain separately gated.

## Evidence and diagnosis

Heart board timestamp 2026-10-25T09:34:29.845384+00:00 reports the exact RED reason:
`install verification FAILED (testpypi; checks F)`.
Release Integrate run 40173226809, job 121108376734 reports:
`finufft (declared by autoarray, absent on Colab, imported)`.

AutoArray added finufft as its CPU NUFFT dependency in #655. Nerves installs
Colab packages using --no-deps and its Array-based project stacks omit finufft.
The repair belongs in autonerves/setup_colab.py, not Heart's scoring or exceptions.

## Plan

1. Add finufft>=2.4.0 to the Array-based Colab stack, matching AutoArray's Linux floor.
2. Test the actual setup-generated pip command for all six projects: Galaxy/Lens
   and their HowTo variants install finufft; Fit-only projects do not.
3. Run the Nerves suite and the existing AutoArray CPU NUFFT parity tests.
4. Obtain the incident-specific Heart RED corrective-PR authorization before
   committing/pushing the source or opening its PR; no merge/release authorized.
5. After separately approved merge, rebuild candidate wheels and rerun install
   verification and integration; reconcile the original Heart finding IDs.

Tier: judge — merge mode: human /prm.

## Local validation, 2026-10-25

- New bootstrap witness on unmodified source: 4 failed / 2 passed, exactly the Array-based projects.
- Patched Nerves suite: 258 passed / 1 skipped (existing sibling-specifier comparison lacks Fit/Galaxy checkouts).
- Existing AutoArray CPU NUFFT parity suite: 7 passed with finufft 2.5.1 and nufftax 0.6.1.
- Full Colab simulation and candidate-wheel integration have not been rerun.
- No thresholds, test coverage, accepted-missing lists or scoring weights changed.

## Execution and remaining gate

Local proposal: /workspace/scratch/f77499d15f98/PyAutoNerves,
branch feature/colab-finufft-bootstrap. Source changes remain uncommitted.
The general health-work authorization is retained; the named-issue corrective
shipping authorization required by AUTONOMY.md has not yet been requested.

## Approved corrective PR

On 2026-10-25 James replied "I approve" to the named-issue corrective-PR request.
Authorization: https://github.com/PyAutoLabs/PyAutoNerves/issues/204#issuecomment-6399922959
PR: https://github.com/PyAutoLabs/PyAutoNerves/pull/205
Commit: 90bd238356203233ab766976306865999a247ad6
Exact RED: `install verification FAILED (testpypi; checks F)`.
Commit/push/one PR authorized; no merge/release/rehearsal. Prior awaiting-authorization notes above are historical.
