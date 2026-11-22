## batch-collect-leftovers
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/706
- completed: 2026-11-22
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/707
- Removed what the retired `batch collect` left in PyAutoBrain: the shift box review button, Pages packet URL and packet path keyed on `collected:` (`dev_status` loses `pages` and the `reviewable`/`url`/`packet` keys); the planner's `read_outcomes`, `previous_carried`, `newest_slot`, `batch_records`, `plan(carried=, carried_from=)` and the "Carried in" line; and the 506-line `packet.css` (the opt-in `digest.html` now carries a few lines of inline style).
- Human decisions at /prm: (b) keep the shift box member rows and the in-progress/awaiting-review counts they feed; (c) drop the `carried` / `carried_from` keys from `batch plan --json` (nothing read them); (a) Heart STALE at ship time was this network's TLS timeouts only, accepted.
- Witness: before/after render of the intake dashboard against one fixed Mind snapshot is unchanged for shift briefs.

## Original prompt

# Remove what batch collect left behind in the planner and the status…

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-11-22
Consequence: notify
Witness: the intake dashboard renders the same for a current shift brief before and after; a record carrying `collected:` or `- outcomes:` still renders without error; `batch plan` output is unchanged against a Mind whose newest record is a shift brief.
Review-minutes: 0
Unattended: ready
Lane: any

Remove what batch collect left behind in the planner and the status box

Type: refactor
Target: PyAutoBrain
Lane: any

`batch collect` was retired in PyAutoBrain#701, but three things in @PyAutoBrain still serve only records that collect wrote. (1) `agents/conductors/batch/_status.py`: the dashboard's batch status box shows its review button and a `batches/packets/<slot>.html` link when the record has `collected:`, which nothing stamps now; `dev_status` also reads member `outcome` words collect wrote. (2) `agents/conductors/batch/_batch.py`: `previous_carried` and `read_outcomes` feed `plan` a "Carried in" line from an `- outcomes:` block only collect wrote. (3) `agents/conductors/batch/packet.css` (506 lines, the review packet's stylesheet) is inlined whole into the opt-in `digest.html` (`_orchestrator._write_packet`), which is one `<pre>`. Decide per item whether shift briefs need it; remove what they do not, and keep old records rendering without error. This changes dashboard and `plan` output for old records, so it is not behaviour-preserving for them.

Witness: the intake dashboard renders the same for a current shift brief before and after; a record carrying `collected:` or `- outcomes:` still renders without error; `batch plan` output is unchanged against a Mind whose newest record is a shift brief.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/2.txt -->
