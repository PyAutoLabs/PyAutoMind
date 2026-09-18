# Adopt fields API in the Euclid pipeline and launch DR1 top 1000

Type: refactor
Target: @euclid_strong_lens_modeling_pipeline
Autonomy: supervised
Filed: 2026-09-18
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/89

## Original request

Can you accept this https://github.com/PyAutoLabs/autolens_workspace/pull/560, and then implement the fields API in euclid_storng lens modeling piepline, then do it in the Science project euclid_dr1, HPCHPCPullPyAuto and get the 1000 lens run wehave been setting ussing up eclipse_catalogue_fits_sep1_top1000_brightest.csv going

## Proposed plan

1. Resolve workspace PR #560's explicit release hold. All three head workflows succeeded; PyAutoGalaxy#621 and PyAutoLens#742 merged September 17, but live PyPI still publishes 2026.9.15.1 from September 15. The sibling workspace_test#322 belongs to the same task; do not close the whole task on a partial merge.
2. Migrate pipeline shear composition to `fields=af.Collection(field=af.Model(al.MassField, ...))`, with lens redshift and existing shear priors preserved. Chain model or instance fields at the same stages as the existing shear. Preserve the full-model final-stage shear-prior reset.
3. Update result readers, simulator and regression fixtures; verify numerical parity, model parameter counts and prior/fixed chaining, catalogue shear columns, and COOLEST output. Run fast tests, the applicable smoke chain and real-output checks.
4. Apply the validated pipeline changes to the Cortex-registered euclid_dr1 science clone, preserving its 18 local commits, science configuration, datasets, old outputs and untracked top-1000 preparation. Never push that clone to its pipeline origin.
5. Verify no jobs use the shared RAL stack, resolve and run the existing HPCPullPyAuto command, confirm remote library revisions and fields support, sync through the project's CLI, and smoke one selected real dataset without overwriting production output.
6. Submit the existing CPU vis_lp-only top-1000 array using the project's hpc/sync CLI, confirm its job ID and queue state, then record the submission with Cortex verbs and update science session notes.

## Detailed implementation surface

- `scripts/initial_lens_model.py`: vis_lp model composition and vis_pix result chaining.
- `scripts/full_model.py`: all source/light/mass stages, including deliberate reset_shear_prior behavior.
- `scripts/sersic_lens_model.py`, `scripts/lens_model_waveband.py`: fixed fields carried alongside lens mass into photometric fits.
- `scripts/simulator.py`: separate tracer fields; preserve the simulated image and truth semantics without regenerating committed data unnecessarily.
- `catalogue/scripts/lens_mass.py`, `workflow/csv_make.py`, `workflow/example/csv/lens_mass.py`: fields.field.shear result paths; inspect compatibility requirements for existing galaxy-attached results.
- Existing tests including COOLEST, catalogue columns, Witt-Wynne and model-chain coverage: update fixtures and add meaningful parity/chaining coverage where absent.
- Science clone: port the validated diff selectively; review any science-only model/readout callers too. New model identifiers must not be mistaken for a resume of the old galaxy-attached fits.

## Branch survey and holds

- Pipeline canonical checkout is clean on main at cf66194. Proposed branch: feature/euclid-fields-api; worktree: euclid-fields-api via standard worktree helper after approval.
- worktree_check_conflict reports sed-chain-cpu-route, sersic-variants, sersic-variants-analysis and grid-offset-prior claims. Open PRs are #70 and #75. Coordinate overlapping script changes before implementation; no claim is silently waived.
- Science clone is main, 18 commits ahead of its pipeline origin, with untracked dataset/dr1_sep1/, dataset/dr1_sep1_top1000/, eclipse_catalogue_fits_sep1_top1000_brightest.csv and hpc/batch_cpu/submit_initial_lens_model_vis_lp_top1000. Preserve all.
- Plan approval required under workspace AGENTS.md before source edits. No issue, source edit, submission or merge performed at filing.

## Verified run preparation

