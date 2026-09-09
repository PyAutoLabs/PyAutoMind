# Cortex scorer blind to runs outside output/ and fails them against…

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: notify
Witness: a task whose "## Where to look" bullets name a relative path outside output/ is scored against that path, and a task with no discoverable run scores UNOBSERVABLE rather than FAIL; both covered by regression tests.
Review-minutes: 0
Unattended: ready

Cortex scorer blind to runs outside output/ and fails them against an unrelated run

Type: bug
Target: PyAutoBrain
Witness: a task whose "## Where to look" bullets name a relative path outside output/ is scored against that path, and a task with no discoverable run scores UNOBSERVABLE rather than FAIL; both covered by regression tests.

Science runs increasingly write to a custom PYAUTO_OUTPUT_DIR rather than output/. The Cortex check-in scorer cannot see those runs at all, and instead of saying so it scores the task against whatever is newest under output/ — manufacturing a confident FAIL from an unrelated run. This violates the door's own stated contract that "UNOBSERVABLE is not FAIL".

In PyAutoBrain/agents/conductors/cortex/_cortex.py:

1. where_paths() (~line 1640) resolves a task's "## Where to look" bullets but keeps a bullet only if p.is_absolute(). Every task writes these bullets relative to the project root (e.g. output_ordered_witness/run_0/...), so the resolved list is always empty in practice.

2. where_paths() also takes only bullet.split()[0] as the candidate path token. Real bullets lead with a project-row label, e.g. "`euclid_dr1_prelim` (project row): `output_ordered_witness/run_0/...`", so the first token is not a path and the real path is never examined.

3. run_artifacts() (~line 1666) then does `bases = list(where) or [r / "output" ...]` and picks the newest .completed marker or zip under output/. With `where` empty this scores a stale, unrelated run directory with no signal to the reader that the run being scored is not the task's run.

Observed on the 2026-09-09 check-in: euclid_dr1_prelim tasks ordered_mge_witness_102005065 and ordered_mge_control_unordered_102005065 both scored "witness FAIL" against a stale phase-4 vis_pix directory belonging to a different tile, while their real completed results sat in output_ordered_witness/. Three subhalo_validation tasks were scored against that same wrong directory. Eight of nine live tasks came back FAILED; none was an actually failed run.

Wanted:
(a) resolve relative Where-to-look bullets against the project root;
(b) scan the whole bullet for path-like tokens rather than only the first;
(c) when a task declares roots and they yield no run, report UNOBSERVABLE instead of falling back to output/ and scoring whatever is newest. Any fallback that changes which run is being scored must say so in the readout rather than presenting the result as the task's own run.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from user-intake -->
