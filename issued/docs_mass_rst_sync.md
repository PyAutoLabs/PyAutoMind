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
