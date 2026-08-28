# sparse-interferometer-docs-sweep

Follow-up to #499/#500 (interferometer sparse operator now supports linear light profiles / MGE /
basis func lists alongside one or more pixelizations). User brief: correct factually incorrect
statements only; no new scripts.

## Shipped
- autolens_workspace #509 / autogalaxy_workspace #227 — prose-only: five
  `# interferometry does not support lens light` comments → the files' own scientific wording;
  seven "VRAM driven by visibility count" generalisations qualified (sparse operator → mask-only);
  "pixelizations use less VRAM than light-profile-only models" → any inversion; SLaM two-dataset
  justifications ("because pixelized reconstructions exploit sparsity", "source_lp does not need it")
  → cost-based wording noting one sparse dataset can serve every stage; two READMEs; both
  `many_visibilities_preparation.py` intros. Notebook twins of edited scripts regenerated.

## Deliberately left alone
- "lens light omitted because interferometer data does not contain it" (science), Bilinear-mesh
  gradient limitation on the sparse path, CPU-numba performance notes, potential-correction
  dense-vs-sparse verification prose, `start_here.py` DFT/NUFFT sentence.
- autogalaxy `pixelization/{modeling,fit}.py` "no parametric bulge for simplicity" — a natural place
  to now demonstrate linear bulge + pixelization on the sparse path (new example; user deferred).

## Original prompt

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
Issued: 2026-08-28
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
