# Profile the Pandora (Abell 2744) cluster likelihoods in autolens_profiling, as Simple was

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- cluster
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: an autolens_profiling PR adds Pandora (Abell 2744) source-plane and image-plane CPU likelihood profiling beside `simple_cluster/`, with a README table of first-call-after-compile, warm median and p10–p90 per likelihood, the JAX–NumPy log L difference, and the observed vs predicted image count per family on the phase-3.2 solver grid; Simple's image-plane row is re-timed on that grid; Pulse contract and repo checks pass
Review-minutes: 20
Unattended: ready
Lane: local-dev
Blocked-by: autolens_profiling#537
Epic: cluster-usability
Phase: 3.5
Filed: 2026-11-26

## Why

Ledger `draft/feature/autolens/cluster_usability.md`, item 5 ("Exercise real workloads in Pulse
and Insight"), for the second tier. Simple's CPU profiling is in autolens_profiling PR #537
(green, open). The human ruled on 2026-11-26 that Pandora profiling goes ahead of phase 4a
(slow-path timings).

## What to do

1. Plan first (start_dev): post the plan on the issue before any edit. Starts only after PR #537
   has merged; build on its layout, cache guard and pinned-fixture checks rather than copying.
2. Pin the Pandora (Abell 2744) inputs from autolens_visualization's reviewed gallery model, as
   #537 pinned Simple's, and validate the scaling catalogue with the consuming reader.
3. Profile both likelihoods on the local CPU (JAX FP64): first call after compile, warm median of
   ≥ 200 synchronised calls after 5 warm-ups, p10–p90, JAX–NumPy agreement, and a breakdown that
   reproduces the headline log L.
4. Use the solver starting grid adopted in phase 3.2 (if 3.2 has not merged, use 0.25″ and say
   so). Record observed and predicted family sizes; an image-plane time from an incomplete solve
   is diagnostic only, as in #537. Re-time Simple's image-plane likelihood on the same grid.
5. Regenerate the dashboard, run the Pulse contract and repo checks, and ship to an open PR.

## Rules

- Plan-first. CPU on the laptop only: no RAL or GPU runs in this phase.
- Inference (autolens_inference / Insight) for Pandora is a later phase, not this one.
- Merge and issue close stay human.
