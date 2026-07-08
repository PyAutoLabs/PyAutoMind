# Profiling agent

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- autolens_profiling
- PyAutoHeart
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Profiling agent. Grow a PyAutoBrain agent that owns performance measurement for the organism, using autolens_profiling as its workspace — the endpoint the polish series (autolens_profiling#52/#54/#56) was building toward. Not lensing-specific: it understands PyAutoFit (searches, likelihood functions, latents), JAX (jit/vmap compile vs steady-state, backend selection), and the CPU / laptop-GPU / HPC-A100 hardware tiers. What it orchestrates, all demonstrated by the polish phases: campaign dispatch (sweep.py instrument matrix, cheapest-first), vram-first validation and probe ingest (probe JSONs -> VMAP_BATCH/VMAP_BATCH_SPARSE with provenance), pinned-value maintenance (pin newly measured instruments; triage pinned_drift flags with the PyAutoHeart profiling_drift vitals leg, merged as Heart#38), baseline snapshots (build_baseline.py, PreOptimizationTimes convention), dashboard refresh, and HPC dispatch/ingest cycles when RAL is available. Future capabilities from the parent prompt: JAX compilation-time profiling of likelihood functions, and hunting generally-slow functions flagged by integration tests. Design questions to settle first: conductor vs faculty per the demonstrated-need doctrine (evidence now exists — three phases ran this workflow through the generic dev-flow with heavy manual orchestration); boundary rules against the health agent (observes verdicts, does not run campaigns) and the hygiene-agent debate (research/pyautobrain/hygiene_agent_decision.md — profiling is performance measurement, not repo hygiene); and whether the agent's first increment is just the campaign/ingest conductor with the future capabilities staged as follow-ups. Implementation is ordinary feature/pyautobrain work per ROUTING.md. Blocked until the clone-mitosis-agent task ships (PyAutoBrain claimed).

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake;
     re-homed maintenance/autofit -> feature/pyautobrain in conversation: agent
     implementations are feature/pyautobrain per ROUTING.md; PyAutoFit was a
     knowledge-domain mention, not the target -->
