# polish phase 1 — holistic design review and lock-in

Type: maintenance
Target: autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of 4 of `polish.md` (see parent for full intent). No profiling runs in
this phase — design and results-presentation groundwork only.

autolens_profiling is now a mature project with good separation into packages
(instruments, latent, likelihood_runtime, likelihood_breakdown, vram, …). Before
the PreOptimizationTimes baseline campaign (phases 2–4), do deep research on the
project and have one last think about ways to improve it: redesigns that make it
more concise and clearer. We will be extending it with more datasets, packages
and instruments, so this is the opportunity to lock the core design in well.

Also scan the repo and make sure that when profiling results come in they are
saved as `.md` or `.json` files and clearly displayed in per-package GitHub
`.md` files for browsing. Design (but do not yet populate) a high-level results
dashboard on the GitHub README. The baseline result set will be named
**PreOptimizationTimes** — the comparison base for the optimization work that
follows.

Out of scope: any profiling runs (phases 2–4); searches; point_source; laptop
GPU (user runs those in a follow-up); the future PyAutoBrain profiling agent
idea recorded in the parent prompt.
