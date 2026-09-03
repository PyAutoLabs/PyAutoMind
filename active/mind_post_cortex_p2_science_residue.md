# Delete the science-epic residue the Cortex split left in Mind

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoCortex
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: `grep -rn "cortex-half\|epic-slice\|theme-sweep\|^Lane:\|experiment/" PyAutoMind --include=*.md --include=*.sh --include=*.py` returns only `complete/` history; `epics.md` has no `jax-inference-profiling` entry; the five named RAL prompts exist as `PyAutoCortex/phases/**` files with `State: planned` and are gone from `draft/`; `batches/2026-08-31-am.*` is gone from Mind and present in Cortex; Mind `pytest -q` and `lifecycle.py check` pass; `pyauto-brain batch plan --dry-run` still runs
Review-minutes: 20
Unattended: ready
Epic: mind-post-cortex
Phase: 2
Filed: 2026-09-03
Issued: 2026-09-03

Phase 2 of `mind-post-cortex`. Touches `REFERENCE.md`, `ROUTING.md`,
`scripts/status.sh` and possibly `tests/` → this is a code-side Mind PR (the
ledger auto-merge will not take it); the Cortex side is its own PR.

## The residue (all verified 2026-09-03)

1. **`cortex-half:` keys** in `epics.md` (entries `jax-inference-profiling`,
   `cluster-strong-lensing`, `graphical-ep`, `euclid-dr1-prep`). Read by no
   code: `_intake.py` `_EPIC_FIELDS = ("title","ledger","status","notes")`.
   Delete the key everywhere; where the Mind half is live (`cluster-strong-
   lensing`, `graphical-ep`, `euclid-dr1-prep`) fold one clause into `notes:`
   ("science half: PyAutoCortex epics.md#<slug>"). Update the `epics.md`
   schema paragraph if it mentions the key.
2. **`jax-inference-profiling` entry** in `epics.md`: its own `status:` says
   the whole programme lives in Cortex and slices ship as autolens_profiling
   PRs, not Mind prompts. One member prompt remains
   (`draft/feature/workspaces/phase_5_dev_leg_prepare_the_mesh.md`) — detach
   it (drop `Epic:`/`Phase:`, keep as an ordinary draft). Retire the entry
   (status `COMPLETE — moved to Cortex 2026-09-01`, then the `--retire`
   move; the ledger is external so only the entry text is archived).
3. **`Lane:` header** (`REFERENCE.md` "Lane" section, `queue.md` schema lines,
   `batches/AGENTS.md` if mentioned). One draft uses it. Remove the Mind-side
   documentation and the one header
   (`draft/maintenance/autolens_profiling/legacy_point_output_sweep.md`, which
   moves to Cortex anyway — see 6). Leave Brain's `_batch.py` lane filter
   alone: Cortex members are `Lane: local-dev` by construction and the Cortex
   REFERENCE owns that key now — add one line there if it is not already
   documented.
4. **`kind: epic-slice` / `kind: theme-sweep`** in `queue.md` (schema + the
   "Three kinds" paragraph) and `REFERENCE.md`: zero consumers
   (`_batch.py` globs `draft/**/*.md` only). Reduce the schema to `kind:
   prompt | retired`; drop the `lane:` line. Sweep the four `kind: retired`
   entries into a short "Retired" footer or delete them.
5. **`experiment/` work-type**: no folder on disk, 0 drafts, 5 historical
   records. Remove it from `ROUTING.md`'s table, `AGENTS.md`'s work-type
   list, `README.md` "Prompt taxonomy", `scripts/status.sh`, and Brain's
   `_sizing.py` work-type table / autonomy cap (`"experiment": ...` at the
   ~L55 and ~L936 dicts) plus any Brain test fixture that enumerates
   work-types. Existing `complete/2026/**` records keep their folders.
   **Leave the `research` cap alone** (verdict-shaped research parks for a
   human by design).
6. **Five run-shaped prompts → Cortex phases.** `draft/research/graphical_ep/
   ep_campaign.md` and `slope_hierarchy_methods_writeup.md`,
   `draft/research/autolens_profiling/cluster_gradient_search_benchmark.md`
   and `multiband_compile_census_completion.md`,
   `draft/maintenance/autolens_profiling/legacy_point_output_sweep.md`. Read
   `PyAutoCortex/REFERENCE.md` (phase-file schema, `State:`, `Gates:`) and
   `docs/schema_decisions.md`; write each as `phases/<project>/<slug>.md`
   with `State: planned` under the matching project in `projects.yaml`
   (`graphical_ep` → `slope_hierarchy` / `ic50_workspace` as fits; profiling
   ones → `inference_programme`). Keep the original prose as the phase body.
   Delete the Mind drafts (git rm) and, if `ep_campaign.md` is the
   `graphical-ep` epic ledger, repoint that `epics.md` entry's `ledger:` at
   the Cortex file or retire the Mind entry if no Mind members remain.
7. **`batches/2026-08-31-am.md` + `packets/2026-08-31-am.html` +
   `reviews/2026-08-31-am.md`**: all-science; the cortex birth migration map
   (`complete/archive/epics/cortex_birth_epic.md`) says they move to the
   Cortex, and `PyAutoCortex/batches/` already holds a `2026-08-31-am.md`.
   Diff the two; if the Cortex copy is complete, `git rm` the Mind trio,
   else port the missing content first. Fix any `batches/AGENTS.md` or
   status-box reference that assumes the am slot exists in Mind.

Then: `pyauto-brain intake --apply dashboard`, Mind `pytest -q`,
`lifecycle.py check`, Cortex `pytest -q` (its ledger_merge / phase parsers),
open both PRs.
