# Critical curves: implement context-aware dispatch, dedupe engines, make clusters honor

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
- PyAutoMind
Themes:
- cluster
- jax-compile
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 3
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Critical curves: implement context-aware dispatch, dedupe engines, make clusters honor it

Part of the Source & Cluster arc (phase 3 of 12). User request (verbatim): "Dig into
critical curves calculations again, make sure they are efficient working and well set
up, need to be careful with no JAX slow down. Then make sure they work on clusters with
sensible test cases. Difficulty here is we have JAX critical curve method which is slow
when not jitted and the standard one. Need to make decision if we always enforce JAX
use on this (e.g. even outside of lens modeling)."

Audit findings (2026-08-19) that settle the decision question with evidence:
- Marching-squares path (LensCalc, numpy/skimage) can never jit — the contour primitive
  (autoarray/operators/contour.py:57-62) explicitly converts JAX arrays back to numpy.
- zero_contour path: warm 67 ms / cold 10.3 s / **eager (JAX_DISABLE_JIT=1) times out at
  >10 min — "unusable without JIT"** (PyAutoMind complete/2026/05/
  fast-viz-zero-contour-perf.md). So "always enforce JAX" is falsified for one-shot
  plotting; the recorded decision (marching_squares default for one-shot, JIT callers
  auto-route) is right — but **the context-aware dispatch was never implemented**; the
  config flag is still a global static.

Concrete defects to fix in the same pass:
1. `autogalaxy/plot/plot_utils.py` and `autogalaxy/util/plot_utils.py` are byte-identical
   twins; imports split across both — dispatcher changes must currently be made twice.
   Deduplicate to one module.
2. Docstring/config contradiction: both copies (:376, :423) label zero_contour
   "(default)" but config/visualize/general.yaml:8 ships marching_squares. Also stray
   text `/btw ok` mid-docstring at :422 (both copies) and a truncated docstring in
   contour.py:17-19.
3. **Cluster plots bypass the dispatcher entirely** (autolens/cluster/plot/
   cluster_plots.py:401/414/480/493 hard-wire marching squares) — clusters can never use
   zero_contour even when configured. Route them through the dispatcher; keep the
   per-source-plane multi-plane handling (LensCalc.from_tracer(use_multi_plane=True,
   plane_j=j)).
4. Cluster-scale test cases: marching squares at arcminute scale needs ≤0.5"/px or
   member-galaxy wiggles are missed (cluster_plots.py comment); the evaluation-grid
   1000×1000 cap hack (lens_calc.py:104-106) interacts badly with that. Add cluster
   test coverage for both engines (multi-plane, per-source-plane curves).

Absorbs `draft/triage/jax_zero_contour.md` (jit/grad parity testing on
autolens_workspace_test — fold in as the verification leg). Related but separate:
`draft/refactor/autogalaxy/einstein_radius_jit_native_seed_finder.md` (JAX-native seed
finder; zero_contour's 25×25 seed scan still routes through skimage) — link, don't
absorb (it is sized too-large on its own).

Sequencing: before the magnification-map phases — critical curves are the contour
overlay on every magnification map and the LEGGOS-style arc-segmentation boundary.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase03_critical_curves_dispatch_cluster.md -->
