# autocti_workspace: five scripts fail on current main (from the 3a smoke triage)

Type: bug
Target: autocti_workspace
Repos:
- autocti
- autocti_workspace
Themes:
- cti
- smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: each of the five scripts below runs end-to-end under `config/build/profile_smoke.yaml` from a fresh clone, run after its producer scripts in dependency order (simulator → fit → database → plot); each is then added to `smoke_tests.txt` in its group, and CI smoke stays green.
Review-minutes: 5
Unattended: ready
Epic: cti-upkeep
Phase: 3
Filed: 2026-11-05

Found by the cti-upkeep 3a triage on 2026-11-05 (autocti_workspace#43). The 79 scripts were run under
profile_smoke against PyAutoCTI main 804ddebd, in dependency order. These five fail for reasons other
than ordering:

| script | error |
|---|---|
| `plot/fpa/imaging_ci/database.py` | `KeyError: "Keyword 'PIXSCAY' not found."` (FITS header read on the database-loaded dataset) |
| `plot/diagnostics/imaging_ci/well_filling.py` | `TypeError: only 0-dimensional arrays can be converted to Python scalars` |
| `dataset_1d/advanced/temporal/database.py` | `AttributeError: 'ModelInstance' object has no attribute 'time'` (likely the FactorGraphModel instance structure; see complete/2026/11/cti-database-examples-drift.md) |
| `dataset_1d/advanced/temporal/plot.py` | SQLAlchemy error (https://sqlalche.me/e/20/gkpj), probably downstream of the database.py failure |
| `imaging_ci/advanced/chaining/noise_scaling.py` | `FileNotFoundError: dataset/imaging_ci/poisson/simple/norm_100/data.fits`; no simulator writes that path (`simulators/examples/poisson_traps.py` writes elsewhere) |

Speed note (not a failure): `imaging_ci/simulators/overview/non_uniform_cosmic_rays.py` takes ~200–430 s,
which keeps it and `overview/overview_4_charge_injection_data.py` (which calls it) out of smoke. A faster
simulation (smaller frame or fewer cosmic rays under test mode) would let both be promoted.
