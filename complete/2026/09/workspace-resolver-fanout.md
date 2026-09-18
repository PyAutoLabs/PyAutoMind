Phase 2 of the workspace regroup. Fixes the last places that derived the workspace root
from "my parent directory", and fixes the CI gate that made a canonical-hook PR unpassable.
No directory layout changed.

## What shipped

- **PyAutoMind#415** — the session-start hook resolves by `.pyauto-root` marker and fans out
  two levels; plus `--skip CHECK` and the narrow, loud `firewall_gate.yml` use of it. 531 passed.
- **PyAutoReduce#75** — the demo dataset path and the `_CAND` canonical-output fallbacks are
  derived, never named. 299 passed, 3 skipped.
- **PyAutoArray#561** — two docstrings stop naming a task bundle removed long ago. 1584 passed.

Merging #415 fired `session_hook_propagate.yml`, which bot-pushes the regenerated hook into
every manifest repo — by design, because "thirty PRs per hook edit is a review queue nobody
would read".

## The defect

`policy/session_start_hook.sh:72` was `WORKSPACE_ROOT="$(dirname "$REPO_DIR")"`. Under a
regroup that is a FAMILY directory, and every consequence was silent because the family
directory really exists: :564 exported it as PYAUTO_ROOT into the whole session, :470 wrote a
`.claude/` tree into it (both the `.git` and writability guards pass, so it SUCCEEDED and built
a second workspace root), and :426 unshallowed one family instead of every repo.

Correct severity, which an early survey overstated: line 47 exits unless CLAUDE_CODE_REMOTE=true,
so the hook never runs in a local CLI session. It is a remote/web-session defect.

Fixing discovery alone was not sufficient — the fan-out moved to a bounded two-level walk
(a directory with `.git` is a checkout and is swept; one without is a family directory and is
looked into exactly one level further). An unbounded walk is not something a session start can
afford. One warm run: 0.144 s.

## The regression this caught in the delegating brief

The brief said "source the resolver when it is reachable". That is unsafe. The resolver anchors
on the BRAIN checkout, and in a task bundle `PyAutoBrain` is a symlink into the canonical
workspace. Measured before the guard:

    REAL bundle worktree: root=/home/jammy/Code/PyAutoLabs   reason=.pyauto-root marker

A hook running inside a bundle would have exported the CANONICAL workspace to the session,
written a `.claude/` root into it and unshallowed its repos. The hook now refuses a resolver
answer that does not CONTAIN its own checkout — the guard `scripts/session_bootstrap.sh` already
carried for the same trap, generalised to an ancestor test.

Fifth instance in this epic of one shape: locating is not writing, and not grading.

## The gate this phase exposed and fixed

The first push went red on exactly one leg, and could not have done otherwise: the sibling
organs are checked out at their mains, so their hook copies are stale BY CONSTRUCTION until
propagation runs on the push to main AFTER merge.

Latent, not new. `policy/session_start_hook.sh` entered the gate's paths filter 2026-08-29
(#369); the generated-hooks leg entered repos_sync 2026-09-03; the last canonical hook edit was
2026-08-27. No hook PR had run under both until this one, and every future one would have been
red forever.

`--skip CHECK` joins `--only`: repeatable, exact label match, subtracting from whatever `--only`
selected, with BOTH validated against the full registry BEFORE narrowing — a typo that silently
disabled a gate is the one failure mode the flag could otherwise introduce. The workflow uses it
only on `pull_request`, only when the PR's real diff (not the paths filter, which has already
matched) touches a canonical hook, whole-line exact so `docs/policy/session_start_hook.sh.md`
does not count. Push to main is untouched and `--skip` is unreachable from it.

It does NOT just drop the check: the same branch asserts PyAutoMind's own installed copies match
canonical — the one repo propagation never writes to — and prints a banner saying green means
"the copies this PR controls are in sync", NOT "every repo is in sync".

