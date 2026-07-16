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
