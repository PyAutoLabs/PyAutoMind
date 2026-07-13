## csv-api-lenstool
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/490 (closed)
- completed: 2026-07-09
- prs: PyAutoGalaxy#491 + autolens_workspace#252 (merged, stacked on #250)
- notes: CSV API stress-tested against user requirements (harness → 12 unit tests): .par-style
  dPIEMassLenstool rows, NFW redshift args, shear+PowerLaw sparse, multipoles, PointFlux,
  flux/time-delay data columns all passed as-is. Five gaps fixed: light-variant qualified class
  names (linear.Sersic); loud typo-column guard (silent default was the worst footgun); loud
  duplicate-row guard; GalaxyTable.properties (floats/strings, nothing dropped); dPIEMassLenstool
  H0/Om0 flat args (a run's cosmology is now CSV-able — the gap measured at 0.3% in b0).
  Lenstool example ported: mass.csv = the .par file as a table (149 rows, header is the .par
  vocabulary), one al.galaxies_from_csv_tables call reconstructs at identical 0.0680" parity;
  refit halos originate from galaxy_af_models_from_csv_tables with input.par priors promoted.