- CSV has exactly 1000 rows; id_str exactly matches the submit script's 1000 unique tile names in order.
- All 1000 selected tiles have their named FITS and info.json under dataset/dr1_sep1_top1000/.
- Prepared script: hpc/batch_cpu/submit_initial_lens_model_vis_lp_top1000; array 0-999; partition ral; 8 CPUs, 64 GB and 18 hours per task; stage vis_lp only.
- hpc/sync jobs returned an empty queue on September 18. Recheck immediately before changing the shared stack or submitting.

## Approval — 2026-09-18

The human approved all three delivery phases and coordinating the existing branches: "yes do 1, 2, 3 remember that RAL is a clone of github so we dont need a release for those changes rto take effecft, letts merge PRs if possible on stuffl ike autolens_Workspace". This lifts the PyPI release hold for the workspace merges in this session. CI must still pass. Work proceeds in an isolated feature/euclid-fields-api worktree; other claimed branches remain untouched. The pipeline migration is one coherent PR, followed by science deployment and the already-authorized submission; no new library API is needed.

## Submission hold — 2026-09-18

User: "dont submit jobs until Ive okayed modeling script". This supersedes earlier submission authorization: complete implementation, local validation and reviewable script preparation, but submit no SLURM jobs (including cluster smoke tests) before fresh modelling-script approval. No jobs submitted before this hold.

## Naming revision — 2026-09-18

User: "I am fixing this throughout the autolens_workspace in anothrer chat, but apply it to these euclid pipelines: ❯ In autolens_workspace and other projects we updated the model composiiton to use MassField last night, however can we change field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear)) to shear = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear))   and fields=af.Collection(field=field),    to fields=af.Collection(shear=field),   in probably all of the example scripts, which will span all the way to SLaM pipelines and other examples throughout workspaces and the test worskpace?"

Apply to Euclid only: the MassField variable and collection key are `shear`, so composition is `fields=af.Collection(shear=shear)`, chained field objects are `result.model.fields.shear` / `result.instance.fields.shear`, and profile parameters are `fields.shear.shear.gamma_1` / `gamma_2`. The inner `shear` names the ExternalShear profile; the outer names the MassField. Workspace and workspace_test edits remain owned by the other chat. No jobs until modelling-script approval.

## Naming correction — 2026-09-18

User: "ok wait I made a mistake, it shuld not be shear.field.field I misread field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear))."

The prior naming revision is withdrawn. Restore the original composition: MassField variable `field`, `fields=af.Collection(field=field)`, and parameters at `fields.field.shear.gamma_1/2`. The fields migration itself continues; no jobs until modelling-script approval.

## Human-authorized Heart RED development override — 2026-09-18

The user replied "I approve" to: "Authorize the development-only Heart override for issue #89, and merge only when every required CI check is green?"

Exact current Heart RED reason: `release validation FAILED (stage integrate)`.
Also acknowledged: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.

Branch gates passed: 230 pipeline tests; 9/9 smoke scripts; independent Sol review CLEAN (27 focused checks); git diff --check clean. Representative legacy/flat models retain 15 parameters and log likelihood agrees within 2e-12; identifiers intentionally differ.

Authorization is scoped to euclid-fields-api / issue #89: commit, push, pending-release PR, and merge only with every required check green during this session. No release, failed-check bypass, or SLURM submission is authorized. The modelling-script submission hold remains.

Latest API correction: no compatibility branches or tests for nested collection-form single fields. Models use fields=field and fields.shear.gamma_1/2. Legacy galaxy-attached result readers remain supported.

## CI blocker — 2026-09-18

PR #90, head `7fbdbe5123828570aa7af08cdf5d4097fb397454`, is not merged.

Both Python 3.12 and 3.13 unit legs fail `test_latent_euclid_variables_traces_under_jax_jit`; each reports 219 passed, 1 failed. Both slow-test legs passed. The newly added bare-fields likelihood/gradient test passed. At the CI judgment, both smoke matrix legs were still running.

CI installed JAX/jaxlib 0.11.2 and jax-zero-contour 2.0.0. The passing local suite uses JAX/jaxlib 0.10.2 with the same contour package. A standalone 15-line circle-contour reproducer with no PyAutoLens, Euclid or MassField code passes on 0.10.2 and fails on 0.11.2:

