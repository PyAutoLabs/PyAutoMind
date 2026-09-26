# RAL PyAuto venv: third-party packages below the library floors (anesthetic, dynesty, psutil, tfp-nightly)

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_profiling
Themes:
- hpc
- dependencies
- reproducibility
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: `pip freeze` in the RAL venv (`/mnt/ral/jnightin/PyAuto`) satisfies every floor/pin in the PyAuto* `pyproject.toml` files (PyAutoFit: `anesthetic>=2.9.0`, `dynesty==2.1.5`, `psutil==6.1.0`; PyAutoArray: `nufftax>=0.6.1,<0.7.0`, `tfp-nightly==0.26.0.dev20260713`), and the RAL sync check reports a floor violation when one is reintroduced.
Review-minutes: 5
Epic: interferometer-likelihood-campaign

Source: autolens_profiling#308 phase B (`results/notes/interferometer_mge_breakdown_2026_09.md`,
"nufftax 0.6.1 only").

## Why

The RAL "libs in sync" check compares library git hashes only. Phase B found the shared
venv on nufftax 0.4.0 (floor 0.6.1), which silently routed large GPU NUFFTs to float32
Pallas kernels (type-2 rel err 1.05e-4 vs 2.9e-13) and invalidated a whole round of A100
jobs (351055-351057). The human upgraded nufftax on 2026-09-25; the same audit showed
anesthetic, dynesty, psutil and tfp-nightly also off their PyAutoFit/PyAutoArray pins.
Re-read the installed versions with `pip freeze` before acting.

## What

- Bring the RAL venv's third-party packages to the library pins (human runs the install;
  RAL SSH is laptop-only).
- Extend the RAL sync check (`HPCPullPyAuto` / Heart) to diff `pip freeze` against the
  PyAuto* dependency floors and pins, not only library hashes.

<!-- filed from autolens_profiling#308 phase C (PR #312), 2026-09-26 -->
