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
| State contradiction | 1 | `build-testpypi-rehearsal-mode` — `status: planned`, but its prompt is in `active/`, i.e. issued and in flight |

Only 4 of 12 entries have an exactly-correct prompt path.

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
- Move `build-testpypi-rehearsal-mode` to `active.md`, or correct its `status:`
  — whichever matches the issue's real state at implementation time.
- Remove the 2 verified-shipped entries, citing the evidence above.
- The 3 `pyautoheart/` entries have no prompt file: either write the prompt from
  the entry's existing `summary:` block (each carries a substantial one) or move
  the entry to `ideas.md`. **Human call at implementation time** — these are the
  M0–M3 release-validation milestone chain and may still be wanted.

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
- **Closing the upstream issues.** PyAutoHands#204 and autolens_workspace#359
  are still open on trackers outside this task's repo. Flagged here for a later
  `/issue_cleanup` run; this PR touches PyAutoMind only.
- `condemned.md`, `queue.md` and `ideas.md` — different schemas, no `prompt:`
  field. Not covered.

## Acceptance

- `python3 scripts/lifecycle.py check` exits `0` on the reconciled tree, and
  exits `1` with a named problem for each of the three new conditions when
  seeded with a fixture that violates it.
- `pytest tests/test_lifecycle_check.py` green.
- No entry left in `planned.md` whose prompt path does not resolve exactly.
