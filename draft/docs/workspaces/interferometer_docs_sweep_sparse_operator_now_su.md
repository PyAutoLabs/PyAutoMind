# Interferometer docs sweep: sparse operator now supports linear light profiles + pixelizations

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
- autolens_workspace
- workspaces
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

# Interferometer docs sweep: sparse operator now supports linear light profiles + pixelizations

Type: docs
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal

## Problem

Since the array library's #500 (issue #499) the interferometer sparse-operator inversion path supports
linear light profiles / MGE / basis func lists fitted alongside one or more pixelizations. Workspace
prose still frames the sparse operator as a pixelization-only tool: five `# interferometry does not
support lens light` comments, seven "VRAM on interferometer datasets is driven primarily by the
visibility count" generalisations, "Pixelizations use a lot less VRAM than light profile-only models,
provided the sparse operator…", the SLaM two-dataset framing ("because pixelized source
reconstructions exploit sparsity", "`source_lp` does not need it") in five pipelines and two READMEs,
and the `many_visibilities_preparation.py` intro.

## Fix

Prose-only corrections of the statements above (original request: "find examples which say this type
of analysis is not possible and update them to say it is. Dont add any new scripts or the like for
now, just replace factually incorrect statements"). Pipelines and code unchanged. Regenerate only the
touched scripts' notebook twins. Out of scope: lens-light-omitted-for-science statements, the Bilinear
gradient limitation, CPU-numba performance notes, potential-correction verification prose.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b766a19b-260c-4b56-8d19-072fa9a34b28/scratchpad/intake_docs_sweep.md -->
