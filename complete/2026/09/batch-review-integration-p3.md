## batch-review-integration-p3
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/339
- completed: 2026-09-02
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/340 (merged, `fb82aab`)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/387 (merged, `7a71955`)
- session: claude-code local (Fable architect, Opus subagents)

### What shipped

Phase 3 — the push half of the batch-review integration branches. **This completes the original
2026-09-02 request in full**: phases 1-2 (the local member→branch map and `collect --integration`)
shipped as PyAutoBrain#338 + PyAutoMind#386 and are recorded in
`complete/2026/09/batch-review-integration.md`; this phase adds the "temporarily put it on GitHub"
half the user asked for, so nothing of the request remains open.

- **`collect --integration --push`.** Opt-in on top of `--integration`, laptop lane only (the
  `--fetch` precedent), using the laptop's own git auth. After the local merges it publishes each
  repo's `integration/<slot>` as a real branch on origin — never a PR, never a base for anything.
  `--push` without `--integration` is a usage error; the cloud lane refuses with a pointer.
- **Never rewrite pushed history.** A remote ref whose tree is identical is left alone; one that
  fast-forwards is advanced; anything else is published as `integration/<slot>-2` (`-3`, …) and
  said so in the packet and report. There is no `--force` path.
- **The record states the expiry.** New `- integration-remote:` (the pushed branch names per repo)
  and `- sweep-after: <YYYY-MM-DD>` (default review-at + 7 days, human-overridable) keys on the
  batch record, which lives in a LEDGER_DIRS auto-merging dir. The packet's integration panel and
  the report name the remote branch per repo.
- **The sweep can now void them.** `bin/branch_sweep.sh` gains a `--records` mode that reads the
  batch records and an `integration/*` case: kept while `sweep-after` is in the future or missing,
  sweepable after it (the Gut transit-clock pattern, storage staying in each repo). The namespace
  is armed for expiry in all three sweep workflows — Brain `branch_sweep.yml` and
  `branch_sweep_all.yml`, and Mind `branch_sweep.yml`, which now also reads `batches/`.
- **Doctrine.** `AUTONOMY.md` "the Brain reads no network except one opt-in flag" gains the second
  network leg, spelled out as opt-in, non-default, laptop only, throwaway integration refs only,
  never `main`, never a PR. Documented alongside in `agents/conductors/batch/AGENTS.md`,
  `batch.sh`, `skills/batch/batch.md` and `PyAutoMind/batches/AGENTS.md`.
- **No real push was performed.** Every push path was exercised against a temp bare origin in the
  tests; the first `--push` against a PyAutoLabs repo is the human's call.

### Commits

PyAutoBrain: `0a72cff` (`--push`, never forced), `a9b7b2e` (`integration-remote:` / `sweep-after:`
record keys, remote in the packet), `7afed66` (`branch_sweep.sh` `integration/*` expiry +
`--records`), `203d3ba` (docs, AUTONOMY.md second network leg), `fc3c214` (CI firewall fix).
PyAutoMind: `1c0ad77c`.

### Verification

