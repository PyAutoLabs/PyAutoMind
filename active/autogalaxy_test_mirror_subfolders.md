# autogalaxy_workspace_test: mirror taxonomy + task subfolders (autolens recipe, one pass)

Type: refactor
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised

Apply the completed autolens_workspace_test recipe (#211/#212/#216/#217) in
ONE pass: mirror autogalaxy_workspace's top-level taxonomy, task subfolders
(jax_likelihood/ jax_grad/ visualization/ simulator/ where >=2 scripts,
provenance-split, singletons at root), redundant prefixes stripped, misc/ for
dataset-agnostic dirs (aggregator, latent, model_composition, jax_assertions —
check whether ellipse/ and quantity/ exist in the USER workspace's top level
first; mirror what it actually has). Move-only, git mv, zero deletions.
Gates identical to the autolens passes. Simulator auto-bootstrap = separate
follow-up (inventory reported, not converted).
