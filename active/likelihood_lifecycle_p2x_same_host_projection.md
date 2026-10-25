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
