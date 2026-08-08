# active-prompt-orphan-triage

- shipped: 2026-08-08
- repos:
  - PyAutoMind
- follows: `complete/2026/08/registry-integrity-check.md`

## Summary

Triaged the 8 `active/` prompts that no registry entry claimed, disposed of
every one, and turned `lifecycle.py orphans` from a report into a gate — it is
now graded by `check`, and the `--check` opt-in flag is gone.

`lifecycle.py orphans` reports **none**.

## Disposals

**Shipped — recorded, dated from the actual commit:**

| Prompt | Record | Evidence |
|---|---|---|
| `ep_optimise_expose_updater_delta.md` | `complete/2026/08/ep-optimise-updater.md` | PyAutoFit#1457 `3b960609`, autofit_workspace#136 `cf8b4077` |
| `workspace_version.md` | `complete/2026/07/workspace-version.md` | autolens_workspace `21702119` — `minimum_library_version: 2026.7.9.1` in `config/general.yaml` |
| `fix_workspace_start_here_colab_links.md` | `complete/2026/07/fix-workspace-start-here-colab-links.md` | autolens_workspace `897465a6` — README Colab links now resolve to the root `start_here.ipynb` |

**Not shipped — parked with the evidence:**

- `matplotlib_inline_standalones.md` — VERIFIED INCOMPLETE. At least two of the
  five standalone `# %matplotlib inline` comments survive on autolens_workspace
  main (both `potential_correction/start_here.py`).
- `benchmark_calibration_runs.md` — VERIFIED NOT STARTED. `benchmarks/runs/` on
  autolens_assistant main still holds only `.gitkeep`; harness and prompt cards
  are in place, only the campaign is missing.

**In flight — claimed by an entry that lacked a `prompt:` field:**

- `research_profiling_experiment_in_the_autolens_pr.md` is the
  `group4-mge-search-benchmark` work (autolens_profiling#82/#83). The parked
  entry existed all along; it just never named its prompt.

**Unverifiable from a cloud session — parked, flagged as such:**

- `euclid_eceb_editorial_revision.md` and
  `pyautoreduce_slacs1430_acs_comparison.md` both work against local paths under
  `/mnt/c/Users/Jammy/Science/`. Their state can only be confirmed from the
  laptop, and the parked entries say so rather than guessing.

## Note on the two unverifiable entries

Parking them clears the orphan condition without asserting anything false, but
it is the weakest disposal here — a task parked because nobody could look is not
the same as a task parked on purpose. Re-check both from the laptop.

## Original prompt

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
active/euclid_eceb_editorial_revision.md
active/fix_workspace_start_here_colab_links.md
active/matplotlib_inline_standalones.md
active/pyautoreduce_slacs1430_acs_comparison.md
active/research_profiling_experiment_in_the_autolens_pr.md
active/workspace_version.md
```

**One of the original eight is already cleared.**
`ep_optimise_expose_updater_delta.md` was finished work (PyAutoFit #1457 →
`3b960609`, autofit_workspace #136 → `cf8b4077`) whose `active.md` entry read
`status: COMPLETE` with no `complete/` record. Recorded 2026-08-08 →
`complete/2026/08/ep-optimise-updater.md`. It had shown up as an orphan only
because its entry declared no `prompt:` field and its slug did not match the
filename stem — which is the concrete argument for the third closing step below.

`mge_sigma_min_workspace_sweep.md` was retired in the same pass (it was claimed,
so never an orphan): recorded to `complete/2026/08/`, with its undischarged
markdown debt split out to
`draft/docs/autolens_workspace/markdown_regeneration_sigma_min.md` so
completion did not swallow it. `active.md` now holds only the two release
drives.

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
