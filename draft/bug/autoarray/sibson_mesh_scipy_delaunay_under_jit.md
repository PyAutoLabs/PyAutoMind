# Sibson natural-neighbour mesh calls scipy Delaunay on a traced array under jit

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

The `slam_source_pix_nn` cell cannot run under Nautilus JAX vmap. It raises
`jax.errors.TracerArrayConversionError`: `scipy.spatial.Delaunay.__init__`
(`scipy/spatial/_qhull.pyx:1874`) is called on a traced `float64[1500,2]`,
traced from `autofit/non_linear/fitness.py:205`.

Call site is `PyAutoArray/autoarray/inversion/mesh/interpolator/sibson.py:555`
(`from scipy.spatial import Delaunay`). The sibling interpolators already
solve this: `interpolator/delaunay.py:170` carries a JAX/NumPy point-location
routine replacing `Delaunay.find_simplex`, and `mesh/mesh/knn.py:103`
documents itself as the variant "that avoids the scipy.spatial.Delaunay
callback". Sibson has no jit-safe route.

EVIDENCE: RAL job 340210 tasks 5 and 6 (2026-08-25) died after ~52 s each,
costing 2 of the 11 InferenceRefs_v1 reference baselines
(autolens_profiling#161). Plain `delaunay_nn` reference rows completed
normally in the same array (3230 s, logZ 30591.09), so the failure is specific
to the composition that routes through Sibson.

FIX: give the Sibson path a jit-safe construction, following whatever
`interpolator/delaunay.py` does, or make the incompatibility explicit at
model-build time instead of at first traced call. Confirm which of the two
sibling routes is the right template before implementing.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p2.md -->
