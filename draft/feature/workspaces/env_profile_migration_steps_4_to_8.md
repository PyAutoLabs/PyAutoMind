# Finish the env-profile migration: steps 4-8 (derivation, marker guard, rename, one-reader, sentinel)

Type: feature
Target: workspaces
Repos:
- autofit_workspace_test
- autogalaxy_workspace_test
- autolens_workspace_test
- PyAutoBuild
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Build-chain campaign (PyAutoBuild#155) Phase 3, remaining migration steps.
Design merged: PyAutoBuild `docs/env_profile_redesign.md` (#162). Steps 1-3
done: validator (#163), single resolver, scrubbed base env (#165 + profiles).
Remaining, each green on its own:

- **Step 4 — derivation rule (RELEASE-SURFACE RISK; do carefully).** Replace
  the hand-enumerated JAX-folder override lists in the ag/al release profiles
  with one rule in `autobuild/env_config.py`: JAX-on in mode=release iff a path
  segment matches `jax_*` / `*_jax` / `*_jit`. The validator (#163) found the
  gap: **3 dead patterns** (ag `quantity/`) to delete + **15 vacuous-JAX
  scripts** (11 al + 4 ag, e.g. `profiles_jit.py`, `tracer_jax.py`) that carry
  markers but resolve NumPy. Those 15 have NEVER run under JAX — DO NOT
  blanket-flip; triage each (passes under JAX? fast enough for the nightly?).
  Only `database/scrape/` doesn't match — rename vs parity-list, no exception
  list. The release path is only exercised by the mega-run, not the per-PR
  smoke gate — land behind a rehearsal or accept mega-run verification.
- **Step 5 — flip `validate_env_profiles` --strict-derivation/--strict-markers
  to errors** + wire into the workspace_test PR gates. Depends on step 4.
- **Step 6 — rename profiles** `env_vars.yaml`->`profile_smoke.yaml`,
  `env_vars_release.yaml`->`profile_release.yaml`; update run_python.py,
  run_smoke.py, workspace-validation.yml, env_config discovery, docs. Wide but
  mechanical; last step.
- **Step 7 — library one-reader fold (own plan):** fold `al.AnalysisDataset`'s
  duplicate early `PYAUTO_DISABLE_JAX` read into base `af.Analysis` (failure
  mode 8).
- **Step 8 — `use_jax: Optional[bool] = None` sentinel (HUMAN-GATED cross-repo
  API change):** only if the human wants "explicitly requested" representable;
  may be declined.

Method (binding): prove empty resolve-diff against the REAL CI env, not a
synthetic one (the step-3 near-miss); adversarial pass before concluding.

<!-- filed 2026-07-17 wrapping the build-chain campaign; steps 1-3 done, see #161 -->
