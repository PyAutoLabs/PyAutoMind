# Fix subhalo detect example false detections…

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- workspaces
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: in subhalo/detect/start_here.py the no-subhalo evidence comes from a search fit under the same positions likelihood as the subhalo searches, and subhalo_refine fixes redshift_source like subhalo_grid_search
Review-minutes: 3
Unattended: ready
Lane: local-dev

Fix subhalo detect example false detections (external bug report, Rishabh Ramteke, by email 2026-11-20)

Type: bug
Target: autolens_workspace
Difficulty: medium
Lane: local-dev
Witness: in subhalo/detect/start_here.py the no-subhalo evidence comes from a search fit under the same positions likelihood as the subhalo searches, and subhalo_refine fixes redshift_source like subhalo_grid_search

autolens_workspace scripts/imaging/features/advanced/subhalo/detect/start_here.py (release 2026.9.8.1) has two bugs:

1. The no-subhalo evidence is taken from the wrong search. The docstring (lines 46-47) says the model is refit without a subhalo to get the no-subhalo evidence, but the code uses evidence_no_subhalo = mass_result.samples.log_evidence (line 843). mass_total is fit under the source pipeline's positions likelihood (line 435), while the subhalo searches use mass_result.positions_likelihood_from(factor=3.0, minimum_threshold=0.2) (lines 515, 600). So Delta ln Z compares two different likelihoods, and a change of positions alone can produce a "detection". Fix: refit the no-subhalo model under the same positions likelihood as the subhalo searches (as the docstring says) and use that evidence.

2. subhalo_refine does not fix the subhalo's redshift_source (only redshift_object, line 611), unlike subhalo_grid_search (line 531). It stays on its U(0, 1) prior, so the refine search can fit a subhalo that barely lenses. Fix: fix redshift_source as in the grid search.

Together they give a false detection on a lens with no subhalo: Delta ln Z = 31.6 for a subhalo with redshift_source = 0.04 and deflection under 0.01". The same refine model refit without the subhalo, under the same positions likelihood, gives Delta ln Z = -0.4.

Check sibling subhalo detect scripts (interferometer, other workspaces, SLaM pipelines) for the same two patterns. Credit the reporter; James will reply by email thanking them.

<!-- formalised by the Intake (Conception) Agent on 2026-11-24 from file:/tmp/claude-1000/-home-jammy-Professional/4e2bfaad-3e60-423a-8f17-3c5bd8710da6/scratchpad/o8.txt -->
