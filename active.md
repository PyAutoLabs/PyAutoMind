
## hpc-tmpdir-slurm-default
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1769
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hpc-tmpdir-slurm-default
- repos:
  - PyAutoFit: feature/hpc-tmpdir-slurm-default
  - autofit_assistant: feature/hpc-tmpdir-slurm-default
  - autofit_inference: feature/hpc-tmpdir-slurm-default
  - autogalaxy_assistant: feature/hpc-tmpdir-slurm-default
  - autolens_inference: feature/hpc-tmpdir-slurm-default
  - autocti_assistant: feature/hpc-tmpdir-slurm-default
- prompt: active/hpc_tmpdir_slurm_default.md
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary (human: "fix the TMPDIR=/tmp gap now too", 2026-11-12)
- heart-ack: YELLOW (PyAutoArray open PR 8d old) acknowledged by the human 2026-11-12 for this HPC fix line

## jax-floor-0-12
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/215
- issued: 2026-11-11
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-floor-0-12
- repos:
  - PyAutoHeart: feature/jax-floor-0-12
  - PyAutoNerves: feature/jax-floor-0-12
  - PyAutoHands: feature/jax-floor-0-12
- prompt: active/raise_jax_floor_to_0_12.md
- research: https://github.com/PyAutoLabs/PyAutoNerves/issues/213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, approved 2026-11-11)
- tier: judge — merge mode: human /prm (authorized in session: "/prm each phase when green"); release human-required
- phases: 1 validate jax 0.12 (Heart PR + local CPU/GPU + quarantined reruns) → 2 Nerves pins/README/Colab → 3 library floors autonerves>2026.11.9.1 + un-quarantine → 4 release validate + human version/approval
- blocked-phase-3: PyAutoArray/PyAutoGalaxy/PyAutoLens claimed by magnification-maps-wiring (Lens#818); euclid_strong_lens_modeling_pipeline claimed by sky-orientation-p2; ask the human at phase 3
- phase-1: DONE 2026-11-12: 0 hangs on 0.12 (15 runs, 4 cores); unit suites CPU+GPU (CUDA 12/13) clean vs 0.11.2 controls; regression = grad through zero contour (draft/bug/autogalaxy/zero_contour_grad_fails_on_jax_0_12.md); human: proceed, NEEDS_FIX the 2 scripts
- scope-added: PyAutoHands release.yml 3 jax pins (phase 2); smoke_install.sh jax asserts in alwt/agwt/euclid (phase 3); 2 #683 re-pins (alwt delaunay_mge/delaunay)
- nightly: PAUSED 2026-11-12 10:19Z (NIGHTLY_RELEASES=false, human) until the floor lands; re-arm after
- decisions: Colab upgrades jax/jaxlib/numpy(+cuda plugin) and prompts a restart; consumer floor autonerves>2026.11.9.1
- heart-ack: YELLOW acknowledged in session 2026-11-11

## magnification-maps-wiring
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/818
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-maps-wiring
- repos:
  - PyAutoArray: feature/magnification-maps-wiring
  - PyAutoGalaxy: feature/magnification-maps-wiring
  - PyAutoLens: feature/magnification-maps-wiring
- prompt: active/magnification_maps_8d_wiring_pretty.md
- epic: cluster-strong-lensing (phase 8d)
- tier: judge — merge mode: human /prm (PyAutoArray → PyAutoGalaxy → PyAutoLens)

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## sky-orientation-p2
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/115
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: (none; removed 2026-11-06)
- repos:
  - euclid_strong_lens_modeling_pipeline: (no branch; phase 2 done 2026-11-06 pending human check of the preview; phases 3-5 next)
- site: 2026-11-06 north-up thumbnails pushed to ECLIPSE_lens_catalogue feature/r2-pages-function-access (f68034d2, Pages deploy ok), _site/lenses rebuilt (RAL 414433), downloads.json → _release/dr1_v5_northup; old _release/dr1_v5 deleted (human OK)
- r2: 2026-11-06 north-up release → _release/dr1_v5_northup (RAL 414405) and per-lens site files refreshed in bucket root (414406/414426, rclone copy, check 0 differences); old _release/dr1_v5 kept
- 2d-pilot: 2026-11-05 RAL 414200+414205 → inspect/north_up_pilot_20261105_v2 (50 lenses, 431/431 fits pass witness; 1 sersic load_error). Review page Science/scratch/sky_orientation_dr1/north_up_pilot_20261105_v2/review/index.html — AWAITING human by-eye review; branch local (c4f1247), no PR yet
- 2d: pilot approved by human 2026-11-05; PR https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/120 open (judge → human /prm); FULL RUN RAL 414229 (80 tasks, 15,007 lenses) → inspect/north_up_full_20261105
- 2d-done: 2026-11-05 north-up release built (RAL 414376) → inspect/dr1_catalogue_v5_release_northup (release_name dr1_catalogue_v5, 76.12 GB, PNG-only diff vs skyframe passed); fit-frame fallbacks vis_pix 91 / multi_wavelength 66 / fit_sersic 8. NEXT: human /prm PR #120, 2b docs, R2 upload last
- merged: euclid#120 (2d north-up re-render) 2026-11-06 (1c7f24c); worktree + branch removed
- merged: euclid#121 (2b release docs) 2026-11-06 (4ce84a5); worktree + branch removed; RAL 414391 done 2026-11-06: final release inspect/dr1_catalogue_v5_release_northup, SHA256SUMS 26/26 OK, superseded builds removed
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 2: 2.0 land v5 branch → 2a catalogue fix → 2b–2e)
- heart-red-override: extended live by the human 2026-10-31 to phase 2 ("Yes, extend it"); development only, merge via /prm
- merged: euclid#116 (2.0 land v5 branch) 2026-10-31
- merged: euclid#117 (2a catalogue frame fix) 2026-10-31
- run: 2c DONE — 413892 live bundle (29,929 coolest regenerated, WCS on 74,772 FITS, 0 errors); re-package 414041 → inspect/dr1_catalogue_v5_release_skyframe (20 parts, 88.24 GB, verified); JSON hard-rule diff vs 10-29 PASSED (inspect/json_diff_skyframe_vs_20261029.txt); 414110 relink rebuilds docs with project-relative snapshot.json paths (2026-11-03). R2 upload deferred to the very end (human 2026-11-03). NEXT 2d north-up re-render pilot (~50, human review), 2b docs
- tier: judge — merge mode: human /prm
- merged: euclid#119 (catalogue parity `_EmptyRow` stub hotfix, human-authorized 2026-11-05 under this claim) 2026-11-05
- 2d-plan: APPROVED by human 2026-11-03 ~18:10 (not started; nothing written yet). scripts/tools/render_north_up.py on branch feature/sky-orientation-p2d: read each zip's image/dataset.fits + files/tracer.json + image/adapt_images.fits + image/adapt_image_plane_mesh_grids.fits; flipud arrays/adapt images, mesh grid + positions y->-y, tracer via sky_frame.plus_y_north_from; re-solve FitImaging at max-L (no search); WITNESS log-L == stored to ~1e-6 every lens, data panel vs rgb_north_up.jpg, positions on arcs; library subplot_fit + image_with_positions, util.subplot_rgb on rgb_north_up.jpg, segmentation from FITS, fit_multi_wavelength per band from output_sed; N/E compass. Pilot ~50 (paper lenses + grade-stratified random + asymmetric) as 2-CPU/5GB ral jobs -> inspect/north_up_pilot_20261103/ + side-by-side review page. Then full run, re-package, 2b docs; R2 upload last.
- merged: euclid#122 (RGB-panel compass + release docs) 2026-11-10 (fbfd7a3); ECLIPSE#6 downloads.json (5d3d68a). Re-render 414683, release 414768 (SHA 26/26), R2 re-upload 414791 + per-lens 414790 (0 differences). Phase 2 COMPLETE; #115 open for phases 3-5. Worktree removed.

