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
