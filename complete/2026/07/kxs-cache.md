## kxs-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/362 (follow-up leg)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/364 (merged)
- notes: |
    Segment-id memoization for the k x s partial pre-bin (design promised a
    cache; phase 2 rebuilt per likelihood evaluation). lru_cache on sizes
    bytes: 62 ms -> 83 us (x750) on a 3000-pixel adaptive mask; read-only
    shared array; suite 867 unchanged. Calibration: merged-unchanged.
