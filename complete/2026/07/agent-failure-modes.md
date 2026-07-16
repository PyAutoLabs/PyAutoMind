## agent-failure-modes
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/130
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/131 (doc) + #132 (mitigations 1+2) + #133 (guard v1.1) — all merged
- summary: campaign #155 Phase 5 capstone. A-E catalogue validated by measurement; enlarged out-of-sample (F1-F5); taxonomy compressed to two root causes; refusals-vs-informs hypothesis sharpened (informs fail even as live self-awareness; refusals ~100% with measured false-positive cost). Mitigations 1+2 SHIPPED and WIRED: pipefail agent-shell default (BASH_EXECUTION_STRING discriminator; $0 approach measured wrong pre-ship) + Mind commit guard. The guard's first live hour produced two false positives on its own author; v1.1 (token-level clause parsing) shipped same hour with both incidents as regression tests — the F5 cost column, lived. Items 3-6 = enumerated follow-ups.

## Original prompt

# Investigate how the organism can stop its agents making these mistakes

Type: research
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Model: Fable

## What this is

The companion to `draft/research/workspaces/env_profile_and_validation_gate_redesign.md`. That
one asks how to redesign a *config system* so it stops producing bugs. **This one asks how to
stop the *agent* producing bugs** — and it is the more uncomfortable of the two, because the
evidence is a single day's transcript in which one Opus session made **fourteen** distinct
errors, most of which it did not catch itself.

This is not a request for a style guide. It is a request to look at real, itemised failure data,
find the structure underneath, and design mechanisms that would actually have fired.

**Take the time this needs.** Read the code, read `AGENTS.md` and the skills, run things, test
your own proposals. If you propose a mechanism, demonstrate against the catalogue below that it
would have caught specific listed errors — a mechanism that would have caught none of fourteen
is not a mechanism.

## The evidence (2026-07-15, one session)

Errors are listed with what was claimed, what was true, what it cost, and what caught it.

### A. Verification that only confirmed what was already assumed

| # | Error | Cost | Caught by |
|---|---|---|---|
| A1 | Read `env_vars.yaml` (smoke) instead of `env_vars_release.yaml` (the profile the failing job loads). Proposed a fix that would have changed nothing. | ~1h; a plausible-but-wrong plan presented to the human | Reading further, by luck |
| A2 | Claimed the smoke change "lets the per-PR gate catch this". Never checked `smoke_tests.txt`, which contains neither script. **Shipped the false claim into a commit message, a PR body, and a source comment.** | A correction commit + 3 corrective comments; the wrong claim nearly landed in `main` | Self, while verifying the change was real — *after* shipping |
| A3 | "`PYAUTO_DISABLE_JAX` has exactly one consumer" — grepped 3 of 5 libraries. Missed `PyAutoLens`, which flips `use_jax` **before** `super().__init__()`. | A fix that was silent for 54 of 97 scripts | Human-requested adversarial pass, *after* the fix was built and offered for ship |
| A4 | "`use_jax` defaults to `False`, so truthiness means explicitly requested" — true for `af.Analysis`, false for the whole `ag.*`/`al.*` surface, which defaults `True`. | Same fix would have fired on default constructions claiming JAX "was requested" | Same adversarial pass |
| A5 | "The fix works — I ran it on a real script." The script was the one path (`af.ex.Analysis`) where the assumption held. | Presented as decisive proof; was not | Same adversarial pass |

**Shape:** every one is *verification pointed at the path already believed*. A5 is the purest: a
real end-to-end run, real output, genuinely green — and worthless, because it exercised the
assumption instead of testing it.

### B. Trusting a stored belief over the repository

| # | Error | Cost | Caught by |
|---|---|---|---|
| B1 | A memory note written **the previous day** said, verbatim, `TRAP: env_vars.yaml TEST_MODE=2 vs release.yml TEST_MODE=1`. The trap was walked into anyway (= A1). | The note fired for nobody | Nothing |
| B2 | Memory said PyAutoArray `feature/inversion-testmode-singular-guard` was "PARKED awaiting ship sign-off". It had shipped by another route; issue closed; branch contributed nothing. **The stale note was used to argue the hygiene tool had a false positive — the tool was right.** | Nearly protected debris and mistrusted a correct tool | Testing the claim against the repo |

**Shape:** stored beliefs decay silently and then argue *against* correct action. B1 is the
strongest datum in this document: **documentation of a trap did not prevent the trap, one day
later, in the same codebase, by the same agent.** Any proposal whose mechanism is "write it down"
must explain why it beats B1.

### C. Recall instead of enumeration

