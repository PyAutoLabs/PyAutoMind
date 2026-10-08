## search-ext-b1-registration
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/492
- completed: 2026-10-08
- epic: search-extensibility (phase B1 registration)
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/1
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/1
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/493
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/292
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/60
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/33
- workspace-pr: https://github.com/PyAutoLabs/.github/pull/34
- merge-commit: PyAutoMind ba34fdb5; PyAutoHeart 8a6ebee353e75963f05bf66f4d37a4324a88a7d2

### Outcome
The two new fit benchmark repos (autofit_inference, autofit_profiling) are registered across the organism: lint-green skeletons with AGENTS.md and hooks on main; Mind `repos.yaml` rows propagated by `repos_sync`; Heart lists both as excluded; Cortex carries a `planned` row; Pulse adopts `tasks/autofit_profiling_bootstrap.md` as B4; the org profile table lists both. Five PRs merged 2026-10-07, Heart#292 and .github#34 on 2026-10-08 (human merge OK for the CI-less org profile). Clears the Heart manifest-drift YELLOW. RAL clones pulled at the skeleton heads.

### Validation and limits
Heart#292 was red on the pre-existing PyAutoBrain#499 theme change, fixed by PyAutoHeart#293 (test relaxed to the `dashboard.md` href; 129 dashboard tests locally, both CI legs green) and re-run green after merging main. Approved deviations: no Pulse/Insight registry rows at B1 (their `check` fails an instance without a published summary; rows land in B4a/B3); Cortex row `planned` until B3. Trap: registry PRs conflict on generated dashboard files when main moves; merge main and re-render with the explicit repo flag. `repos_sync --write --root <bundle>` refuses symlinked checkouts; run with `--skip "shared-standards blocks (generated)"` then `--only ... --repo X`.

## Original prompt

# Register autofit_inference and autofit_profiling across the organism, with minimal skeletons (epic search-extensibility, phase B1 registration)

Type: feature
Target: autofit
Repos:
- autofit_inference
- autofit_profiling
- PyAutoMind
- PyAutoHeart
- PyAutoCortex
- PyAutoPulse
Themes:
- inference
- profiling
- infrastructure
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: search-extensibility
Status: active
Filed: 2026-10-07
Issued: 2026-10-07

Phase B1 (registration half) of the search-extensibility epic
(`draft/research/autofit/search_extensibility_epic.md`; plan in
`search_extensibility_epic_report.md` §4 B1; skeleton table in
`search_extensibility_epic_surveys/04_inference_profiling_infra.md` §6). The
human gate half of B1 (two `gh repo create`) passed 2026-10-07: both repos
exist on GitHub, public, MIT, one Initial commit with LICENSE, and are cloned
at `fit/autofit_inference` and `fit/autofit_profiling`. Those undeclared
checkouts are today's Heart manifest-drift YELLOW
(`repos_sync.py --check` → "workspace checkouts (manifest ↔ disk): 2
mismatch(es)"); this phase clears it.

## Original request (verbatim from the epic plan)

"B1 — Births and registration (HUMAN GATE; no dependencies). Repos: the new
`fit/autofit_inference` and `fit/autofit_profiling`, plus PyAutoMind,
PyAutoHeart, PyAutoCortex, PyAutoBrain and the org `.github`. Scope: two
`gh repo create` calls; skeleton PRs copied per `surveys/04 §6`, carrying the
`repos_sync:*` blocks and a layout allowlist for `.claude/`+`CLAUDE.md`; Mind
`repos.yaml` rows, then `repos_sync --write` (run with `PYAUTO_ROOT` asserted
in a private env), `ROUTING.md` and `epics.md`; Heart `excluded:`; a Cortex
row for autofit_inference; Brain `clean_slate.sh`; org profile rows; a RAL
clone plus `hpc/sync check`; adopt the Pulse task `autofit_profiling_bootstrap`:
answer its open question and link it to this epic. Verify: `repos_sync
--check`, `cortex.py check`, both `lint.yml` runs green, `hpc/sync check`
reaches RAL. Witness: both repos are checked out at their declared paths, and
`repos_sync --check` and `cortex.py check` are green."

Brief addendum (2026-10-07): "B1 registration (Mind repos.yaml → repos_sync,
Heart excluded, Cortex row, Pulse `fit` @profiling-summary@2, Insight `fit`
@inference-summary@1; adopts PyAutoPulse `tasks/autofit_profiling_bootstrap.md`)".

