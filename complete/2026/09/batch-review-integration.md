## batch-review-integration
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/337
- completed: 2026-09-02
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/338 (merged, `7a7c689`)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/386 (merged, `e869ce6`)
- session: claude-code local (Fable architect, Opus subagents)

### What shipped

Phases 1-2 of the batch-review integration branches: the reviewer can now run a whole batch
together instead of one PR at a time.

- **Phase 1 — a reliable member → (repo, branch) map.** The batch record stores no repo/branch per
  member and `active.md`'s `repos:` field has four dialects, so the evidence JSON now records each
  PR's `head_ref` / `head_sha` / `head_repo` straight from `gh` (`GH_FIELDS` gains
  `headRefName,headRefOid,headRepository,headRepositoryOwner`). Later phases drive off that map,
  never off `active.md` parsing.
- **Phase 2 — `batch collect --integration`.** Opt-in, laptop lane only (same precedent as
  `--fetch`), also triggered by a `- integration: yes` line in the batch record at dispatch. It
  builds **one throwaway worktree root per slot** (`~/Code/PyAutoLabs-wt/integration-<slot>/`, via
  the existing `worktree_create`, so `activate.sh` + PYTHONPATH + per-task cache dirs come for
  free) and, per affected repo, cuts `integration/<slot>` from `origin/main` and merges every
  member's head branch in dispatch order.
- **Conflicts are reported, not resolved.** A member whose merge conflicts is left OUT of that
  repo's branch (merge aborted) and named in the packet and report with the conflicting paths.
  That report is the answer to the original request's "how would this resolve at the end" — it is
  the honest output, not a failure (exit code unchanged).
- **Nothing is pushed.** No remote ref is touched, no PR is opened; the integration root is
  disposable and the canonical checkouts are never used. New Brain network leg is a read-only
  `git fetch origin`, opt-in and documented beside `--fetch`.
- **Fetch fix.** `GH_FIELDS` asked `gh pr view --json` for `merged`, which is not a field — `gh`
  failed the whole request, so every `--fetch` had been scoring UNOBSERVABLE. Now `mergedAt`, with
  `merged` derived. Pre-existing break, found by the end-to-end smoke.
- Packet gains a sentinel-bounded `integration` region (sentinels always emitted, so a refresh
  never blanks it); report gains `## Integration branches` with the copy-paste
  `source <root>/activate.sh` line first; record gains an `- integration-root:` stamp.
  `bin/worktree.sh` gains `PYAUTO_WT_BRANCH` for non-`feature/` roots.
- PyAutoMind#386 is the companion doc change: `batches/AGENTS.md` documents the
  `- integration: yes` / `- integration-root:` record keys.

### Commits

PyAutoBrain: `dcd33e2` (head fields in the evidence JSON), `99e98c9` (`PYAUTO_WT_BRANCH`),
`f39230f` (`_integration.py`), `68054fa` (collect wiring, report, packet region, record stamp),
`7cdf59c` (docs), `bf3e57b` (`mergedAt` fetch fix). PyAutoMind: `3715b97a`.

### Verification

