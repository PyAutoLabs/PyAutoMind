## info-exclude-identifier-fields
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1261
- summary:
    `model.info` was rendering `pytree_token N` lines for every
    `LightProfileLinear` (40+ per basis fit in SLaM chaining output) —
    an internal JAX-pytree counter set in `__init__`, declared in
    `__exclude_identifier_fields__` so the unique_id hash already
    ignores it. PyAutoFit's `AbstractPriorModel.info` did not honor
    that contract. Fix walks each leaf's parent and consults
    `type(parent).__exclude_identifier_fields__`; PyAutoGalaxy and
    other libs need no changes. Verified end-to-end via SLaM
    (`PYAUTO_TEST_MODE=3 slam_start_here.py`): unique_id hashes and
    `model.results` byte-identical to baseline, `model.json`
    semantically identical, 120 `pytree_token` lines across 3 fits
    dropped to zero. Also generalises to the existing
    `GridSearch.__exclude_identifier_fields__ = ("number_of_cores",)`.
