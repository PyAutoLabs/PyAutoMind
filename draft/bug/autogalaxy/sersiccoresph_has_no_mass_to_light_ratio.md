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