Proven not to be a weakening: with the leg skipped, desyncing that copy by one line leaves the
drift check at exit 0 and fails the run through the assertion instead. That demonstration caught
a bug IN THE FIX — the first `-k` selected one of the two hook tests, silently deselecting the
end-at-deliverable guard — now pinned by a test that extracts the `-k` from the workflow and
asserts it matches both. Confirmed in live CI: `2 passed, 47 deselected`.

## Design decision: a science library does not import an organ

PyAutoReduce deliberately does not reach for the resolver. It is a released PyPI distribution:
someone who `pip install pyautoreduce`s and clones the repo to run `scripts/` has no Brain
checkout, no marker and no workspace, so an import-by-file-path of a developer-box organ would be
dead code on every machine but one — the exact failure class that resolver's docstring exists to
kill. It also answers a question one level up from the one asked, and would invert the dependency
direction.

Instead: `$AUTOREDUCE_DEMO_ROOT` → a bounded sibling probe (the full cross-product of "is THIS
repo in a family folder" x "is autolens_assistant") → an unverified guess, plus a `--demo-root`
flag. Resolution demonstrated across six layouts including the phase-3 one.

The four `_CAND` fallbacks replaced a GUESS at where the canonical checkout is with the FACT git
already holds: a worktree's `.git` is a file reading `gitdir: <canonical>/...`. Verified the
resulting candidate lists are byte-identical to the originals.

## Witness

- Hook: 11 new cases, all red against the unmodified hook. The defect itself, from the red run:
  "installed .../workspace/lens/.claude/settings.json" while the true root got none.
  512 passed after (baseline 501), then 531 with the gate work (+19).
- Gate: the original CI failure reproduced line for line on a real 4-repo layout, then cleared on
  the same tree with all 17 other legs still running and printing.
- Paths: `git grep "Code/PyAutoLabs" -- '*.py'` empty in both repos; six-layout resolution table.
- Live CI after the fix: firewall PASS, banner printed, both hook tests selected.

## Filed, not fixed here

- `PyAutoArray/files/{ghost_peak,pca_rotation}_experiment.py` import
  `autoarray.inversion.mesh.interpolator.rectangular_spline`, which no longer exists, so neither
  can run. Confirmed independently by the PyAuto API gate. Filed as a decision (repair or retire):
  `draft/maintenance/autoarray/files_experiment_scripts_import_a_removed_module.md`.
- `scripts/session_bootstrap.sh` carries the same one-level defect (:280 fan-out, :121 extras
  scan, :138 shallow scan) and its root guard REJECTS a correct nested root. It is a phase-3 root
  enumerator; until that lands the multi-repo bootstrap door still misses nested checkouts even
  though the hook no longer does.

## Next

Phase 2c — `draft/maintenance/pyautobrain/workspace_smoke_shim_bootstrap.md` — the 12 smoke
shims, split out of this task because they are NOT copies (12 distinct checksums, 5 shape-classes)
and have no propagation mechanism, so patching them twelve times would re-affirm the structure
that made them drift. Its witness deliberately requires that a single edit reach all 12 without a
hand sweep.

Phase 3 (the physical regroup into `lens/ galaxy/ fit/ cti/ reduce/`, organs staying flat) waits
for the in-flight tasks to clear the release gate, and MUST create the `.pyauto-root` marker in
the same commit as the move — step 3 of the resolver is still deliberately wrong for an unmarked
nested workspace. Note also that the marker does not discriminate the canonical workspace from a
task bundle, so a phase-3 consumer assuming "marker means canonical" will land in a bundle.

## Original prompt

# Workspace resolver fan-out: the hook, the smoke shims and the hardcoded paths

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoMind
- PyAutoReduce
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: with a nested workspace fixture the regenerated session-start hook resolves the TRUE root rather than the family directory and fans out over every manifest repo rather than one family; `git grep -c 'WORKSPACE_ROOT="$(dirname "$REPO_DIR")"'` returns 0 across all repos after propagation; and no tracked Python file in PyAutoReduce or PyAutoArray matches `Code/PyAutoLabs`.
Review-minutes: 25
Unattended: needs-slicing
Issued: 2026-09-18
Unblocked: phase 1a SHIPPED 2026-09-18 (PyAutoBrain#392, PyAutoHeart#232, PyAutoHands#283, PyAutoMind#414) — record complete/2026/09/workspace-location-contracts.md. The resolver this consumes is on main: `_pyauto_root` resolves by `.pyauto-root` marker with the sibling-organ probe demoted to a fallback, and exports PYAUTO_ROOT_REASON / PYAUTO_ROOT_MARKER for shell callers. NOTE the limitation this phase inherits: step 3 is still wrong for a NESTED workspace with no marker (pinned by a test, deliberately, to protect the remote single-repo case), so the marker is the only thing protecting a regrouped tree.

Phase 2 of the PyAutoLabs workspace regroup. Changes NO directory layout. Mechanical fan-out that
CONSUMES the single resolver phase 1a introduces, so it cannot land before it.

## Scope

1. **The session-start hook — 1 source, 37 generated copies.**
   `PyAutoMind/policy/session_start_hook.sh:72` is `WORKSPACE_ROOT="$(dirname "$REPO_DIR")"`. Verified
   2026-09-18: exactly 37 copies exist, all byte-identical (single md5 dbcdbbde9ef3b44f54cbb1dca94fbf95),
   and all 37 carry that line. Give it the phase-1a marker walk and regenerate via
   `repos_sync.py --write`.
   Correct severity, which an early survey overstated: the hook exits at :47 unless
   CLAUDE_CODE_REMOTE=true, so it never runs in a local CLI session. It is a remote/web-session defect,
   not a local one — real, but not the dominant local risk.
   Fixing root discovery is NOT sufficient on its own: the one-level fan-out must move too —
   :426 (the ensure_full_clone unshallow loop), :470 (install_workspace_settings, which would write a
   bogus .claude/ root INTO a family directory, every guard passing), and :564 (the PYAUTO_ROOT export,
   which poisons every downstream consumer). Coverage exists in PyAutoMind/tests/test_session_bootstrap.py
   and tests/test_session_hook_sync.py.

2. Renumbered — the smoke shims moved OUT of this task. They are
   `draft/maintenance/pyautobrain/workspace_smoke_shim_bootstrap.md`: 12 repos, no propagation
   mechanism, and the 12 files are NOT copies (12 distinct checksums, 5 shape-classes). That task
   carries the prior question of whether 12 divergent copies of one bootstrap should exist at all.

3. **The 7 tracked Python files that hardcode an absolute workspace path.**
   Only one is a genuine cross-repo reference and the only one a regroup actually breaks:
   `PyAutoReduce/scripts/reduce_cosmos_web_ring.py:34` ->
   `/home/jammy/Code/PyAutoLabs/autolens_assistant/dataset/imaging/cosmos_web_ring/wavebands`.
   Also `PyAutoReduce/prototypes/` starred_vs_epsf_m92.py:30, starred_vs_epsf_omegacen.py:26,
   starred_vs_epsf_comparison.py:31, starred_epsf_spike.py:38 (all
   `Path.home()/"Code/PyAutoLabs/PyAutoReduce/scripts/output"`), and
   `PyAutoArray/files/ghost_peak_experiment.py:39`, `pca_rotation_experiment.py:28`
   (`~/Code/PyAutoLabs-wt/` inside docstrings).
   This corrects an earlier sweep that reported ZERO such files; an independent Codex review found them.

## Not in this phase

The physical move, the repos.yaml `path:` field, the ~12 root enumerators, worktree.sh and the
IDE/PYTHONPATH/symlink migration are phase 3. Also deferred there: the `smoke_install.sh` flat
`pip install ./PyAutoFit ./PyAutoArray ...` chain, which PyAutoHeart runs LOCALLY via
`heart/smoke.py:313` with `cwd=organism_root` (`smoke.py:229` builds `organism_root / repo` the same
way) — it is a shared CI+local script whose two callers would need different layouts, which is exactly
the ordering hazard the Codex review named. Do not introduce a universal `root / manifest.path` rule
before that is resolved.
