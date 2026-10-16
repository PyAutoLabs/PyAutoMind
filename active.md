
## search-ext-b5c2a-freeze
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/17
- issued: 2026-10-16
- prompt: active/search_ext_b5c2a_pilot_judge_freeze.md
- status: PR-open 2026-10-16 (autofit_inference#18, PyAutoCortex#71, PyAutoInsight#34; CI green; correlated_nd@2 frozen in 44c5e77f1fb0; awaiting human /prm in that order)
- session: Claude Code CLI (Fable 5.1); plan approved in-chat 2026-10-16 (two phases, 2a now; present-and-wait, not --auto); execution delegated to an Opus worker
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5c2a-freeze
- repos:
  - autofit_inference: feature/search-ext-b5c2a-freeze
  - PyAutoInsight: feature/search-ext-b5c2a-freeze
  - PyAutoCortex: feature/search-ext-b5c2a-freeze
- classification: research (autofit_inference primary; PyAutoCortex ledger, PyAutoInsight task row), Consequence judge, Autonomy supervised; Feature Agent: split-into-phases — 2a judge+calibrate+A2+freeze (no compute), 2b `draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md` (realisations 2–3 + submit)
- suggested-branch: feature/search-ext-b5c2a-freeze
- epic: search-extensibility
- heart-at-door: STALE 2026-10-16 (Release STALE; monitoring RED 28/100) — continue per start_dev 0a; no override needed
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/18
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/71
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/34
- decision-taken: A2 memory headroom 2x (--mem = max(8 G, ceil(2 x peak)), peak = 8 G for an OOM class): d50 Nautilus n_live_400 16 G, d100 cold NUTS 17 G — revert: change MEMORY_HEADROOM in calibrate_correlated_nd.py and regenerate
- decision-taken: d100 Nautilus n_live_200 (and n_live_100/400, d100 warm NUTS) deferred from the scored menu — 40/40 n_live_200/400 attempts failed at the pin before sampling (nautilus HDF5 checkpoint, D = 100), affordability unmeasured — revert: drop from _correlated_nd.A2_DEFERRED by a later amendment after a fix
- decision-taken: OOM cells d50 Nautilus n_live_100 and d50 warm NUTS deferred by the cap rule read as "no attempt ended on its own" (9 at cap + 1 oom each) — revert: cap rule = every attempt Terminated at the cap (cells become probe-first)
- decision-taken: σ-ratio bands per task under @2 (evidence [0.85, 1.1] on 79 rows; posterior kept [0.5, 2.0], 1 row < 20) — revert: one band for both tasks (would flip 34 accepted pilot NUTS rows)
- decision-taken: evidence calibration set also requires §4(c) (excludes 6 collapsed banana Nautilus rows that would drag the band to 0) — revert: drop the (c) filter in calibrate_correlated_nd.calibrate
- decision-taken: new oom attempt class; the 4 OOM cap stubs rewritten from sacct; @2 reruns an oom run once at 2x memory — revert: git revert the reconcile commit 31ba4a6
- decision-taken: harness fix in 2a — chain diagnostics no longer relabel correlated_nd (all 80 Emcee/Zeus pilot rows had failed on 'g0.centre'); those 8 cells probe-first — revert: revert the _posterior/_runner hunks of b3845e8
- compute: nothing submitted in B5c-2a; RAL 410866 results/ pulled (930 rows, per-dataset tar) from the private copy /mnt/ral/jnightin/inference/autofit_inference_b5c into the worktree autofit_inference results/searches/ (committed on feature/search-ext-b5c2a-freeze, autofit_inference#18), sacct extract at results/accounting/correlated_nd_pilot_sacct.tsv; private copy left as is; B5c-2b inputs in results/calibration/correlated_nd_wave1.json (timeouts, probe_first, scored_deferred, memory_raised_gb)

## direct-conv-symmetric
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/635
- issued: 2026-10-16
- prompt: active/direct_conv_symmetric_row_restriction.md
- status: library-dev
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/direct-conv-symmetric
- repos:
  - PyAutoArray: feature/direct-conv-symmetric
- classification: feature (PyAutoArray primary; write-up phase autolens_profiling + PyAutoPulse after library), Consequence glance, Autonomy supervised; serial numba only (human: Nautilus-level parallelism); campaign PyAutoPulse#62
