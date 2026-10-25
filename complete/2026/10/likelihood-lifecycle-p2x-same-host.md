Follow-up to #463 (human ruling 2026-10-25: never project across machines). PR autolens_profiling#465 merged 29caed89 under a Heart RED development override (live human chose this task alone; four records written; lint green; human /prm).

- project() keeps only the reference host whose host_class equals the record's measured class (hpc_ral_cpu → ral_cpu_node; hpc_a100 → ral_gpu_node, including the A100 node's CPU legs as CPU workers). An unmatched class, or a GPU record on a host without GPUs, gives not_projected with a reason. Duplicate classes raise an error. per_call_measured_on_host is removed.
- Current runtime records: 50 projected and 5 not projected, unchanged. RAL CPU (19) and A100 CPU legs (9) lose their other-host entries; the worked tables didn't change.
- Memory variation is out of scope by human ruling.

NEXT in the epic: the Pulse throughput view (draft/feature/pyautopulse/likelihood_lifecycle_p2x_throughput_view.md), then 2b. Each needs its own RED override while Heart is RED.

## Original prompt

# Likelihood lifecycle phase 2x follow-up: project each row only onto the host class it was measured on

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: no v3 record's projected_node_throughput contains a host whose class differs from the row's measured host class; build_catalogue --check --validate-with ../PyAutoPulse and pytest pass
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-25
Issued: 2026-10-25

Human ruling 2026-10-25, after #463 merged: "Don't project to other machines, don't investigate memory, continue epic."

#463 projects each runtime row onto every reference host with its device class, including hosts it was not measured on (the laptop, and the other RAL node type), flagged `per_call_measured_on_host: false`. Remove those entries: project only onto the reference host matching the row's measured host class (`hpc_ral_cpu` → `ral_cpu_node`; `hpc_a100` → `ral_gpu_node`, which also covers its `jax_cpu_sparse@hpc_a100` CPU legs; laptop rows → `laptop`). A host class with no matching reference host gives `not_projected` with a reason. Drop the `per_call_measured_on_host` field, since it is always true now. Update tests, regenerate catalogue → dashboard → coverage, and fix the docs wording. Memory variation between runs is out of scope (human ruling).
