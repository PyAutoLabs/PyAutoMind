# Profiling work now lives in Pulse

Requested by James on 2026-10-03. Pulse owns profiling campaign intent and pending tasks; Mind retains development PR claims and historical completion records. Start at [Pulse](https://pyautolabs.github.io/PyAutoPulse/) for one-chat check-ins.

Merge the Pulse control-room PR before this migration. Original texts and checksums are retained in [migration.yaml](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/migration.yaml), pinned to Mind `f21898e042be67afd86cc9c512879b3ad1c9ca9a`.

| Former Mind prompt | Pulse task |
|---|---|
| `draft/bug/autolens_profiling/runtime_cell_single_jit_gpu_warmup.md` | [runtime_cell_single_jit_gpu_warmup](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/runtime_cell_single_jit_gpu_warmup.md) |
| `draft/bug/autolens_profiling/timing_noise_audit.md` | [timing_noise_audit](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md) |
| `draft/bug/workspaces/mge_likelihood_breakdown_steps_are_cumulative_an.md` | [mge_likelihood_breakdown_steps_are_cumulative_an](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_likelihood_breakdown_steps_are_cumulative_an.md) |
| `draft/feature/autolens_profiling/gradient_cost_probe.md` | [gradient_cost_probe](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/gradient_cost_probe.md) |
| `draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md` | [numba_breakdown_harness_memo_blind](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/numba_breakdown_harness_memo_blind.md) |
| `draft/feature/autolens_profiling/search_settings_estimation_infrastructure.md` | [search_settings_estimation_infrastructure](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/search_settings_estimation_infrastructure.md) |
| `draft/maintenance/autolens_profiling/jax_compile_probe_needs_own_cell_builder.md` | [jax_compile_probe_needs_own_cell_builder](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/jax_compile_probe_needs_own_cell_builder.md) |
| `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md` | [mass_field_flat_adoption_science_repos](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mass_field_flat_adoption_science_repos.md) |
| `draft/research/autoarray/mge_nnls_fix_pyautoarray_571_slam_60.md` | [mge_nnls_fix_pyautoarray_571_slam_60](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md) |
| `draft/research/autofit/autofit_profiling_bootstrap.md` | [autofit_profiling_bootstrap](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md) |
| `draft/research/autolens_profiling/cluster_pointsolver_speed.md` | [cluster_pointsolver_speed](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/cluster_pointsolver_speed.md) |
| `draft/research/autolens_profiling/imaging_production_over_sampling.md` | [imaging_production_over_sampling](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/imaging_production_over_sampling.md) |
| `draft/research/autolens_profiling/interferometer_decision_matrix_last_cell.md` | [interferometer_decision_matrix_last_cell](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_decision_matrix_last_cell.md) |
| `draft/research/autolens_profiling/interferometer_fixed_mapper_curvature_preload.md` | [interferometer_fixed_mapper_curvature_preload](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_fixed_mapper_curvature_preload.md) |
| `draft/research/autolens_profiling/interferometer_nnls_memo_scattered_stream_guard.md` | [interferometer_nnls_memo_scattered_stream_guard](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_nnls_memo_scattered_stream_guard.md) |
| `draft/research/autolens_profiling/interferometer_streaming_scaling.md` | [interferometer_streaming_scaling](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_streaming_scaling.md) |
| `draft/research/autolens_profiling/interferometer_w_tilde_fft_size_levers.md` | [interferometer_w_tilde_fft_size_levers](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_w_tilde_fft_size_levers.md) |
| `draft/research/autolens_profiling/point_solver_profiling_cells.md` | [point_solver_profiling_cells](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/point_solver_profiling_cells.md) |
| `draft/research/autolens_profiling/point_source_image_plane_gpu_breakdown.md` | [point_source_image_plane_gpu_breakdown](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/point_source_image_plane_gpu_breakdown.md) |
| `draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md` | [point_source_source_plane_chi_squared_speed](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/point_source_source_plane_chi_squared_speed.md) |
| `draft/research/autolens_profiling/pointsolver_cpu_speed_campaign_remainder.md` | [pointsolver_cpu_speed_campaign_remainder](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/pointsolver_cpu_speed_campaign_remainder.md) |
| `draft/research/autolens_profiling/post_certified_solver_likelihood_breakdown.md` | [post_certified_solver_likelihood_breakdown](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/post_certified_solver_likelihood_breakdown.md) |
| `draft/bug/workspaces/profile_lens_aggregator_needs_config_dir.md` | [profile_lens_aggregator_needs_config_dir](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/profile_lens_aggregator_needs_config_dir.md) |
| `draft/bug/workspaces/gradient_pixelization_pin_residual_drift.md` | [gradient_pixelization_pin_residual_drift](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/gradient_pixelization_pin_residual_drift.md) |
| `draft/research/autonerves/pair_jax_xla_env_vars_with_measured.md` | [pair_jax_xla_env_vars_with_measured](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/pair_jax_xla_env_vars_with_measured.md) |
| `draft/research/autolens/quick_update_plotting_cost.md` | [quick_update_plotting_cost](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/quick_update_plotting_cost.md) |

The issued timing-noise audit keeps autolens_profiling#362; its planned row is removed to avoid duplicate scheduling. Mixed library/science tasks and shared epics remain here with Pulse pointers. Completed records are unchanged.

Migration scope includes pending profiling campaigns, instrumentation, measurement reliability and benchmark research, including those misfiled under other targets. Library implementation fixes, release-smoke repairs and science inference campaigns retain their existing lifecycle owners.

Prerequisite: [Pulse#7](https://github.com/PyAutoLabs/PyAutoPulse/pull/7).
