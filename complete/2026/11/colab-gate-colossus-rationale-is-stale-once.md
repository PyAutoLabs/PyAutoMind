The `colossus` accepted-miss in PyAutoHeart `heart/config/colab_gate.yaml` now says the los_halos simulator notebooks reach it and stop on Colab with an ImportError naming colossus and `autolens[los]` (accepted 2026-11-19), instead of "no workspace or HowTo notebook reaches the module".

Decision taken (PR labelled `decision-taken`, accepted by the human at /prm): the `hmf` entry is kept rather than removed, reworded "only released ≤2026.11.19.1; delete after next release". The released autolens 2026.11.19.1 on PyPI still imports hmf unguarded and the continuous check F audits PyPI, so without the entry check F fails. Deleting it after the next release is filed as `draft/bug/pyautoheart/colab_gate_delete_hmf_after_next_release.md`.

Witness: `verify_install.sh F` (continuous, PyPI stack plus an autolens_workspace main clone with the regenerated los_halos notebooks) PASS — accepted colossus (autolens/lens/los.py:207) and hmf (los.py:147) warnings, imaging cell OK. Heart tests 74 passed; targeted smoke selected no script; tenant firewall OK; independent Opus review CLEAN; Heart GREEN; CI GREEN at /prm. Not checked: the los_halos notebooks were not run on real Colab.

Shipped in PyAutoHeart#357 (https://github.com/PyAutoLabs/PyAutoHeart/pull/357), merged 2026-11-20 by human /prm. Issue https://github.com/PyAutoLabs/PyAutoHeart/issues/356. Done by shift worker 2026-11-19-pm2 (4cccb01f).

## Original prompt

# Colab gate: colossus rationale is stale once los_halos needs it

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: notify
Witness: `PyAutoHeart/heart/config/colab_gate.yaml` has no `hmf` entry, its `colossus` entry says the `los_halos` simulator notebooks stop on Colab with a clear ImportError naming colossus (accepted by the human 2026-11-19), and the Colab gate check passes against the regenerated autolens_workspace notebooks.
Review-minutes: 0
Unattended: ready
Verified: 2026-11-19 44f1e202 (PyAutoHeart)
Lane: any

## Finding

`@PyAutoHeart/heart/config/colab_gate.yaml:21-23` accepts `colossus` as missing on Colab on the
grounds that "no workspace or HowTo notebook reaches the module". After PyAutoLens#868 and
autolens_workspace#681 (LOSSampler moved from the broken hmf to colossus, shift 2026-11-19-pm),
the regenerated `los_halos` notebooks (`simulator.ipynb`, `simulator_jax.ipynb`) do reach it, so
that reason becomes false. The entry for `hmf` (line 23) is stale: nothing imports hmf any more.

## Ruling

The human, 2026-11-19: "fine for los_halos to stop in Colab". So **do not** add colossus to
`PyAutoNerves/autonerves/setup_colab.py` `_SHARED_EXTRAS`. On Colab those notebooks stop with
`ImportError: ... optional dependency colossus ... pip install autolens[los]`, which is accepted.

## Ask

1. Rewrite the colossus rationale to say exactly that (los_halos notebooks reach it; they stop
   with a clear ImportError on Colab; accepted 2026-11-19).
2. Remove the stale `hmf` entry.
3. Run the Colab gate against the notebooks regenerated after #681 merges.

Unblocked 2026-11-19: PyAutoLens#868 and autolens_workspace#681 merged (20:50Z, 20:52Z), so the notebooks exist.

## Provenance

[from: independent adversary review, Fable 5.2, shift 2026-11-19-pm] advisory 1 on PyAutoLens#868;
record `batches/2026-11-19-pm.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cef12910-5f37-434a-b812-60fddb7f44b6/scratchpad/intake/colab_gate_colossus_los_halos_rationale.md -->