## Scope (as surveyed 2026-10-07)

1. **Skeleton PRs, one per new repo**, minimal and lint-green on an empty repo:
   `AGENTS.md` with the four `repos_sync:*` marker pairs (history markers are
   what lets `--write` self-install deliverable/filing/standards), `AI_POLICY.md`
   pointer, `ruff.toml` (root sentinel), `.gitignore`, `README.md`, `activate.sh`
   (fit-only PYTHONPATH: Nerves + Fit; RAL shared-venv branch), `hpc/{sync,
   sync.conf.example, README.md}` with `PROJECT_NAME=<repo>` and a `batch_cpu`
   template only (`--partition=ral`), and a `lint.yml` that runs only what
   exists (ruff check/format, lychee over README). autofit_inference also gets
   `CORTEX.md` and `wiki/project/{state,_template}.md`. No harness, datasets,
   exporters or dashboards (B2/B4a). No `scripts/validate_structure.py` (so no
   layout allowlist is needed; if one is ever added, `.claude` must be in
   `ALLOWED_TOP_DIRS`).
2. **Mind**: two `repos.yaml` rows mirroring `autolens_inference`/
   `autolens_profiling` (`category: project`, `role`), `repos_sync --write`
   from the resolved checkout (root `AGENTS.md` routing rows, hooks and blocks
   into both new repos, folded into the skeleton PRs), `ROUTING.md` targets
   example, `epics.md` status. Hand-edit the family index `fit/AGENTS.md`
   (not generated, not under git) to add both rows.
3. **Heart**: two `excluded:` lines in `config/repos.yaml` (documentation only;
   not polled).
4. **Cortex**: a `projects.yaml` row for `autofit_inference` mirroring the
   autolens_inference row with `status: planned` (no ledger needed until B3's
   first runs flip it to `active` via `cortex.py new`), `ral_root:
   /mnt/ral/jnightin/autofit_inference`, `partition: ral`, `assistant:
   autofit_assistant`.
5. **Pulse**: adopt `tasks/autofit_profiling_bootstrap.md` with a dated
   check-in linking this epic (its open question, repo creation, is answered)
   and update the `campaigns.yaml` task `next:`. **No `registry.yaml` row**:
   Pulse `check` fails any instance without a published summary and has no
   pending status; the `fit` @profiling-summary@2 row lands in B4a as planned.
6. **Insight**: likewise **no row** at B1; the `fit` @inference-summary@1 row
   lands in B3 as planned. Record both intended instance names in the ledger.
7. **Brain**: no `clean_slate.sh` entry needed (the lens siblings have none;
   `_repo_paths.py` reads Mind `repos.yaml`). Do not hardcode the new names in
   any Brain/Heart/Hands script (repos_sync firewall).
8. **Org profile**: two rows in the PyAutoFit table of
   `.github/profile/README.md` (checkout `/home/jammy/Code/PyAutoLabs/.github`,
   PyAutoLabs/.github), one PR.
9. **RAL**: `git clone` both repos to `/mnt/ral/jnightin/<project>` over
   `euclid_jump`, then `hpc/sync check` from each local repo.

## Order

Skeleton PRs first (an `AGENTS.md` must exist before `repos_sync --write`),
then Mind (its PR waits for the skeletons to merge if its lint checks them
out), then Heart/Cortex/Pulse/.github in any order. Pulse and Insight CI
resolve `repo` against PyAutoMind main, so nothing in them references the new
repos before the Mind PR merges.

## Verification

`repos_sync.py --check` green (the two mismatches gone); `cortex.py check`
green; both skeleton `lint.yml` runs green; `pyauto-pulse check --offline`
green; Heart tick → manifest drift clear; `hpc/sync check` reaches RAL and
finds both remote roots.

## Witness

Both repos checked out at their declared `fit/` paths and declared in
`repos.yaml`; `repos_sync --check` and `cortex.py check` green; Heart's
manifest-drift YELLOW reason gone at the next tick.
