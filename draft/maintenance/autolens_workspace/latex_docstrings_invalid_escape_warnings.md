# LaTeX in non-raw docstrings emits SyntaxWarning: invalid escape sequence

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft — the § "Scope to establish first" measurement is DONE for autolens_workspace (2026-08-09)

## 2026-08-09 — the sweep this prompt asks for, run

Still open; nothing has been fixed. But § "Scope to establish first" says to report
the count and affected repos **before** proposing a change, so here is that number
for autolens_workspace main (`9974f891`):

**80 warnings across 17 files** in `scripts/` — six times the "roughly a dozen
per script across the four" this prompt was filed on, and well beyond
potential_correction. So the prompt's own instinct ("do NOT assume this is
confined to potential_correction") was right.

By escape sequence:

| seq | n | | seq | n | | seq | n |
|---|--:|---|---|--:|---|---|--:|
| `\d` | 15 | | `\e` | 7 | | `\l` | 4 |
| `\c` | 15 | | `\k` | 5 | | `\*` | 3 |
| `\s` | 10 | | `\,` | 5 | | `\p` | 2 |
| `\m` | 9 | | `\o` | 4 | | `\h` | 1 |

Worst files (all `likelihood_function.py`, i.e. the maths-heavy prose):

```
12  scripts/imaging/features/advanced/potential_correction/likelihood_function.py
10  scripts/interferometer/features/advanced/potential_correction/likelihood_function.py
 8  scripts/interferometer/features/pixelization/likelihood_function.py
 8  scripts/imaging/features/pixelization/likelihood_function.py
 7  scripts/interferometer/likelihood_function.py
 7  scripts/imaging/likelihood_function.py
```

The concentration in `likelihood_function.py` files is a useful shape: these are
the scripts that carry LaTeX-heavy derivations, so option 1 (raw docstrings) would
touch mostly files whose rendered output is already equation-dense — check the
`r"""` prefix's appearance there specifically before choosing.

**The sibling workspaces and HowTo* repos are still uncounted** — this measurement
covers autolens_workspace only.

### TRAP — the command in § "Scope to establish first" silently reports zero

Both snippets below use `SyntaxWarning`. These escapes are only a `SyntaxWarning`
on **Python 3.12+**; on 3.11 and earlier they are a `DeprecationWarning`, so

```bash
python3 -W always::SyntaxWarning -m compileall -q scripts/     # → 0 hits on 3.11
python3 -W always::DeprecationWarning -m compileall -q scripts/ # → 80 hits on 3.11
```

The first form reports a clean sweep on an older interpreter and looks exactly
like "already fixed". This cost a mis-grade during the sweep before the source was
read directly and found unchanged. Use `-f` too, or `__pycache__` suppresses
recompilation and the counts silently drop. Anyone picking this up on a 3.11
environment should run both.

---

## Origin

Split out of #457 (potential-correction `ENV: full_datasets` declarations, PR #459 merged
2026-08-03). Observed while running those scripts under the smoke profile; deliberately NOT bundled
there because it is unrelated to the dpsi-mesh failure and warrants a wider pass than three files.

## The problem

Workspace scripts write LaTeX in ordinary (non-raw) triple-quoted docstrings, so Python parses
`\o`, `\c`, `\d`, `\,`, `\p`, `\s` as escape sequences and emits `SyntaxWarning: invalid escape
sequence` on every run. Observed on all four potential-correction scripts:

```
scripts/imaging/features/advanced/potential_correction/start_here.py:11: SyntaxWarning: invalid escape sequence '\d'
  pixelized corrections $\delta\psi$ to the lensing potential are defined on a coarse regular mesh
scripts/imaging/features/advanced/potential_correction/start_here.py:72: SyntaxWarning: invalid escape sequence '\,'
  ... $10^{10} \, M_\odot$ NFW dark ...
scripts/interferometer/features/advanced/potential_correction/likelihood_function.py:297: SyntaxWarning: invalid escape sequence '\,'
  - the curvature is $F = A^T \, (T^H C^{-1} T) \, A$ ...
```

Roughly a dozen warnings per script across the four. These are currently benign — Python still
stores the literal backslash — but the behaviour is deprecated and is scheduled to become a
`SyntaxError`, so this is a latent break, not only noise.

## Scope to establish first

Do **not** assume this is confined to potential_correction. Sweep the workspace (and likely the
sibling workspaces + HowTo* repos) before deciding the fix's size:

```bash
python3 -W error::SyntaxWarning -c "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)" <script>
```

or compile every script and collect the warnings:

```bash
python3 -W always::SyntaxWarning -m compileall -q scripts/ 2>&1 | grep "invalid escape sequence"
```

Report the count and the distinct repos affected before proposing the change.

## Candidate fixes (decide after the sweep)

1. **Raw docstrings** — prefix the affected docstrings with `r"""`. Minimal and local, but the
   `r` prefix appears in the user-facing script text and is carried into generated notebooks and
   markdown; check how it renders before committing to it.
2. **Escape the backslashes** (`\\delta`) — leaves the docstring non-raw but doubles every
   backslash, which is noisier to read and easy to regress.

Option 1 is the conventional fix; option 2 is listed so the trade-off is on the record.

## Constraints

- Docstring content is user-facing tutorial prose — do not reword the LaTeX or the surrounding
  sentences while fixing the escapes. Prose changes belong to a docs task, not this one.
- Notebooks are regenerated, never hand-edited. Verify the regenerated `.ipynb` renders the maths
  identically, and check `workspace_index.json` / `llms-full.txt` for unintended churn.
- Verify with `-W error::SyntaxWarning` afterwards so the fix is proven by the warning
  disappearing, not by the script merely still running.

## Related

- `complete/2026/08/potential-correction-env-declaration.md` — the task this was split from.
