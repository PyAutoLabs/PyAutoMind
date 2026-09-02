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
