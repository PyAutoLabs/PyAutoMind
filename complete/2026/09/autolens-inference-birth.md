## autolens-inference-birth
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/399 (closed completed 2026-09-10)
- completed: 2026-09-10
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/400
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/28
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/224
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/375
- library-pr: https://github.com/PyAutoLabs/.github/pull/9
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/1
- shipped: 2026-09-10 — six PRs on `feature/autolens-inference-birth`: PyAutoHeart #224
  (`94b64cb1`), PyAutoBrain #375 (`095812d4`), .github #9 (`e82a0757`),
  autolens_inference #1 (`bd4fe48d`), then PyAutoMind #400 (`5b88d0f9`) and PyAutoCortex
  #28 (`1a151fd5`) after merging `main` back in (both had gone `dirty` on generated
  dashboards; Mind also on `epics.md`).
- classification: feature (autolens_inference) — epic `autolens-inference`, phase 1 of 4.
  Human-gated: `PyAutoLabs/autolens_inference` was created 2026-09-10 by `gh repo create
  --public` after a dedicated confirmation question (the gh token carries `repo` scope and
  the human is org admin — the first agent-run org-repo creation; earlier births were by
  hand on github.com).
- summary: `autolens_inference` is born as the from-scratch restart of the retired Cortex
  project `inference_programme` (PyAutoCortex#22), with **nothing inherited** — the human
  distrusts that programme's runs, so its baselines, notes, target code, searches
  framework and result JSONs stay out (phase 2 archives and deletes them from
  autolens_profiling). Delivered: a workspace-root checkout with the autolens_profiling
  skeleton minus the searches tier (48 files: `ruff.toml` sentinel, `_inference_cli.py`
  with `--backend/--inversion/--seed` reserved for phase 3, `instruments/`, three
  simulators, an empty-state README renderer with `--check`, `hpc/sync` as profiling's
  no-push fork plus the `PYAUTO_PULL_DIRS` seam extended to `PULL_DESTS` in lockstep,
  A100 `gpu` and `ral` SLURM templates, lint + profile workflows; `wall/rates.py` ships
  EMPTY on purpose); `repos.yaml` row (`category: project`) with `repos_sync --write`
  regenerating the root routing table; `ROUTING.md` target; `epics.md` entry;
  `PyAutoCortex/projects.yaml` row (`mirror: none`, `assistant: autolens_assistant`,
  `partition: both`, `status: active`) with dashboards re-rendered; Heart `excluded:`;
  Brain `clean_slate.sh` exclusion; org-profile README row. RAL: clone at
  `/mnt/ral/jnightin/autolens_inference` on `main`, `activate.sh` resolves autolens /
  autofit / autoarray 2026.8.17.1, `hpc/sync check|status|jobs|du|pull` all pass and a
  pull writes `.cortex/pull.json`.
- witness: `repos_sync.py --check` 16/16 legs OK; `cortex.py check` OK; autolens_inference
  `lint` green on PR #1 (ruff, README idempotence, wall gate, 4 pytest, 3 smoke
  simulators); PyAutoMind 412 / PyAutoCortex 126 / PyAutoHeart 967 / PyAutoBrain 944
  passed; CI green on every leg of every run for the four merged-first PRs; `.github` has
  no checks configured (merged MERGEABLE/CLEAN under the human's `/prm`, as for the
  Cortex birth).
- heart: not GREEN at ship (test run NOT ready — autolens multi_dataset notebook + script
  timeouts, workspace_test `delaunay.py` failed; release validation incomplete). None of
  it touches the six doc/manifest repos; merged under the human's `/prm`.
- deviations: `scripts/repos_sync.py` gained a `FIREWALL_ALLOWLIST` entry — naming the
  new repo in Brain's clean-slate comment trips the tenant-firewall leg otherwise (a data
  declaration, not a check bypass). The workspace root `/home/jammy/Code/PyAutoLabs` is
  **not a git repo**, so the regenerated root `AGENTS.md` lives on disk only.
  `_inference_cli.py` dropped `--vmap-probe`, `--variant`, `--n-instances`,
  `--cold-evals` (they only served excluded tiers). `check_submits.py` now also gates
  `hpc/batch_*/template`.
