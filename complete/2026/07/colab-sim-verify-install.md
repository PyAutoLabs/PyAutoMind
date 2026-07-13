## colab-sim-verify-install
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/45 (auto-closed on merge)
- completed: 2026-07-09
- prs: PyAutoConf#121 + PyAutoHeart#46 (merged 2026-07-09)
- note: verify_install check F simulates the Colab bootstrap end-to-end (venv + fake google.colab incl. output submodule for JAX's colab_lib + injected cell verbatim + tag-matched clone + real notebook cell). SKIPs until the next release ships the setup_colab registry, then self-activates. PyAutoConf gained the workspace_dir override. First run found PyAutoBuild#126: ~28/49 workspace datasets are committed 15x15 smoke artifacts (evidence corrected on the issue: no release-lineage re-smallification; 2026-05-21 pre-build commits wrote them to main). Rider: checks A/C clone from PyAutoLabs owner.

## Original prompt

# Colab-simulation leg in verify_install (closes the last Colab maturity gap)

Autonomy: safe
Difficulty: medium
Status: launched 2026-07-09 (user-approved in-session: "ok do this" on the exact proposal)

## Original request (verbatim)

> ok do this: - Nothing actually executes the Colab bootstrap path. The setup cell is
> unit-tested and the no-op-outside-Colab path is exercised everywhere, but no CI
> simulates a real Colab session (fresh env → pip from PyPI → setup_colab.setup() →
> clone → run a cell). Heart's verify_install is the nearest thing; a "colab-simulation"
> leg there (or a periodic real-Colab manual check, which your PyAutoMind overview
> already lists as a manual step) would close it.

## Design

New **check F** in `PyAutoHeart/heart/checks/verify_install.sh` (fits the existing
A–E suite: throwaway venv, PASS/FAIL/SKIP row, JSON sidecar → readiness):

1. venv + `pip install autolens jax` — emulates Colab's preinstalled base env
   (honours --version / --testpypi like check A).
2. Install a fake `google.colab` stub into the venv's site-packages so
   `import google.colab` succeeds — activating the real on-Colab code path.
3. Run the injected setup cell's code verbatim: bootstrap `pip install autoconf
   --no-deps`, then `setup_colab.setup("autolens", raise_error_if_not_gpu=False,
   workspace_dir=<tmp>)`. If the installed autoconf predates the registry
   (`setup` missing) → SKIP with "ships next release" (honest, self-activating).
4. Assert: workspace cloned (at the installed-release tag when it exists), cwd
   moved into it, autoconf config path pushed.
5. "Run a cell": `import autolens as al` + `al.Imaging.from_fits(dataset/imaging/
   simple/...)` from the cloned workspace — proves a notebook body would run.

**PyAutoConf**: add `workspace_dir: str | None = None` override to
`setup_colab.setup` (threads into `_colab_setup`/`_clone_workspace`) — needed
because the registry hardcodes Colab's `/content/...`, unwritable in CI. Update
unit tests.

Deep on-demand check — never in the <30s tick; runs via `pyauto-heart
verify_install` with the existing sidecar consumption.
