# Promote the multi-start gradient MAP optimizer to a first-class PyAutoFit

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autolens_workspace_developer
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Promote the multi-start gradient MAP optimizer to a first-class PyAutoFit search. Add a new JAX/optax NonLinearSearch to PyAutoFit — a multi-start gradient MAP optimizer (working name af.MultiStartGradient) — growing the search library alongside af.Nautilus, af.LBFGS and af.Drawer. This promotes the winning method from the Phase-3 GPU MAP-optimizer benchmark (autolens_workspace_developer PR#99): wide multi-start first-order gradient descent, vmapped over N independent broad starts on the GPU, which reliably recovers the truth basin where every single-start, line-search and second-order method fails. The new search runs N broad starts in parallel on the shared unconstrained parameterization, with the local optax update rule (Adam/ADABelief/Lion) and the start count N as first-class configurable knobs, and returns the best-basin MAP point plus per-start basin diagnostics through PyAutoFit's standard search/samples/result contract. Port the reference implementation from searches_minimal/gpu_multi_start_adam.py and _grad_setup.py (unconstrained z-transform, robust finite-gradient start generation, batched value_and_grad). The top two configurations to ship first are Adam (best) and ADABelief (tied); Lion optional. Line-search/second-order methods (L-BFGS/BFGS/NCG/LM/GN) all failed the benchmark and are explicitly out of scope. Library-first in PyAutoFit, then workspace examples showing the search on an imaging lens fit; keep JAX out of unit tests (cross-backend validation belongs in workspace_test). Likely splits into phased PRs (core search + samples/result, config + packaged defaults, workspace examples).

<!-- formalised by the Intake (Conception) Agent on 2026-07-14 from user-intake -->
