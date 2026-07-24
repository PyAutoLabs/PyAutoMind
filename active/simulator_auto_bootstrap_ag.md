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
