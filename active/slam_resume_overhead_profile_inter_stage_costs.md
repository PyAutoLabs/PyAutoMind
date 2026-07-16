# SLaM resume overhead: profile inter-stage costs, judge speed-up vs checkpointing

Type: feature
Target: workspaces
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

It is common for a user to set off a lens model, get so far, and then resume that model. For SLaM pipelines,
this can take time if it has to do tasks between each stage, which makes doing the science slower.

First, can you extend autolens_profiling to have some testing and profiling code for this, its part of the
core run time and thus falls under profiling rather than hygeine (e.g. in the context of agent work).

Then, can you assess if it is slow, whether the best way forward is to try and speed it up or if it would
be feasily to build a checkpoing system, where resuming goes straight to the latest result to
resume? Normally this would be fine, the issue is that stuff like adapt images, which get passed through
the pipeline, would need to be carefully thought about so the resume has their data loaded from the right place.
This may make a full chckpointing system unnecessary complex. You judge.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_raw.md -->
