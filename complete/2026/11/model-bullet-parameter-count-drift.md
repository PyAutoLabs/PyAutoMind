Docs task (queue #11), run in-session on 2026-11-16 alongside cluster-regime-narrative after the human authorized the coordination on autolens_workspace#672. Shipped as autolens_workspace#675, merged to main as 6da5e25f on `ci-verdict` GREEN (8/8). The merge API returned a 502 and left the PR showing open, so the lead closed it by hand. Issue autolens_workspace#672.

**Fixed:** four `__Model__` docstrings now name the profiles each script composes and the true `prior_count`:
- guides chaining: N=9;
- mass_stellar_dark chaining: N=6 then N=14, with `NFWSph` → `NFW`, and the summary says `model_2` does not fit the source;
- point_source start_here: N=5.

The notebooks were regenerated.

**Witness:** the counts parser went from 6 mismatches to 0. All four scripts smoke-ran with exit 0. The independent review found two issues; both were fixed and re-run.

**Open (human, on #672):** `model_2` in `mass_stellar_dark/chaining.py` omits the source, so most of its 14 parameters are unconstrained. This is a likely code bug. The older "priors from search 1" text there is also inaccurate.

## Original prompt

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
Verified: 2026-11-14 c2c8b256 (autolens_workspace)
Lane: any
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
