# Witt–Wynne guide follow-up: broader tests + human design/example review

Type: test
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- point-source
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Filed: 2026-08-28

Follow-up to witt-wynne-projection (autolens_workspace#510): extend the Witt-Wynne SIEP projection guide (scripts/guides/misc/witt_wynne.py) with more tests, and hold a human review of the design and of the workspace example. Type: test. Target: autolens_workspace. Tests: broaden the validation grid vs PointSolver (PowerLaw slopes 1.8-2.2, axis ratios 0.5-0.95, shear 0-0.15, shear/ellipticity misaligned by 0-90 deg, sources at 0.5x/0.9x/1.02x/1.4x caustic scale, both fold and cusp approaches, high-z Euclid-like redshifts), quantify verdict-agreement rate and position/lag residuals as a function of shear-ellipticity misalignment, test the source-on-major-axis degeneracy (quartic double root) and add a guard or documented behaviour, test the .in writer round-trip against the compiled Zenodo C++ for every case, and test zero_centre exports. Human review: James reviews (a) the design choices documented in the guide's __Conventions__ section — caustic-matching vs vector-sum projection, least-squares astroid fit for e, the PA = theta_ccw + 90 map, the minus sign on shear in the vector sum, h=0.7 handling in time lags — and (b) the workspace example prose/structure as a guides/misc entry, before this is offered to Paul Schechter. Difficulty: medium. Priority: normal. Autonomy: human-required.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from user-intake -->
