# Optimize the fast non-negative least squares solver for the Delaunay and rectangular mesh pipelines

Type: feature
Target: autolens_profiling
Repos:
- PyAutoArray
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

You are working in the PyAutoLens codebase. First, review the recent Delaunay mesh speed-up work and understand what was changed and why. Then assess whether optimizing the fast non-negative least squares solver is the right next target, considering both Delaunay and rectangular mesh pipelines. If it is, propose and implement a careful optimization with benchmarks and numerical stability checks. Keep the design clean and document it so that it can be ingested into PyAutoBrain later. Before coding, summarize your understanding, confirm the optimization target, and outline a step-by-step plan.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; work-type corrected docs->feature and target->autolens_profiling in review; difficulty bumped small->medium) -->
