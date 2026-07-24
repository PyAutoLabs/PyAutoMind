## Outcome — SHIPPED + MERGED 2026-07-24 (PR #333)
Issue #332 closed. One-line release override mirrors the interferometer
sibling: imaging/features/potential_correction/ sets SMALL_DATASETS=0 in
release (dpsi_factor=2 mesh starved under the cap — July #315 shape; found
during #213). Declaration alternative REJECTED — would lift the smoke cap
too. Smoke byte-identical (273 scripts); release changes exactly the one
matched script.

## Original prompt

# Release profile: imaging potential_correction runs mesh-starved under SMALL_DATASETS

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised

Found during Phase 2b (autolens_workspace_test#213, 2026-07-24), confirmed with
file:line. The release profile exempts the interferometer potential-correction
consumer from the small-datasets cap but NOT its imaging sibling:

- `autolens_workspace/config/build/profile_release.yaml:56-57` —
  `pattern: "interferometer/features/potential_correction/"` →
  `set: { PYAUTO_SMALL_DATASETS: "0" }` (with an explanatory comment at
  :50-55 about dpsi-mesh starvation).
- `autolens_workspace/scripts/imaging/features/potential_correction/likelihood_function.py`
  has NO equivalent: no in-file `full_datasets` declaration, not in no_run,
  not covered by the `imaging/start_here` pattern (:42-43). Under the release
  default `PYAUTO_SMALL_DATASETS: "1"` (:32) it runs capped — the exact
  dpsi-grid-too-sparse failure shape from July (#315).

**Fix:** give the imaging script the same treatment as its sibling — the
doctrine-preferred form is an in-file `__Env__` section declaring
`full_datasets` (with the dpsi-mesh rationale), which covers every profile
and removes the need for the release override pair entirely; consider
converting the interferometer release override to a declaration in the same
pass (both scripts, one PR, resolved-env diff documents the two intentional
release-side changes and confirms smoke unchanged... NOTE smoke: adding
full_datasets also lifts the smoke cap for these scripts — check their smoke
runtimes are acceptable before choosing declaration vs release-override-only).
