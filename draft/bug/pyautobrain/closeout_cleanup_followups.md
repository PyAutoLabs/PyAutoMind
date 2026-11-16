# Shift close-out clean-up follow-ups (from PyAutoBrain#634/#635)

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Consequence: glance
Priority: medium
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators
Lane: any

1. **Worktree removal after an unattended merge.** After autofit_workspace#185 merged, the watcher left the task's worktree and local branch behind; the lead removed them by hand. By reap time the claim naming the worktree is gone, and `worktree_remove`'s stale-claim guard reads the canonical `active.md`, which is stale during a shift. Make the close-out remove it, the way /prm does, or report it in the digest.
2. **In-turn notify merges skip the queue retirement.** A worker that merges in-turn (`notify`) leaves its `queue.md` entry live, and `lifecycle.py check` then fails.
3. `_orchestrator.py` `_SCOPE_FAILED_RE` misses newer systemd's "Failed to connect to user scope bus via local transport". Such a machine fails the spawn instead of falling back. This laptop runs systemd 249 and is fine.
4. `_digest.py` `prompt_url`: a prompt that only ever existed on a merged side branch gets no Mind link. No link is shown rather than a dead one.
5. `_orchestrator.py` ~2334: when a close-out merged without writing its complete record, the queue entry is still retired, and `shipped-as` names only the PR.

Witness: one offline test per item that fails on the code at 7be8e94ba.
