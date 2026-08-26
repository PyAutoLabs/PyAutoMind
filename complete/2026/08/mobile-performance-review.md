- completed: 2026-08-26
- issue: none — this task began as an environment review in a mobile session, not
  as a filed prompt, so it carries no `active/` entry to fold. Recorded here
  because the work shipped, not because a prompt was closed.
- prs:
  - https://github.com/PyAutoLabs/PyAutoBrain/pull/289 (merged, `640eb27`)
  - https://github.com/PyAutoLabs/PyAutoHeart/pull/184 (merged, `36ba02f`)
  - https://github.com/PyAutoLabs/PyAutoHands/pull/267 (merged, `4d979df`)
  - https://github.com/PyAutoLabs/PyAutoMind/pull/341 (merged, `713e35c`)
- classification-note: four repos, merged in gate order — Brain first (Mind's
  `firewall_gate.yml` pins it to `main`), then Heart and Hands, then Mind.
- classification: bug (organism infrastructure; all four organ repos)
- summary: |
    A review of why recent mobile tasks were slow found five environment
    defects, four of them in this organism's own code. Every one failed
    *silently*: the affected code is written to degrade, so a wrong answer and
    an absent one were indistinguishable. The headline case is the Brain board
    reporting "clear to work" in brightgreen from a process that had not been
    able to query anything.

## The five

1. **The SessionStart hook never fired in a multi-repo session.** Claude Code
   registers project hooks from the session's project directory; a session
   holding several organs clones them side by side *under* that directory, so
   the project directory is their parent — not a repo, no `.claude/`, no hook.
   In exactly the sessions holding the most repos, none of the Python-3.12
   setup ran, and the session used the container's 3.11: one minor below this
   organism's floor and below every CI leg, with mypy and flake8 reading the
   interpreter and judging code against 3.11 rules. This is a local-green/CI-red
   generator, and nothing announced it.

   Fixed by deriving the repo from the hook's own path, self-installing a
   workspace-root fan-out for the next session in the container, and adding
   `scripts/session_bootstrap.sh` as a door anything can knock on — called by
   `bin/pyauto-brain` before every verb, so a `/verb` cannot run in an
   unbootstrapped session.

2. **The workspace root was a hardcoded `$HOME` path.** `agents/_common.sh` plus
   five Python entrypoints. In a remote session `$HOME` is `/root` while the
   checkouts are under `/home/user`, so every consumer resolved into a directory
   that does not exist and reported empty. One resolver each for shell and
   Python now; neither names an absolute path.

3. **`gh` is absent, but 19 skill bodies and 15 scripts drive it.** Added
   `skills/GITHUB_ACCESS.md` (the gh→MCP mapping), pointers from every
   gh-driving page, and `bin/_gh.sh` so a script says what to do instead of
   leaving an empty command substitution to be read as an answer.
   `nightly.sh` — the release driver — had no check at all.

4. **Shallow clones make ancestry checks lie.** `merge-base --is-ancestor`
   reports "not an ancestor" for a commit whose ancestry is merely absent, and
   the ship/close-out procedures act on that answer. Already logged once in
   `complete/2026/08/status-sh-repos-missing-source.md` as an environment note;
   now fixed at the source. Observed here: PyAutoMind had 249 of 4398 commits.

5. **The board answered questions it could not ask.** Rows now distinguish
   *asked, nothing* from *could not ask*; a 403-on-CONNECT is named as an
   egress-policy block rather than a retryable failure; a sibling checkout
   answers when the published copy is blocked; and green is emitted only by a
   render that read everything.

## Key traps

- **The tenant firewall caught the fix doing the disease.** The first draft of
  the resolvers named `~/Code/PyAutoLabs` as a fallback, and
  `repos_sync.py`'s firewall check flagged it — correctly: an instance fact in
  organ code is exactly what caused the bug. The fallback turned out to be
  redundant as well as wrong (on a developer box the organs *are* side by side,
  so deriving from the checkout already covers it), so the allowlist **shrank**
  by seven entries instead of growing by three.

- **A partial board is worse than a short one.** The degraded rows existed
  before this work — at the foot, where a reader who stopped at the headline
  never saw them. The banner, the qualified headline and the grey badge are all
  the same point: absence of findings is not a finding.

- **Proved by the fix landing.** Allowing the Pages host in the environment's
  network policy made the readiness leg live, and it immediately surfaced a
  **Heart verdict RED · 45** that the board had been rendering as "clear to
  work". The class of harm was not hypothetical.

- **The existing suites caught two real defects in this change.** A `readlink`
  dependency introduced into a script that `test_branch_sweep.py` deliberately
  runs with a lean PATH, and — via a new guard — a gh-driving page the change
  had missed. Both fixed before merge.

- **What could not be fixed in code.** The network allowlist is cloud-environment
  configuration on claude.ai, per environment, with no organization-level
  equivalent and no server-managed setting that can add domains. Documented in
  `PyAutoBrain/board/AGENTS.md` rather than automated.

## Validation

539 PyAutoBrain tests, 224 PyAutoMind tests, `lifecycle.py check` and
`repos_sync.py --check` clean, `ruff` clean on every file touched. 32 new tests
across four files; every guard was confirmed to FAIL against the pre-fix tree
before being trusted. The library-first order (Brain before Mind) was
reproduced locally first: Mind's `firewall_gate.yml` pins PyAutoBrain to `main`,
so the narrowed allowlist showed 7 mismatches against the old main and 0 against
the branch.

## Follow-up

`draft/feature/pyautobrain/board_without_gh.md` — eleven board legs still read
GitHub through `gh api` and stay dark in a remote session. The blindness is now
visible rather than green-and-wrong, which is why this was filed rather than
rushed.


## What CI caught that local validation did not

Two things, both worth keeping.

**The hook is generated into four repos, not two.** The canonical source is
`PyAutoMind/policy/session_start_hook.sh` and `repos_sync.py --write` installs a
copy into every checked-out organ. This session held only PyAutoMind and
PyAutoBrain, so `--write` regenerated two copies and `--check` passed locally —
while PyAutoHeart and PyAutoHands still carried the old text. `firewall_gate.yml`
checks all four organ mains and went red naming exactly those two.

The lesson generalises beyond this task: **a drift check over N repos is only as
strong as the number of them your session can see.** A local `--check` that
passes proves nothing about repos absent from the workspace, and the tool cannot
tell you what it did not look at. The fix was to attach the two missing repos,
regenerate, and ship a one-file PR to each.

**The PR-open event did not trigger PyAutoMind's workflows.** No run appeared for
15+ minutes on a PR whose diff matches four path filters, one of which
(`spawn_drift.yml`) has no filter at all. Actions was healthy: a
`workflow_dispatch` on the same ref started instantly, and the later
`synchronize` push fired all three normally. Treated as a GitHub-side miss on
that one event rather than a repo misconfiguration — recorded because the
symptom (a PR with zero checks) reads exactly like "no CI configured", and the
right response is to verify with a dispatch rather than to merge unchecked.

## Close-out notes

- No GitHub issue: the task began as an environment review in a mobile session
  rather than a filed prompt, so there is no issue to close and no `active/`
  entry to fold.
- The Mind PR hit a dashboard conflict against a base that moved (#340). Resolved
  by regenerating from source, never by a line-level merge of the generated page
  — and re-staged after regenerating, which is the trap a previous record on this
  repo logged.