## results-library-p5a-assistant
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/176
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: workspace-shipped, awaiting-merge (judge → human /prm; wiki-currency waits on a PyAutoFit release)
- worktree: ~/Code/PyAutoLabs-wt/results-library-p5a-assistant
- repos:
  - autolens_assistant: feature/results-library-p5a-assistant
- prompt: active/results_library_p5a_assistant.md
- epic: results-library (phase 5a)
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/177
- heart-ack: STALE 'release validation incomplete: no rehearsal for current source' (human 2026-11-02)

## gradient-correctness-sweep
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/517
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-correctness-sweep
- repos:
  - autolens_profiling: feature/gradient-correctness-sweep
- prompt: active/gradient_correctness_sweep.md
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/518 MERGED 2026-11-02 via /prm (32e13e85; items 10, 11 + sweep note). Umbrella stays open; further profiling-repo work re-syncs feature/gradient-correctness-sweep to main first
- phase: order approved 2026-11-02; done 10, 11 (PR #518), 12 (retired), 1 (re-filed narrower into draft/bug/autogalaxy/wrong_jax_gradient_on_mge_likelihoods_fd.md); item 2 IN PROGRESS (paused 2026-11-02 night, RAL 413991 PENDING)
- resume: (1) `sacct -j 413991` → when done pull output/p517_item2/{A_sparse_main,B_dense_main,C_sparse_tag}/…/gradient.json + .log from the RAL worktree into Science/scratch/gradient_correctness_sweep_2026-11-02/ral_item2/ and run small_step_check on them (A vs C = library effect incl #672; A vs B = sparse path vs CPU backend); (2) then items 3, 5 (local, seconds), 6, 13, 8/9/7 per the approved order in wiki/research/gradient_correctness_sweep.md
- compute-tracking: RAL 413991 (item 2, group/delaunay/euclid CPU, legs A sparse@main / B dense@main / C sparse@tag 2026.10.25.1; partition ral; human go 2026-11-02). RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/gradient-correctness-sweep (9d2ee2d3), private libs /mnt/ral/jnightin/PyAuto_wt/gradient-correctness-sweep; rows under output/p517_item2/<leg>/
- tier: judge — merge mode: human /prm

## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## nautilus-30d-diagnostics
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/12
- issued: 2026-11-10
- session: OpenAI Codex desktop
- status: awaiting-merge (full30D attribution completed; CI green; human merge)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-30d-diagnostics
- retained-repos: autofit_profiling (feature/nautilus-30d-diagnostics)
- coding-claim-transfer: same-session approved transfer to nautilus-compact-plot-adapter; PR13/worktree/raw data retained, no further edits on that branch.
- prompt: active/nautilus_30d_diagnostics.md
- epic: nautilus-fast-likelihoods (experimental phase0b.2; outside Pulse)
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/13
- commit: 2c3c0aaef3700754b9ec56ff506680f66c433f4b; attribution measurement375fa0be68e9c65436b466398eb560bf838650ba; prior corrected comparisonab896cd
- heart-red-override:
  - authorization: live phase0b development/pilot/PR despite RED; plot plan approved; "Allow one final-summary timing call per case"; fresh attempt "I approve, continue"; after harness correction "Run corrected comparison once"; attribution plan approved with "continue". No merge/release.
  - current-reasons: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure" (authoritative2026-11-10T15:48:37.310808+00:00).
  - gates:111tests,Ruff,catalogue,33links,synthetic runtime preflight,full30D finalization/PNG and integrity passed. Exact-head CI42849107773/job129944533530 every step green, including lychee. Prior failures retained; no independent review claimed.
- evidence: initial5D/10D fresh-sample successes; first30D120s timeout (partial logZerror−0.049803,ESS2633.6/10000), two repeats/output unrun.159.24s,~93MB retained; measured3cf17ea. Full30Daccuracy incomplete.
- output-followup: separate replay120.06s timeout inside visualization,123.19s total;~45MB retained; measured e701a77; unchanged copied checkpoint.
- retained-plot-attempts:01host guard before launch,all3unrun,6.438s at51663d1;02no-corner harness keyword collision before any timing call,22.364s,two unrun at9dbc272,~45MiB retained. Fixab896cd and regression; both failures retained.
- latest-plot-comparison:03no-corner success54.054s; six-parameter success62.278s (1200x1200PNG); full30D timeout120.092s during PNG export after9.997s axes and74.739s posterior plotting.242.32s total including4.518s preflight;~156MiB raw retained. Same12x12in/100dpi canvas and all33984samples; no defaults/library changes.
- prior-comparison-invariants: successes have exactly1summary timing call each,0new sampler calls, unchanged posterior/native34100count. All3copied checkpoints byte-identical. Full30D did not reach final summary and produced noPNG; no success receipt.
- attribution: full30D success114.77s,118.76s aggregate incl3.881s preflight,1037MiB RSS;1200x1200PNG/495axes verified. Drawing21.519s,plot-loop residual13.914s,hist dispatch residual10.793s,quantiles10.407s,binning0.785s,PNGwriting0.095s. SnapshotI/O4.112s. No optimization/speedup claim; earlier timing variation material.1summarycall/0sampling,posterior/native34100count unchanged,checkpointbyte-identical;~56MiB raw retained.
- next: human review/merge; no further compute authorized. Optimization candidates require a new scoped plan and matched repeats. Outside Pulse; fullphase0b/evidence accuracy incomplete.

## nautilus-compact-plot-adapter
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1762
- issued: 2026-11-10
- session: OpenAI Codex desktop
- status: awaiting-merge (bounded plotting experiment stopped at host guard; no further compute)
- prompt: active/nautilus_compact_plot_adapter.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-compact-plot-adapter
- retained-repos: PyAutoFit and autofit_profiling (feature/nautilus-compact-plot-adapter); worktrees and raw data retained
- epic: nautilus-fast-likelihoods (experimental phase1; outside Pulse)
- tier: judge — merge mode: human /prm
- heart-red-override: live approval for both plans despite RED; exact reasons "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". Development/validation/PR only; no merge/release/CI bypass.
- dependency: profiling branch starts from diagnostic PR13 head2c3c0aa; no automatic base merge. Existing archives retained. Checkpoint member1763 follows sequentially.
- coding-claim-transfer: same-session claims return to checkpoint member1763; plotting implementation/report published, no active edits.
- validation: measured e57611dc6 full suite4298 passes/2skips/1expected failure; final4996f422a65focused passes and exact-head Python3.12/3.13/nojax CI42865681739 green;10smoke cases;121tooling tests/Ruff/catalogue pass. Separate validation extras did not change retained measurement environment.
- pilot: attempt01 preflight halt2.145s/zero children, metadata paths corrected. Explicitly approved attempt02 at producer3bce28c completed5/6 then host-load guard535.88s total; two complete pairs2.022x/1.344x with identical PNGs, zero sampling and1summary timing call/case. Unpaired third baseline excluded. No retry. Report53ed047; all raw retained. Outside Pulse; full phase0b/evidence accuracy incomplete.
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1764
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/14
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1764

## nautilus-checkpoint-batching
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1763
- issued: 2026-11-10
- session: OpenAI Codex desktop
- status: awaiting-merge (bounded experiment complete; negative performance result; human review)
- prompt: active/nautilus_cpu_checkpoint_batching.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-checkpoint-batching
- retained-repos: PyAutoFit and autofit_profiling (feature/nautilus-checkpoint-batching); all worktrees/raw retained, no further compute
- epic: nautilus-fast-likelihoods (experimental phase1; outside Pulse)
- tier: judge — merge mode: human /prm
- heart-red-override: live approved both plans despite RED; exact current reasons "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure" (2026-11-10T16:45:59.194451+00:00). No merge/release/CI bypass.
- dependency: independent library baseline bdb7af0; profiling helpers from diagnostic PR13 head2c3c0aa. Plot member retained during validation; no simultaneous performance pilots.

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1765
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/15
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1765
- validation: fullsuite4302passed/2skipped/1expected failure,10smoke cases,125tooling tests/Ruff/catalogue; author review only. Frozen librarye16fba3ee/producerd108719; attempt01 halted after38.12s: interruption success, resume receipt error,18unrun/all timings unrun. Integer serialization fixed in daf0cc6; test portability4e90392, report15afe55. Read-only checkpoint reopening confirmed exact control result with zero likelihood calls and unchanged bytes; failed pilot case remains failed. Live human selected "Run corrected checkpoint pilot once". Attempt02 uses clean15afe55 (harness identical to approved daf0cc6), unchanged20children/120s/4096MiB/1800s limits; stop on first failure. Attempt02 halted46.74s at host-load guard after one interruption success44.94s;19unrun including resume/all timings. Saved checkpoint hash unchanged,4600recoverable/4800completed,200lost/0inflight. Report5206f0b, tooling CI42869583879 green; exact library3.12/3.13/nojax CI42867205132 green. Both attempts retained (~15.7MiB); no further compute or merge.

- fresh-pilot-approval: live human "Try the checkpoint pilot again once the host is quiet, with the same limits. Keep it outside Pulse and leave merge for me." Attempt03 authorized once, unchanged harness and20children/120s/4096MiB/1800s caps. Wait for three one-minute-load readings below1.0 spaced30s before launch; no change to in-run2.0 guard. Preserve attempts01/02/03.

- final-experiment: approved quiet-host attempt03 at producer5206f0b/librarye16fba3ee completed20/20 in931.93s, max88.91s/493.1MiB;4exact recovery controls and6exact sampling pairs passed. Native interval1 faster in all6: sampler21.2–48.8%/median28.1% longer with interval5, fullfit15.6–46.6%/median23.8% longer. Checkpoint time2.81–4.44x, syscall bytes2.37–2.62x. Negative result; keep native default, no promotion. Controlled loss200/500completed,0inflight, saved file hashes intact. Reporte1cebf8; all3attempts~120MiB retained. CI exposed existing /proc test reaping race; narrow test-only fix c06cae0. Final exact-head CI42877256638 passed all125tooling/Ruff/format/catalogue/link checks. Both draft PRs remain open for human review; no further compute. No merge/release/Pulse; widerphase0b incomplete.
- latest-heart: 2026-11-10T18:35:43.930077+00:00 RED: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "PyAutoCTI: 1 uncommitted source change(s)". Existing task-wide live RED development approval retained; unrelated CTI source untouched, no release or CI bypass.

## nautilus-spawn-training-pool
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/16
- issued: 2026-11-10
- session: OpenAI Codex desktop (session ID unavailable)
- status: workspace-dev (diagnostic and one corrected pilot approved2026-11-12)
- prompt: active/nautilus_spawn_training_pool.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-spawn-training-pool
- repos:
  - autofit_profiling: feature/nautilus-spawn-training-pool
- epic: nautilus-fast-likelihoods (experimental; outside Pulse)
- tier: judge — merge mode: human /prm
- heart-red-override: live human approved this bounded experiment despite RED; exact reasons "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "PyAutoCTI: 1 uncommitted source change(s)" (authoritative18:35:43Z). No merge/release/CI bypass.
- dependency: profiling starts diagnosticPR13 at2c3c0aa, carry c06cae0 test-only race fix. Read-only pinned Fitbdb7af0/Nerves9b204c9 and retained runtime; no installed source edits or dependency upgrade.
- authorization: max18children/120s/4096MiB each/1800s total including preflight and between-case waits. Four native networks, two spawned training workers, serial likelihood/adaptation. Quiet-host admission and stop-on-first-failure; no retries. Attempt01 executed once and stopped on its first failure; no rerun launched.

- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/17
- validation: 83530ce,145tooling tests,Ruff/check-format,catalogue pass; author review only. Six runtime correctness children passed; first timing child failed because Fit finalization removed its resume checkpoint. Correction retains a hard link before cleanup; native sampling/output settings unchanged. Exact-head CI42883149380 green.
- latest-heart: 2026-11-10T19:02:33.949929+00:00 RED: "PyAutoFit: 6 uncommitted source change(s)"; "PyAutoArray: 1 uncommitted source change(s)"; "PyAutoGalaxy: CI failure"; "PyAutoGalaxy: 5 uncommitted source change(s)"; "PyAutoLens: CI failure"; "PyAutoLens: 9 uncommitted source change(s)"; "PyAutoCTI: 6 uncommitted source change(s)". Live approval covers this bounded development experiment; unrelated canonical dirty sources are not pinned measurement dependencies. No release/merge/CI bypass.

- pilot-start: producer c9f6d2e exact-head CI42881651770 green. Quiet readings0.8862/0.6841/0.4131; one training-pool-01 attempt ran at frozen c9f6d2e.

- pilot-result: halted96.82s,6success/1error/11unrun,0complete timing pairs; exact four-network coefficient/prediction parity and both recovery witnesses passed, control16300evaluations/ESS10020.771588733165. Controlled likelihood loss0/inflight0; training seeds0/1 observed started (workers can advance before kill). Max25.00s/556.9MiB; no live descendants;~17MiB raw data retained. No speedup claim. Correction83530ce needs a new explicit decision for one fresh18-child/120s/4096MiB/1800s quiet-host attempt. No automatic retry, merge or Pulse.

- corrected-pilot-approval: live human selected "Run corrected pilot once" at83530ce. One fresh training-pool-02 attempt after quiet-host gate, same18children/120s/4096MiB/1800s; retain both, outside Pulse, human merge.

- corrected-pilot-admission: bounded quiet-host-02 watch ended without three consecutive readings below1.0; no training-pool-02 directory or child launched,0s pilot budget consumed. Approval remains valid for one corrected attempt at83530ce. Retained .session/quiet-host-02.jsonl and summary, no background watch.

- RAL-direction: live human "yeah we should be doing the real timing on RAL". Do not resume laptop quiet admission. Proposed one exclusive ral CPU-node job, four bound physical cores,8GiB/35min scheduler cap; original18children/120s/4GiB/1800s scientific limits. Same issue16/PR17; no source edits or job submission yet.
- RAL-blocker: configured jump_finan authentication rejected publickey/password/keyboard-interactive before reaching RAL; remote topology/runtime unverified. Concrete amendment saved in active/nautilus_spawn_training_pool.md for approval; no credential/config edits.

- RAL-implementation:352eafb,190tooling tests/Ruff/format/shell syntax/catalogue pass; author review only, exact-head CI42890122136 green. Allocation/cgroup/physical-core admission and single-job wrapper implemented, runtime inventory and RAL protocol saved. No RAL runtime evidence or job submission; user confirms existing route and will restore authentication. One approved job remains unused; no more laptop timing.
- RAL-heart:2026-11-10T19:52:15.059564+00:00 exactRED: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "autocti_workspace: Smoke Tests failure on main". Existing live experiment development override and explicit RAL-amendment approval retained; no release/merge/CI bypass.

- RAL-access-restored: user supplied working WSL SSH_AUTH_SOCK; using it explicitly per command reaches euclid-saas. No keys/config changed. Slurm22.05.11,ral up/idle nodes,OverSubscribe=NO,CR_CORE_MEMORY,task/affinity+task/cgroup,ConstrainCores/RAMSpace enabled. Shared Python3.12.4/scikit-learn1.5.1/numpy2.2.6 differ; do not change them. Isolated task staging under profiling/autofit_profiling_wt/nautilus-spawn-training-pool started; no job submitted.

- RAL-live-validation: producer107ec1c,194tests and exact-head CI42898804169 green; legacy Slurm22 TRES supported. Sources staged; isolated Python3.12.10/runtime in progress. No scientific job submitted. Heart2026-11-10T20:50:57.253679+00:00 RED: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "autocti_workspace: Smoke Tests failure on main"; existing experiment override, outside Pulse/human merge.

- RAL-bedtime-handoff: human requested resumable state. Task-owned installer/shell stopped and verified absent; no scientific job, child or watcher. Clean producer107ec1c/194tests/CI42898804169 green. Sources and partial Python3.12.10 extraction retained;88 binary pins resolve, two pure-Python utilities separated. Resume .session/RESUME.md (also Science scratch training/RESUME.md). Original one-job approval remains unused; outside Pulse/human merge.

- RAL-resume-2026-11-11: saved SSH agent socket absent; current path requested from human. Producer107ec1c/CI42898804169 unchanged green; fresh Heart08:47:27RED "autocti_workspace: Smoke Tests failure on main", existing override. Prepared .session/ral-resume-stage-03.sh, not executed. No remote writes or job; authorization unused.

- RAL-agent-restored-2026-11-11: new human-provided WSL agent restores both explicit-proxy and ordinary euclid_jump access. No prior pilot receipt or queued training job. Ral partition up,5idle nodes,OverSubscribe=NO. Runtime-only staging-03 active; retained log in task .session. Local ignored hpc/sync.conf targets the isolated task. No scientific submission; source107ec1c/CI green; existing limits/override unchanged.

- RAL-runtime-2026-11-11: staging04 installed Python3.12.10 and88 binary packages; utilities confirmed by staging05 after an SSH interruption. Runtime validation05 timed out at600s without a pass receipt; diagnostic validation06 adds phase markers/stack traces with1200s setup cap. No numerical sampling or job submitted. Fresh Heart09:53:07YELLOW, only "PyAutoArray: open PR 7d old". Source107ec1c/CI green; outside Pulse/human merge.

- RAL-runtime-cache-proposal: validation05 timed out600s; diagnostic06 exited139 during early module import (cause unresolved); isolated probe07 passed stdlib portion but timed out180s before baseline module completed, json37.325s/re26.467s cumulative. No science/job. Proposed local runtime/source cache with all outputs retained on NFS, same35min/4cores/8GiB and18children/120s/4GiB/1800s bounds; canonical amendment awaits approval before job-script edits. All setup processes ended and logs retained.

- RAL-cache-implementation: live human approved amendment. Producer c243ef676ffa15fc9e4808abc104a93c70bc8145;229 tooling tests/Ruff/format/shell/catalogue pass. Private RAL login-host local runtime passed full provenance in7.35s with90 exact third-party pins/native digest; no scientific work. Artifact09 checksum verified; fresh restore09 passed49.95s (53.29s including guarded cleanup), no sampling/training. Final retained-checkout staging timed out600s in NFS git status before checkout update; no submission environment/pilot output, no Slurm job submitted. Original single-job authorization unused; resume staging after NFS recovers. Heart receipt2026-11-11T10:45:45.346227+00:00 RED: "release validation FAILED (stage integrate)" under existing development override. NFS outputs/all science limits unchanged; outside Pulse/human merge.

- RAL-submission-2026-11-12: recovered current live user-owned SSH agent by matching prior public-key fingerprints, no key/config edits. Bounded NFS checks and final staging passed; retained producer clean atc243ef6, exact-head CI43015855847 green. Submitted ONCE via hpc/sync: job415132. Original authorization USED; no automatic replacement/requeue. Monitor this job, retain raw results; outside Pulse/human merge. Latest recorded Heart2026-11-11T13:01:05.642178+00:00 YELLOW, "PyAutoArray: open PR 8d old"; existing development authorization retained.

## simulator-roundoff-control
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/124
- issued: 2026-11-12
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/simulator-roundoff-control
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/simulator-roundoff-control
- prompt: active/simulator_round_off_control_test_obsolete.md
- tier: judge — merge mode: human /prm (human asked /bug then /prm 2026-11-12)