`TypeError: Argument 'functools.partial(...)' of type '<class functools.partial>' is not a valid JAX type`

The trace passes through `jax_zero_contour.ZeroSolver.newton` → `jax.lax.custom_root` → the solver loop carrying the callable. No test was skipped, weakened, or marked expected-failure; no dependency downgrade was applied to CI or the shared environment.

Evidence retained locally under `PyAutoMind/tmp/euclid-flat-fields/`: `ci-failed.log`, `zero-contour-repro.py`, `repro-jax010.log`, `repro-jax011.log`. The new-JAX reproduction used an isolated temporary environment; the production environment was not changed.

Science deployment remains pending: local euclid_dr1 at d53b9ce, RAL PyAutoLens at 7197380. RAL's interpreter `/mnt/ral/jnightin/PyAuto/PyAuto/bin/python3` successfully imported `/mnt/ral/jnightin/PyAuto/PyAutoLens/autolens/__init__.py` and confirmed bare-field normalization absent. Stack preconditions checked Nerves, Fit and Array as clean/main/up-to-date; the 180-second read-only check timed out during Galaxy. HPCPullPyAuto was not run. No code sync or SLURM submission occurred. The final modelling-script approval hold remains.

Upstream repair completed: complete/2026/09/euclid-jax-contour-compat.md (PyAutoGalaxy#623 and autogalaxy_workspace_test#123).

## Merged and locally ported — 2026-09-18

PyAutoGalaxy#623 merged at 90e757d336e62b75790befacc77e2d6dde460879 (4/4 checks); workspace-test#123 at ae45e490f75260533d0f18bb3bc2ce951377a0d5 (3/3). Pipeline #90 rerun against the repaired source passed all 9 checks and merged at 9cdee7b10e916b4e2d172257f26c37881f094802. Local science selectively ported all 21 reviewed files and committed d53b9ce -> 2430e4ecd0815ee1cfb4809e3836e178dd5a90b6, preserving all 18 science commits and untracked preparation; never pushed to pipeline origin. Actual local interpreter/import/model check passes with 15 priors, fields.shear.gamma_1/2 and tracer.fields list.

RAL remains unchanged. Job 343413 fixed_light_numba_s5b is RUNNING and its activate.sh imports shared canonical PyAuto checkouts. Do not refresh while it runs. Next: recheck queue and all library cleanliness/divergence (Fit status previously timed out), preserve three editor backups, run inspected HPCPullPyAuto, verify imported bare-field normalization and compatibility adapter, then sync project via hpc/sync and record pre/post facts with Cortex. No source sync, stack refresh or SLURM submission performed. Hold remains: dont submit jobs until Ive okayed modeling script. Cortex operational note pushed at 3c32bcc; exact state in tmp/euclid-flat-fields/deployment-state.json.

## Submission approved; RAL code deployed — 2026-09-18

User: “ah you are right, then let us submit dont worry about the comment”. This lifts the modelling-script submission hold for the prepared CPU vis_lp top-1000 array. Keep fields=field unchanged. Queue was empty before HPCPullPyAuto. RAL Galaxy is now 90e757d336e62b75790befacc77e2d6dde460879 and Lens 478213e787781517113e96f80013270df482f665; the other three libraries and all editor-backup hashes are unchanged. Project code/config transferred through hpc/sync; all 115 checked hashes match local science 2430e4e. Actual RAL imports/model check passed, including flat fields.shear paths, 15 priors, list-valued tracer.fields and CompatibleZeroSolver.

Data transfer remains in progress and no job has been submitted. The 703 MB lossless top-1000 archive upload is slow; an initially stalled connection was restarted with timeouts. Interrupted direct transfers may have left partial input files: verify the archive checksum and every prepared dataset before submission. Use the project hpc/sync submit cpu submit_initial_lens_model_vis_lp_top1000 only after completeness checks. Logs/manifests are in tmp/euclid-flat-fields; Cortex progress recorded in c37c8f4. No release gate has been lifted.
