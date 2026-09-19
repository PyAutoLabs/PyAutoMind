# Trim external-shear narrative from workspace examples

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
Witness: Workspace scripts no longer contain the expanded `__External Shear__` explanatory prose or the verbose `MassField` parenthetical, while the examples retain their field composition and generated notebooks match the scripts.
Filed: 2026-09-19

## Original user request

> The __External Shear__ section in imaging/modeling.py and other script is wayyyyy too much information and text, it didnt use to explain the shear at all. I think literally all the text under it can be removed, This can also be removed (a `MassField`, its own model object -- see `__External Shear__` below), maybe with a small note in brackets to say it is extensible and other fields could be added.

## Intended scope

Review the matching external-shear prose across the workspace scripts rather than fixing only one generated example. Remove the recently expanded explanatory paragraphs, shorten the inline model-composition label to a small note that other fields can be added, preserve all executable `MassField` / `fields=` composition, regenerate notebooks from scripts, and run the documentation and workspace guards appropriate to prose-only edits.
