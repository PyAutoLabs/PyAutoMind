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
