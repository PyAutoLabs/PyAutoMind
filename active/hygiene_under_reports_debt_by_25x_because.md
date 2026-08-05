# Hygiene under-reports debt by 25x because its repo arrays skip

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Hygiene under-reports debt by 25x because its repo arrays skip two libraries. The hygiene conductor scans a hardcoded list of checkouts in PyAutoBrain agents/conductors/hygiene/hygiene.sh. That list is stale: the LIB_REPOS array holds five entries where the body map (repos.yaml) has six, silently skipping the CTI and Reduce libraries, and it mislabels the config layer as a library; ORG_REPOS covers four of seven organs. The result is wrong output, not stale prose. On a real run the crlf mode printed '5 library .py w/ CRLF' when the true count is 127 — 122 of them in the skipped CTI library, breaking that repo's LF-only rule with nobody watching. The deps mode audits five pyproject.toml instead of six; tidy inspects nine of roughly seventeen managed checkouts. Every clean bill of health the conductor has issued understates reality. This is an internal inconsistency, since the sibling scanners _hygiene_config.py and _hygiene_refs.py already reach the CTI library. The drift checker cannot catch the gap: its tenant-firewall entry for hygiene.sh pins the current broken set as an allowlist instead of verifying coverage. The repair should derive the arrays from the body map rather than re-hardcoding them. Widening coverage will surface a large backlog of genuine new findings, so land the coverage repair and the triage of what it uncovers as separate tasks.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
