## intake-reconcile
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/52 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/53 (merged)
- notes: |
    Added `intake reconcile` — the fourth backlog mode. Ranks backlog prompts
    that look already-shipped via four Mind-local signals: complete.md path
    references (follow-up wording incl. "next step" downgrades to likely-open),
    duplicate basenames in issued/, token overlap with completed headers, and
    hand-set Status values that formalise preserves verbatim. Always read-only;
    retirement + repo-level verification stay human. Live run: 20 suspects of
    74, incl. candidates the manual audit missed (nnls_gpu_bottleneck,
    jax_substructure/5-6 referenced by a retroactive close-out) — pending a
    human review pass.
