# inference-setup-producer

Type: feature
Target: autolens_inference
Repos: autolens_inference
Difficulty: large
Consequence: judge
Autonomy: supervised
Priority: high
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/20
Epic: inference-setup-redesign (phase 2)

## Authorization

Human: "prm, and continue through all phases autonomously to the end".
The approved five-phase design and original request are preserved in
draft/feature/pyautoinsight/inference_setup_redesign.md. Phase1 merged Insight#14.
Explicit current authorization covers implementation and merge/close-out on
green checks of all remaining approved phases. No compute, science acceptance
or release. Tier: judge — merge mode: human-authorized in-turn merge after
independent CLEAN review, required tests and every CI job pass.

## Plan

Publish a v2 setup catalogue alongside the existing v1 summary. Define stable imaging rectangular/delaunay and point-source setup identities, explicitly retain unknown and archived evidence; no promotion. Reorganize runnable leaves into scripts/<dataset>/<model>/baseline_slam.py or baseline.py; update all callers, wall-rate cell identifiers, CI/docs without relabelling old results. Keep shared scientific model builders. Add an explicit prepared-baseline artifact manifest with content hashes, exact dataset/model/prior/stage identity and baseline likelihood/parameter/posterior evidence; implement export/reuse validation and cold/warm/resume distinction separately from JIT/cache state. Provide sampler stage investigation entrypoints for supported samplers only, preserving scientific model/prior/adapt state; inspect installed APIs instead of guessing. Add setup wiki summaries and document reproducible CLI from completed baseline to mass_total[1] experiment. Tests must cover mappings, retained provenance, artifact identity failures, start semantics and shared problem reuse. No full science runs or HPC jobs. Full existing checks and meaningful small smoke only. Coordinate exporter with merged Insight v2 contract; if contract needs a compatible refinement report to root. Do not fake runnable NUTS/SMC support where APIs or artifact resume are unavailable; expose an honest unsupported path and explain remaining work to root.

## Survey

@autolens_inference: canonical main, no active claim at survey. Isolated worktree under
/home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-producer, branch feature/inference-setup-producer.
Preserve all unrelated canonical untracked data. Source setup through start_workspace.

## Original request

prm, and continue through all phases autonomously to the end
