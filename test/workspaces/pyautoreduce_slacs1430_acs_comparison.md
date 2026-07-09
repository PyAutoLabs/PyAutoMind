# PyAutoReduce validation: slacs1430+4105 ACS reduction vs trusted legacy dataset

Type: test
Target: workspaces
Repos:
- autolens_assistant
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Validate PyAutoReduce against a trusted legacy reduction: reduce the SLACS lens slacs1430+4105 from archival HST/ACS data using PyAutoReduce, then compare the resulting modeling-ready dataset (data, noise map, PSF) to the long-used collaborator-provided dataset at /mnt/c/Users/Jammy/Science/subhalo/dataset/slacs/slacs1430+4105 (used for many years in subhalo work). Comparison is a science project driven through autolens_assistant: image/noise/PSF residuals plus lens-model parity fits on both datasets.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
