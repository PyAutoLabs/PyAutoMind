The efficacy review that `docs/agent_failure_modes.md` §9 committed to when
mitigation 6 shipped (PyAutoBrain#140, live 2026-07-17): after the ship series,
has the falsified-by checkpoint stage gone rote? **Verdict: not proven rote —
proven unobservable, which is its own finding. Keep the stage, vocabulary
unchanged; make the reviewer's engagement with each lifted claim part of the
recorded verdict so a rote pass becomes ledger-visible.**

- completed: 2026-08-18
- origin: spun out of PyAutoBrain#130 at its 2026-08-15 close (the one §9 item
  still open); executed as a dashboard-work research session on branch
  `claude/automind-falsified-by-checkpoint-cmsqsi` (PyAutoBrain + PyAutoMind)
- deliverables: Outcome block under mitigation 6 + §9 close-out in
  PyAutoBrain `docs/agent_failure_modes.md`; follow-up prompt
  `draft/feature/pyautobrain/review_claim_dispositions.md`; this record

## Instrument validation first (the method note's D1 guard)

Before trusting any firing-rate number, the claim-lifter was re-exercised on
2026-08-18: a probe text with three known load-bearing claims ("proven
byte-identical", "no-op", "does not affect") lifts 3/3 through the live
`load_bearing_claims()`, and the 5 pinning tests in
`PyAutoBrain/tests/test_review_claims.py` pass (8/8 with the in-place-resolve
tests). A low firing rate below is therefore a fact about the inputs, not a
dead instrument.

## The evidence base

Two sources, honestly scoped:

1. **The autonomy log ship series, 2026-07-17 → 2026-08-01** — every `--auto`
   ship gate since go-live: 21 distinct tasks ran a review leg (jax-compile-time-research,
   inject-keck, inject-alma-simobserve, cold-compile-reduction,
   autotune-off-default, pix-nonfinite-localisation,
   interpolator-aggregator-test-mode, multistart-gradient-auto-convergence
   ph1+ph2, multistart-cadence-int-cast, delaunay-nan-callback,
   multistart-cadence-followups, python-312-floor 1A/1B/1C/1D/1E/4A/4B/4C/4D),
   plus one August cloud-session faculty run recorded in
   [[autohands-firewall-allowlist]] — **22 review-leg gates**, past the ~10-ship
   trial window. August ships after 08-01 were largely interactive/cloud
   sessions the autonomy log does not row; they are not counted either way.
2. **Retro-measurement of the claim matcher over real shipped history** — the
   ReviewSurface is ephemeral (nothing persists what it lifted per ship), so
   firing rate was re-derived by running the live matcher over the squash-merge
   messages on `origin/main` since 2026-07-17 in the two repos available to the
   session. This is a proxy for the branch-message surface (squash messages
   carry the PR body, not always the full branch log) and covers organism
   repos only, not the library ships — disclosed, not hidden.

## 1. Firing rate: neither empty nor saturated

| repo | main commits since 2026-07-17 | with ≥1 lifted claim |
|---|---:|---:|
| PyAutoBrain | 50 | 13 (26%) |
| PyAutoMind | 66 | 3 (5%; registry moves dominate) |

Trigger distribution over the 26 lifted claim-lines: `verified` 17,
`unchanged` 5, `identical` 3, `byte-identical` 2, `no-op` 1. The vocabulary is
not too narrow (it fires regularly) and not too broad (74–95% of ships surface
nothing).

The interesting shape: `verified` dominates, and it mostly lifts the author's
**evidence sentence** ("Verified they actually bite: reverting only
_feature.py fails 7 of the new tests"), not a bare unsupported claim. Shipped
commit messages in this window conspicuously carry "Verified by/against
<probe>" inline — the claim culture mitigation 6 wanted. A zero finding rate
is therefore at least partly deterrence, not only non-engagement.

## 2. Finding rate: zero — and the record cannot say why

Across the 22 review-leg gates: `unverified-claim` FINDINGS raised: **0**.
Grep across the whole Mind (completion records, autonomy log, active/) finds
the category name only in the stage's own shipping records and this prompt.

FINDINGS the review leg did raise in the window were generic-correctness
(2026-07-27 multistart-cadence-int-cast: `int()` truncation → infinite loop,
caught by the run's own review pass 1) or came from **external** adversarial
reviews (Codex gpt-5.6-sol on 07-27, Claude Opus 5 on the 07-29
python-312-floor merges) — not from step 2a.

Distinguishing "unnecessary" from "rubber-stamped": the honest answer is the
ledger cannot distinguish them, and that is the review's central finding (§5).

## 3. Were any load-bearing? One documented exercise; it held

Exactly one autonomy-log row records the adversarial claim pass operating on a
lifted claim: 2026-07-21 interpolator-aggregator-test-mode — *"adversarial
pass on 'no-op outside test mode' claim — gated by is_test_mode()+.exists(),
proven by off-switch test"*. The claim had a falsified-by basis; correctly no
finding; the outcome was unchanged. No ship was held and no correction was
produced by the stage in the window. Its per-ship cost is also ≈ zero (a
stdlib regex plus a few surface lines), so "earning its cost" is a low bar —
but the earning is currently invisible.

Sharpest counter-datum: the one confirmed-wrong load-bearing claim of the
window — the 2026-07-27 "5 siblings affected" count, falsified to 2 by the
external Codex review — lived in an **issue comment**, outside the
commit-message surface the stage reads. The stage could not have caught the
one escape that actually happened. (Widening the scanned surface to issue
text was considered and not recommended: issue prose is where hedged
discussion belongs; the boundary-crossing record the stage guards is the
branch itself.)

## 4. Idle-phrasing exclusion: holding, with two cheap residuals

No changelog/rename chatter is lifted (the pinning test's contract holds on
real data). Residual false positives observed in the retro-measurement:
mid-sentence fragments of wrapped prose (line-based matching lifts "…row, so
the yardstick is real data from the same machine. Verified by"), and narrative
`identical`/`unchanged` describing the *bug*, not the change ("a night the
gate correctly stopped looked identical"). Cost is seconds of reviewer
attention per ship with **no bypass pressure** — unlike the F5 refusal class,
an over-lifted line cannot train bypass-by-default because nothing blocks.
Within budget; no vocabulary change recommended.

## 5. Rubber-stamping: the signature is undetectable as instrumented

The rote signature — claims lifted, reviewed CLEAN, no evidence cited — was
looked for and **cannot be confirmed or refuted**: the ReviewSurface is
ephemeral, and 20 of the 22 gates recorded only "review CLEAN" / "review
self-CLEAN". A healthy pass and a rote one write the identical ledger row.
Two gates only (07-21 above; the August cloud run) left evidence the surface
was engaged at all. Additionally, on autonomous ships the "reader" that
enforcement was delegated to is the branch's own author (`review self-CLEAN`)
— the design's reader-enforcement premise is diluted exactly where the stage
matters most.

## Verdict

**Keep, vocabulary unchanged; close the observability gap.** The instrument
is live and calibrated, the one documented exercise worked as designed, the
false-positive cost is negligible, and the claim culture it targets has
visibly moved toward evidence-inline commit messages. But a stage whose
engagement leaves no trace will go rote silently if it has not already; per
the campaign's own ranking (deleting beats detecting beats reminding), the
fix is to move it from remind-shaped to detect-shaped: the reviewing agent's
verdict gains a **one-line disposition per lifted claim** — `claim →
basis-cited <what> | idle | FINDING` — carried into the ship evidence
(autonomy-log review cell / PR body). A bare CLEAN over a non-empty claims
surface then reads as drift in the ledger, which is the reader-enforcement
the original design promised. Filed as
`draft/feature/pyautobrain/review_claim_dispositions.md` (small, safe).

## Original prompt

# Has the falsified-by checkpoint stage gone rote after ten ships

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

## What this is

The efficacy review that `docs/agent_failure_modes.md` §9 committed to when
mitigation 6 shipped: *"trial on the next ship series, review whether it went
rote after ~10 ships."* Spun out of PyAutoBrain#130 when that issue was closed
(2026-08-15) — it was the one §9 item still genuinely open, and nothing tracked
it.

This is an investigation producing a written verdict from evidence. No code
change is committed up front; a fix may follow from the finding.

## Background

Mitigation 6 (PyAutoBrain#140, merged 2026-07-17, live) made the review faculty
lift **load-bearing empirical claims** out of a branch's commit messages into
the `ReviewSurface` as `claims to falsify` — the trigger vocabulary is `no-op`,
`byte-identical`, `does-not-affect`, `proven`, `behaviour-preserving`. `AGENTS.md`
step 2a then makes an unsupported one a FINDING of kind `unverified-claim`.

Its design was deliberately reader-enforced rather than an author checklist, and
scoped to load-bearing phrasing only, precisely so it could not decay into the
"remember-to-run checklist" the campaign's own constraints ban. It targets the
A5/F3 failure class — confident-wrong effect-claims.

## Why it needs reviewing

The doc's constraint list bans checklists as a mechanism, and a routine
adversarial pass is the single mechanism most likely to decay into one. The
worry is explicit in the shipping comment: *"the one that needs care not to
become the banned checklist."* A stage that fires on every ship and is waved
through every time is worse than no stage, because it also carries false
assurance.

## What to investigate

Over the real ship history since 2026-07-17:

1. **Firing rate** — on how many ships did `claims to falsify` populate at all,
   versus come back empty? An always-empty surface means the vocabulary is too
   narrow; an always-full one means it is too broad.
2. **Finding rate** — how many `unverified-claim` FINDINGS were actually raised,
   and what happened to each? A stage that never produces a finding across ~10
   ships is either unnecessary or being rubber-stamped; distinguish those two.
3. **Were any load-bearing?** For each finding, did falsifying the claim change
   the outcome — a correction, a held ship — or was it cosmetic? This is the
   measure of whether the stage is earning its per-ship cost.
4. **Idle-phrasing exclusion** — is the load-bearing-only scoping holding, or has
   the matcher started lifting incidental prose? Check for false positives of
   the kind that trained bypass-by-default in the guard's first hour (the F5
   cost column).
5. **Rubber-stamping** — look for the signature: claims lifted, reviewed CLEAN,
   no evidence cited in the review. That is the rote failure, and it looks
   identical to a healthy pass unless you read what the reviewer actually did.

## Deliverable

A verdict with the numbers behind it, and one of: keep as-is, narrow/broaden the
trigger vocabulary, or retire the stage. If the finding is "it went rote", say
what would fire instead — per the campaign's own ranking, deleting the
possibility beats detecting it, and detecting beats reminding.

## Method note

Validate the instrument before trusting it: check that the review faculty's
claim-lifting still runs on a branch with known load-bearing claims before
concluding anything from a low firing rate. A null result that looks like a
finding (D1) is the exact failure this campaign catalogued.

<!-- formalised by the Intake (Conception) Agent on 2026-08-15 from user-intake -->