| # | Error | Cost | Caught by |
|---|---|---|---|
| C1 | Hand-wrote repo lists for sweeps **at least five times**. Each missed repos: `autolens_profiling`, `HowToFit/Galaxy/Lens`, `autolens_assistant`, `PyAutoReduce`, `euclid_strong_lens_modeling_pipeline`. Reported "final state" three times before it was final. | Repeated false "all clear"; 11 debris branches nearly left behind | Only by finally enumerating `*/` |
| C2 | `PyAutoMind/repos.yaml` — **the canonical body map, listing all 30 repos** — contains *every* repo missed in C1. It was never used. | The lever existed and was not reached | Checked only at the human's prompting, at the very end |

**Shape:** C2 is the twin of B1. B1 = a note that existed and didn't fire. C2 = a *tool* that
existed and wasn't reached. Both were available at the decisive moment; neither was consulted.
The organism's problem may be less "we lack the right artifact" than "nothing routes the agent to
it while it is making the decision".

### D. Tools and heuristics trusted without validation

| # | Error | Cost | Caught by |
|---|---|---|---|
| D1 | Ran `git merge-tree --write-tree` (needs git ≥2.38; local git is **2.34.1**). It failed for **all 57 branches**, and the failure rendered as a tidy column of `?? INSPECT` — **a null result that looked exactly like a finding.** | A whole sweep's output was meaningless and was nearly reported | Noticing the *uniformity* of the result was implausible |
| D2 | `git cherry` was about to be used as the debris heuristic. Tested against a branch **proven** to contribute nothing: it reported `+` ("not upstream"). The heuristic was wrong. | None — caught before use | Deliberately testing the heuristic against known ground truth |
| D3 | `git diff stash@{0} origin/main` used to ask "does this stash contain anything unique?". It compares whole trees, so it measured how far `main` had moved. Output was large, plausible, and meaningless — and was printed before being questioned. | Nearly drew conclusions about 5 stashes from noise | Self, on re-reading the output |

**Shape:** D1 and D3 are the dangerous kind: **a broken method that produces confident-looking
output**. D2 is the antidote and the only clean save in the whole day — *validate the instrument
against a case whose answer you already know, before trusting it*. That habit was applied exactly
once, by chance.

### E. Shared-state and convention errors

| # | Error | Cost |
|---|---|---|
| E1 | `prompt_sync_push` does `git add -A`; it swept a **concurrent session's** file into this session's commit. A memory note about this exists; it did not fire (another B1). | Committed another agent's in-flight state |
| E2 | Told the human a dirty file was "not mine". It was mine. | A false statement in a status report |
| E3 | Filed a prompt into `active/bug/<target>/` when `active/` is flat. | Lifecycle tool couldn't find it |
| E4 | `complete.md` H2 slug didn't match the record filename; drift guard caught it. | Rework; **the guard worked** |

## What actually caught things — the most useful signal in here

Sort the fourteen by what caught them:

- **Mechanisms that REFUSED an action: 100% hit rate.**
  - `worktree_remove` refused to delete a worktree with uncommitted work → forced a look → correct call.
  - `git` refused `branch -D` on checked-out branches → led to discovering a hidden `.worktrees/`
    directory holding 5 abandoned worktrees that no scan knew about.
  - `lifecycle.py check` refused on slug drift (E4).
  - The `PreToolUse` API gate (per `AGENTS.md`) is the same species.
- **Mechanisms that INFORMED: 0% hit rate.** The memory note (B1), the `git add -A` note (E1),
  `AGENTS.md` conventions (E3), `repos.yaml`'s existence (C2). All present. None fired.
- **Human intervention:** caught A3, A4, A5 — the three worst — via one request for an
  adversarial pass, *after* a broken fix had been built and offered for shipping.
- **Luck / self-review:** A1, A2, D1, D3.

**The hypothesis worth testing hardest: guardrails that block work, guardrails that inform do
not.** If that survives your scrutiny, it should dominate the design. If it does not, say so —
it is drawn from one day and one agent, and is exactly the kind of tidy conclusion this document
elsewhere warns about.

## What to investigate

1. **Validate or destroy the catalogue.** It was written by the agent that made the errors, which
   is grounds for suspicion (see "Trust nothing here"). Re-derive what you can. The git version
   (2.34.1), `repos.yaml`'s contents, `smoke_tests.txt`'s contents, and the `use_jax` defaults are
   all checkable in minutes.
2. **Find the real taxonomy.** The A–E grouping is a first pass, not a finding. Is there a smaller
   set of root causes? Candidate framing to attack: *the agent reliably verifies, and reliably
   verifies the wrong thing* — every A-class error involved real work producing real evidence for
   a proposition nobody had questioned.
