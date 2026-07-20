# Split lensing regimes into multi_galaxy_lens, group and cluster

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
- autolens_workspace_test
- workspaces
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

Reorganize the PyAutoLens documentation and example library by splitting systems
above the standard single-galaxy strong-lens regime into THREE distinct categories,
applied throughout the PyAutoLens docs, autolens_workspace, autolens_workspace_test,
and profiling (developer) workspaces:

  1. multi_galaxy_lens
  2. group
  3. cluster

This is primarily a documentation and workflow decision intended to help users
understand the different modelling regimes they are likely to encounter. The final
documentation should present these as three separate sections, each with its own
tutorials, example scripts, API documentation, and modelling philosophy.

For each regime, research representative example lenses, well-known papers, and
observational samples (e.g. SLACS, BELLS, HST Frontier Fields, etc.) to motivate the
examples we include. Use Fable (or equivalent literature research) to identify the
best examples rather than relying on prior knowledge. Recommend the most appropriate
real lens systems, surveys, papers, and benchmark datasets to accompany each section
so tutorials are grounded in widely used literature examples.

## 1. Multi-galaxy lenses
Galaxy-scale strong lenses where two or more galaxies contribute significantly to the
lensing potential, but there is NO dominant group or cluster dark matter halo.
Host halo masses ~10^11-10^13 M_sun; no separate group-scale halo required. Mass model
= multiple galaxy-scale mass profiles (EPL, SIE), one per significant deflector, plus
external shear where appropriate. These galaxies are co-dominant lenses, not satellites
embedded in a larger host halo. Source modelling = standard PyAutoLens workflow, either
parametric source light (Sersic) or pixelized source reconstructions (Delaunay, adaptive
meshes).

## 2. Group-scale lenses
Dominant group-scale dark matter halo, total masses ~10^13-10^14 M_sun. Lens galaxies
represented as tidally truncated subhalos (Pseudo-Jaffe or truncated isothermal) whose
parameters are usually tied through scaling relations. IMPORTANT: every group-scale
tutorial and example should present the inclusion of the group dark matter halo as an
EXPLICIT modelling choice. Some systems genuinely require a group halo; others may be
adequately described by the galaxy members alone. Users should learn BOTH workflows and
understand when introducing a host halo is scientifically motivated; the docs must
explain this decision rather than assuming the host halo is always present. Source
modelling: typically ONE dominant extended lensed source, a natural extension of the
existing source reconstruction framework (Sersic, multi-Gaussian, pixelized Delaunay,
adaptive meshes). Mass model more sophisticated than galaxy-scale, but source-modelling
philosophy largely unchanged.

## 3. Cluster-scale lenses
NOT fundamentally different from group lenses in mass parameterization. Halo masses
> 10^14 M_sun (often 10^15). Mass model still = one or more extended host halos + many
truncated member galaxies + scaling relations for the galaxy population. PyAutoLens
should distinguish cluster-scale lenses through the SOURCE MODELLING STRATEGY. Clusters
commonly contain dozens-to-hundreds of member galaxies and simultaneously lens many
independent background galaxies over a wide redshift range; modern cluster models include
tens-to-hundreds of multiply-imaged systems. Reconstructing every source as extended
Sersic/pixelized is generally not practical or necessary. Standard strategy becomes:
multiple image positions; point-source constraints; individual source redshifts; joint
optimization of a common cluster mass model. Extended source reconstructions should be
presented as specialised follow-up analyses of individual systems, not the default
cluster workflow.

## Documentation structure (three regimes)
- Multi-galaxy: multiple co-dominant galaxy halos; no explicit host halo; standard
  extended source reconstruction.
- Group: optional host halo (user decides); truncated member galaxies; single extended
  source via parametric or pixelized methods.
- Cluster: one or more host halos; large populations of truncated member galaxies
  (typically >20, often hundreds); many background sources at different redshifts;
  default workflow based on point-source constraints rather than extended reconstruction.

Key design principle: group- and cluster-scale lenses share essentially the SAME mass
modelling framework; the distinction in PyAutoLens is driven by the observational regime
and therefore the source modelling strategy.

## Additional key requirements
1. Retain the main_galaxies / extra_galaxies / scaling_galaxies API for ALL three
   regimes; all 3 tiers are used across all 3 examples. Basic MGL examples use just
   main_galaxies, but include extra_galaxies and scaling_galaxies as extensions in
   features (analogous to imaging / interferometer / point_source single-galaxy examples).
   Group-scale default start_here and simulator/modeling examples should include scaling
   galaxies and extra galaxies; cluster obviously should too.
2. For galaxy-scale examples (imaging, interferometer, point_source) in features, include
   examples with extra_galaxies and scaling_galaxies, but make clear that while
   extra_galaxies are expected to be used, scaling_galaxies would just be a load of
   galaxies far from the lens.
3. The scaling_galaxies in the galaxy-scale and multi-galaxy-lens examples should NOT
   include truncation, and thus use mass profiles like isothermals (untruncated) — which
   follows how scaling galaxies are currently implemented in the group package, consistent
   with the discussion above.

## Execution note
Documentation + workflow + example-library reorganization spanning PyAutoLens docs,
autolens_workspace, autolens_workspace_test, and profiling/developer workspaces. The
actual implementation will be re-planned in Fable (including the literature research);
this intake only needs to capture and formalize the requirement, classified and sized,
ready to go.

<!-- formalised by the Intake (Conception) Agent on 2026-07-20 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4f664d3e-f867-455d-891d-fa159bb6c79a/scratchpad/mgl_group_cluster_split.md -->
