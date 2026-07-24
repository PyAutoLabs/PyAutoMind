## Outcome — SHIPPED + MERGED 2026-07-24 (PR #95)
Issue #94 closed. autolens#213 recipe: 4 datasets byte-repro-VERIFIED
(np.array_equal after seeded regen) then tip-removed (19 files, 1.3MB); 42
consumers guard-swapped path.exists->should_simulate (ALL already carried
bootstraps — ag_test was born with the pattern); 4 BOOTSTRAP-TARGET no_run
entries; 1 declaration removal (imaging/model_fit). Cleaner than autolens:
zero real/external data, no protective cases, no gitignore allowlist.
Dry-runs 6.7-7.8s. All gates green.

## Original prompt

# autogalaxy_workspace_test: simulator auto-bootstrap (autolens #213 analogue)

Type: refactor
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised

Apply the autolens_workspace_test#213 conversion: should_simulate bootstrap
in consumers, git rm the regenerable datasets (tip-removal only), BOOTSTRAP-
TARGET no_run entries, declaration audit. The #92 inventory already
classified ALL FOUR committed datasets (imaging/interferometer/ellipse/multi
jax_test) as seed-fixed regenerable with no byte-tuned literals and no
protective cases — a clean conversion. Gates as #213 (incl. clean-clone
bootstrap dry-runs).
