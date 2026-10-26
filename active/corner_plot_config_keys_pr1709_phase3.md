# Workspace config + docs for corner-plot labels and latent plots (phase 3 of PyAutoFit#1709)

Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autofit_workspace/issues/177
Type: docs
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: awaiting-merge
Consequence: glance
Blocked-by: Published PyAutoGalaxy release containing merged #656, current-head CI and human merge decision. Accepted implementation/validation scope is complete.
Library-completion: complete/2026/10/latent-profile-declarations.md
Release-evidence: PyAutoFit 2026.10.23.1 is published/non-yanked and includes #1709 (verified 2026-10-26).
Filed: 2026-10-21

Remainder of `complete/2026/10/finish-pr-1709-corner-plots.md`. The library defaults cover the missing keys, so nothing breaks meanwhile.

- `config/visualize/plots_search.yaml` `nest:` add `corner_anesthetic_components`, `corner_anesthetic_latent` (false),
  `corner_anesthetic_latent_components`, with the library's comments.
- `config/output.yaml` add `latent_model_parameters: true`.
- `config/notation.yaml` `superscript:` comments: it now applies only to priors directly on an unnamed `Model`;
  named components are labelled by their path (`lens.bulge`, `source.pix.reg`).
- Contributor branches `feature/corner-plot-labels` on autofit/autogalaxy/autolens_workspace, HowToLens and HowToGalaxy may
  already carry these; land theirs if so.
- Release note: corner-plot labels change from class abbreviations to component paths (user-visible).

## Approved continuation — 2026-10-26

User request (verbatim): "ok do that" — approving completion of the remaining development and validation against merged Galaxy code, leaving shipping gated on publication.

Resume the five existing contributor branches. Verify their prose against current output paths, plot-only periodic recentering and actual component labels; make only necessary corrections. Regenerate changed notebooks using Hands, execute the affected curated Markdown examples with real sampling or verified completed real-run caches, inspect the latent output/figures, and refresh focused/smoke/review/PR evidence. Preserve all original claims and human merge authority; do not publish or merge these workspace PRs. Record any genuine execution blockers with evidence rather than calling smoke-generated output scientific validation.


## Pre-release preparation checkpoint — 2026-10-26

Approved intent remains: finish examples, generated Markdown and PR validation against merged local Galaxy; do not release or merge workspaces.

- Normal Fit latent cookbook completed. Galaxy imaging completed on full 100×100 data, 5,458 posterior samples, seven generated figures; visual labels and latent summaries verified.
- Twenty notebooks regenerated from canonical scripts. Fourteen edited Python files preserve executable AST; prose now distinguishes plot-only angle recentering and conditional `files/latent/samples.csv` output. Config review removed a duplicate Fit key and preserved CRLF/effective YAML values. Lens config-comment correction remains outstanding.
- Isolated fresh smoke: Fit 8 scripts + 2 notebooks and Galaxy 14 scripts + 2 notebooks passed. Other three suites not started; older 152-check result is not final continuation evidence. Validation copies and all outputs retained.
- Galaxy interferometer generator unexpectedly exited 143 (SIGTERM) while creating latent samples after sampling. Kernel reports parent exited; no Python traceback. Its 300-minute timeout had not elapsed; sender unknown. Checkpoint retained (`n_like=3350`, `explored=True`). No retry performed.
- Per ship-workspace failed-step rule, requested human approval to retry from checkpoint. Lens imaging was deliberately interrupted afterward with SIGINT (exit130) to leave no unattended render. Its checkpoint is retained; this is an operator stop, not an observed scientific failure. No new PR push, publication, merge or close-out performed.
- Resume: resolve retry decision; correct remaining Lens comments between renders; resume Galaxy interferometer and Lens imaging, then remaining four curated pages; run remaining three smoke suites; complete independent artifact review; update existing five contributor PRs and current-head CI evidence. Keep `release-gate: PyAutoGalaxy`.

