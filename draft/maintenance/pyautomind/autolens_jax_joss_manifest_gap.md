# `autolens_jax_joss` is missing from the body map, and `repos_sync.py` structurally cannot see it

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Themes:
- mind-workflow
- hygiene
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Consequence: glance
Witness: `repos.yaml` lists `autolens_jax_joss`; the regenerated routing table in the workspace-root `AGENTS.md` carries its row; and `python3 PyAutoMind/scripts/repos_sync.py --check` reports a checkout that is on disk but absent from the manifest as DRIFT — demonstrated by temporarily removing one manifest entry and seeing the check go red, where today it stays silent.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-18

## The omission

`autolens_jax_joss` exists **on disk** in this workspace **and on GitHub**
(`PyAutoLabs/autolens_jax_joss`, public — confirmed 2026-09-18 via `gh repo view`), but
is **absent from `PyAutoMind/repos.yaml`**. It holds 7 live benchmark files under
`benchmarks/`, and a Mind draft already refers to it
(`draft/feature/autolens_jax_joss/autolens_jax_joss_benchmark_repo.md`).

## The blind spot that hid it

`python3 PyAutoMind/scripts/repos_sync.py --check` reports
**"37 of 37 checked out, 2 excluded"** — a clean bill of health — because it
drift-checks **manifest → disk only**. It walks the entries in `repos.yaml` and asks
whether each is present and whether its `git remote` agrees. It **structurally cannot
see a checkout that is not in the manifest**, so an unlisted repo is not a failure, it
is silence.

The consequence is not cosmetic: the repo is invisible to **every manifest-driven
sweep**, including the audit whose whole job was to answer *"did we miss a repo?"*.
It was found only because a separate AST sweep walked the filesystem.

## Two deliverables

1. **Add the repo to `repos.yaml`.** Category `project` alongside `autolens_profiling`
   / `autolens_inference`, with a one-line role, then
   `python3 PyAutoMind/scripts/repos_sync.py --write` to regenerate the routing table
   in the workspace-root `AGENTS.md` and the owner map in
   `PyAutoBrain/skills/WORKFLOW.md`. Check whether it also needs adding to the
   `PAT_PYAUTOLABS` repo list (memory `PAT403`: a newborn repo missing from that list
   propagates 403s).

2. **Add a disk → manifest check.** A checkout present in the workspace and absent from
   `repos.yaml` should register as **DRIFT**, not silence. Decide how deliberate
   exclusions are declared (there are already 2 excluded entries) so the new check has
   a legitimate way to stay quiet, rather than growing a hard-coded skip list.

## Not this prompt

The **2 pre-existing YELLOW remote-session-block mismatches for PyAutoHeart /
PyAutoHands** are unrelated to this and are already acknowledged. Do not fold them in.

Related and worth reading before starting, but separable:
`draft/refactor/pyautomind/repos_sync_check_dedup.md` collapses the eleven `check_*`
functions into one declaration per generated surface — if that refactor is done first,
the new check is one more declaration.

Filed 2026-09-18 from the flat-`fields=` adoption sweep's follow-up audit
(issue autolens_workspace#561), which found the repo while sweeping for remaining
`fields=` consumers.
