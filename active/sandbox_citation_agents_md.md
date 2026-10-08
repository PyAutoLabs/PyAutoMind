# Repoint autolens_assistant wiki citation from retired autolens_workspace CLAUDE.md to AGENTS.md

Type: maintenance
Target: autolens_assistant
Repos:
- autolens_assistant
Difficulty: small
Autonomy: safe
Priority: normal
Memory: wiki/lensing/log.md; index.md; wiki/AGENTS.md
Status: formalised
Consequence: notify
Witness: autoassistant wiki-currency `--check-citations` on autolens_assistant reports 0 missing cited paths.
Review-minutes: 0
Unattended: ready
Issued: 2026-10-08

# Repoint autolens_assistant wiki citation from retired autolens_workspace CLAUDE.md to AGENTS.md

Found by /review_release on PyAutoHands release run 37653172766, release 2026.10.7.1, which published fine.

**autolens_assistant wiki citation.** The release job `wiki_currency_check / wiki-currency` failed only on `--check-citations`: `wiki/core/operations/sandbox.md` (line 8, `paths: [CLAUDE.md, README.md]` citing `autolens_workspace`) points at `autolens_workspace:CLAUDE.md`, which was retired on 10-07 (repos_sync "retire the CLAUDE.md pointer"; AGENTS.md is the file now). Fix = repoint the citation to `AGENTS.md` (verify the cited content actually lives in autolens_workspace's AGENTS.md; adjust prose in the page if it says CLAUDE.md). Also grep the rest of autolens_assistant wiki/skills (and the sibling assistants autogalaxy_assistant / autofit_assistant, which run the same check) for other `CLAUDE.md` citations to now-retired files — include them only if the citation checker would flag them. Reproduce the checker locally if feasible (the drift-report shows the check is `--check-citations` in autoassistant's wiki-currency tooling) and confirm 0 missing paths after the fix.

<!-- formalised by the Intake (Conception) Agent on 2026-10-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/714552f3-a2ad-45fd-8b3e-cf45adbd6f01/scratchpad/intake/wiki_cite.md -->
