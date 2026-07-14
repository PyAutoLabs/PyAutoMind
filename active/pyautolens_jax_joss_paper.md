# Set up the PyAutoLens-JAX JOSS paper

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Request

Create a second JOSS paper template alongside the existing `PyAutoLens/paper`
directory. Give the new paper the title:

> PyAutoLens-JAX: Differentiable GPU-accelerated strong and weak lensing from galaxies to clusters

Preserve the existing paper and follow its repository-local JOSS structure and
conventions where appropriate.

## Summary draft supplied by the author

> Gravitational lensing probes luminous and dark matter from individual galaxies to groups and clusters, using observations that increasingly provide multiple complementary forms of information. A single system may include multi-band optical or infrared imaging, radio interferometer visibilities, point-source constraints from lensed quasars or supernovae, and weak-lensing shear measurements. Fully exploiting modern lensing datasets therefore warrants joint probabilistic modelling across physical scales, lensing regimes, and observational data types.
>
> PyAutoLens is now implemented using JAX throughout its core modelling framework, providing just-in-time compilation, GPU acceleration, and automatic differentiation without introducing a separate package or replacing its established object-oriented API. Galaxy-, group-, and cluster-scale mass models can be constrained using strong lensing, weak lensing, CCD imaging, interferometer visibilities, and point-source observables. Crucially, these are not isolated capabilities: users can combine any number of datasets, lensing regimes, lens planes, and physical scales within a single differentiable, GPU-accelerated probabilistic model.

## Original request verbatim

> ok, we are now writing another PyAutoLEens JOSS paper whiuch can go side by side with the paper in PyAutoLens/paper, can you set up a template in the repo and make the title PyAutoLens-JAX: Differentiable GPU-accelerated strong and weak lensing from galaxies to clusters
