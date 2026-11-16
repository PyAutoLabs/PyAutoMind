Shipped in PyAutoNerves#212 (merged 2026-11-08, 9b204c9); issue PyAutoNerves#211 closed.

- New `autonerves/parse_cache.py`: each config YAML/JSON file parsed once per process (keyed on path +
  mtime + size, deep-copied on return); routed through YAMLConfig, JSONPriorConfig.from_directory and
  Config.logging_config.
- Witness: deep-compare test over every packaged config directory (plus a manual check over 8
  PyAutoFit/Array/Galaxy/Lens config dirs) equal; parses 468 → 148 in a simulated register sequence;
  config time 1.41 s → 0.56 s. 301 tests pass; unittest 3.12/3.13/nojax green.
- Not measured: end-to-end `visualization.py` ≥0.8 s speed-up (workspace not in the session).
- Library change: unreleased until the next PyAuto release.

## Original prompt

# Cache `autonerves` config parsing — 308 YAML files parsed per script run

Type: refactor
Target: autonerves
Repos:
- PyAutoNerves
Themes:
- performance
- ci
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: notify
Witness: The parsed config objects compare equal before and after (deep-compare test over every packaged config directory), YAML parses per script run drop from 308 to at most one per distinct directory (counted by a parse hook), and `visualization.py`'s run is faster by at least 0.8 s.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-10
Issued: 2026-11-08

Found by `/ci_speedup` (2026-09-10) while profiling the slowest CI smoke scripts.

`autonerves` parses **308 YAML files on every script run** — 186 of them inside
`json_prior/config.py:from_directory`, reached from only **5 call sites**. That
is roughly **1.5–2s of every PyAuto script's runtime**, in CI and on a laptop.

Because it is per-process fixed overhead, it does not show up as any one
script's problem — it is a flat tax on the whole scripts lane, and on every
tutorial and workspace example a user runs.

A library-level cache (parse once per directory, keyed on path + mtime) would
pay back across the entire lane rather than one script. Behaviour-preserving:
the parsed config must be identical, which is the acceptance test.

Measured on `autogalaxy_workspace_test scripts/imaging/visualization/visualization.py`,
where it is 1.0s of a 26.8s run — but the same 308 parses happen in every script
profiled during that audit.
