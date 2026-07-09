# FactorGraphModel per-type visualize_combined dispatch

Type: refactor
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

FactorGraphModel.visualize_combined (autofit/graphical/declarative/collection.py) routes EVERY factor into
the lead factor's Visualizer.visualize_combined — mixed-dataset graphs (AnalysisImaging + AnalysisWeak,
first built by the weak series step 8) crashed until PyAutoLens's visualizers grew type filters
(PyAutoLens#587). Fix the producer: group model_factors by their analysis Visualizer class and call each
group's visualize_combined once with that group's factors and the matching sub-instances. Homogeneous
graphs must produce byte-identical behaviour (single group == today's call). The PyAutoLens type filters
stay as defence in depth. Unit test with two stub Visualizer classes recording their calls.
