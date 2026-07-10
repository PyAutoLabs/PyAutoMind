# Adopt the LensTool reference-magnitude (mag0) convention for the scaling-relation tier

Type: docs
Target: workspaces
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Adopt the LensTool reference-magnitude (mag0) convention for the scaling-relation tier across the autolens_workspace examples, replacing the non-standard max(sample-luminosity) anchor. Referee point (Limousin 2005/2007, Eliasdottir 2007, Bergamini 2019): the scaling-relation normalization should be anchored to a FIXED reference magnitude / reference luminosity (LensTool's mag0, conventionally the BCG magnitude), NOT the max luminosity of the scaling sample; the exponent should be FIXED (Faber-Jackson / fundamental plane), not fitted. DECISION (user-selected): use an explicit fixed reference-luminosity/magnitude CONSTANT documented as settable to the BCG (a fiducial L* where no BCG photometry exists), so einstein_radius_ref/b0_ref = the Einstein radius / lens strength of a galaxy at the reference magnitude. This is a strict reparameterization (alpha_new = alpha_old*(L_ref_new/L_ref_old)**exponent), so simulated member physics MUST stay identical and priors must still bracket the reparameterized truth.

THREE example families are affected (verified by grep on current main):
1. cluster/ (modeling.py ~L373-390, start_here.py ~L300-302, likelihood_function.py ~L150, simulator.py ~L332-333): dPIE; b0 = b0_ref*(L/L_ref)**0.5; exponent ALREADY fixed 0.5; rs ALREADY scaled ~L**0.5. ONLY change the anchor (max -> explicit reference) + docstrings. DO NOT re-free the exponent or touch rs scaling. Note the fixed rs_ref may need a numeric rescale to keep member rs identical under the new anchor.
2. group/features/scaling_relation/ (modeling.py ~L262-280, fit.py ~L237-238, likelihood_function.py ~L166-167, simulator.py): Isothermal (no truncation radius); theta_E = theta_E_ref*(L/L_ref)**0.5; exponent ALREADY fixed 0.5. ONLY change the anchor + docstrings. Group BCG has NO photometry in the dataset (centre only) -> use a documented fiducial L*.
3. imaging/features/scaling_relation/ (modeling.py ~L280-294, fit.py ~L226, likelihood_function.py ~L172, simulator.py hardcodes the truth via einstein_radius=0.3*L**1.0): the ODD ONE — theta_E = scaling_factor * L**scaling_exponent with scaling_factor~U(0,0.5) AND scaling_exponent~U(0,2) BOTH free and NO reference ratio (raw luminosity). OPEN QUESTION to resolve before editing: is this example deliberately a FREE-exponent teaching case (demonstrating the general fit) that should stay as-is, with only cluster+group re-anchored? Or should it also be made LensTool-like (introduce reference-magnitude ratio + fix exponent 0.5)?

4. **SLaM pipelines (VERIFIED inventory miss — added after adversarial grep; ChatGPT flagged, Claude confirmed against the tree):** group/slam.py (TWO sites: L314/330 and L791/807) and group/features/linear_light_profiles/slam.py (TWO sites: L261/276 and L724/739). All four use the OLD form: scaling_factor~U(0,0.5) * total_luminosity**scaling_relation with scaling_relation~U(0,2.0) (FREE exponent, raw luminosity, no reference ratio) — i.e. exactly the referee-objected parameterization, in PRODUCTION SLaM pipelines that users actually run. These were missed by the original prompt. Recommendation: re-anchor these to the standard fixed-0.5 reference-magnitude convention regardless of how the imaging-toy pedagogy question resolves (SLaM is production, not a teaching demo). Note each file has the pattern at TWO source-lp stages.

VERIFIED FALSE POSITIVES (do NOT touch): guides/advanced/multi_plane.py:201 — `scaling_factor` there is `cosmology.scaling_factor_between_redshifts_from` (a cosmological scale factor, pure name collision). group/modeling.py, group/features/multi_gaussian_expansion/modeling.py, imaging|interferometer/features/extra_galaxies/modeling.py, cluster/csv_api.py, modeling_for_luminosities.py — all docstring cross-references only, no instantiation.

REPARAMETERIZATION MATH (correct form — ChatGPT's numbers are right but its symbolic formula is written backwards): to keep simulated member physics identical when L_ref changes, p_ref_new = p_ref_old * (L_ref_new / L_ref_old)**0.5 (the ref value INCREASES when the fiducial L* > old max). Worked truths for fiducial L*=1.0: group theta_E_ref 0.135 -> 0.201; cluster b0_ref 0.12 -> 0.190, rs_ref 10.0 -> 15.8. TRAP: make the SIMULATOR and MODEL share the SAME explicit reference luminosity so members stay consistent by construction — otherwise the cluster's fixed rs values mismatch (simulator on max=0.4 vs model on L*=1.0).

CONSTRAINTS: beta is already fixed at 0.5 in cluster+group and the cluster tier already scales the truncation radius rs~L**0.5 — do NOT regress these (the stale-note trap). Regenerate notebooks after editing scripts.

RESOLVED DECISIONS (user, 2026-07-10): (a) dPIE core radius `ra` — SCALE it ra~L**0.5 for full LensTool PIEMD fidelity (add ra_ref; scale like rs; update the cluster simulator truth for ra too). (b) Imaging toy AND SLaM — RE-ANCHOR both to the standard fixed-0.5 reference-magnitude convention (one convention everywhere; no free-exponent variant retained). (c) Bergamini kinematic exponents (sigma~L^0.27) — mention in docs as the "when kinematics exist" refinement, not the default. Net scope: uniform LensTool reference-magnitude convention with fixed exponent 0.5 and full r_core/r_cut/b0 luminosity scaling across ALL sites — 3 feature families (cluster, group/scaling_relation, imaging/scaling_relation) + 2 SLaM pipelines (group/slam.py, group/features/linear_light_profiles/slam.py; 4 sites) + their simulators/fit/likelihood + regenerated notebooks.

GATE: user reviewed convention with ChatGPT (Fable usage exhausted); adversarial verification done; decisions resolved. Ready for /start_dev. Files under autolens_workspace/scripts/; notebooks regenerated via PyAutoBuild.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from user-intake -->
