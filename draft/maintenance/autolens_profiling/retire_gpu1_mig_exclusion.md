# Retire the euclid-ral-gpu-1 MIG exclusion: drop every `--exclude` line, the preflight backstop and the README section

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- hpc
- ral
- hygiene
Difficulty: small
Autonomy: safe
Priority: medium
Status: draft
Consequence: judge
Witness: `grep -rn "euclid-ral-gpu-1\|_gpu_preflight\|MIG" hpc/ activate.sh` returns nothing except a dated historical note in hpc/README.md, and one A100 submit dispatched without the exclusion completes on euclid-ral-gpu-1
Review-minutes: 10
Unattended: ready
Filed: 2026-09-05

Original request (verbatim):

> give me prompt to remove any MIG thing

## Why now

On 2026-08-26 one A100 on `euclid-ral-gpu-1` (PCI 07:00.0) was left in MIG mode with no
instances, SLURM kept advertising it as a plain `gpu:A100`, and any job landing on it died
at `cuInit` with `RuntimeError: Unable to initialize backend 'cuda'`. The 2026-08-28 fix was
`#SBATCH --exclude=euclid-ral-gpu-1` on every `hpc/batch_gpu` submit plus
`hpc/batch_gpu/_gpu_preflight.sh` sourced as a requeue backstop, at the cost of half the
A100 fleet (4 of 8). `hpc/README.md` "GPU node exclusion" records the retirement condition:
confirm MIG mode is off from inside a job on that node, then drop the `--exclude` lines,
then the preflight.

That condition was met on 2026-09-05. From inside `srun --partition=gpu
--nodelist=euclid-ral-gpu-1 --gres=gpu:4`, `nvidia-smi --query-gpu=index,pci.bus_id,
mig.mode.current` reported `Disabled` on all four cards including 07:00.0, and a JAX CUDA
backend init plus a `jnp` reduction succeeded on each GPU individually via
`CUDA_VISIBLE_DEVICES=0..3` under the canonical `activate.sh` venv.

## Scope (autolens_profiling only)

1. Remove `#SBATCH --exclude=euclid-ral-gpu-1` and its accompanying "Node exclusion
   (2026-08-28)" comment block from every submit under `hpc/batch_gpu/` (86 files carry it
   at filing time) and any under `hpc/batch_cpu/`. Use a scripted sweep over the exact
   lines, then diff-review; do not hand-edit 86 files.
2. Remove the `source .../_gpu_preflight.sh` line from every submit that carries it (85 at
   filing time) and delete `hpc/batch_gpu/_gpu_preflight.sh`. The `--requeue` dispatch
   convention may stay documented but is no longer required by this guard.
3. `activate.sh` and `hpc/batch_gpu/submit_search_nautilus_inference_refs_v1_array.sh`
   mention the node or MIG outside the standard block; read each and strip only the
   MIG-motivated logic, keeping anything unrelated.
4. `hpc/README.md`: replace the "GPU node exclusion: euclid-ral-gpu-1 is off-limits"
   section with a short dated history note (what happened, when it was retired, the probe
   command that confirms the node, and the instruction to re-add the exclusion if the
   `cuInit` failure signature ever returns). The retirement checklist that section
   currently holds is the procedure to follow.
5. Results notes under `results/notes/` that mention the exclusion as context of a past
   run (`clipper_campaign/RESULTS.md`, `inference/PROGRAMME.md`, `inference/DECISIONS.md`,
   `inference/phase_08_regularization/RESULTS.md`) are historical records: leave them.
6. Verify: `AUTOLENS_PROFILING_SMOKE=1` import smoke unaffected, `ruff` clean,
   `build_readme.py --check` passes, and dispatch one cheap GPU submit (the
   `submit_delaunay_nn_benchmark_a100` benchmark is a good candidate) forced onto
   `euclid-ral-gpu-1` with `sbatch --nodelist=euclid-ral-gpu-1`; it must complete and its
   log must show a CUDA device.

## Out of scope

The in-flight `delaunay-nn-breakdown` task (autolens_profiling#219) writes new submits
with the exclusion dropped and a dated comment; merge order does not matter, the sweep
in step 1 simply finds nothing to remove in those files. The RAL admins' side (why the
card was in MIG mode) is not ours.
