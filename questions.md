# Questions

Parked questions from shift workers, waiting for the human (M3.5,
PyAutoBrain#645). The shift watcher adds entries through its one Mind writer;
a `/questions` chat (PyAutoBrain `skills/questions`) answers, defers or drops
them with `scripts/questions_edit.py`. Never edit by hand: the section an
entry sits under is its state, and `lifecycle.py check` validates the file.
An answer releases the parked task: the next shift resumes it with the answer
in its prompt. Kind `ruling` is filed by the readiness pass (PyAutoBrain
`batch ready`, M3.3) for a gate on a queued task: it carries `gate:`, may have
no `issue:`, never holds or releases a parked task, and answering it records
the ruling on the prompt.

```markdown
### Q<n>. <task> — <short ask>
- task: draft/<work-type>/<target>/<name>.md
- issue: https://github.com/<owner>/<repo>/issues/<n>
- kind: question
- gate: <kebab-case slug>         (kind ruling only; a ruling may have no issue:)
- ask: <one line>
- options: (a) <first> · (b) <second>
- shift: <slot>
- asked: <YYYY-MM-DDTHH:MMZ>
- worker: <session key>
```

## Open

### Q32. cluster_usability — `cluster_usability` is Unattended: needs-slicing, so no shift starts…
- task: draft/feature/autolens/cluster_usability.md
- kind: ruling
- gate: unattended
- ask: `cluster_usability` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass

### Q33. cluster_usability — `cluster_usability` is Autonomy: human-required, so a shift worker wo…
- task: draft/feature/autolens/cluster_usability.md
- kind: ruling
- gate: human-required
- ask: `cluster_usability` is Autonomy: human-required, so a shift worker would park at ship.
- options: (a) lower it to supervised · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass

### Q34. cluster_usability — `cluster_usability` has no valid Lane:, so every unattended pick fail…
- task: draft/feature/autolens/cluster_usability.md
- kind: ruling
- gate: no-lane
- ask: `cluster_usability` has no valid Lane:, so every unattended pick fails closed.
- options: (a) declare Lane: any · (b) declare a laptop lane · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass

### Q36. adaptive_rectangular_meshes_repeat_the_adapt_ima — `adaptive_rectangular_meshes_repeat_the_adapt_ima` is Unattended: nee…
- task: draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md
- kind: ruling
- gate: unattended
- ask: `adaptive_rectangular_meshes_repeat_the_adapt_ima` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass

### Q38. interferometer_adapt_image_get_the_imaging_mesh — `interferometer_adapt_image_get_the_imaging_mesh` is Unattended: need…
- task: draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md
- kind: ruling
- gate: unattended
- ask: `interferometer_adapt_image_get_the_imaging_mesh` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass

### Q42. blas_thread_oversubscription_multiprocess_searches — `blas_thread_oversubscription_multiprocess_searches` cannot start: re…
- task: draft/bug/autofit/blas_thread_oversubscription_multiprocess_searches.md
- kind: ruling
- gate: claimed
- ask: `blas_thread_oversubscription_multiprocess_searches` cannot start: repo PyAutoFit is claimed by `vmap-jit-recompiles-per-nautilus-batch-length` in active.md with no coordination line naming it.
- options: (a) wait for vmap-jit-recompiles-per-nautilus-batch-length to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-27-pm
- asked: 2026-11-27T23:49Z
- worker: readiness pass

### Q43. blas_thread_oversubscription_multiprocess_searches — `blas_thread_oversubscription_multiprocess_searches` is Unattended: n…
- task: draft/bug/autofit/blas_thread_oversubscription_multiprocess_searches.md
- kind: ruling
- gate: unattended
- ask: `blas_thread_oversubscription_multiprocess_searches` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-27-pm
- asked: 2026-11-27T23:49Z
- worker: readiness pass

### Q44. blas_thread_oversubscription_multiprocess_searches — `blas_thread_oversubscription_multiprocess_searches` is Autonomy: hum…
- task: draft/bug/autofit/blas_thread_oversubscription_multiprocess_searches.md
- kind: ruling
- gate: human-required
- ask: `blas_thread_oversubscription_multiprocess_searches` is Autonomy: human-required, so a shift worker would park at ship.
- options: (a) lower it to supervised · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-27-pm
- asked: 2026-11-27T23:49Z
- worker: readiness pass

### Q45. blas_thread_oversubscription_multiprocess_searches — `blas_thread_oversubscription_multiprocess_searches` has no valid Lan…
- task: draft/bug/autofit/blas_thread_oversubscription_multiprocess_searches.md
- kind: ruling
- gate: no-lane
- ask: `blas_thread_oversubscription_multiprocess_searches` has no valid Lane:, so every unattended pick fails closed.
- options: (a) declare Lane: any · (b) declare a laptop lane · (c) drop it from the queue
- shift: 2026-11-27-pm
- asked: 2026-11-27T23:49Z
- worker: readiness pass

## Deferred      <!-- entries add: - until: YYYY-MM-DD (absent: until the next sitting) -->

## Answered      <!-- entries add: - answered: <time> by <login> (chat|issue), - answer:, - answer-comment: <url> -->

### Q3. dataset_model_free_grid_offset_pytree_roundtrip — PyAutoFit is claimed by ep-projected-model-shared-prior (#1773). No f…
- task: active/dataset_model_free_grid_offset_pytree_roundtrip.md
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1777
- kind: question
- ask: PyAutoFit is claimed by ep-projected-model-shared-prior (#1773). No files overlap. Allow a separate worktree off main for this fix?
- options: (a) Override: separate worktree off main now (recommended) · (b) Wait until #1773 merges · (c) Drop: blocks nothing today
- shift: 2026-11-16-pm
- asked: 2026-11-16T18:38Z
- worker: b778571d
- answered: 2026-11-16T18:42Z by Jammy2211 (issue)
- answer: Use 1: (a) override — separate worktree off main for this fix alongside #1773, since no files overlap.
- answer-comment: https://github.com/PyAutoLabs/PyAutoFit/issues/1777#issuecomment-6925624924

### Q1. cluster_regime_narrative — The `features/extended_source/` example and the `autolens_workspace_t…
- task: active/cluster_regime_narrative.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/670
- kind: question
- ask: The `features/extended_source/` example and the `autolens_workspace_test` script are parked with a question on the issue (`awaiting-input`): which data, how the mass model is handed off, and whether…
- shift: 2026-11-14-pm2
- asked: 2026-11-14T17:56Z
- worker: a033837e
- answered: 2026-11-18 by Jammy2211 (chat)
- answer: Not now — cluster extended sources will not be developed for a while. The questions moved unanswered to draft/feature/workspaces/cluster_pixelized_analysisfactor.md ("Deferred"); prose half merged as autolens_workspace#671.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/670#issuecomment-6974154944

### Q8. results_library_p5c_dr1_census — `results_library_p5c_dr1_census` cannot start: repo PyAutoFit is clai…
- task: draft/feature/autofit/results_library_p5c_dr1_census.md
- kind: ruling
- gate: claimed
- ask: `results_library_p5c_dr1_census` cannot start: repo PyAutoFit is claimed by `ep-projected-model-shared-prior` in active.md with no coordination line naming it.
- options: (a) wait for ep-projected-model-shared-prior to ship · (b) record a coordination line · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T09:35Z by Jammy2211 (chat)
- answer: (b) record a coordination line: the census touches only PyAutoCortex and reads released PyAutoFit on RAL, so it shares PyAutoFit with ep-projected-model-shared-prior with no file overlap. Coordination line added to that claim in active.md.

### Q4. hpc_sync_submit_pass_time_requeue_env — `hpc_sync_submit_pass_time_requeue_env` is Unattended: never, so no s…
- task: draft/feature/autolens_inference/hpc_sync_submit_pass_time_requeue_env.md
- kind: ruling
- gate: unattended
- ask: `hpc_sync_submit_pass_time_requeue_env` is Unattended: never, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T12:14Z by Jammy2211 (chat)
- answer: (a) make it ready: slice or size it so a shift can start it

### Q6. numba_wtilde_validation_legs_stall_nautilus — `numba_wtilde_validation_legs_stall_nautilus` is Unattended: never, s…
- task: draft/research/autolens_inference/numba_wtilde_validation_legs_stall_nautilus.md
- kind: ruling
- gate: unattended
- ask: `numba_wtilde_validation_legs_stall_nautilus` is Unattended: never, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T12:14Z by Jammy2211 (chat)
- answer: (a) make it ready: slice or size it so a shift can start it

### Q9. results_library_p5c_dr1_census — `results_library_p5c_dr1_census` is Unattended: never, so no shift st…
- task: draft/feature/autofit/results_library_p5c_dr1_census.md
- kind: ruling
- gate: unattended
- ask: `results_library_p5c_dr1_census` is Unattended: never, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T12:14Z by Jammy2211 (chat)
- answer: (a) make it ready: slice or size it so a shift can start it

### Q10. results_library_p5c_dr1_census — `results_library_p5c_dr1_census` is Autonomy: human-required, so a sh…
- task: draft/feature/autofit/results_library_p5c_dr1_census.md
- kind: ruling
- gate: human-required
- ask: `results_library_p5c_dr1_census` is Autonomy: human-required, so a shift worker would park at ship.
- options: (a) lower it to supervised · (b) keep it for an attended session · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T12:14Z by Jammy2211 (chat)
- answer: (a) lower it to supervised

### Q7. hpc_campaign_epic — Epic hpc-campaign is queued but no next-phase prompt is filed (no ope…
- task: draft/research/autofit/hpc_campaign_epic.md
- kind: ruling
- gate: no-next-phase
- ask: Epic hpc-campaign is queued but no next-phase prompt is filed (no open Phase: member in draft/ or active/).
- options: (a) file the next phase's prompt · (b) close the epic · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T12:14Z by Jammy2211 (chat)
- answer: (a) file the next phase's prompt — the human asked for it to be done now

### Q11. campaign_fill_submit_without_dependency — `campaign_fill_submit_without_dependency` cannot start: repo PyAutoFi…
- task: draft/feature/autofit/campaign_fill_submit_without_dependency.md
- kind: ruling
- gate: claimed
- ask: `campaign_fill_submit_without_dependency` cannot start: repo PyAutoFit is claimed by `compound-prior-model-json` in active.md with no coordination line naming it.
- options: (a) wait for compound-prior-model-json to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-18-pm
- asked: 2026-11-18T17:32Z
- worker: readiness pass
- answered: 2026-11-18T17:44Z by Jammy2211 (chat)
- answer: (a) — the gate is clear: compound-prior-model-json shipped (PyAutoFit#1783 merged 2026-11-18T17:40Z by human /prm) and its active.md claim is released; PyAutoFit is free for this task.

### Q12. campaign_per_stage_status_root — `campaign_per_stage_status_root` cannot start: repo PyAutoFit is clai…
- task: draft/feature/autofit/campaign_per_stage_status_root.md
- kind: ruling
- gate: claimed
- ask: `campaign_per_stage_status_root` cannot start: repo PyAutoFit is claimed by `compound-prior-model-json` in active.md with no coordination line naming it.
- options: (a) wait for compound-prior-model-json to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-18-pm
- asked: 2026-11-18T17:32Z
- worker: readiness pass
- answered: 2026-11-18T17:44Z by Jammy2211 (chat)
- answer: (a) — the gate is clear: compound-prior-model-json shipped (PyAutoFit#1783 merged 2026-11-18T17:40Z by human /prm) and its active.md claim is released; PyAutoFit is free for this task.

### Q13. campaign_zip_complete_pattern — `campaign_zip_complete_pattern` cannot start: repo PyAutoFit is claim…
- task: draft/feature/autofit/campaign_zip_complete_pattern.md
- kind: ruling
- gate: claimed
- ask: `campaign_zip_complete_pattern` cannot start: repo PyAutoFit is claimed by `compound-prior-model-json` in active.md with no coordination line naming it.
- options: (a) wait for compound-prior-model-json to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-18-pm
- asked: 2026-11-18T17:32Z
- worker: readiness pass
- answered: 2026-11-18T17:44Z by Jammy2211 (chat)
- answer: (a) — the gate is clear: compound-prior-model-json shipped (PyAutoFit#1783 merged 2026-11-18T17:40Z by human /prm) and its active.md claim is released; PyAutoFit is free for this task.

### Q5. numba_wtilde_validation_legs_stall_nautilus — `numba_wtilde_validation_legs_stall_nautilus` cannot start: repo PyAu…
- task: draft/research/autolens_inference/numba_wtilde_validation_legs_stall_nautilus.md
- kind: ruling
- gate: claimed
- ask: `numba_wtilde_validation_legs_stall_nautilus` cannot start: repo PyAutoArray is claimed by `galaxy-duplicate-pytree-registration` in active.md with no coordination line naming it.
- options: (a) wait for galaxy-duplicate-pytree-registration to ship · (b) record a coordination line · (c) drop it from the queue
- shift: ready-2026-11-18
- asked: 2026-11-18T09:23Z
- worker: readiness pass
- answered: 2026-11-18T17:44Z by Jammy2211 (chat)
- answer: (a) — the gate is clear: galaxy-duplicate-pytree-registration shipped (PyAutoArray#702, completed in Mind 8918e26d2) and its active.md claim is released; PyAutoArray is free for this task.

### Q18. latent_total_source_flux_jax_vs_numpy_regression — The jit-vs-NumPy total_source_flux gap no longer reproduces (green on…
- task: active/latent_total_source_flux_jax_vs_numpy_regression.md
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/137
- kind: question
- ask: The jit-vs-NumPy total_source_flux gap no longer reproduces (green on main CI 2026-11-16 and locally). How should the bug be closed?
- options: (a) Close as fixed upstream; file the hpc/sync items as their own prompt (recommended) · (b) Bisect the library commits from 09-30 to 11-16 to name the root cause, then close · (c) Keep it open; fix only the hpc/sync items under #137
- shift: 2026-11-20-am
- asked: 2026-11-20T08:43Z
- worker: 8333550b
- answered: 2026-11-20T11:55Z by Jammy2211 (issue)
- answer: 1 — (a) close as fixed upstream; file the hpc/sync items as their own prompt
- answer-comment: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/137#issuecomment-7038440330

### Q19. slam_simultaneous_subhalo_grid_search_fits_last — SLaM simultaneous grid-search fix is blocked: SearchGridSearch over a…
- task: active/slam_simultaneous_subhalo_grid_search_fits_last.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/683
- kind: question
- ask: SLaM simultaneous grid-search fix is blocked: SearchGridSearch over a FactorGraphModel crashes in PyAutoFit make_result (KeyError). How to proceed?
- options: (a) Fix PyAutoFit first (follow-up draft queued), then resume this branch (recommended) · (b) Ship a workspace-only interim: grid search on band 0 with its dataset_model, documented as single-band · (c) Leave the stage as is with a note in the script; close #683
- shift: 2026-11-20-am
- asked: 2026-11-20T09:06Z
- worker: 24ac8476
- answered: 2026-11-20T11:56Z by Jammy2211 (issue)
- answer: 1 — (a) fix PyAutoFit first (the queued follow-up draft/bug/autofit/grid_search_factor_graph_make_result_keyerror.md), then resume branch feature/slam-simultaneous-subhalo-grid-search and open the PR
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/683#issuecomment-7038127994

### Q20. numba_wtilde_validation_legs_stall_nautilus — Phase-4 stalls explained (rectangular SMA is flat on every route; dat…
- task: active/numba_wtilde_validation_legs_stall_nautilus.md
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/73
- kind: question
- ask: Phase-4 stalls explained (rectangular SMA is flat on every route; datacube ~50% not-PD and unreproducible in-run values). Which remedy per leg?
- options: (a) Rect: raise SMA S/N + rerun both routes; Datacube: 1 CPU-h RAL worker-vs-serial test first (recommended) · (b) Rect: guard zero adapt image, record unmeasurable; Datacube: shrink mesh or raise prior floor, rerun · (c) Record both as limitations only; mark the #59 rows invalid · (d) Other (answer on the issue)
- shift: 2026-11-20-am
- asked: 2026-11-20T09:22Z
- worker: da579b3a
- answered: 2026-11-20T11:57Z by Jammy2211 (issue)
- answer: do a and d — rectangular SMA: raise the SMA cell's S/N, re-simulate and rerun the rectangular legs on both routes; datacube SMA: first run the ~1 CPU-hour controlled RAL test on current main (frozen points re-evaluated inside a Nautilus-style worker pool vs serial) before choosing a remedy
- answer-comment: https://github.com/PyAutoLabs/autolens_inference/issues/73#issuecomment-7038206561

### Q17. sed_chain_waveband_fit_can_spin_forever — SED waveband hang: n_like_max=50000 already exists but caps calls, no…
- task: active/sed_chain_waveband_fit_can_spin_forever.md
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136
- kind: question
- ask: SED waveband hang: n_like_max=50000 already exists but caps calls, not time. Which cap, and who runs the RAL repro/witness?
- options: (a) (1) Wall-clock cap: PyAutoFit Nautilus timeout + pipeline constants, marker, test (recommended) · (b) (2) Pipeline only: lower n_like_max named constant + capped marker + test · (c) (3) Close as covered by SED_SKIP_BANDS gap-fill
- shift: 2026-11-20-am
- asked: 2026-11-20T08:41Z
- worker: 79ac305d
- answered: 2026-11-20T12:05Z by Jammy2211 (issue)
- answer: 1 — (a) wall-clock cap: library-first PyAutoFit PR adding a timeout to af.Nautilus, then the pipeline PR with per-band WAVEBAND_TIMEOUT_S, a lower named WAVEBAND_N_LIKE_MAX, a capped marker, QA column and a fast test
- answer-comment: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136#issuecomment-7039080077

### Q14. cti_upkeep_epic — `cti_upkeep_epic` cannot start: repo PyAutoHeart is claimed by `colab…
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: claimed
- ask: `cti_upkeep_epic` cannot start: repo PyAutoHeart is claimed by `colab_gate_colossus_rationale_is_stale_once` in active.md with no coordination line naming it.
- options: (a) wait for colab_gate_colossus_rationale_is_stale_once to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass
- answered: 2026-11-23T09:43Z by human (chat)
- answer: (a) waited: colab_gate_colossus_rationale_is_stale_once has shipped (complete/2026/11/colab-gate-colossus-rationale-is-stale-once.md), so the PyAutoHeart claim is released and this gate no longer applies.

### Q26. sparse_terms_nufft_origin_and_mask_compatibility — Should this task include a coordinated PyAutoGalaxy PR to preserve th…
- task: active/sparse_terms_nufft_origin_and_mask_compatibility.md
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/707
- kind: question
- ask: Should this task include a coordinated PyAutoGalaxy PR to preserve the mask fingerprint through FITS reload?
- options: (a) Include PyAutoGalaxy and coordinate the reader change with the aggregator-reload task. · (b) Ship the two PyAutoArray fixes first and track the FITS round trip separately.
- shift: 2026-11-23-am3
- asked: 2026-11-23T11:37Z
- worker: codex:1b72ba278ac443b1bf858031a61c1c9a
- answered: 2026-11-23T16:59Z by Jammy2211 (issue)
- answer: go with the recommendation
- answer-comment: https://github.com/PyAutoLabs/PyAutoArray/issues/707#issuecomment-7107940971

### Q27. sensitivity_slam_source_pixelized_mappervalued — Which subhalo should the pixelized sensitivity example inject and fit?
- task: complete/2026/11/sensitivity-slam-source-pixelized-mappervalued.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/685
- kind: question
- ask: Which subhalo should the pixelized sensitivity example inject and fit?
- options: (a) Keep spherical Ludlow NFW and express the injection and fit prior using mass_at_200. · (b) Use spherical generalized NFW with the script’s explicit inner slope 2.2 and concentration 12.
- shift: 2026-11-23-am3
- asked: 2026-11-23T11:41Z
- worker: codex:b1a928033a0d472f97e99ca81604b708
- answered: 2026-11-23T16:59Z by Jammy2211 (issue)
- answer: use Keep the declared spherical Ludlow NFW model. Use its mass_at_200 parameter, with a fixed injection of 10⁹ solar masses and a log-uniform fit prior from 10⁶ to 10¹² solar masses, following the sensitivity start_here example's parameterization.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/685#issuecomment-7107827909

### Q25. pr504_sibling_guards_net_gap_proxy — Open the Lens guard PR with the two pre-existing JIT timing failures…
- task: active/pr504_sibling_guards_net_gap_proxy.md
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/369
- kind: question
- ask: Open the Lens guard PR with the two pre-existing JIT timing failures documented, or wait for the separate cache fix?
- options: (a) Open the Lens PR with both timing failures documented · (b) Wait for the separate JIT-cache fix, then rerun the scripts
- shift: 2026-11-23-am3
- asked: 2026-11-23T11:25Z
- worker: codex:6c263331ed1148a5bab5c2774723a66f
- answered: 2026-11-23T17:03Z by Jammy2211 (chat)
- answer: Open the Lens PR now and document the two existing JIT timing failures.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace_test/issues/369#issuecomment-7108088891

### Q28. smoke_cache_stats_warnings_nameerror — Should the cache-stats repair wait for the active PyAutoHeart #364 cl…
- task: active/smoke_cache_stats_warnings_nameerror.md
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/365
- kind: question
- ask: Should the cache-stats repair wait for the active PyAutoHeart #364 claim to clear, or proceed in a separate coordinated worktree?
- options: (a) Resume once #364 releases PyAutoHeart · (b) Authorize separate coordinated worktrees
- shift: 2026-11-23-am3
- asked: 2026-11-23T11:46Z
- worker: codex:5fc344efb14046e589cd52ab4d7cf254
- answered: 2026-11-23T17:03Z by Jammy2211 (chat)
- answer: Resume the cache-statistics repair once the existing PyAutoHeart #364 claim clears through the approved PR merge.
- answer-comment: https://github.com/PyAutoLabs/PyAutoHeart/issues/365#issuecomment-7108095009

### Q15. cti_upkeep_epic — `cti_upkeep_epic` is Unattended: needs-slicing, so no shift starts it.
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: unattended
- ask: `cti_upkeep_epic` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass
- answered: 2026-11-26T18:03Z by Jammy2211 (chat)
- answer: (a) make it ready: slice or size it so a shift can start it.

### Q16. cti_upkeep_epic — `cti_upkeep_epic` is Autonomy: human-required, so a shift worker woul…
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: human-required
- ask: `cti_upkeep_epic` is Autonomy: human-required, so a shift worker would park at ship.
- options: (a) lower it to supervised · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass
- answered: 2026-11-26T18:06Z by Jammy2211 (chat)
- answer: (a) lower it to supervised.

### Q21. dr1_campaign_sed_status_root — `dr1_campaign_sed_status_root` waits for draft/feature/autofit/campai…
- task: draft/feature/euclid/dr1_campaign_sed_status_root.md
- kind: ruling
- gate: blocked-by
- ask: `dr1_campaign_sed_status_root` waits for draft/feature/autofit/campaign_per_stage_status_root.md (per-stage `status_root:` must be merged into PyAutoFit first) (its Blocked-by).
- options: (a) wait for draft/feature/autofit/campaign_per_stage_status_root.md (per-stage `status_root:` must be merged into PyAutoFi… · (b) remove the Blocked-by · (c) drop it from the queue
- shift: 2026-11-20-am
- asked: 2026-11-20T09:30Z
- worker: readiness pass
- answered: 2026-11-26T18:07Z by Jammy2211 (chat)
- answer: (a) wait for campaign_per_stage_status_root; blocker promoted to #1 of the autopilot queue.

### Q22. dr1_campaign_zip_success_checks — `dr1_campaign_zip_success_checks` waits for draft/feature/autofit/cam…
- task: draft/feature/euclid/dr1_campaign_zip_success_checks.md
- kind: ruling
- gate: blocked-by
- ask: `dr1_campaign_zip_success_checks` waits for draft/feature/autofit/campaign_zip_complete_pattern.md (`zip_complete` must accept a pattern in PyAutoFit first) (its Blocked-by).
- options: (a) wait for draft/feature/autofit/campaign_zip_complete_pattern.md (`zip_complete` must accept a pattern in PyAutoFit firs… · (b) remove the Blocked-by · (c) drop it from the queue
- shift: 2026-11-20-am
- asked: 2026-11-20T09:30Z
- worker: readiness pass
- answered: 2026-11-26T18:07Z by Jammy2211 (chat)
- answer: (a) wait for campaign_zip_complete_pattern; blocker promoted to the top of the autopilot queue.

### Q23. dr1_campaign_sed_status_root — `dr1_campaign_sed_status_root` cannot start: repo euclid_strong_lens_…
- task: draft/feature/euclid/dr1_campaign_sed_status_root.md
- kind: ruling
- gate: claimed
- ask: `dr1_campaign_sed_status_root` cannot start: repo euclid_strong_lens_modeling_pipeline is claimed by `sed-waveband-search-cap` in active.md with no coordination line naming it.
- options: (a) wait for sed-waveband-search-cap to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-23-am2
- asked: 2026-11-23T09:59Z
- worker: readiness pass
- answered: 2026-11-26T18:08Z by Jammy2211 (chat)
- answer: (a) resolved: sed-waveband-search-cap shipped 2026-11-24 and its euclid pipeline claim cleared.

### Q24. dr1_campaign_zip_success_checks — `dr1_campaign_zip_success_checks` cannot start: repo euclid_strong_le…
- task: draft/feature/euclid/dr1_campaign_zip_success_checks.md
- kind: ruling
- gate: claimed
- ask: `dr1_campaign_zip_success_checks` cannot start: repo euclid_strong_lens_modeling_pipeline is claimed by `sed-waveband-search-cap` in active.md with no coordination line naming it.
- options: (a) wait for sed-waveband-search-cap to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-23-am2
- asked: 2026-11-23T09:59Z
- worker: readiness pass
- answered: 2026-11-26T18:08Z by Jammy2211 (chat)
- answer: (a) resolved: sed-waveband-search-cap shipped 2026-11-24 and its euclid pipeline claim cleared.

### Q29. multi_dataset_jax_likelihood_delaunay_wrong_likelihood — Retire the September likelihood report now that fresh main passes, or…
- task: active/multi_dataset_jax_likelihood_delaunay_wrong_likelihood.md
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371
- kind: question
- ask: Retire the September likelihood report now that fresh main passes, or provide the original inputs for a historical reproduction?
- options: (a) Retire the report · (b) Supply September g/r FITS files, stack revisions and configuration
- shift: 2026-11-24-am
- asked: 2026-11-24T08:07Z
- worker: codex:996ec11541bd477796142ec5b768b320
- answered: 2026-11-26T18:08Z by Jammy2211 (issue)
- answer: retire
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371#issuecomment-7127116263

### Q30. substructure_util_zero_padded_halo_slots_make — All four profile families pass the padded scan witness on main. Retir…
- task: draft/bug/autogalaxy/substructure_util_zero_padded_halo_slots_make.md
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/871
- kind: question
- ask: All four profile families pass the padded scan witness on main. Retire the duplicate draft or supply another failing population?
- options: (a) Retire the duplicate draft · (b) Supply a different failing population
- shift: 2026-11-24-am
- asked: 2026-11-24T08:32Z
- worker: codex:33cff8e853b042bc81657d044e7b878b
- answered: 2026-11-26T18:08Z by Jammy2211 (issue)
- answer: retire
- answer-comment: https://github.com/PyAutoLabs/PyAutoLens/issues/871#issuecomment-7127151259

### Q31. smoke_cache_stats_warnings_nameerror — see the question on the issue
- task: active/smoke_cache_stats_warnings_nameerror.md
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/365#issuecomment-7126294143
- kind: question
- ask: see the question on the issue
- shift: 2026-11-24-am
- asked: 2026-11-24T08:34Z
- worker: codex:64472140ca8443f8a5e1ce9c73f90fc7
- answered: 2026-11-26T18:08Z by Jammy2211 (issue)
- answer: resume after 369 merges (Heart#369 merged 2026-11-24T09:21Z)
- answer-comment: https://github.com/PyAutoLabs/PyAutoHeart/issues/365#issuecomment-7127183290

### Q39. group_los_halos — Group LOS halos: autolens_workspace is held by #701 (dataset FITS onl…
- task: active/group_los_halos.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/703
- kind: question
- ask: Group LOS halos: autolens_workspace is held by #701 (dataset FITS only, disjoint files). Wait for it to merge, or override the claim now?
- options: (a) Wait for #701 to merge, then build the plan in #703 as written · (b) Override the claim now (files disjoint) and build the plan · (c) Re-scope or retire the prompt (imaging half already done)
- shift: 2026-11-26-pm2
- asked: 2026-11-26T21:31Z
- worker: 1f616415
- answered: 2026-11-27T11:00Z by Jammy2211 (chat)
- answer: (a) wait for #701, then build the plan in #703 as written. #701 merged 2026-11-27T10:57Z; claim released.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/703#issuecomment-7216556772

### Q40. group_subhalo_sensitivity — Group subhalo sensitivity: autolens_workspace is held by #701, and un…
- task: active/group_subhalo_sensitivity.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/702
- kind: question
- ask: Group subhalo sensitivity: autolens_workspace is held by #701, and under smoke the Witness evidence map is all zeros. Wait or override, and accept an S/N-map Witness?
- options: (a) Wait for #701; accept the injected-signal S/N map (with vs without companions) as Witness · (b) Override the claim now; accept the S/N-map Witness · (c) Wait for #701; keep the evidence Witness, run with ENV: real_search · (d) Retire or re-scope the prompt (imaging half already done)
- shift: 2026-11-26-pm2
- asked: 2026-11-26T21:31Z
- worker: 0f971892
- answered: 2026-11-27T11:00Z by Jammy2211 (chat)
- answer: (a) wait for #701 (merged 2026-11-27T10:57Z, claim released); accept the injected-signal S/N map (with vs without companions) as the Witness.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/702#issuecomment-7216557095

### Q41. vmap_jit_recompiles_per_nautilus_batch_length — see the question on the issue
- task: active/vmap_jit_recompiles_per_nautilus_batch_length.md
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1811#issuecomment-7204076931
- kind: question
- ask: see the question on the issue
- shift: 2026-11-26-pm2
- asked: 2026-11-26T21:49Z
- worker: 04ca20f9
- answered: 2026-11-27T11:00Z by Jammy2211 (issue)
- answer: Option 1: pad in call_wrap so every batch compiles at one shape.
- answer-comment: https://github.com/PyAutoLabs/PyAutoFit/issues/1811#issuecomment-7216451269

### Q35. adaptive_rectangular_meshes_repeat_the_adapt_ima — `adaptive_rectangular_meshes_repeat_the_adapt_ima` cannot start: repo…
- task: draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md
- kind: ruling
- gate: claimed
- ask: `adaptive_rectangular_meshes_repeat_the_adapt_ima` cannot start: repo PyAutoArray is claimed by `sparse_terms_nufft_origin_and_mask_compatibility` in active.md with no coordination line naming it.
- options: (a) wait for sparse_terms_nufft_origin_and_mask_compatibility to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass
- answered: 2026-11-27T11:00Z by Jammy2211 (chat)
- answer: (a) gate cleared: sparse_terms_nufft_origin_and_mask_compatibility shipped 2026-11-27 (PyAutoArray#721), so its PyAutoArray claim is released. Recorded at /prm; the needs-slicing ruling Q36 stays open.

### Q37. interferometer_adapt_image_get_the_imaging_mesh — `interferometer_adapt_image_get_the_imaging_mesh` cannot start: repo…
- task: draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md
- kind: ruling
- gate: claimed
- ask: `interferometer_adapt_image_get_the_imaging_mesh` cannot start: repo PyAutoArray is claimed by `sparse_terms_nufft_origin_and_mask_compatibility` in active.md with no coordination line naming it.
- options: (a) wait for sparse_terms_nufft_origin_and_mask_compatibility to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-26-pm
- asked: 2026-11-26T20:56Z
- worker: readiness pass
- answered: 2026-11-27T11:00Z by Jammy2211 (chat)
- answer: (a) gate cleared: sparse_terms_nufft_origin_and_mask_compatibility shipped 2026-11-27 (PyAutoArray#721), so its PyAutoArray claim is released. Recorded at /prm; the needs-slicing ruling Q38 stays open.

## Dropped       <!-- entries add: - dropped: <date> by <login> — <why> (task shelved) -->

### Q2. markdown_regeneration_sigma_min — The human answered "do 1" (real regeneration off the laptop) at 18:32…
- task: draft/docs/autolens_workspace/markdown_regeneration_sigma_min.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/669
- kind: question
- ask: The human answered "do 1" (real regeneration off the laptop) at 18:32Z, but neither machine for option 1 can be used unattended, so the human has to choose (a) laptop GPU with them there or (b) RAL w…
- shift: 2026-11-14-pm3
- asked: 2026-11-14T20:23Z
- worker: a8222e1a
- dropped: 2026-11-16 by Jammy2211 — Lets retire this markdown feature (the human on autolens_workspace#669, 2026-11-16 09:13) (task shelved)
