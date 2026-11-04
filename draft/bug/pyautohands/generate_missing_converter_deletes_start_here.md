# autohands generate: missing ipynb-py-convert deletes start_here.ipynb and leaves temp.py

Type: bug
Target: PyAutoHands (autohands generate)
Consequence: glance

Found 2026-11-04 (workspace-hygiene-sweep-1104). In ~/venv/PyAuto313 `ipynb-py-convert` is not installed
(only in the old ~/venv/PyAuto and PyAutoGPU). `autohands generate autolens|howtolens|howtogalaxy` then dies
with FileNotFoundError AFTER removing the root `start_here.ipynb` and writing `temp.py` — a destructive partial
run (restored by hand from git).

Two fixes: (1) preflight `shutil.which("ipynb-py-convert")` before anything destructive, like the existing
unknown-project guard; (2) add ipynb-py-convert to the PyAuto313 dev environment / requirements.
Also worth a warning: the Colab Gemini stamp reads the local `*_assistant` checkout, and a stale (behind origin)
assistant silently rewrites the context of every notebook (239 spurious diffs here) — warn when the assistant
checkout is behind origin/main.
