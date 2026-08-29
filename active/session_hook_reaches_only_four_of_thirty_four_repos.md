# The SessionStart hook is generated into 34 repos and current in 4

Type: maintenance
Target: organs
Repos:
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-29

`repos_sync.py --write` installs `.claude/hooks/session-start.sh` into **every**
checked-out repo in the manifest, not just the organs — `write_session_hooks`
iterates `repos`, and 34 repos carry a copy today. Two regeneration waves in a
row (2026-08-26 and 2026-08-27) were run from sessions that could attach only
the organs, so 30 of those copies are a hook-pass behind, and two repos carry
none at all.

Measured on a full local workspace, 2026-08-27, before any edit:

```
check session-start hooks (generated): 34 mismatch(es)
  ✗ 30 × '<repo>': .claude/hooks/session-start.sh differs from policy/session_start_hook.sh
  ✗ 'euclid_assistant': no .claude/hooks/session-start.sh, no .claude/settings.json
  ✗ 'admin_jammy':      no .claude/hooks/session-start.sh, no .claude/settings.json
```

The stale 30 are every library (@PyAutoFit, @PyAutoArray, @PyAutoGalaxy,
@PyAutoLens, @PyAutoCTI, @PyAutoReduce, @PyAutoNerves), every workspace and
`_test` / `_developer` workspace, the three HowTo repos, the four `*_assistant`
repos, @PyAutoMemory, @PyAutoGut, @PyAutoScientist, `pyautolabs.github.io` and
`euclid_strong_lens_modeling_pipeline`.

## Why no gate sees it

`PyAutoMind/.github/workflows/firewall_gate.yml` is the only CI leg that runs
the full drift check, and it checks out exactly PyAutoMind + PyAutoBrain +
PyAutoHeart + PyAutoHands. Absent repos are skipped by design (so a partial or
web checkout runs clean), which means the other 30 are invisible to it. The
organ repos' own PR gates run `--only "tenant firewall (organ code)"` and never
touch this leg. So the only place this is visible is a full local-workspace
`--check` — and the sessions doing the regenerating have been remote ones that
hold four repos.

That is the same failure the four-organ pass paid for (PyAutoMind#360): a drift
check is only as strong as the number of repos the session running it can see.
This one is a rung wider — the *check* is right, the *rollout surface* is 8x
the set anyone has been regenerating.

## Questions this needs answered, not assumed

- **Do the non-organ repos want the hook at all?** It exists to make a remote
  session run Python 3.12. A library repo opened alone in a web session has the
  same need, so probably yes — but that is a decision, and if the answer is no
  for some class of repo, the fix is an opt-out in the manifest rather than 30
  regenerations forever.
- **`admin_jammy` and `euclid_assistant` have no `.claude/` and no hook.**
  `admin_jammy` has no `AGENTS.md` either and is local tooling under a personal
  namespace; `euclid_assistant` has an `AGENTS.md` but no `.claude/`. Decide
  whether they are in scope or manifest-level exclusions.
- **How does this not recur?** A regeneration wave run from a four-repo session
  will re-stale the other 30 the next time the canonical hook changes. Either
  the check has to report the gap somewhere a four-repo session can see it, or
  a scheduled full-workspace job has to own the propagation (compare
  `spawn_drift.yml`, which runs weekly with no `paths:` filter for exactly this
  reason).

## Done when

- The decision above is recorded, and every in-scope repo carries a
  byte-current hook.
- `repos_sync.py --check` on a full local workspace is clean, or every
  remaining exception is a recorded manifest exclusion rather than drift.
- A named mechanism stops the next canonical hook change from silently
  re-staling the long tail.
