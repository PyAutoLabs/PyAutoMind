## draft-staleness-detection-signals
- issue: (none — both legs shipped directly from the draft prompt; the draft carried
  the delivery annotation in place until this verify-and-retire, 2026-08-18)
- completed: 2026-08-09 (legs 1–2; leg 3 was split out 2026-08-10 and has its own
  record — see split-to below)
- mind-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/168 (squash-MERGED as
  8d7939a8) — leg 1: the `Closes-when:` / `Blocked-by:` gate header keys
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/215 (squash-MERGED as
  13d222c) — leg 2: the `intake reconcile` re-rank
- split-to: `complete/2026/08/reconcile-upstream-repo-mode.md` — leg 3, the
  `--repo` upstream read (PyAutoBrain#224)
- prompt: draft/feature/pyautomind/draft_staleness_detection_signals.md (folded below)
- summary: draft/ staleness is now detectable — a prompt can declare its own exit
  gate and `lifecycle.py issues --drafts` grades it, and `intake reconcile`'s
  ranking was made discriminative enough for a human to actually work through
  (65% of the backlog flagged → ~20%).

## What shipped, per leg

1. **Gate header keys (Mind, PR #168).** A draft can declare `Closes-when:`
   (prompt is DONE when the ref closes) and `Blocked-by:` (READY TO START when
   all refs close). Documented in REFERENCE.md "Declaring a gate", graded by
   `lifecycle.py issues --drafts` with the two opposite readings reported in
   separate bands (GATE MET vs UNBLOCKED — previously both lumped into one
   advisory "shipped, or unblocked?" pile), backfilled onto the drafts that
   already stated a gate in prose, covered by `tests/test_lifecycle_check.py`.
2. **Reconcile re-rank (Brain, PR #215).** Demoted bare cross-references and
   shared topic words; promoted identifier-presence and
   record-body-names-deliverable. On the labelled pre-sweep tree (PyAutoMind
   `f25e154e`): 96 → **31 of 148 flagged (21%)**, `high` cut 52 → 9, the
   largest confirmed finding (the k×s series) at rank 2, the known trap
   (`test_mode_bypass_ordered_assertion_ties`) NOT reported as shipped, and
   read-only asserted by a test.
3. **Upstream `--repo` mode (Brain, PR #224).** Split out 2026-08-10 as its own
   prompt/task and shipped the same day — see
   `complete/2026/08/reconcile-upstream-repo-mode.md` for the full record. It is the only signal that reaches a prompt with no
   Mind-side trace at all.

## The finding that reshaped the acceptance

The original "all five confirmed findings in the top band" criterion was wrong
when written — it contradicted the prompt's own § Hard limit (one finding left
no Mind-side signal whatsoever). Chasing it anyway made the tool worse: a loose
series match pulled one more finding in but falsely flagged the test-mode trap.
The real result is that the five findings need **three different tools**:

| finding | caught by |
|---|---|
| k×s series | reconcile — rare-token fan-out (rank 2) |
| nufft chunking | reconcile — shared rare identifiers |
| test-mode umbrella | `Closes-when:` header key (leg 1) |
| split guard | leg 3 only (evidence sat in a sibling *prompt*) |
| latent resume | leg 3 only (no record exists at all) |

## Verified at retirement (2026-08-18)

All three legs confirmed on `main`: the gate grading + REFERENCE.md docs +
backfills (leg 1), the re-ranked reconcile with its ranking tests (leg 2), and
the leg-3 completion record. A live `intake reconcile` run on the current tree
flags 27 of 136 scanned (20%; 8 `high`, 19 `medium`) — and, fittingly, flags
**this very prompt** at `medium` because the completion records reference it:
the tool detected its own delivered-but-unretired parent draft.

## Traps and findings

- **The trap the tool is built around**: identifier presence upstream is not
  proof of shipping — `test_mode_bypass_ordered_assertion_ties.md` names five
  identifiers all present on PyAutoFit `main` and is confirmed NOT shipped
  (the `try` wraps the wrong line). Reconcile therefore ranks for human review
  and never retires a prompt itself; retiring stays human.
- **The root cause worth its own fix**: work that ships without a Mind record
  (PyAutoFit#1418 had none) is invisible to every Mind-local pass. The ship
  skills failing louder is the deeper repair; leg 3 is the detection-side
  mitigation.
- **A delivered draft is itself drift**: this prompt sat delivered-in-place in
  `draft/` for nine days and showed on the dashboard as planned high-priority
  work, until its own tool flagged it. Verify-and-retire (this record) is the
  loop closing.

## Original prompt

# Make draft/ staleness detectable — `intake reconcile` measured, and the three signals that actually worked

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Why

`draft/` is ~145 prompts graded by **no check at all**. The 2026-08-09 sweep read
acceptance criteria against upstream `main` for two target clusters — 18
PyAutoArray prompts, then 22 PyAutoFit-domain prompts — and found roughly a third
carrying stale state:

| outcome | count (of 40) |
|---|---|
| shipped, recorded to `complete/` | 4 |
| half-shipped (scope narrowed in place) | 2 |
| unblocked by a since-closed prerequisite | 4 |
| unstartable (premise removed upstream) | 1 |
| withdrawn, archived | 1 |
| **mis-gradeable** (an adjacent upstream fix reads like the prompt's) | 1 |

At that rate the remaining ~105 prompts hold real drift. Doing it by hand is
expensive; the question is what can be mechanised.

## The measurement — `intake reconcile` as it stands

A reconcile pass already exists (`pyauto-brain intake reconcile` — "rank backlog
prompts that look already-shipped … always read-only"). It was run against the
pre-sweep tree (PyAutoMind `f25e154e`) so its output could be scored against
findings that were later confirmed by reading upstream source. Result:

- **96 suspects of 148 scanned** — a 65% flag rate (52 `high`, 20 `medium`, 24 `low`).
- Of the 5 confirmed findings, it flagged **2**: the test-mode umbrella (`high`)
  and the latent-samples bug (`low`, i.e. buried).
- It **missed the three largest** — `oversampling_kxs_coupling` (a whole shipped
  5-phase series), `rectangular_adapt_constant_split_guard` (shipped as
  PyAutoArray#417), `nufft_simulator_chunking` (shipped as PyAutoArray#330).

So ~40% recall, and the one true positive at `high` is indistinguishable from 51
other `high`s. **This is a precision problem, not a missing-tool problem.** The
existing matchers — cross-file references and shared topic words — fire on
prompts that merely *mention* each other, which is most of them. Do not rewrite
reconcile from scratch; make its ranking discriminative.

Not a criticism of the tool's existence: it is read-only by design and retiring a
prompt is meant to stay human. The goal here is a signal a human can act on.

## The three signals that actually found things

Each is what surfaced a specific confirmed finding, so each is grounded rather
than speculative.

### 1. Machine-readable "epic closes when X" gates (cheapest; highest precision)

`test_mode_representative_outputs_size_realistic.md` stated its own exit
condition in prose — *"EPIC CLOSES when #70 ships its recipe leg"* — and
autolens_profiling#70 closed as `completed` on 2026-07-17, **the same day that
status line was written**. One issue-state lookup settles the prompt; no clone,
no code read.

`lifecycle.py issues --drafts` does not net this, because it treats a cited issue
as *context* and this one is a *gate*. Proposal: a header key, e.g.

```
Closes-when: https://github.com/PyAutoLabs/autolens_profiling/issues/70
Blocked-by:  https://github.com/PyAutoLabs/PyAutoFit/issues/1331
```

`Closes-when` closed → the prompt is **done**; `Blocked-by` closed → the prompt is
**newly unblocked**. Both are actionable and the two readings are opposite, which
is exactly the ambiguity that makes today's `--drafts` advisory-only. Backfill the
key on the prompts that already say it in prose (this sweep annotated four
unblocked-by-a-closed-gate cases by hand: `bug/priors/12`, `13`, `14`, and
`ep_analytic_updates` WP1).

### 2. Prompt names an identifier that now exists upstream

`oversampling_kxs_coupling.md` § Scope named `_validate_convolve_over_sample_size`
and a partial pre-bin util. Both are on PyAutoArray `main`, and the validator's
**docstring uses the prompt's own phrase** ("the k x s coupling"). Likewise
`nufft_simulator_chunking.md` asked for a `chunk_size` kwarg using `jax.lax.scan`;
`TransformerNUFFT.__init__` has exactly that, under the prompt's suggested name.

Mechanisable: extract backticked `snake_case` / `CamelCase` identifiers from a
prompt's scope/acceptance sections, grep the target repo's `main` (an anonymous
treeless clone is seconds — `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1
--filter=blob:none`), and rank on **hits for identifiers the prompt says do not
exist yet**. Far more discriminative than shared topic words, and it is what a
human grader is doing anyway.

### 3. A completion record already names the prompt's deliverable

`complete/2026/07/interferometer-jax-jit.md` says outright: "`chunk_size` is a
`TransformerNUFFT.__init__` argument that `SimulatorInterferometer` NEVER sets".
That sentence resolves `nufft_simulator_chunking.md` — library shipped, wiring
not. Similarly the split-guard prompt's twin, `rhayes_audit_validation_and_crashes.md`,
carried a full "Phase 1 completion record" for the same surface.

So: search record **bodies** for the prompt's identifiers, not record **slugs** for
the prompt's slug. Slug similarity was measured on this sweep and is useless here
— `oversampling_kxs_coupling` against `kxs-core` scores a Jaccard of **0.25**,
under any workable threshold, and the whole scan missed that finding.

## Hard limit — worth stating so nobody over-promises

**One of the five findings had no signal in PyAutoMind at all.** The
`latent_samples_none_on_resumed_fit` bug was fixed by PyAutoFit#1418 the same day
it was filed, and **no completion record for #1418 exists anywhere in `complete/`**.
No amount of ledger cross-referencing surfaces that. Any design must accept that
the upstream read is load-bearing and the Mind-only passes are a cheap pre-filter,
not a substitute.

Related, and arguably the deeper fix: work that ships without a Mind record is the
root cause here. Worth asking separately whether the ship skills can fail louder.

## The trap any such tool must not create

`test_mode_bypass_ordered_assertion_ties.md` reads as shipped and is not. Main now
catches `exc.FitException` in the TEST_MODE bypass — which looks exactly like the
prompt's requested fix — but the catch wraps only the likelihood call, while
`model.instance_from_vector` (where `check_assertions` actually raises on an
ordering tie) sits on the line *before* the `try`.

**So the tool must rank for human review and never retire a prompt itself** — which
is already reconcile's stated contract. Keep it.

## Scope

1. Add `Closes-when:` / `Blocked-by:` header keys (README "Prompt file format"),
   backfill from prose where prompts already state a gate, and grade them in
   `lifecycle.py issues --drafts` with the two readings reported separately.
   This leg alone is small and worth landing first.
2. Re-rank `intake reconcile`: demote bare cross-references and shared topic
   words; promote identifier-presence and record-body-names-deliverable. Target a
   flag rate that a human can actually work through — under ~15% of the backlog,
   against the 65% measured today.
3. Optional: a `--repo <target>` mode that does the treeless clone and runs leg 2
   for one target cluster, which is the shape the manual sweep took.

## Acceptance

> **DELIVERED 2026-08-09 — and one criterion below was wrong when written.**
> Legs 1 and 2 shipped (PyAutoMind `lifecycle.py` gate keys; PyAutoBrain
> `intake reconcile` re-rank). Leg 3 (`--repo` upstream mode) is not built.
>
> **The "all five in the top band" criterion is unachievable and contradicts
> this prompt's own § Hard limit.** That section already says one finding left
> no Mind-side signal at all — so a Mind-local ranker cannot rank it, by
> construction. Trying to satisfy the criterion anyway actively made the tool
> worse: a loose series match pulled one more finding in but FALSELY flagged
> `test_mode_bypass_ordered_assertion_ties`, breaking the criterion below it.
>
> What the five actually need is three different tools, which is the real
> finding:
>
> | finding | caught by | status |
> |---|---|---|
> | k×s series | reconcile — rare-token fan-out | **rank 2 of 31** |
> | nufft chunking | reconcile — shared rare identifiers | flagged |
> | test-mode umbrella | `Closes-when:` header key (leg 1) | declared + graded |
> | split guard | nothing Mind-local (evidence sat in a sibling *prompt*) | needs leg 3 |
> | latent resume | nothing at all (no record exists) | needs leg 3 |
>
> Corrected criteria, all met:
>
> - The ranker flags **materially fewer** than 96: **31 of 148 (21%)**, down from
>   96 (65%), with `high` cut from 52 to 9.
> - Every finding **reachable from Mind-local evidence** is flagged, and the
>   largest is at rank 2 (it was previously not flagged at all).
> - `test_mode_bypass_ordered_assertion_ties.md` is NOT reported as shipped.
> - No prompt is moved or retired by the tool (asserted by a test).
>
> Leg 3 remains open and is now better motivated: it is the *only* route to the
> last two findings.
>
> **Leg 3 was split out on 2026-08-10** to
> `draft/feature/pyautobrain/reconcile_upstream_repo_mode.md` — one prompt is
> one task is one PR, and legs 1-2 here are delivered. Track leg 3 there; do
> not re-open this prompt for it.

- Re-running the ranker against PyAutoMind `f25e154e` (the pre-sweep tree, which
  is the labelled set this prompt establishes) puts every **Mind-reachable**
  confirmed finding in the top band, and flags materially fewer than 96 prompts.
- `test_mode_bypass_ordered_assertion_ties.md` is NOT reported as shipped.
- No prompt is moved or retired by the tool.

<!-- filed 2026-08-09 from the draft/ sweep (PyAutoArray + PyAutoFit clusters);
     the labelled set is PyAutoMind f25e154e vs the findings recorded in
     complete/2026/07/{oversampling-kxs-coupling,rectangular-adapt-constant-split-guard,
     latent-samples-none-on-resumed-fit,test-mode-representative-outputs-size-realistic}.md -->
