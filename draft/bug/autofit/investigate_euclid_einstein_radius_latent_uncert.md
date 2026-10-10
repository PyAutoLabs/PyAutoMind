# Investigate Euclid Einstein-radius latent uncertainty collapse

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- PyAutoMind
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/light-profile-fitting.md
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing

## Original author requests (verbatim)

"yeah do both, can we check this einstein radius error I do worry it might be a bit small which would imply over fitting"
"worth checking if these einstein radii used delaunay source?"
"the model.results file should also have einstein radius values whose errors you can compare to see if there is a latents issue?"
"intake a prompt in PyAutoMind to investigate this"

## Objective and scope

Investigate whether the unusually small effective Einstein-radius uncertainties in
Euclid ECLIPSE-C originate in latent posterior summarisation, numerical radius
calculation, inadequate sampler convergence, or genuinely narrow conditional
posteriors. Primary owner @PyAutoFit; trace the derived quantity into @PyAutoLens
and @PyAutoGalaxy and the Euclid science pipeline as needed. This prompt requests
an investigation and evidence-backed remediation recommendation. Do not assume
overfitting or a latent bug, silently replace effective radii with SIE parameters,
or change paper numbers/fit products. File only now; do not start development.

## Confirmed evidence (2026-10-10)

The paper lives at /mnt/c/users/jammy/science/euclid_dr1/paper. Full audit is in
review/review_responses.md under COMMENTS-P5-C5 and its follow-ups; the paper
change log and tasks.md record this unresolved precision check.

The plot generator plots/figure_einstein_radius_population.py joins
output/inspect/dr1_prelim_grade_ab_run250/lens_mass.csv to
output/catalogue_swg/inspection/consensus_75.csv and selects Success. These are
PRELIMINARY 2990-sample products, not the new full 15070-candidate catalogue.

For 1762 successes, recomputing
100 * (upper_1_sigma - lower_1_sigma) / (2 * median)
for effective_einstein_radius gives median 0.2676552%, with 16th/84th percentiles
0.03074917% / 0.8557021%. No negative or missing intervals. BUT 162/1762 (9.19%)
have exactly identical lower and upper bounds. The corresponding sampled SIE
parameter einstein_radius has no zero-width intervals; across all 1762 its
fractional-error median is 0.48460933%, percentiles 0.12559675% / 1.39948047%.
The two radius definitions differ; covariance can change uncertainties.

The original producer ../euclid/catalogue/scripts/lens_mass.py selects
initial_lens_model/vis_pix and reads latent.effective_einstein_radius. Original
pipeline ../euclid/scripts/initial_lens_model.py specifies Delaunay sources.
All four locally available successful preliminary-fit ZIPs explicitly store a
Delaunay mesh in files/model.json; latent medians AND bounds match the CSV to
absolute tolerance 1e-12. model.results and latent.results agree with their
respective catalogue columns to their four-decimal printed precision:

| Full lens ID | SIE fractional error (%) | Effective latent error (%) |
|---|---:|---:|
| Tile102007899RA0631694872236DECNEG0650584220817 | 0.457660 | 0.047291 |
| Tile102008219RA0727851454839DECNEG0644382776514 | 0.361155 | 0.308000 |
| Tile102008468RA3567390985250DECNEG0647172046261 | 0.910299 | 1.513636 |
| Tile102008848RA0601376380877DECNEG0634605061157 | 0.309273 | 0.241765 |

For the first: model.results radius 0.7215 arcsec, bounds (0.7163,0.7229);
latent.results 0.7061, bounds (0.7054,0.7061). Fractional latent error is about
9.7 times narrower. Differences already exist before catalogue/plot export.
None of these four local fits is one of the 162 collapsed cases.

Original archives are under /mnt/c/users/jammy/science/euclid/output/
dr1_prelim_grade_ab/<lens>/initial_lens_model/vis_pix/<hash>.zip and unpacked
siblings. The four inspected ZIPs have summaries, not raw sample CSVs or sampler
HDF5 checkpoints; the latter must be located/recovered. Searches for the first
and fourth examples report 100005 samples, near a 100000 likelihood-call cap;
the other two report 54840 and 55230. A .completed marker is not proof of sampler
convergence; establish what these counters and stopping criteria actually mean.

## Suspected mechanism — NOT established for historical runs

Current local @PyAutoFit code:
- autofit/non_linear/samples/pdf.py: SamplesPDF.samples_drawn_randomly_via_pdf_from
  uses np.random.choice with posterior-weight probabilities, retaining the
  original Sample objects and their original weights.
- autofit/non_linear/analysis/latent.py: latent_samples_from retains sample.weight.
- SamplesPDF.values_at_sigma uses these weights again in weighted quantiles.
- autofit/non_linear/search/updater.py selects this PDF-draw path.

This appears to apply weights twice after posterior resampling. It can distort
latent quantiles, but its presence in the actual production version has NOT been
verified and it has NOT been shown to explain the collapsed intervals.
Science-tree ../euclid/config/output.yaml currently enables latent_draw_via_pdf
with latent_draw_via_pdf_size = 100. Recover historical config/revisions.

## Required investigation

1. Reproduce the catalogue audit and retain per-object identifiers, bounds,
   zero-width flags and fit provenance. Sample zero-width, very narrow, ordinary,
   and broad intervals; distinguish preliminary and full DR1 datasets.
2. Establish exact historical library versions/configuration and stored search
   metadata. Locate raw posterior samples/checkpoints; document unavailable
   inputs explicitly. Never infer historical execution solely from current code.
3. Test the posterior-resampling/weighting contract with a deterministic known
   distribution or identity latent with unequal weights. Compare all original
   weighted samples, equally weighted posterior-resampled draws, and the existing
   path. Check repeated samples, effective sample size, 100-draw Monte Carlo
   variability, finite-value filtering and summary fallback behaviour. Use
   controlled seeds and convergence with draw count; do not use a universal
   correction factor for the catalogue.
4. Recompute effective radii from real posterior samples when available using
   the original weights exactly once. Compare SIE model.results, latent.results,
   samples_summary.json, latent_summary.json and CSV values for the SAME fit.
   Examine radius definition/covariances and critical-curve numerical precision
   (grid resolution, CPU/JAX paths where applicable) before attributing width
   differences to a statistical bug.
5. Check sampler stopping/convergence and weight concentration in capped searches.
   Separate formal errors conditional on fixed lens light, chosen mass/source
   model and noise/PSF treatment from calibration/systematic uncertainty.
   Small errors alone are not evidence of Delaunay source overfitting.
6. Report root-cause confidence, affected versions/latent quantities (including
   whether magnification/flux summaries share the issue), and bounded remedial
   work. Identify whether corrected post-processing suffices or fits must be
   repeated. Specify any additional coverage/simulation checks needed before
   scientific precision claims can be trusted.

## Deliverable / acceptance

A reproducible diagnostic report with an input/provenance manifest, original vs
recomputed uncertainty comparisons, a minimal synthetic reproducer if a bug is
confirmed, and a clear conclusion for each suspected cause (confirmed, ruled out,
or unresolved with missing evidence). Recommend scoped fixes/regression tests
and a catalogue-recovery plan; do not launch a full-sample rerun or overwrite
published/science products. Any implementation proceeds through normal approved
development workflow. Keep private science data and paper text out of public
issues/PRs; use synthetic examples and minimal approved diagnostics there.

<!-- formalised by the Intake (Conception) Agent on 2026-10-10 from file:tmp/euclid_einstein_uncertainty_intake.md -->
