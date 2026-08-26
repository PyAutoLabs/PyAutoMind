"""`status.sh --repos` must not source a file that isn't in the repo.

The flag used to `source scripts/pyauto_status.sh` and call a `pyauto-status`
shell function. Both went with the cross-repo dashboard when it became a leg of
the Heart-owned health door, so the branch sourced a missing file — and because
it ended in `exit 0`, it reported success while printing nothing at all. Silent
success is the part worth pinning: a caller could not tell the dashboard had
gone (issue #331).

These tests run the real script rather than grepping it, because the failure was
in what the shell *did* with the branch, not in how it read.

Fictional fixtures only, per `test_spawn_privacy.py` — `tests/**` is KEEP-copied
verbatim into the public template, so nothing here names a real task or prompt.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "scripts" / "status.sh"


def _run(*args):
    return subprocess.run(["bash", str(STATUS), *args],
                          capture_output=True, text=True, cwd=ROOT)


def test_repos_flag_fails_loudly_and_names_its_replacement():
    result = _run("--repos")
    assert result.returncode != 0, "a retired flag must not report success"
    assert "/health status" in result.stderr


def test_repos_flag_raises_no_shell_error():
    """The old branch failed as `No such file` + `command not found`."""
    noise = _run("--repos").stderr + _run("--repos").stdout
    assert "No such file or directory" not in noise
    assert "command not found" not in noise


def test_no_source_of_a_missing_script():
    """Every file the script sources must exist — the root cause, generalised."""
    for line in STATUS.read_text().splitlines():
        stripped = line.strip()
        if not stripped.startswith(("source ", ". ")):
            continue
        target = stripped.split(maxsplit=1)[1].strip('"\'')
        resolved = target.replace("$ROOT", str(ROOT)).replace("${ROOT}", str(ROOT))
        assert "$" not in resolved, f"unresolved variable in `{stripped}`"
        assert Path(resolved).is_file(), f"{stripped} sources a missing file"


def test_default_run_still_reports_the_registry():
    result = _run()
    assert result.returncode == 0, result.stderr
    assert "== Registry ==" in result.stdout
