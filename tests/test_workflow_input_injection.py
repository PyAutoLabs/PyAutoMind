"""No Mind workflow interpolates a dispatch input into a shell (PyAutoMind#565).

The editable dashboard holds a token that can dispatch ANY `workflow_dispatch`
workflow here with attacker-chosen inputs, so every such input is untrusted.
`${{ inputs.x }}` inside `run:` is pasted into the script before bash parses
it: a value like `'; curl … | sh #` runs. Inputs must reach a step through
`env:` and be validated there (policy/github_tokens.md, "The dashboard input
token"). This scan fails on any regression, in any workflow; the behaviour
tests run the validating steps themselves with hostile values.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
FILES = sorted(WORKFLOWS.glob("*.yml")) if WORKFLOWS.is_dir() else []
#: An expression that reads a dispatch input or a repository_dispatch payload.
UNTRUSTED = re.compile(
    r"\$\{\{[^}]*\b(inputs\.|github\.event\.inputs|client_payload)", re.S)


def _steps(wf):
    for name, job in (wf.get("jobs") or {}).items():
        for i, step in enumerate(job.get("steps") or []):
            yield f"{name}[{i}] {step.get('name', '')}".strip(), step


@pytest.mark.skipif(not FILES, reason="no workflows shipped here")
def test_no_workflow_interpolates_an_input_into_a_script():
    hits = []
    for path in FILES:
        wf = yaml.safe_load(path.read_text())
        for where, step in _steps(wf):
            scripts = [step.get("run") or ""]
            # actions/github-script evaluates `script:` as JavaScript: the same
            # injection, one language over.
            scripts.append((step.get("with") or {}).get("script") or "")
            for text in scripts:
                if UNTRUSTED.search(str(text)):
                    hits.append(f"{path.name}: {where}")
    assert hits == [], ("dispatch inputs interpolated into run:/script: — pass "
                        "them through env: and validate them: " + "; ".join(hits))


def test_the_scan_catches_the_patterns_it_exists_for():
    for bad in ("x='${{ inputs.limit || 0 }}'", 'b="${{ github.event.inputs.b }}"',
                "echo ${{ github.event.client_payload.ref }}"):
        assert UNTRUSTED.search(bad), bad
    assert not UNTRUSTED.search('override="${LOOKBACK_HOURS_INPUT:-}"')


# --------------------------------------------------------------------------- #
# the validating steps, run with hostile values
# --------------------------------------------------------------------------- #
def _step(workflow, name):
    path = WORKFLOWS / workflow
    if not path.is_file():
        pytest.skip(f"{workflow} is not shipped here")
    for _where, step in _steps(yaml.safe_load(path.read_text())):
        if step.get("name") == name:
            return step["run"]
    raise AssertionError(f"{workflow}: no step {name!r}")


def _bash(script, tmp_path, **env):
    out, summary = tmp_path / "out", tmp_path / "summary"
    full = dict(os.environ, GITHUB_OUTPUT=str(out), GITHUB_STEP_SUMMARY=str(summary),
                GITHUB_EVENT_NAME="workflow_dispatch", GITHUB_REF_NAME="main", **env)
    res = subprocess.run(["bash", "-e", "-c", script], cwd=tmp_path, env=full,
                         capture_output=True, text=True)
    return res, (out.read_text() if out.exists() else "")


PAYLOADS = ["'; touch PWNED; '", "$(touch PWNED)", "`touch PWNED`", "1;touch PWNED",
            "a\ntouch PWNED"]


@pytest.mark.parametrize("workflow", ["arxiv_papers.yml", "arxiv_interests.yml"])
@pytest.mark.parametrize("value,ok", [("", True), ("168", True), ("2160", True),
                                      ("0", False), ("2161", False), ("12345", False),
                                      ("-1", False), ("1e3", False)]
                         + [(p, False) for p in PAYLOADS])
def test_lookback_hours_is_validated(tmp_path, workflow, value, ok):
    res, _ = _bash(_step(workflow, "Validate dispatch inputs"), tmp_path,
                   LOOKBACK_HOURS_INPUT=value)
    assert (res.returncode == 0) is ok, res.stdout + res.stderr
    if not ok:
        assert "::error title=Invalid input::" in res.stdout
    assert not (tmp_path / "PWNED").exists()


@pytest.mark.parametrize("branch,ok", [
    ("claude/dashboard-input-x1", True), ("codex/fix.thing", True),
    ("chatgpt/a/b", True), ("main", False), ("feature/x", False),
    ("archive/condemned/x", False), ("claude/a..b", False), ("claude/x.lock", False),
    ("claude/x y", False)] + [("claude/" + p, False) for p in PAYLOADS])
def test_the_ledger_merge_branch_is_validated(tmp_path, branch, ok):
    res, out = _bash(_step("mind_ledger_merge.yml", "Resolve the branch"), tmp_path,
                     BRANCH_INPUT=branch, MODE_INPUT="audit")
    assert (res.returncode == 0) is ok, res.stdout + res.stderr
    assert not (tmp_path / "PWNED").exists()
    if ok:
        assert f"branch={branch}\n" in out and "mode=audit\n" in out


def test_the_ledger_merge_mode_is_validated(tmp_path):
    res, _ = _bash(_step("mind_ledger_merge.yml", "Resolve the branch"), tmp_path,
                   BRANCH_INPUT="claude/x", MODE_INPUT="merge; touch PWNED")
    assert res.returncode == 1 and not (tmp_path / "PWNED").exists()


@pytest.mark.parametrize("mode,limit,ok", [
    ("audit", "0", True), ("delete", "25", True), ("", "", True),
    ("delete", "1001", False), ("delete", "-1", False), ("rm", "0", False)]
    + [("delete", p, False) for p in PAYLOADS] + [(p, "0", False) for p in PAYLOADS])
def test_the_branch_sweep_inputs_are_validated(tmp_path, mode, limit, ok):
    script = _step("branch_sweep.yml", "Sweep")
    # Everything before the sweep itself is the validation.
    script = script[:script.index(".brain/bin/branch_sweep.sh")] + 'echo "ok $mode $limit"\n'
    res, _ = _bash(script, tmp_path, MODE_INPUT=mode, LIMIT_INPUT=limit)
    assert (res.returncode == 0) is ok, res.stdout + res.stderr
    assert not (tmp_path / "PWNED").exists()
