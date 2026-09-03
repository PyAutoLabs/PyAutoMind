## memory-queue-filing-gate
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/75 (closed, completed)
- completed: 2026-09-01
- library-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/76 (MERGED 2026-09-01T19:35:02Z, 23017555)
- batch: 2026-08-31-pm — member `memory-queue-filing-gate`, tier `notify`, 0 review-minutes; `--auto`, effective level supervised, shipped via **decide-and-flag** (`decision-taken` label). `batches/reviews/2026-08-31-pm.md` records `decision: UNREVIEWED`
- shipped: repaired the PyAutoMemory queue automation, hard-broken since dcd1e2c
  (2026-08-24) and stalling #69/#71/#72 since 2026-08-28 — added the PyAutoBrain sibling
  checkout to `queue_filing.yml`, made `queue_actions.yml`'s push retry conflict-proof
  (fetch + `reset --hard` + re-run the idempotent action script, instead of
  rebase-and-discard), and added an `if: failure()` report step so a failed run comments
  on its issue instead of failing silently.
- verified: `make validate` + full pytest 169 passed; no downstream (organ repo, no
  script surface). Review CLEAN over the ReviewSurface, retry semantics verified by a
  scratch-repo simulation of the #69 conflict. Adversary leg: witness HOLDS, FINDINGS with
  no blockers — findings 1 and 2 fixed in b5bc248.
- post-merge (checked 2026-09-03): labels were re-applied on #69 (`interests-add`) and
  #71/#72 (`queue-intake`), and `queue_filing.yml` has run **green** since the merge
  (2026-09-01T19:39:39Z and 2026-09-03T15:00Z) where it failed on 2026-08-31 and at
  19:39:38Z. **The witness's last leg is still unmet:** no filing PR has been opened, and
  #69/#71/#72 are all still open. The gate no longer fails; whether it now *files* is a
  separate, still-unanswered question and is the follow-up this record leaves behind.
- traps: adversary finding 3 — the same discarding retry lives in `knowledge_board.yml`
  and `arxiv_refs.yml` and was recorded as a follow-up, not fixed here.
- notes: **Ledger reconciliation 2026-09-03** — merged 2026-09-01, `active.md` row never
  retired. Written by `mind-post-cortex` phase 1 (PyAutoMind#389).

## Original prompt

# Repair the PyAutoMemory queue automation: filing gate, push retry, silent failures

Type: bug
Target: PyAutoMemory
Repos:
- PyAutoMemory
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: after the fix, re-applying `queue-intake` to #71 produces a green `queue_filing.yml` run that opens a filing PR — `gh run list --workflow queue_filing.yml` shows `success`, where every run since 2026-08-24 shows `failure`.
Review-minutes: 0
Unattended: ready
Issued: 2026-08-31

The dashboard's per-paper buttons file issues that are never acted on. Three
(#69, #71, #72) have sat open since 2026-08-28. All three were picked up — all
three workflow runs failed. Three distinct faults, each confirmed from the runs.

## 1. queue_filing.yml has been hard-broken since 2026-08-24

The `Gate the filing (validate + tests)` step runs `python -m pytest tests/ -q`
but never checks PyAutoBrain out beside the repo. Commit dcd1e2c ("The Memory
board joins the family look") moved the board theme into
`PyAutoBrain/board/_theme.py` and added the sibling checkout to `validate.yml`
and `knowledge_board.yml` — but not to `queue_filing.yml`. Every run since then
fails with 30 `tests/test_board.py` errors:

    RuntimeError: the shared board theme (PyAutoBrain/board/_theme.py) is not in
    reach — check PyAutoBrain out beside this repo or set PYAUTO_BRAIN

Runs 33201706952 (#71) and 33202478094 (#72) both died there *after* Claude had
already correctly filed the BibTeX entry and the wiki sources stub, so the
filing work is thrown away on every attempt. `make validate` passes; only the
pytest half of the gate fails. The last filing that ever worked was #50/PR#53 on
2026-08-21, three days before the regression.

Fix: add the `actions/checkout@v4` PyAutoBrain step (`repository:
PyAutoLabs/PyAutoBrain`, `path: PyAutoBrain`) before the gate, matching
`validate.yml`. Claude's own in-prompt step 5 tells it to run the same pytest and
"fix your own filing mistakes until both are green" — an environmental failure it
cannot fix, so the checkout must land before the claude-code-action step, not
just before the gate.

## 2. queue_actions.yml push retry cannot survive a conflicting concurrent commit

    for attempt in 1 2 3; do
      if git push; then exit 0; fi
      git pull --rebase origin main || exit 1
    done

On #69 (`interests-add`, run 33180301104) the push was rejected, the rebase hit a
content conflict in `arxiv-interests.md` against a sibling queue action, and the
`|| exit 1` discarded the commit entirely. Rebasing a stale commit is the wrong
shape here: the retry should fetch, `reset --hard origin/main`, re-run the action
script and re-commit. That is naturally idempotent given the
`already-there` / `already-gone` / `already-done` statuses the scripts already
return. Worth checking why the `concurrency: queue-actions` group did not
serialise the two runs (#68's job committed at 14:28:15 while #69's checkout
still pointed at 3c00470) — but the retry must be conflict-proof regardless.

## 3. queue_actions.yml never reports its own failures

`Close or report on the issue` is implicitly `if: success()`, so when the push
step dies the issue gets no comment at all. #69 has sat open and completely
silent — which is why the whole thing reads as "never swept up" rather than
"failed". `queue_filing.yml` already carries an `if: failure()` comment step;
`queue_actions.yml` needs the same.

## Close-out

Re-drive the three stuck issues (#69, #71, #72) by re-applying their labels, and
confirm each lands: #71/#72 open a filing PR, #69 moves its paper into the
reading queue and closes.

Witness: after the fix, re-applying `queue-intake` to #71 produces a green
`queue_filing.yml` run that opens a filing PR — `gh run list --workflow
queue_filing.yml` shows `success`, where every run since 2026-08-24 shows
`failure`.

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/edae1245-b1c8-4a05-9b7a-aa4a5128dae1/scratchpad/queue_prompt.md -->
