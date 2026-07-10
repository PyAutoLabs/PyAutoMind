# PyAutoScientist 3b-3: implement the Clone agent (lightweight-seed first)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoBuild
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft — issue when spawn (3b-1) ships

Implement `agents/conductors/clone/` against its approved DESIGN.md
(Brain#59): CLI wiring, CloneDecision, the mandatory clone-mode question —
implementing **lightweight-seed mode first** (constitution + setup skill +
empty wiki scaffolds + pending-stub queue), since it is the
autoproject_assistant path in the PyAutoScientist adoption story and needs
no domain corpus. exact-clone / differentiated-sibling modes follow on
demand. Generation executes via Build; the newborn validates via Heart
(per the design's organ split).
