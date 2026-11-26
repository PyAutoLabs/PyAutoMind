# Building blocks

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Autonomy: supervised
Priority: high
Status: draft
Epic: stars-gnfw-lens-model-in-the-mass
Phase: 1
Witness: unit tests show the 2F1 helper matches `scipy.special.hyp2f1` to 1e-12 for slopes 0 to 2.4 on NumPy and JAX, and each aperture-normalised profile encloses its `mass_ap` inside `theta_ap` to 1e-8.
Lane: any
Filed: 2026-11-25

A shared JAX-safe 2F1 helper for the gNFW enclosed mass, the ring convergence and enclosed mass from deflections, and the Sérsic (usable mass-only) and gNFW profiles normalised by projected mass inside an aperture.

Slice 2 wraps these in a general mass-sheet frame (the epic prompt's "Assessment" section, settled 2026-11-26). Two things follow for this slice: the ring helper returns the projected mass inside the ring as well as the ring convergence (one deflection call on three rings), and the aperture-normalised Sérsic works as a mass-only profile, because the frame holds the stars' mass while the galaxy holds their light.

## Seam

Slice 1 of 4 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns PyAutoGalaxy; first — nothing before it; before slice 2 (The mass-sheet frame). One unattended run; reviewed against its own witness; revertible on its own PR(s).
