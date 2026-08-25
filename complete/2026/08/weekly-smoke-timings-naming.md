# The weekly sweep's smoke timings now have a name a consumer can glob for

PyAutoHeart#182 → `9e3f1c8` (closing PyAutoHeart#181), merged 2026-08-25.
Follow-on gap from `complete/2026/08/smoke-timings-dataset.md`, filed the day
before by the retime-sweep record. Small, self-contained CI wiring — but the
verification is where the substance is.

## What shipped

- **`workspace-validation.yml` gained a named timing upload on both legs** —
  `run_scripts` and `run_notebooks` — alongside (not replacing) their existing
  `results-*` uploads. `smoke_timings.json` had been written into every report
  dir since PyAutoHands `d2a22f4`, but only the **PR gate** (`smoke-tests.yml`,
  PyAutoHeart#167) published it under a name. The weekly channel goes through a
  different body, so the widest timing sample the organism produces survived
  only *inside* the per-leg `results-*` zips and expired with them at 30 days.
- **The artifact name carries the leg**:
  `smoke-timings-{scripts,notebooks}-<project>-<directory>`. That was the
  prompt's named trap — the PR gate has two legs per run and a fixed name is
  safe there; this body runs ~98. The `(project, directory)` pair is exactly
  what the sibling `results-*` names already rely on the script matrix to keep
  unique.
- **Only the JSON is uploaded, and deliberately with no `retention-days`**
  (the `results-*` siblings use 30). The report dir already ships as
  `results-*`; the gap was discoverability, not payload. Dropping the retention
  cap means the dataset now *outlives* the zips it was extracted from —
  confirmed live: `smoke-timings-scripts-autolens-imaging` expires 2026-11-23
  against its `results-*` sibling's 2026-09-24.
- Six tests in `tests/test_workflow_wiring.py`, beside the existing PR-gate
  timing tests. Heart suite 641 passed; PR gate green on both legs.

## Key traps / findings

- **Two artifact namespaces, two contracts — keep them apart.** `results-*` is
  what `analyze` downloads and hands to `aggregate_results.py`, which globs
  `**/*.json` and skips the timing sidecar **by name**. Publishing timings under
  a `results-*` name would have aimed them at the one consumer that
  deliberately excludes them. A test pins the separation.
- **Option (b) was a promise, not a fix.** The prompt offered widening the
  deferred phase-3 board ingester to also glob `results-*`. Grepping first
  settled it: nothing in PyAutoHeart referenced `smoke-timings` outside
  `smoke-tests.yml` and its tests — the ingester does not exist, so there was
  no contract to widen.
- **`if: always()` earned its place on the first real run.** The one script leg
  that failed still published its timings — including the `TIMEOUT` row and the
  cap it hit, which is the single most valuable row in the dataset.
- **`failed_only` log queries paginate.** A `get_job_logs(failed_only=true)`
  call reported "1 failed job" on a 71-job run; the PR's check-run list showed
  **four**. The first answer was a page, not a total. On a wide matrix, count
  failures from the check-run list, never from a single log query.
- **Dispatching a verification sweep on the feature branch attaches its checks
  to the PR.** Because run and PR share a head sha, ~138 check runs (including
  the reds) landed on PyAutoHeart#182. `mergeable_state` stayed `clean` — the
  weekly channel is not a required check — but it makes the PR look red to a
  human. Worth knowing before doing it again.

## Verification (the part worth keeping)

A full weekly sweep was dispatched on the branch —
[run 32902243623](https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/32902243623),
`referenced_workflows` resolving to `workspace-validation.yml@5829bbb`, so it
exercised the branch body rather than `main`'s.

```
203 artifacts = 1   workspace-validation-report
              + 6   notebooks-<project>   (generate_notebooks runs nothing — no timings by design)
              + 196 → 98 results-* / 98 smoke-timings-*
```

One-to-one across every executed leg. **No name collisions** — not one upload
step failed in the whole run, which is the proof, since `upload-artifact@v4`
hard-fails with a 409 on a duplicate.

Baseline for contrast: the 2026-08-24 weekly run `32688412626` produced 109
artifacts and zero `smoke-timings-*`.

### The sweep's four red legs, none of them this change

| Failing job | Cause |
|---|---|
| `run_scripts (autolens_test, multi_dataset)` | `jax_likelihood/shared_preloads.py` → `TIMEOUT (300s)` |
| `run_notebooks` ×3 (howtofit ch1, howtogalaxy ch2 + ch4) | DNS failure fetching `actions/download-artifact@v4` from `internal-api.service.iad.github.net`, all dying in "Prepare all required actions" before any step, within one ~3-minute window |
| `smoke / analyze` | designed downstream consequence — "Fail the run if validation is not ready" |

The scripts failure is at step 9 (`run_python.py`); the new step 12 then ran and
succeeded (690 bytes, artifact 9583834034). The three notebook legs produced
neither a `results-*` nor a `smoke-timings-*`, which is why the 98/98 pairing
is unaffected.

## Follow-ups

- **`shared_preloads.py` belongs on the jax-stall ledger.** It is a
  `multi_dataset/jax_likelihood` family member **not** on
  `draft/bug/ci/jax_vmap_jit_compile_stall.md`'s list (which names `mge.py` and
  `rectangular_mge.py`). 16/17 scripts passed and its siblings ran 11.7s /
  20.7s / 49.3s, so the >6x outlier is the same bimodality signature. Not added
  to that ledger by this task.
