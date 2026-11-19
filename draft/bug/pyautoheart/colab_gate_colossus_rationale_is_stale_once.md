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
