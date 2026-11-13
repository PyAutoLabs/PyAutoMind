# Heart: a durable verdict history, and every stop classed as infrastructure, flake or product

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: glance
Witness: (a) two consecutive `heart-health.yml` runs with an unchanged verdict each append one line to `timings/verdicts.jsonl` (time, profile, verdict, score, reasons each with a `class`); `wc -l` before/after shown; (b) a unit test maps a fixture of today's reason strings to classes (e.g. "driver lost its GitHub credentials" → infrastructure, a retry-pass script → flake, "release validation FAILED" with a script error → product); (c) a script prints "days RED by class" over the file
Review-minutes: 10
Unattended: never
Lane: any

Source: REL-14 and REL-11 of the ecosystem review (2026-11-10), section B8. **Both unverified by the review: re-check first.**

**REL-14.** `PyAutoHeart/.github/workflows/heart-health.yml:261-269` commits only when README or timings change, so an unchanged RED leaves no trace; the README strip sat unchanged 23 days in September. The append-only pattern already exists (`timings/gates.jsonl`).
- Re-check: `git log --format=%ad -- README.md` on PyAutoHeart since 2026-11-01 vs the number of `heart-health.yml` runs.
- Change: append one verdict line per computation (cloud runs only) to a tracked JSONL; one commit per run is acceptable, or batch with the existing timing commit.

**REL-11.** The review counted 107 of 965 completed tasks as release-machinery work, and several RED/blocked stretches were the gate misreporting (Brain#577 token expiry, Heart#321 DST skew, Heart#225 phantom failures).
- Re-check: `python3 mind_records.py` in `Science/scratch/ecosystem_review_2026-11/evidence/release_loop/` against Mind complete/2026/11 (the share since the M2 builds).
- Change: give each red/yellow reason a `class` (infrastructure, flake, product) in `heart/readiness.py`'s reason builder, carry it into the nightly page (`PyAutoBrain/agents/conductors/release/nightly.sh` `page` calls, e.g. :350, :394, :428) and the Heart board, and chart days-red by class. Stage 3's retry already records flaky scripts (Heart#345); use that, do not re-derive it.

**Constraint (REL-13, preserve):** keep the driver's exit-code contract (0 shipped/skipped, 2 blocked at a gate, 1 driver error) and its named steps; classes are added to messages, never by changing exit codes.

Feeds the lane metric in `shift_keeps_heart_green_lane.md` ("nights shipped over active nights", days RED by class).
Tier glance: records and labels only; no gate changes.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
