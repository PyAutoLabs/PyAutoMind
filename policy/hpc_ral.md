## HPC access (RAL, GPU)

<!-- Moved verbatim from the workspace-root AGENTS.md (PyAutoMind#482) so the
     always-loaded root shrinks to a pointer stanza that keeps the two hard
     rules. Read this page on demand before any RAL / SLURM work. -->

- Cluster is RAL: connect via SSH alias `euclid_jump` (→ euclid-saas.roe.ac.uk, user `jnightin`), which `ProxyJump`s through `jump_finan`; aliases + keys are in `~/.ssh/config`. Projects live under `/mnt/ral/jnightin/<project>`.
- The PyAuto stack on RAL is a virtualenv under `/mnt/ral/jnightin/PyAuto` (`PYAUTO_HPC_BASE`, sourced by `activate.sh`) that mirrors this local install, with the library `main`s kept in sync — check/refresh that sync with `HPCPullPyAuto`.
- Drive GPU runs with the project's `hpc/sync` CLI: `hpc/sync push-submit gpu <script>` submits a SLURM `gpu`-partition array (one dataset per array task; JAX auto-uses the GPU), then `hpc/sync jobs` / `tail gpu` / `pull`. You may run these directly from a CLI session on your machine; in a cloud/web session there's no SSH access or keys, so treat this as context only.
- **CPU arrays never go on `gpu` (human rule, 2026-09-30).** Bulk/production CPU-only arrays use `--partition=ral` only — never `gpu`, `ral,gpu` or `gpu,ral`, even when ral is drained or busy (wait for ral). On 09-30 euclid_dr1 `ral,gpu` CPU arrays took all 124 CPUs on euclid-ral-gpu-1/-2 and left all 8 A100s idle but unschedulable for hours. Only exemption: small CPU timing legs on `gpu` without `--gres` with ≤8 CPUs/task, throttle ≤`%2`, and no pending GPU jobs (`squeue -p gpu -t PD` shows no gres/gpu). Partition ≠ device: check TRES for gres/gpu with `scontrol show job` before calling it a GPU run; for a stuck A100 job compare node AllocTRES cpu vs CfgTRES.
- Never reorder, hold or cancel another campaign's jobs without the human's OK.
