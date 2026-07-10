# Nightly driver: failed commit fetch is indistinguishable from a quiet night

Type: bug
Target: pyautobrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

## What happened (2026-07-10, first scheduled run of the armed nightly)

The 06:05 scheduled `Nightly Release` run in PyAutoBrain skipped with
"💤 no qualifying activity" — but 2026-07-09 was one of the most active nights on
record (7 merges; replaying the gate on the real window commits for PyAutoLens
alone gives `activity: PyAutoLens (25), active: True`). The release that should
have shipped did not.

Root cause chain:

1. **PyAutoBrain has no Actions secrets at all** — `nightly-release.yml` sets
   `GH_TOKEN: ${{ secrets.PAT_PYAUTOLABS }}` and
   `PYAUTO_RELEASE_WEBHOOK_URL: ${{ secrets.PYAUTO_RELEASE_WEBHOOK_URL }}`, both
   empty (secrets live in PyAutoBuild, never mirrored to PyAutoBrain; the arming
   day's testing evidently exercised the Build side only). Every `gh api` call
   failed instantly — 11 repo fetches completed in 0.4 s total.
2. **`nightly.sh` line ~166** turns any fetch failure into an empty commit list:
   `gh api ... 2>/dev/null || echo '[]'` — so a driver that cannot see GitHub
   reads as "the organism was quiet". The 💤 skip path then *advances the
   anchor* (or would, when the variable write works), silently swallowing the
   missed night.
3. Secondary symptoms in the same run, same cause: "PYAUTO_RELEASE_WEBHOOK_URL
   not set — outcome NOT posted to Slack" (the skip never reached Slack; the
   morning digest showed nothing wrong) and "could not persist
   NIGHTLY_LAST_WINDOW_END".

## Second hole (found by the 2026-07-10 08:03 dry-run, WITH a working token)

With secrets set, a `dry_run: true` dispatch still skipped: the anchor variable
`NIGHTLY_LAST_WINDOW_END` did not exist yet, and the anchor read
(`anchor="$(gh api .../variables/$ANCHOR_VAR --jq .value 2>/dev/null || true)"`)
captured the **404 JSON error body on stdout** instead of empty — so the
`[[ -z "$anchor" ]]` 24h-fallback never fired and the commits fetch ran with
`since={"message":"Not Found",...}` → all fetches failed → `[]` → 💤 again.
Worse, the skip path then *persisted* `WINDOW_END` as the new anchor, silently
shrinking the next window past the missed activity (manually reset to
2026-07-09T06:05:39Z on 2026-07-10). Fix: validate the anchor against
`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$` and fall back to 24h on any
mismatch; and never advance the anchor on a night whose fetches errored.

## Fix

- **Human/config leg (not code):** set the two secrets on PyAutoBrain
  (`gh secret set PAT_PYAUTOLABS --repo PyAutoLabs/PyAutoBrain`, same for
  `PYAUTO_RELEASE_WEBHOOK_URL`). Owner of the values: James.
- **Code leg (this task):** make fetch failure loud, per the design's own
  "skip loudly" doctrine:
  - In the fetch loop, distinguish "gh api failed" from "empty list returned".
    Simplest: drop `|| echo '[]'`, collect per-repo failures; if **all** repos
    fail (token dead / network gone) → `page "activity fetch failed (driver
    cannot see GitHub)"` and exit 1 — never the 💤 path, never advance the
    anchor. Partial failures → include "N repos unreadable" in the summary and
    proceed on what was read (a readable active repo still qualifies the night).
  - Cheap guard at step 0/1: if `gh api rate_limit` (or any trivial call) fails,
    page immediately — catches the tokenless case before any judgment.
  - Unit-test via `activity_gate.py` where possible (e.g. a `fetch_errors`
    count in the verdict JSON); the shell driver keeps only the plumbing.
- Consider a Heart check ("nightly driver could not see GitHub / skipped N
  consecutive nights while repos were active") as a follow-up, not this task.

## Cross-references

- `PyAutoBrain/agents/conductors/release/nightly.sh` (fetch loop, `page`, `advance_anchor`)
- `PyAutoBrain/agents/conductors/release/activity_gate.py` + `tests/test_activity_gate.py`
- `PyAutoBuild/docs/nightly_release_design.md` §4 (activity gate), §5 (paging)
- Run: https://github.com/PyAutoLabs/PyAutoBrain/actions/runs/29072930245
- Discovered during the docs-infrastructure work session (PyAutoLabs/PyAutoFit#1341) —
  unrelated to it: nothing in that work touched PyAutoBrain workflows or secrets.
