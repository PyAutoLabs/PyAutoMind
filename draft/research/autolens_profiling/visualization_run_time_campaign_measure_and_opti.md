# Visualization run-time campaign: measure and optimize modeling-run visualization in autolens_profiling and PyAutoPulse

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
- PyAutoGalaxy
- PyAutoLens
- autolens_inference
Themes:
- visualization
- profiling
- jax-compile
Difficulty: too-large
Autonomy: human-required
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: never
Lane: ral
Campaign: visualization
Filed: 2026-11-06

Human request (verbatim, 2026-11-06): "intake a larger prompt which is to incorporate visualization run times and optimization into autolens_profiling and PyAutoPulse fully as a whole campaign, the prompt can have us fully flesh out the scope with Fable first just have it something I have on the list ready to do"

## Intent

Make visualization a first-class profiling campaign. Today it is a blind spot: we profile likelihoods, samplers and wall times in depth, but not what a modeling run spends drawing figures (quick updates, stage-end visualization, critical curves and caustics, subplots, source reconstructions). The campaign should measure it, place it in autolens_profiling (scripts + wiki campaign ledger) and PyAutoPulse (a campaign with tasks, a dashboard row and a walltime share), and drive optimizations through the normal start_dev flow.

## Step 1: scope it with Fable before any work

This prompt is a placeholder. Its first session is a **scoping conversation with Fable** (Feature Agent / epic planning, human in the loop) that turns it into a phased epic. Nothing is implemented until that scope is agreed. Questions the scoping should settle:

- **Denominator:** what share of a real run's wall time goes to visualization, per likelihood family and scale? Use the phase-4 walltime rows (autolens_inference#59) and per-figure timings; decide if a run-level "viz share" belongs in `walltime-validation@1` or a new Pulse schema.
- **Inventory:** which figures fire at quick-update vs stage-end vs aggregator time, how often (cadence), and on which device and process. Includes the JAX-parent / Nautilus-worker interaction and plotting under fp64.
- **Instrumentation:** a reusable per-figure timer harness in autolens_profiling (cold vs warm, compile vs run, CPU vs A100) and how its rows reach Pulse.
- **Known leads to fold in, not duplicate:**
  - autolens_profiling#521: critical-curves zero-contour feasibility. Pilot: zero-contour 21–38 s per figure vs marching squares ~1.3 s, because it recompiles every figure.
  - `draft/refactor/autogalaxy/zero_contour_pytree_compile_cache.md`: pytree compile-cache refactor, gated on #521.
  - Pulse task `quick_update_plotting_cost`.
  - Phase-3a cluster critical-curve findings (seed coverage, path completion).
- **Optimization levers to assess:** caching and compile reuse, skipping or deferring expensive panels during quick updates, cadence policy, resolution and grid caps, backend choice per figure, and moving visualization out of the sampler's critical path.
- **Ownership:** Pulse owns campaign intent and pending tasks; library fixes go through start_dev; the Eyes organ owns figure appearance. Name the boundary.
- **Phasing and exit:** pre-registered rules for "visualization is cheap enough" per scale, and which phases are GPU/RAL work.

## Output of step 1

A phased epic (parent prompt + phase prompts, or Pulse tasks for the measurement phases), each with Consequence and Autonomy declared, plus a Pulse campaign entry. Then start the first phase via /start_dev.

<!-- formalised by the Intake (Conception) Agent on 2026-11-06 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b8d07835-3b05-4ec8-8d02-781e09e7a2b3/scratchpad/viz_campaign.md -->
