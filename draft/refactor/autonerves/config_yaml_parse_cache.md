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
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10

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
