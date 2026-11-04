# Record the `glance` Shadow-window ruling in AUTONOMY.md — grant narrowed, after the spot audit

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Issued: 2026-11-04
Filed: 2026-11-03
Closes-when: the human returns verdicts on /mnt/c/Users/Jammy/Workspace/Science/scratch/shadow_window_audit_2026-11-03/audit.md
Consequence: judge
Witness: AUTONOMY.md carries a dated section recording the human's ruling on the tier-`glance` Shadow window (69/20, all stage-1 `merged-unchanged`) with its revert condition, and a doctrine test pins (i) a witness that is not PASS (none, n/a, partial, waived) never auto-merges, (ii) the audit's outcome, and (iii) unattended (watcher) `glance` merges count in a separate stage-2 sub-window; `autonomy_log.md`'s Shadow header states the ruling; `pytest PyAutoBrain/tests -q` green
Review-minutes: 10
Unattended: never
Lane: any

Decided with the human 2026-11-03 (recommendation accepted): **grant `glance`, narrowed, after
a spot audit; start a separate stage-2 count for unattended merges.**

The pre-registered rule (`complete/2026/09/prm-shadow-row-notify-tier.md`, "The decision rule,
pre-registered"): grant if no `merged-after-substantive-change` / `not-merged` rows; grant
narrowed if every case falls in one identifiable sub-class; refuse otherwise. The window stood
at **69 counted rows (target 20), all `merged-unchanged`, all stage 1**, about 21 with no
independent review, most under a non-GREEN Heart.

Steps:

1. **Spot audit (human).** Eight rows were picked across every risk class, in
   `Science/scratch/shadow_window_audit_2026-11-03/audit.md`. The human writes `ok` or
   `minded — <why>` per row. Any `minded` row → amend that Shadow row to
   `merged-after-substantive-change` and let it define the narrowed-out sub-class.
2. **Record the ruling in AUTONOMY.md**, as a dated section after "Merge authority follows
   Consequence — 2026-10-02":
   - `glance` is confirmed for **in-turn** auto-merge (the shipping session, human nearby);
   - **narrowing (both already proposed):** a witness that is not PASS — none, n/a, partial
     or waived — means human `/prm`; and, if the audit finds tier drift (rows 3, 4 and 6 are
     public helpers or APIs and a library return-value change), anything touching a public API,
     a default or a library return value is `judge` whatever the declared tier;
   - **unattended `glance`** (watcher-started close-outs, AUTONOMY "Shift briefs and unattended
     `glance`") opens its own **stage-2 sub-window**: its first 10 merges each need the
     independent different-model adversary leg actually run, are counted apart from the
     stage-1 rows, and gate that sub-rule;
   - the revert condition: any `reverted` row still demotes `glance` immediately.
3. **Ledger accuracy:** a counted row whose merge was a human-typed `/prm` (row 8 suggests
   `fixed-model-json`, PyAutoFit#1708) is re-marked as not an auto-merge, and the count fixed.
4. **autonomy_log.md**: the Shadow header states the ruling and opens the stage-2 sub-window
   table.

Related: the autonomous-orchestrators epic depends on this for unattended merges; its pilot
(phase 4) must not auto-merge unattended until step 2's stage-2 sub-window exists.

<!-- filed by hand 2026-11-03 after the human accepted the Shadow-window recommendation; headers mirror intake's -->
