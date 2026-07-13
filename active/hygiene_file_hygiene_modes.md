# PyAutoBrain — hygiene file-hygiene modes (phase 5: crlf / config / artifacts)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 5 of the hygiene conductor — three **cheap, org-specific** pre-scan modes
chosen because they map to *documented recurring pain* in this codebase and
nothing currently catches them (evidence gathered 2026-07-11: no lint/ruff/vulture
in CI, 224 CRLF `.py` files in PyAutoArray, divergent library↔workspace config
yaml key sets). All three are conductor-only (PyAutoBrain) — cheap file/git scans,
**no Heart legs** (point-in-time debris/surface, not over-time regression signals).

**`crlf` (debris).** `git grep -Il $'\r$' -- '*.py'` across the managed repos;
count files with CRLF line endings (immediately surfaces the ~224 in PyAutoArray —
the documented "CRLF files… 10× diffs" gotcha). Fix hint: `sed -i 's/\r$//'` /
`dos2unix`; delegate → `/refactor`.

**`config` (surface).** Diff each library's `config/*.yaml` against the matching
workspace config (autofit/autogalaxy/autolens pairs); flag keys present in the
library config but **missing downstream** — the "mirror new library config keys
into workspace configs" chore. Use a small stdlib+PyYAML helper
(`_hygiene_config.py`) for a proper *recursive* key diff (top-level-only would
miss nested drift, which is where it actually happens); degrade gracefully if
PyYAML is absent. Delegate → `/refactor` (mirror the keys).

**`artifacts` (debris).** Flag tracked files that look like leaked generated
data/outputs — generated-data extensions (`*.fits *.hdf5 *.npy *.npz *.pkl *.pt`)
and `output/` paths — that should be gitignored (the "ship_workspace leaks binary
outputs" pattern). Low false-positive by targeting data extensions + output dirs,
not a blanket size scan. Delegate → gitignore + `git rm --cached` (or
`/repo_cleanup`).

**Wiring:** add the three to `MODE_ORDER` / `MODE_KIND` / `MODE_DELEGATE` and the
`prescan()` dispatch in `agents/conductors/hygiene/hygiene.sh`; update the modes
table (`AGENTS.md`) and the `/hygiene` veneer. They join the default ranked
worklist like the other debris/surface modes. Stdlib/bash + one PyYAML helper —
the conductor still never imports the science stack.

**Boundary/doctrine:** these are demonstrated-need additions (each maps to a
recorded recurring bug), not symmetry. Kept cheap so they belong in the fast
default scan (unlike the off-tick perf legs).

**Done when:** `hygiene {crlf,config,artifacts}` each emit a real count + delegate
(human + `--json`); the default run ranks them; PyAutoBrain tests cover each
pre-scan's classification + the config helper's recursive diff on a fixture.

<!-- filed 2026-07-11 from the "what checks should we add?" discussion; grounded in
     the no-lint-in-CI / 224-CRLF / config-drift evidence. Cheap org-specific trio. -->
