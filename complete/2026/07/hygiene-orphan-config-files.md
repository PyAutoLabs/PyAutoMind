- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/155
- library-pr:
  - PyAutoLabs/PyAutoBrain#156
- workspace-pr:
  - PyAutoLabs/autocti_assistant#11
  - PyAutoLabs/autocti_workspace#6
  - PyAutoLabs/autocti_workspace_test#9
  - Jammy2211/autofit_workspace_developer#24
  - PyAutoLabs/autofit_workspace_test#71
  - PyAutoLabs/autogalaxy_workspace_test#88
  - PyAutoLabs/autolens_assistant#89
  - PyAutoLabs/autolens_workspace_test#206
  - PyAutoLabs/euclid_strong_lens_modeling_pipeline#35
- notes: Closed the /hygiene orphan-config-FILE blind spot recorded as the open follow-up of the grids.yaml removal (autolens_workspace#317). `_hygiene_config.py` iterated only LIBRARY yamls and skipped any without a workspace counterpart, so a workspace config file the libraries never shipped was structurally invisible — how dead grids.yaml survived ~1yr in 10 repos. THE SIGNAL: the earlier prototype flagged by FILENAME orphanhood (~120 hits, nearly all legit) and was rightly abandoned; the honest test is REACHABILITY (does anything READ it), which separates the noise by OWNER — build/* -> PyAutoHands (suppress), priors/* -> JSONPriorConfig class-path resolution (suppress), non_linear/{nest,mle,mcmc} -> nothing (DEAD). Suppression = explicit ORPHAN_OWNERS map IN the checker, deliberately NOT a per-repo .hygieneignore (20 files + a staleable config surface = the failure mode being fixed). THE ELEGANT PART: the library's own shipped set IS the reachability oracle — it ships non_linear/GridSearch.yaml (live) but not nest/mle/mcmc (dead), so orphan-vs-library-set keeps the live one and surfaces the dead ones with ZERO per-file rules. Mirror self-scoping (scan only repos whose config shares >=1 file with the lib set) excludes organ repos with no hardcoded list. ACCEPTANCE (non-negotiable, all passed): reconstructed the REAL pre-#317 grids.yaml blob (git cat-file -p ce99ca12b^:config/grids.yaml) in a temp tree and proved the detector re-finds it; flags non_linear today; silent on build/priors. 16 tests pass. THE DETECTOR FOUND A THIRD DEAD CLUSTER not in the brief: visualize/include.yaml in 2 test repos (no lib ships it, nothing reads conf visualize.include, no Include2D class, user-facing workspaces already dropped it) — folded into the cleanup. Post-merge the detector reports 0 orphan files on synced main (was 26+2); only 19 pre-existing key-mirror items remain. EDGE CASE recorded: autofit_workspace_developer config shares no live file so the mirror-heuristic skips it — its 2 dead files swept manually (a config tree that is ENTIRELY dead orphans is invisible to a mirror check). GOTCHAS: autofit_workspace_developer is owned by Jammy2211 not PyAutoLabs (PyAutoLabs gh api pulls 404'd — resolve owner from git remote); PyAutoCTI/test_autocti/config/non_linear.yaml is a FILE not a dir (different layout, untouched); 2 assistant PRs merged with PRE-EXISTING unrelated red (wiki-currency drift + boundary's 4 unclassified docs/images files — both fail on every recent PR to those repos, neither required, did not block earlier grids.yaml merge). This task was env-profile-derivation-blocked earlier the same day; unblocked when its 6 rename PRs merged.

## Original prompt

# Give /hygiene sight of orphan config FILES (reachability, not filename match)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- autocti_assistant
- autocti_workspace
- autocti_workspace_test
- autofit_workspace_developer
- autofit_workspace_test
- autogalaxy_workspace_test
- autolens_assistant
- autolens_workspace_test
- euclid_strong_lens_modeling_pipeline
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Why

`/hygiene config` has a structural blind spot recorded during the `grids.yaml`
removal: `PyAutoBrain/agents/conductors/hygiene/_hygiene_config.py` iterates over
**library** yamls and, at line 67, skips any without a workspace counterpart. A
workspace config file with **no library counterpart is therefore invisible to
it**. That is how a dead `config/grids.yaml` survived in 10 repos for ~1 year.

A previous prototype flagged orphans **by filename** and produced 100+ hits,
nearly all legitimate, so it was not shipped — it needed a suppression design
first. This task supplies that design.

**The prototype's signal was wrong.** Filename-orphanhood asks "does a library
ship a file with this name?", which is not the question. The question is
**reachability**: does anything read this file? Measured 2026-07-23 across the
workspace — 120 orphan instances, 30 distinct — the noise separates cleanly by
*owner*:

| Family | Instances | Read by | Verdict |
|---|---|---|---|
| `build/*` (`env_vars`, `no_run`, `markdown_examples`, …) | ~39 | PyAutoHands | legitimate |
| `priors/*` | ~40 | `JSONPriorConfig`, resolved by class path | legitimate |
| `non_linear/{nest,mle,mcmc}.yaml` | ~26 | **nothing** | **dead** |

## The second finding this exposed

`config/non_linear/{nest,mle,mcmc}.yaml` is dead config in 9 repos — the same
class of defect as `grids.yaml`, found by the very signal this task builds.

Verified 2026-07-23: no library reads `conf.instance["non_linear"]` for these
(checked all six of autofit/autogalaxy/autolens/autoarray/autocti/autonerves).
Search defaults come from **Python signature defaults**, not config —
`PyAutoFit/autofit/non_linear/search/nest/nautilus/search.py:41` declares
`n_live: int = 3000` while the workspace `nest.yaml` says `n_live: 200`, and the
file has no effect. The three user-facing workspaces (autolens/autofit/
autogalaxy) already dropped them; the stragglers are the test, assistant,
developer and euclid repos.

Note `config/non_linear/GridSearch.yaml` **is** live (`conf.instance
["non_linear"]` resolves to `{'gridsearch': ...}`) — do not remove it.

## Scope

**Part 1 — the detector (PyAutoBrain).** Extend `_hygiene_config.py` with an
orphan-file check driven by reachability, keeping its existing key-mirror diff
intact. Suppression lives in an **explicit owner map in the checker itself** — a
small reviewable table (`build/*` → PyAutoHands, `priors/*` → path-resolved
prior config), deliberately *not* a per-repo `.hygieneignore`, which would add
20 new files and a config surface that can itself go stale — the exact failure
mode being fixed.

**Part 2 — the cleanup.** Delete the ~26 dead `non_linear/{nest,mle,mcmc}.yaml`
files across the 9 repos listed above.

## Guardrails

- **Acceptance test, non-negotiable:** the check must flag `grids.yaml` when run
  against the pre-deletion tree (retrospective validation on a commit before
  `autolens_workspace#317`), flag `non_linear/{nest,mle,mcmc}.yaml` today, and
  stay **silent** on `build/*` and `priors/*`. A check that cannot re-find the
  bug that motivated it is not validated.
- `_hygiene_config.py` is **stdlib + PyYAML only** — it must never import the
  science stack. Preserve the `sys.exit(1)` fallback when PyYAML is absent.
- Preserve the `count|summary` single-line prescan contract the conductor
  consumes; the orphan count is a *surface* signal ("files to review"), not a
  bug count, consistent with the existing key-mirror wording.
- Extend `PyAutoBrain/tests/test_hygiene_conductor.py` — the suppression map is
  the part most likely to rot, so cover both a suppressed and an unsuppressed
  orphan.
- Per-repo verification for Part 2: `PyAutoCTI/test_autocti/config/` is what the
  CTI test conftest points `conf.instance` at, so the autocti repos are the ones
  with a real failure mode — run their suites after deleting, exactly as the
  `grids.yaml` sweep did.
- `gh pr create` fails on this workspace's SSH remotes → use
  `gh api repos/O/R/pulls -X POST`.

## Related

- Sibling prompt `draft/maintenance/workspaces/config_key_mirror_drift.md`
  covers the opposite direction (keys missing FROM workspaces). Neither it nor
  the current checker catches an orphan FILE; this closes that.
- Follows the `grids.yaml` removal (autolens_workspace#317, 12 PRs) which
  recorded this gap as its open follow-up.
- Discovered while purging the autoconf-era legacy surface (PyAutoNerves#137) —
  `priors/subconfig.json` and `eden.yaml` were orphan config files that survived
  for the same reason.
