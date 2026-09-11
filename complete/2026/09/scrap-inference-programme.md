## scrap-inference-programme
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/245
- completed: 2026-09-11
- epic: autolens-inference (phase 2 of 4)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/246
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/376
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/401
- gut-archive: `refs/heads/archive/condemned/autolens-profiling/inference-programme` @ `c8b60580` (PyAutoGut)
- summary: |
    Phase 2 of the autolens-inference epic. The retired inference programme is gone from
    autolens_profiling, archived whole rather than deleted, and the Brain samplers faculty's
    mature tier now points at the new autolens_inference repo.

### What shipped

- **autolens_profiling#246** — 555 files removed, 24 modified. Out went the `searches`
  framework and its leaves, `results/searches`, the `InferenceRefs_v1` baselines,
  `results/notes/inference` and `results/notes/gradient_slam`, `CORTEX.md`, 58 search
  submit scripts and 8 search tests. `build_readme.py`, lint, the profile/wall paths and
  docs were repaired around the hole; `lint` green on the merged head.
- **PyAutoBrain#376** — the samplers faculty's mature tier repointed from
  autolens_profiling's scrapped searches tier to `autolens_inference`.
- **PyAutoMind#401** — firewall allowlist rows so the samplers faculty may name
  `autolens_inference`. This was the merge-order key: until it was on Mind `main`, the
  Tenant firewall step in Brain Tests failed on both py3.12 and py3.13 legs of #376.

### Nothing was destroyed

`origin/main` of autolens_profiling as it stood before the deletion is held by PyAutoGut
as a durable, recoverable ref:

```
refs/heads/archive/condemned/autolens-profiling/inference-programme  @  c8b60580
```

Every scrapped file is `git fetch`-able from there. `build_objective` now raises
`NotImplementedError` naming that ref rather than failing silently.

### Issues

- autolens_profiling#218 and #205 closed as `not_planned` — both were work inside the
  scrapped tier.
- autolens_profiling#166 retitled: it survives as the PyAutoArray `log_det_method` default
  question (slogdet vs cholesky, cost-aware), with the inference-programme framing removed.
- A `condemned.md` entry records the scrapping.

### Deliberately left

`scripts/misc/jax_compile/probe.py` built its cells through `searches._setup.build_for_cell`,
which went with the tier; its pinned warm-compile records and the compile dashboard are
intact but the probe cannot run. Filed as
`draft/maintenance/autolens_profiling/jax_compile_probe_needs_own_cell_builder.md` — give the
probe a builder autolens_profiling owns; restore nothing from the archive ref.

### Traps

- **Merge order is load-bearing.** The Tenant firewall gate in Brain Tests reads the
  allowlist from PyAutoMind `main`, not from the PR under test, so Mind#401 had to merge
  and the Brain run be re-run before #376 could go green. A re-run of the failed jobs
  cleared it with no code change.
