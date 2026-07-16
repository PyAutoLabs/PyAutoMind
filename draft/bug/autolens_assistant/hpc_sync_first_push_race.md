# hpc/sync first-push race — parallel rsyncs before remote base dir exists

Type: bug
Target: autolens_assistant
Repos:
- autolens_assistant
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Bug in autolens_assistant hpc/sync: on the FIRST push to a new remote project, push() launches the CODE_DIRS rsyncs in parallel before anything has created the remote base directory, so all of them fail with 'mkdir failed: No such file or directory' (rsync only creates one path level). The '[root files]' rsync then creates the base dir, so dataset/ syncs and the overall command exits 0 — the failure is silent until sbatch can't find hpc/batch_gpu. Fix: ssh mkdir -p the remote project dir before the parallel rsyncs (or add --mkpath). Found during slope_hierarchy first push (job 330464 postmortem, 2026-07-16).

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->
