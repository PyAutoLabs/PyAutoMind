# Flagship 'PyAutoLens for LensTool users' example on real cluster data (SMACS J0723)

Type: docs
Target: cluster
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Flagship "PyAutoLens for LensTool users" end-to-end cluster example on real data, reproducing a published LensTool model as closely as possible.

Most cluster strong-lensing modelers use LensTool. A workspace example that says "if you use
LensTool, this script does the same thing in PyAutoLens" — same profile (dPIE), same scaling
relation convention, same multiple-image positional likelihood, on real public data with a
published LensTool model to compare against — would be extremely valuable for adoption.

Candidate cluster: **SMACS J0723.3-7327** (the first JWST cluster). It is relatively regular
(single BCG), has public HST (RELICS) + JWST imaging, and has multiple published LensTool models
with parameter tables to reproduce and compare against: the RELICS/Sharon HST model (Mahler et al.,
arXiv:2208.08483; model products public on MAST via doi:10.17909/T9SP45), Mahler et al. 2022
(arXiv:2207.05007, HST model with MUSE spectroscopic redshifts), and Caminha et al. 2022.
Alternatives if SMACS0723 proves too complex: a relaxed CLASH cluster (e.g. Abell 383, Richard et
al. 2011) or a group-scale lens; final choice is part of this task — criteria are: few multiple-image
families (~5), spectroscopic redshifts available, published LensTool parameter table, public imaging.

The example should:
- Ingest the published multiple-image catalogue (positions + redshifts) via the cluster CSV API
  (point_datasets.csv), and the cluster-member catalogue into scaling_galaxies.csv.
- Compose the same mass model as the published LensTool work: cluster-scale dPIE halo(s) + BCG +
  scaling-relation members (LensTool convention: fixed exponents, reference-anchored normalization,
  r_cut scaling), using the LensTool-native dPIE parameterization (from_lenstool conversion).
- Fit with the source-plane chi^2 (LensTool's default) and show the image-plane chi^2 as the
  rigorous upgrade, with prose mapping every PyAutoLens concept to its LensTool equivalent
  (.par file section -> CSV row / model component; sigma,r_core,r_cut -> b0,ra,rs; image-plane vs
  source-plane optimization; Bayesian evidence vs chi^2/RMS).
- Compare recovered parameters and image-position RMS against the published LensTool values, and
  state honestly where conventions prevent exact parity.

Location: `autolens_workspace/scripts/cluster/` (e.g. `lenstool.py` or a `lenstool/` subfolder if
the data-prep stage warrants a second script). Real-data download/prep must be reproducible
(documented MAST fetch or a packaged dataset under `autolens_workspace/dataset/cluster/`).

Depends on: the dPIE LensTool parameterization/parity prompt and the scaling-relation
reparameterization prompt. There is a real prospective user available for back-and-forth beta
testing once a draft exists — plan for an iteration loop with them.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/p3_lenstool_example.md -->
