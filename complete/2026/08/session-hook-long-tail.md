## session-hook-long-tail (SessionStart hook: manifest exclusions, a visible denominator, and push-triggered propagation to the 30-repo long tail)
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/369
- completed: 2026-08-29
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/372
- prompt: draft/maintenance/organs/session_hook_reaches_only_four_of_thirty_four_repos.md (bundle `mind-workflow`)
- summary: `repos_sync.py --write` generates the canonical SessionStart hook into every checked-out manifest repo (34), but the only CI leg that drift-checks it (`firewall_gate.yml`) holds the four organs and skips absent repos by design, so two canonical-hook edits (2026-08-26/27) re-staled the other thirty with nothing seeing it. By the time this task issued, the thirty had been regenerated and pushed by hand (2026-08-28) — the symptom was gone and the live scope was the decision record plus a mechanism. Decisions: non-organ repos keep the hook (a library or workspace opened alone in a web session needs 3.12 like an organ); `euclid_assistant` and `admin_jammy` are manifest exclusions via a new `session_hook: false` key (personal namespace, categories already excluded from the org-wide sweeps, never had a `.claude/`). The hook leg now prints its denominator — `OK (34 of 35 checked out, 2 excluded)` — so a four-repo session can see it is seeing four. `policy/session_start_hook.sh` joined `firewall_gate.yml`'s path filter (an edit to the hook did not trigger the gate at all). New `session_hook_propagate.yml`: on push to `main` touching the hook or the generator, derives the in-scope repos from `repos.yaml`, shallow-clones each with `PAT_PYAUTOLABS`, calls `write_session_hooks` over that tree and pushes a `github-actions[bot]` commit of the two hook files where they changed; `dry_run` dispatch input; an ignored `.claude/` is reported failed, not "current"; a generator crash fails the job.
- validation: 10 new tests in `tests/test_session_hook_sync.py` (exclusion, denominator, mismatch+denominator, workflow names); suite 291 → 296 after merging main; full `repos_sync.py --check` clean on the canonical workspace; propagation step exercised against three local throwaway origins (push / already-current / dry-run / ignored-.claude paths).

## Traps and findings
- **A generated file that is untracked passes a `git ls-files` contract test locally and fails it on the PR.** The spawn-template test `test_no_tracked_file_is_unmatched_by_mind_rules` went red only in CI because the new workflow was `??` when the local suite ran. Any new tracked file under `.github/` needs a `MIND_RULES` decision — run the suite after `git add`, not before. Corrective commit classified it DROP (rule 9c: `PAT_PYAUTOLABS` + cross-repo pushes).
- **`set -e` off + a crashing generator = a green run that propagated nothing.** In the propagation step every clone must survive a sibling's failure, so `set -e` is off; without an explicit exit-status check on the generator, a crash left every clone untouched and the loop reported all of them "already current". Found in simulation, not in production.
- `repos_sync.py --write --root <task worktree>` is not a scoping mechanism — through `worktree_create`'s symlinks it regenerates into the canonical checkouts (record `organ-remote-block-and-uv-hook-repair`). The workflow calls `write_session_hooks` directly over a clone tree for the same reason the CLI is wrong there: the full `--write` would also rewrite AGENTS.md blocks, run every drift leg on a half-workspace, and print credentialed remotes.
- The untracked `euclid_assistant/.claude/` residue of an earlier `--write` had been masking that the repo never carried a hook; removing it made the exclusion decision visible rather than implicit.
- The propagation trigger is event-driven (push to the hook / generator), not a weekly cron: the copies only go stale when those files change, and a weekly sweep would spend 30 clones a week finding nothing. First live run after merge: `gh workflow run session_hook_propagate.yml -f dry_run=true`, read the step summary.

## Original prompt

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
