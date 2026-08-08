# build-testpypi-rehearsal-mode

- shipped: 2026-06-30
- pr: https://github.com/PyAutoLabs/PyAutoHands/pull/111
- commit: `71936fb47c19fd6ba7b64fa9283bf7231e47b165`
- repos:
  - PyAutoHands (the prompt targets "PyAutoBuild", this repo's former name)
- milestone: M1 — prerequisite for the Heart release-validation gate (M2)

## RECORD RECONSTRUCTED AFTER THE FACT (2026-08-08)

This record was **not** written at ship time by `ship_library`. The task shipped
on 2026-06-30 and nothing in the Mind was updated: the prompt stayed in
`active/`, and `planned.md` went on listing it as `status: planned` for six
weeks. It was found during the registry-integrity audit
(`draft/maintenance/pyautomind/registry_integrity_check.md`) and reconstructed
from upstream git evidence, which is why it carries less detail than a record
written by the ship path — there is no contemporaneous trap/finding log.

Everything below is verified against PyAutoHands `main`, not inferred.

## Summary

Added a TestPyPI-only `rehearsal` mode to `release.yml` so the release pipeline
can build and publish the current source to TestPyPI and **stop** — no PyPI
upload, no git tag, no notebook generation, no Colab-URL bumps. That is what
lets the Heart install and validate the actual wheels before any PyPI
promotion, which is the only way packaging-layer bugs (bad `MANIFEST`, missing
data file, direct-URL dependency) get caught.

## Evidence it shipped

In `PyAutoHands/.github/workflows/release.yml` on `main`:

- a `rehearsal` `workflow_dispatch` input, described in-file as "the one mode
  switch: false (default) = a full real release";
- a `resolve_mode` job publishing `rehearsal` as a job output — the single
  source of truth for rehearsal-vs-live;
- a unique PEP 440 dev segment appended per rehearsal run, so repeated
  dispatches never collide, plus `--skip-existing` on the upload;
- the PyPI/tag/notebook jobs gated `if: needs.resolve_mode.outputs.rehearsal != 'true'`.

The merge commit body states the intent directly: *"to unblock the Heart
wheel-based release-validation gate (M2)"*, and notes it was "Validated live on
run #645".

It has been in production use since: the 2026-08-07 release drive ran Stage 2
as rehearsal run 31192317261 → `testpypi 2026.8.7.1.dev70601`.

## Scope delivered beyond the prompt

The same PR carried a dispatch-surface cleanup the prompt did not ask for:
removed the dead `skip_scripts` / `skip_notebooks` knobs, the redundant
`skip_release` dry-run (rehearsal supersedes it) and the defunct
`update_notebook_visualisations` job, leaving the dispatch surface as
`minor_version + rehearsal`. It also added a pre-upload direct-reference-URL
guard — the `[nss]` `git+` footgun named in the prompt's motivation — and
renamed Pulse→Heart, PyAutoAgent→PyAutoBrain.

## The milestone chain this belonged to

M1 of four, all four now shipped and all four discovered stale in `planned.md`
on the same day: M0 `heart-ci-linkage` (PyAutoHeart `heart/checks/ci_status.*`),
M1 this task, M2 `heart-release-validation` (`pyauto-heart validate --ingest`),
M3 `heart-release-profile-wheel-integration` (the named `release` profile in
`heart/validate.py`). The other three had no prompt file to fold and were
removed from `planned.md` rather than recorded.

## Original prompt

# Add a TestPyPI-only "rehearsal" mode to release.yml

Type: feature
Target: PyAutoBuild
Repos:
- PyAutoBuild
Status: planned
Difficulty: too-large
Autonomy: supervised
Priority: normal
Milestone: M1 — prerequisite for `feature/pyautoheart/release_validation.md` (M2)

## Why

The Heart-owned release-validation pipeline (see
`feature/pyautoheart/release_validation.md`) needs to test the organism against
**built wheels**, not source checkouts — that is the only thing that catches
packaging-layer bugs (a bad `MANIFEST`, a missing data file, a too-loose or
direct-URL dependency). Two real incidents in `complete.md` motivate this: the
PyAutoFit `[nss]` `git+` direct URL silently broke every TestPyPI upload for
weeks, and the nufftax/JAX dependency-floor mismatch produced broken installs —
neither was caught by the source-based validation.

`release.yml` already knows how to build and publish to TestPyPI (its
`release_test_pypi` job), but that capability is **coupled to the full
release** (TestPyPI → PyPI → tag → notebook commits in one flow). We need to be
able to build + publish the current source to TestPyPI **and stop**, so Heart
can install and validate those wheels before any PyPI promotion.

## Task

Add a `rehearsal` (TestPyPI-only) execution mode to `release.yml`:

- A new `workflow_dispatch` input (e.g. `rehearsal: true`, or reuse/extend the
  existing skip flags) that:
  - builds every package from current source and **publishes to TestPyPI**,
  - then **STOPS** — no PyPI upload, no git tag, no `tag_and_merge`, no notebook
    generation/commit to workspaces, no Colab-URL bumps.
- Emit the resolved TestPyPI version string as a workflow output / artifact so
  the caller (Heart / Brain health agent) can install exactly those wheels.
- Keep the existing full-release path untouched and default.

This is intentionally small and isolated — it is the highest-value, lowest-risk
piece and unblocks the rest of the redesign. It does not change the full release
flow; it just exposes "build + TestPyPI, then halt" as a first-class mode.

## Notes / footguns

- Respect the "pure executor" boundary: `release.yml` runs no readiness checks;
  it just builds/publishes. The gate lives in Heart.
- Verify the TestPyPI upload step tolerates re-runs of the same version
  (TestPyPI rejects duplicate filenames) — the rehearsal will be dispatched
  repeatedly. Use a dev/local version suffix or `--skip-existing` semantics as
  appropriate.
- Confirm no `git+` direct URLs leak into any uploaded wheel's metadata
  (the original `[nss]` failure) — a rehearsal that can't upload is the bug
  this whole effort exists to surface early.

## Validation

- Dispatch the rehearsal mode manually; confirm wheels appear on TestPyPI, the
  version string is emitted, and the workflow halts before PyPI/tag/notebook
  steps.
- `pytest` in PyAutoBuild stays green.

## PR

"PyAutoBuild: TestPyPI-only rehearsal mode in release.yml".

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
