# `ell_comps` kwargs KeyError in imaging/modeling after API drift (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autogalaxy_workspace
- HowToGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked since 2026-04-10; still parked after the 2026-07-21 census. Same failure in two repos (one
root cause): `KeyError on ('galaxies','galaxy','bulge','ell_comps'...)` kwargs after API drift.

Affected: `autogalaxy_workspace/scripts/imaging/modeling` and the HowToGalaxy copy of the same script.

Decide whether the drift is in the model-composition/kwargs path (PyAutoGalaxy/PyAutoFit) or just a
stale call-site in the scripts — reproduce on clean main first. Fix, then remove the NEEDS_FIX marker
from BOTH repos' config/build/no_run.yaml. If scripts change, regenerate notebooks.
