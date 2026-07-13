# PyAutoScientist Phase 3a: spawn spec, template family seed, decisions locked

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

The judgment-tier slice of Phase 3, executed before Fable access ends
(2026-07-12). Design settled in
`docs/pyautobrain/pyautoscientist_phase3_research.md` — the four locked
calls (human-approved in-session 2026-07-10):

1. Template family (PyAutoProject / autoproject_workspace /
   autoproject_workspace_test) built as GitHub template repos —
   hand-seeded exemplar science (1D Gaussian), mechanical layers later
   stamped by spawn.
2. autoproject_assistant is the Clone/Mitosis agent's lightweight-seed
   mode — never hand-built; gated on clone implementation (3b).
3. Fresh slate = `spawn`: generated PyAutoMind-template / PyAutoMemory-template
   stamped from the live repos by partition rules; live repos stay live.
4. Nerves: promote PyAutoConf's role (body map + docs), defer repo rename,
   never rename the package.

## Deliverables (this prompt)

- `docs/pyautobrain/spawn_spec.md` — the partition rule set
  (structure-vs-content per file class for Mind + Memory + the template
  family's mechanical layers), written so 3b implementation is mechanical.
- The PyAutoProject family seeded: three repos with the 1D Gaussian
  exemplar (library: model + Analysis + packaged config; workspace:
  start_here.py in docstring-cell convention + config/general.yaml +
  config/build/copy_files.yaml; workspace_test: smoke script +
  smoke_tests.txt). Created private; flipping public is a human decision.
- 3b prompt series drafted (Status: draft, issued one-at-a-time as
  predecessors ship, per the no-bulk-issue rule).
- Nerves role promotion: repos.yaml role text update + repos_sync --write.

## Acceptance

- spawn_spec.md complete enough that an execution-tier session can
  implement spawn without judgment calls.
- Template repos pass: library tests green locally; start_here.py runs
  end-to-end; scripts follow the docstring-cell convention exactly.
- Zero diffs to organ code, skills, AGENTS.md; live setup untouched.
- repos.yaml role text change verified by repos_sync --check/--write.
