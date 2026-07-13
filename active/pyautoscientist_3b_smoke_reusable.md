# PyAutoScientist 3b-2: generalise smoke_tests.yml into a reusable workflow

Type: maintenance
Target: PyAutoBuild
Repos:
- PyAutoBuild
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft — issue when phase3a ships

The ~10 per-workspace smoke_tests.yml files are fat hand-copies
(hard-coded dependency-chain checkouts). Create one reusable workflow
(Build- or Heart-owned; follow the docs-build.yml precedent) parameterised
by package + dependency chain; convert ONE workspace first, diff the
check runs for parity, then sweep the rest + HowTos. Update Heart's
required-workflow names only if they change (they should not). This is
the missing piece that makes an adopter's workspace CI a thin caller —
and deletes ~9 duplicate files from the live setup.
