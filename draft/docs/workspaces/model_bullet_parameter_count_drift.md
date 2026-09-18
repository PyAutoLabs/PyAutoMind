# autolens_workspace: `__Model__` bullets whose profiles or parameter counts do not match the code

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- notebooks
Difficulty: small
Autonomy: safe
Priority: low
Consequence: notify
Witness: a script that parses each `__Model__` docstring's "[N parameters]" / "N=…" bullets and compares them with `af.Model(...).prior_count` of the models the script composes reports no mismatch for the files below; the four named sites read true.
Review-minutes: 2
Unattended: ready
Filed: 2026-09-18

Found while sweeping every script for the MassField migration (autolens_workspace#559),
left untouched there because fixing them means rewriting parameter counts, which that
sweep promised not to do:

- `scripts/guides/modeling/chaining.py:126` — bullet claimed "`Isothermal` with
  `ExternalShear` [7 parameters]" while the code composes `Isothermal` only; the
  stale shear mention was removed in #559 but "[7 parameters]" and the "N=14" total
  do not match 5 + 4 either.
- `scripts/imaging/features/advanced/mass_stellar_dark/chaining.py:191` — "The lens
  mass model also includes an `ExternalShear` [2 parameters]" but neither `model_1`
  nor `model_2` has a shear, and `model_2`'s `af.Collection` omits the source, so the
  stated N=22 is wrong too.
- `scripts/imaging/features/multi_gaussian_expansion/{fit,simulator}.py`,
  `scripts/point_source/features/multiple_sources/simulator.py`,
  `scripts/point_source/start_here.py:197` — claimed a shear that no code composed;
  #559 reworded these to the truth, but their counts were not re-derived.
- `autolens_workspace_test/scripts/{imaging/{convolution,model_fit},imaging/simulator/{no_lens_light,with_lens_light},interferometer/model_fit,interferometer/simulator/{no_lens_light,with_lens_light}}.py`
  — docstrings claim an `Isothermal` and `ExternalShear` model but contain no shear.

Fix each bullet to name the profiles the code composes and the true `prior_count`;
consider a small checker (docstring count vs `prior_count`) the smoke runner could
assert, so the drift cannot recur.
