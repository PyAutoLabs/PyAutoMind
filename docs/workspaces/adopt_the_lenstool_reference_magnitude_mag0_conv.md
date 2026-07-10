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
3. imaging/features/scaling_relation/ (modeling.py ~L280-294, fit.py ~L226, likelihood_function.py ~L172): the ODD ONE — theta_E = scaling_factor * L**scaling_exponent with scaling_factor~U(0,0.5) AND scaling_exponent~U(0,2) BOTH free and NO reference ratio (raw luminosity). OPEN QUESTION to resolve before editing: is this example deliberately a FREE-exponent teaching case (demonstrating the general fit) that should stay as-is, with only cluster+group re-anchored? Or should it also be made LensTool-like (introduce reference-magnitude ratio + fix exponent 0.5)?

CONSTRAINTS: beta is already fixed at 0.5 in cluster+group and the cluster tier already scales the truncation radius rs~L**0.5 — do NOT regress these (the stale-note trap). Regenerate notebooks after editing scripts. GATE: user is double-checking the physics/convention with Fable first (r_core/dPIE ra scaling? Bergamini kinematic exponents as documented refinement? imaging-example pedagogy?) — do not start_dev until that verdict is in. Files under autolens_workspace/scripts/; notebooks regenerated via PyAutoBuild.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from user-intake -->
