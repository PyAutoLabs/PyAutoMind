## heart-evidence-audit
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/83
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/84 (merged)
- summary: readiness evidence-chain audit (build-chain campaign #155 Phase 2). Per-leg evidence map; findings A (test_run server-first path unreachable from every real entrypoint), B (version_skew unfailable by releases), C (verify_install never satisfied post-PR#77); finding 3 resolved (HowTo* smoke passed on force-committed datasets purged by #151 — pre-existing falsehood, not a regression; satellite prompt filed). Verdict-worth: gate holds partly by paralysis; nightly grant kept formally, treated inoperative until test_run wiring fixed + one verify_install ingest runs. Five fix items in doc §5; fix PRs follow separately.

## Original prompt

# Audit the evidence chain behind Heart's release verdict — can the GREEN gate be trusted at all?

Type: research
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBuild
- HowToLens
- HowToGalaxy
- HowToFit
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: high
Model: Fable
Status: formalised

## What this is

An **audit of the evidence chain**, not a bug fix. On 2026-07-15 a single half-day of work on one
YELLOW leg turned up **three unrelated integrity failures in the evidence Heart uses to decide
whether it is safe to release** — plus a fourth in the agent layer that routes the work. Each was
small. Each was found by accident while doing something else. None was detected by any gate.

The question worth answering is not "what are the three bugs" — two are already fixed or filed. It
is: **Heart is the authoritative "is it safe to release?" verdict, the armed nightly ships live to
PyPI on Heart-GREEN with deliberately no force input — and today every leg we looked at had
unreliable evidence underneath it, in a different way each time. So what is the verdict actually
worth right now, and what design makes the chain trustworthy?**

The recurring shape, across today and the 2026-07-15 release before it:

> **The organism keeps acting on evidence that was never produced, was produced and discarded, was
> destroyed after production, or was compared against something incomparable — and in every case the
> surface reported success.**

## The four findings (measured 2026-07-15 — re-measure; do not inherit)

### 1. Evidence produced, then discarded — install-verification leg (FIXED, PR#77 `e43a3a9`)

Stage 3 (`workspace-validation.yml`, `mode=release`) has always run `verify_install` A–E against the
TestPyPI wheels. `heart/validate.py` consulted the sidecar **only in the failure direction**: 
`ready is False` force-failed the stage, a **PASS contributed nothing**, and nothing ever wrote the
`verify_install.json` that `heart/state.py` reads. The leg reported `install verification not run`
**forever**, regardless of how often the check passed.

Measured before the fix: `~/.pyauto-heart/verify_install.json` **absent**; `validation_report.json`
from the real 2026-07-15 release run ingested cleanly (integrate `pass`, 543p/0f) with **zero**
`verify_install` trace. Fixed by carrying the sidecar as evidence and persisting it on `--ingest`.
`workspace-validation.yml` needed **no change** — it had always passed `--verify-install`. The CI
side was wired correctly the whole time; only the Python side threw the result away.

**The interesting part is not the fix.** It is that a check ran in CI, for months, at real cost, and
its success was structurally incapable of reaching the verdict it existed to inform — and the only
symptom was a leg that read "not run", which everyone interpreted as "nobody ran it yet".

### 2. Evidence destroyed by running the tests — `test_run` leg (FILED, unfixed)

Running PyAutoHeart's own unit suite overwrites the developer's **live** `~/.pyauto-heart/test_run.json`.
`tests/test_test_run.py` isolates the *input* (`results_dir=tmp_path`) but not the *output*:
`heart/checks/test_run.py:36` resolves `HEART_STATE_DIR` at import, `:231` writes to it
unconditionally. A 10,234-byte real state file became this 251-byte fixture:

    {"cloud_url": "U", "failed": 0, "parked_stale": [], "parked_stale_count": 0, "passed": 0,
     "per_project": {}, "ready": true, "run_label": "cloud#9", "ts": "2026-06-25T00:00:00Z"}

Measured effect of re-aggregating with the stub in place:

    before:  yellow score 60  — "workspace validation not passing (3 failed, 2026-07-09T09-48-30Z)"
                              — "58 stale parked script(s)"
    after:   stale  score 70  — "test run stale (20d old)"

Both real reasons **disappear**. It is **not** a fake-GREEN today — the fixture's hardcoded `ts`
reads 20d old, past `TEST_STALE_DAYS=10`, so it degrades to STALE and still blocks. **That is luck,
not design.** A fixture with a fresh `ts` clears the leg outright. Recovery on the day was possible
only because `state.json` still held a pre-clobber copy; **a `tick` between clobber and restore would
have destroyed the evidence permanently.** Filed: `draft/bug/pyautoheart/test_suite_clobbers_live_heart_state.md`.

### 3. Evidence compared against an incomparable surface — the `mode=smoke` re-run (OPEN)

The prompt that started this work asserted the `test_run` leg's 3 failures were "already disproven by
the fresh release run (543p/0f)", making the leg an **ops re-run**. Both halves of that are unsupported:

- `mode=release` **skips notebook execution** and is scoped to the autofit/autogalaxy/autolens
  workspaces + `_test` siblings. It could never have disproven a HowTo* or notebook failure — those
  are never executed on that path. A green release run is **not** evidence about the smoke surface.
- The re-run (run `29418019889`, 13:09→13:33Z) came back **`ready=False`, 1036 passed / 145 skipped /
  30 failed**. Against the leg's 2026-07-09 record (620 passed / 3 failed):

  | project | 2026-07-09 (leg) | 2026-07-15 (new) |
  |---|---|---|
  | autofit | p26/f0 | p52/f2 |
  | autogalaxy | p108/f0 | p212/f4 |
  | autolens | p226/f0 | p459/f5 |
  | howtolens | p38/f0 | p67/f9 |
  | euclid | p5/f0 | **absent** |
  | **totals** | **620p/3f** | **1036p/30f** |

  Every project's pass count roughly **doubled** and `euclid` vanished. **This is not "27 new
  regressions" — it is a different surface.** Working hypothesis (**unverified — settle it**): the
  old run executed scripts only, the new one scripts *and* notebooks, since each tutorial exists as
  both `.py` and `.ipynb`. **Nobody knows what the leg's "3 failed" was measuring.** A gate whose
  history cannot be compared across runs is not a trend, it is a number.

- Root cause of the sample inspected — **one class, not 30 bugs**:
  `FileNotFoundError: 'dataset/imaging/simple__no_lens_light/data.fits'` (and
  `simple__no_lens_light__mass_sis`). HowToLens commits **zero** dataset files
  (`git ls-files 'dataset/*'` → 0; `.gitignore:9` is `dataset/`), so its tutorials must simulate at
  runtime — and the data was not there. `tutorial_0_visualization` failed as **both** `.py` and
  `.ipynb`, so this is **not** notebook infrastructure. 20 of the 30 failures are `.ipynb`.

  **Unestablished, and the obvious lead:** whether this is downstream of `PyAutoBuild#150` dropping
  `git add -f dataset/` (the simulated-dataset leak fix, #126) — the same change that caused the
  2026-07-15 release abort and that `draft/research/pyautobuild/pre_build_git_add_failure_audit.md`
  is already chartered to audit. **Do not assume the link. Establish it or kill it.** If releases
  were historically force-committing simulated datasets into workspaces, then removing that (rightly)
  may have removed the data the smoke surface silently depended on — meaning the smoke gate was
  passing on artifacts a *release* put there, not on anything the repo guarantees.

### 4. The router that classifies this work is itself stale (OPEN, unfiled)

`bin/pyauto-brain feature draft/release/pyautoheart/<x>.md` parsed work-type=`draft`,
target=`release`, resolved **no repos**, and recommended "re-home as a research task". Its path parser
predates the Mind lifecycle split to `draft/ → active/ → complete/` (Mind#71, closed 2026-07-13). It
will misroute **every prompt filed since that split**. It was overridden by hand. Note this is the
second Brain-agent misroute recorded in `autonomy_log.md` in two days (the arXiv digest task records
another).

## The design questions worth more than the audit

1. **What is Heart's verdict worth today?** Three of three legs examined had unreliable evidence
   underneath. The nightly's standing grant (`AUTONOMY.md`) is explicitly conditioned on
   Heart-GREEN with **no force input** — the gate is load-bearing for unattended live PyPI releases.
   Is the correct conclusion "the gate held" (it never went GREEN, so nothing shipped wrongly) or
   "the gate held **by luck**, and its inputs are not trustworthy enough to authorise the grant"?
   **Argue it, don't assert it.**

2. **Is a leg that cannot go GREEN a gate, or a permanently-lit warning light?** The install leg was
   structurally incapable of being satisfied and nobody noticed for months, because "not run" is
   indistinguishable from "not run *yet*". How many other legs are in that state **right now**?
   Enumerate them: for each leg, what exact artifact satisfies it, who writes it, and has that writer
   **ever actually run**? (cf. "merged is not the same as ever ran" — the lesson of the 07-15 release.)

3. **Should Heart's state dir be writable by anything except a check?** Finding 2 exists because a
   *global* path is resolved at import and written from library code that tests call directly. Prefer
   deleting the trap to documenting it: if `run()` returned its summary and only the CLI persisted,
   the tests could not pollute anything because there would be nothing to pollute.

4. **What does the `test_run` leg actually measure, and is it comparable across runs?** If the smoke
   surface can silently double between runs, "3 failed → 30 failed" is not a regression signal. A
   gate needs a stable denominator. Does one exist? Should the report record its own surface
   definition so two runs can be compared at all?

5. **Does the smoke surface depend on artifacts a release put there?** If finding 3's dataset absence
   traces to #150, then the smoke gate was green because releases were leaking datasets into repos —
   i.e. the gate was validating a state the repo never guarantees, and fixing the leak exposed it.
   That would make this a *pre-existing* falsehood newly revealed, not a regression. **The distinction
   changes the entire remediation.**

## Trust nothing here

Written by the agent that made today's mistakes. Several of its conclusions **were wrong that day**
and were caught only by re-checking — the same shape as the 2026-07-15 release errors:

- **"This could fake a GREEN verdict."** — **false.** Measured, the stub degrades to STALE (score 70)
  because its `ts` is 20d old; it still blocks. Asserted before measuring; the measurement corrected it.
- **"The release run's 543p/0f disproves the leg's 3 failures."** — inherited from the prompt and
  **repeated to the human before checking**. `mode=release` never runs notebooks or HowTo*. Caught
  only after dispatching the re-run.
- **"Line 245 is the simulator ordering logic."** — **false.** It is a `nufftax` dependency comment.
  Skim-matched a keyword and called it a finding.
- **"3 failed → 30 failed is a regression."** — **false**, or at least unsupported: the surfaces differ.

Treat this document as a lead sheet, not a source of truth. **Every number above is re-measurable —
re-measure it.**

## What to produce

1. **A per-leg evidence map.** For every leg in `heart/readiness.py`: the exact artifact that
   satisfies it, the writer, the last time that writer actually ran, and whether the leg is currently
   *satisfiable at all*. Measured (a per-leg matrix beats prose), not reasoned.
2. **An answer to design question 1** — what the verdict is worth today, with evidence, and whether
   the nightly's standing grant should stand unchanged, be narrowed, or be paused pending the chain
   being fixed. This is the deliverable the human most needs.
3. **A verdict on finding 3's root cause** — is the dataset absence downstream of #150, and is the
   smoke gate's history comparable across runs? Settle both; they are currently open.
4. **What you rejected and why**, including: is an autouse `conftest.py` fixture the right fix for
   finding 2, or does it hide the design smell?
5. **Open decisions for the human**, separated from what you are confident about.

## Method

- **Run things.** Everything here is cheap to re-measure and expensive to be wrong about.
- **Prove no-ops and absences empirically.** "Provably inert" and "already disproven" both preceded
  being wrong today.
- **Reproduce against the real repos**, never a synthetic model of a `.gitignore`. This exact
  shortcut failed on 2026-07-15 (see the pre_build brief's "Trust nothing here").
- **Adversarial pass before concluding:** for each load-bearing claim — what would have to be true for
  this to be false, and have I looked?
- **Prefer deleting the trap to hardening it.**

## Constraints

- **Do not run PyAutoHeart's test suite against a live `~/.pyauto-heart`** until finding 2 is fixed —
  it destroys real state (that is how it was found). Sandbox `HEART_STATE_DIR`.
- **Never dispatch `release.yml`.** Its `rehearsal` input defaults to `false` = a real PyPI release.
  `workspace-validation.yml mode=smoke` is safe (no publish); `mode=release` rehearses to TestPyPI.
- **Do not "fix" a leg by re-running until it goes green.** If a re-run changes the verdict, that is a
  finding about the evidence, not a remediation.
- Release work is `human-required` (`AUTONOMY.md:56`). This brief is research: **produce judgment, not
  a merged fix.** Design first; plan approval before any implementation.

## Related

- `draft/research/pyautobuild/pre_build_git_add_failure_audit.md` — same failure shape (a `git add`
  whose failure is handled wrongly in one of two opposite directions), same file that aborted the
  07-15 release. **Findings 3 and 5 likely intersect it; read it first.**
- `draft/bug/pyautoheart/test_suite_clobbers_live_heart_state.md` — finding 2, filed separately.
- `draft/research/pyautobrain/agent_failure_modes_structural_mitigations.md` — finding 4 and the
  "trust nothing here" list are more data for it.

<!-- filed 2026-07-15 from the wire-verify-install-leg session (PyAutoHeart#76/PR#77 merged e43a3a9) -->
