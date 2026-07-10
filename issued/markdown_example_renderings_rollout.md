# Markdown example renderings — batch 2a (three workspaces)

Type: docs
Target: workspaces
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Roll the executed-markdown rendering system (built in phase 1: PyAutoBuild
generate_markdown.py + the autolens_workspace pilot, PRs PyAutoBuild#137 +
autolens_workspace#263 — BOTH MERGED 2026-07-10, issue PyAutoBuild#134 closed)
out to the three workspaces. The generator is repo-agnostic, so this is config
+ execution + README links per repo — no new tooling expected. User direction
2026-07-10: run this phase on Opus. The HowTo trio is a separate follow-on
batch 2b ([[markdown_renderings_howto]]).

Decisions locked 2026-07-10: cluster EXCLUDED (heaviest fit, least
representative — add later as a one-off once run cost is known); workspaces
first, HowTo second; sequential builds (memory pressure).

Curated lists (grounded in a survey — only scripts that exist):

- **autolens_workspace** (extend phase-1 config): interferometer
  (start_here/simulator/likelihood_function/fit/modeling), point_source
  (start_here/simulator/fit/modeling — no likelihood_function), multi
  (start_here/simulator/modeling), group (all five), weak
  (simulator/likelihood_function/fit/modeling — no start_here). NOTHING from
  features/. cluster excluded.
- **autogalaxy_workspace** (new config + README links): root start_here.py;
  imaging (all five); interferometer (all five); multi
  (start_here/simulator/modeling); ellipse (simulator/fit/modeling); guides
  galaxies.py + data_structures.py.
- **autofit_workspace** (new): overview/overview_1_the_basics.py,
  overview_2_scientific_workflow.py, overview_3_statistical_methods.py
  (no start_here.py exists; 1D-Gaussian fits, seconds each).

Operational notes from phase 1 (all enforced/learned in the generator):
execution is never TEST_MODE — each modeling/start_here fit pays one real
sampling run, cached in output/ for near-instant regeneration (measured 122s vs
1h55m); the build restores tracked files scripts modify (all three main
checkouts carry stale dataset regen dirt — the worktree branches clean); leave
the workspace tree alone while a build runs; local paths are redacted; expect
~2MB per rendered page. Each new repo needs config/build/markdown_examples.yaml,
README links, and a git check-ignore on markdown/ (autogalaxy/autofit have no
images/ rule, so clean). Wall-clock ~8-20h cumulative real sampling across ~13
genuine fits (point_source/multi quick; interferometer/group/imaging modeling
heavy); resumable background build. Consider PNG size optimization if a repo's
total grows well beyond the autolens pilot's 19M.
