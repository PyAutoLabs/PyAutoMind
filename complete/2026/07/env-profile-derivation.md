## env-profile-derivation
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/181 (closed)
- completed: 2026-07-23
- library-pr: PyAutoHands#182 #183 #184; PyAutoHeart#100 #101 #102; PyAutoLens#643
- workspace-pr: autolens_workspace_test#203 #204 #205; autogalaxy_workspace_test#85 #86 #87; autofit_workspace_test#69 #70; autofit_workspace#113 #114; autogalaxy_workspace#149 #150; autolens_workspace#323 #324; HowToFit#30 #31; HowToGalaxy#40 #41; HowToLens#50 #51; autocti_workspace_test#7 #8; euclid_strong_lens_modeling_pipeline#34; PyAutoBrain#154
- summary: Env-profile migration steps 4-8 (build-chain Phase 3 finale), 32 PRs in one day, all merged with branch+main CI green. Step 4: release JAX set DERIVED from name markers (`derive_jax_markers: true`; `jax_*`/`*_jax`/`*_jit` segment/stem) instead of hand-enumerated overrides — 15 JAX-named scripts had NEVER run JAX in the nightly; single `apply_profile()` resolution core (was 3 line-identical copies). 6 files renamed to carry markers honestly (2 mid-stem `_jit_` viz files; 4 explicit-`use_jax=True` scrape scripts). Step 5: validator strict flags wired centrally into Heart's reusable smoke workflow — one edit gates all 9 calling repos. Step 6: `env_vars.yaml`→`profile_smoke.yaml`, `env_vars_release.yaml`→`profile_release.yaml` across 11 workspace repos in 3 stages (dual-name tooling window → 12 rename PRs → legacy names become validator ERRORS); renames proven byte-identical by resolved-env equivalence over 288 scripts. Step 7: PYAUTO_DISABLE_JAX has exactly one reader (af.Analysis.__init__) — fixed a LIVE bug: AnalysisLens.__init__ overwrites self._use_jax and point/weak passed the raw param, so the env downgrade was a silent no-op for AnalysisPoint + weak (red-green proven); nightly impact = 1 script flips to NumPy (point_source/visualization.py, verified 8s pass). Step 8 (use_jax sentinel) DECLINED by human 2026-07-23 — structural gates judged sufficient; recorded on the issue.
- traps: verify config-only changes by resolved-env diff (resolve_clean), never smoke. This gh supports NEITHER text-parsing (`awk $2` hits the "/" in "smoke / smoke (3.12)") NOR `--json` on `gh pr checks` — both fail silently and a zero-checks grace path then merges unverified; always read CI via `gh api repos/<r>/actions/runs`. `pkill -f <script>` inside a compound command kills its own launching shell before later statements run. AnalysisLens-style attribute overwrite after super() is how a single-reader invariant silently breaks — grep for later assignments to the same attribute, not just for env reads. Release cost control = per-script n_like_max caps + no_run + 1800s cap + NumPy-default policy, NOT test mode (TEST_MODE=0 in release).

## Original prompt

# Finish the env-profile migration: steps 4-8 (derivation, strict gate, rename, one-reader, sentinel)

