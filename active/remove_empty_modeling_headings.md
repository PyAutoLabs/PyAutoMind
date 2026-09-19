# Remove empty modeling headings from workspace examples

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- notebooks
- mass-field
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: No script or generated notebook contains an `__External Shear__` section; all `__Source Galaxy__` sections and executable model composition remain unchanged.
Filed: 2026-09-20
Issued: 2026-09-20

## Original user request

> We still have empty __External Shear__ sections everywhere, simply do not make this a docstringed section and remove it. Also, simulator.py files have __Source Galaxy__ which is empty under __Ray Tracing__ which describes the surce and is also not required

## Intended scope

Remove all 17 now-empty `__External Shear__` headings left by the previous prose cleanup. Preserve every `__Source Galaxy__` section. Edit scripts only, regenerate notebooks through PyAutoHands, and validate that no external-shear section remains.