- **Parallel claim on autolens_profiling** with `reconstruction-row-split` (#243) held
  throughout: file sets were disjoint and neither worktree ever ran `git add -A`.

### Next

Phase 3: `draft/feature/autolens_inference/slam_base_driver.md` — backend-parameterised
SLaM base-run driver, per-stage results and submits. Unblocked; nothing from the retired
programme is reused.

## Original prompt

# Scrap the retired inference programme from autolens_profiling (autolens-inference phase 2)

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoMind
- PyAutoGut
Themes:
- inference
- hygiene
- gut
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: autolens-inference
Phase: 2
Status: active
Consequence: judge
Witness: `git -C autolens_profiling ls-files | grep -c "scripts/misc/searches\|scripts/[a-z_]*/searches\|results/searches\|results/baselines/InferenceRefs_v1\|results/notes/inference\|results/notes/gradient_slam"` prints 0 on the branch; `git ls-remote PyAutoGut refs/heads/archive/condemned/autolens-profiling/inference-programme` resolves; autolens_profiling `lint` is green; autolens_profiling#218 and #205 are closed
Review-minutes: 25
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/245

The human retired the Cortex project `inference_programme` on 2026-09-07 (PyAutoCortex#22)
and on 2026-09-10 ruled that **none** of its material is trusted or inherited by the
successor repo `autolens_inference` ("I dont trust a lot of this, some runs were dodgy,
so just scrap it and move it somewhere not in autolens_inference"). This phase moves that
material out of `autolens_profiling` into the Gut's attic and deletes it from `main`, so
profiling becomes what its `repos.yaml` role says: likelihood timing only.

## What goes to the attic (one archive ref, then deleted from main)

Survey first — `git ls-files` plus a grep for `searches` / `inference` / `InferenceRefs` /
`gradient_slam` across the repo — and list every path before deleting. Expected set:

- `scripts/misc/searches/` (the 13.8k-line searches framework: `_runner.py`, `_setup.py`,
  `_samplers.py`, `_targets.py`, `_metrics.py`, `_per_lane.py`, `_recovery.py`,
  `sweep.py`, `aggregate.py`, `bijector_ab.py`, `slogdet_ab*.py`, `clipper_campaign.py`,
  `positions_transects.py`, `restamp_target_block.py`, its README and tests)
- `scripts/<dataset_class>/searches/**` (the ~60 thin sampler leaves)
- `results/searches/**` (177 result JSON/PNG rows), `results/baselines/InferenceRefs_v1/**`
- `results/notes/inference/**` (PROGRAMME.md, DECISIONS.md, LITERATURE.md, methods/,
  targets/, phase_*/), `results/notes/gradient_slam/**`
- `hpc/batch_gpu/submit_*` and `hpc/batch_cpu/submit_*` that drive searches
  (`nautilus`, `nss`, `nuts`, `smc`, `multi_start`, `prodigy`, `positions`, `bijector`,
  `slogdet`, `clipper` in the name); keep the likelihood-runtime / breakdown /
  parallel-scaling submits
- `CORTEX.md` (it only explained which of three ledgers counted) — replace with one
  line in `AGENTS.md`: science runs are the Cortex's, and this repo has no project row
- `scripts/misc/test/test_hazards_*` only if they import from `searches`; keep the
  compile-pin tests

Not in scope: `_production_config.py`, `instruments/`, `simulators/`, `likelihood_runtime`,
`likelihood_breakdown`, `hazards`, `vram`, `wall`, `lens/` — those are profiling's own.
The RAL run outputs are already stashed at
`/mnt/ral/jnightin/inference_programme_retired_2026-09-07` and are not touched.

## Mechanics

1. `@autolens_profiling`: on the task branch, `git rm -r` the set above; then fix every
   consumer: `scripts/misc/tooling/build_readme.py` (drop the `searches` section
   renderer and its sentinel regions in `README.md` + `scripts/misc/searches/README.md`),
   `.github/workflows/lint.yml` (the smoke list names `searches/nautilus/mge.py`) and
   `profile.yml` (`sections` input), `scripts/misc/wall/rates.py` + `check_submits.py`
   (rows that only served search submits), `AGENTS.md` / `README.md` prose, the
   `.claude/skills/profile_likelihood` skill if it mentions searches. Regenerate the
   README with `build_readme.py`; `ruff`, `build_readme.py --check`,
   `check_submits.py --check`, pytest must pass.
2. `@PyAutoGut` + `@PyAutoMind`: BEFORE the deletion commit is merged, materialise the
   pre-deletion tree as a durable ref: `pyauto-gut archive` (read `PyAutoGut/README.md`
   and `PyAutoBrain/skills/hygiene` for the verb) pushing
   `refs/heads/archive/condemned/autolens-profiling/inference-programme` to PyAutoGut —
   verify with `git ls-remote` on the **Gut** remote, not origin (memory: the archive
   verb pushes to origin unless `PYAUTO_GUT_REMOTE` is set). Add the entry to
   `PyAutoMind/condemned.md` per its "Entry schema" (what, why, ref, recover-by, void-after).
3. Issues: close autolens_profiling#218 (gradient-slam `mass_pix` dev leg — superseded by
   autolens_inference phase 3) and #205 (RAL legacy_point sweep — the tree was stashed on
   2026-09-07). Leave #166 (slogdet as PyAutoArray default) open but edit its title/body
   to drop the "gradient-slam-baseline phase 23" framing: it is a library question, not
   epic residue. Delete `PyAutoMind/draft/feature/autolens_profiling/gradient_slam_*.md`
   and remove the archived epic entry's forward pointer if `complete/archive/epics/`
   names a live successor.
4. `PyAutoCortex`: nothing — the `inference_programme` row is already `status: retired`;
   do not delete rows (rulings cite them).

## Original request (verbatim, 2026-09-10)

"I dont trust a lot of this, some runs were dodgy, so just scrap it and move it somewhere
not in autolens_inference: What still stands and should be carried in verbatim: the 9
certified InferenceRefs_v1 baselines, the MGE Prodigy result (5/5 hits at 163–297 s vs
Nautilus 939 s), the positions binding rule, the target_id hashing, the schema-v2 run
JSON, and the tolerance table (2 nats, 0.2σ, σ-ratio in [0.8, 1.25]). Also the
13.8k-line searches framework under autolens_profiling/scripts/misc/searches/, which is
the runner this repo needs."
