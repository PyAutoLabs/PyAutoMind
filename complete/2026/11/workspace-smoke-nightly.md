# Workspace smoke nightly and pinned SHAs (M3.7d)

Completed 2026-11-19. Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/354

M3.7d of the autonomous-orchestrators epic. Nightly `workspace-smoke.yml` with a SHA gate that skips when no workspace main moved and the latest run was green, a full sweep at least every 7 days, and a `force` input; a SHA record artifact on every run; smoke runs pinned to the gate's SHAs; a separate `workspace-smoke-pinned.yml` for bisect runs. Heart `test_run` reads only runs on main and re-attests a skipped night. The covered repos are read from `workspace-validation.yml`.

## Merge receipts

- PyAutoHeart#355: 8ab527dfda9c332a9effecebc0c46210abf81443 (merged by the human's /prm, 2026-11-19)

Feature head 947756f90 is an ancestor of origin/main. Organ repo: no release obligation.

## Validation and review

Review by Fable 5.2: round 1 FINDINGS (1 high, 1 medium, 2 low), fixed. One CI red on the tenant firewall, fixed by reading the covered repos from `workspace-validation.yml`. Run 43034177136 (2026-11-11) was a real failure on a feature branch. Tier: judge (no shadow row).

## Outstanding verification

Witness items 2 (a skipped night), 3 (a pinned dispatch) and 4 (the SHA record on a real run) need runs on main. They are NOT verified by this merge and remain outstanding until the nightly and a pinned dispatch have run on main.

## Original prompt

# M3.7d Workspace Smoke runs nightly when a `main` moved, and accepts pinned SHAs

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) `.github/workflows/workspace-smoke.yml` has a nightly `schedule:` and tests only `main`; pinned runs have their own entry, `workspace-smoke-pinned.yml`, whose required `commit_shas` input is passed to `workspace-validation.yml` (amended 2026-11-19 in review: a pinned run that passes must not read as the smoke verdict for `main`); (2) a scheduled run on a night when no library or workspace `main` SHA differs from the last successful run's ends in under 2 minutes with the summary line "no main moved since run <id>" and conclusion success; (3) `gh workflow run workspace-smoke-pinned.yml -f commit_shas='{"PyAutoGalaxy":"<sha>"}'` runs the workspaces against that SHA and records it in the run's `commit_shas.json`; (4) every run writes the SHAs it tested to its summary and to an artifact, in a form `gh run view --json` or `gh run download` can read; (5) Heart's `test_run` leg still reads the latest completed run as before, and a skipped night does not make it STALE
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat, on the cloud verification lane of the orchestrator speed review: "approved, all rulings yes".

## Why

`workspace-smoke.yml` is the only run of every workspace against the libraries' `main`. It runs on Mondays at 03:00 UTC and takes 26 to 36 minutes. Library PR CI runs no workspace script. After M3.7b a shift's merges carry only a targeted smoke, and the human's `/prm` merges already carry no sweep, so `main` can hold a workspace break for up to a week. The sweep moves after the merge and has to run often enough to find a break within a day.

`commit_shas` is an input of `workspace-validation.yml` and `release-integrate.yml` but not of `workspace-smoke.yml`, whose `workflow_dispatch` takes no inputs. Bisecting a red run needs it.

## Ruling (human, 2026-11-19)

- **S4 (Heart half).** The nightly CI minutes are accepted.

## Shape

- `workspace-smoke.yml`: add a nightly cron (keep Monday's as the same schedule); a first job that compares the current `main` SHAs of the libraries and workspaces with those recorded by the last successful run and skips the body when none moved; the `commit_shas` input passed through to `workspace-validation.yml`.
- Record the tested SHAs per run so M3.7e can print "workspaces verified through `<sha>`" and name the suspect PRs between two runs.
- Check how Heart's readiness reads this workflow (`gh run list --workflow workspace-smoke.yml`) and keep a skipped night from ageing the evidence into STALE.
- Look at run 43034177136 (2026-11-11, dispatched by hand, failed) and say in the PR whether it was a real failure or a flake, because M3.7e blocks merges on a red run.

## Order

Independent of M3.7a to M3.7c; may be built in parallel. M3.7e needs it.

## Witness items 2 to 4, observed on `main` (2026-11-19, Opus 5.5 session)

- **Item 4, the SHA record on a real run:** run 44573385455 (dispatch, 17:05Z) swept ("no SHA record from the last successful run (44521331980)") and uploaded `workspace-smoke-shas` with 15 repos' SHAs. Attempt 1 failed on one script (`autolens_workspace/scripts/group/slam.py`, a test-mode prior bound of 0; filed as `draft/bug/autolens_workspace/group_slam_sigma_upper_zero_flake.md`); the failed job re-run passed, so the run concluded success.
- **Item 2, a skipped run:** run 44581790051 (dispatch, about 18:25Z) read `swept: false`, "no main moved since run 44573385455"; the gate passed and the smoke job was skipped. This was a dispatch rather than the 03:00 cron; both go through the same gate.
- **Item 3, a pinned dispatch:** run 44579050941 of `workspace-smoke-pinned.yml` with `commit_shas={"PyAutoGalaxy":"2ec0e3611…"}` swept "pinned by dispatch: PyAutoGalaxy" and concluded success, on its own entry: the latest `workspace-smoke.yml` run on `main` stayed 44581790051.
