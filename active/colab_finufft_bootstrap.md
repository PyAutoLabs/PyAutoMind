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
