# SersicCoreSph has no mass_to_light_ratio argument

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: Either `SersicCoreSph.__init__` accepts `mass_to_light_ratio`, the `sersic_core.yaml` prior block is restored and a test shows its deflections scale linearly with it, or the class docstring states it is intensity-scaled by design and the config-priors walker test stays green.
Review-minutes: 3
Unattended: ready

SersicCoreSph stellar mass profile has no mass_to_light_ratio argument. Found by the config-priors-drift walker test (PyAutoGalaxy#618 / PR #619): `autogalaxy/config/priors/mass/stellar/sersic_core.yaml` carried a `SersicCoreSph.mass_to_light_ratio` prior block that was silently dead because `SersicCoreSph.__init__` only accepts `alpha, centre, effective_radius, gamma, intensity, radius_break, sersic_index`. Its elliptical sibling `SersicCore` in the same module does take `mass_to_light_ratio`. Decide whether the spherical stellar profile is missing the argument (bug: the mass profile cannot be scaled by M/L) or whether the class is deliberately intensity-scaled, and either add the argument + restore the prior block or document why not. The dead prior block was removed in PR #619; restore it if the argument is added.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->

Issued: 2026-10-25

## Execution 2026-10-25
User authorized selecting and implementing four related tasks. Scope: Restore SersicCoreSph mass-to-light ratio. Separate branch and PR; no merge authorization. Related group executes serially with non-overlapping source edits.

## Implementation evidence (2026-10-25)

- Library PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/664 at `0fee6daf0e299539d43bdfa185200b76436ef2a3`; published Git tree equals the tested local tree.
- Full library suite: `python3 -m pytest -q -n auto test_autogalaxy`, 1360 passed, 6 skipped; Python 3.12, released 2026.10.25.1 dependencies.
- Log: `/workspace/scratch/e0d55f00a4c5/evidence/sersic-core-sph-ml-suite.log`.
- Heart readiness GREEN, score 100, no reasons; evidence timestamp 2026-10-25T20:54:46Z.
- GitHub Tests and Docs for the exact PR head were running at the final check; no CI success or merge claimed.
- Merge mode: human `/prm`; no merge, close-out or release authorized/performed.
- Appended optional mass_to_light_ratio=1.0 preserves positional/default calls; af.Model gains restored LogUniform prior. Tests cover zero, fractional and doubled convergence/deflections. MGE deflections use 1e-6 relative tolerance (observed fractional-rounding error 3.3e-8), analytic convergence 1e-12. Downstream PyAutoLens Tracer compatibility smoke passed.