3. **Design mechanisms that fire at the decisive moment.** Directions worth weighing (argue with
   them; they are hypotheses):
   - **Convert informational guidance into refusals.** Which of B1/C2/E1/E3 could become a hook,
     a check, or a tool that *blocks* rather than reminds?
   - **Give the repeated questions a single blessed implementation.** "Does this branch contribute
     anything to main?" was hand-rolled three times today, two ways wrong (D1, D2), before landing
     on merge-and-compare-trees. That should be one tested command (`pyauto-gut`? a Heart check?),
     not a thing each agent reinvents under time pressure. Same for "which repos exist?" →
     `repos.yaml`. Same for "what env does this script actually run with?" →
     `autobuild repro_command`, which **already exists** and was not used today.
   - **Make null results impossible to mistake for findings** (D1). A tool that errors 57/57 times
     should be loud, not a tidy column.
   - **Make "validate the instrument against a known case" (D2) systematic** rather than lucky.
   - **Make the adversarial pass routine rather than requested.** It caught the three worst errors
     and cost ~15 minutes. What is the cheapest way to make it always run before a ship
     checkpoint — and does making it routine blunt it?
4. **Attack the memory system honestly.** B1 and B2 are two different failures — a note that
   didn't fire, and a note that was wrong and *argued against the truth*. Is per-session memory a
   net positive here? What would make it fire when it matters, or fail safe when stale? Consider
   that "recalled memories … reflect what was true when written" is already policy and still
   produced B2.
5. **Cost the proposals.** The agent is the scarce resource. A mechanism that adds 15 minutes to
   every task to prevent a 5-night outage is cheap; one that adds an hour to every trivial edit is
   not. Say which is which.

## Constraints — read these before proposing anything

- **Do not propose documentation as a primary mechanism.** B1 is the refutation: a one-day-old
  note naming the exact trap, in the exact repo, did not fire. If you propose writing something
  down, you must explain why it beats B1. "Put it in `AGENTS.md`" is E3, which also failed.
- **Do not propose a checklist the agent must remember to run.** That is a hand-maintained
  "remember to" list, and today's other brief establishes that such lists *are* the trap.
- **Prefer deleting the possibility of the mistake** to detecting it, and detection to reminding.
- **Do not gold-plate.** The organism already has `repos.yaml`, `autobuild repro_command`,
  `lifecycle.py check`, `worktree.sh`'s refusals, and a `PreToolUse` gate. Several failures today
  were *non-use of existing levers*, not absent ones. Reaching for the existing lever beats
  building a new one — check what exists before designing.
- **This must not become a system so heavy that agents route around it.** A guardrail that gets
  bypassed is worse than none, because it also carries false assurance.

## Trust nothing here

This document was written by the agent that made all fourteen errors, on the same day, and is
therefore exactly the kind of artifact it warns about: confident, tidy, and unaudited. At least
one prior conclusion of this agent's ("the tool has a false positive", B2) was stated with
conviction and was wrong. Treat the catalogue as leads. Where a claim matters to your design,
check it — most are checkable in minutes.

Note also the selection bias: this catalogue contains the mistakes that were *eventually noticed*.
The errors that were never caught are, by construction, absent — and A2 (a false claim shipped
into a commit message, caught only by chance, after merge-time) suggests the unnoticed set is not
empty. Consider how you would estimate its size.

## What to produce

A design document (propose where it lives), covering:

1. A **validated failure taxonomy** — corrected against your own checking, with the catalogue's
   errors either confirmed, refuted, or reclassified.
2. **A ranked set of structural mitigations**, each with: which catalogue entries it would have
   caught, why it fires at the decisive moment (vs. B1/C2), its cost per task, and how it fails.
3. **An explicit "rejected" section** — including anything above you think is wrong. The
   "refusals work, reminders don't" hypothesis is the one most worth trying to break.
4. **Open decisions for the human**, separated from what you are confident about. In particular:
   how much friction is acceptable at a ship checkpoint, and whether the memory system earns its
   keep in its current form.
5. **A migration path.** Land incrementally; nothing big-bang. This machinery sits in the path of
   all real work.

## Method

- **Run things.** Check the git version, read `repos.yaml`, read `smoke_tests.txt`, read
  `run_smoke.py`, grep the `use_jax` defaults. Every claim in section A–D is checkable.
- **Validate your instruments against known cases before trusting them** (D2 is the one habit
  that worked all day).
- **Adversarial pass before concluding**: for each load-bearing claim — *what would have to be
  true for this to be false, and have I looked?* Then look.
- **Enumerate; do not recall.** `repos.yaml` for repos, `*/` for directories. C1 is what recall
  costs.
