# O'Riordan M_max to virial mass: a factor 15 to 40 mismatch…

Type: research
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A short note states, with the equations and the numbers, which mass O'Riordan et al.'s `M_vir` column is (NFW-equivalent virial mass of the (v_max, r_max) profile, pre-infall mass of a stripped subhalo, or something else), reproduces at least three rows of their 2023 Table 1 from that reading to 10%, and gives the conversion a simulator should use between infall M200c and M_max with its range of validity; or it records that the table cannot be reproduced and the question that was put to the author.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

O'Riordan et al. define subhalo mass as M_max, the mass inside r_max, and model subhalos as NFW
profiles in (v_max, r_max). Table 1 of their 2023 paper (arXiv 2211.15679, z = 0.5) maps
M_vir = 1e8, 1e9, 1e10, 1e11, 1e12 to M_max = 10^6.2, 10^7.4, 10^8.6, 10^9.8, 10^11.0, a constant
ratio M_vir / M_max of about 63, with v_max = 6.3 to 134 km/s and r_max = 0.16 to 22.3 kpc.

An NFW profile fixed by (v_max, r_max) has a definite M200c. Two checks on 2026-11-20 disagree with
the table by more than an order of magnitude:

- The `dm_sightlines` project's `ORiordan2025` preset (Moliné et al. 2022 redshift fit for
  r_max(v_max), as the 2024 and 2025 papers cite) gives M200c / M_max = 4.3, 4.3, 3.4, 2.7, 1.7 for
  those five M_max values.
- By hand, from the table's own first row (v_max = 6.3 km/s, r_max = 0.16 kpc): M_max =
  v_max^2 r_max / G = 1.5e6, as tabulated; the NFW through that point has concentration about 50
  and M200c of about 9e6, six times M_max, not 63 times. For a 1e8 halo with their quoted
  concentration of 60 the NFW mass inside r_max would be about 1.5e7, not 1.6e6.

So the tabulated M_vir is not the virial mass of the NFW profile that (v_max, r_max) defines. The
usual difference between virial and 200c masses is at most about 1.3 and cannot explain it.

## Why it matters

The simulator's fiducial subhalo population is drawn in infall M200c and its O'Riordan preset in
M_max. Comparing the two, converting f_sub between them, and saying which of our masses an
O'Riordan sensitivity limit (for example 10^8.8 in M_max for Euclid) corresponds to all depend on
this conversion. A factor of 4 against a factor of 63 moves that correspondence by more than a
decade in mass. It also decides whether "1e6 to 1e11 in M_max" overlaps our "1e6 to 1e10 in M200c"
almost entirely or hardly at all.

## Questions to answer

1. What is `M_vir` in their Table 1? Candidates: the pre-infall (peak) virial mass of a subhalo
   whose present-day, tidally stripped profile has that (v_max, r_max), taken from the ShinUchuu
   catalogues they fitted; a virial mass with respect to the mean matter density; or a relation
   between M_max and M_vir fitted to simulation data independently of the NFW form. Read the 2023
   paper's Section 2 and table caption closely, and the Moliné et al. catalogue definitions.
2. Does the 2023 concentration column (c_vir of 60, 42, 30, 21, 15) follow from r_vir / r_s or from
   r_vir / r_max? The numbers suggest checking both.
3. Which conversion do the 2024 and 2025 papers use, if any? They switch to the Moliné 2022
   relation and never reprint the table.
4. If the answer is "pre-infall mass of a stripped subhalo", what bound-mass fraction does it
   imply, and how does that compare with the tidal-track model pyHalo uses (Du et al. 2025: bound
   mass function about 20 times below the infall one near the Einstein radius)? A factor of 15 to
   40 is the same order.
5. Ask Conor O'Riordan if the papers do not settle it.

## Out of scope

Changing library code. The outcome is a note and, if it changes a conversion a library docstring
or workspace example states, a separate bounded prompt.

## Provenance

[from: dm_sightlines science project, phase 3, 2026-11-20] Filed at the human's explicit request
as a follow-up investigation. Numbers: `Science/development/dm_sightlines/results/phase3_subhalos/SUMMARY.md`
(check 2); literature notes with the table transcribed:
`Science/development/dm_sightlines/wiki/project/literature/subhalo_modelling_notes.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-20 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/p_oriordan.md -->
