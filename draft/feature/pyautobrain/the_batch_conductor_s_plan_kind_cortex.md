# The batch conductor's `plan --kind cortex` admits only `ready` phases…

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

The batch conductor's `plan --kind cortex` admits only `ready` phases, so a slot made of legacy-born `awaiting-ruling` members and `submitted`/`running` carry-forwards (batch 2026-09-02-pm) had to be hand-written. Add a form (`plan --kind cortex --board` or admit awaiting-ruling + submitted/running members by default) so such slots are conductor-opened and their packets conductor-built.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from user-intake -->
