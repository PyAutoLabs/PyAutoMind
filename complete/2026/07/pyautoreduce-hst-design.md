## pyautoreduce-hst-design
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/1 (open — close offer pending)
- completed: 2026-07-08
- prs: none (new repo, direct-to-main per approved plan; commits b9d1d77..160d240)
- notes: |
    PyAutoReduce conceived, bootstrapped and design-validated in one day.
    Repo + autoreduce skeleton (stage subpackages, instruments/ adapter
    boundary, numpy-only tests) + registered in repos.yaml. Design doc A
    (HST/ACS: defaults-first deviation table, Bayer noise recipe + R,
    3-tier PSF w/ drizzled-PSF invariant, download->reduce->evict cache,
    pixfrac/kernel as user-facing dials) + roadmap skeleton (WFC3/JWST/
    _flt products). Spike reduced slacs0008-0004 from MAST end-to-end:
    units e-/s confirmed (data ratio 0.934), legacy noise consistent with
    R=1.364 applied (0.678*R=0.924~data ratio), ~7% scale offset -> phase-1
    acceptance item. Literature: SLACS V used NO drizzle (bilinear ACSPROC
    + L.A. Cosmic + TinyTim); pixfrac spans 0.6-1.0 across follow-ups.
    Env: reduction stack in ~/venv/PyAuto under constraints (user rule).
    Follow-up filed: feature/pyautoreduce/hst_acs_phase1.md (single prompt).
    Deferred: PyAutoBrain WORKFLOW.md table regen (checkout parked on
    clone-mitosis-agent branch).
