## docs-mass-rst-sync
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/519
- completed: 2026-05-18
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/520
- repos: PyAutoLens
- notes: Pure rST docs sync — brought PyAutoLens/docs/api/mass.rst into line with the al.mp.* / al.lmp.* / al.lmp_linear.* namespaces it documents. Added missing entries to Total (dPIE family), Mass Sheets (ExternalPotential), Stellar (GaussianGradient, SersicCore*), Dark (cNFW family, virial-mass variants). Moved PointMass out of Total into a new Point Mass section that also lists SMBH / SMBHBinary. Added two new sections at the bottom: Stellar Light+Mass [ag.lmp] and Linear Light+Mass [ag.lmp_linear]. No Python code touched. Surfaced as follow-up while writing the autolens_workspace mass / light+mass guides (#178 / #180).

## Original prompt

Sync `PyAutoLens/docs/api/mass.rst` to cover every exported `al.mp.*`
class and add documentation sections for `al.lmp.*` and
`al.lmp_linear.*`. Surfaced as a follow-up while writing the
`scripts/guides/profiles/{mass.py,light_and_mass_profiles.py}` guides
(issues #178 / #180) — both guides reference the published API
reference URL, so the reference itself should list every class the
guides demonstrate.

Gaps to fix in the existing sections:

- Total: add `dPIEMass`, `dPIEMassSph`, `PIEMass`, `dPIEPotential`,
  `dPIEPotentialSph`.
- Mass Sheets: add `ExternalPotential` (the recently merged
  line-of-sight potential).
- Stellar: add `GaussianGradient`, `SersicCore`, `SersicCoreSph`.
- Dark: add `cNFW`, `cNFWSph`, `cNFWMCRLudlow`, `cNFWMCRLudlowSph`,
  `cNFWMCRScatterLudlow`, `cNFWMCRScatterLudlowSph`,
  `gNFWVirialMassConcSph`, `gNFWVirialMassgNFWConcSph`,
  `NFWVirialMassConcSph`.

New sections to add:

- `Point Mass [ag.mp]` — `PointMass`, `SMBH`, `SMBHBinary`.
- `Stellar Light+Mass [ag.lmp]` — every class in
  `autogalaxy.profiles.light_and_mass_profiles`.
- `Linear Light+Mass [ag.lmp_linear]` — every class in
  `autogalaxy.profiles.light_linear_and_mass_profiles`.

Pure rST docs change — no Python code touched. PyAutoGalaxy has no
`docs/api/mass.rst` so the sync is one-way (PyAutoLens only).
