# autofit_assistant: the deferred skill tranche (chain/custom/simulate/plot/debug)

Type: feature
Target: PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Author the deferred autofit_assistant skill tranche (deferral human-approved 2026-07-10 on autofit_assistant#1): af_chain_searches (prior passing / start points, grounded in autofit_workspace scripts/searches/start_point.py), af_custom_analysis (Analysis subclass patterns beyond plain wrapping: custom Result/visualization hooks, grounded in cookbooks/analysis.py), af_simulate_dataset (simulate 1D/user-model data for testing, grounded in scripts/simulators), af_plot_fit (autofit.plot + matplotlib-over-instances conventions, grounded in cookbooks and plot scripts), af_debug_fit_failure (triage flowchart: likelihood sanity, prior coverage, sampler diagnostics — expands af_run_search's triage section). House style per skills/_style.md; each skill's recipe must execute against the installed stack before shipping; register in skills/README.md + .claude/skills symlinks; run the four currency legs.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fe0b3759-ba31-4d76-9ce1-aefd030356bd/scratchpad/raw_skill_tranche.md -->
