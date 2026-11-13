# Refresh the DNA observation of the RAL shared PyAuto environment

Type: maintenance
Target: PyAutoDNA
Repos:
- PyAutoDNA
Priority: low
Consequence: notify
Lane: ral

Source: dna-policies-section (PyAutoDNA#6, complete/2026/11/dna-policies-section.md). The DNA board lists the RAL
shared environment (`ral-login`) as stale (last observed 2026-10-08). It runs jax 0.11.2, so once re-observed the
board should flag it as a hanging JAX CPU setup.

## What happened on 2026-11-11
`dna collect ral-login --probe-backend` (DNA code copied to /mnt/ral/jnightin/dna_collect, run with the shared venv
/mnt/ral/jnightin/PyAuto/PyAuto activated, `--repo` the five library mirrors) sat in NFS D-state on euclid-saas for
24+ minutes and died without a receipt.

## What
Collect it so it cannot hang a login shell: run the collect as a short SLURM job on a `ral` compute node (1 CPU,
15 min, `--no-requeue`, via `hpc/sync`), or drop `--repo` (the per-repo `git status` over NFS is the likely stall)
and probe the backend separately. Copy the receipt back privately, `dna import`, `dna export-public`, PR.
