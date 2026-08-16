- library-prs: https://github.com/PyAutoLabs/PyAutoFit/pull/1480
- merge-commits: PyAutoFit `5c9244bc1d0c000804899a0378dcb0187f9716af` (2026-08-16)
- issue: none — split out of the prior-support Clipper prompt's "do not lose these"
- summary: A run interrupted while writing output left a half-written JSON file,
  and every later run of that search name died on it — from inside an *optional*
  sanity check — until the output directory was deleted by hand. Fixed in three
  legs: `open_atomic` (temp file + `os.replace`) for `save_json` and
  `save_search_internal`; `Fitness.check_log_likelihood` treating a corrupt
  summary as absent, with a warning; and the multi-start resume guard widened so
  corrupt state falls into the fresh-start branch below it.
- validation: 9 new tests; full suite 1800 passed / 4 skipped / 1 failed
  (pre-existing). Merged result with #1478 + #1479: 1819 passed.
- release: not performed; merged PR remains in the pending-release queue.

## The one fact behind all three legs

**`json.JSONDecodeError` subclasses `ValueError`.** So it is neither a
`FileNotFoundError`, a `TypeError` nor a `KeyError`, and it fell through every
guard on the resume path — `check_log_likelihood`'s `except FileNotFoundError`
and the multi-start `except (FileNotFoundError, TypeError, KeyError)` alike.
Asserted directly in a test so it cannot quietly stop being true.

## CORRECTION to the filed prompt — reproduce before you fix

The prompt described the poisoned rerun as "a 4-second no-op run that reads as a
clean result (zero deaths, because zero steps)". **That did not reproduce.**

What reproduces against `main`, using the real trigger (a float32 killing
`save_json` at the end of a successful fit):

```
run 1: TypeError: Object of type float32 is not JSON serializable
run 2: JSONDecodeError: Expecting value: line 1 column 13 (char 12)
```

A hard crash naming no file and offering no remedy, on *every* rerun of that
name. The silent-no-op variant presumably needs a **surviving**
`search_internal`, whose restored `total_steps` short-circuits the loop — but
the crash path deletes that directory first. Same root cause, and the fix covers
both paths, but only the crash is evidenced. **Do not cite the no-op as
observed.**

Also worth knowing: LBFGS does *not* poison. It simply refits and overwrites.
The hazard is specific to searches that read prior output while resuming.

## Legs, and why each is separate

1. **Atomicity.** `open(path, "w+")` truncates first and writes second, so any
   failure destroys the file that was there. `open_atomic` catches
   `BaseException`, not `Exception` — a `KeyboardInterrupt` mid-write leaves
   identical debris. Applied to `save_search_internal` too, which matters more:
   that is what a resumed run restores its step count and counters from.
2. **Recovery.** `check_log_likelihood` already returned early on a *missing*
   summary; a *corrupt* one is the same situation, since there is no
   trustworthy old likelihood either way. It warns rather than staying silent —
   an unreadable file is a real event, unlike a missing one.
3. **The resume guard.** Found by audit, not by the prompt: the same narrow
   except-tuple meant a corrupt `search_internal` raised instead of falling into
   the fresh-start branch directly beneath it.

Legs 1 and 2 are independent by design — 1 stops the debris being created, 2
recovers from debris created by older versions, killed processes or a full disk.

## Trap in testing this

The end-to-end regression test must assert the second run actually **takes the
resume path**. Without that, a run short-circuited as already-complete
(`is_complete` -> `result_via_completed_fit`) passes the test while asserting
nothing. The `.completed` marker also is not found by `rglob(".completed")` under
the test config — use `paths._has_completed_path`.

## Original prompt

# A crashed run poisons the next run of the same name — silently, as a clean result

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Filed 2026-08-16. Split out of the prior-support Clipper prompt's "Two incidental
bugs found while investigating — do not lose these" section (item 2), which asked
for it to be filed separately once confirmed. It is confirmed — see Grounding.
That prompt has since shipped as PyAutoFit#1477; its record is
`complete/2026/08/prior-support-clipper.md`. **This bug was not fixed by it** —
verified still present at `1f4b66a`, the merge commit itself.

> **IN FLIGHT — PyAutoFit#1480 open 2026-08-16**, branch
> `claude/autofit-crashed-run-poisons-resume`. Advance to `complete/` on merge.
>
> **CORRECTION, from reproducing it.** This prompt says the poisoned rerun is
> "a 4-second no-op run that reads as a clean result". **That did not
> reproduce.** What reproduces against `main` is a hard crash:
> `JSONDecodeError: Expecting value: line 1 column 13 (char 12)`, naming no
> file and offering no remedy, on every rerun of that search name. The
> silent-no-op variant presumably needs a *surviving* `search_internal`, whose
> restored `total_steps` short-circuits the loop — the crash path deletes it
> first. Same root cause, and the fix covers both, but only the crash is
> evidenced. Do not cite the no-op as observed.
>
> Fixed in three legs, the third of which the prompt below only hinted at:
> (1) `open_atomic` — temp file plus `os.replace` — used by `save_json` **and**
> `save_search_internal`; (2) `check_log_likelihood` treats a corrupt summary
> as absent, as it already did for a missing one, warning rather than aborting
> the run from inside an optional check; (3) the multi-start resume guard
> widened so corrupt state falls into the fresh-start branch below it.
>
> 9 new tests. Full suite 1800 passed / 4 skipped / 1 failed (pre-existing).

