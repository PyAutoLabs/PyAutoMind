## Outcome — SHIPPED + MERGED 2026-07-24 (PR #93)

Issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/92
(closed). The full autolens recipe (#212+#216+#217) in ONE pass: mirror
taxonomy (ellipse/ imaging/ interferometer/ multi/ + misc/ — ellipse is a
dataset PEER in the user workspace, checked not assumed; multi/ created),
provenance-split task subfolders, prefix strip, 148 git-mv renames, zero
non-__init__ deletions. All gates identical-resolution green (54 scripts).

## Notables
- One-pass is cheaper than autolens' two passes — the recipe is now proven
  transferable; autocti/autofit _test repos differ structurally (autofit has
  no dataset taxonomy) so only sub-moves apply there if ever wanted.
- Simulators stayed in jax_likelihood/ (no pre-existing simulator/ dirs; all
  jax-declared so the segment rule holds).
- Dataset inventory (on #92): ALL FOUR committed datasets seed-fixed
  regenerable, no byte-tuned literals, no protective cases — the follow-up
  auto-bootstrap conversion is clean (drafted).

## Follow-ups
draft/refactor/autogalaxy_workspace_test/simulator_auto_bootstrap_ag.md
(issue when wanted — clean per the inventory).

## Original prompt

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
