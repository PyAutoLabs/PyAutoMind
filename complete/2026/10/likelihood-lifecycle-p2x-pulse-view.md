Pulse half of likelihood-lifecycle phase 2x. PyAutoPulse#77 merged db5e7c02 on human /prm ('Ship and prm', Heart YELLOW acknowledged after release 2026.10.25.1).

- profiling-summary@3 validates resources and projected_node_throughput (additive, optional; malformed blocks are refused; no cross-machine hosts; Pulse never recomputes).
- Setup browser View selector (per call, the default, or per node); dashed amber 'projected' badge with an accessible tooltip (η + source, bound_by + worker caps, per-call basis, what isn't modelled); board column 'Node throughput (projected)'.
- New knowledge/cpu_parallel_vs_gpu_batched.md: 7 decision rules (formula, memory cap, W~ sharing after fork unknown until phase 4, η 1.0 declared, n_batch ceiling, fork rules, RAL hosts, 2a worked examples). knowledge/ is new; decisions/ stays human-decision-only.
- Lens refetched at autolens_profiling 29caed89: 626 resources blocks; 78 throughput blocks (50 projected).

Note: no class:optimal lens rows yet (phase 3), so the default Class filter shows few per-node values. NEXT: phase 2b interferometer.

## Original prompt

# Likelihood lifecycle phase 2x (Pulse): per-call vs per-node-throughput view, and a research page on comparing CPU-parallel and GPU-batched setups

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: the Pulse board and setup browser offer a per-call / per-node-throughput switch; projected values render visibly distinct and show their efficiency basis; `pyauto-pulse check` passes on the refetched lens receipt; the knowledge page is linked from the board
Review-minutes: 25
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-25
Issued: 2026-10-25

Pulse half of the human's 2026-10-25 ruling: numba CPU runs one process per core under Nautilus multiprocessing, so CPU vs GPU must be compared as node throughput. Depends on `complete/2026/10/likelihood-lifecycle-p2x-node-throughput.md (merged autolens_profiling#463)`, the producer task that declares `projected_node_throughput`.

## Boundary

The producer declares, Pulse validates and displays, and the Brain's profiling conductor judges. Pulse computes no projection itself and issues no verdict.

## Scope

1. **Validate the producer's new fields.**
   - Fields: `cpus_per_eval`, `peak_rss_gb`, `projected_node_throughput` with `basis`, `parallel_efficiency`, its source and `bound_by`.
   - These are additive to `profiling-summary@3`, unless the producer task found that a version bump is needed.
2. **Board and setup browser:** a per-call / per-node switch.
   - Projected values carry a "projected" badge or hatching, plus a tooltip giving η and its source and the bounding limit.
   - Measured values from phase 4 replace the badge when they arrive.
   - The default view stays per-call until phase 4 measures η, so projections never headline.
3. **Knowledge page:** "Comparing CPU-parallel and GPU-batched setups", which the autolens_assistant reads as decision rules. It covers:
   - the formula;
   - the memory cap per worker (ao ~25 GB) and whether the W~ operator is shared after fork (copy-on-write);
   - parallel efficiency, declared until measured;
   - the Nautilus batch ceiling;
   - the JAX fork rule;
   - the RAL reference hosts;
   - the 2a worked examples (hst and ao Delaunay).
