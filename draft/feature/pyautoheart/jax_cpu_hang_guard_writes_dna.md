# Heart guard: run the XLA:CPU hang reproducers on every allowed jax version and write DNA records

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoDNA
- autolens_profiling
Priority: medium
Consequence: glance

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
The deadlock recurred five times because test-mode smokes never call a compiled likelihood enough times, and the 0.11.2 hang is invisible on big nodes (16 cores: 0/25) but certain at 4 cores (25/25).

## What
A scheduled Heart check: for each jax version the PyAutoNerves requirement allows, run autolens_profiling scripts/misc/jax_version_policy (hang_case.py on the exported modules + fft) for 300 calls pinned to 4 cores, then `dna import-matrix` the rows as PyAutoHeart (or PyAutoDNA research) validation records so the DNA board's JAX CPU policy panel and its yellow "hanging setup" item stay current. Exported modules must be re-exported with the oldest allowed jax (0.9.2 could not read 0.11.2 exports).

## Human decisions (2026-11-12, plan approved; paused before any code for the autonomy focus)

- **DNA write path:** Heart's run uploads the JSONL rows and fires `repository_dispatch` to a
  NEW PyAutoDNA workflow (`ingest-hang-guard`), which downloads them, runs
  `dna import-matrix`, re-renders the board and commits. Writes stay inside DNA; DNA has no
  schedule (its AGENTS.md rule).
- **Cadence:** weekly (Mondays, alongside workspace-smoke), plus whenever PyAutoNerves' jax
  requirement or the set of jax releases it allows changes. Implement it as a cheap daily
  fingerprint job that triggers the full run only on a change or on Monday.
- **Plan:** phase 1 = Heart `jax-hang-guard.yml` on a 4-core runner. Enumerate every PyPI jax
  release inside Nerves' `jax` specifier (today 0.12.0, 0.12.0.1); one throwaway venv each;
  re-export the modules with the OLDEST allowed jax; read autolens_profiling
  `scripts/misc/jax_version_policy` at main (read-only, record its SHA; no claim needed);
  `run_matrix.py --flags none --cases fft,lapack,export:<4 modules> --calls 300`; any hang =
  red + Heart finding. Phase 2 = `library:` Delaunay cells via `--shadow`.
- **Tier:** judge (glance declared, no Witness). Merge mode: human /prm, authorized "/prm when green".