Type: feature
Target: workspaces
Repos:
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- PyAutoHands
- PyAutoFit
- PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Build-chain campaign Phase 3, the last remaining work from the umbrella closed
2026-07-22 (epic PyAutoHands#155). Tracked on **PyAutoHands#161**. Design
merged: `PyAutoHands/docs/env_profile_redesign.md` (#162). Steps 1-3 done:
validator (#163), single resolver, scrubbed baseline env (#165 + profiles).

## What this is about

Each `*_workspace_test` repo has two env profiles under `config/build/`:
`env_vars.yaml` (**smoke** — the per-PR gate) and `env_vars_release.yaml`
(**release** — the nightly mega-run). `PyAutoHands/autohands/env_config.py`
resolves them: a `defaults:` block applied to every script, then an ordered
`overrides:` list of path patterns that flip vars for specific scripts.

In the ag/al **release** profiles `PYAUTO_DISABLE_JAX: "1"` is the default and
JAX is re-enabled by a **hand-enumerated list of ~10 folder patterns**. That
enumeration is the failure mode the whole campaign exists to remove: a
hand-maintained list of paths silently rots as scripts are added or renamed,
and the failure is quiet — a `jax_grad/` script that falls off the list runs
NumPy and asserts a gradient that is all zeros, or tests nothing at all.

The decided policy (design doc §2, human 2026-07-16) is NOT "release =
production defaults" — that was rejected on measured JIT compile cost
(autolens_profiling#71). `mode=release` validates every script on the NumPy
path **plus a derived, loud, bounded JAX set**. Step 4 is what makes that set
derived instead of enumerated.

## Measure first — the 2026-07-17 numbers are stale

Re-run the validator before planning; do not carry old counts into the work.
Measured **2026-07-22** (after the `autobuild`→`autohands` rename and the
dead-entry purge, both of which moved these numbers):

```
python3 PyAutoHands/autohands/validate_env_profiles.py <workspace_test_root>
```

| repo | override-enumeration | JAX-marked but resolves NumPy | unmarked but resolves JAX |
|------|---------------------|-------------------------------|---------------------------|
| autolens_workspace_test | 10 | 11 | 9 |
| autogalaxy_workspace_test | 8 | 4 | 0 |
| autofit_workspace_test | 0 | 0 | 0 (clean — `DISABLE_JAX "0"`, no overrides, the #47 shape) |

The 3 dead patterns the old brief mentioned (ag `quantity/`) are **gone** —
purged by the no_run/env_vars dead-entry campaign. `autofit_workspace_test`
needs no work at all; this task is ag + al.

## Step 4 — the derivation rule (do this first; RELEASE-SURFACE RISK)

Replace the enumerated `PYAUTO_DISABLE_JAX` overrides with one rule in
`autohands/env_config.py`: JAX-on in `mode=release` iff a path segment matches
`jax_*` / `*_jax` / `*_jit`.

**This is not a config tidy — it changes which backend scripts run on.** Every
script below either starts or stops using JAX, and none of the "starts" has
ever run under JAX. Triage each individually: does it pass under JAX, and is it
fast enough for the nightly? Three groups, from the measured lists:

1. **Turns ON (marked, currently NumPy — 15 scripts).** al: `jax_assertions/`
   (8 files, incl. `__init__.py`), `hessian_jax.py`, `profiles_jit.py`,
   `tracer_jax.py`. ag: `jax_assertions/` (4 files). Highest value — files
   literally named for JAX that have never been JAX-validated — and the
   highest chance of a red nightly.
2. **`database/scrape/` (7 files, al).** The one place the rule does not match:
   these need JAX **on** but carry no marker. Decide **rename vs one
   documented parity entry**. The design says no exception list, so a rename is
   the honest option, but it touches paths that `no_run.yaml`,
   `copy_files.yaml` and docs may reference — sweep for references first.
3. **Turns OFF — a regression risk the old brief missed.**
   `imaging/modeling_visualization_jit_delaunay.py` and
   `..._jit_rectangular.py` resolve JAX-on **today** only because the override
   pattern `imaging/modeling_visualization_jit` substring-matches them. Under
   the derivation rule their stems end `_delaunay` / `_rectangular`, so they
   would **stop** getting JAX and silently no-op (the very failure the rule
   exists to prevent). **Resolve this before writing the rule** — it is
   evidence the `*_jit` suffix match is the wrong shape, and a
   segment-contains form may be what the design actually needs.

Also decide what the rule does with `__init__.py` (3 of the counted files are
package inits, not runnable scripts) — probably skip them in the validator
rather than special-case the rule.

**Verification (binding).** Verify by **resolved-env diff, never by smoke**:
run `resolve_clean()` (`autohands/validate_env_profiles.py:56`) over every
script, old profile vs new rule, and read the diff line by line — it must be
exactly the triaged set above and nothing else. Traps from prior config
sweeps: `overrides:` **order is load-bearing** (later entries win; `defaults:`
order is not), and an empty `overrides:` block loads as `None`, not `[]`. And
per the step-3 near-miss: prove it against the **real** CI env, not a synthetic
clean one — a synthetic run passed 65/65 while the real env would have gone
red, because the smoke profiles relied on a `PYAUTO_` var injected by the
workflow rather than by the profile.

The release path is exercised only by the mega-run, not the per-PR gate. Land
behind a rehearsal, or accept mega-run verification and say so on the PR.

## Step 5 — make the validator binding

Flip `--strict-derivation` / `--strict-markers` from warnings to errors and
wire `validate_env_profiles` into the three `*_workspace_test` PR gates.
Depends on step 4 (today it would fail on 42 warnings across ag+al).
Acceptance: a PR adding a JAX-marked script outside the derived set fails its
own gate.

## Step 6 — rename the profiles

`env_vars.yaml` → `profile_smoke.yaml`, `env_vars_release.yaml` →
`profile_release.yaml`. Update `autohands/env_config.py` discovery,
`run_python.py`, `run_smoke.py`, `workspace-validation.yml`, docs. Wide but
mechanical; do it **last**, and re-sweep for the old names after every merge
from main — git rename-detection is blind to *new* files using the old name,
which is how the `autobuild`→`autohands` rename leaked.

## Step 7 — library one-reader fold

`al.AnalysisDataset` reads `PYAUTO_DISABLE_JAX` a second time, *before*
`super().__init__()` (design doc failure mode 8). Fold it into base
`af.Analysis` so there is exactly one reader. Own plan; PyAutoFit + PyAutoLens,
so library-first then workspace. Behaviour-preserving — prove it with a unit
test asserting both construction orders resolve identically.

## Step 8 — `use_jax: Optional[bool] = None` sentinel (HUMAN-GATED)

Only if the human wants "explicitly requested" distinguishable from
"defaulted". Cross-repo API change; **may be declined** — ask before building.

## Suggested phasing

Step 4 is a session on its own (the triage is the work). Steps 5+6 can pair.
Step 7 is independent of 4-6 and could go first if a session is short. Step 8
needs a decision before any code.

<!-- rewritten 2026-07-22 at umbrella close: current validator numbers, the
     modeling_visualization_jit_* turns-OFF finding, the resolve_clean
     verification idiom, post-rename paths (PyAutoHands/autohands/).
     Supersedes the 2026-07-17 filing. -->