Evidence root: `.worktrees/corner-plot-workspace-config/logs/continuation/` — `provenance.json`, `prose-code-proof.json`, `smoke-validation-summary.json`, `smoke-validation-equivalence.json`, `galaxy/imaging-evidence.json`, `galaxy/interferometer-interrupted.json`, renderer logs and `review/preliminary-review.md`. Workspace changes remain local in the existing claimed worktrees.

## Retry approval — 2026-10-26

User: "ok do that" — explicitly approves retrying the interrupted renders, completing remaining validation and updating the five existing PRs. No release or workspace merge authorized. Lens config-comment corrections now preserve parsed values; normal Lens imaging resumed from its checkpoint.

## Validation milestone — 2026-10-26

All fresh isolated smoke checks passed: Fit 10, Galaxy 16, Lens 44, HowToLens 50, HowToGalaxy 32 (146 scripts + 6 notebooks). Source/config review and independently regenerated parity for all 20 notebooks are CLEAN. Galaxy imaging/interferometer/ellipse completed on full data and passed independent artifact review; the approved interferometer checkpoint retry succeeded.

Published existing-PR updates: Fit #174 `aaed07d7377e7374be0433775c3b3adb16598339`; Galaxy #259 `dc1082a953772c0e8bedd244f7f62d0cb0110a58`; HowToLens #100 `1f0b479f683f8e226456d647c40339591f95c182`; HowToGalaxy #87 `c190915` (full SHA available in repo). Fit/Galaxy/HowToLens current-head CI all passed; HowToGalaxy unchanged fork workflows approved to run. No merge/release.

Lens imaging's normal fit completed; explicit notebook plots remain active. Remaining Lens pages execute in the separate, existing `validation-continuation/autolens_workspace` copy after archiving smoke datasets/output. Modeling scripts and simulators match the actual worktree by SHA; full-data, non-test execution still required. Copy only reviewed generated artifacts back after render completion.

## Final development wrap-up — 2026-10-26

User questioned the cost of full modeling runs, accepted focused validation instead, then requested (verbatim): "yes, finis the PRs and wrap up this epic task". This supersedes the earlier requirement to freshly render every affected modeling page. No further full modeling is required. It does not authorize release or merge.

### Completed and reviewed

- All five existing contributor PRs updated by normal pushes; no history rewrite. Canonical script changes, generated notebooks and reviewed output artifacts are committed.
- Fresh isolated Heart smoke passed 146 scripts + 6 notebooks. All 20 changed notebooks independently regenerated and checked. Source/config review CLEAN; final prose-only qualification preserves executable AST and configuration values, so smoke evidence remains applicable.
- Six representative full-data pages executed and independently reviewed CLEAN: Galaxy imaging, interferometer and ellipse; Lens imaging, interferometer and point-source. Lens has 10/8/6 valid figure references respectively and 9,898/2,739/1,848 saved posterior rows. Copied artifacts verified against reviewer SHA256 manifests. Fit latent cookbook also completed normally. These are execution checks, not scientific convergence claims.
- Superscript wording now acknowledges profiles within the same named path can share a label. Correct latent CSV/summary paths and plot-only angle recentering documented; all original effective settings preserved.
- Group full run stopped intentionally (SIGINT, exit130) at the human's direction. Checkpoint preserved, no completion claim. Group source/notebook included and smoke-tested; `markdown/group/modeling.md` remains the prior artifact and is explicitly excluded from fresh rendered-output claims. This is an accepted validation limitation, not pending modeling work.
- Fresh Heart remains YELLOW/no RED: existing cloud `autolens scripts/group/slam.py` failure, generated smoke-bootstrap drift, aged Hands/Mind PRs, and missing release rehearsal. No release-readiness claim.

### Final PR heads

