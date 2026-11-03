"""One declaration per generated marker block drives both check and --write.

`repos_sync.GENERATED_BLOCKS` is the registry: each `GeneratedBlock` names its
check-leg label, its marker pair, where its copies live and what fills them,
and that one declaration is what the drift check grades and what `--write`
fills. These pin the refactor that introduced it (one check function and one
`write_block` call site per surface, collapsed into the registry):

* the registry itself — labels, marker pairs, order — and that every declared
  block is a registered check leg (an undeclared leg would be written but
  never graded, or graded but never written);
* the CLI's printed output for every block leg, on a stale fictional tree and
  again after `--write`, byte-for-byte. The expected transcripts below were
  captured from the pre-refactor script, so they are the behaviour the
  declarations must reproduce.

Conventions, as in the sibling repos_sync tests:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Hermetic.** The script runs as a subprocess from a scratch copy of the
   Mind, against a tmp workspace root — never the sibling checkouts.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

ROUTING = "root AGENTS.md routing table (generated)"
OWNER = "WORKFLOW.md owner map (generated)"
MAP = "organism-map blocks (generated)"
HISTORY = "never-rewrite-history blocks (generated)"
REMOTE = "remote-session blocks (generated)"
DELIVERABLE = "end-at-deliverable blocks (generated)"
FILING = "where-to-file blocks (generated)"
PUBLIC = "public front-door organ tables (generated)"

REGISTRY = [
    (ROUTING, "<!-- repos_sync:begin -->", "<!-- repos_sync:end -->"),
    (OWNER, "<!-- repos_sync:begin -->", "<!-- repos_sync:end -->"),
    (MAP, "<!-- repos_sync:map:begin -->", "<!-- repos_sync:map:end -->"),
    (HISTORY, "<!-- repos_sync:history:begin -->",
     "<!-- repos_sync:history:end -->"),
    (REMOTE, "<!-- repos_sync:remote:begin -->", "<!-- repos_sync:remote:end -->"),
    (DELIVERABLE, "<!-- repos_sync:deliverable:begin -->",
     "<!-- repos_sync:deliverable:end -->"),
    (FILING, "<!-- repos_sync:filing:begin -->", "<!-- repos_sync:filing:end -->"),
    (PUBLIC, "<!-- repos_sync:organs:begin -->", "<!-- repos_sync:organs:end -->"),
]

MANIFEST = """\
categories:
  organ: {label: Organ, role: the organs}
  library: {label: Library, role: the libraries}
repos:
  OrganCore: {category: organ, github: Example/OrganCore, role: the core organ}
  OrganTwo: {category: organ, github: Example/OrganTwo, role: the second organ}
  LibAlpha: {category: library, github: Example/LibAlpha, role: a library}
  LibQuiet: {category: library, github: Example/LibQuiet, role: a quiet one, filing_block: false}
