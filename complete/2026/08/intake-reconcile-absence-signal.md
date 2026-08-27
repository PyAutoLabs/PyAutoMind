- issue: none — filed as a PyAutoMind prompt on 2026-08-27 by the session that
  re-picked `smoke_install_stale_jax_pin.md`, four days after it had shipped.
  Prompt: `draft/feature/pyautobrain/intake_reconcile_absence_signal.md`
  (retired by this record).
- shipped: 2026-08-27 — PyAutoBrain#307 (main 3b4eedf7). Shipped in one PR with
  its sibling `reconcile-duplicate-prompt-signal`: both add a signal to the same
  scan, and implementing them together was cheaper than either alone.
- classification: feature (PyAutoBrain) — a new leg on the `intake reconcile`
  ranker, opt-in behind `--repo`.
- summary: leg 3 tested PRESENCE — "the prompt names things that exist
  upstream" — and is structurally blind to a task that shipped leaving no
  Mind-side trace while the files it names still exist. Leg 4 inverts it: a
  literal line the prompt QUOTES that is gone from a file it names. On the
  motivating case both existing guards passed a prompt that had shipped
  (`lifecycle.py check` has no invariant for a prompt that was never `active/`;
  `reconcile --repo` found 0 suspects of 132), and the new leg flags it.

## The filters, and what they cost to find

The first cut had three filters and passed its tests. Run against the LIVE
backlog — 134 prompts read at the workspace-test repo — it produced **six hits,
all six false**, and the loudest was the most wrong: a prompt quoting 23 lines
of a seed finder it wanted *written* scored 101.0, above every true positive.

Two more filters took that to 0 while the retired prompt, restored into `draft/`
to reproduce, still fires:

- **The anchor must be corroborated.** At least one line the prompt quotes for
  that extension must still be PRESENT in the file it names. One present line
  proves the prompt is talking about this file, in this checkout; only then does
  a sibling line's absence mean something happened. Kills proposed code, which
  is absent because it has never existed.
- **The prompt must mention the repo being read.** A prompt read against a repo
  it is not about quotes lines absent by construction. This was the open
  question the filing prompt raised — the `Repos:` header had the answer all
  along, while `--repo` had to be told the target by hand.

The three original filters stand: an explicit source-language fence (a traceback
goes in a bare fence and is absent from every repo by construction), a named file
that exists upstream, and absence from the whole checkout so a moved line reads
as the refactor it is.

## Key traps / findings

- **Passing tests are not a measurement.** The three-filter cut was green and
  wrong. What found the defect was pointing it at the real backlog and reading
  all six hits — and the two worst were structural, not tunable. A ranker can
  only be judged against the corpus it will run on.
- **Two of the positive fixtures were wrong the same way the false positives
  were.** They quoted only absent lines, which the real prompt never did — it
  quoted two, one still present. Fixtures invented to exercise a signal will
  drift toward the signal's happy path unless they are built from the real case.
- **The loudest output was the most wrong.** Score ordering is a claim about
  confidence; a leg whose top hit is its worst error is not merely noisy, it is
  actively misleading. That is why leg 4, like leg 3, feeds only
  `upstream_score` and can never reach a Mind-local band.
- **CI caught what no test could.** The tenant firewall rejected the first two
  commits: the new comments named a concrete satellite repo in `.py` files, and
  the framework organs must stay adoptable as a config-diff fork. Genericised
  rather than allowlisted — growing `FIREWALL_ALLOWLIST` means one more file an
  adopting fork must rewrite. The test file was already violating its own
  header, which promises every fixture is fictional.
- **A `\b` cannot match before a leading dot.** `_PATH_RE` silently truncated
  `.github/workflows/release.yml` to a path resolving against no file — and
  dot-directories are where CI recipes live, which is half of what these
  prompts are about. Found by a test, not by reading.

## Follow-ups

- **Scheduling was scoped out and stays out.** The filing prompt asked whether
  anything should run this on a schedule. Reconcile is on-demand and read-only
  by design, and the answer is not obvious enough to settle here: `--repo` is
  the only network access in PyAutoBrain, and putting it on a timer would make
  it the first scheduled one. Left for a prompt of its own if the drift recurs.
