# Remove empty modeling headings from workspace examples

- Status: complete
- Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/574
- PR: https://github.com/PyAutoLabs/autolens_workspace/pull/575
- Merge commit: `2439de9073229bcdaded899878fc34310ec9a0cf`
- Completed: 2026-09-20

## Shipped

Removed all 17 empty `__External Shear__` sections from the autolens_workspace scripts and regenerated notebooks. Preserved all 17 `__Source Galaxy__` sections and executable model composition.

## Validation

- No `__External Shear__` section remains in scripts or generated notebooks.
- All 17 `__Source Galaxy__` sections remain in scripts and generated notebooks.
- Touched scripts compile and the script size guard passes.
- Local smoke suite passed: 37/37 curated scripts and 2/2 curated notebooks.
- GitHub CI passed all seven jobs, including Python 3.12 and Python 3.13 smoke tests.

## Original prompt

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
