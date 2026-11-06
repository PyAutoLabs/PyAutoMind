## cti-five-failing-scripts
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/45
- completed: 2026-11-06
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/46

Merged 2026-11-06 by glance-tier auto-merge (plan approved by the human; Heart STALE "release validation stale: source moved since rehearsal (PyAutoNerves)" acknowledged by the human). Issue #45 closed. cti-upkeep phase 3.

Root causes, found by re-running from a fresh clone in dependency order (the 11-05 triage table was partly wrong):
- `dataset_1d/advanced/temporal/{database,plot}.py`: each fit is a FactorGraphModel, so `samples.max_log_likelihood()` / `median_pdf()` / `errors_at_*_sigma()` return a ModelInstance with entries `0..3` plus `factor`. Take `[0]` (the shared `cti` and `time`), as `fit.py` does with `result_list[0].instance`. `agg.values("samples")` returns only the 5 top-level fits; the "25 fits" log line is the sub-fit scrape.
- `plot/diagnostics/imaging_ci/well_filling.py`: `float()` on a 1-element binned EPER array (NumPy 2 refuses it) → `[0]`. Not arcticpy-related. The file is CRLF.
- `imaging_ci/advanced/chaining/noise_scaling.py`, four layered bugs: dataset path `poisson/simple/` → `poisson/`; `set_noise_scaling_map_dict()` was removed in PyAutoCTI 96f958ce, so assign `dataset.noise_scaling_map_dict`; `Result.noise_scaling_map_dict` fits `analysis.dataset_full`, so pass the already-built `imaging_ci_full_list`; under profile_release, visualization fits dataset_full with hyper noise, so the maps go on the full datasets too.
- `plot/fpa/imaging_ci/database.py`: the PIXSCAY KeyError did NOT reproduce once its simulator and fit ran first. It was a triage artefact.
- The temporal/plot.py "SQLAlchemy error" is a re-run-only bug: under test mode the DB lives at `output/test_mode/<name>.sqlite`, but the scripts delete `output/<name>.sqlite`. Filed as `draft/bug/autocti_workspace/database_scripts_stale_sqlite_under_test_mode.md` (6 scripts).

Evidence: smoke_tests.txt 36 → 44. Fresh clone profile_smoke 44/44 (573 s); profile_release 43/44, the noise_scaling full-dataset failure fixed (f00ade8) and re-run green under both; PR CI smoke 3.12/3.13 + navigator green. Four notebooks regenerated with `generate.py autocti`.

Cost: the plot/fpa/imaging_ci chain adds about 230 s (smoke) / 430 s (release; fit alone 296 s), kept because the Witness requires it: a /ci_speedup candidate.

## Original prompt

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
Issued: 2026-11-06

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
