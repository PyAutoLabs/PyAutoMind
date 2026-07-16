# Release does not sync __version__ stamps and workspace pins back to main

Type: bug
Target: PyAutoBuild
Repos:
- PyAutoBuild
- PyAutoHeart
- PyAutoConf
- autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Symptom

A successful release (including the nightly build) leaves the organism's version
references in a **split, stale state**. After the `2026.7.9.1` release the whole
stack was still stamped with the now-yanked `2026.7.6.649` in five library
`__init__.py` files, every workspace `version.txt` / `config/general.yaml:
workspace_version` pin, and two READMEs — while the same repos' Colab URLs had
already moved to `2026.7.9.1`. Fixing it by hand took a 15-repo bump on
2026-07-13.

## Root cause

`PyAutoBuild/.github/workflows/release.yml` bumps and pushes to `main` only:

- Colab URL tag refs (`release.yml:652,697`),
- regenerated notebooks (`:605`),
- stamped wheels + git tags (`:403,411`).

It intentionally does **not** commit back to `main`:

- library `__init__.py` `__version__` — `sed`'d for the wheel only (`:128,403`),
  never committed to the library mains,
- workspace `version.txt` / `config/general.yaml:workspace_version` — the
  "Write workspace version" step was **removed** under **PyAutoBuild#120**'s
  compatibility-floor redesign (`:607-611` comment).

So a release moves the URLs and tags but freezes the `__version__` stamps and
version pins → the observed drift.

## Fix

Make a successful release bump **every live version reference consistently** and
commit it back, so this stale/split state cannot recur. Expected scope:

- `PyAutoBuild/.github/workflows/release.yml` — re-add (or re-model) the
  write-back of library `__init__.py` stamps and workspace pins alongside the
  existing Colab-URL / notebook / tag commits.
- `PyAutoBuild/pre_build.sh` — the README "pkg vX" pin bump path (`:53`) that
  also drifted.
- `PyAutoHeart` `version_skew` check — `internals.md` already flags it "needs a
  follow-up rework to compare floors against release tags rather than
  stamp-vs-pin"; reconcile it with whatever model this fix adopts.

## Constraints / design note

This partially reverses/extends the **PyAutoBuild#120** floor-model redesign
(wheels/tags as the release anchor, `minimum_library_version` as a deliberate
floor). Weigh the churn vs. consistency tradeoff #120 was avoiding, and respect
the never-rewrite-history rules, before choosing between "commit stamps back to
every main on each release" vs. an alternative that keeps mains authoritative.

**Must NOT touch** historical/provenance references to old versions:
`autolens_profiling/**` result files and filenames (e.g. `..._v2026.7.6.649.json`),
`scripts/yank_pypi_browser_console.js` (the yank list), PyAutoHeart/PyAutoConf
test fixtures, and PyAutoMind history.

## Findings 2026-07-15 — the fork above, with evidence

Triggered again by the `autolens_assistant` session-start drift check reporting
`autolens: 2026.7.15.1 -> 2026.7.9.1` (all five libraries, exit 1) after the
`2026.7.15.1` release. **This section adds evidence for the fork the "Constraints
/ design note" above deliberately deferred; it does not decide it.**

### Measured, not inferred

- The local checkout **is exactly the release**: `git describe --tags` in
  PyAutoLens = `2026.7.15.1`; all five repos clean vs `origin/main`.
- `origin/main` carries `__version__ = "2026.7.9.1"` for **all five** libraries.
  **There are no stamps on main to pull.** The only unpulled commits were
  `Release 2026.7.15.1: bump Colab URL tag refs`, touching zero `__init__.py`.
- The `2026.7.15.1` **tag itself** also carries `__version__ = "2026.7.9.1"`.
- The published wheel `autolens-2026.7.15.1-py3-none-any.whl` **does** carry
  `__version__ = "2026.7.15.1"`. `release.yml:403` behaves exactly as documented.
- The drift check reports **only** version-string drift and **zero API-surface-hash
  drift** — the documented and installed APIs are byte-identical. The version
  comparison is redundant with the hash it already computes, and strictly worse.

### Root cause of the false positive (new)