"""

POLICIES = {
    "never_rewrite_history.md": "HISTORY POLICY\n",
    "remote_sessions.md": "REMOTE POLICY\n",
    "end_at_deliverable.md": "DELIVERABLE POLICY\n",
    "where_to_file.md": "FILING POLICY\n",
    "shared_standards.md": "STANDARDS\n<!-- board-owners -->\nBOARD\n",
    "session_start_hook.sh": "#!/bin/sh\n",
    "end_at_deliverable_hook.sh": "#!/bin/sh\n",
}


def _block(tag):
    return f"<!-- repos_sync:{tag}:begin -->\nold\n<!-- repos_sync:{tag}:end -->\n"


ROOT_BLOCK = "<!-- repos_sync:begin -->\nold\n<!-- repos_sync:end -->\n"


def _workspace(tmp_path):
    """A stale fictional workspace exercising every marker-block state:
    stale, opt-in absent, self-insertable, unanchored, excluded, required."""
    root = tmp_path / "ws"
    mind = root / "PyAutoMind"
    (mind / "scripts").mkdir(parents=True)
    for name in ("repos_sync.py", "smoke_bootstrap_sync.py"):
        shutil.copy(SCRIPTS / name, mind / "scripts" / name)
    (mind / "repos.yaml").write_text(MANIFEST)
    (mind / "policy").mkdir()
    for name, text in POLICIES.items():
        (mind / "policy" / name).write_text(text)

    def agents(name, body):
        path = root / name / "AGENTS.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)

    agents("OrganCore", "# core\n" + _block("map") + _block("history") + _block("remote"))
    agents("OrganTwo", "# two\n" + _block("history") + _block("deliverable")
           + _block("filing"))
    agents("LibAlpha", "# alpha\n" + _block("history") + _block("deliverable"))
    agents("LibQuiet", "# quiet\n")
    (root / "AGENTS.md").write_text("# root\n" + ROOT_BLOCK)
    workflow = root / "PyAutoBrain/skills/WORKFLOW.md"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("# workflow\n" + ROOT_BLOCK)
    profile = root / ".github/profile/README.md"
    profile.parent.mkdir(parents=True)
    profile.write_text("# profile, no organ markers\n")
    scientist = root / "PyAutoScientist/README.md"
    scientist.parent.mkdir(parents=True)
    scientist.write_text("# scientist\n" + _block("organs"))
    return root


def _run(root, *args):
    env = {k: v for k, v in os.environ.items() if k != "PYAUTO_ROOT"}
    proc = subprocess.run(
        [sys.executable, "scripts/repos_sync.py", "--root", str(root), *args],
        cwd=root / "PyAutoMind",
        capture_output=True,
        text=True,
        env=env,
    )
    out = (proc.stdout + proc.stderr).replace(str(root), "<root>")
    return f"{out}rc={proc.returncode}\n"


def _only(*labels):
    return [arg for label in labels for arg in ("--only", label)]


HINT = "run `python3 PyAutoMind/scripts/repos_sync.py --write`"

STALE_CHECKS = {
    ROUTING: f"""\
check {ROUTING}: 1 mismatch(es)
  ✗ AGENTS.md: routing table block is stale — {HINT}
rc=1
""",
    OWNER: f"""\
check {OWNER}: 1 mismatch(es)
  ✗ PyAutoBrain/skills/WORKFLOW.md: owner map block is stale — {HINT}
rc=1
""",
    MAP: f"""\
check {MAP}: 1 mismatch(es)
  ✗ 'OrganCore': organism-map block is stale — {HINT}
rc=1
""",
    HISTORY: f"""\
check {HISTORY}: 3 mismatch(es)
  ✗ 'OrganCore': never-rewrite-history block is stale — {HINT}
  ✗ 'OrganTwo': never-rewrite-history block is stale — {HINT}
  ✗ 'LibAlpha': never-rewrite-history block is stale — {HINT}
rc=1
""",
    REMOTE: f"""\
check {REMOTE}: 1 mismatch(es)
  ✗ 'OrganCore': remote-session block is stale — {HINT}
rc=1
""",
    DELIVERABLE: f"""\
check {DELIVERABLE}: 4 mismatch(es)
  ✗ 'OrganCore': no deliverable block — {HINT} (it inserts one after the history block)
  ✗ 'OrganTwo': end-at-deliverable block is stale — {HINT}
  ✗ 'LibAlpha': end-at-deliverable block is stale — {HINT}
  ✗ 'LibQuiet': no deliverable block — add the markers (<!-- repos_sync:deliverable:begin --> / <!-- repos_sync:deliverable:end -->) to its AGENTS.md, then {HINT}
rc=1
""",
    FILING: f"""\
check {FILING}: 3 mismatch(es)
  ✗ 'OrganCore': no where-to-file block — add the markers (<!-- repos_sync:filing:begin --> / <!-- repos_sync:filing:end -->) to its AGENTS.md, then {HINT}
  ✗ 'OrganTwo': where-to-file block is stale — {HINT}
  ✗ 'LibAlpha': no where-to-file block — {HINT} (it inserts one after the deliverable block)
rc=1
""",
    PUBLIC: f"""\
check {PUBLIC}: 2 mismatch(es)
  ✗ .github/profile/README.md: no repos_sync:organs marker block (add the markers, then run --write)
  ✗ PyAutoScientist/README.md: organ table stale — {HINT}