- `tests/test_batch_integration.py` (19 new tests) — temp bare origin + clone, two members on the
  same file: alpha merged, beta left out with `paths == ["a.py"]`, canonical checkout untouched
  (the prompt's Witness); clean multi-member; idempotent re-run; dirty worktree skipped;
  fork / merged / missing-head reported not merged; packet region sentinelled, escaped and
  preserved across refresh; cloud lane refused with a pointer; `plan --integration` → rc 2.
- `tests/test_batch_collect.py` — head fields in the `--json` argv and the row; `mergedAt` → `merged`.
- Full Brain suite: **815 passed**; 1 pre-existing failure
  (`test_cortex_conductor.py::test_a_fixture_tree_finds_the_schema_its_checkout_ships`) that only
  fails inside a task worktree where PyAutoCortex is a symlink — passes on the canonical checkout.
- Laptop smoke on real repos: `collect --slot 2026-08-31-pm --fetch --integration` (all PRs merged
  → `nothing to integrate`, no root built); then with an evidence file naming four unmerged
  branches → PyAutoFit clean, PyAutoArray one merged + two conflicted with paths listed; second run
  reproduced identical trees; root and `integration/*` branches removed afterwards, canonical repos
  back on `main` and clean.
- CI: Brain run 33661956257 (pytest 3.12 + 3.13) success; Mind run 33661975077 privacy success.
- Heart: **YELLOW acknowledged by the human at plan approval**; both reasons unrelated to this
  change — PyAutoArray open PR 10 days old, and release validation incomplete (no rehearsal for
  current source).

### Traps

- `git merge-tree --write-tree` is unavailable on git 2.34.1 here, so there is no dry-run preview —
  the throwaway worktree *is* the preview.
- The packet page cannot be the opt-in button: it is static and credential-free. Opt-in lives in the
  batch record or the `collect` flag.
- Never integrate in the canonical checkouts: they feed every other shell/agent and
  `bin/morning.sh` → `pull_all_main.sh` flips them back to `main`.

### Next

Phase 3 (`--push`, never-force refresh, `integration/*` sweep expiry) is filed as
`draft/feature/pyautobrain/batch_review_integration_branches_p3_push.md`.

## Original prompt

# Batch review: opt-in integration branches so a reviewer can run the whole batch together

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: notify
Witness: a batch-conductor test builds a temp repo with two member branches, runs `collect --integration`, and asserts `integration/<slot>` tree == merge of both heads plus a packet line `clean` / `conflicted: <path>` per repo; evidence JSON carries `headRefName` for every member PR
Review-minutes: 0
Unattended: ready
Issued: 2026-09-02


## Original request (verbatim, 2026-09-02)

For the PyAutoMind runs, I would like to be able to run the code representative of everythign in the review. This
is often require as I need to check if the outputs of a run are as expected and the like. Would it be possible
to make it so when the review is made, a single set of branches I can checkout locally and then created and
temporarily put on GitHub, which puts all changes together? I guess this could be problematic if PRs and changes
conflict, so I am happy to be told this cannot be done safely, but I guess it would also give me a sense of how
work would be resolved at the end. I dont necessarily always need this so it could also be something I can request
at the top of a review via a button, thus saving tokens when sensible.

## Agreed design (assessment 2026-09-02, user: "yep sounds good")

Cheapest safe version is entirely local and needs no new credentials or doctrine change. Libraries are
imported via hardcoded PYTHONPATH (no editable installs), so checking out a merged branch per repo inside a
dedicated worktree root is enough to run everything. Never do this in the canonical checkouts: they feed
every other shell/agent and `bin/morning.sh` -> `pull_all_main.sh` flips them back to main.

### Phase 1 — record member -> (repo, branch) reliably
- The batch record (`PyAutoMind/batches/<slot>.md`) stores no repo/branch/PR per member; `read_active` /
  `active_for` in `PyAutoBrain/agents/conductors/batch/_batch.py` recover PR URLs by regex over
  `active.md`, whose `repos:` field has four dialects. Do not parse those.
- Add `headRefName` (and `headRepository`/repo name) to `GH_FIELDS` (`_batch.py` ~632) and to the evidence
  JSON schema in `agents/conductors/batch/AGENTS.md` ("The evidence JSON"). This is the authoritative
  member -> (repo, branch) map the later phases drive from.

### Phase 2 — `batch collect --integration` (laptop lane, opt-in)
- New flag on `bin/pyauto-brain batch collect`, off by default, laptop lane only (same precedent as the
  opt-in `--fetch` leg that shells to `gh`). Also honour an `integration: yes` line in the batch record at
  dispatch so the human can request it up front.
- Creates one integration worktree root for the slot via the existing helper
  (`PyAutoBrain/bin/worktree.sh` `worktree_create integration-<slot> <repos...>`), which writes
  `activate.sh` with its own PYTHONPATH and per-task NUMBA_CACHE_DIR / MPLCONFIGDIR.
- Per affected repo: cut `integration/<slot>` from `origin/main`, then real `git merge` of each member's
  head branch in dispatch order (git 2.34.1 on this box has no `merge-tree --write-tree`, so no dry-run
  preview; the throwaway worktree is the preview). A conflicting member is left OUT of that repo's branch
  (merge aborted), never resolved by the agent.
- Packet reports per repo: clean / conflicted with the conflicting paths and which member collided. This
  is the "how would this resolve at the end" signal the organism has never had; conflicts are the honest
  output, not a blocker. Print one copy-paste `source <root>/activate.sh` line.
- The packet page cannot be the button: it is static and credential-free (Submit is a link to GitHub's
  new-file form). Opt-in lives in the record / the collect flag, not the page. Cost is git time, not model
  tokens, so default-off is about clutter.
- Regenerable packet region (sentinel-bounded, like `tiles` / `rulings`) so refresh splices it.

### Phase 3 (later, separate) — `--push` and expiry
- `--integration --push` pushes `integration/<slot>` per repo from the laptop's own git auth. New network
  leg in the Brain (stdlib-only/offline invariant, `AUTONOMY.md` ~552-560): explicit, opt-in, laptop only.
- Real branches only (GitHub accepts refs/heads/* and refs/tags/*). Refresh = new commit or `-2` suffix,
  never force-push (never rewrite pushed history). Never a PR, never a base for anything.
- `PyAutoBrain/bin/branch_sweep.sh` would classify `integration/*` as unmerged -> kept forever: ship an
  expiry rule (record the branch names + a `sweep-after` date in the batch record, which lives in a
  LEDGER_DIRS auto-merging dir) so the sweep can void them after the review closes.

## Constraints
- Batch planner already limits each shift to one member per library repo (members collide at merge), so
  within-repo conflicts should be rare; cross-repo single-member cases (one member, five organ PRs) are the
  common case.
- Not the Gut organ: an integration ref is live work being previewed, not condemned material, and a Gut ref in
  the Gut repo cannot be checked out as a library repo. Reuse only the pattern (prefix + manifest line + sweep-after).

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c4232aa1-7376-4851-8e3f-29ef2f9e65cd/scratchpad/intake_raw.md -->
