- epic: autonomous-orchestrators (phase 1 of 7; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: doctrine and formats only. PyAutoMind#522: new policy/shift_watcher.md (deterministic non-LLM watcher is the one exemption to end_at_deliverable; no Claude tool, arms nothing, no dispatch without an open brief, STOP file checked first); batches/AGENTS.md "Shift brief (2026-11-03)" with fenced example brief + digest + proof-packet format + calibration rule; REFERENCE.md documents Lane: any | local-dev | ral | gpu | wsl-data. PyAutoBrain#552: AUTONOMY.md "Shift briefs and unattended `glance` — 2026-11-03" (shift brief = launch; unattended glance merges with five guards; one Mind writer per shift; drafts-only decomposition; push-notification test), Consumers + hard-invariant entries, batch skill/conductor brief rule (brief --check / dispatch / digest marked planned), 5 doctrine tests.
- deviation (approved): policy/end_at_deliverable.md left byte-identical — repos_sync stamps it into 50 repos; the one-line pointer to shift_watcher.md rides with the next routine stanza refresh.
- witness: hook payloads ScheduleWakeup/CronCreate/RemoteTrigger run/send_later exit 2, RemoteTrigger list exit 0; Revert condition 6 → 11; repos_sync --check green (canonical --root); pytest Mind 711 / Brain 1409; lifecycle drift pre-existing (active/chapter2-explanations.md).
- traps: from a task worktree repos_sync --check reports COWLS_COSMOS_Web_Lens_Survey undeclared (worktree_create flattens lens/ to the root) — run it with --root ~/Code/PyAutoLabs; with the worktree activate.sh PYAUTO_ROOT/MIND/BRAIN set, test_repos_sync_root_default and test_grouped_organ_consumers each fail one test on main too — unset them for a clean suite.
- next: phase 2 draft/feature/pyautobrain/autonomous_orchestrators_p2_lane_schema_census.md.
- heart: YELLOW at start (monitoring RED reasons), judge tier, human /prm.

## Original prompt

# Autonomous orchestrators phase 1: policy amendments and the shift brief, digest, proof-packet and push formats

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- autonomy
- orchestration
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Epic: autonomous-orchestrators
Phase: 1
Filed: 2026-11-03
Issued: 2026-11-03
Consequence: judge
Witness: prose only, no code — (a) `bash PyAutoMind/policy/end_at_deliverable_hook.sh` fed a PreToolUse payload for each of ScheduleWakeup, CronCreate, RemoteTrigger run and send_later still exits 2 with the policy line, and the read-only RemoteTrigger list payload exits 0; (b) `grep -c "Revert condition" PyAutoBrain/AUTONOMY.md` rises by exactly the number of new sections and each new H2/H3 carries a 2026-11 date; (c) `python3 PyAutoMind/scripts/lifecycle.py check`, `python3 PyAutoMind/scripts/repos_sync.py --check` and `pytest PyAutoBrain/tests -q` green on both branches; (d) `batches/AGENTS.md` contains a fenced example brief and a fenced example digest that the phase-2 validator will be written against
Review-minutes: 20
Unattended: never
Lane: any

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md. Read the epic's "Human
decisions (2026-11-03)", "Lane, not Needs", "Design principles" and "External facts" first.
They are the spec, and the decisions are human rulings, not proposals. This phase writes
**doctrine and formats only**; every line of code moved to phase 2
(`autonomous_orchestrators_p2_lane_schema_census.md`).

## Deliverables

1. **`PyAutoMind/policy/end_at_deliverable.md` (prose; the hook is untouched).** Keep the
   rule for every Claude session verbatim. Add one paragraph: the deterministic watcher
   (a non-LLM script, phase 3) is the only thing that keeps time and starts sessions; it is
   not a session, calls no Claude tool and arms nothing inside a session; orchestrator and
   worker sessions still never arm timers and the hook keeps blocking them. Keep the 08-31
   and 09-03 history as the reason. Name the kill switch (a `STOP` file the watcher checks
   first) so the exemption has an off switch in the same paragraph that grants it.
2. **`PyAutoBrain/AUTONOMY.md`** — one dated section, "Shift briefs and unattended
   `glance` — 2026-11", each sub-rule with its *Revert condition*:
   - **Shift brief = launch.** A human-written brief with `review-at:` grants dispatch for
     its scope until `review-at:`; this is the launch act "What a batch launch is" requires,
     and it replaces "never dispatch on a schedule" inside that grant only. A watcher tick
     with no open brief dispatches nothing.
   - **Unattended `glance` merges between check-ins**, extending "Merge authority follows
     Consequence" (2026-10-02) from the in-turn wait to a watcher-started close-out, with
     every guard from the epic: independent-session witness; pause on Heart RED or an
     unmatched YELLOW; the brief's per-shift merge cap; the Shadow window keeps appending;
     never `judge`, never `decision-taken`, never a release.
   - **One Mind writer per shift.** Only the orchestrator commits to PyAutoMind during a
     shift, from a temporary worktree; workers write ledger lines into the lease directory
     for it to commit. Cite the 09-30, 10-07 and prompt_sync_push losses as the reason.
   - **Goal decomposition files drafts only**, with proposed `Witness:`, `Consequence:`
     and `Lane:`, bulk-approved at check-in.
   - **The push-notification test** — does waiting until `review-at:` cause harm or waste
     the shift? — the four qualifying classes, the budget of about one per shift, and the
     rule that a second push is itself a digest finding.
   Add the new section to the "Consumers" list and keep "Skills must link here rather than
   copying the tables".
3. **`PyAutoBrain/skills/batch/batch.md` + `agents/conductors/batch/AGENTS.md`:** the
   backlog dip under the brief's policy replaces "do not silently substitute your own
   picks" (the brief *is* the human's composition: named tasks first, then the dip policy);
   the digest separates brief work from backlog picks with a one-line reason per pick; the
   member-session contract gains "spawned from the orchestrator's session template, never
   bare". Describe `batch brief` / `dispatch` / `digest` as the verbs phases 2–3 add, marked
   *planned* so the page does not claim code that does not exist.
4. **`PyAutoMind/batches/AGENTS.md` schema.** Extend the batch record into the **shift
   brief** (same file, same folder, same ledger-merge rules), with a fenced example:
   - `brief:` block — ordered primary goals; named tasks (prompt paths); the backlog policy
     (`none` | `fill-idle` | `scoped:` epics/tags/tiers + `exclude:`); `review-minutes:`,
     `review-at:`, `lanes:` (any subset of `any local-dev ral gpu wsl-data`), `merge-cap:`,
     `token-budget:` and, when RAL is allowed, a `ral-allowance:` (packets, partition,
     CPU-hours) that phase 5 consumes;
   - the existing `heart-ack:` and `expected-effects:` keep their meaning;
   - a `review-minutes-actual:` of the **previous** shift is required before a new brief
     is accepted (the calibration rule the 08-31 record never closed);
   - the **digest** section, appended at collect: brief work vs backlog picks, one proof
     packet per task, then the shift counters (merges, `glance` auto-merges, reverts,
     pushes, drafts filed, packets sent, workers crashed, tokens, review-minutes planned);
   - the **proof packet** format: one screen — the claim, before/after numbers or a figure
     path, the witness command and its output, what was not checked, the one-command
     revert;
   - **delivery:** the digest is also posted once as a comment on the shift's PyAutoMind
     issue (`issue:` key); the HTML packet becomes opt-in (`packet: yes`).
5. **`PyAutoMind/REFERENCE.md`:** document `Lane:` in the optional header beside
   `Consequence:`/`Witness:` (it is undocumented today) with the values `any | local-dev |
   ral | gpu | wsl-data`, each of the last three implying `local-dev`, and the planned
   "RAL test packet" handoff in one sentence (the Science orchestrator is the single RAL
   gateway; phase 5). Spell `none` as `any`.

## Out of scope

Any code: `LANE_VALUES`, `_lane_ok`, intake pass-through, census, the brief validator
(phase 2); the watcher, leases, kill switch and usage guard (phase 3); the pilot (phase 4);
the RAL submission path (phase 5).

## Review

One PR per repo (PyAutoMind, PyAutoBrain), read together by the human. These rewrite the
autonomy contract, so never auto-merge; the witness makes the read a diff of prose with
every machine check already green.

## Approved plan (2026-11-03, laptop design-review session; human approved the six epic decisions)

Tier: judge — merge mode: human /prm. One PR per repo, opened by the working session; never
auto-merged. Branch `feature/autonomous-orchestrators-p1` in both repos.

**Deviation from deliverable 1, approved:** `policy/end_at_deliverable.md` stays byte-identical.
Its text is `DELIVERABLE_POLICY_FILE` in `scripts/repos_sync.py`, stamped as a generated block
into every synced repo's AGENTS.md and drift-checked (50 of 50 on 2026-11-03); editing it reddens
`repos_sync.py --check` until ~50 stanza commits land. The watcher exemption therefore lives in a
**new** page `policy/shift_watcher.md`, linked from AUTONOMY.md and `batches/AGENTS.md`; the
one-line pointer inside `end_at_deliverable.md` rides with the next routine stanza refresh.

Steps:

1. **PyAutoMind `policy/shift_watcher.md`** (new, ~25 lines): a deterministic script (systemd user
   timer or cron, phase 3) that polls `gh pr checks`, the project `hpc/sync jobs` verb and Mind
   state, and starts Claude sessions (`claude --bg`) only when there is work. It calls no Claude
   tool, arms nothing inside a session, dispatches nothing without an open brief whose
   `review-at:` has not passed, and does nothing while `STOP` exists in its slot directory. Cite the
   2026-08-31 and 2026-09-03 drains as the reason the exemption is this narrow.
2. **PyAutoBrain `AUTONOMY.md`**: new H2 after "Merge authority follows Consequence — 2026-10-02":
   `## Shift briefs and unattended \`glance\` — 2026-11-03`, sub-rules as H3s, each ending with
   `*Revert condition:*`:
   - *Shift brief = launch.* A human-written brief with `review-at:` in
     `PyAutoMind/batches/<slot>.md` is the launch act of "What a batch launch is"; the grant
     covers the named tasks plus the brief's backlog-dip policy until `review-at:`; a watcher
     tick with no open brief dispatches nothing. Revert: one dispatch outside a brief's scope
     returns batching to per-task `--auto`.
   - *Unattended `glance` merges.* Extends the 2026-10-02 table: the in-turn wait may be
     replaced by a watcher-started close-out after CI lands, only when (i) an independent
     session ran the `Witness:` (a different model where available, as leg 5), (ii) Heart is not
     RED and any new YELLOW matches the brief's `expected-effects:`, (iii) the brief's
     `merge-cap:` is not reached, (iv) the Shadow window row is appended at close-out, (v) the
     task is `glance`, not `decision-taken`, not a release. Revert: a `reverted` row demotes as
     the 2026-10-02 section says; one merge past the cap retires this sub-rule.
   - *One Mind writer per shift.* Only the orchestrator commits to PyAutoMind during a shift,
     from a temporary worktree; workers write ledger lines into the lease directory. Cite the
     2026-09-30 reset --hard loss, the 2026-10-07 autostash conflict markers and the
     prompt_sync_push sweeps. Revert: one lost Mind edit traced to a worker commit.
   - *Goal decomposition files drafts only*, with proposed `Witness:`, `Consequence:`, `Lane:`,
     bulk-approved at check-in. Revert: never loosened before the Shadow window confirms.
   - *The push-notification test.* Does waiting until `review-at:` cause harm or waste the
     shift? The four classes (data loss / destructive risk; RAL-rule breach or runaway usage;
     whole shift blocked on one human decision; credential or security problem), the ≈1 per
     shift budget, a second push is itself a digest finding. Revert: two pushes in one shift the
     human judged unnecessary retires push for that orchestrator.
   Also add the section to "Consumers" (batch, start_dev, prm) and extend the hard-invariants
   first bullet: "…except as 'Merge authority follows Consequence' (2026-10-02) and 'Shift briefs
   and unattended `glance`' (2026-11-03) grant them".
3. **PyAutoBrain `skills/batch/batch.md`**: in "2. Here are the ones I want" replace "do not
   silently substitute your own picks" with the brief rule (named tasks first, then the dip
   policy; unbriefed backlog is never dipped); in "3. Go" say that writing the brief with
   `review-at:` is the dispatch and workers are spawned from the orchestrator's session
   template, never bare; add a "Planned verbs" note (`batch brief --check`, `dispatch`, `digest`
   are phases 2–3, not yet code); in the collect section describe the digest (brief work vs
   backlog picks with a one-line reason each) and that the ledger plus the shift issue comment
   is the review surface, the HTML packet opt-in. **`agents/conductors/batch/AGENTS.md`**: the
   constraints table gains "Brief scope" and "Merge cap" rows with their why; "It proposes; the
   human launches" gains the brief sentence.