- https://github.com/PyAutoLabs/autofit_workspace/pull/174 — `aaed07d7377e7374be0433775c3b3adb16598339`
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/259 — `dc1082a953772c0e8bedd244f7f62d0cb0110a58`
- https://github.com/PyAutoLabs/autolens_workspace/pull/595 — `83c4aaf295334659593a70bcea2c69cf7c45811f`
- https://github.com/PyAutoLabs/HowToGalaxy/pull/87 — `1236e75f5f1c456573feedb21b50b0ef8a716a95`
- https://github.com/PyAutoLabs/HowToLens/pull/100 — `09b3b6b342a1d13f192f7a4d57253a60c6cc9fc7`

### Remaining shipping steps

Current-head CI and a human merge decision remain gates. Galaxy-dependent workspaces additionally wait for a published Galaxy release containing #656. Keep the task active as awaiting-merge, with `release-gate: PyAutoGalaxy`; do not mark shipped or close the issue. No release performed.

All modeling/smoke processes stopped. Preserve the claimed worktrees, isolated validation copies and checkpoints until shipping/cleanup is separately authorized. Existing untracked Lens `dataset.fits` left untouched. Final evidence: task worktree `logs/continuation/{final-heads.json,smoke-validation-summary.json,readiness-wrapup.json,ci/,review/,lens/}`.

Process lesson: configuration/label/prose tasks should use focused semantics, notebook parity, smoke and representative visual checks. Do not expand them into fresh scientific inference across every example without a specific acceptance need and explicit cost agreement.


## Authorized backlog continuation — 2026-10-26

User request: "ok do all that, but note that Pulse we are working on so ignore". User also authorized the surfaced Heart RED development override for CI repairs and release-blocker development. In-turn green merges are authorized; no release through RED.

Fit workspace #174 merged c3b261752ea507b9d99e090b6461c9b4b92e4858. Four Galaxy-dependent PRs remain release-gated. A separate minimal prerequisite PR in autolens_workspace will set PYAUTO_TEST_MODE=1 for only scripts/group/slam.py in config/build/profile_smoke.yaml: the script requires fitted luminosity, and mode2 produced UniformPrior(0,0). The exact mode1 candidate passed canonical isolated Heart smoke in64.7s using fresh reduced data. No scientific prior, timeout, selection, dataset scale or assertion changes. Deliver this config-only prerequisite from origin/main before recovery validation; do not merge the broader community PR prematurely. Preserve contributor history and all existing output/data including untracked dataset.fits.

Validation evidence: .worktrees/pr-closeout-group-smoke-diagnostic/mode1.log and its autolens_workspace/test-results/. The prior release script run passed140.79s but predates Galaxy#656; fresh release validation still required.


## Release deferred by human — 2026-10-26

User deferred production on 2026-10-26: "lets not do a gated production release, lets do that in a bit once I have other AI tasks finish". No production release or full integration will be dispatched in this session. Own library freeze cleared so parallel tasks can finish.

Completed: original non-Pulse PRs Fit workspace174, Memory140, inference30, Mind505, Hands315, Mind-template4 and Memory-template3 merged. Necessary corrective PRs Mind517, Heart320 and Lens workspace603 merged with passing CI. Pulse79 was merged by another session; this session did not act on it.

Remaining release-gated community PRs: Galaxy workspace259, Lens workspace595, HowToGalaxy87, HowToLens100. Galaxy656 must be published before merging these. Lens595 now365c8311be8e6fdefc47947ba903f0ef08bd228b includes merged prerequisite603. All task data preserved.

Already-started TestPyPI-only run40363490490 remains in progress, version2026.10.26.1.dev84101. Five builds/uploads succeeded; install jobs ongoing at handoff. No completed rehearsal artifact/source verification or release-clearance claim. No waiter or scheduled continuation armed. Later release must recheck source pins, obtain fresh full validation and Heart verdict after other tasks finish; source may move now freeze is cleared. Clean prebuild clones retained at .worktrees/pr-backlog-release-clean, evidence at .worktrees/pr-backlog-evidence/recovery and heart319.
