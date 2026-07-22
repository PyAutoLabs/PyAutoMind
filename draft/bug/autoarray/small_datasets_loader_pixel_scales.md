# PYAUTO_SMALL_DATASETS loader keeps uncapped pixel_scales for at-or-below-cap data

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

PYAUTO_SMALL_DATASETS loader keeps uncapped pixel_scales for at-or-below-cap data.

Root cause of the group/slam PriorException (supersedes draft/bug/autolens/group_slam_priorexception_limits.md). The fault is in PyAutoArray, not in any workspace script.

autoarray/util/dataset_util.py cap_array_2d_for_small_datasets handles one case and silently drops the other:
- data LARGER than the 16x16 cap -> crops it AND rebuilds it at SMALL_DATASETS_PIXEL_SCALES (0.6). Correct.
- data already AT-OR-BELOW the cap (because a capped simulator just wrote it at 0.6) -> early-returns, keeping the callers uncapped pixel_scales (0.1). Wrong.

Consequence: the frame is mislabelled 6x (plus/minus 0.8 arcsec instead of plus/minus 4.8 arcsec). Off-centre galaxies fall outside it, their non-negative linear intensity solve correctly returns exactly 0.0, total_luminosity becomes 0, and min(5*0.5*0**0.6, 5.0) collapses a UniformPrior to lower==upper==0.0. The PriorException is four steps downstream of the fault.

FIX (about 4 lines): in the at-or-below-cap branch, when the cap is active, rebuild the Array2D at SMALL_DATASETS_PIXEL_SCALES and return that scale, mirroring what the crop branch already does. Returning a corrected scalar alone is NOT enough: the Array2D is constructed before the call and carries its own geometry. A first prototype that only fixed the scalar still failed. Also update the docstring, which currently documents only the crop case and calls the early return a no-op.

NO workspace script changes are needed. pixel_scales=0.1 is a TRUE statement about the dataset in normal operation and belongs in a tutorial script; the cap silently invalidates it and the loader must correct it.

PROVEN on clean main, standard capped smoke env (PYAUTO_TEST_MODE=2, PYAUTO_SMALL_DATASETS=1), fresh dataset:
- unmodified scripts/group/slam.py + patched loader -> EXIT 0, all six searches ran
- unmodified script, unpatched loader -> PriorException at slam.py:307
- script with pixel_scale hardcoded to 0.6, unpatched loader -> EXIT 0 (confirms the scale, not the science, was the problem)

Evidence the capped data really is 0.6 arcsec/px: the simulated 16x16 image has clumps at (+3.6,+2.4) and (-4.8,-4.8) arcsec under 0.6, matching the declared extra-galaxy centres (3.5,2.5) and (-4.4,-5.0). Under 0.1 they would be at (0.55,0.45) - nowhere near.

Safety of the >=cap-implies-0.6 inference: every committed and generated imaging dataset checked is either cropped-and-relabelled to 0.6 or written by a capped run at 0.6. It is still an inference; a genuinely small real-scale dataset added later would be mislabelled. See the follow-up prompt on simulators recording their own scale.

BEHAVIOUR CHANGE TO VALIDATE: four datasets have committed 15x15 files (double_einstein_ring, mass_stellar_dark, scaling_relation, extra_and_scaling_galaxies). Scripts loading them will now receive 0.6 instead of 0.1. That is a correction (the data genuinely is 0.6) but must be spot-checked.

ALSO IN SCOPE: remove the group/slam NEEDS_FIX line from autolens_workspace/config/build/no_run.yaml, and the dead one from HowToLens/config/build/no_run.yaml (HowToLens has no group/ scripts at all).

VALIDATION PLAN: pytest test_autoarray/ (add an at-or-below-cap test case); clean-dataset and clean-output run of scripts/group/slam.py under the standard capped smoke env expecting exit 0; the four committed-15x15 scripts; one crop-path script to confirm that branch is untouched.

DEAD ENDS ALREADY RULED OUT, do not redo: (1) the 132-vs-35 should_simulate split is NOT drift - commit 0f294fc70 scoped that migration to smoke-tested scripts deliberately, and since dataset/ is gitignored, exists() and should_simulate are equivalent on a clean CI checkout. (2) An FOV-preserving rewrite of the cap is NOT needed for this bug. (3) Flooring or guarding the collapsed prior is wrong - an off-frame profile solving to exactly zero intensity is the correct result of a non-negative solve.

<!-- formalised by the Intake (Conception) Agent on 2026-07-22 from user-intake -->
