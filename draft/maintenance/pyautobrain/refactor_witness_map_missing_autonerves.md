# Refactor Agent witness map lacks PyAutoNerves test suite

Type: maintenance
Target: pyautobrain
Repos:
- @PyAutoBrain
Difficulty: low
Autonomy: safe
Priority: low
Status: draft
Filed: 2026-08-19 (backfilled from git)

## Finding (2026-08-19, lazy-heavy-imports RefactorDecision)

`pyauto-brain refactor` reported `[unwitnessed: pyautonerves]` and advised
"strengthen tests first", but PyAutoNerves has a real suite
(`test_autonerves`, 157 tests, verified jax-less in the JAX-default arc).
The witness map only knows autoarray/autofit.

## Task

Add PyAutoNerves (`PyAutoNerves/test_autonerves`) — and audit the other
organ/library repos — to the Refactor Agent's witness map so refactor
decisions stop flagging witnessed repos as unwitnessed.