- The phase-3 Heart-board timing ingester (deferred in
  `complete/2026/08/smoke-timings-dataset.md`) now has one glob to write
  against — `smoke-timings-*` — covering both the PR gate and the weekly sweep.

## Original prompt

# The weekly smoke run's timings land in `results-*` under no discoverable name

Type: maintenance
Target: pyautoheart
Repos:
- @PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: low
Status: issued
Filed: 2026-08-24
Issued: 2026-08-25

Follow-on gap from `complete/2026/08/smoke-timings-dataset.md` (PyAutoHands
`d2a22f4` + PyAutoHeart#167 `3df42b5`, merged 2026-08-24). All facts below
verified 2026-08-24 via the Actions API.

## The gap

`RunReport.write()` now emits `smoke_timings.json` (schema `smoke_timings/1`)
in **every** report dir, but the named upload
(`smoke-timings-<python-version>`, `if: always()`, `if-no-files-found: ignore`)
was added only to the reusable **PR-gate** workflow
`@PyAutoHeart/.github/workflows/smoke-tests.yml`.

The weekly `workspace-smoke.yml` run goes through
`@PyAutoHeart/.github/workflows/workspace-validation.yml`, which has no such
named upload — e.g. run `32688412626` (2026-08-24 04:00 UTC, success,
136 jobs).

Its `run_scripts` / `generate_notebooks` legs *do* emit the file now. Verified
differentially: the `results-scripts-autolens-imaging` artifact grew from
**2 files / 3,950 bytes** (2026-08-19, run `32277952488`) to **3 files /
5,306 bytes** (2026-08-24, PyAutoHands at `d2a22f4`). So the weekly timing
data — by far the widest sample the organism produces — persists only *inside*
the per-leg `results-*` zips, under no name a consumer can glob for.

## Task

Pick one and record the decision in the PR body:

- **(a)** Add the same named upload to `workspace-validation.yml`'s script and
  notebook legs (`if: always()`, `if-no-files-found: ignore`). Simpler and
  symmetric with the PR gate — **preferred unless (b) proves cheaper.**
- **(b)** Explicitly commit the deferred **phase-3 Heart-board timing
  ingester** (the follow-up named in `complete/2026/08/smoke-timings-dataset.md`)
  to globbing `smoke_timings.json` out of `results-*` artifacts as well as
  `smoke-timings-*` ones, and say so in that contract.

**Trap for (a): artifact-name collisions.** The PR gate has one leg per python
version, so a single fixed name is safe there. The weekly run has ~50+ legs in
one run, so a fixed `smoke-timings-<python-version>` would collide — the name
must carry the leg's package/directory (mirroring how `results-*` is already
disambiguated, e.g. `results-scripts-autolens-imaging`).

## Acceptance

- Weekly-run timing data is either published under a predictable
  `smoke-timings-*` name, **or** the ingester contract explicitly covers
  `results-*` — not left implicit either way.
- No change to PR-gate behaviour (`smoke-tests.yml` untouched, or provably
  equivalent).
- `workspace-validation.yml` stays green; no artifact-name collisions in a
  full weekly run.
