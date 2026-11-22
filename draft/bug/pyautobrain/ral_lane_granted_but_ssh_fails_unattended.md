# A brief can grant the `ral` lane while unattended ssh to RAL does not work

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: with a fake `ssh` that exits 255, `pyauto-brain batch brief --check` on a brief whose `lanes:` include `ral` prints one warning naming the host and the ssh error and still exits 0; with a fake `ssh` that exits 0, and on a brief without `ral`, it prints no such warning and runs no ssh.
Review-minutes: 5
Unattended: ready
Lane: any

## Finding

Shift 2026-11-20-am ran with `lanes: any local-dev ral` and a `ral-allowance:`. Its worker on
`sed_chain_waveband_fit_can_spin_forever` could not do the task's "reproduce before fixing" step:

    ssh euclid_jump → Permission denied … Too many authentication failures
    (unattended key auth through jump_finan)

It parked on a question (euclid_strong_lens_modeling_pipeline#136) after spending a
session. Nothing at launch said the lane was unusable: the brief check validates the allowance's
numbers, not that a worker can reach the host without a prompt.

## Ask

reproduce before fixing: `ssh -o BatchMode=yes -o ConnectTimeout=10 euclid_jump true` from the laptop exits non-zero with "Too many authentication failures" (if it now exits 0 the ssh side is fixed; still do the check below).

1. At `batch brief --check`, when the brief's `lanes:` include `ral`, probe the host once with
   `ssh -o BatchMode=yes -o ConnectTimeout=10 <host> true` and print one warning when it fails,
   with ssh's own last line. A warning, never a refusal: the human may be about to fix it. It runs
   in the launch chat, never in the watcher (PyAutoBrain `AUTONOMY.md` "The watcher's network
   surface"), and only for a brief that grants `ral`. Take the host name from where the HPC
   tooling already reads it; do not hard-code it in organ code (tenant firewall).
2. Out of scope for the PR, for the human on the laptop: "Too many authentication failures"
   usually means the agent offers every loaded key before the right one. `IdentitiesOnly yes`
   with a named `IdentityFile` on the jump host entries in `~/.ssh/config` is the usual fix. Say
   so in the PR body; do not edit the human's ssh config.

## Provenance

[from: orchestrator review 2026-11-22 of shift 2026-11-20-am, proof packet of sed_chain_waveband_fit_can_spin_forever]
