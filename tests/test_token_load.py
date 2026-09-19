"""The token report handles both workspace layouts and fails visibly on drift."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/token_load.py"


def workspace(tmp_path, grouped):
    root = tmp_path / "workspace"
    root.mkdir(parents=True)
    (root / "AGENTS.md").write_text("root\n")
    organ_dir = root / "organs" if grouped else root
    brain = organ_dir / "PyAutoBrain"
    mind = organ_dir / "PyAutoMind"
    for repo in (brain, mind):
        (repo / ".git").mkdir(parents=True)
        (repo / "AGENTS.md").write_text("rules\n")
    for path in (
        brain / "skills/start_dev/start_dev.md",
        brain / "skills/start_dev/SKILL.md",
        brain / "skills/prm/prm.md",
        brain / "skills/prm/SKILL.md",
        brain / "skills/prm/closeout.md",
        brain / "skills/prm/mcp.md",
        brain / "skills/prm/freeze.md",
        brain / "skills/start_dev/reference.md",
        brain / "skills/prm/reference.md",
        brain / "skills/CONTEXT.md",
        brain / "skills/WORKFLOW.md",
        brain / "skills/GITHUB_ACCESS.md",
        mind / "REFERENCE.md",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("one\ntwo\n")
    return root, brain, mind


def run(root, *options):
    return subprocess.run([sys.executable, str(SCRIPT), *options, "--root", str(root), "--json"],
                          text=True, capture_output=True)


def test_report_resolves_grouped_and_flat(tmp_path):
    for grouped in (True, False):
        root, brain, mind = workspace(tmp_path / str(grouped), grouped)
        proc = run(root, "report")
        assert proc.returncode == 0, proc.stderr
        report = json.loads(proc.stdout)
        assert report["files"]["Brain AGENTS"]["path"] == str(brain / "AGENTS.md")
        assert report["files"]["Mind AGENTS"]["path"] == str(mind / "AGENTS.md")
        assert report["files"]["start_dev body"]["lines"] == 2
        assert report["totals"]["start_dev_lines"] == 8
        assert report["totals"]["prm_lines"] == 8
        assert report["totals"]["core_union_lines"] == 12
        assert report["totals"]["agents_tokens_approx"] == 6
        assert not report["violations"]


def test_missing_paths_are_reported_and_check_fails(tmp_path):
    root, brain, _ = workspace(tmp_path, False)
    (brain / "skills/prm/reference.md").unlink()
    report = run(root, "report")
    assert report.returncode == 0
    assert "missing" in json.loads(report.stdout)["files"]["prm reference"]
    check = run(root, "check")
    assert check.returncode == 1
    assert "missing: prm reference" in json.loads(check.stdout)["violations"][0]


def test_budgets_cover_agents_and_both_core_procedures(tmp_path):
    root, _, _ = workspace(tmp_path, True)
    check = run(root, "check", "--agents-budget", "4", "--start-dev-budget", "1",
                "--prm-budget", "1")
    assert check.returncode == 1
    violations = json.loads(check.stdout)["violations"]
    assert any("AGENTS total" in item for item in violations)
    assert any("start_dev_lines" in item for item in violations)
    assert any("prm_lines" in item for item in violations)
