# Likelihood lifecycle phase 5G: autolens_assistant: an `al_explain_setup` skill and an "auto unless…" rewrite of `al_configure_search`

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- hpc-gpu
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/191
Consequence: judge
Witness: autolens_assistant has `skills/al_explain_setup.md`, registered in `skills/README.md` with generated `.claude` / `.codex` adapters and a registration test. For a finished or running fit it reads `files/setup.json` + `files/parallel.json` (and the printed header + Setup/Parallel/Estimate lines), matches the setup to its `setup_rules.yaml` row, quotes the rule sentence, links the likelihood's autolens_profiling `wiki/campaigns/<type>/<variant>/day_zero.md` page and its Pulse decision, explains the estimate (measured cell, Nautilus-only heuristic, efficiency curve, size band) and flags the untested branches that apply. For a planned fit it uses `al.estimate_runtime` and describes the banner. `skills/al_configure_search.md`'s compute section reads "Compute setup: auto unless…" (`setup="auto"` + `number_of_cores="auto"` by default; when to override; the explicit table kept as the override route, with the stale "sparse operator is numba-only / never on GPU" claims fixed), within the Colab context cap. The small edits are done: AGENTS.md, al_load_results, al_run_search, al_debug_fit_failure, init-slam, al_profiling_setup, hpc_campaign, sources.yaml. `make test` passes.
Review-minutes: 25
Unattended: no
Lane: any
Gate: 5A–5E and the setup banner MERGED. Merge with or after the library release carrying them: the assistant's wiki-currency CI checks skill snippets against released `autolens`, so do not use gate-off markers. Plan approved by the human on 2026-11-25.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25

## Context

- **Report §3.5:** "Assistant: al_explain_setup skill: reads setup.json + the designation rule + autolens_profiling/inference notes and explains the choice and the estimate; al_configure_search updated to 'auto unless…'".
- **Survey 2026-11-25** (canonical main a752b42):
  - No skill knows `setup=` / `PYAUTO_SETUP` / `setup.json` / `parallel.json` / the estimate.
  - `al_configure_search.md:84-126` has a CPU-acceleration table; :97 and :122 are stale (JAX sparse setups exist; `jax_gpu_sparse_fp64_wtilde` is the A100 interferometer pixelized designation).
  - Skills are registered via `skills/_bootstrap_skill.md` + `skills/README.md`, with adapters from `bash organs/PyAutoBrain/bin/install.sh --write-project-discovery autolens_assistant` (`--check-project-discovery`). The registration-test pattern is `autoassistant/tests/test_greeting_skill.py`.
  - The Colab context cap is 20,000 characters (`colab/contexts.yaml:193` maps al_configure_search; `make colab-contexts`).
  - API gate: `make audit` / `autoassistant/audit_skill_apis.py`; `.github/workflows/wiki-currency.yml` runs against released autolens.
  - Evidence to cite:
    - `PyAutoArray:autoarray/config/setup_rules.yaml`;
    - `autolens_profiling:wiki/day_zero.md` + `wiki/campaigns/<type>/<variant>/day_zero.md` (20 pages; Rule / Day-zero evidence / Untested branches / Revisit);
    - PyAutoPulse `decisions/<id>.md` (local, or `github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/<id>.md`);
    - `PyAutoLens:autolens/config/runtime_estimates.yaml`;
    - autolens_inference `INFERENCE_SUMMARY.md` wall-time validation.
  - `sources.yaml` lacks autolens_inference and PyAutoPulse.
- **Design calls (human-approved 2026-11-25):**
  1. The skill reads the JSON files directly, with no new MCP tool now (a `get_setup_info` would go in PyAutoFit core later).
  2. Write and open the PR now, merge with or after the release; no gate-off markers.
  3. The `wiki/core/operations/hpc*.md` rewrite (via `al_update_wiki`) and the `hpc/` template `--use_cpu` → `--setup` migration go in a separate follow-up draft.
  4. Keep the explicit route documented as the override, so users on the current PyPI release keep working advice.

## Out of scope

- The wiki/core rewrite and the hpc template migration (follow-up).
- A PyAutoFit MCP `get_setup_info` tool.
- 5H science projects.
- The R6 default flip.
