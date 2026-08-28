# Interferometer pixelization examples: linear bulge + pixelization hybrid on the sparse path

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

# Interferometer pixelization examples: linear bulge + pixelization hybrid on the sparse path

Type: docs
Target: autogalaxy_workspace
Repos:
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal

## Problem

`scripts/interferometer/features/pixelization/{fit,modeling}.py` reconstruct the whole `clumpy` galaxy on the
mesh "for simplicity (no parametric bulge)", pointing at the imaging counterpart for the hybrid model. The
only real reason was that the sparse-operator path could not combine a linear light profile with a mapper;
since the array library's #500 it can.

## Fix

Convert both scripts to the linear-bulge + pixelization hybrid mirroring the imaging examples: `fit.py` adds
`ag.lp_linear.Sersic` with the simulator's bulge geometry alongside the `RectangularUniform` pixelization on
the `apply_sparse_operator()` dataset and indexes both linear objects; `modeling.py` fits
`af.Model(ag.lp_linear.Sersic)` + pixelization (N = 1 + 6). Update the intro / model / linear-objects prose,
keep mesh + regularization unchanged, run both under the smoke profile, regenerate the two notebook twins.
Not applied to the lens workspace: its interferometer datasets contain no lens light (science reason).

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b766a19b-260c-4b56-8d19-072fa9a34b28/scratchpad/intake_bulge_pix.md -->
