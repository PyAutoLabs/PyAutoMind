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
Consequence: judge
Witness: Brain and Mind test suites pass; the batch-record schema test accepts a sample shift brief (goals, named tasks, backlog policy, review-minutes, review-at, lanes) and rejects one missing `review-at`; intake parses a `Needs:` header into the census; `end_at_deliverable_hook.sh` still blocks timers for ordinary sessions
Review-minutes: 20
Unattended: never

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md. Read the epic file's
"Human decisions (2026-11-03)" and "Design principles" sections first. They are the spec,
and they are human rulings, not proposals.

## Deliverables

1. **`PyAutoMind/policy/end_at_deliverable.md` (+ hook if needed).** Keep the rule for every
   Claude session. Add the single exemption: the deterministic watcher (a non-LLM script,
   built in phase 2) is the only thing that keeps time and starts sessions. Orchestrator and
   worker Claude sessions still never arm timers. Keep the 08-31 and 09-03 history as the
   reason.
2. **`PyAutoBrain/AUTONOMY.md`:**
   - **Shift brief = launch.** A human-written brief grants dispatch for its scope until
     `review-at`. This replaces "never dispatch on a schedule" inside that grant only.
   - **Unattended `glance` merges between check-ins**, with the guards:
     - an independent-session witness;
     - a pause on Heart RED or an unmatched YELLOW;
     - a per-shift merge cap;
     - the shadow window continues;
     - never `judge`-tier work or a release.
   - **Goal decomposition files drafts only.**
   - **The push-notification test.** Does waiting until `review-at` cause harm or waste the
     shift? Which classes qualify, and a budget of about 1 per shift.
3. **`PyAutoBrain/skills/batch/batch.md` + `agents/conductors/batch/AGENTS.md`:**
   - backlog dips under the brief's policy replace "never substitute your own picks";
   - the digest separates brief work from backlog picks, with a one-line reason per pick.
4. **`PyAutoMind/batches/AGENTS.md` schema.** Extend the batch record into the shift brief:
   - ordered primary goals;
   - named tasks;
   - the backlog policy (none / fill-idle / scoped + exclusions);
   - review-minutes, `review-at` and lanes;
   - the merge cap.

   Add the **digest** format: per task a one-screen proof packet (before/after numbers or a
   figure, the witness output, what was not checked), plus tokens used, review minutes
   planned vs actual, merges, reverts, pushes and drafts filed.
5. **`Needs: ral | gpu | wsl-data | none` prompt header.** Document it in REFERENCE.md beside
   `Consequence:`/`Witness:`, and make intake and census parse it. Intake should propose a
   value when the text mentions RAL, GPU or `/mnt/c`. Document the planned "RAL test packet"
   handoff (the Science orchestrator is the single RAL gateway). Only the field and the
   documentation land here; the handoff itself is phase 4.

## Out of scope

The watcher, dispatch, leases and kill switch (phase 2), any orchestrator runtime, and the
RAL submission path.

## Review

One PR per repo, read together by the human. These rewrite the autonomy contract, so never
auto-merge.

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b15ff817-f0d9-4ab3-b23f-735fcbb990f5/scratchpad/autonomous_orchestrators_p1.md -->
