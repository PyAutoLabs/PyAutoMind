# Science projects: hardware selection via `auto`, verify imaging behaviour

Status: draft — parked 2026-11-26, human resumes 2026-11-27. Do not start before then.

## Request (verbatim)

> we had science runs on slacs, cowls, 0946 get confused or be inconsistent on using the right
> hardware (JAX or numba on GPU or CPU). It should be Science projects dont try to specify in the
> python scripts now but it all comes via auto. update Science projects to use auto and verify for
> imaging we get the rightr behaviour based on logs in those chats. dont start this now ill resume
> it tomorow

## Scope

- Science projects under `~/Science/Science/active/` for SLACS, COWLS and 0946 (SDSSJ0946).
- Remove hand-set backend/hardware choices from their Python scripts (JAX vs numba, GPU vs CPU,
  e.g. `use_jax=...`, env-var or device forcing) so selection comes from the libraries' `auto` path.
- Verify, for imaging fits, that `auto` picks the right backend and device: check the run logs
  and the earlier chat sessions for those three projects, where the confusion was seen.

## Notes for the resuming session

- Read `Science/Science/AGENTS.md` and each project's own `AGENTS.md` first.
- Find what `auto` resolves to in the current stack before editing (library side, not guessed).
- If `auto` itself chooses wrongly for imaging, that is a library bug: file it separately, don't
  patch around it in the science scripts.
- Plan before editing; laptop pilots only, real runs on RAL per `policy/hpc_ral.md`.

## Added 2026-11-26: check the two-job split on RAL

Request (verbatim):

> also when we do this tomorrow also investigate if this is true on RAL Why two jobs: JAX and the
> Nautilus process pool can't share a process, so source_lp gets its own job. Job B reloads A's result.

- Find where this claim is made (job scripts, READMEs or comments in the science projects' RAL
  submission setup) and test whether it still holds on RAL with the current stack.
- In particular: can a JAX fit (earlier pipeline stages) and a Nautilus CPU process pool
  (`source_lp`) run in one process or job, or does the pool genuinely break or hang after JAX
  has initialised? Run a small pilot on RAL rather than reasoning from memory.
- If one job works, the A → B split (job B reloading job A's result) may be unnecessary; if it
  is still needed, record why in the project docs. Tie the answer into the `auto` change above.