4. **PyAutoMind `batches/AGENTS.md`**: a "Shift brief (2026-11-03)" subsection with a fenced
   example record carrying `brief:` (ordered goals, named tasks as prompt paths,
   `backlog: none | fill-idle | scoped:` + `exclude:`, `review-minutes:`, `review-at:`, `lanes:`,
   `merge-cap:`, `token-budget:`, optional `ral-allowance:` with packets / partition /
   cpu-hours), `issue:` and `packet: yes`; a "Digest" subsection with a fenced example (brief
   work / backlog picks with reasons / one proof packet per task / counters: merges, glance
   auto-merges, reverts, pushes, drafts filed, packets sent, workers crashed, tokens,
   review-minutes planned); the proof-packet one-screen format (claim, before/after numbers or
   figure path, witness command and output, what was not checked, one-command revert); the
   calibration rule (no new brief while the previous record lacks `review-minutes-actual:`);
   and a note that `batches/examples/` (phase 2) is not a record.
5. **PyAutoMind `REFERENCE.md`**: in the optional header block add
   `Lane: any   # any | local-dev | ral | gpu | wsl-data; the last three imply local-dev`; in
   "The review-cost model" add a `Lane:` bullet (resource routing; the Science orchestrator is
   the single RAL gateway via a RAL test packet — phase 5).
6. **PyAutoBrain `tests/test_autonomy_doctrine.py`**: assertions on the new section's heading
   date, the five sub-rule headings, five `revert condition:` lines, "never" + "judge", and the
   Consumers entry (the existing pattern for prose the organism depends on).
7. **Witness run** on both branches, as the header says. `repos_sync.py --check` needs every
   synced repo checked out, so from a web/mobile session report it as *partial* and let the
   laptop `/prm` (or the repos' own CI) complete it.

Remote-session notes: bootstrap first (`bash PyAutoMind/scripts/session_bootstrap.sh`), GitHub
through the MCP tools per `PyAutoBrain/skills/GITHUB_ACCESS.md`, and keep the Mind **registration**
(`active.md`, the `draft/ → active/` move) on its own `claude/...` branch so `mind_ledger_merge`
auto-merges it; the Mind **policy/REFERENCE/batches** edits go on `feature/autonomous-orchestrators-p1`
as an ordinary PR (they are code-side paths and never auto-merge).

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b15ff817-f0d9-4ab3-b23f-735fcbb990f5/scratchpad/autonomous_orchestrators_p1.md; revised 2026-11-03 (design review: split to prose-only, code moved to phase 2) -->
