# autolens_jax_joss benchmark repo + real-data start_here pairing

Type: feature
Target: autolens_workspace
Repos:
- autolens_jax_joss (new repo)
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Create a repo autolens_jax_joss which provides examples to run each JAX benchmark from the PyAutoLens-JAX paper draft and reports the run time and info. These benchmarks currently do not exist.

Single-dataset and single-regime benchmarks (establish GPU acceleration and autodiff across lensing scales and data types):

- Galaxy-scale CCD imaging: Model JWST COSMOS-Web Ring F150W imaging, including lens-light subtraction and a pixelized source reconstruction, in approximately five minutes.
- Interferometry: Model a real ALMA strong-lensing dataset containing more than one million interferometer visibilities in approximately five minutes.
- Point-source lensing: Model a real multiply imaged quasar or supernova using point-source observables, including image positions and, where available, time delays or flux information, in under five minutes.
- Group-scale strong lensing: Model a real group-scale lens containing multiple deflecting galaxies in under five minutes, demonstrating that PyAutoLens-JAX is not restricted to isolated galaxy-scale lenses.
- Cluster-scale strong lensing: Model a real cluster lens with multiple mass components, multiple images, and potentially multiple source planes in under five minutes.
- Weak lensing: Fit a weak-lensing shear catalogue using a differentiable JAX likelihood in under five minutes, demonstrating that PyAutoLens-JAX is not restricted to strong-lensing data.

Joint and multi-dataset benchmarks (different datasets, lensing regimes, and physical scales combined in a single differentiable, GPU-accelerated probabilistic model):

- Multi-band imaging: Jointly model the four available JWST COSMOS-Web Ring bands, constraining a common lens mass model while fitting the wavelength-dependent lens and source emission in each dataset.
- Joint strong and weak lensing: Constrain a single group- or cluster-scale mass model using both strong-lensing and weak-lensing observables.
- Imaging and point-source lensing: Jointly model extended arcs and point-source constraints from a lensed quasar or supernova within the same lens model.
- Imaging and interferometry: Jointly fit optical or infrared imaging and radio or submillimetre interferometer visibilities, constraining a common mass model using complementary observations of the lensed source.

Pairing requirement: pair each benchmark to the start_here.py file in each autolens_workspace package. For example the JWST COSMOS-Web Ring F150W example, which is made fast, is paired to autolens_workspace/scripts/imaging/start_here.py. All 6 single-dataset start_here.py examples should use real data, and each JOSS example should use the same real data.

The four multi examples pair to examples in autolens_workspace/scripts/multi or scripts/weak/features/strong_lensing. A new multi script will likely be needed for the imaging + point-source lensing joint-modelling benchmark.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b23fc486-a111-4a87-a6c8-b4ca86dd0749/scratchpad/intake_autolens_jax_joss.md -->
