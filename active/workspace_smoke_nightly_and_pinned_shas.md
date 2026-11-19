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
Witness: (1) `.github/workflows/workspace-smoke.yml` has a nightly `schedule:` and a `workflow_dispatch` input `commit_shas` that it passes to `workspace-validation.yml`; (2) a scheduled run on a night when no library or workspace `main` SHA differs from the last successful run's ends in under 2 minutes with the summary line "no main moved since run <id>" and conclusion success; (3) `gh workflow run workspace-smoke.yml -f commit_shas='{"PyAutoGalaxy":"<sha>"}'` runs the workspaces against that SHA and records it in the run's `commit_shas.json`; (4) every run writes the SHAs it tested to its summary and to an artifact, in a form `gh run view --json` or `gh run download` can read; (5) Heart's `test_run` leg still reads the latest completed run as before, and a skipped night does not make it STALE
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
