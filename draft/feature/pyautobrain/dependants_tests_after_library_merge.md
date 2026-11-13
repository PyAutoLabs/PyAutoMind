# Run dependants' unit tests after a library merge, and name the merge that reddened them (M4.6, second half)

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- PyAutoFit
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: notify
Witness: Merge a deliberately breaking change to a scratch branch of an upstream library, then dispatch the new job against it. Each dependant's unit suite in `config/repos.yaml` `dependencies:` runs and goes red, and its run names the upstream repo and sha. A green upstream merge produces green dependant runs. Heart's dev-ship gate reads the fresh dependant runs, not the last run on the dependant's own `main`.
Review-minutes: 15
Unattended: never
Lane: local-dev

Source: PyAutoBrain#628 (programme M4.6), re-check comment 2026-11-13, from findings REL-6, FLOW-3 and FB-5. The first half of M4.6, the `pyauto-brain ci-verdict` script, shipped on `feature/ci-verdict`. This draft is the half the issue left out of scope.

## What holds today

- After a library's CI finishes on `main`, `lib-tests.yml` job `heart-refresh` dispatches a feed refresh (PyAutoHeart#340).
- The dev-ship gate blocks on CI on `main` of the touched repos and their dependants.
- But nothing **re-runs** a dependant. The refresh re-reads each dependant's last run on its own `main`. An upstream merge that breaks a downstream library (or `autolens_profiling` lint) stays invisible until that repo is next pushed. This happened with PyAutoArray#634 → autolens_profiling#424 (10-15/16) and PyAutoArray#682 → autolens_profiling#523/#524 (11-09).
- The library `main.yml` callers trigger only on push to `main`, pull_request and (Galaxy, Lens) workflow_dispatch. PyAutoArray has no `workflow_dispatch`.

## Proposed change

1. **A post-merge dependants job in `lib-tests.yml`.** On a push to `main` with green unit legs, read the dependants from `config/repos.yaml` `dependencies:`. Dispatch each dependant's unit workflow on its `main` with inputs `upstream=<repo>` and `upstream_sha=<sha>`. Add `workflow_dispatch` with those inputs to every library `main.yml` caller.
2. **Name the cause.** A dispatched run sets its run name to `dependant check after <upstream>@<sha>`. A red one is labelled "caused by sibling main: <upstream>@<sha>" in the Heart feed reason. This is the FB-5 classifier, scoped to runs Heart itself started.
3. **Consumers.** Add `autolens_profiling` lint, and any other consumer that reads generated library surfaces, as a dependant of PyAutoArray/Galaxy/Lens in `dependencies:`. It is then dispatched the same way.
4. **Ledger (FLOW-3, optional slice).** Add a `merged-then-corrected` shadow outcome and a `caused-by:` field to bug records (PyAutoMind `lifecycle.py`). The Mind writer back-annotates the earlier row. Split this into its own task if it grows.

## Out of scope

- Stage 3 library suites against the release wheels, and publish atomicity (REL-6's release half). These were not re-checked on 2026-11-13.
- Testing a stacked PR against its sibling branch (FB-5's `depends-on` idea).

## Open decisions (human)

- Dispatch on every library merge, or coalesce bursts with a concurrency group, as `heart-health.yml` does?
- Should a dependant red caused by an upstream merge block the upstream repo's next dev-ship, or only the dependant's?
