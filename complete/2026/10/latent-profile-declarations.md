# Profile latent declarations — Galaxy #656

Completed: 2026-10-26
Tracking issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/669 (closed)
PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/656 (merged)
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/656

## Outcome and authority

Human approved completing the existing contributor PR and merging on green. Normal merge preserved contributor history; reviewed head `6c0fac8f0d6a215ca705383767d0597061d1ee11` merged as `e92eea86a8b2a8345b0d0135876df634d05a7865` at 11:39:42 UTC. Git ancestry against origin/main proved the entire claimed branch merged. No release authorized or performed.

Declarations now expose elliptical axis ratio/angle, shear magnitude/angle and multipole strengths/phases through PyAutoFit's latent protocol. Completion review fixed the light-profile cosine/sine ordering (the original PR reported incorrect phases), split m3/m4 declarations so fixing one mode does not suppress the other, restored ExternalShear/PowerLawMultipole class docstrings, preserved notation comments and new labels, and raised autofit>=2026.10.23.1 to require the verified protocol release. Shared PowerLaw/multipole ellipticity retains one conversion under its canonical owner path.

## Validation

- Galaxy full suite: 1,383 passed, 49 warnings. Focused conversion suite:23 passed.
- Downstream Lens full suite:952 passed,1 existing xfail,44 warnings.
- Heart smoke:172 individual passes,0 failures/skips in11 complete reports: Fit10,Galaxy16,Lens44,Lens regression37,Euclid9,HowToLens50,CTI3,CTI regression3.
- An initial isolated-root setup omitted the Hands link; corrected before scripts ran. Parallel environment preparation collided in shared wheel build directories; rerun sequentially successfully, with no source changes. The long-running outer shell returned143 after all reports were complete; every individual result was checked, and the final CTI regression workspace rerun passed with exit0. These setup/exit anomalies are not represented as clean aggregate command exits.
- Configuration-comment checker:0 uncommented leaves.
- Independent review CLEAN. Verified six actual Sersic/Gaussian light Models (m3-only,m4-only,both), scaled ellipse k=.1/phase12°, both shared mass/multipole insertion orders, original class docstrings and dependency metadata. Physical Fourier reconstruction at37 independent angles agreed with the profile convention.
- Actual synthetic output witness:Analysis latent_samples_from processed400 shear samples, Samples.write_table preserved original angles in CSV, and corner_anesthetic(latent=True) rendered a continuous posterior. Raw angle span179.9798°, plotting span12.1076°. Synthetic correctness evidence, not a science fit.
- Review claim dispositions: branch-cut plotting-only claim verified through actual output/renderer; no unrelated implementation changes verified against full diff; linked ellipse and independent light-mode claims verified by real-model/Fourier witnesses.
- Exact-head CI:all4 jobs across both workflows passed, none skipped: [Tests](https://github.com/PyAutoLabs/PyAutoGalaxy/actions/runs/40316139231) (no-JAX,Python3.12,Python3.13) and [Docs](https://github.com/PyAutoLabs/PyAutoGalaxy/actions/runs/40316139167).
- Fresh Heart at11:33:17 UTC:YELLOW, no RED reasons. Acknowledged warnings: cloud workspace validation autolens scripts/group/slam.py; three manifest-drift entries; old Hands/Mind PRs; no current release rehearsal. Clean canonical library checkouts were fast-forwarded to clear stale-local-main RED reasons. Freeze clear before merge.

## Follow-up and cleanup

The corner-plot workspace task remains active. Its Galaxy implementation dependency is merged; publication and executed latent-output Markdown validation remain. Keep pending-release until the release workflow proves publication; merge is not publication.

Human explicitly approved deleting this task's worktrees and validation outputs (about228MB), while retaining the separate corner worktree. Evidence is retained here and on issue669/PR656; raw synthetic outputs may be regenerated. Glance tier, stage1 independent review (no independent-model adversary), tiered merge action merged-unchanged.

Revert, if needed, from a fresh Galaxy feature branch: `git revert -m 1 e92eea86a8b2a8345b0d0135876df634d05a7865`.

## Original prompt

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
