# Heart vitals leg: pinned-value drift flags from autolens_profiling

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

autolens_profiling's runtime cells compare each run's log-likelihood/evidence
against pinned baseline values, but (as of phase 2 of the polish series,
autolens_profiling#54) they **record and flag** drift instead of crashing:
every result JSON carries `pinned_expected` and `pinned_drift` (a list of
`{label, expected, got, rel_diff, rtol}` records; empty list = all compared
values matched; `pinned_expected: null` = instrument has no pin). The boundary
rule is written in `autolens_profiling/results/notes/design_lock_in.md`:
profiling records and flags, `autolens_workspace_test` adjudicates library
correctness.

Give PyAutoHeart a vitals leg that closes the loop: scan
`autolens_profiling/results/**/*.json` for non-empty `pinned_drift` fields and
surface them in the readiness verdict (a drifted likelihood is a health
finding — either a library regression or a stale pin, and either way the
profiling baselines are non-comparable until resolved). Report per finding:
cell (path), instrument, label (eager/JIT/vmap/full/cube), expected vs got,
and the PyAutoLens version from the JSON. Probably YELLOW-tier, mirroring how
other stale/failing legs report; follow Heart's existing check conventions
(read PyAutoHeart/AGENTS.md first).

Origin: user request 2026-07-08, in-conversation during phase 2 ("pair it to
PyAutoHeart as something which would get caught and checked in the testing
health stuff there").
