The health conductor had no STALE branch, so a stale-only readiness verdict was
mis-reported as UNKNOWN. The card printed `adopted verdict = stale` with a score,
then the recommendation printed "UNKNOWN — could not obtain a verdict from the
vitals faculty", the triage counts read `0 blocker(s) · 0 real warning(s) ·
0 expected first-run gap(s)`, and the script exited 4 — the same code as "Heart
unreachable". PyAutoHeart makes STALE a first-class freshness tier and
`AUTONOMY.md` leg 4 treats it as PASSING the dev-ship gate, so collapsing it onto
unknown left a machine caller unable to tell an evidence gap from a dead sensor.

**PR:** PyAutoBrain#199 (issue #198) — merged 2026-08-05, branch
`claude/health-conductor-stale-verdict-6ve1sl`.

## What changed

Three sites, all in `agents/conductors/health/health.sh`:

- **Triage item classifier** — walked only `(red, yellow)`, so stale reasons never
  became items. Now walks `stale_reasons` too and, mirroring the pre-existing
  "severity wins over the keyword class" rule for red, forces them to a new
  `evidence-gap` kind.
- **Recommendation chain** — a STALE branch ahead of the baseline-gap one, naming
  the top evidence gap and preferring the release-validation gap when present.
- **`_exit_code_for`** — STALE maps to 6.

Docs updated in the same diff: the header's exit-code table and
`agents/conductors/health/AGENTS.md` (its second copy of that table, the triage
taxonomy "three kinds" → "four", the recommended-action table).

## Findings worth keeping

- **The exit code is 6, not the free slot 1 — and the reason generalises.** `1` is
  the shell's own generic failure (a missing `_common.sh`, a failed `readlink`),
  and STALE is a *passing* tier for the ship gate, so a crash exiting 1 would have
  been readable as a pass. Fail-safe direction: an accidental exit must never
  resemble a passing verdict. This is the same reasoning the file already applied
  to usage errors ("exits 5 — kept distinct from the verdict codes so misuse is
  never read as a real YELLOW"). Full ladder now: 0 green / 2 yellow / 3 red /
  4 unknown / 5 usage / 6 stale.
- **A stale reason is NOT a baseline gap.** The tempting one-line fix — file stale
  reasons into the existing `baseline-gap` kind — is wrong: that bucket renders as
  "accept, not action items", while a stale reason's whole point is that re-running
  the named check IS the action. Hence the new `evidence-gap` kind, and
  `blocks_green: true` on it.
- **Refresh commands must be grounded like fix topics.** The conductor already
  refused to invent `pyauto-heart fix` topics; the same discipline now governs
  refresh entry points. Real ones only — `pyauto-brain release validate` (the hard
  gate, delegated because the release conductor owns the MCP boundary),
  `pyauto-heart verify_install`, `pyauto-heart tick` for anything the <30s tick
  measures. `test_run` and `url_check` have no known entry point, so they get
  `command: None` and prose naming the check.
- **Heart needed no change.** `heart/readiness.py` already computed and exported
  `stale_reasons` correctly; this was purely a Brain-side consumer bug. Worth
  remembering when a tier is added to Heart: the consumers are the risk surface,
  not the producer.

## Validation

`tests/test_health_conductor.py` (new, 18 tests) stubs `pyauto-heart` on `PATH`
and drives the conductor end-to-end through the vitals faculty. It pins the three
fixed sites, that every verdict maps to a distinct exit code, that the documented
tables do not drift from `_exit_code_for`, that refresh commands are never
invented, and — as regression guards — that red still dominates a stale reason and
that a Heart with no `stale_reasons` key behaves exactly as before (the tier is
additive). Full suite 222 passed (204 pre-existing + 18); CI green on 3.12 + 3.13.

## Follow-up filed as a finding, not folded in

`agents/faculties/vitals/AGENTS.md` has the same class of omission: step 1
documents the tier correctly, but step 3 ("Reason about significance") groups only
Blocking/Warnings and step 4 ("Determine overall readiness") reads "any
`red_reasons` → RED, else any `yellow_reasons` → YELLOW, else GREEN" — no stale
rung, in the very faculty this conductor consults. Docs-only; kept separate under
"one prompt = one task".

## Environment

Cloud session (web-github): no worktree, no `gh` CLI. Worked in the canonical
`/home/user/PyAutoBrain` checkout on the mandated branch; issue and PR via the
GitHub MCP surface.

## Original prompt

# Bug: the health conductor mis-reports a STALE verdict as UNKNOWN.

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Bug: the health conductor mis-reports a STALE verdict as UNKNOWN. In PyAutoBrain agents/conductors/health/health.sh the recommendation chain branches on green / blockers / real-warnings / (gaps or yellow) and otherwise falls through to an UNKNOWN branch, and _exit_code_for maps only green/yellow/red with a catch-all 4. When PyAutoHeart returns STALE the card correctly prints 'adopted verdict = stale' with a score, then the recommendation incorrectly prints 'UNKNOWN - could not obtain a verdict from the vitals faculty' and the script exits 4. The triage item classifier only walks the red and yellow reason lists, so stale reasons are dropped and the counts wrongly read 0 blockers / 0 warnings / 0 gaps. PyAutoHeart AGENTS.md makes STALE a first-class freshness tier that the dev-ship gate treats as passing, so a caller cannot distinguish 'Heart says STALE' from 'Heart unreachable'. Reproduced on a live health run 2026-08-05.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
