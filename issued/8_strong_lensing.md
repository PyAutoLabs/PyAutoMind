# Combined strong plus weak lensing example

Type: feature
Target: weak
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Combined strong plus weak lensing example. Add autolens_workspace/scripts/weak/features/strong_lensing/ with dedicated simulator.py, fit.py and modeling.py showing weak-lensing shear constraints combined with strong lens modeling of the same mass distribution — the science mode where weak shear is the extra large-radius signal around strong-lens clusters (Niemiec 2020 hybrid-Lenstool, arXiv:2002.04635) and strong-lens groups (Oguri 2012 Sloan Giant Arcs Survey, arXiv:1109.2594), not cosmic shear or galaxy-galaxy lensing. simulator.py simulates the SAME tracer into an imaging dataset (strong) and a surrounding WeakDataset shear field (weak); fit.py fits both with a shared tracer; modeling.py combines AnalysisImaging + AnalysisWeak via PyAutoFit analysis summing to show the joint fit constraining the mass profile better than either alone (parametric core + large-radius shear, the hybrid-Lenstool insight). Depends on AnalysisWeak from feature/weak/4_modeling.md.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
