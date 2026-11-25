# Likelihood lifecycle phase 5F: autolens_workspace + HowToLens: a `guides/advanced` auto-setup guide, retired stale compute-setup prose, `cpu_fast_modeling.py` as the override example, and SLaM scripts passing one setup to every stage

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- HowToLens
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/688
Consequence: judge
Witness: `autolens_workspace/scripts/guides/advanced/auto_setup.py` exists (with its generated notebook) and explains, runnable in test mode:
- what `setup="auto"` decides (backend, device, operator, precision, transformer, threads, `number_of_cores="auto"`) and what it never decides (model, sampler, HPC request);
- the per-dataset table of designated setups (CPU vs A100);
- the three terminal lines printed at fit start (Setup / Parallel / Estimate) and how to read them, including "extrapolated" and "uncalibrated";
- how to override (`setup=aa.Setup(...)`, a setup_id string, `PYAUTO_SETUP`);
- the lazy sparse operator for calculations outside modeling (`lazy_sparse_operator`);
- `setup.json` / `parallel.json` and aggregator reloads;
- factor graphs (one shared setup).

It is linked from `guides/advanced/README.md` and the modeling start-here guide. Stale prose that hand-sets `use_jax` / `apply_sparse_operator` / cores for speed is retired or points to the guide. `cpu_fast_modeling.py` becomes the explicit-override example, and the `example_cpu_and_gpu.py` contradiction is fixed. The SLaM workspace scripts build one setup (or apply it to the dataset once) and pass it to every stage (5C design call 4). HowToLens gets a concise CLI explanation where it introduces running a fit. Workspace smoke passes.
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5A–5E MERGED (PyAutoNerves#223; PyAutoArray#709, #710, #712; PyAutoGalaxy#752, #753; PyAutoLens#882, #886, #888; PyAutoFit#1795, #1796; autolens_profiling#535). The workspace ships after the libraries are released, or against source main (library-first gate). The concise CLI banner polish (if approved as a library fix) lands first, so the guide shows the final output.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25

## Context

- **Report §4 Phase 5, 5F:** "autolens_workspace + HowToLens (stale prose retired; `cpu_fast_modeling.py` becomes the override example; `example_cpu_and_gpu.py` contradiction fixed; concise CLI explanation)". The 5C design call 4 put the SLaM one-setup change here.
- **Human 2026-11-25:** "make sure in the phasing we have a guides/advanced on this". `scripts/guides/advanced/` currently holds add_a_profile, custom_analysis, multi_plane, over_sampling, over_sampling_chaining.
- **The per-dataset designations** (setup_rules.yaml, from the 39 Pulse designations):

  | Likelihood | CPU | A100 |
  |---|---|---|
  | imaging pixelized | numba sparse | JAX dense |
  | imaging MGE | JAX CPU dense | JAX GPU dense |
  | interferometer pixelized | numba w-tilde | JAX w-tilde |
  | interferometer MGE | JAX dense NUFFT | JAX GPU dense NUFFT |
  | group / multi_galaxy / multi_dataset | as imaging | as imaging |
  | datacube | numba w-tilde | CPU row only |
  | point / cluster | JAX CPU | JAX GPU |
  | weak | JAX CPU dense | JAX GPU dense |

  All are fp64.
- **A 2026-11-25 test-mode run** of `al.AnalysisImaging(dataset, setup="auto")` + `af.Nautilus(number_of_cores="auto")` printed the Setup, Parallel and Estimate lines. They were separated by other log lines, the Setup line was verbose (rule id repeated as decision id), and a stale "Starting non-linear search with JAX (CPU: cpu)." line came before the numba setup resolved. The guide must show the output after any banner fix.
- Follow Brain `skills/WRITING_STYLE.md` and the workspace's script/notebook conventions (generate notebooks from scripts).

## Out of scope

- Library code (5A–5E are done; any banner polish is its own library fix).
- Assistant skills (5G).
- Science projects (5H).
- The default flip (R6).
