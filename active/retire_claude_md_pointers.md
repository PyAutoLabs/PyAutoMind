# Retire the CLAUDE.md → AGENTS.md pointer files (AGENTS.md is native now)

Type: maintenance
Target: pyautomind
Repos:
- @PyAutoMind
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07

## Request (verbatim, from the 2026-10-07 token-efficiency review)

> Do a review of the Pyauto ecosystem, mostly with a view to ensure we have
> things set up to ensure efficient token use, we do this routine review quite
> often. Note that claude supports AGENT.md now so maybe we can remove all
> CLAUDE.md? [...] yes do 1, sort other findings [...] Make sure you dont do a
> change which would impact codex or other agents.

## Measured facts (Claude Code 2.1.292, tested 2026-10-07)

- Claude Code ≥ 2.1.277 loads `AGENTS.md` natively (built-in plugin
  `cc-plugin-agents-md`, default mode `claude-md-or-agents-md`).
- In that mode **any CLAUDE.md in the cwd or an ancestor makes the engine ignore
  every AGENTS.md** (ancestor, cwd and nested). With no CLAUDE.md in the chain,
  ancestor + cwd AGENTS.md load at start and nested ones load lazily on first
  Read — exactly how CLAUDE.md behaves today. So the 46 per-repo pointer files
  and the unversioned workspace-root `CLAUDE.md` must all go together.
- A file CLAUDE.md `@`-imports is never loaded twice, so the pointers cost no
  tokens today; this is hygiene (46 files, a lint leg, generator code, tests).
- Codex, Cursor etc. read AGENTS.md directly and never read CLAUDE.md, so
  removing the pointers cannot affect them.

## Scope (this repo only)

1. `scripts/repos_sync.py` — invert the pointer lint. Today
   `check_claude_md_pointers` (L1353-1374) reports a repo that *has* AGENTS.md
   but no CLAUDE.md pointer. New rule: a repo that has AGENTS.md must have **no**
   `CLAUDE.md`. **Keep the check-leg name `"CLAUDE.md → AGENTS.md pointers"`
   byte-identical** — `PyAutoHeart/heart/checks/manifest_drift.py` parses the
   `--check` output by that name (`tests/test_manifest_drift.py:52-57`) and must
   need no change. Replace `write_claude_md_pointers` with a removal leg that
   deletes a `CLAUDE.md` only when it is a content-free pointer (matches
   `CLAUDE_IMPORT_RE` and has no other non-comment, non-heading prose); a
   CLAUDE.md with real content is reported as a problem, never deleted. Drop
   `CLAUDE_MD_POINTER`; update `GENERATED_TOP_LEVEL` (L1420-1441), the structure
   lint agreement, the docstrings at L65 and L105, and the section comment at
   L1295-1305.
2. `.github/workflows/session_hook_propagate.yml` — let the propagation job
   carry the pointer removal (a deletion of a content-free file is the same
   class of byte-trivial change as the hook copies it already pushes). It must
   honour `dry_run`; document it in the header comment. The real dispatch stays
   human.
3. `scripts/spawn.py` — stop writing `wiki/CLAUDE.md` in templates (L726) and
   drop the `wiki/CLAUDE.md` row from the template doc (L425); KEEP rules may
   stay tolerant. Update `docs/pyautobrain/spawn_spec.md` (L36, 68, 71, 72).
4. Tests: `tests/test_repos_sync_structure_lint.py` (L32-178),
   `tests/test_session_hook_sync.py` (L485-529), `test_spawn_template_contract.py`,
   `test_spawn_privacy.py`. Add a test that a content-bearing CLAUDE.md is
   reported, not deleted.
5. New `policy/hpc_ral.md` holding the "HPC access (RAL, GPU)" section verbatim
   from the workspace-root AGENTS.md (text below), so the root can shrink to a
   three-line pointer stanza that keeps the two hard rules (CPU arrays never on
   `gpu`; never reorder/hold/cancel another campaign's jobs). Draft that stanza
   in the PR body; the root file is unversioned and the human session edits it.

### HPC section to move (verbatim from root AGENTS.md)

- Cluster is RAL: connect via SSH alias `euclid_jump` (→ euclid-saas.roe.ac.uk, user `jnightin`), which `ProxyJump`s through `jump_finan`; aliases + keys are in `~/.ssh/config`. Projects live under `/mnt/ral/jnightin/<project>`.
- The PyAuto stack on RAL is a virtualenv under `/mnt/ral/jnightin/PyAuto` (`PYAUTO_HPC_BASE`, sourced by `activate.sh`) that mirrors this local install, with the library `main`s kept in sync — check/refresh that sync with `HPCPullPyAuto`.
- Drive GPU runs with the project's `hpc/sync` CLI: `hpc/sync push-submit gpu <script>` submits a SLURM `gpu`-partition array (one dataset per array task; JAX auto-uses the GPU), then `hpc/sync jobs` / `tail gpu` / `pull`. You may run these directly from a CLI session on your machine; in a cloud/web session there's no SSH access or keys, so treat this as context only.
- **CPU arrays never go on `gpu` (human rule, 2026-09-30).** Bulk/production CPU-only arrays use `--partition=ral` only — never `gpu`, `ral,gpu` or `gpu,ral`, even when ral is drained or busy (wait for ral). On 09-30 euclid_dr1 `ral,gpu` CPU arrays took all 124 CPUs on euclid-ral-gpu-1/-2 and left all 8 A100s idle but unschedulable for hours. Only exemption: small CPU timing legs on `gpu` without `--gres` with ≤8 CPUs/task, throttle ≤`%2`, and no pending GPU jobs (`squeue -p gpu -t PD` shows no gres/gpu). Partition ≠ device: check TRES for gres/gpu with `scontrol show job` before calling it a GPU run; for a stuck A100 job compare node AllocTRES cpu vs CfgTRES.
- Never reorder, hold or cancel another campaign's jobs without the human's OK.

## Out of scope

- The 46 per-repo deletions themselves (the propagation job does them after
  this merges, human-dispatched; dry run first).
- `repos.yaml` role-text trims (would regenerate 8 organ map blocks — its own wave).
- PyAutoBrain's stale CLAUDE.md references — sibling prompt
  `draft/maintenance/pyautobrain/absorb_claude_notes_into_agents_md.md`.

## Done when

`python3 scripts/repos_sync.py --check` passes on a workspace with no
CLAUDE.md files and fails naming any repo that still has one; the Mind test
suite is green; `--write`/the propagation job remove only content-free pointers.