rc=1
""",
}

AGENTS = "<root>/{}/AGENTS.md"

WRITE = f"""\
wrote: <root>/.pyauto-root
updated: <root>/AGENTS.md
updated: <root>/PyAutoBrain/skills/WORKFLOW.md
updated: {AGENTS.format("OrganCore")}
skipped (no markers): {AGENTS.format("OrganTwo")}
inserted deliverable markers: {AGENTS.format("OrganCore")}
updated: {AGENTS.format("OrganCore")}
updated: {AGENTS.format("OrganCore")}
updated: {AGENTS.format("OrganCore")}
updated: {AGENTS.format("OrganTwo")}
skipped (no markers): {AGENTS.format("OrganTwo")}
updated: {AGENTS.format("OrganTwo")}
updated: {AGENTS.format("LibAlpha")}
skipped (no markers): {AGENTS.format("LibAlpha")}
updated: {AGENTS.format("LibAlpha")}
skipped (no markers): {AGENTS.format("LibQuiet")}
skipped (no markers): {AGENTS.format("LibQuiet")}
skipped (no markers): {AGENTS.format("LibQuiet")}
inserted where-to-file markers: {AGENTS.format("OrganCore")}
inserted where-to-file markers: {AGENTS.format("LibAlpha")}
updated: {AGENTS.format("OrganCore")}
updated: {AGENTS.format("OrganTwo")}
updated: {AGENTS.format("LibAlpha")}
skipped (no markers): <root>/.github/profile/README.md
updated: <root>/PyAutoScientist/README.md
"""

HOOKS = "".join(
    f"wrote: <root>/{name}/{rel}\n"
    for name in ("OrganCore", "OrganTwo", "LibAlpha", "LibQuiet")
    for rel in (".claude/hooks/session-start.sh",
                ".claude/hooks/end-at-deliverable.sh", ".claude/settings.json")
)

# After --write every block is clean except the two copies --write is not
# allowed to place markers in: a repo with no anchor for the deliverable block,
# and a front-door README that never opted into the organ table.
AFTER_WRITE = f"""\
check {ROUTING}: OK
check {OWNER}: OK
check {MAP}: OK
check {HISTORY}: OK
check {REMOTE}: OK
check {DELIVERABLE}: 1 mismatch(es)
  ✗ 'LibQuiet': no deliverable block — add the markers (<!-- repos_sync:deliverable:begin --> / <!-- repos_sync:deliverable:end -->) to its AGENTS.md, then {HINT}
check {FILING}: OK
check {PUBLIC}: 1 mismatch(es)
  ✗ .github/profile/README.md: no repos_sync:organs marker block (add the markers, then run --write)
rc=1
"""

def test_registry_declares_each_generated_block_once_in_order():
    declared = [(b.label, b.begin, b.end) for b in repos_sync.GENERATED_BLOCKS]
    assert declared == REGISTRY
    assert len({b.label for b in repos_sync.GENERATED_BLOCKS}) == len(REGISTRY)


def test_every_declared_block_is_a_registered_check_leg(tmp_path):
    root = _workspace(tmp_path)
    out = _run(root, "--only", "no such leg")
    legs = out.split("choose from: ", 1)[1]
    for label, _, _ in REGISTRY:
        assert f"'{label}'" in legs


def test_stale_check_output_is_pinned_per_block_leg(tmp_path):
    root = _workspace(tmp_path)
    for label, expected in STALE_CHECKS.items():
        assert _run(root, "--check", "--only", label) == expected, label


def test_write_transcript_and_post_write_checks_are_pinned(tmp_path):
    root = _workspace(tmp_path)
    labels = [label for label, _, _ in REGISTRY]
    out = _run(root, "--write", *_only(*labels))
    assert out == WRITE + HOOKS + AFTER_WRITE
    # A second, check-only run grades the written copies the same way.
    assert _run(root, "--check", *_only(*labels)) == AFTER_WRITE
    core = (root / "OrganCore/AGENTS.md").read_text()
    assert "<!-- repos_sync:history:end -->\n\n<!-- repos_sync:deliverable:begin -->\n" \
        "DELIVERABLE POLICY\n<!-- repos_sync:deliverable:end -->" in core
    assert "<!-- repos_sync:filing:begin -->\nFILING POLICY\n" in core
    assert "FILING" not in (root / "LibQuiet/AGENTS.md").read_text()
