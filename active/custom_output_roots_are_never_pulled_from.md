# Custom output roots are never pulled from the HPC — each project's…

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoCortex
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-09-09
Consequence: notify
Witness: a science run written to a custom PYAUTO_OUTPUT_DIR is pulled to the laptop by the project's own sync CLI without that path being hand-added to a per-project array.
Review-minutes: 0
Unattended: ready

Custom output roots are never pulled from the HPC — each project's hpc/sync has its own static PULL_DIRS

Type: bug
Target: PyAutoBrain
Witness: a science run written to a custom PYAUTO_OUTPUT_DIR is pulled to the laptop by the project's own sync CLI without that path being hand-added to a per-project array.

Science runs increasingly write to a custom PYAUTO_OUTPUT_DIR (one output root per arm, so parallel arms do not collide). Those roots are never pulled to the laptop, because each science project's hpc/sync carries its own hard-coded PULL_DIRS array and both the `pull` and `pull-full` verbs iterate it.

Evidence from 2026-09-09:
- euclid_dr1_prelim: PULL_DIRS=(output output_sed inspect)
- subhalo_validation: PULL_DIRS=(output results)
- slope_hierarchy_scale: PULL_DIRS=(output)
Three different file hashes — these are divergent per-project forks, not copies of a shared template, so there is no single place to add a path.

Concrete miss: euclid_dr1_prelim jobs 342375_[0-1] (ordered MGE witness) and 342377_0 (unordered control) completed on RAL and wrote to output_ordered_witness/. 166MB across three completed runs sat unpulled; the Cortex check-in reported the tasks as FAILED. Retrieving them needed a temporary edited copy of the project's own sync CLI.

The human confirms splitting results into custom output folders will become commonplace, so a per-project path addition is not the fix.

Options to weigh (design decision wanted, not a predetermined answer):
- glob output* in PULL_DIRS so any output root is pulled by convention;
- have the pull consult the Cortex task ledger's declared output roots for that project;
- give the sync CLI a flag the Cortex check-in can pass.

Filed against PyAutoBrain because the Cortex check-in door is what invokes each project's `<sync_cli> pull` and is the only place a general convention can be consulted centrally; part of this task is deciding whether the convention belongs there, in PyAutoCortex, or in the per-project science clones under the Science directory (which are not workspace repos).

Sibling task: the Cortex scorer bug filed alongside this one (scorer blind to runs outside output/) — that one makes such runs scorable once pulled; this one makes them arrive.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from user-intake -->
