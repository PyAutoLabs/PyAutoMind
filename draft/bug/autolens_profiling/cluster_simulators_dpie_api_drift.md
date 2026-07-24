# cluster/group simulators broken by dPIE Lenstool-default swap (#506)

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised

Found by the #84 restructure gates (2026-07-24), reproducible on main:
scripts/misc/simulators/{cluster,group}.py call
al.mp.dPIEMassSph(ra=, rs=, b0=) — the pre-#506 signature. Installed
signature is (centre, sigma, r_core, r_cut, redshift_object,
redshift_source, H0, Om0) (dPIE Lenstool-default swap, PyAutoLens#506
MERGED). Blocks any full cluster-family profiling run (auto-simulate
invokes the simulator, which crashes). Fix: port the two simulators to
the new parameterisation, preserving the intended physical setup
(convert ra/rs/b0 to sigma/r_core/r_cut equivalents — see the #506 PR
for the mapping); then a full cluster smoke-run (the #84 gate that was
blocked) verifies. Also blocks the parked group4 GPU runs if their
simulator path hits the same signature — check simulators/group4_mge.py.
