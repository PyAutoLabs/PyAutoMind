# Cluster scaling relation: LensTool convention (reference-anchored, fixed exponent, r_cut scaling)

Type: feature
Target: cluster
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Reparameterize the cluster scaling-relation tier to the LensTool / referee-endorsed convention: reference-anchored normalization, fixed exponent, and truncation-radius scaling.

Current state (`autolens_workspace/scripts/cluster/modeling.py` + `start_here.py`, and
`scripts/group/features/scaling_relation/`): each scaling-tier member gets
`b0 = scaling_factor * luminosity ** scaling_exponent` with `scaling_factor ~ U(0,1)` and
`scaling_exponent ~ U(0,2)` both free, while `ra` and `rs` are held fixed for the whole tier.

A referee/collaborator comment on a paper using this parameterization is correct about standard
practice, and the workspace should move to it:

1. **Anchor the normalization to a reference galaxy** (BCG/BGG or L*): parameterize
   `b0_i = b0_ref * (L_i / L_ref)^beta` so the free parameter is the Einstein-radius-like strength
   of the reference galaxy — physically interpretable, easy to set a prior range on, and
   dimensionally clean (the current `scaling_factor` has units arcsec/L^beta that change with beta).
2. **Fix beta by default.** LensTool convention derives from Faber-Jackson:
   sigma_0 = sigma_0* (L/L*)^(1/4), and since b0 ∝ sigma^2 this gives beta = 0.5 for b0.
   Default beta fixed at 0.5, with prose explaining it can be freed or set from fundamental-plane /
   velocity-dispersion fits.
3. **Scale the truncation radius too**: LensTool scales r_cut = r_cut* (L/L*)^(1/2) (and r_core
   similarly, though r_core is usually fixed negligible). Currently `rs` is fixed at 10.0" for the
   whole tier — add `rs_i = rs_ref * (L_i/L_ref)^0.5` with `rs_ref` free or fixed, documented.

Scope: update `scripts/cluster/modeling.py`, `scripts/cluster/start_here.py`,
`scripts/cluster/simulator.py` (truth relation should be generated in the new convention so
recovered parameters are interpretable), `scaling_galaxies.csv` schema if needed (a reference-galaxy
row or normalization column), and the group-scale feature docs
`scripts/group/features/scaling_relation/modeling.py` + `modeling_for_luminosities.py` prose so both
tiers tell the same story. Keep the old free-(alpha, beta) form documented as an option — it is
mathematically equivalent for alpha and some users will want beta free — but the default and the
tutorial prose should follow the LensTool convention. Note the luminosity input convention: papers
often compute L from the MGE decomposition (L = sum_i 2*pi*sigma_i^2 I_i / q_i); the prose should
state luminosities are relative (only L_i/L_ref matters), which sidesteps unit questions.

Depends on nothing; should land before the "PyAutoLens for LensTool users" flagship example, which
will use this convention.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/p2_scaling_relation_lenstool.md -->
