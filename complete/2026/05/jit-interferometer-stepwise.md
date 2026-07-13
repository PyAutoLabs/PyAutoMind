## jit-interferometer-stepwise
- issue: none — direct followup to autolens_workspace#120
- completed: 2026-05-14
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/61
- repos: autolens_workspace_developer
- notes: Phase 2 of the datacube roadmap. Upgraded jax_profiling/jit/interferometer/delaunay.py (~604 → ~1100 lines) to step-by-step parity with the imaging sibling jax_profiling/jit/imaging/delaunay.py. 8 per-step JIT timings entries (imaging-sibling numbering preserved for cross-reference; lens-light steps 3-4 dropped): ray-trace data grid, ray-trace mesh grid, inversion setup (steps 5-8 combined incl. NUFFT), data vector D (vis-space real+imag), curvature matrix F (real+imag summed), regularization matrix H (ConstantSplit), reconstruction (NNLS), mapped recon + log evidence (vis-space χ²). Step-by-step total 0.298s, full-pipeline JIT 0.316s (5% XLA cross-step fusion gap). Correctness: per-step log_evidence from inversion matrices matches FitInterferometer.log_evidence exactly; full-pipeline JIT matches eager at rtol=1e-4; eager + full-pipeline regression assertions against EXPECTED_LOG_EVIDENCE_SMA = -3167.5258928840763 still pass. Prereq for the future jit/datacube/delaunay.py profiler (Phase 3).
