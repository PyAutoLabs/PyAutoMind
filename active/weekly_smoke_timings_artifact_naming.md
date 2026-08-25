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
