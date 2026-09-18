# linear_operated Sersic has no prior yaml file

Type: maintenance
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Witness: Either `config/priors/light/linear_operated/sersic.yaml` exists mirroring `linear/sersic.yaml`, or the folder README states the MRO fallback is intended; in both cases `test_autogalaxy/test_priors_config.py` encodes the chosen rule and passes.
Review-minutes: 3
Unattended: ready

light/linear_operated has a sersic.py but no sersic.yaml prior file. Found by the config-priors-drift sweep (PyAutoGalaxy#618): `autogalaxy/profiles/light/linear_operated/sersic.py` exists, but `autogalaxy/config/priors/light/linear_operated/` only ships `gaussian.yaml`, so a linear-operated Sersic model resolves its priors through the MRO fallback to the standard `light/linear/sersic.yaml`. Decide whether that fallback is the intended behaviour (then say so in the folder README) or add a `linear_operated/sersic.yaml` mirroring `linear/sersic.yaml`. Extend the new `test_autogalaxy/test_priors_config.py` walker if a "every profile module has a prior file" rule is wanted.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->
