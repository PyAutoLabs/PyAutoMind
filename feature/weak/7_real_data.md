# Weak lensing real data example on Abell 2744. Reproduce a

Type: feature
Target: weak
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Weak lensing real data example on Abell 2744. Reproduce a not-too-complex published cluster weak-lensing analysis end to end on a public shear catalog, as the first PyAutoLens weak-lensing result on real data. Target: Abell 2744 (HST Frontier Fields cluster) — public catalogs include the Medezinski et al. 2016 Subaru/Suprime-Cam analysis (arXiv:1507.03992) and the JWST UNCOVER pyRRG-JWST shear catalog; pick whichever is cleanest to obtain and document provenance. Requires: (1) a WeakDataset catalog loader (from_fits / from_csv: positions, e1/e2, weights, optional source redshifts); (2) reduced shear support — real catalogs measure g = gamma/(1-kappa), not shear, so FitWeak/simulator need a reduced-shear mode, plus sigma_crit / lensing-efficiency scaling for a source redshift distribution; (3) an autolens_workspace/scripts/weak/real_data example fitting an NFW (or NFW+substructures) mass model and reproducing the published tangential shear profile and mass within errors (Oguri 2012 SGAS-style analysis). Depends on AnalysisWeak from feature/weak/4_modeling.md.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
