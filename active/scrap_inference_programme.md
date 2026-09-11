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
