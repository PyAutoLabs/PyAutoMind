## multi-shared-state-core-api
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/379 (CLOSED)
- completed: 2026-07-10
- epic: multi_shared_state_examples phase 2/4 (design PyAutoLens#599 D1-D6 + reg amendment)
- library-pr:
  - https://github.com/PyAutoLabs/PyAutoArray/pull/380 (merged f8a32d43b)
  - https://github.com/PyAutoLabs/PyAutoLens/pull/600 (merged 1513236da)
- repos: PyAutoArray, PyAutoLens
- notes: Imaging shared-state consumer under --auto safe (four-leg gate: 896+962+378 tests, six-workspace smoke all green after contention reruns, review CLEAN w/ end-to-end FactorGraph bit-identical parity + compute-once, Heart YELLOW 7-reason set human-acked). Shared object = source-plane mesh geometry ONLY (aa.PreloadsImaging; no H per user amendment, no F/L/mapper — per-exposure PSFs/offsets). TracerToInversion pg-list preload consult; FitImaging preloads threading; pytree no_flatten. Two CRLF diff-inflation traps caught (autoarray __init__.py, autolens test file). Merged + cleaned same day; phase 3 follows.
