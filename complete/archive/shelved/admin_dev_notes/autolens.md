[TLC]

- Scientific workflow example with full output customization.
- The png / PIL layer for scaling a workflow up to large samples, this should only interface with the 
  output folder and allow a user to move to dataset at end. Should use Aggregator API (maybe with speed up options) and I 
  should develop with Notebook interface in mind (e.g. splicing pngs to get single or multi notebook plots)
- The result.json layer should mirror the png / PIL layer, and not go straight to the dataset layer, with a careful consideration of samples.csv and latent.csv.

[Interferometer]

- LLM to data prerparation guide.

[Source]

- Magnification tools for source models.
- Mapping image arrays (e.g. the data) to the source plane so we can compare how the source-plane appears.
  Do for simple rectangular grid, then add subgrid, interpolation.
- Make magnification equivalent.


[group]

-SLaM light currently makes extra galaxies free and scaling fixed, do we want more customization?

[JAX gradients]

- Extend integration tests to use jax.grad alongside jax.jit.
- Add to autolens_workspace a guide on jax gradient.
- Implement a few autofit gradient searches, prob those used by heculens or giga lens.

[Mass Profile Test]

- Related to HowToLens new notebnook for chapter 1, produce end-to-end testing of a mass profile via consistency checks.
- Put at high level docs.


[HowToLens]

- The grids tutorial should also introduce what a strong lens is, and use simple images to show how grid are fundamental to lensing.
Its nonsense we h ave to wait until tutorial 4 to discuss what a strong lens is, by bring it to tutorial 1 people will get the point.
This can be the focus and the slim / native stuff a brief aside. Can also explain slim / native. Maybe also show some lensed images?
Really give a clear sense of ray tracing.
- Add equations to lectures from likelihood function noteobok.
- Add dedicated notebook to lensing formalism before summmary in chapter 1.
- Use dictionary API for tracer in later tutorials of chapter 1.
- Move imaging / fitting to chapter 2.
- Flesh out chapter 3 to be Advanced Modeling.

[Documentation]

- update readthedocs configs to point to workspce.
- Add Contents to Results and Database scripts.
- advanced features give a brief summary of what they are and link to worksapce.


[Point Source]

- Copy gravity.jl likelihood functions.
- magnificatgion ^-2 in noise map, following LEnsTool and Jack  discussion (equation 10 https://ui.adsabs.harvard.edu/abs/2007NJPh....9..447J/abstract)
- Test cases of point finding for quad, group, cluster.
- Point solver uses triangles for mapping.
- Add optimizer based approach for solver.
- Add all forms of image and source plane pairing / chi squared.
- Time delays, Flux.
- Point source visusliazation, RMS of point source.
- High level docs.
- Extended source models.
- Include PSF in model fitting of point source.

[Potential Corrections]

- Use Xiaoyue's repository and Claude CLI to implement potential corrections.

[PSF]

- Add delta function example w/ examples.
- Extensive Documnetation.
- Extend documentation.
- Estimating the PSF preprocess example by fitting Gaussians
- Add PSF checks, make docs clear a user should go to (11, 11), but base this value on the flux %. 

[Features]

- Database tutorial for big datasets with efficient / fast visuals.


[Tasks]

- Logging: DISPLAY EVERYTHING (PSF SIZE, IMAGER SIZE, MASK STUFF, IT WILL STOP BUGS).
- Fix plot of SNR light profile which do not output by default.

