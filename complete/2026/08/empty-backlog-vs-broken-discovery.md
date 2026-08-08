- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/213 (closed on merge)
- completed: 2026-08-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/214 (squash-merged as `330b75a`); Mind bookkeeping PyAutoMind#157
- split-from: conductor-discovery-lifecycle-split (PyAutoBrain#211/#212, complete/2026/08) — that task fixed the broken discovery roots and deliberately left this as separate work
- summary: a conductor's empty selection result read the same whether the backlog was genuinely bare or discovery was pointed somewhere wrong. Added `empty_discovery_reason(mind, work_type)` to the sizing faculty, distinguishing a bad path / a non-Mind checkout / a missing work-type (listing those present) / a genuinely empty backlog; the three conductors print it on their empty paths. Diagnosis only — `discover_prompts` keeps its signature and result, exit codes unchanged, and #212's end-to-end assertions pass untouched. CI green on both pytest legs; 267 tests pass (261 + 6 new).

## Key findings

- **The ambiguity was the bug, not the wrong path.** #211's actual defect was a one-line stale root, trivially fixable at any point in the four weeks it lived. What made it survive was that a broken root and an empty backlog printed the same sentence. Worth generalising: **when a failure mode is "nobody noticed", the fix that matters is usually to the signal, not to the code that failed.** The parent task's own completion record flagged this and left it unfiled; it took a follow-up to close.
- **"No `draft/`" is the wrong test for Mind-ness.** A freshly-spawned Mind has `active.md` but no `draft/` yet — the template ships without it, since `active/` and `draft/` hold only instance state. Testing `draft/` alone would tell a legitimately-empty new Mind that it is not a Mind checkout. The check is `draft/` **or** `active.md`, and there is a regression test for exactly that case.
- **The diagnostic names `PYAUTO_MIND`, not `--mind`.** `_sizing.py` and the conductors' Python layer take `--mind`, but the surface a human drives is `bin/pyauto-brain`, which resolves the checkout through `resolve_mind` → the `PYAUTO_MIND` env var. An error message must name the knob the *reader* has, not the one the callee has.
- **Sizing over-scored a detailed bug prompt for the second time running.** Intake scored this `large` (7) as it did the parent (8), for a change that is one helper, three call sites and a test. Both were corrected to `small`/`safe` at filing with rationale inline. Two for two on carefully-written bug reports: the heuristic's word-count and risk-vocabulary terms partly measure *how well the prompt was written*. Not filed as a task — flagged here so a third instance reads as a pattern rather than a coincidence.

## Also in this change set

`planned.md` sweep (separate commit, PyAutoMind#157): removed `brain-lifecycle-path-fixes` (shipped 2026-07-16, record in complete/2026/07 — it had sat listed as blocked for three weeks after shipping) and `lenstool-scaling-slam` (superseded by dpie-lenstool-default, per that task's own record). Both verified against completion records rather than their own self-annotations.

**`planned.md` is not covered by `lifecycle.py check`** — that invariant guards `active.md` against `complete/` only. That is why this drift went unnoticed and why it needed a manual sweep. Noted, not fixed; a guard would be its own task.

## Environment note

Shipped from a cloud/web session: no `~/Code/PyAutoLabs-wt/` worktree layout, so work ran directly in the PyAutoBrain checkout on the session-designated branch. Because the branch's previous PR had already merged, the branch was restarted from `origin/main` and force-pushed with `--force-with-lease` — safe only after confirming the remote tip's tree was identical to `main`. Note that `git cherry` is the wrong check after a **squash** merge: it compares patch-ids, so a branch of N commits squashed into one shows all N as unmerged (`+`). The reliable test is `git diff --quiet <remote-branch> <main>`.

## Original prompt

# Empty backlog is indistinguishable from broken discovery in the conductors

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

<!-- Header corrected from the IntakeDecision at filing time (2026-08-08):
     difficulty large -> small, autonomy supervised -> safe, PyAutoMind dropped
     from Repos. Same over-sizing the parent task (#211) hit and recorded: the
     heuristic scores prompt verbosity and the risk vocabulary a careful bug
     report necessarily uses, not the size of the change. This one adds one
     helper plus three call sites and a test. PyAutoMind is read, not modified. -->

Split out of `conductor-discovery-lifecycle-split` (PyAutoBrain#211/#212,
complete/2026/08), which fixed the broken discovery roots but deliberately left
this behind as separate work.

## Problem

When a conductor's selection mode finds nothing it prints a flat message:

- `feature agent: no feature prompts found in PyAutoMind.`
- `bug agent: no bug prompts found in PyAutoMind/draft/bug/.`
- `refactor: no prompts under refactor/ — try 'candidates'`

Each is consistent with two very different situations:

1. the backlog genuinely holds no prompts of that work-type; or
2. discovery is pointed somewhere wrong — a bad `--mind`, a non-Mind checkout, a
   layout change the discoverer has not learned.

Case 2 is what #211 was: three conductors reported case 1 for four weeks while
sitting on 87 prompts, and nobody noticed, because the message a broken root
produces is the same message an empty backlog produces. That was the entire
reason the bug survived — not the wrong path itself, which was a one-line error.

## Fix

Make an empty result explain itself in @PyAutoBrain. The discoverer knows which
roots it probed and what it found there; the conductors currently throw that away.

1. `agents/faculties/sizing/_sizing.py` — add a companion to `discover_prompts`
   that classifies an empty result against the Mind it was pointed at, and
   returns a human-readable reason. The distinctions worth drawing:
   - the Mind path is not a directory, or holds no `draft/` and no registry
     files — **not a Mind checkout**;
   - it is a Mind, but `draft/<work-type>/` does not exist — **no such
     work-type**, and the message should name the work-types that DO exist;
   - the folder exists and is empty, or holds only READMEs — a genuinely
     **empty backlog**, the only case that should read as "nothing to do".
2. The three conductors print that reason on the empty path instead of the flat
   sentence. Keep the current exit codes; this is about the message.
3. Regression test in `tests/test_conductor_discovery.py` (or a sibling): the
   three cases produce three distinguishable reasons, and a populated Mind is
   untouched.

## Scope

Message-and-diagnosis only. Do NOT change discovery behaviour, ranking, or exit
codes — `discover_prompts` keeps its signature and its result, and the
end-to-end non-empty assertions from #212 must keep passing unchanged.

<!-- formalised by the Intake (Conception) Agent on 2026-08-08 from file:/tmp/claude-0/-home-user/a776a449-cbea-5069-9c29-7ed6fa93a291/scratchpad/silent_empty.md -->
