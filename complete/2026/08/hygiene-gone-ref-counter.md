- issue: none (the prompt was never issued — the defects were fixed under other issues, see below)
- delivered-by: **PyAutoBrain#205** (squashed `7ad1e43`, 2026-08-07) and **PyAutoBrain#200** (squashed `5cb1c73`, 2026-08-05, issue PyAutoBrain#197)
- classification: library (PyAutoBrain) — bug, infrastructure
- LEDGER BACKFILL, not new work: this record was written 2026-08-08 when the prompt
  was picked up for development and found already delivered. No code was written for
  it. Defect 2's delivery is separately recorded in
  `complete/2026/08/hygiene-coverage-drift.md`; Defect 1 (#205) had **no** record
  until this one, so the ledger carried a gap.

## What the prompt claimed

`hygiene tidy` under-reported git debris by roughly an order of magnitude — it
reported "12 stale branches across 9 repos, 0 stashes, 0 [gone] refs, 0 dirty
checkouts" when the real state was 91 branches across 28 repos, 4 stashes, dozens of
`[gone]` refs and 3 dirty checkouts. Two independent defects.

## Both defects were already fixed

**Defect 1 — the `[gone]` counter could never be non-zero.** `prescan_tidy` counted
with `git branch -vv | grep -c '\[gone\]'`, but porcelain prints the upstream as
`[origin/<branch>: gone]`, never the bare `[gone]`, so the pattern matched nothing in
every repo, always. Fixed by **PyAutoBrain#205** (2026-08-07), which switched to
`for-each-ref --format='%(upstream:track)'` — the idiom
`enumerate_condemn_candidates` and `repo_cleanup` already used — and added a
regression test building a fixture with a genuinely gone upstream, verified to fail on
the unfixed counter.

**Defect 2 — the scan covered 9 repos, not the organism.** `prescan_tidy` iterated
hardcoded `LIB_REPOS` + `ORG_REPOS` literals, so PyAutoCTI, PyAutoReduce, PyAutoMemory,
every workspace, every HowTo and every assistant were invisible; the "0 stashes" and
"0 dirty checkouts" figures were scope artifacts, not detector bugs. Fixed by
**PyAutoBrain#200** (2026-08-05): `LIB_REPOS`/`ORG_REPOS`/`WS_REPOS` are now derived
from the body map via `_hygiene_repos.py` reading `repos.yaml`, with a
`repos_sync.py` coverage check that fails if they drift from the map or if a repo name
is written back into an array literal. That is exactly the resolution the prompt asked
someone to decide on, and it names the same `_hygiene_extras.py`/PR#193 precedent.

## Verification done before retiring the prompt (2026-08-08)

The prompt specified its own control: *"Before the fix, `prescan_tidy` must reproduce
`0 [gone] refs` on a checkout known to have some. After, the count must be non-zero on
that same tree. A green run on a tree with zero `[gone]` refs proves nothing — pick the
tree first."* That control was run rather than assumed:

- Built a throwaway repo with a real bare remote, pushed a branch, deleted it on the
  remote, and `fetch --prune`d so the checkout genuinely carried a `[gone]` ref.
- On that same tree: the old form `git branch -vv | grep -c '\[gone\]'` → **0**;
  the shipped form `for-each-ref '%(upstream:track)' | grep -c '\[gone\]'` → **1**.
- Confirmed no repo-name array literal survives anywhere in `hygiene.sh` — every loop
  runs over the derived `CODE_REPOS`/`SCAN_REPOS`, including `run_tidy` and
  `enumerate_condemn_candidates`, the two the prompt named as sharing the limitation.

## Trap worth keeping

Establishing "already fixed" required deepening the clone. Cloud-session checkouts are
**shallow** (`git rev-parse --is-shallow-repository` → true), and a shallow PyAutoBrain
makes `git diff origin/main...<branch>` fail with `no merge base` and makes
`git log origin/main..<branch>` list commits that ARE on main. Both look like evidence
of divergence and are artifacts of the graft boundary. `git fetch --deepen=500` first,
then test ancestry with `git merge-base --is-ancestor`.

## Original prompt

# The hygiene tidy pre-scan reports 0 [gone] refs unconditionally, and scans only 9 of ~28 repos

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Found during a `/repo_cleanup` sweep on 2026-08-04. `hygiene tidy` reported
"12 stale branches across 9 repos, 0 stashes, 0 [gone] refs, 0 dirty checkouts".
The real state at that moment was 91 branches across 28 repos, 4 stashes,
dozens of [gone] refs and 3 dirty checkouts.

Two independent defects produce that gap.

## Defect 1 — the `[gone]` counter can never be non-zero

`agents/conductors/hygiene/hygiene.sh:129`:

    g=$(git -C "$dir" branch -vv 2>/dev/null | grep -c '\[gone\]' || true)

`git branch -vv` prints the upstream as `[origin/<branch>: gone]`, never the
bare `[gone]`. The pattern matches nothing, in every repo, always. Proof on
PyAutoHands, which had three at the time:

    git branch -vv | grep -c '\[gone\]'                        -> 0
    for-each-ref --format='%(upstream:track)' refs/heads       -> [gone] x3

`prescan_tidy` then folds `gone` into the `total` at line 133-134, so the
conductor's prioritisable count for `tidy` is systematically understated and
`tidy` under-ranks itself against the other hygiene modes.

Fix: count via `for-each-ref '%(upstream:track)'` (already the idiom used in
`repo_cleanup`'s own audit), or match `: gone]`.

Note `enumerate_condemn_candidates` at line 419 does NOT share this bug — it
uses `for-each-ref` correctly.

## Defect 2 — the scan covers 9 repos, not the organism

`prescan_tidy` (line 121) iterates `LIB_REPOS` + `ORG_REPOS` only:

    LIB_REPOS=(PyAutoNerves PyAutoFit PyAutoArray PyAutoGalaxy PyAutoLens)
    ORG_REPOS=(PyAutoBrain PyAutoHands PyAutoHeart PyAutoMind)

That is the "9 repos" in the summary line. Invisible to it: PyAutoCTI,
PyAutoReduce, PyAutoMemory, PyAutoGut, PyAutoScientist, every workspace, every
HowTo, every assistant, autolens_profiling, admin_jammy. Both the "0 stashes"
and "0 dirty checkouts" figures were scope artifacts, not detector bugs — all 4
stashes and all 3 dirty trees lived in repos it never looks at.

Decide whether the fix is to derive the repo set from `PyAutoMind/repos.yaml`
(the body map) rather than re-listing it, which is the same hard-coding problem
`_hygiene_extras.py` was just refactored to remove in PR #193. `run_tidy` /
`enumerate_condemn_candidates` share the same two lists and the same limitation.

## Why it matters

`hygiene tidy` is the advertised front door for git debris and the thing a
human reads before deciding whether a cleanup is worth running. Under-reporting
by roughly an order of magnitude makes it read as "nothing much to do" when
there is. A wrong-but-quiet number is worse than no number.

## Control

Before the fix, `prescan_tidy` must reproduce `0 [gone] refs` on a checkout
known to have some (any repo with a merged-and-deleted upstream). After, the
count must be non-zero on that same tree and match
`for-each-ref | grep -c '\[gone\]'`. A green run on a tree with zero [gone] refs
proves nothing — pick the tree first.

<!-- raised from a /repo_cleanup sweep, 2026-08-04 -->
