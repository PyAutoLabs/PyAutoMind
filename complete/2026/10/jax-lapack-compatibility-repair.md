# JAX LAPACK deadlock compatibility repair

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/274
- completed: 2026-10-04
- scope: Compatibility repair phase only. Umbrella dashboard repair remains active; no release clearance.
- authorization: “ok great then wrap up the work her,e prm authorized if needed and continue”

- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/184
- merge: PyAutoNerves 82a60579a1e715e62094c9d3e14f3a8e10540970
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/297
- merge: PyAutoHands 5e42698d6f4d51912624c4c93bd3afe9fdf41d63
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1659
- merge: PyAutoFit 83844c526ef3fd5d9015e1dd2de6c6182e53f909
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/647
- merge: PyAutoGalaxy 1aa5aa7f2d52d61c6554e0dc7d7cbc70d0b85eb5
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/280
- merge: PyAutoHeart 4920ab98a8a42026ff91545b890a9ff64de43e11
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/612
- merge: PyAutoArray 9a6237f09a4cc26abad0e8e0742f4da955631033
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/766
- merge: PyAutoLens b695e57b69d168e33b760b169c29cfcf0d9cd8f9
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/112
- merge: PyAutoCTI 5e876a01fed677d3923e501ca6b1cc79ed0e1bbe

All eight PRs merged after all28 jobs across12 current-head workflow runs passed, mergeability CLEAN, freeze clear, and independent Sol review CLEAN. Git ancestry proves every claimed branch is merged.9255 local tests passed (2 skips,5 xfails). CPU/CUDA original-likelihood and numerical probes pass0.9.2/0.11.2; hosted37210342253 passes both withPython3.12.14 and113 unchanged non-JAX pins.25 resolver cases plus fresh normal resolution pass.

Policy preserves>=0.7,<0.12, excludes0.10.* /0.11.0;0.10.2 native LAPACK/Eigen deadlock reproduced, other exclusions source-based. Older0.9.2 lacks path; OSS>=0.11.1 disables it. HistoricalFFT workaround retained. No blanket older-version certification. Consumer autonerves>2026.10.4.1 guard prevents permissive-Nerves fallback; publish protected Nerves first using human-selected higher base version. No package publication here.

Original release validation remains failed. Prior interleaved comparison remains inconclusive. Point-gradient broader diagnostic times out both versions at300s. Follow-up inspection of saved0.11.2 native dump finds active main-thread JAX partial evaluation / cosmology Simpson integration at gradient.py:374, rather than a captured LAPACK wait; later image-plane likelihood prints, proving progress beyond that sample. This does not explain the final timeout.0.9.2 native capture failed; gdb absent. Keep all evidence and investigate separately.

Canonical clean main checkouts fast-forwarded; retained task worktree/data and unrelated dirty science untouched. No Anthropic auth changes, release/rehearsal, upstream report, watcher or cap increase. #274 and active prompt retained for remaining scope; do not close whole umbrella or delete retained worktree.

Evidence: Mind tmp/heart-timeout-20261004/prm-audit.json, merged-prs.json, full-suites/, hosted-37210342253/; Heart committed diagnostics. User requested an Anthropic-repair prompt for a separate chat; handoff supplied, no auth work performed here.
