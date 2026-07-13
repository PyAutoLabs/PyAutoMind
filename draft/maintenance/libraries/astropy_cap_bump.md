# Bump astropy cap to allow 8.x (drop the stale `<=7.2.0`)

Type: maintenance
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Filed 2026-07-12 from a `/hygiene deps` audit.

## Why

`astropy` is capped at `>=5.0,<=7.2.0` in both **PyAutoArray** and
**PyAutoGalaxy** `pyproject.toml`. The cap is demonstrably too tight: the
development venv already runs **astropy 8.0.1** with the full stack passing, and
PyPI latest is 8.0.1. A fresh `pip install` today would *downgrade* astropy to
7.2.0 because of the cap. This is the clearest stale cap in the audit — the
installed environment is the proof it works.

## Scope

- Raise the astropy cap in `PyAutoArray/pyproject.toml` and
  `PyAutoGalaxy/pyproject.toml` from `<=7.2.0` to admit 8.x (e.g.
  `>=5.0,<9.0` or `>=5.0,<=8.0.1` — pick per the repo's cap convention).
- Keep the two repos' astropy specifiers **consistent** (they match today; the
  audit found no cross-repo conflict — don't introduce one).
- No source changes expected; astropy 8 already imports and runs in the venv.

## Verify

- Library-first ship: PyAutoArray then PyAutoGalaxy (Galaxy inherits Array).
- Smoke: an imaging fit that touches astropy (WCS / units) still runs.
- Confirm a clean-venv resolve pulls astropy 8.x, not 7.2.0.

## Out of scope (recorded, not this task)

Other stale caps from the same audit — route separately if wanted: scipy
`<=1.17.1`→1.18.0, scikit-learn `<=1.8.0`→1.9.0, xxhash `<=3.4.1`→3.8.1
(Tier 1); networkx `==3.1`→3.6.1, psutil `==6.1.0`→7.2.2, corner
`==2.2.2`→2.3.0, nufftax `<0.5.0`→0.6.1 (Tier 2). Tier-4 sampler pins
(dynesty/nautilus/zeus/getdist/colossus) intentionally left alone.