- `tests/test_batch_integration.py` — temp bare origin: `--push` publishes `integration/<slot>`
  equal to the local branch; a second run after main moves lands as a new commit or an
  `integration/<slot>-2` branch and never force-updates the first (the prompt's Witness);
  `--push` without `--integration` is rc 2; cloud lane refused; a conflicted repo still pushes the
  partial branch and the panel names the missing members.
- `tests/test_branch_sweep.py` — an `integration/*` branch whose record `sweep-after:` is past is
  classified sweepable, one whose date is future or absent is kept.
- Full Brain suite: **834 passed** (1 permitted deselect — the known
  `test_cortex_conductor.py` case that only fails inside a task worktree where PyAutoCortex is a
  symlink).
- CI: Brain run 33687748948 (pytest 3.12 + 3.13) success on head `fc3c214`; Mind run 33687526086
  privacy success (drift skipped) on head `1c0ad77c`. Both PRs MERGEABLE/CLEAN at merge.
- Heart: **YELLOW acknowledged by the human at plan approval** — `PyAutoArray: open PR 10d old`
  and `release validation incomplete: no rehearsal for current source`; neither touches this change.

### Traps

- **The tenant firewall reads comments, not just code.** The first CI wave went red because
  `bin/branch_sweep.sh`'s new comments used instance names to illustrate the `integration/*` case.
  `fc3c214` removes them. Worked examples in an organ script belong in the tests, not the comments.
- The push is the *only* new network verb, and it is opt-in twice over (`--integration` then
  `--push`) — do not let a future caller collapse that into one flag.
- Expiry lives on the record, not on the ref: a pushed `integration/<slot>` with no
  `sweep-after:` is kept forever by design, so the record write is not optional.

### Next

Nothing outstanding — the 2026-09-02 request is complete across phases 1-3. The first real
`--push` against a PyAutoLabs repo remains a human decision.

## Original prompt

# Batch review integration branches phase 3: --push, never-force refresh, sweep expiry

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: safe
Priority: medium
Depends-on: shipped in complete/2026/09/batch-review-integration.md (PyAutoBrain#338, PyAutoMind#386 — phases 1-2, merged 2026-09-02)
Status: formalised
Consequence: notify
Witness: a test with a temp bare origin runs `collect --integration --push` and asserts origin carries `integration/<slot>` equal to the local branch; a second run after main moves lands as a new commit or an `integration/<slot>-2` branch and never force-updates the first; `branch_sweep.sh` classifies an `integration/*` branch whose record `sweep-after:` is past as sweepable and one that is not as kept
Review-minutes: 0
Unattended: ready
Issued: 2026-09-02

## Context

Phases 1-2 shipped as PyAutoBrain#338 (issue #337) + PyAutoMind#386: `batch collect --integration` builds
one throwaway worktree root per slot merging every member's head branch per repo, locally only. This phase
adds the "temporarily put on GitHub" half of the original request (2026-09-02), so the reviewer can check
the merged state out on another machine or hand it to CI.

## Scope

1. `--integration --push` (laptop lane only, opt-in on top of `--integration`): after the local merges,
   `git push origin integration/<slot>` per repo from the laptop's own git auth. Real branches only
   (GitHub accepts refs/heads/* and refs/tags/*). Never a PR, never a base for anything; the packet's
   integration panel and the report gain the remote branch name per repo.
2. Never rewrite pushed history: if `origin/integration/<slot>` already exists and differs, push a NEW
   commit on top when fast-forwardable, else push `integration/<slot>-2` (`-3`, ...) and say so; never
   `--force`. Record the pushed branch names on the batch record (`- integration-remote:`), which lives in
   a LEDGER_DIRS auto-merging dir.
3. Expiry: `- sweep-after: <YYYY-MM-DD>` on the batch record (default = review-at + 7 days, human may
   override); `PyAutoBrain/bin/branch_sweep.sh` gains an `integration/*` case — kept while the record's
   sweep-after is in the future or missing, sweepable after it (pattern borrowed from the Gut transit clock,
   storage stays in each repo). Today the sweep would classify these as unmerged-and-kept forever.
4. Doctrine: `PyAutoBrain/AUTONOMY.md` "The Brain reads no network except one opt-in flag" gets an
   explicit clause for `--integration --push` (opt-in, non-default, laptop only, push of throwaway
   integration refs only, never main, never a PR); batch `AGENTS.md`, `batch.sh`, `skills/batch/batch.md`
   and `PyAutoMind/batches/AGENTS.md` document the flag and keys.
5. Tests per the Witness plus: `--push` without `--integration` is a usage error; non-laptop lane refuses
   with a pointer; a conflicted repo (member left out) still pushes the partial branch and the panel says
   which members are missing from it.

## Constraints

- Builds on `_integration.py` and the record keys from phases 1-2 — PyAutoBrain#338 and
  PyAutoMind#386 merged 2026-09-02 (`complete/2026/09/batch-review-integration.md`), so this is unblocked.
- Remote sessions have no usable push credential (GITHUB_ACCESS.md); this is a laptop leg like `--fetch`.
- `git merge-tree --write-tree` is unavailable (git 2.34.1 on the laptop); nothing here needs it.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c4232aa1-7376-4851-8e3f-29ef2f9e65cd/scratchpad/intake_phase3.md -->
