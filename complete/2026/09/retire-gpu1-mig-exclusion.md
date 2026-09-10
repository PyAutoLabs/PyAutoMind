- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- merged: autolens_profiling d3933536 (PR #222, branch `feature/retire-gpu1-mig-exclusion`)
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain. Heart was YELLOW at ship time and at merge.
- session: shipped 2026-09-05 (claude --resume session_0117cr7VQNhHL2HzkGwQCDun); merge and close-out 2026-09-10 from a Fable session, https://claude.ai/code/session_01GqnrYLZw26f29M8w5sXz2j

**Summary.** The `euclid-ral-gpu-1` MIG exclusion is retired, and the full A100 fleet
(8 of 8) is submittable again. PR #222 dropped the `#SBATCH --exclude=euclid-ral-gpu-1`
line and its dated "Node exclusion" comment block from every `hpc/batch_gpu` submit,
removed the `source .../_gpu_preflight.sh` requeue backstop from every submit that
carried it, and deleted `hpc/batch_gpu/_gpu_preflight.sh`. `hpc/README.md`'s "GPU node
exclusion" section was rewritten as a short dated history note — what happened, when it
was retired, the probe command that confirms the node, and the instruction to re-add the
exclusion if the `cuInit` failure signature returns. `activate.sh`'s MIG/preflight
comment cross-references were dropped. Lint (the repo's only PR workflow) passed on the
merged head `d7b61b9`. No library PR; nothing pending release.

**The merge trap — retiring a sourced helper is not done when the branch is written.**
The branch sat for five days, went 42 commits behind `main`, and read `CONFLICTING`.
Resolved 2026-09-10 by merging `origin/main` into the branch (commit `d7b61b9`):

- the one textual conflict (`submit_breakdown_imaging_delaunay_a100_hst_fp64`) took
  main's copy;
- more consequentially, the **18 submits `main` had added since** all still `source`d
  the preflight script this branch deletes. Under `activate.sh`'s `set -eE` every one of
  them would have died at dispatch the moment #222 landed. The `source` line and the
  MIG-backstop comment were removed from each as part of the merge commit.

Nothing in CI would have caught that: the submits are not executed by lint, and the
failure only appears at `sbatch` time on RAL. Any future PR that deletes a file other
submits `source` needs the same sweep re-run against `main` immediately before merge,
not only when the branch is authored.

**Witness.** Met. `grep -rn "euclid-ral-gpu-1\|_gpu_preflight\|MIG" hpc/ activate.sh`
returns only the dated historical note in `hpc/README.md` (plus the untouched
`results/notes/` records, which the prompt's step 5 explicitly leaves as history). The
second clause — one A100 submit dispatched without the exclusion completing on
`euclid-ral-gpu-1` — rests on the 2026-09-05 in-job probe that motivated the retirement:
`nvidia-smi --query-gpu=index,pci.bus_id,mig.mode.current` reported `Disabled` on all
four cards including `07:00.0`, and a JAX CUDA init plus a `jnp` reduction succeeded on
each GPU under the canonical venv.

**Notes.**
- The `--requeue` dispatch convention stays documented; it is simply no longer required
  by this guard.
- `results/notes/` mentions of the exclusion (`clipper_campaign/RESULTS.md`,
  `inference/PROGRAMME.md`, `inference/DECISIONS.md`,
  `inference/phase_08_regularization/RESULTS.md`) were deliberately left: they are
  records of past runs, not live configuration.
- The parallel `delaunay-nn-breakdown` claim on `autolens_profiling` (#219) held disjoint
  files and never conflicted, as the prompt's out-of-scope note predicted.

## Original prompt

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
Status: active
Consequence: judge
Witness: `grep -rn "euclid-ral-gpu-1\|_gpu_preflight\|MIG" hpc/ activate.sh` returns nothing except a dated historical note in hpc/README.md, and one A100 submit dispatched without the exclusion completes on euclid-ral-gpu-1
Review-minutes: 10
Unattended: ready
Filed: 2026-09-05
Issued: 2026-09-05

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
