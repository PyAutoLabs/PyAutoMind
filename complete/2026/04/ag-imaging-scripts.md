## ag-imaging-scripts
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/10
- completed: 2026-04-26
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/367
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/11
- notes: Ports four imaging integration tests from autolens_workspace_test/scripts/imaging/ to single-galaxy autogalaxy (model_fit, visualization, visualization_jax, modeling_visualization_jit). Library side: ag.AnalysisImaging.__init__ had a custom signature that didn't forward **kwargs, breaking AnalysisImaging(use_jax_for_visualization=True) — fixed by adding **kwargs forwarding (mirrors al.AnalysisImaging which inherits from AnalysisDataset directly). Smoke side: PYAUTO_FAST_PLOTS=1 skipped savefig and broke visualization.py's file-existence assertions; first attempt was os.environ.pop in the script (user pushed back), correct fix is a per-pattern unset in config/build/env_vars.yaml — saved to memory.
