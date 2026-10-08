# Inference setup evidence lookup for the assistant

Type: feature
Target: autolens_assistant
Repos: autolens_assistant
Difficulty: medium
Consequence: judge
Autonomy: safe
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/156
Epic: inference-setup-redesign (phase 4)

Human authorization: "prm, and continue through all phases autonomously to the end".
Parent: draft/feature/pyautoinsight/inference_setup_redesign.md. Original design
approved in conversation; in-turn merge on passed tests/independent review/CI
is explicitly authorized for remaining phases. No compute/science acceptance.

Implement @autolens_assistant pinned inference catalogue lookup mirroring the
existing profiling lookup. Read inference-summary@2 from a fixed committed
checkout, validate provenance/bytes and bind model/dataset/prior/stage/setup,
initialization and hardware/configuration. Return exact, approximate or absent
matches with reasons, immutable result citations, baseline acceptance and archived
qualifications, recorded time/work/seed diagnostics; never extrapolate runtime or
select a sampler from dimension alone. Preserve unknown metadata and distinguish
cold/warm/resume from compilation/cache. Consume producer catalogue rather than
maintain duplicate summaries. Add a skill, discovery and a small example query,
CLI/module and meaningful hermetic tests against the merged contract. Follow
existing discovery-generation conventions. Source/contract docs only; no source
library change or new science run. Run full existing tests and applicable checks.

Survey: canonical main has unrelated untracked dataset/abell_1201; use isolated
worktree .worktrees/inference-setup-advice and feature/inference-setup-advice.
No conflicting claim. Tier judge; human-authorized merge on green all gates.

Original request: prm, and continue through all phases autonomously to the end