`autolens_assistant`'s `api_audit_baseline.json` is generated in a **clean venv
against real wheels**, where stamps are correct (see
`complete/2026/07/assistant-pin-bump-2026-7-9-1.md`: *"Verified via clean-venv
`--write-baseline` … vs real 2026.7.9.1 wheels"*). The daily driver runs the
libraries from **source checkouts on PYTHONPATH**, where stamps are frozen by
design under #120. **Baseline is wheel-derived, check is source-derived ⇒ a
structurally permanent false positive, independent of release cadence.**

Consequence for fork (a): committing stamps back to main **would not reliably fix
this**. It would hold only between pulling and the next release, and return
mid-cycle. The Symptom above is real, but this particular trigger is not evidence
for (a).

### The wider pattern

PyAutoConf#118 / PyAutoBuild#120 moved the model to compatibility **floors**
(`autoconf/workspace.py:146` — older raises, newer passes) and made releases
wheels+tags-only. **The consumers were never updated.** Three now read a floor as
an exact pin:

1. `autolens_assistant` `audit_skill_apis.py --check-version` — exact equality on
   `__version__`; the last exact-pin holdout in the stack.
2. `PyAutoHeart` `version_skew` — "compares frozen stamps"
   (`draft/feature/pyautoheart/version_skew_floor_rework.md`).
3. Workspace floors not yet adopted
   (`draft/feature/workspaces/minimum_library_version_adoption.md` — *floors need
   an installable version*).

This reframes the fork: the defect may be **the consumers misreading the model**,
not the missing commits.

### The part the floor model does NOT excuse

After `2026.7.9.1`, mains carried floors pointing at the **yanked** `2026.7.6.649`.
A floor must always name an *installable* version. That is a genuine bug and worth
fixing whichever fork wins — and it is the strongest surviving argument in the
Symptom above.

### Recommendation to weigh (explicitly not decided)

Fork (b), *keep mains authoritative*: adopt installable floors, rework the two
stale consumers, and make the assistant check source-checkout-aware (`git
describe` when a module resolves to a checkout, else `__version__`) — or drop its
version equality entirely in favour of the API-surface hash that already passes.
Then rewrite or shelve this prompt with the reasoning recorded.

Counterweight for (a): #120 removed the commit-backs after they caused stale CI
storms, an email flood and an org-wide cron pause. Re-adding them rebuilds that
engine. But (a) is the only fork that makes `__version__` on main *true*, which is
the recurring human expectation — see below.

### Note for whoever picks this up

This idea has now surfaced by hand **twice**: the 15-repo bump on 2026-07-13, and
again 2026-07-15. A memory documenting the floor design did not prevent either.
Documenting the trap is not working — prefer **deleting the false signal** that
prompts the urge (the exact-equality check) over explaining why the signal is
wrong.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake; re-homed triage/ -> bug/pyautobuild/ by hand (classifier low-confidence) -->
<!-- Findings 2026-07-15 appended by hand from a CLI session (/intake, folded into this prompt rather than filed as a duplicate research/ prompt). -->

## DECIDED 2026-07-16 — fork (b): mains stay authoritative

Human decision (build-chain campaign PyAutoBuild#155 Phase 4, "follow the
recommendation"): do **not** re-add stamp/pin commit-backs to main — that
rebuilds the CI-storm/cron-pause engine #120 removed, and the 2026-07-15
findings showed it would not even fix the recurring trigger (wheel-derived
baseline vs source-derived check is release-cadence-independent).

Execution programme (each its own task, serialised on claims):
1. `draft/feature/workspaces/minimum_library_version_adoption.md` — adopt
   installable floors in the 7 workspace configs, drop legacy keys.
   (autolens_workspace currently claimed by jax-joss-benchmarks — serialise.)
2. `draft/feature/pyautoheart/version_skew_floor_rework.md` — re-point the
   Heart leg at floors-vs-release-tags, and make it enforce the one invariant
   nothing guards today: **a floor must name an installable (non-yanked)
   version** (Phase 2 audit finding B: the current leg is unfailable by
   releases). Depends on 1.
3. `autolens_assistant` `--check-version`: source-checkout-aware (git
   describe for checkouts) or drop version equality for the API-surface hash
   that already passes — kills the structurally-permanent false positive.
4. README version pins: per the Phase 1 audit (#157) they are orphaned;
   under fork (b) the runner owns them or they leave the READMEs in favour of
   "install the latest release" — decide in task 1's plan alongside the
   floors.

This prompt stays filed as the Phase 4 tracker until tasks 1–3 ship; the
Symptom section above remains accurate history, and the "15-repo hand bump"
urge it documents is answered by deleting the false signals (3), not by
resurrecting commit-backs.
