Each science project's `hpc/sync` hard-coded its `PULL_DIRS` array, which both
`pull` and `pull-full` iterate, so a run written to a custom `PYAUTO_OUTPUT_DIR`
was never fetched at all. On 2026-09-09 that stranded 173 MB of
`euclid_dr1_prelim` ordered-MGE results on RAL, and the Cortex check-in — unable
to see them — reported the tasks as FAILED.

The Cortex check-in now derives the `output*` roots its tasks declare in their
`## Where to look` bullets (reusing `_path_tokens()` from #370/#371, the sibling
task that made such runs scorable once present) and passes them to each
project's own pull as `PYAUTO_PULL_DIRS`. Each script **appends** them to its
own `PULL_DIRS`. This extends the env-override convention that
`hpc/sync.conf.example` already documented for `HPC_HOST` / `HPC_BASE` /
`PROJECT_NAME`; an unset variable reproduces the previous behaviour exactly, and
`pull-full` inherits the change because it iterates the same array. The organ
boundary is unchanged — Cortex still only runs the human's own CLI and never
reaches RAL itself.

**Only `output*` roots are ever passed.** A pull rsyncs remote to local, and
real tasks name `results/`, `wiki/project/state.md`, `scripts/…` and
`hpc/batch_cpu/…` in the same bullets as their output roots; handing those to a
pull would overwrite the human's own source with the cluster's copy. A test
asserts that guard directly.

**Shipped**

| repo | PR | merge commit |
|---|---|---|
| PyAutoBrain | #373 | `11aa3f83` |
| euclid_strong_lens_modeling_pipeline | #59 | `da9ff852` |
| subhalo_validation | #1 | `ab4bf323` |
| slope_hierarchy_scale | #1 | `be6e88da` |

**Evidence.** PyAutoBrain full suite 943 passed / 1 failed — the failure is the
known pre-existing worktree-symlink trap, which passes in the canonical checkout
and in CI. Four new tests cover root selection, pooling and dedupe, the
unchanged-when-nothing-declared path, and the environment assignment reaching
the child process. `bash -n` plus an append/dedupe harness passed on all three
edited scripts: unset reproduces each project's own list, extra roots append,
an already-present root is not duplicated.

Live witness, a dry-run pull against RAL for `euclid_dr1_prelim`: without the
seam the pull enumerated `output/`, `output_sed/` (absent) and `inspect/`
(absent), never mentioning `output_ordered_witness/`; with
`PYAUTO_PULL_DIRS=output_ordered_witness` that root appears and is not reported
missing. `rsync --dry-run --stats` shows it holds 115 files (90 regular, 25
dirs), 173,465,562 bytes on RAL.

**Scope decisions.** The three active projects only; the nine dormant/retired
keep the old behaviour and pick the convention up when reactivated. The retired
`inference_programme` is structurally different (parallel
`PULL_DIRS`/`PULL_DESTS`/`LOG_INDICES`) and would need bespoke work.
`subhalo_validation` and `slope_hierarchy_scale` are PyAutoLabs repos outside
`repos.yaml`; they were edited in worktrees taken off their science clones so
the live science trees never switched branches. Neither has any CI configured —
both were merged on the local evidence after an explicit human decision.

**Gates.** Heart RED at ship on five organism-scope reasons, acknowledged
in-session by the human and recorded as a `heart-ack` on the task row; nothing
in these four repos is in the release chain. Heart freeze: not frozen at merge.

**Follow-ups, deliberately out of scope.** `find_logs()` globs every historical
run stem so `leg_resume` reads an old job's `.out`, and `void` remains in
`FAILED_RUN_STATES` — those two are what still make the check-in read FAILED.
The root cause behind this task is that 12 `hpc/sync` scripts are forks of one
ancestor sharing 55-95% of their text with no provenance marker; de-forking them
to a maintained template is the durable fix and remains unfiled.

## Original prompt

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
