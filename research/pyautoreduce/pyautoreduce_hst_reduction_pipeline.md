# PyAutoReduce: new HST data-reduction project for lens modeling

Type: research
Target: PyAutoReduce (new repo)
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

I want to make a new project, PyAutoData (but feel free to suggest better names), which performs all data reductions required for PyAutoLens modeling (and also PyAutoGalaxy). First, the focus will be on HST data reduction, making images comparable to the data I am used to modeling (e.g. /mnt/c/Users/Jammy/Science/subhalo/dataset/slacs). It should therefore drizzle the individual exposures to a common mosaic, do PSF estimation, have an RMS noise map including Poisson counts. Future work will include reducing other HST data (e.g. other wavelengths, WFC3), JWST data and other instruments, and producing individual frames for modeling (e.g. _flt images with cosmic rays). My understanding is you will have to download large HST tiles, but ultimately we only need cut-outs of each strong lens, so the project should have tools which exploit this to avoid too much hard disk space being used to store lots of tiles where possible. Read some strong lensing literature to work out how HST data reduction is performed; this github repo may give guidance albeit I think their reduction pipeline is not as high quality as SLACS (https://github.com/ajshajib/hst-lens) and it may also not do ACS. Do deep research in planning this, make a thorough plan for the HST steps and then a follow-up which we will flesh out later to do JWST (and other instruments). Where possible, we should stick to the default data reduction pipeline of each instrument and only add changes or deviations or customizations when required for specific lensing calculations. You will also benefit from trying to find science publications on weak lensing or AGN modeling which describe detailed PSF modeling.

## Intake notes (2026-07-08)

- **Name decided:** PyAutoReduce (user confirmed 2026-07-08; original prose above says "PyAutoData" — superseded).
- **New repo** — no existing PyAuto* repo is the target; creating the repo is part of the work. Once named, add it to `PyAutoMind/repos.yaml` and run `repos_sync.py --write`.
- **Phase 1 (this prompt):** deep research + thorough plan for HST/ACS reduction matching SLACS-quality data products (drizzled mosaic, PSF estimate, RMS noise map with Poisson counts), plus tile-download/cut-out strategy to limit disk use. Reference dataset: `/mnt/c/Users/Jammy/Science/subhalo/dataset/slacs`.
- **Phase 2 (skeleton only for now, fleshed out later):** WFC3 / other HST wavelengths, JWST, other instruments, per-exposure `_flt` frames with cosmic rays.
- **Design principle:** stick to each instrument's default reduction pipeline (e.g. STScI drizzlepac/calacs); deviate only where lensing calculations require it.
- **Research inputs:** strong-lensing literature on HST reduction (SLACS as the quality bar); https://github.com/ajshajib/hst-lens as guidance (lower quality than SLACS, possibly no ACS); weak-lensing / AGN-modeling publications for detailed PSF modeling practice.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/be7cb926-7874-4cc2-8c05-64c9644a64d9/scratchpad/intake_pyautodata.md -->
