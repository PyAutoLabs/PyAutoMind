Pre-M3.1 fixes from the warm-up live shift `2026-11-14-pm` (epic `autonomous-orchestrators`). Shipped as PyAutoBrain#635 (7be8e94ba), merged 2026-11-14 on `ci-verdict` GREEN. Issue PyAutoBrain#634.

**Fixed:**
- **Links:** a digest or status task title now links to its PR, else the work repo's issue. The digest's Mind link is pinned to a commit, so it cannot 404.
- **Daemon:** workers and close-outs launch through `systemd-run --user --scope`, so the `claude --bg` daemon leaves the watcher unit's cgroup. They fall back to a plain launch, and nothing ever stops a daemon.
- **Wording:** outcome first, in plain words, with the detail on a smaller second line. Asked for by the human after a 5-minute phone review.
- **Firewall:** the worker template runs the tenant firewall before an organ push.
- **Queue:** an unattended close-out now retires the shipped task's `queue.md` entry in the same ledger commit. Lead follow-up: any failure in Mind's lifecycle code stays one op's failure.
- **N1:** a worker still out at review-at reads "still running at review time".

**Witness:**
- 10 new offline tests, each failing on origin/main.
- Brain suite: 2014 passed. The 1 failure is environmental, from the bundle's `PYAUTO_ROOT`.
- The real warm-up digest was re-rendered, before and after (`Science/scratch/m3_1_prep/warmup/render_634/`).

**Review:** independent Opus, CLEAN, with 5 follow-ups. The lead fixed 2. The other 3, plus the deferred items, are in `draft/bug/pyautobrain/closeout_cleanup_followups.md`.

## Original prompt

# Warm-up live shift 2026-11-14-pm: findings to fix before M3.1 shift A

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators
Lane: any

The first live shift with real workers (`batches/2026-11-14-pm.md`, PyAutoMind#569) passed its goal:
one unattended close-out merge (autofit_workspace#185, stage-2 row in `autonomy_log.md`, pilot row
with `actor: unattended-watcher`), a refusal on red CI (PyAutoHeart#347), the App-posted status
comment, and `/pause` + `/resume` each acknowledged within one tick. Human review took 5 minutes.
These items came out of it; 1–3 should land before shift A (Mon 2026-11-16 09:30Z).

1. **Digest task links 404 and point at the wrong place.** Each task title links to
   `PyAutoMind/blob/main/draft/...`, but by digest time the prompt has moved (draft → active →
   `complete/YYYY/MM/<hyphenated-slug>.md`), so the link is dead. The human, reading on a phone,
   wants the title to land on the work itself: the PR (or the work repo's issue), with the Mind
   record as a secondary link resolved at render time. Witness: open the first link in the
   PyAutoMind#569 digest → 404.
2. **Leftover `claude` daemon in the watcher's cgroup.** `claude --bg` started a transient
   `claude daemon run` plus `bg-pty-host` spares inside `pyauto-orchestrator.service`; they outlive
   the workers (1 h 07 m at 13:33Z) and systemd logs "Found left-over process … unclean termination"
   on every tick. Witness: `journalctl --user -u pyauto-orchestrator.service --since 13:33` and
   `ps -o pid,etime,args -p <pid>`. Fix: spawn outside the unit's cgroup (e.g. `systemd-run --user
   --scope`) or stop the daemon when no shift workers remain; decide which, and keep a tick from
   killing a live worker.
3. **Plainer wording in the status comment and digest.** Human: "could be slightly more logical
   and human readable … quite wordy but not too bad". Lead the line per task with the outcome in
   plain words (merged / needs you / failed CI), then the link; move tier, model, `why:` and slug
   into a smaller second line or the proof packet. Follow Brain `skills/WRITING_STYLE.md`.
4. **Token reservation is low.** Two small tasks measured 498 403 worker tokens (≈ 250k each) plus
   70 223 close-outs — 568 626 of 600 000. Brief A assumes 55k–190k per worker; re-check A's
   2.0 M budget and the 250k reservation against this (cache-read 13.8 M is outside the cap).
5. **Workers don't run the tenant firewall before pushing organ code.** PyAutoHeart#347 failed CI
   because `heart/timings.py` gained a literal `'PyAutoArray'` (firewall: instance facts in an
   unlisted file). The worker prompt for organ repos should run
   `python3 PyAutoMind/scripts/repos_sync.py --check --only "tenant firewall (organ code)"`
   before pushing. #347 stays open for `/prm` after a fix.
6. **Attribution note (no change needed now).** GitHub shows #185 `mergedBy: Jammy2211` because the
   watcher merges with the human's `gh` login; the pilot row and the stage-2 row carry
   `unattended-watcher (mergedBy Jammy2211)`, so the audit reads Mind, not GitHub. Revisit if
   merges move to the App.