- **Not in scope, as the prompt said:** having the ship skills record Mind state
  is the upstream cause. This leg detects the drift that already exists.

## Original prompt

# `intake reconcile` cannot see a prompt that shipped with no Mind-side trace

Type: feature
Target: pyautobrain
Repos:
- @PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-27

Add the inverted signal: a prompt quoting a literal line that is GONE upstream.

Found 2026-08-27 by re-picking draft/maintenance/ci/smoke_install_stale_jax_pin.md
via /start_dev. The prompt had shipped four days earlier
(autolens_workspace_test#266, closed by PR #268, a97f052, merged 2026-08-23) and
had never been retired: no active.md entry, no active/ move, no complete/ record.
It kept rendering on dashboard.md as pickable backlog with a live /start_dev chip,
which is exactly how it got picked again.

Nothing detects this class today. Two guards were checked directly against the
restored prompt:

1. `lifecycle.py check` — its invariant is that no active.md slug has a record.
   A task that skips Mind state entirely is in NEITHER place, so the check passes.
2. `pyauto-brain intake reconcile` — every signal it emits (`referenced`,
   `record-says-shipped`, `shared-identifiers`, `rare-topic-overlap`,
   `stale-status`) needs a Mind-side trace. With the prompt restored,
   `intake reconcile maintenance/ci` did not flag it. Neither did
   `intake reconcile maintenance/ci --repo autolens_workspace_test`, pointed
   straight at the right repo reading its live source: **0 suspects of 132
   scanned**.

## Why --repo missed it

`--repo` tests PRESENCE: "the prompt NAMES things that exist upstream". This
prompt names `smoke_install.sh`, which does still exist — so presence tells you
nothing.

The defect this prompt described was an ABSENCE. It quoted a literal line:

```bash
pip install "jax<0.7" "jaxlib<0.7"
```

That line is gone from upstream. A backlog prompt quoting a literal code line
that no longer exists in the file it names is close to a proof the work shipped —
far stronger than the presence signal already implemented, and it fires precisely
in the no-Mind-side-trace case the existing signals are blind to.

## Suggested scope

1. Add an absence signal to `intake reconcile --repo`: for each fenced code block
   or backticked line in the prompt that looks like source (not prose), check
   whether it still occurs in the file the prompt names. Quoted-and-now-absent
   ranks higher than any current signal.
2. Keep it in the existing `needs-review` band and keep retirement human — the
   same guard rail reconcile already states. A quoted line can vanish for reasons
   other than the prompt shipping (an unrelated refactor, a reworded quote), so
   this ranks for review, it does not retire.
3. Consider whether the prompt's `Repos:` header should drive the upstream target
   automatically. Here the target FOLDER was `ci` (not a repo, so `--repo` is
   refused and must be passed by hand) while the header named
   `@autolens_workspace_test`. The header had the answer the flag had to be told.
4. Decide whether anything should run this on a schedule. Today reconcile is
   on-demand and read-only, so the drift persists silently until someone re-picks
   the prompt — which is a working detector, just an expensive one.

Not in scope: closing the loop by having the ship skills record Mind state. That
is the upstream cause and deserves its own prompt if it is worth chasing; this one
is about detecting the drift that already exists.

<!-- Sizing: the intake classifier derived large (8) and resolved the target as
     workspaces/autolens_workspace_test — both wrong, and wrong the same way the
     retired prompt warned about: it keyed on the evidence repo, which this prompt
     quotes heavily, rather than on where the code lives. `reconcile` is
     PyAutoBrain/agents/conductors/intake/_intake.py. Corrected to
     pyautobrain/medium by hand: the change is one added signal inside an existing
     scan, and the prompt is long because the evidence is. -->

<!-- Evidence for the "0 suspects" claim was produced by restoring the retired
     prompt into draft/ and re-running both reconcile modes against it, then
     removing it again. Reproduce that way, not from a fresh backlog. -->
