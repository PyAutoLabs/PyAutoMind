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

### Q14. cti_upkeep_epic — `cti_upkeep_epic` cannot start: repo PyAutoHeart is claimed by `colab…
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: claimed
- ask: `cti_upkeep_epic` cannot start: repo PyAutoHeart is claimed by `colab_gate_colossus_rationale_is_stale_once` in active.md with no coordination line naming it.
- options: (a) wait for colab_gate_colossus_rationale_is_stale_once to ship · (b) record a coordination line · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass

### Q15. cti_upkeep_epic — `cti_upkeep_epic` is Unattended: needs-slicing, so no shift starts it.
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: unattended
- ask: `cti_upkeep_epic` is Unattended: needs-slicing, so no shift starts it.
- options: (a) make it ready (slice or size it) · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass

### Q16. cti_upkeep_epic — `cti_upkeep_epic` is Autonomy: human-required, so a shift worker woul…
- task: draft/maintenance/autocti/cti_upkeep_epic.md
- kind: ruling
- gate: human-required
- ask: `cti_upkeep_epic` is Autonomy: human-required, so a shift worker would park at ship.
- options: (a) lower it to supervised · (b) keep it for an attended session · (c) drop it from the queue
- shift: 2026-11-19-pm2
- asked: 2026-11-19T21:49Z
- worker: readiness pass

### Q17. sed_chain_waveband_fit_can_spin_forever — SED waveband hang: n_like_max=50000 already exists but caps calls, no…
- task: active/sed_chain_waveband_fit_can_spin_forever.md
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136
- kind: question
- ask: SED waveband hang: n_like_max=50000 already exists but caps calls, not time. Which cap, and who runs the RAL repro/witness?
- options: (a) (1) Wall-clock cap: PyAutoFit Nautilus timeout + pipeline constants, marker, test (recommended) · (b) (2) Pipeline only: lower n_like_max named constant + capped marker + test · (c) (3) Close as covered by SED_SKIP_BANDS gap-fill
- shift: 2026-11-20-am
- asked: 2026-11-20T08:41Z
- worker: 79ac305d

### Q18. latent_total_source_flux_jax_vs_numpy_regression — The jit-vs-NumPy total_source_flux gap no longer reproduces (green on…
- task: active/latent_total_source_flux_jax_vs_numpy_regression.md
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/137
- kind: question
- ask: The jit-vs-NumPy total_source_flux gap no longer reproduces (green on main CI 2026-11-16 and locally). How should the bug be closed?
- options: (a) Close as fixed upstream; file the hpc/sync items as their own prompt (recommended) · (b) Bisect the library commits from 09-30 to 11-16 to name the root cause, then close · (c) Keep it open; fix only the hpc/sync items under #137
- shift: 2026-11-20-am
- asked: 2026-11-20T08:43Z
- worker: 8333550b

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
