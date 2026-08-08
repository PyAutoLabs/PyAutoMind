# Teach `lifecycle.py check` to validate the registry files

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

`scripts/lifecycle.py check` reports **OK** on a `planned.md` in which 8 of 12
entries are wrong. The registry is the first thing any task-selection pass
reads, so the rot is not cosmetic — it actively costs sessions. This task closes
that gap: extend `cmd_check` to validate the registry files, then fix what it
finds.

## Why now (measured, 2026-08-08)

A task-selection pass picked the two highest-leverage `planned.md` entries and
spent most of a session discovering **both were already fixed on main**:

- **`notebook-kernel-cwd-auto-simulate`** (PyAutoHands#204) — FIXED.
  `autohands/build_util.py:302` no longer shells out to
  `jupyter nbconvert --execute`; it runs `autohands/run_notebook.py`, which sets
  `resources['metadata']['path']` through the Python API so the kernel starts at
  the repo root. The in-code comment describes this exact bug. Verified on
  PyAutoHands main at `a5bac76`.
- **`auto-simulate-guard-wrong-simulator-target`** (autolens_workspace#359) —
  FIXED. All 246 `should_simulate` guards in autolens_workspace were audited
  against the 54 simulators' declared `dataset_type`/`dataset_name` outputs:
  **236 resolvable, 0 mismatches.** The 10 unresolved are benign — a simulator
  matching its own glob, `guides/hpc/example_cpu_and_gpu.py` (path built from an
  `hpc_dataset_path` variable), and the `guides/results/` scripts whose first
  subprocess target is the `_quick_fit.py` helper rather than a simulator.

Neither entry had a prompt file, so neither was reachable through the normal
`$start-dev` path — the staleness was only discoverable by reading upstream
code.

## The drift, classified

`planned.md` holds 12 entries. Resolving each `prompt:` path through the
fallback chain that `AGENTS.md` documents (`draft/<rel>`, bare `<rel>`,
`active/<name>`):

| Class | N | Entries |
|---|---|---|
| Prompt file never existed in git history | 2 | `notebook-kernel-cwd-auto-simulate`, `auto-simulate-guard-wrong-simulator-target` |
| Prompt file truly missing | 3 | `heart-ci-linkage`, `heart-release-validation`, `heart-release-profile-wheel-integration` |
| Legacy `PyAutoMind/<type>/<target>/` path, resolves only via fallback | 3 | `samples-parameter-paths`, `nfw-truncated-potential-accuracy`, `piemass-potential` |
| State contradiction | 1 | `build-testpypi-rehearsal-mode` — `status: planned`, but its prompt is in `active/` |

Only 4 of 13 entries had an exactly-correct prompt path.

**Six of the thirteen were work that had already shipped.** Chasing each of the
five missing-prompt entries to its upstream repo found the capability live on
main in every case:

| Entry | Milestone | Shipped as |
|---|---|---|
| `notebook-kernel-cwd-auto-simulate` | — | PyAutoHands `build_util.py:302` → `run_notebook.py`, setting `resources['metadata']['path']` |
| `auto-simulate-guard-wrong-simulator-target` | — | autolens_workspace: 236 resolvable guards, 0 mismatches |
| `build-testpypi-rehearsal-mode` | M1 | PyAutoHands `release.yml` — `rehearsal` dispatch input, `resolve_mode` job, downstream jobs gated `if: rehearsal != 'true'`, dev-segment version output. Entry targeted "PyAutoBuild", which is now PyAutoHands |
| `heart-ci-linkage` | M0 | PyAutoHeart `heart/checks/ci_status.{sh,py}` + `tests/test_ci_status.py`; the script's own comment says it "replaces the old `gh run list --limit 1`" — verbatim the defect the entry described |
| `heart-release-validation` | M2 | PyAutoHeart `pyauto-heart validate --ingest` → `heart/validate.py`, `validation_report.json`, `.github/workflows/release-integrate.yml` |
| `heart-release-profile-wheel-integration` | M3 | PyAutoHeart `heart/validate.py` carries the named `release` profile and gates fidelity on `profile == release`; TestPyPI wheel install in `heart/checks/verify_install.sh` |

The whole M0–M3 release-validation milestone chain shipped without a single
registry entry being retired. That is the cost this check exists to prevent.

## Why `check` misses all of it

`cmd_check` (`scripts/lifecycle.py:376`) validates exactly two conditions:

1. an `active.md` slug that also has a `complete/` record;
2. a filename present in both `active/` and `complete/`.

It never opens `planned.md` or `parked.md`, and never resolves a `prompt:` path
in any registry file. `scripts/lifecycle.py` also has **no test** —
`tests/` holds only `test_repos_sync_hygiene_coverage.py`,
`test_spawn_privacy.py`, `test_spawn_template_contract.py`.

## Scope

Two legs, one PR — the data fix is required for the new check to land green.

**Leg 1 — the check.** In `cmd_check`, parse `## <slug>` entries and their
`- key: value` fields from `active.md`, `planned.md` and `parked.md`, and add:

- **Prompt resolution** — every `prompt:` path resolves through the documented
  fallback chain, else `DRIFT`. Report the resolved location when it differs
  from the literal path, so legacy paths are visible rather than silently
  absorbed.
- **State contradiction** — a `planned.md`/`parked.md` entry whose prompt lives
  in `active/` (it is issued) or under `complete/` (it shipped) is drift. This
  is the check that would have caught `build-testpypi-rehearsal-mode`.
- **Slug uniqueness** — a slug must not appear in two registries at once.

Match the existing `problems` list + `lifecycle check: DRIFT` output shape; do
not change the exit-code contract (`0` OK, `1` drift).

**Leg 2 — reconcile the 8 entries.**

- Rewrite the 3 legacy paths to their exact `draft/...` form.
- Remove the 6 verified-shipped entries, citing the evidence table above. The
  M0–M3 chain needed no reconstruction from its `summary:` blocks after all —
  every milestone was already live upstream.
- Removal is the right disposal, not a fabricated `complete/` record: these
  shipped under other tasks' PRs, and inventing dated records with merge
  evidence nobody verified would put a worse lie in a more trusted place.

**Leg 3 — `tests/test_lifecycle_check.py`.** Drive the real `cmd_check` against
fixture registry trees (tmp_path with `draft/`, `active/`, `complete/` and
synthetic registry files) — one case per new condition, plus a clean tree
asserting `OK`. Follow `test_repos_sync_hygiene_coverage.py` for style.

## Explicitly out of scope

- **Online issue cross-checking.** A local check catches the two shipped entries
  only because their prompt files are missing; had the files existed, nothing
  offline would flag "this shipped upstream". Catching that class needs each
  entry's `issue:` cross-checked against GitHub, which makes `check`
  non-hermetic and credentialed. Decided 2026-08-08 to keep `check` offline;
  filed as a follow-up idea instead.
- **Closing the upstream issues.** ~~PyAutoHands#204 and autolens_workspace#359
  are still open~~ — **wrong, corrected 2026-08-08.** Both were closed as
  `completed` on 2026-07-28, eleven days before this audit called them open.
  That claim was inferred from PyAutoMind's own stale registry rather than read
  off GitHub, which is the exact mistake this task exists to stop. No
  `/issue_cleanup` is owed.

  This sharpens the conclusion. **The trackers were accurate the whole time;
  only the Mind was stale.** Every one of the six shipped entries had correct
  upstream state available — a closed issue, a merged PR, a live capability on
  `main` — and none of it reached `planned.md`. The drift is not GitHub going
  out of date, it is the Mind never reading back. That is the strongest
  argument for the online cross-check ruled out of scope above: the signal it
  would consult was already correct and already free.
- **The orphaned `active/` prompt.** Removing `build-testpypi-rehearsal-mode`
  from planned.md leaves `active/release_yml_testpypi_rehearsal_mode.md` sitting
  in `active/` with no registry entry — shipped work whose prompt was never
  advanced to `complete/`. `check` does not look for prompts that no registry
  claims, so this is invisible to it. Two follow-ups, both deliberately not
  taken here: give that prompt a proper `complete/` record via the ship path,
  and add an orphan-prompt check (every `active/*.md` is claimed by an
  `active.md` or `parked.md` entry) — the mirror of the checks added here.
- `condemned.md`, `queue.md` and `ideas.md` — different schemas, no `prompt:`
  field. Not covered.

## Acceptance

- `python3 scripts/lifecycle.py check` exits `0` on the reconciled tree, and
  exits `1` with a named problem for each of the three new conditions when
  seeded with a fixture that violates it.
- `pytest tests/test_lifecycle_check.py` green.
- No entry left in `planned.md` whose prompt path does not resolve exactly.
