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
