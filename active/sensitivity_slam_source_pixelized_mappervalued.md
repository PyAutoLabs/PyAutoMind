# `subhalo/sensitivity/slam_source_pixelized.py` fails on main: `al.MapperValued` no longer exists

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: awaiting-input
Issued: 2026-09-03
Consequence: glance
Witness: `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_pixelized.py` runs to completion under the smoke profile on a clean `main` checkout, and the symbol it uses for the source-plane mapper values is one the installed PyAutoLens exports.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-23 dbc63e65 (PyAutoLens), ba7f7738 (autolens_workspace)
Lane: any

Pre-existing failure observed twice while validating sibling work, both times reproduced on an
unmodified `main` checkout (control run), so neither task fixed it:

- adapt-image-snr-cap (autolens_workspace#522, record `complete/2026/09/adapt-image-snr-cap.md`)
- over-sample-snr-double-division (autolens_workspace#523, record
  `complete/2026/09/over-sample-snr-double-division.md`), smoke 31/32 with this as the one FAIL.

Failure: `AttributeError: module 'autolens' has no attribute 'MapperValued'` (6 s in under the smoke
profile). The script is not in `smoke_tests.txt`, so CI never runs it and the drift is invisible.

Ground against the installed API before editing (grep `autolens_assistant/skills/` or `dir(al)`) —
the class moved or was renamed in PyAutoArray/PyAutoLens; the sensitivity mapping's
`visualize`/`mapper_valued` block is the call site. Check the parametric sibling
`slam_source_parametric.py` too: the same record notes a separate pre-existing
`'Model' object has no attribute 'centre'` failure there.

## Answers from the human
- Q27 (2026-11-23, shift 2026-11-23-am3 question on autolens_workspace#685): use Keep the declared spherical Ludlow NFW model. Use its mass_at_200 parameter, with a fixed injection of 10⁹ solar masses and a log-uniform fit prior from 10⁶ to 10¹² solar masses, following the sensitivity start_here example's parameterization. https://github.com/PyAutoLabs/autolens_workspace/issues/685#issuecomment-7107827909
