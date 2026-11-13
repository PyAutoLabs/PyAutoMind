## Outcome

The 2026.11.12.1 Colab bootstrap asked every Colab user to restart after a jax-only
upgrade (it restarted whenever numpy was loaded, and importing setup_colab loads
numpy), and Heart's Colab gate (check F) failed. Fixed on main 2026-11-12:

- PyAutoNerves#218 (5aa847f): upgrade only what is below the floor (jax+jaxlib
  together; numpy only if <2.2; the CUDA plugin with jax); raise
  ColabRestartRequired only if an UPGRADED module is already loaded. Tests: the
  live-Colab case and others; a control fails 5/8 on the released code. Local
  live-Colab simulation (jax 0.11.1 + numpy 2.4.6, real pip): jax upgraded, no
  restart, the same process then runs jax 0.12.0.1.
- PyAutoHeart#337 (9afbd3f): check F re-runs the setup cell once in a fresh process
  after a restart request (exit 4), as a user would; a second request or any other
  error fails. Tests run the real driver.
- Merged with Nerves#218's colab-gate leg red (human-approved): that gate audits the
  RELEASED bootstrap, so check F clears only after the next release.

## Original prompt

# Colab setup asks for a restart when nothing loaded was upgraded (check F red)

Type: bug
Target: PyAutoNerves
Repos: @PyAutoNerves @PyAutoHeart
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-12
Issued: 2026-11-12

## Evidence

The jax>=0.12 floor (PyAutoNerves#215/#216, released 2026.11.12.1) added
`autonerves/setup_colab.py::_ensure_jax_floor`. It raises `ColabRestartRequired`
whenever `"jax" in sys.modules or "numpy" in sys.modules` after upgrading. On
live Colab (manifest 2026-11-12: jax 0.11.1, jaxlib 0.11.1, numpy 2.4.6) it
upgrades only jax/jaxlib, numpy already meets >=2.2, and still demands a
restart because numpy is imported. Heart's Colab gate (verify_install check F)
fails `setup cell rc=1` (release-integrate run 43238247828,
`verify_install_release`, 2026-11-12):

    Upgrading JAX for PyAuto (found jax 0.11.1, jaxlib 0.11.1, numpy 2.4.6; ...)
    autonerves.setup_colab.ColabRestartRequired: JAX and NumPy were upgraded. Restart the runtime ...

Check F audits the RELEASED bootstrap, so Heart reads red here until a fixed
Nerves is published. While red, that also holds the nightly, which is harmless.

## Fix

1. Nerves: build the pip spec list only for packages actually below the floor,
   and raise `ColabRestartRequired` only if one of THOSE modules is already in
   `sys.modules` (jax/jaxlib → `jax`/`jaxlib`; numpy → `numpy`; CUDA plugin →
   `jax`). On Colab jax is normally not imported before the setup cell, so most
   users then need no restart. Update the message to name what was upgraded.
   Tests in test_autonerves/test_setup_colab.py: numpy already new + loaded and
   jax old + not loaded → no restart; jax old + loaded → restart.
2. Heart Colab gate emulation (heart/checks/colab_gate.py driver): on
   `ColabRestartRequired`, re-run the setup cell in a fresh process once, as a
   user would; fail only if the second run also fails.
3. Release (nightly or manual) to clear check F, which audits the released bootstrap.
