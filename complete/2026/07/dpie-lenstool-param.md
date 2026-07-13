## dpie-lenstool-param
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/485 (closed)
- completed: 2026-07-09
- prs: PyAutoGalaxy#487 + PyAutoLens#576 + autolens_workspace_test#151 (all merged)
- notes: Lenstool-native dPIE parameterization, end to end. Conventions verified against the
  Lenstool C source (shallow clone of git-cral): b0 = 6·(648000/c²)·σ_LT²·(D_LS/D_S) with σ_LT
  the fiducial v_disp (σ0 = √(3/2)σ_LT trap documented loudly); .par ellipticite = (a²−b²)/(a²+b²)
  → epot = (1−q)/(1+q) = |ell_comps| (set_lens.c conversion); rc/rcut ↔ ra/rs one-to-one.
  Shipped from_lenstool classmethods + dPIEMassLenstool/Sph wrapper profiles (model-fitting in
  Lenstool parameters — user-directed mid-run scope addition; angle arg renamed angle_pos after
  colliding with EllProfile.angle()). Two correctness fixes surfaced by parity work:
  (1) dPIEMass.potential_2d_from was an MGE approximation 6–15% off vs ci05f deflections for
  elliptical profiles — replaced with the analytic KK93 I0.5 potential ported from Lenstool pi05
  (e_pcpx.c), ∇ψ now matches deflections to 1.7e-8; (2) _ellip() min-clamps at 1e-5 (Lenstool
  set_lens.c identical), fixing NaN deflections at ell_comps=(0,0). 6-leg parity script in
  workspace_test (1e-7–1e-10) incl. a .par recipe for true-Lenstool reference regeneration.
  Gotchas: analytical_hessian_2d_from is profile-frame (det/magnification rotation-invariant,
  documented); cluster start_here/modeling are NOT smoke-able (>500s TEST_MODE even on main,
  control-verified — memory saved); prior configs must accompany new model-fittable profiles.
  Foundation for docs/cluster/8_lenstool_users_example.md.
