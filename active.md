# Active Tasks

## inference-programme-ledger
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/134
- status: pr-open (https://github.com/PyAutoLabs/autolens_profiling/pull/135)
- worktree: ~/Code/PyAutoLabs-wt/inference-programme-ledger
- repos:
  - autolens_profiling: feature/inference-programme-ledger
- prompt: active/inference_programme_ledger.md
- note: docs-only (results/notes/inference/ PROGRAMME.md + DECISIONS.md + LITERATURE.md).
  The mge-lane-death claim it was recorded as disjoint from is gone — archived
  2026-08-18 as superseded (`complete/2026/08/mge-lane-death.md`); its
  `research/mge-lane-death` branch was never created.
  This is the canonical copy of the 2026-08-17 human-approved inference programme.

## stored-sample-reconstruction-guard
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1486
- status: library-dev — WORKSPACE HALF SHIPPED; the PyAutoFit hardening (#1486) is what remains
- worktree: ~/Code/PyAutoLabs-wt/stored-sample-reconstruction-guard
- repos:
  - PyAutoFit: feature/stored-sample-reconstruction-guard
  - autogalaxy_workspace: feature/stored-sample-reconstruction-guard
- workspace-PR: **MERGED 2026-08-17T22:08Z** as `1b5005c8` (squash), branch deleted. All 6 checks green
  (smoke 3.12 3m37s, smoke 3.13 3m44s, 3x navigator). Verified present on origin/main. This closes the
  nightly Workspace Smoke red; Heart's `workspace validation not passing` reason should clear on its
  next tick. Was: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/210 (no pending-release label —
  `valid_sample_instance_pairs` ships in RELEASED autofit 2026.8.15.1, wheel inspected, so the
  library-first gate does not apply)
- heart-ack (2026-08-17, human): acknowledged YELLOW score 70 to ship PR#210. Exact reasons acked:
  "workspace validation not passing (1 failed, cloud#31992749671: autogalaxy notebooks/guides/samples.ipynb)";
  "manifest drift: tenant firewall (organ code) — 9 mismatch(es) vs PyAutoMind/repos.yaml";
  "release validation incomplete: no rehearsal for current source". Ack does NOT extend to new reasons.
- prompt: active/to_instance_guard_gap.md
- CONFLICT OVERRIDE (deliberate, 2026-08-17): `worktree_check_conflict` exits 1 — PyAutoFit is also
  claimed by `version-stamp-sync-guards` (PyAutoHands#235). Proceeding was authorized by the human
  after verifying the two are FILE-DISJOINT: that branch's only commit (`9ec8a3877`) touches
  `autofit/__init__.py` + `files/release.sh`; this task touches `autofit/non_linear/samples/`.
  Two git worktrees on one repo with different branches is legal; the guard is a workflow
  convention, not a git limit. If #235 starts touching `non_linear/samples/`, stop and re-coordinate.
- summary: `Sample.instance_for_model(ignore_assertions=True)` (`sample.py:178-212`, the CI failure
  site) and the shared `to_instance` decorator (`interface.py:32-40`) materialize stored samples with
  no `FitException` recovery. PyAutoFit#1466 wrote recovery by hand at two call sites only
  (`max_log_likelihood`, `draw_randomly_via_pdf`). Fails PyAutoHeart Workspace Smoke nightly on
  `autogalaxy_workspace guides/results/aggregator/samples.ipynb`; holds Heart's
  `workspace validation not passing` reason open.
- design (human-decided): `to_instance` takes a per-method recovery policy — `recover="next_valid"`
  for `max_log_posterior`, `recover="raise"` (typed `SamplesException`) for `from_sample_index` and
  the marginalized methods. Release note: raise path changes the user-visible type from
  `ModelParameterException` (a ValueError) to `SamplesException` (plain Exception).
- split-out: PyAutoFit#1487 — weight-threshold prune retains zero-weight samples with checks ENABLED.
  Do not fix here.
- do-not: do NOT weaken PyAutoGalaxy `validate_ell_comps`; do NOT edit the tutorial. Test mode is NOT
  implicated (`ENV: real_search` releases `PYAUTO_TEST_MODE`) — verified, do not re-open.

## heart-green-validation-ingest
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/567 (open, reopened 2026-08-11T00:22Z)
- session: none — the Codex session that did the work ran out of credits after merging, before any bookkeeping. Registered 2026-08-11 by a cloud session reconstructing its state from GitHub.
- status: EVIDENCE PENDING INGEST — not a code task. All four fixes are MERGED (see complete/2026/08/heart-red-guarded-sample-escape.md); the green run exists; only the ingest is owed.
- what is owed: PyAutoHeart `Release Integrate` run **31534325304** (dispatched 2026-08-11T20:42:55Z on main `b7634e2c`, finished 21:50:07Z) came back **SUCCESS** — 53 jobs, 52 green, `integrate / run_notebooks` skipped by design. Its `release-stage-report` artifact has never been consumed, so Heart's verdict does not yet reflect it.
- resume: **nothing to type.** `heart/checks/release_run.py` self-refreshes this channel — the next Heart tick on the dev box reads the latest completed `release-integrate` run, finds no sidecar for run id 31534325304, and downloads + ingests its `release-stage-report` through `heart.validate.run()` automatically (a fresher local ingest is never regressed; an ingested run is never re-downloaded). So any `/health`, `/wake_up` or bare tick from the laptop closes this out. Manual fallback only if that path fails: `gh run download 31534325304 -R PyAutoLabs/PyAutoHeart -n release-stage-report -D <dir>` then `pyauto-brain release validate --ingest <dir>`.
- deadline: the artifact expires **2026-11-09**. After that the evidence is gone and the run must be re-dispatched from scratch.
- why not from a cloud session: two independent reasons, and the second is the load-bearing one. (1) Actions artifact downloads 403 at the egress proxy (`productionresultssa14.blob.core.windows.net` CONNECT refused) even though the GitHub API returns a valid signed URL — the `artifacts-are-laptop-only` trap already recorded under release-drive-2026-08-07; the proxy README classes that as an org policy denial to report, not route around. (2) Even with the file in hand, `validate --ingest` writes `validation_report.json` into `HEART_STATE_DIR` (`~/.pyauto-heart`), which on a cloud container is ephemeral and shared with nothing — the dev box's verdict would be untouched. Heart's authoritative verdict lives where its state lives.
- note on the README dashboard: the `<!-- heart:begin -->` block is rendered by the CLOUD `Heart Health` job, which runs only the two GitHub-API checks against an empty `.heart-state`. Its `test run status unknown` / `install verification not run` / `no release validation for current source` gaps are inherent to that cloud snapshot, NOT a claim that the dev box lacks the evidence. Do not read the README block as the dev-box verdict.
- current verdict: Heart's last committed dashboard (2026-08-11T05:51Z, i.e. BEFORE the green run) reads STALE score 65, listing `no release validation for current source` among its evidence gaps. That is the STALE tier behaving correctly — an evidence gap, not a fault, and this ingest is its remedy.
- do-not: do NOT re-dispatch `Release Integrate` to "refresh" this. The run is green and its artifact is live; a re-dispatch costs ~70 minutes of CI and proves nothing new. Only re-dispatch if the artifact has expired or main has moved.
- repos-none-claimed: this entry claims NO repos — deliberately on one line, NOT as 2-space `  - Repo` bullets, because `worktree_check_conflict` treats any such bullet as a live claim.

## release-drive-2026-08-03
- issue: (no issue — a human-authorized manual release drive, not a dev task)
- session: claude --resume e0105850-b98b-47ff-9ada-cba04a455a65
- status: SHIPPED 2026-08-07 — superseded by release-drive-2026-08-07 below, which carried this drive's payload to PyPI as 2026.8.7.1. This entry is now history; do NOT re-run it. (Was: Stage 2/3 CLEAR TO RE-RUN on request, 2026-08-04.)
- split-from: simulator-util-to-af-ex (#1444), closed out 2026-08-04 → complete/2026/08/simulator-util-to-af-ex.md. That task shipped; this release drive it opened did not, so it was split out rather than buried in a completion record.
- why a release is owed: workspace main now calls `af.ex.util` helpers that exist on PyAutoFit main but NOT on PyPI. Control test PROVED the breakage — AttributeError on the first simulator call against released autofit 2026.7.29.2 in a clean venv with PYTHONPATH unset — and HowToFit ships NO datasets (`dataset/` gitignored, 0 tracked files), so a new user gets no data at all. The `pending-release` gate was overridden 2026-08-03 on explicit human instruction ("all five once green") with that consequence stated, which makes publishing the remedy, not a preference.
- release-drive: human authorized driving a release 2026-08-03 (chose "Drive the release" over merging early or re-cutting workspace-only). Drive via `pyauto-brain release validate` — NOT the nightly driver; AUTONOMY.md forbids converting a manual release into the scheduled-nightly exception.
- release-progress: Stage 0/1 preflight PASS. Stage 2 rehearsal #1 (run 30841336540, dev69901) DISCARDED — PyAutoLens#686 merged 18:31:35Z DURING that build while the PyAutoLens job checked out at 18:27:31Z, so those wheels lacked #686; writing the post-build live-main sha would have attested to source the wheels never contained. Stage 2 rehearsal #2 = run 30841883371 SUCCESS → testpypi 2026.8.3.1.dev70001, verified every library main HEAD commit-time PREDATES its job checkout before writing commit_shas.json. Artifacts dir `~/.pyauto-heart/manual_validation_20260803_pm` (rehearsal.json + testpypi_version.txt + commit_shas.json).
- commit-shas (from rehearsal #2): PyAutoNerves e82c17fd / PyAutoFit 26033fb4 / PyAutoArray 54ba44e8 / PyAutoGalaxy 4249384b / PyAutoLens 4927738e. SUPERSEDED — do not use. The shipped SHAs are recorded under release-drive-2026-08-07 below; these were already stale on 2026-08-04 and the 2026-08-07 drive re-derived them from a fresh rehearsal.
- release-outcome (Stage 3 run 30842349506, COMPLETE): 30 jobs, exactly 2 failures, both diagnosed and both now FIXED AND MERGED. (1) autolens/point_source — #453 updated only ONE of the two model blocks in scripts/point_source/start_here.py, leaving prose saying PointSolved and code saying Point; with PyAutoLens#686 making solved all-to-all the default that raises PointProfileMismatchException. Regression proven: the same script passed 40.4s in run 30788224561 and failed 4.5s here. Fixed by autolens_workspace#461, MERGED 2026-08-03T21:41:40Z. (2) verify_install check D (`pip rc=0 import rc=1`) — fixed by PyAutoHeart#134 (`--pre` on the TestPyPI path), squash-MERGED 2026-08-04 as 46a331a, both pytest legs green on head fb0eff4b, one file `heart/checks/verify_install.sh` +24/-1.
- release-resume: re-rehearse (new wheels, so check D resolves the candidate family with `--pre`), re-dispatch integrate, then `gh run download <run> -R PyAutoLabs/PyAutoHeart -n release-stage-report -D <artifacts-dir>` and `pyauto-brain release validate --ingest <artifacts-dir> --commit-shas <artifacts-dir>/commit_shas.json`. Never `--force` a RED/YELLOW without a fresh human ack. On GREEN the PUBLISH step is a SEPARATE human decision.
- release-scope-flag: RESOLVED 2026-08-04 — this release also carries PyAutoLens#686 (point-source defaults, 4927738e), which was not one of the fixes the drive set out to ship. Human answer: ship it. Verified before accepting: #686's exp-3 merge gate had landed two days before the merge, Tests+Docs green on 4927738e, it carries the `## API Changes` heading the breaking-change release notes require, and a workspace sweep found all 8 `al.AnalysisPoint` call sites relying on the new all-solved default compose `al.ps.PointSolved` — the only mismatch (point_source/start_here.py) was autolens_workspace#461, merged.
- do-not: do NOT pick up `ep.py` or any `ep*` script as a release blocker — human decision 2026-08-03 to park them for a while (PyAutoFit #1332 F10 tracks the underlying EP message-projection instability). They are parked NEEDS_FIX in autofit_workspace_test config/build/no_run.yaml via #82, which `run.py` loads unconditionally and profile-independently, so the parking holds for the RELEASE profile too.
- dep-floor-regression: CLEARED 2026-08-03 21:30Z — complete/2026/08/dep-floors-source-chain-ci.md (PyAutoNerves#146). Root cause was the `1.0.dev0` source stamp, not the floors; the floors stand unchanged. All five previously-blocked workspace PRs re-ran green and merged.
- correctives-worktree: REMOVED 2026-08-04 — both correctives merged, `~/Code/PyAutoLabs-wt/release-validate-correctives` gone (worktrees + local/remote `feature/release-validate-correctives` branches deleted in autolens_workspace and PyAutoHeart, `worktree prune` run in both; the dir held only tracked files, no output/ artifacts).
- heart-context (2026-08-04): verdict YELLOW, score 70, `red_reasons: []`. Reasons = workspace validation not passing / tenant-firewall manifest drift (2 mismatches vs repos.yaml) / release validation stale (source moved since rehearsal — expected, see commit-shas above). The workspace-validation reason has shrunk since the snapshot: autofit_workspace_test#84 fixed the jax_assertions entry it names.
- repos-none-claimed: this entry claims NO repos — deliberately listed on one line, NOT as `  - Repo` bullets, because `worktree_check_conflict` treats any 2-space `  - <Repo>` bullet as a live claim regardless of which field it sits under.

## release-drive-2026-08-07
- issue: (no issue — a human-authorized manual release drive, not a dev task)
- status: SHIPPED 2026-08-07. All five libraries published to PyPI at **2026.8.7.1**. Verified independently against pypi.org (not just the run conclusion): each package reports `latest = 2026.8.7.1`, and `autolens-2026.8.7.1-py3-none-any.whl` + `autogalaxy-2026.8.7.1-py3-none-any.whl` were downloaded from the live index as proof of installability.
- supersedes: release-drive-2026-08-03 (above). That drive's payload shipped here; its recorded commit_shas were stale and are NOT the shipped set.
- commit-shas (SHIPPED, verified still at origin/main immediately before ingest): PyAutoNerves 5a67f181 / PyAutoFit f02ea7ed / PyAutoArray 828d5c13 / PyAutoGalaxy 63d69b87 / PyAutoLens e4c7ba70.
- discharges: the mge-sigma-min-workspace-sweep RELEASE DEBT (see above) — `sigma_min` confirmed present in the released autogalaxy wheel.
- root-cause of the stalled nightly (2026-08-06): the GitHub Actions outage dropped push triggers, so several merges to main had NO Tests run and two runs failed on runner provisioning. Not a code fault. Remedy: `workflow_dispatch` added to PyAutoGalaxy + PyAutoLens `.github/workflows/main.yml` (PRs #560 / #693, both merged) so a main-HEAD run can be re-requested on demand without an empty commit.
- validation: Stage 0/1 preflight PASS. Stage 2 rehearsal run 31192317261 (PyAutoHands release.yml, rehearsal:true) → testpypi 2026.8.7.1.dev70601. Stage 3 integrate run 31193443960 (PyAutoHeart release-integrate.yml) → 51/51 jobs green, `status: pass`, 657p/0f/101s/0t, verify_install checks A–F all PASS. Artifacts `~/.pyauto-heart/manual_validation_20260807`.
- MGE-regression NOT reproduced: the 2026-08-06 integrate failed on `scripts/interferometer/features/multi_gaussian_expansion/likelihood_function.py` (numpy LinAlgError: Singular matrix). It passed here — and the script genuinely RAN rather than being silently dropped, proven by the count moving 324p+1f → 325p+0f with the total unchanged.
- ingest-trap (cost one cycle): the first readiness tick after a clean ingest came back RED with `stale_reasons: []` and only `PyAutoGalaxy/PyAutoLens: 4 commit(s) behind origin`. That is a LOCAL-clone signal, not a validation failure — the merged workflow_dispatch PRs had never been pulled. Fast-forwarding both local mains to the validated SHAs re-ticked GREEN score 100. Do not `--force` past this; sync the clone.
- pre_build-trap (caught before it fired): `pre_build` runs `black scripts/` then `git add scripts/`, and `git add` on a directory stages UNTRACKED files too — an uncommitted WIP script in `autolens_assistant/scripts/` would have been reformatted and pushed public inside the "pre build" commit. This is the same leak class the script's own comments describe fixing for `dataset/`/`config/` (#126); the `scripts/` path still has the hole. Mitigation used: move the file out of the repo before the run, restore after (verified byte-identical by md5). Worth a real fix so it is not left to operator vigilance. FIXED 2026-08-08 on branch `claude/automind-task-planning-163wk7` (PyAutoHands) — prompt `draft/bug/pyautohands/pre_build_stages_untracked_wip.md`. The hazard was first REPRODUCED against the pre-fix script on throwaway fixture repos (private file committed as "pre build" and pushed to the remote, exit 0, silently), then closed by two legs: a fail-fast preflight sweeping all 13 repos for untracked files under `notebooks/`/`scripts/`/`slam_pipeline/` before the first is touched (it must precede everything — run_workspace pushes each repo before moving to the next), and staging narrowed to `git add -u` plus explicit adds of run-created files, so the directory-wide form cannot return. Covered by `tests/test_pre_build_staging.py`, which runs the real script against fixture git repos with real bare remotes. No `--allow-dirty` override by design. Also answers the open atomicity question in PyAutoHands `docs/pre_build_failure_audit.md` §6. SHIPPED 2026-08-08: PyAutoHands#232 (issue, closed completed) → PyAutoHands#233 MERGED as a5bac76b, all three pytest legs green (3.12/3.13/3.14, 309 passed / 4 skipped — the count reconciles with local, confirming the new fixture tests actually ran rather than being collected-but-skipped). Mind bookkeeping PyAutoMind#152 MERGED as 62869a2e.
- release-run: 31200419263 (PyAutoHands release.yml, rehearsal:false → live). All five `release (...)` publish jobs SUCCESS; tags pushed and PyPI agree, so the line-428 hazard (upload timing out AFTER tagging) did not occur.
- post-publish failures (do NOT re-drive the release for these — the publish is complete and correct): (1) `wiki_currency_check` autolens — died on `No matching distribution found for autolens==2026.8.7.1` ~4 min after upload; a PyPI index-propagation race, proven by `wiki_currency_check_autofit` starting 2s earlier and PASSING, and by the wheel downloading fine minutes later. RESOLVED 2026-08-07 — autolens_assistant is CLEAN on all five legs, so the race was the whole story and no autolens follow-up is owed. A CI job re-run was impossible (`HTTP 403: The workflow run containing this job is already running`), so it was graded locally by the documented method instead: a fresh venv with `autolens==2026.8.7.1` from PyPI, `PYTHONPATH` cleared, and all four libraries verified to resolve to venv site-packages rather than this workspace's source checkouts (the `baseline-repin-TRAP` — grading against source installs would have been meaningless). Results: `--check-version` clean (baseline matches autolens 2026.8.7.1), `--scope all` 68 files / 143 symbols / **0 missing-broken**, `--lint-idioms` clean (214 files), `--check-citations` 105 files / 413 citations / **0 missing, 0 warnings**, `--check-provenance` **0 errors** (49 pages). Contrast autogalaxy's 5 provenance errors — the two failures shared a red badge but not a cause. (2) `wiki_drift_issue` — pure fallout, `Artifact not found: wiki-drift-report`, because (1) died before writing it. (3) `wiki_currency_check_autogalaxy` — REAL drift, see the provenance prompt filed under draft/maintenance/autogalaxy_assistant/.
- artifacts-are-laptop-only: Actions artifact downloads are blocked from cloud/mobile sessions (egress policy 403s `productionresultssa2.blob.core.windows.net` on CONNECT) — this is what stopped the cloud session finishing the ingest. Both wiki drift reports were captured to `~/.pyauto-heart/release_20260807_wiki_drift/` while on the laptop.
- do-not: do NOT use the nightly driver for a manual release — AUTONOMY.md forbids converting a manual release into the scheduled-nightly exception.
- repos-none-claimed: this entry claims NO repos — deliberately on one line, NOT as 2-space `  - Repo` bullets, because `worktree_check_conflict` treats any such bullet as a live claim.

## version-stamp-sync-guards
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/235
- prompt: active/version_stamp_sync_and_release_sed_guards.md
- session: claude --resume d73342fb-c33f-4028-8741-30cbe0c856a3
- status: pr-open (https://github.com/PyAutoLabs/PyAutoLens/pull/700)
- worktree: ~/Code/PyAutoLabs-wt/version-stamp-sync-guards
- repos:
  - PyAutoNerves: feature/version-stamp-sync-guards
  - PyAutoArray: feature/version-stamp-sync-guards
  - PyAutoFit: feature/version-stamp-sync-guards
  - PyAutoGalaxy: feature/version-stamp-sync-guards
  - PyAutoLens: feature/version-stamp-sync-guards
  - PyAutoHands: feature/version-stamp-sync-guards

## howto-setup-notebook-audit
- issue: (none — cloud session, no issue filed; the six PRs below carry the record)
- prompt: active/missing_setup_notebook_audit.md
- session: cloud (Claude Code on the web), no local worktree
- status: pr-open (six PRs, awaiting CI)
- PRs: HowToFit#45 / HowToGalaxy#66 / HowToLens#70 / autofit_workspace#138 /
  autogalaxy_workspace#211 / autolens_workspace#485 — each one commit on the branch below, on
  top of the main it was cloned from.
- no pending-release gate: `setup_notebook` is long-shipped in released autofit/autogalaxy/autolens
  and is already called by every other example script in these repos, so the library-first merge
  gate does not apply to the three workspace legs.
- repos-none-claimed: this entry claims NO repos as 2-space `  - Repo` bullets — the work ran
  in a cloud container with no local worktree, so `worktree_check_conflict` must not read it as
  a live claim. The branches are listed as prose below.
- branches: HowToFit `fa6c03f` / HowToGalaxy `9aa173c` / HowToLens `1ff2fa0` /
  autofit_workspace `6180480` / autogalaxy_workspace `d3fb5b5` / autolens_workspace `181694c`,
  all on `claude/howto-setup-notebook-audit-dm2j9e`.
- audit result: every `.py` under `scripts/` (plus each HowTo's root `start_here.py`) was checked
  in all three HowTo repos and all five user-facing workspaces. 39 scripts were missing the
  `# from auto* import setup_notebook; setup_notebook()` line — HowToFit 3, HowToGalaxy 2,
  HowToLens 6, autofit_workspace 1, autogalaxy_workspace 5, autolens_workspace 22. All 39 fixed,
  with the matching generated notebook updated to the uncommented form PyAutoHands emits.
- clean: autocti_workspace (79 scripts, 0 missing).
- out of scope, deliberately: autoreduce_workspace (30 scripts, all missing) has NO `notebooks/`
  directory, so the line is not part of its convention yet — same for every `*_workspace_test`
  and `*_workspace_developer` repo (checked by tree listing; none generates notebooks). If
  autoreduce_workspace ever starts generating notebooks, its 30 scripts need this sweep.
- placement: after the module docstring, or after the `from auto* import jax_wrapper` line where
  a script has one (workspace convention). One outlier, autolens_workspace
  `scripts/guides/units/mass_to_light_ratio_units.py`, opens on imports rather than a docstring —
  the line went at the top of the file, still ahead of every import.
- not regenerated by PyAutoHands: the notebooks were patched by hand to the exact shape the
  generator emits (verified against already-correct sibling pairs, and `json.dumps(nb, indent=1)`
  round-trips byte-identically). A real `generate.py` run should be a no-op on these; confirm that
  before merging.
- adjacent, NOT done here: `draft/maintenance/workspaces/notebook_setup_notebook_drift_siblings.md`
  is the separate regeneration-drift sweep (notebooks carrying the COMMENTED form). Different
  failure, different task — untouched.
