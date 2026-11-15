# Smoke install tfp comment sweep in workspaces

Type: maintenance
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
- HowToGalaxy
- HowToLens
- euclid_strong_lens_modeling_pipeline
Themes:
- hygiene
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Witness: `grep -n -i "tfp\|tensorflow" .github/scripts/smoke_install.sh` in each listed repo shows only the updated note that tensorflow-probability is no longer a dependency (wording identical to autolens_workspace_test / autogalaxy_workspace_test after PyAutoArray#694), no command lines change, and each repo's smoke CI is green.
Review-minutes: 0
Unattended: ready
Lane: any
Issued: 2026-11-15
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/673

Follow-up from PyAutoArray#694 (vendored `bessel_kve`, dropped `tfp-nightly`; record
`complete/2026/11/matern-vendor-bessel-kve.md`). The two workspace_test repos had their
`.github/scripts/smoke_install.sh` comments updated in autogalaxy_workspace_test#137 and
autolens_workspace_test#366. The same stale comment ("The working modified-Bessel dependency is
`tfp-nightly`, pinned by `PyAutoArray[optional]` above", and "#184 removed that dependency when the
stack moved to tfp-nightly") remains in the five repos above. Comment-only change; mirror the
workspace_test wording.

<!-- formalised by the Intake (Conception) Agent on 2026-11-15 from file:/tmp/claude-0/-home-user/3f1fc7c8-0fc2-59a3-b82b-ac29d67b5941/scratchpad/intake2.md -->
