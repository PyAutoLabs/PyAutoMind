# Pre-release documentation and configuration consistency

Type: refactor
Target: autogalaxy_workspace
Repos:
- HowToFit
- autofit_workspace
- autogalaxy_workspace
Consequence: judge
Autonomy: supervised
Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
Issued: 2026-10-25

## Original request

"Can we do more heart and hygeine work before release to properly clean up loads"
"Ok do all that and the continue"

## Scope and plan

Clean the non-overlapping part of the verified hygiene findings: three adjacent documentation boundaries in HowToFit tutorial_7_the_details.py; two boundaries in autogalaxy_workspace pixelization modeling/fit scripts; six missing config keys in autofit_workspace and nineteen in autogalaxy_workspace. No changes to scientific code, output identifiers, thresholds or existing workspace overrides. Source-only main snapshots are used in session clones.

1. Combine the five adjacent documentation blocks, preserving all prose and executable AST.
2. Add only absent YAML leaves from the corresponding library defaults, preserving comments and existing values. Verify effective merged values unchanged.
3. Regenerate notebooks/catalogues through PyAutoHands; check notebook prose and code preservation and run the required workspace smoke validation where supported.
4. Keep remaining autolens_workspace work blocked by the active matrix-free task; do not take its repo claim.
5. Prepare reviewable diffs and verification. Heart remains RED; development shipping needs task-specific current authorization, separate from the earlier Nerves corrective approval. No merge, release or rehearsal.

Tier: judge — merge mode: human /prm.

## Completion

All five documentation findings removed and 25 mirror gaps accounted for without changing effective config or executable statements. Generated artifacts verified; smoke results and limitations stated. Source PRs require the existing Heart gate, never a waived test.
