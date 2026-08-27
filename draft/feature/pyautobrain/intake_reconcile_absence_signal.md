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
