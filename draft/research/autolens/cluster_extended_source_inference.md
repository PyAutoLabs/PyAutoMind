# Cluster extended-source inference: gradient-based fitting building on JAX knowledge

Type: research
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoFit
- autolens_profiling
Themes:
- cluster
- jax-gradient
- pixelization
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 11
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Cluster extended-source inference: gradient-based fitting building on JAX knowledge

Part of the Source & Cluster arc (phase 11 of 12), gated on phase 10. User request
(verbatim): "Once this is robust begin to extend inference with extended sources, build
on JAX gradient knowledge."

Scope: research-first. Phase 10 delivers post-inference refinement (mass model mostly
fixed); this phase asks whether full joint inference of cluster mass + pixelized
sources is tractable with the JAX gradient stack (MultiStart/gradient samplers, SMC
warm-start work, implicit-diff PointSolver gradients from #657).

Known constraints from the JAX campaign memory: pixelized-source gradient sampling was
previously found infeasible (reg/logdet NaN localisation work, Delaunay sqrt(dual_area)
NaN grads, Delaunay needs custom_jvp); factor-graph fits multiply the cost by
n_sources. The research question is what changed/what is needed: which mesh (rectangular
uniform is the gradient-safest), which sampler tier, what the per-iteration cost is at
cluster scale (phase 2 factor-graph profiling cell feeds this), and whether
positions-likelihood + imaging-likelihood factor graphs are jointly jit-able.

Deliverable: a written feasibility verdict with profiling numbers and a go/no-go for a
follow-up implementation prompt — not shipped inference machinery.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase11_cluster_extended_inference.md -->
