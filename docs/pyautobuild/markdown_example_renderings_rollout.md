# Markdown example renderings — phase 2 rollout (workspaces + HowTo)

Type: docs
Target: workspaces
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Roll the executed-markdown rendering system (built in phase 1: PyAutoBuild
generate_markdown.py + the autolens_workspace pilot, PRs PyAutoBuild#137 +
autolens_workspace#263, issue PyAutoBuild#134) out to the rest of the
user-decided curated list. Prerequisite: phase-1 PRs merged. The generator is
repo-agnostic, so this is config + execution + README links per repo — no new
tooling expected.

Scope (from the user's 2026-07-10 decision, minus what phase 1 shipped):

- autolens_workspace remaining dataset types: interferometer, point_source,
  multi, group, weak — per type the curated five where they exist
  (start_here, simulator, likelihood_function, fit, modeling); NOTHING from
  features/ folders. cluster is EXCLUDED pending a runtime decision (known
  >500s even in TEST_MODE; a real cluster modeling run may be many hours —
  ask before including).
- autogalaxy_workspace: root start_here.py + imaging/interferometer/multi/
  ellipse curated five + its guides equivalents.
- autofit_workspace: its flagship examples (no root start_here.py exists —
  survey the workspace and propose the curated set; likely overview/ +
  cookbooks entry points).
- HowToFit / HowToGalaxy / HowToLens: curated list still UNDECIDED — propose
  (e.g. the first tutorial of each chapter) and confirm with the user before
  building.

Operational notes from phase 1 (all enforced/learned in the generator):
execution is never TEST_MODE — each modeling script pays one real sampling
run, cached in output/ for near-instant regeneration (measured 122s vs
1h55m); the build restores tracked files scripts modify; leave the workspace
tree alone while a build runs; local paths are redacted from published
output; expect ~2MB per rendered page with images. Each new repo needs its
config/build/markdown_examples.yaml, README links, and a check that its
.gitignore doesn't swallow markdown/ (autolens's `**/images/` rule was safe
because nbconvert emits `*_files/`). Consider PNG size optimization
(fixed dpi / pngquant) if totals grow beyond the autolens pilot's 19M.
