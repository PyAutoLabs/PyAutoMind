# Chapter 3 adaptive continuation — five-block review

Status: follow-up split from the merged reviewed checkpoint.
Target: HowToLens Chapter 3 only.
Consequence: judge

## Shipped checkpoint

`complete/2026/10/howto-chapter3.md` records merged HowToLens#112 and HowToGalaxy#95. Lens lessons1–4 and Galaxy lessons1–3 are complete; do not redo their accepted prose or edit Chapter2. Existing Lens adaptive lessons8/11/12 remain available with original numbering.

## Remaining user request

Consolidate the retained adaptive material around Delaunay, Hilbert image meshes and Split regularization, with useful phenomenological explanations rather than likelihood derivations. Explain why the adaptive choices help with the practical reconstruction problems introduced earlier. End with an actual Delaunay model fit. Keep a subtle preference for Delaunay in the later sections, without claiming it is universally optimal.

The standalone fit-problems tutorial was explicitly cancelled. Do not recreate it or restore the model-fit stub. Non-interpolating rectangular meshes were explicitly dropped. Preserve MGE as the analytic baseline and a useful tool; only Maresca Figure1 is approved.

## Workflow

Research current workspace/SLaM APIs, then present five blocks at a time with actual Python code and detailed conversational explanations. The overall direction is approved; the remaining adaptive blocks have not yet been reviewed. Do not bulk-author them as approved content. Use the Brain docs workflow, then implement approved blocks, validate actual figures/fits, regenerate notebooks/catalogues and ship a separate PR.

Exact approved draft history and generated checkpoint notebooks: `C:\Users\Jammy\Workspace\Science\scratch\chapter_3_implementation_2026-10-31`. Heart RED overrides on the previous PRs were task-specific and do not imply a new shipping grant.
