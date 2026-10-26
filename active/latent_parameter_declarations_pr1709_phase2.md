# PyAutoGalaxy latent-parameter declarations (phase 2 of community PR PyAutoFit#1709)

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: library-dev
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/669
Consequence: glance
Release-evidence: PyAutoFit 2026.10.23.1 is published/non-yanked and contains #1709; prerequisite cleared (verified in this session).
Existing-PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/656
Filed: 2026-10-21

Remainder of `complete/2026/10/finish-pr-1709-corner-plots.md`. PyAutoFit#1709 (merged 2026-10-21) added
`latent_parameters` class declarations, `af.Periodic`, path superscripts and the latent corner plot. The
contributor (@samlange04, proposal PyAutoLabs/.github#38) will open the PyAutoGalaxy PR declaring the
conversions after release. Their `feature/latent-parameters` branch was not public on 2026-10-21.

- Declare the conversions on PyAutoGalaxy components: external shear `(gamma_1, gamma_2)` → magnitude + angle;
  elliptical `ell_comps` → axis_ratio + angle (`Periodic` 180); multipoles → strength + phase (`Periodic` 360/m).
- Linked ellipticity (a power law's `ell_comps` shared into its multipoles) must keep the mass's latents. PyAutoFit
  now converts shared priors for every holder; add a PyAutoGalaxy test with real `PowerLaw` + multipole.
- Update the `notation.yaml` `superscript:` block comments. It now applies only to a bare unnamed `Model`.
- Review the contributor's PR rather than authoring it, unless they ask us to take it over.


## Completion review — 2026-10-26

User request (verbatim): "whats the issue with 656 can we finish it too?"

The historical note above predates the contributor PR: it is now public on
`samlange04/PyAutoGalaxy`, branch `feature/latent-parameters`, reviewed head
`180bb8fe85fe652b9f9190bdc66b3c4e651a6639`. Reuse this PR and preserve its history.
The original two workflows / four jobs passed on 2026-10-22, but GitHub now
reports CONFLICTING/DIRTY. Read-only merge survey finds a content conflict only
in `autogalaxy/config/notation.yaml`, against the merged explanatory comments.
PyAutoGalaxy canonical checkout is clean on main; no competing library claim.

Verified review findings:
- The task's shared-prior witness (real PowerLaw plus multipole sharing ell_comps)
  is absent from the contributor tests.
- `latent_parameters` precedes the class string in ExternalShear and
  PowerLawMultipole, so those strings cease to be Python class docstrings.
- Scaled and light-profile multipole conversion behavior needs direct coverage,
  beyond the existing class-declaration assertions.

### Approved completion plan

Human approved completion and merge on green on 2026-10-26.

1. Register this existing task via start_dev/create_issue; attach a claimed
   PyAutoGalaxy worktree under `.worktrees/latent-profile-declarations`, using
   the existing contributor branch. No duplicate implementation PR.
2. Merge origin/main normally; resolve notation.yaml preserving the new latent
   labels/gamma subscripts and all explanatory comments. Update the unnamed-Model
   superscript prose as required by the original prompt.
3. Move declarations below the class docstrings in
   `autogalaxy/profiles/mass/sheets/external_shear.py` and
   `autogalaxy/profiles/mass/total/power_law_multipole.py`.
4. Extend `test_autogalaxy/test_convert.py` with a real linked PowerLaw/multipole
   model and scaled/light-multipole conversion witnesses; preserve periodic
   angle semantics (plot recentering only, stored values keep conversion range).
5. Run focused and full Galaxy tests, downstream Heart smoke, independent
   review, and a synthetic latent-output/angle-wrap check. Update the existing
   PR and judge every CI run/job on the new head.
6. Tier: glance. Proposed merge mode: merge on green only after witness,
   review, CI and Heart gates pass. This plan does not authorize a release.
   Carry pending-release into completion state and update the existing corner
   task's dependency; do not imply merging Galaxy publishes it to PyPI.

Witness: new declarations produce the expected latent columns/periods for real
profile models, linked ellipticity retains the mass latent parameters, original
class docstrings remain present, notation comments are complete, and tests plus
synthetic stored-output/plot-recentering checks pass.

The planning Heart feed was YELLOW (Release YELLOW; monitoring RED), 12 hours
old. Obtain current authoritative readiness at shipping; old green PR checks
are not evidence for the updated branch.
