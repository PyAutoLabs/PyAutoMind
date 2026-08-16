# A crashed run poisons the next run of the same name — silently, as a clean result

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Filed 2026-08-16. Split out of
`draft/feature/autofit/prior_support_clipper.md` ("Two incidental bugs found
while investigating — do not lose these", item 2), which asked for it to be
filed separately once confirmed. It is confirmed — see Grounding.

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
