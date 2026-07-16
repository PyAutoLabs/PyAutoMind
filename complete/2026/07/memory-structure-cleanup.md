## memory-structure-cleanup (wiki/ + bibliography restructure, structure lint, template sync — SHIPPED)
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/24 (CLOSED; design note posted as issue comment)
- completed: 2026-07-16
- prs: PyAutoMemory#25 + PyAutoMind#82 + PyAutoBrain#121 — ALL MERGED (order Brain->Memory->Mind so the memory faculty never lost its PyAutoMemory surface).
- summary: five root *_wiki/ folders -> wiki/<domain>/ (lensing/smbh/cti/methods/galaxies) with the shared schema promoted to wiki/CLAUDE.md; 9 legacy root .bib files + Euclid/Paykari2020.bib deleted after a key-level audit proved every unique key already existed in bibliography/pyautomemory.bib (library.bib: 2918 entries = only 1035 unique keys, all present — the files were internally duplicated ADS exports); pyautopaper.bib compat symlink retired (zero live references); stray ADS papers (2 root PDFs, 5 one-file topic folders, cticomments, euclid.sty) deleted after closing the one coverage gap (Hall 1952, PhysRev.87.387 — canonical entry + resolved its sources/ TODO section); structure lint (scripts/validate_structure.py: top-level allowlist, .bib only in bibliography/, PDF-magic-byte detection catching extensionless ADS downloads) wired into make validate + new CI; write contract in AGENTS.md; spawn.py template ships wiki/CLAUDE.md + empty wiki/example/ + bibliography/ — a fork starts green.
- root cause of the mess: index.md INSTRUCTED committing acquired PDFs into topic folders while README said PDFs live off-repo — the contradiction that produced the strays (fixed).
- generator bugs found by actually running spawn end-to-end (merged = ran, this time): generate_memory had NO KEEP_SUB branch (planned .github/* files silently skipped — dest dir created, file never written); empty_body wrote HTML comments into .yaml (parsed as a broken bibkey alias, failing the template's own validator); wiki/CLAUDE.md KEEP leaked the 'slacs' canary via schema examples (swapped to H0LiCOW); SPAWNED_FROM needed allowlisting. A spawned template now passes its own make validate + pytest.
- traps: in a git WORKTREE .git is a FILE, not a dir (structure lint had to special-case it); structure lint validates git-tracked content (git ls-files), not the filesystem — .pytest_cache/ false-positive otherwise; empty untracked dirs are invisible to git-semantics linting (test models a folder WITH a file).
- concurrency: PyAutoBrain#121 was a user-approved small parallel PR from main while workspace-agent held the repo claim (no file overlap) — recorded in active.md note at the time; three other tasks landed on Mind main mid-flight with zero conflicts (registry files never touched on the feature branch).
- follow-ups (design note on #24): canonical-key TODO sweep (345 TODO source sections; DOI/title matching vs canonical — Hall1952 is the proof of pattern); 856/1099 canonical entries not yet cited by any wiki page (fills via reading queue, not a bulk job); keep ONE canonical bib (no per-domain shards); deleted blobs stay in git history (~16MB — no rewrite, ever); intake-writer draft/-prefix bug still open (this session hand-moved two stranded prompts).

## Original prompt

# PyAutoMemory structure cleanup and long-term design (wiki/ + bib/ layout, PyAutoScientist rules)

Type: research
Target: PyAutoMemory
Repos:
- PyAutoMemory
- PyAutoScientist
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

PyAutoMemory, This feels like it could be cleaned up:

- Have a wiki/ folder with the wikis, analgous to autolens_assistant, at the moment the wiki fodlers seem scattered.
- Fodlers like CTI, DarkMatterModels, Euclid and LightProfFits contain individual .pdf files or .bib files. These must be
some sort of unused hangover from previous work which can be removed?
- Is bibliography/pyautopaper.bib now redundant?
- There are like 9 .bib files in the main repo, I am sure I just dumped them here but its time to clean them up. Either
consolidate to one .bib file or have a bib folder next to wiki which puts the .bib entries in sensible standalone files.
I know bib referencing is hard for AI so these do contain important info so dont just delete some, but also remove duplication.
- [devaucoleurs1948.247D](../PyAutoMemory/devaucoleurs1948.247D) and [Hubble1926.321H](../PyAutoMemory/Hubble1926.321H) surely
dont belong here?

In general, it feels like some rules need to be put in place across PyAutoScientist to prevent PyAutoMemory
from ending up in this statem and it would benefit from a bit more structure (e.g. the wikis folder, bib folder)
to make it more navigateable for a random user. This structure would also generalize it and make it more useable
for anyone in the PyAutoScientist ecosystem, especially as then theyd just need empty wiki, bib folders and
whatnot.

Finally do deep research and think hard about any other longer term changes we can make to the structure and
design of PyAutoMemory.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/bccad7d5-61a2-4177-b2e0-0dafc0feed05/scratchpad/intake_pyautomemory_cleanup.md -->