## The defect

A run that dies during output leaves a **truncated JSON file** on disk and no
`.completed` marker. The next search with the same `name` then resumes into that
wreckage and produces a result that *looks clean*.

The chain, each link verified against `main`:

1. `directory.py:79` opens the output file with `open_(..., "w+")`, which
   **truncates first**. If `json.dump` then fails partway — as it does on
   numpy `float32`, see `draft/bug/autofit/save_json_numpy_scalar_typeerror.md`
   — a partial file is left where a valid one was. There is no
   write-to-temp-then-rename, so the write is **not atomic**.
2. `DirectoryPaths.is_complete` (`directory.py:180`) tests only
   `self._has_completed_path.exists()`. The crash happened before that marker
   was written, so `is_complete` is `False` and `abstract_search.py:582`
   dispatches to `start_resume_fit` rather than to `result_via_completed_fit`.
3. The resume path reads the truncated file — `load_samples_summary`
   (`directory.py:334`) via `load_json`, `load_samples_info`
   (`directory.py:343`) via a bare `json.load` — and raises
   `json.JSONDecodeError`.
4. **`JSONDecodeError` subclasses `ValueError`.** The multi-start resume guard at
   `@PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:720`
   catches `(FileNotFoundError, TypeError, KeyError)` — so a corrupt previous
   output does **not** fall through to the "no previous samples found" fresh
   start branch. That branch is what should have run.

## Why this is the bad kind of bug

The observed symptom was a **4-second no-op run that read as a clean result** —
zero lane deaths, because zero steps were taken. Every counter said the cell was
healthy. A search that does nothing and a search that finds nothing wrong are
indistinguishable in the output, so this silently corrupts measurement.

This is a new instance of the cached-result hazard already recorded in
`complete/2026/08/multistart-nan-step-diagnostics.md` — same class, new entry
point. It cost real time during autolens_profiling#128 and is written into
`draft/feature/autofit/clipper_validation_campaign.md` as a trap that campaign
must work around. Fixing it here removes the need for that workaround.

## The fix — two independent legs, both worth landing

1. **Make the write atomic.** Serialise to a temp file in the same directory and
   `os.replace` it into place. A crash then leaves either the previous valid
   file or nothing — never a truncated one. This is the leg that removes the
   whole class, not just the numpy trigger.
2. **Make a corrupt prior output loud, or treat it as absent.** Decide which,
   and state it: either widen the resume guard so an undecodable previous
   output falls through to the fresh-start branch (cheap, but discards prior
   work silently), or fail fast with a message naming the offending file and
   telling the user to delete `output/<name>/`. **Do not leave the current
   third behaviour**, where it neither resumes nor restarts but reports success.

Leg 2 is a judgement call about resume semantics, which is why this is
`supervised` rather than `safe`. Note the guard at `search.py:720` is
multi-start-specific — audit whether the other searches' resume paths have the
same narrow-except shape before fixing only this one.

## Verify

- Write a deliberately truncated `samples_summary.json` into an otherwise valid
  output directory with no `.completed` marker, then run the same search again:
  it must either restart cleanly or raise a message naming the file — and must
  **not** return a zero-step result reported as complete.
- Assert the recorded step count equals the requested `n_steps` in that test;
  that assertion is precisely what would have caught this in the field.
- Kill a run mid-`save_json` (or monkeypatch it to raise) and confirm the
  previously-written file on disk is still valid JSON — the atomicity leg.
- `ValueError`/`JSONDecodeError` is covered explicitly by a test, since the
  inheritance is the thing that made the existing guard miss it.

<!-- Grounding: verified against PyAutoFit main at 1f4b66a93 (shallow clone,
     2026-08-16). Read directory.py:66-80 (open_ "w+" truncation, no atomic
     rename), directory.py:180 (is_complete = marker file only),
     directory.py:334/343 (load_samples_summary / load_samples_info JSON reads),
     abstract_search.py:582 (is_complete dispatch), and
     multi_start_gradient/search.py:692-746 (resume try/except and the
     fresh-start fallback). Confirmed json.JSONDecodeError.__mro__ includes
     ValueError and not TypeError/KeyError. Symptom observed during the Clipper
     prototype, autolens_profiling#128. -->
