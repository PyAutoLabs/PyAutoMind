# Roche against pyHalo tidal-track subhalo stripping: explain the factor of 70

Type: research
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: A short note decomposes the gap between the two stripping models into its parts (bound mass, truncation radius, the density rescale f_t, the compensating sheet, the r₃D and infall-redshift inputs), gives the number each part contributes, and ends with one of three verdicts backed by those numbers: a genuine physical difference between the models, a bug (named, with file and line, in the project's Roche code, in the pyHalo adapter, or in pyHalo), or another stated explanation.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

## Finding

The `dm_sightlines` science project draws lens subhalos in infall M200c (10⁶–10¹⁰ M☉, f_sub = 1.6%
inside 2θ_E) and truncates them in one of two ways:

- **Roche** (the project's fiducial; Gilman et al. 2020): r_t = 1.4 kpc (m/10⁷ M☉)^(1/3)
  (r₃D/50 kpc)^(2/3), no change to ρ_s.
- **pyHalo's tidal track** (pyHalo 1.5.3's CDM default, `TRUNCATION_GALACTICUS_ZINFALL`, called
  through `sightlines/population/pyhalo_adapter.py`): a bound mass drawn from a fit to Galacticus
  as a function of infall concentration and z_infall − z_lens at host concentration 6, then ρ_s
  scaled by f_t (Du et al. 2024) and r_te solved so the profile's total mass is the bound mass.

On the same 2,210 subhalos per realisation (8 seeds, z_lens 0.5, z_source 1.0, θ_E 1.6″):

| | Roche | pyHalo tidal track |
|---|---|---|
| median r_t / r_s | 4.36 | 0.0575 |
| bound-mass fraction inside 2θ_E | 1.44% | 0.071% |
| ρ_s relative to Roche at 10⁷, 10⁹ M☉ | 1, 1 | 0.27, 0.62 |
| compensating sheet κ | −0.00756 | −0.00034 |
| Δχ² surviving a full refit, subhalos alone | 96 [86, 268] | 1.3 [0.6, 5.1] |
| Δχ² surviving a full refit, subhalos + line of sight | 178 [124, 371] | 55 [17, 70] |

The line of sight alone gives 41 in both. So the subhalo contribution to the surviving lensing
signal differs by a factor of about 70, and the bound mass by about 20. A third variant, Roche with
subhalo structure evaluated at the lens redshift instead of at infall, gives 32 for subhalos alone.

What has been checked: the project's Roche formula matches pyHalo's `TRUNCATION_ROCHE_GILMAN2020`
by reading; the adapter reproduces pyHalo's two calls and the truncated profile's total mass equals
the sampled bound mass to 10⁻⁶; one whole pyHalo realisation traced by lenstronomy and by the
project agrees to 7.5×10⁻¹⁵″. What has not: whether either model's output is right.

## Why it matters

Which population dominates the signal that survives a macro-model refit, subhalos or the line of
sight, flips with this choice (73% subhalos with Roche, 6% with the tidal track). Any forecast or
inference built on the simulator inherits it. The human ruled on 2026-11-25 that Roche stays the
project's fiducial with the pyHalo model as an option; this investigation is to say why they differ
so much and whether that is physics.

## Questions to answer

1. **Decompose the gap.** Hold the subhalos fixed and change one thing at a time: Roche r_t with
   pyHalo's f_t; pyHalo's r_te with f_t = 1; Roche radii rescaled to give pyHalo's bound masses;
   each with and without its sheet. Which step carries the factor of 70 in Δχ², and why is it
   larger than the factor of 20 in bound mass?
2. **Is pyHalo's stripping the size the literature says?** At host concentration 6 pyHalo's median
   log₁₀(m_bound/m_infall) is −2.97 [−4.78, −1.81] for infall concentration 6 at Δz = 3.3, and the
   project's median infall redshift is 3.8. Compare with Du et al. 2024/2025 (bound mass function
   about 20 times below the infall one near the Einstein radius), with Galacticus output if it can
   be had, and with N-body results for subhalos in projection near the Einstein radius of a
   10¹³ M☉ host.
3. **Is Roche the size the literature says?** The Roche radius is evaluated at the subhalo's
   present r₃D, with no orbit history and no change to the inner density. Median r_t/r_s = 4.4
   keeps about 90% of the infall mass. Is that how Gilman et al. 2020 used it, what r₃D
   distribution did they pair it with, and what bound fractions did they report?
4. **Inputs to pyHalo's model.** It takes a redshift difference, z_infall − z_lens, on a grid that
   ends at Δz = 8.1 and extrapolates linearly to a clip at 9.5 (a docstring there says "time
   elapsed since infall in Gyr"; the code returns a redshift difference). What fraction of the
   project's subhalos fall in the extrapolated region, and does the bound-mass fraction change if
   they are excluded? Is host concentration 6 right for a 10¹³ M☉ host at z = 0.5 (the project's
   own host concentration is 5.51)?
5. **Bug hunt, both sides.** Units and cosmology in the adapter (pyHalo H0 = 67.5 against Planck15;
   kpc against arcsec; M200 against total mass); the r₃D the project feeds Roche (drawn conditional
   on the projected radius, where pyHalo draws it independently); pyHalo rounding truncation radii
   (to 0.001 kpc in Roche, to 10⁻¹⁰″ on output, which made one stripped subhalo's radius zero);
   the tidal-track sheet, whose reference population is 40,000 subhalos (6.6% Monte Carlo error);
   pyHalo's own subhalo sheet, which removes about 17 times the bound mass it renders.
6. **The lens-redshift variant.** Why does evaluating structure at z_lens instead of at infall cut
   the Roche subhalo signal to a third, and does the same explanation account for part of the
   pyHalo gap (pyHalo also sets structure at infall)?

## Out of scope

Changing the project's fiducial (ruled: Roche stays) or library code. The outcome is a note. A bug
found in the project is fixed in the project; a bug found in pyHalo is reported to its author by
the human.

## Provenance

[from: dm_sightlines science project, phase 5, 2026-11-25] Filed at the human's explicit request:
"intake an issue to compare Roche to PyHalo in more detail and work out if its a genuine physical
thing or bug or give an explanation". Numbers:
`Science/development/dm_sightlines/results/phase5_sensitivity/SUMMARY.md` and
`dataset_summary.md` (RAL job 416199);
`Science/development/dm_sightlines/results/phase5_pyhalo/NOTES.md` section 4 and
`galacticus_check.json`; summary in
`Science/development/dm_sightlines/wiki/project/phase5_note.md` section 5.1. pyHalo lives only in
the overlay environment `~/Code/PyAutoLabs/scratch/dm_sightlines_output/venv_x`. The project is
exploratory and separate from the Mind orchestrator; this is a bounded prompt, not an epic.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/b8695ba5-cbcf-4056-87b2-33b1f080236d/scratchpad/raw/p_roche_vs_pyhalo.md -->
