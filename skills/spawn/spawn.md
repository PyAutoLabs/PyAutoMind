# Spawn: Stamp the Fresh-Slate Templates

Regenerate the PyAutoScientist fresh-slate templates
(`PyAutoMind-template`, `PyAutoMemory-template`) from the live Mind and
Memory checkouts, and optionally publish them. A **PyAutoMind primitive** —
the generator and its partition rules are
`scripts/spawn.py` + `docs/pyautobrain/spawn_spec.md`; this skill only
drives them. Change the spec first, then mirror the tables in the script.

## Usage

```
/spawn              # dry-run: file plan + canary scan (default, read-only)
/spawn --apply      # regenerate AND force-sync the published template repos
```

## Steps

1. **Dry-run first, always:**
   `python3 PyAutoMind/scripts/spawn.py` — report the plan. Any
   `UNMATCHED` file is a **human decision**: a new file class in Mind or
   Memory needs a partition rule in the spec before spawn may run clean.
   Never classify ad hoc.
2. **On `--apply`** (human-confirmed):
   - `python3 PyAutoMind/scripts/spawn.py --write <scratch>/templates`
   - For each template repo: clone `PyAutoLabs/<name>-template`, replace
     its content with the regenerated tree (preserve `.git`), commit
     `"spawn: regenerate from <source-sha>"`, push. This force-sync is the
     **one sanctioned exception** to never-rewrite-history — these repos
     are generated views (their READMEs say so); never apply this
     treatment to any other repo.
3. Verify: `python3 PyAutoMind/scripts/spawn.py --check <scratch>/published-clones`
   exits 0, and the `Spawn Drift` workflow (`.github/workflows/spawn_drift.yml`)
   is green on its next run.

## Notes

- spawn never mutates the live repos; `--stamp-family` (the PyAutoProject
  family's mechanical layers) is separate and writes into family checkouts
  you point it at.
- The canary scan failing means instance content leaked past the partition
  rules — stop and fix the rules, never the output.
