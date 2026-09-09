# Active Tasks

## cortex-scorer-where-paths
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/370
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/371
- issued: 2026-09-09
- heart-ack: 2026-09-09 in-session, five reasons "release validation FAILED (stage integrate)", "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772)", "profiling drift: runtime/imaging/mge/mge_likelihood_summary_hst_v2026.8.17.1.json [eager, full, vmap]", "profiling drift: runtime/imaging/mge_mass_jax/mge_mass_jax_likelihood_summary_hst_v2026.8.17.1.json [jax_mge_mass]", "profiling drift: runtime/imaging/pixelization_numba_mge_mass/pixelization_numba_mge_mass_likelihood_summary_hst_v2026.8.17.1.json [numba_cpu_mge_mass]" — all organism-scope in the libraries; this branch is the PyAutoBrain Cortex conductor and its tests, nothing in it is in the release chain
- session: claude --resume session_01FKSwTBuNwcJc2FPNpSCrkp
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/cortex-scorer-where-paths
- repos:
  - PyAutoBrain: feature/cortex-scorer-where-paths
- summary: |
    Cortex check-in scorer: `where_paths` keeps only absolute `## Where to look`
    bullets and reads only each bullet's first token, so every real (relative,
    label-prefixed) bullet is dropped and `run_artifacts` falls back to the
    newest run under `output/` — scoring a task against an unrelated run and
    reporting a confident FAIL. Fix resolves relative bullets against the
    project roots, scans the whole bullet for path-like tokens, and refuses to
    fall back when a task declares roots that yield no run (UNOBSERVABLE, not
    FAIL); any fallback that does happen is marked as one in the readout.

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"

## aggregator-temp-unzip
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1584
- prompt: active/aggregator_temporary_unzip.md
- issued: 2026-09-09
- session: claude --resume session_01EwQS9x9Ls1NBUpbASL7n1s
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1592
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/aggregator-temp-unzip
- repos:
  - PyAutoFit: feature/aggregator-temp-unzip
- heart-ack: 2026-09-09 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run of 2026-09-09T07:23Z); nothing in this branch is in the release chain; human typed /prm after the reason was quoted back
