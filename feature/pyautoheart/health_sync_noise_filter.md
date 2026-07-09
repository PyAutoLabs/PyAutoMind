# Noise-filter the health_sync startup table + recurring repo_cleanup cadence

Type: feature
Target: PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: normal

## Original request (verbatim)

> When I open my virtual enviroment and it runs health, I still get a lot of
> stuff: [~1,000-line dirty-file dump across HowTo*/workspace repos] […]
> Is there an agent in PyAutoBrain whose job it is to clean this up? […]
> I normally just run the health agent and let it do a "full" census of
> everything so I think it should be catgching this stuff too?
>
> do both, and make sure theres a plant hat will ensure repo_cleanup runs
> semi regularly

## Context

The venv-startup `health` table comes from `PyAutoHeart/scripts/health_sync.sh`
(`_health_sync`), which dumps raw `git status --porcelain` per repo. Heart
already has a real-vs-noise classifier — `heart/noise.py` + `noise_globs` in
`config/repos.yaml` — that matches essentially all of the ~1,000 regenerated
dataset artifacts flooding the output (`*.fits`, `*data.json`, `*model.json`,
`*tracer.json`, `*.png`, `*test_report.md`, …). The deep census classifies;
the startup dashboard doesn't. The handful of real items (staged notebook
deletions in autolens_workspace_test, personal notes, untracked AGENTS.md
files) are buried.

## Scope

- Make `health_sync.sh` reuse the `heart.noise` classification: MOD/UNTR
  columns show noise-collapsed counts (e.g. `315 dirty → 313 noise, 2 real`),
  and the "Dirty files:" listing shows **real** files only, with a per-repo
  one-line noise summary.
- Add an `--all` flag to restore today's full raw listing.
- Keep the table fast (classification is fnmatch on porcelain already in hand;
  no extra git calls) and keep working when `heart.noise`/PyYAML is
  unavailable (fall back to raw counts, flagged as unclassified).
- Update/extend Heart tests covering the sync table if any exist.
- **Cadence leg:** establish a semi-regular `/repo_cleanup` cadence — a
  scheduled weekly *audit-only* run (read-only phase 1 report, e.g. alongside
  the existing morning-health crons) that surfaces the report for the user;
  mutations stay interactive per the skill's confirmation rules.
