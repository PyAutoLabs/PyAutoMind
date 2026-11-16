# Nightly: write down the outcome, and open a bug task per failing script the same night

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-10
Epic: autonomous-orchestrators
Consequence: glance
Witness: (a) after a nightly, one machine-readable outcome line exists with class (shipped, partial, skipped or blocked), stage reached, version, the Hands and Heart run ids and any failing scripts with their error lines, and the class agrees with PyPI and the tags for that night; (b) the classifier replayed over the 123 nights in `evidence/nightly_ci/nightly_table_final.csv` reproduces that table's classes; (c) on a Stage 3 failure, one bug prompt per failing script is filed, with the quoted error line, and a second failure of the same script does not file a duplicate
Review-minutes: 15
Unattended: needs-slicing
Lane: any

Source: the ecosystem review of 2026-11-10, findings NIGHT-1 and NIGHT-2, both confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B8 and Appendix A. Data: `evidence/nightly_ci/` in that folder.

**What was measured.** Across 123 scheduled nights (2026-07-10 to 2026-11-09) the driver published in full on 22, in part on 2, skipped 11 and was blocked on 88. Of the 100 driver runs that ended green, 21 had shipped, so the run colour says nothing about shipping. On three nights the driver reported "blocked" although the release tag exists in all five libraries. A blocked night is marked by a named step since 2026-08-04; what is still recorded nowhere durable is shipped versus skipped, which gate stopped the night, the version and the cause. Those live in Slack and in logs that expire after 90 days: 37 logs are already gone.

Stage 3 (release-integrate) is the stop on 54 of the 88 blocked nights. In the failed runs with script lines there are 93 failures across 55 script paths, and 20 runs had exactly one failing leg of about 47. On 11 of the 24 nights with a real regression, a script that had failed the night before failed again. Two scripts from one PR blocked five nights running.

**Slice 1: the outcome record.** In `agents/conductors/release/nightly.sh`, write one outcome line per night to a durable place the digest reads (a ledger file committed by the driver). After a live run, verify the release directly: the version is on PyPI for every library and the tag exists on every released repo. Report three distinct outcomes (shipped, partial, not shipped) and name the failing job.

**Slice 2: same-night bug tasks.** When Stage 3 fails, file one Mind bug prompt per failing script, deduplicated by path, with the quoted error line and the PRs merged in the activity window as suspects. A shift can then pick it up the same day, so no script blocks two nights.

**Slice 3, separate and larger: catch it on the PR.** For PRs that touch a workspace or a library API, run the workspace scripts selected by the changed paths at the release profile, with the runner Stage 3 uses. The two five-night scripts passed their PR's smoke check only because neither was in `smoke_tests.txt`.

Not in scope: a script-level retry and an expiring quarantine in Stage 3. They need a doctrine line on when quarantine is allowed, which is the human's ruling (REL-2 in the report).

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
