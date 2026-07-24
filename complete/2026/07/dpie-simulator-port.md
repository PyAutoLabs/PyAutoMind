## Outcome — SHIPPED + MERGED 2026-07-24 (PR #87)

Issue #86 closed. The dPIE "API drift" resolved as a pure class-name swap:
PyAutoLens#506 RENAMED the (ra, rs, b0) parameterisation to dPIEMassB0Sph
(new dPIEMassSph = Lenstool subclass converting sigma/r_core/r_cut->b0).
Identical parameters kept -> cluster data BIT-IDENTICAL, zero
re-calibration. 8 call sites ported (simulators/cluster.py x3 incl. the
af.Model mirror; likelihood_breakdown image_plane x3 + source_plane x2).
Issue premise corrected: group.py/group4_mge.py use Isothermal, never
affected — the parked group4 GPU runs are NOT blocked by this.

## Lesson
"API removed" often = "API renamed" — check for a legacy alias/renamed
class before deriving parameter conversions (the #506 diff kept the old
maths as dPIEMassB0Sph + a from_b0 classmethod).

## Verification
The #84-blocked cluster smoke gate passes end-to-end (59.7s: auto-simulate
-> fixed simulator -> both planes -> results). No hardcoded literals tied
to dPIE data anywhere (source_plane's reference LL is computed at runtime).

## Original prompt

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
