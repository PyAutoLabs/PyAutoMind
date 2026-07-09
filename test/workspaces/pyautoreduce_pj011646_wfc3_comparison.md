# PyAutoReduce validation: PJ011646 WFC3 reduction vs Aris's dataset

Type: test
Target: workspaces
Repos:
- autolens_assistant
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Follow-up to the slacs1430+4105 PyAutoReduce validation: reduce the lens PJ011646 from archival HST/WFC3 data using PyAutoReduce and compare the result to Aris's existing dataset at /mnt/c/Users/Jammy/Science/aris_PJ011646/dataset/aris/PJ011646. Same comparison methodology as the SLACS task (image/noise/PSF residuals plus lens-model parity fits via autolens_assistant); exercises the WFC3 reduction path rather than ACS. Blocked-by: the slacs1430+4105 comparison task should ship first so the methodology is settled.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
