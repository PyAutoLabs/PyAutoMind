# JAX autodiff audit: light profiles, pixelized-source gradients, and likelihood gradients

Type: research
Target: autolens_profiling
Repos:
- PyAutoLens
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

You're working in the PyAutoLens or PyAutoArray codebase, using the usual profiling workspace, profiling agent, and PyAutoBrain flow. First, investigate the state of JAX autodiff support for Sérsic light profiles, linear Sérsic light profiles, and Multi-Gaussian Expansion light profiles. Profile what's there, identify what breaks tracing or differentiation, and add or refine automated tests comparing autodiff against finite differences. Second, investigate gradients for pixelized source reconstructions, starting with the Delaunay mesh. We expect that full gradients may not be feasible there. Confirm why and document where it fails. Then move to the rectangular mesh, where we think gradients might be possible. Before starting that part, ask me for the relevant paper if you don't already have it. Third, validate gradients for the source plane chi-squared used for point sources, and for the weak lensing likelihood.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; work-type & target corrected in review: research / autolens_profiling) -->
