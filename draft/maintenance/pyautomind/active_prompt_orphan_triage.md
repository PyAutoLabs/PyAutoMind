# Triage the 8 orphaned active/ prompts, then make `orphans` a gate

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

`scripts/lifecycle.py orphans` reports **8 of 10** prompts in `active/` that no
registry entry claims. Each is work whose state nobody is tracking. Triage them,
dispose of each, then flip the reporter into a gate.

## Background

`check` gained registry-integrity validation on 2026-08-08
(`draft/maintenance/pyautomind/registry_integrity_check.md`), covering the
direction **registry → prompt**: every `prompt:` path resolves, exactly, into
the state folder its registry implies. The audit that motivated it found six
`planned.md` entries for work that had already shipped — including the whole
M0–M3 release-validation milestone chain.

`orphans` is the mirror direction, **prompt → registry**, and it was added in
the same pass but deliberately left **report-only**: it exits 0 unless given
`--check`. Wiring it into `check` immediately would have left the tree red with
8 findings, and a red gate nobody can turn green gets ignored or disabled. The
condition is only worth gating once the backlog is at zero.

## The inventory (2026-08-08)

```
active/benchmark_calibration_runs.md
active/ep_optimise_expose_updater_delta.md
active/euclid_eceb_editorial_revision.md
active/fix_workspace_start_here_colab_links.md
active/matplotlib_inline_standalones.md
active/pyautoreduce_slacs1430_acs_comparison.md
active/research_profiling_experiment_in_the_autolens_pr.md
active/workspace_version.md
```

**One is already diagnosed.** `ep_optimise_expose_updater_delta.md` belongs to
the `ep-optimise-updater` entry in `active.md`, which records
`status: COMPLETE 2026-08-08` with both PRs merged (PyAutoFit #1457 →
`3b960609`, autofit_workspace #136 → `cf8b4077`). That is finished work still
sitting in `active.md`, so it wants the normal ship disposal:
`lifecycle.py record ep-optimise-updater --date 2026-08-08 --from-file <body>
--prompt ep_optimise_expose_updater_delta.md --apply`, which writes the record,
folds the prompt and drops the `active.md` section in one step. The entry
already carries enough substance for a rich record. It is an orphan only
because the entry declares no `prompt:` field and the slug does not match the
filename stem.

The remaining seven need the same question answered individually: **shipped,
still in flight, or abandoned?** Answer it against the upstream repo, not from
the prompt's own text — that is the lesson of the M0–M3 chain, where every
prompt still read as pending while the capability was live on `main`.

## Disposal per outcome

- **Shipped** → `lifecycle.py record <slug> --date <YYYY-MM-DD> --from-file
  <body> --prompt <name> --apply`. If the record has to be reconstructed after
  the fact, say so in it and cite the upstream commit/PR — see
  `complete/2026/06/build-testpypi-rehearsal-mode.md` for the shape.
- **In flight** → add the missing `active.md` entry, including a `prompt:`
  field so the claim is by path rather than by slug coincidence.
- **Abandoned** → `complete/archive/shelved/`, or `condemned.md` if it is
  self-material for the Gut's transit-and-void lifecycle.

## Then close the loop

Once `lifecycle.py orphans` reports none:

1. call `orphan_prompts(ROOT)` from `cmd_check` so the condition becomes drift,
   and delete the report-only carve-out documented in `cmd_orphans`;
2. move the three orphan tests in `tests/test_lifecycle_check.py` under the
   `check` legs alongside the registry ones;
3. consider requiring a `prompt:` field on every `active.md` entry that has a
   prompt file. Slug-matching exists only because entries predate the
   convention, and it is the weaker claim — `ep-optimise-updater` shows a real
   entry and its real prompt failing to match on name alone.

## Acceptance

- `python3 scripts/lifecycle.py orphans` prints `none`.
- Every disposal is evidenced: a `complete/` record with an upstream
  commit/PR, a new `active.md` entry, or an archive/condemned move.
- `orphans` is called from `cmd_check`, and `pytest tests/` is green.