- traps: another session's `prompt_sync_push` (`git add -A`) swept this task's untracked
  draft prompt into its own commit while the draft was being moved to `active/` — removed
  from `origin/main` by a follow-up commit; the canonical PyAutoMind checkout held that
  session's staged close-out throughout, so every Mind write here went through a detached
  temp worktree of `origin/main`. `ledger_merge.py classify --base origin/main` with no
  paths HANGS (killed; a second session's identical hung process was left alone). The new
  `.gitignore` lacked `logs/` until `hpc/sync pull` exposed it. Mind #400 and Cortex #28
  went `dirty` within the hour because both mains regenerate dashboards on every push.
- follow-ups: phase 2 `draft/maintenance/autolens_profiling/scrap_inference_programme.md`
  (Gut-archive + delete the searches tier, baselines and inference notes; close
  autolens_profiling#218/#205, reframe #166); phase 3
  `draft/feature/autolens_inference/slam_base_driver.md` (backend-parameterised SLaM
  driver, per-stage rows, six submits with measured WALL-BASIS); phase 4 = `cortex.py new
  autolens_inference slam_hst_base` once phase 3 lands. Not filed: hoisting `instruments/`
  + `simulators/` into PyAutoLens (third copy now exists); `hpc/sync status` creates local
  `logs/**` dirs before its dry run; the human is confident the `PAT_PYAUTOLABS` token
  already covers the new repo — the next `session_hook_propagate` run is the witness.
- session: claude-code-cli, Fable architect; research by 7 Opus explore agents, execution
  by 4 Opus subagents (skeleton, registries, RAL, conflict resolution); close-out via
  `/prm` 2026-09-10.

## Original prompt

# autolens_inference birth: checkout, skeleton and registration (phase 1 of 4)

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoMind
- PyAutoCortex
- PyAutoHeart
- PyAutoBrain
- .github
Themes:
- inference
- repo-birth
- cortex
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: autolens-inference
Status: active
Consequence: judge
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check` exits 0 with the new row; `python3 PyAutoCortex/scripts/cortex.py check` exits 0 with the `autolens_inference` row; the new repo's `lint` workflow is green on its first PR; `autolens_inference/hpc/sync check` from the laptop reaches `/mnt/ral/jnightin/autolens_inference`
Review-minutes: 30
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/399

`PyAutoLabs/autolens_inference` was created on github.com on 2026-09-10 (public, empty,
after a dedicated confirmation). This phase makes it a first-class citizen of the
organism: a local checkout at the workspace root, the autolens_profiling skeleton with
**no searches tier and no inherited results**, and a row in every registry a project repo
needs. It is the from-scratch restart of the retired Cortex project `inference_programme`
(PyAutoCortex#22): none of that programme's baselines, notes, target code or run JSONs
come across — the human does not trust them ("some runs were dodgy"); their disposal is
phase 2. Design record: session memory `project_autolens_inference_birth.md`.

## Scope

1. **Checkout + skeleton** (`@autolens_inference`): clone into
   `/home/jammy/Code/PyAutoLabs/autolens_inference`. Copy from `autolens_profiling`:
   `ruff.toml` (root sentinel), `activate.sh`, `AGENTS.md` (rewritten for inference;
   keep the `repos_sync:*` blocks verbatim), `CLAUDE.md`, `AI_POLICY.md`, `LICENSE`,
   `README.md` with auto-table sentinels, `CORTEX.md` naming the `projects.yaml` key,
   `.gitignore` (`output/`, `hpc/sync.conf`, `hpc/batch_*/{output,error}`, regenerable
   `dataset/`, caches), `config/{general,latent}.yaml`, `instruments/`,
   `scripts/misc/{simulators,tooling/build_readme.py,test/}`, `_profile_cli.py` renamed
   `_inference_cli.py` with the smoke variable `AUTOLENS_INFERENCE_SMOKE`,
   `hpc/{sync,sync.conf.example,README.md,batch_gpu/,batch_cpu/}` (profiling's no-push
   fork plus the `PYAUTO_PULL_DIRS` append block from
   `euclid_strong_lens_modeling_pipeline/hpc/sync:121-124`; `PULL_DIRS=(output results)`;
   `.gitignore` stubs in `batch_*/{output,error}`), `.github/workflows/{lint,profile}.yml`.
   Empty task dirs `scripts/{imaging,interferometer,point_source}/{slam,searches}/` with
   READMEs; `results/{slam,searches}/`; `wiki/project/state.md` + `_template.md`.
   Config-name grammar `{local,hpc_a100}_{jax_cpu,numba_cpu,jax_gpu}_{dense,sparse}_{fp64,mp}`
   documented in AGENTS.md. **No search runner, no SLaM driver yet** (phase 3).
2. **Mind** (`@PyAutoMind`): `repos.yaml` row under `# --- project`
   (`github: PyAutoLabs/autolens_inference`, `category: project`, role one-liner);
   `repos_sync.py --write`; `ROUTING.md` targets vocabulary gains `autolens_inference`;
   `epics.md` gains `autolens-inference` (phases: 1 birth, 2 scrap ancestor, 3 base-run
   driver, 4 Cortex task `slam_hst_base`).
3. **Cortex** (`@PyAutoCortex`): `projects.yaml` row — `remote: PyAutoLabs/autolens_inference`,
   `local_path: /home/jammy/Code/PyAutoLabs/autolens_inference`,
   `ral_root: /mnt/ral/jnightin/autolens_inference`, `mirror: none`, `sync_cli: hpc/sync`,
   real `sync_verbs`, `ledger: wiki/project/state.md`, `assistant: autolens_assistant`,
   `witness_file: results/**/*.json`, `partition: both`, `status: active`, dated note.
   Re-render the dashboards.
4. **Heart** (`@PyAutoHeart`): `config/repos.yaml` `excluded:` gains `autolens_inference`.
5. **Brain** (`@PyAutoBrain`): `bin/clean_slate.sh` dataset/results exclusion gains the
   repo; `bin/install.sh` only if a `skills/` dir ships (it does not in phase 1).
6. **Org profile** (`@.github`): `profile/README.md` PyAutoLens table gains the row.
7. **RAL**: `git clone` into `/mnt/ral/jnightin/autolens_inference` on the login node,
   verify `source activate.sh` resolves the stack, `hpc/sync check` from the laptop.

## Out of scope

Phase 2 (Gut-archive and delete profiling's searches tier, baselines, inference notes;
close autolens_profiling#218/#166/#205 and the gradient_slam drafts), phase 3 (the
backend-parameterised SLaM driver, per-stage result writer, submit scripts), phase 4
(Cortex task `slam_hst_base`). Hoisting `instruments/`+`simulators/` into PyAutoLens is a
separate prompt once the third copy exists.

## Human gates

- Extend the `PAT_PYAUTOLABS` fine-grained token's repository list with
  `autolens_inference` before the first `session_hook_propagate` run.
- `projects.yaml` and `repos.yaml` are code: both land by PR + human merge.

## Original request (verbatim)

autolens_profiling is now a mature and highly useable repo, which allows us to track all aspects of how long a likelihood function takes to compute and to speed it up. I now want to make a new project and repo, autolens_inference, which behaves analogously, but is for all non-linear search and inference tasks, especially working out the best searches with gradients or without gradients. We did work to this effect on a JAX gradient epic, which I retired because it was too unwelidly, this project will be the centre of us learning all that stuff. It will have the same structure as autolens_profiling (E.g. scripts, with datasets in like, like scripts/imaging) and it will also support the same dataset types (e.g. hst, euclid, alma), this could mean some shared functionality move to PyAutoLens (or PyAutoReduce?) or another repo but only if you think that is worth it. Unlike autolens_profiling, this one will both need an output folder, have an RAL link to get to the A100s and may have the inference projects managed via PyAutoCortex, not via PyAutoMind, as it is more science-y in its management and inspection then software development. We will ultimately map out inference for imaging, interferome,ter point source (source and image hci squared), but our first real cortex task will start from running the standard imaging SLaM pipeline with our current setup (e.g. through to mass[1] with nautilus everywhere), where this run will use JAX CPU to numba CPU (standardbeing used on euclid runs atm) and A100 GPU whole way through, for both normal and sparse mesh likelihood functions. This is to get us our starting "base" from which we will then try lots of inference things to improve from there, frame it all around a HST imaging dataset for now. Insrastructure for other dataset types ca be built, but imaging is the main priority for now. Do some deep research and ask me if you think the project would benefit from anything else I havent thoguht of

Follow-up (same session): "I dont trust a lot of this, some runs were dodgy, so just scrap it and move it somewhere not in autolens_inference" — regarding the InferenceRefs_v1 baselines, MGE Prodigy result, positions rule, target_id hashing, schema-v2, tolerance table and the searches framework. Decisions taken: workspace-default mesh, simulated HST cell, workspace-root public checkout.
