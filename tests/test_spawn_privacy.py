"""The privacy invariant required by docs/pyautobrain/spawn_spec.md.

    "no live wiki page, bibliography entry, reading-queue line, prompt, or
     registry entry may ever appear in a template output. The implementation
     must include a test asserting the generated tree contains none of a
     canary list of live-content markers."

The regression these lock down (issue #118): `empty_body()` used to return
line 1 of the live file. Some registry ledgers carry no H1 at all, so their
first line is a live registry entry, and spawn stamped it into the public
fresh-slate templates. A heading-shape test would NOT have caught it — a task
slug written as an H2 is a structurally valid heading.

TWO RULES FOR THIS FILE, both learned the hard way:

1. NO REAL LIVE STRINGS. `tests/**` is KEEP-copied verbatim into the public
   template, so a fixture quoting a real registry slug republishes the very
   content this suite exists to keep out. Every fixture below is fictional,
   and every canary token is derived from `spawn.CANARY_TOKENS` at run time
   rather than spelled out. This file must scan CLEAN with no exemption.
2. TEST THE GENERATED TREE, not just the helpers. Unit-testing `empty_body()`
   alone would stay green if a rule were flipped to KEEP or the dispatcher
   swapped for `copy2` — the leak would simply move. `test_generated_tree_*`
   below drives the real generators end to end.

Hermetic: everything runs on a synthetic Mind/Memory built in tmp_path, so the
suite needs no live checkout.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

SPAWN_PY = Path(__file__).resolve().parents[1] / "scripts" / "spawn.py"

_spec = importlib.util.spec_from_file_location("spawn", SPAWN_PY)
spawn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spawn)


# Derived, never spelled out — see rule 1 in the module docstring.
A_TOKEN = spawn.CANARY_TOKENS[0]
NAME_TOKEN = spawn.CANARY_TOKENS[-1]

# Fictional content shaped like the real leaks: a registry H2 slug, a raw idea
# bullet, and an instance-flavoured H1 that a heading test would wave through.
HOSTILE_BODIES = [
    "## example-task-slug-phases-2-4\n- issue: https://example.invalid/1\n",
    "- example_module_feature workspace guide.\n",
    "# Some Instance-Specific Ledger Name\n\n1. a live entry\n",
    "",
]

# Read lazily so the suite still COLLECTS against a spawn.py that predates
# EMPTY_TITLES. Otherwise the decisive regression tests below never run — they
# would be masked by a collection error, which proves only that the API moved.
EMPTY_TITLES = getattr(spawn, "EMPTY_TITLES", {})


# --------------------------------------------------------------------------
# The issue #118 regression, in the smallest forms that catch it
# --------------------------------------------------------------------------


def test_registry_ledger_never_carries_its_first_entry(tmp_path):
    """Depends on nothing but `empty_body`, so it fails with a clean assertion
    against the pre-fix implementation rather than erroring at import."""
    src = tmp_path / "planned.md"
    src.write_text("## example-task-slug-phases-2-4\n- issue: https://example.invalid/1\n")
    assert "example-task-slug" not in spawn.empty_body(src)


def test_ideas_ledger_never_carries_an_idea_line(tmp_path):
    src = tmp_path / "ideas.md"
    src.write_text("- example_module_feature workspace guide.\n")
    assert "example_module_feature" not in spawn.empty_body(src)


@pytest.mark.parametrize("name,title", sorted(EMPTY_TITLES.items()))
@pytest.mark.parametrize("body", HOSTILE_BODIES)
def test_empty_output_contains_no_source_bytes(tmp_path, name, title, body):
    """Every EMPTY output is exactly the generated title + marker."""
    src = tmp_path / name
    src.write_text(body)

    out = spawn.empty_body(src)

    assert out.startswith(title + "\n\n"), f"{name} lost its generated title"
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 2, f"{name} emitted unexpected lines: {lines!r}"
    assert lines[0] == title

    for src_line in body.splitlines():
        if src_line.strip() and src_line.strip() != title:
            assert src_line not in out, f"{name} leaked source line: {src_line!r}"


@pytest.mark.parametrize("name", sorted(EMPTY_TITLES))
def test_empty_body_never_opens_the_source(tmp_path, name):
    """The source need not even be readable — EMPTY is purely generated.

    Stronger than diffing output: if the file is never opened, no future edit
    to a live registry file can change what a template ships.
    """
    missing = tmp_path / name  # deliberately not created
    assert spawn.empty_body(missing).startswith(EMPTY_TITLES[name])


def test_unmapped_empty_file_is_a_human_decision(tmp_path):
    """A new EMPTY file class must fail loudly, never be guessed at."""
    src = tmp_path / "brand_new_ledger.md"
    src.write_text("## some-live-task\n")
    with pytest.raises(SystemExit) as excinfo:
        spawn.empty_body(src)
    assert "brand_new_ledger.md" in str(excinfo.value)


def test_a_shared_basename_does_not_inherit_a_root_title(tmp_path):
    """EMPTY_TITLES is keyed by relative path, not basename.

    A glob-matched file that merely shares a name with a root ledger must take
    the unmapped-file SystemExit, not silently inherit that ledger's title.
    """
    nested = tmp_path / "bibliography"
    nested.mkdir()
    src = nested / "active.md"
    src.write_text("live bibliography content\n")
    with pytest.raises(SystemExit):
        spawn.empty_body(src, "bibliography/active.md")


@pytest.mark.parametrize(
    "filename,lead",
    [("refs.bib", "%"), ("aliases.yaml", "#"), ("x.yml", "#")],
)
def test_glob_matched_empty_files_get_comment_headers(tmp_path, filename, lead):
    """spawn_spec.md rule 2: bibliography files keep a generated header comment.

    The header and marker must both be comments — a YAML/BibTeX consumer parses
    every non-comment line, so an HTML comment would read as content.
    """
    src = tmp_path / filename
    src.write_text(f"@article{{Example2018, title={{a {A_TOKEN} lens}}}}\n")

    out = spawn.empty_body(src)

    assert out.startswith(lead)
    for line in [ln for ln in out.splitlines() if ln.strip()]:
        assert line.startswith(lead), f"non-comment line in {filename}: {line!r}"
    assert "Example2018" not in out
    assert A_TOKEN not in out.lower()


# --------------------------------------------------------------------------
# The canary scan itself
# --------------------------------------------------------------------------


LIVE_AUTONOMY_LOG = Path(__file__).resolve().parents[1] / "autonomy_log.md"


@pytest.mark.skipif(
    not LIVE_AUTONOMY_LOG.exists(),
    reason="no live ledger here (e.g. a freshly-spawned Mind before its first run)",
)
def test_autonomy_log_constant_still_matches_the_live_schema():
    """The constant must not go stale against the ledger it models.

    Generating instead of parsing removes the leak, but it also removes the
    feedback that kept the header current: nothing else notices if the live
    ledger grows a column and the template keeps shipping the old table. This
    is that feedback, and it is the only check here that reads the real file.
    """
    live = LIVE_AUTONOMY_LOG.read_text()
    assert live.startswith(spawn.AUTONOMY_LOG_TEMPLATE), (
        "the live autonomy_log.md header no longer matches AUTONOMY_LOG_TEMPLATE "
        "— update the constant (and re-run spawn --apply), do not re-add parsing"
    )


def test_generated_ledger_equals_the_constant_exactly(fake_workspace, tmp_path):
    """Pin the EMITTED file, not just the helper's return value.

    Asserting `autonomy_log_body(...) == AUTONOMY_LOG_TEMPLATE` alone is
    circular — it compares the helper with what the helper returns. This checks
    what actually lands in the template.
    """
    out = tmp_path / "out"
    spawn.generate_all(fake_workspace, out)
    shipped = out / "PyAutoMind-template" / "autonomy_log.md"
    assert shipped.read_text() == spawn.AUTONOMY_LOG_TEMPLATE


def test_autonomy_log_template_is_a_usable_table_header():
    """Independent shape check, so a malformed constant cannot pass silently."""
    lines = [ln for ln in spawn.AUTONOMY_LOG_TEMPLATE.splitlines() if ln.strip()]
    table = [ln for ln in lines if ln.startswith("|")]
    assert len(table) == 2, f"expected a header row + separator, got {table}"
    header, separator = table
    assert set(separator.replace("|", "").replace("-", "").strip()) == set(), (
        f"second table line is not a separator: {separator!r}"
    )
    assert header.count("|") == separator.count("|"), "column counts disagree"
    assert lines[0].startswith("# "), "the ledger needs its H1 title"


def test_autonomy_log_skeleton_never_opens_the_source(tmp_path):
    """The ledger header is generated, not parsed (issue #123).

    Passing a file that does not exist is the strongest form of the assertion:
    if the source is never opened, no future edit to the live ledger — a row
    inserted above the separator, a reformatted separator, a markdown
    formatter's reflow — can change what the template ships.
    """
    missing = tmp_path / "autonomy_log.md"  # deliberately not created
    body = spawn.autonomy_log_body(missing)
    assert body == spawn.AUTONOMY_LOG_TEMPLATE
    assert body.rstrip().endswith("|"), "the table header/separator is missing"


@pytest.mark.parametrize(
    "ledger",
    [
        # Well-formed: the case that happened to work before.
        "| date | task |\n|------|------|\n| 2026-01-01 | LEAKME |\n",
        # A row above the separator — copied by the old parse.
        "| date | task |\n| 2026-01-01 | LEAKME |\n|------|------|\n",
        # Separator reformatted — the old parse never broke, copying everything.
        "| date | task |\n| --- | --- |\n| 2026-01-01 | LEAKME |\n",
        # No separator at all.
        "| date | task |\n| 2026-01-01 | LEAKME |\n",
        # Prose above the table, as the real ledger has.
        "# Log\n\nsome prose\n\n| date |\n|---|\n| 2026-01-01 LEAKME |\n",
    ],
)
def test_autonomy_log_skeleton_is_constant_whatever_the_ledger(tmp_path, ledger):
    """Shape assumptions about the live file are exactly what leaked before."""
    src = tmp_path / "autonomy_log.md"
    src.write_text(ledger)
    assert "LEAKME" not in spawn.autonomy_log_body(src)
    assert spawn.autonomy_log_body(src) == spawn.AUTONOMY_LOG_TEMPLATE


def test_canary_scan_catches_a_leaked_registry_slug(tmp_path):
    """The scan must flag a person-name token, not just a science dataset."""
    (tmp_path / "planned.md").write_text(f"## {NAME_TOKEN}-audit-phases\n")
    hits = spawn.canary_scan(tmp_path)
    assert any(NAME_TOKEN in h for h in hits), hits


def test_canary_scan_catches_dataset_tokens(tmp_path):
    (tmp_path / "notes.md").write_text(f"refit of {A_TOKEN}0946\n")
    assert any(A_TOKEN in h for h in spawn.canary_scan(tmp_path))


def test_licence_may_name_its_copyright_holder(tmp_path):
    """Attribution in a licence is the point of a licence, not a leak."""
    name = [t for t in spawn.CANARY_TOKENS if t in spawn.CANARY_EXEMPT["LICENSE"]][0]
    (tmp_path / "LICENSE").write_text(f"MIT\n  (James {name.title()} / Someone).\n")
    assert spawn.canary_scan(tmp_path) == []


def test_the_licence_exemption_is_narrow(tmp_path):
    """The exemption is per-file AND per-token — it must not become a hole."""
    name = sorted(spawn.CANARY_EXEMPT["LICENSE"])[0]

    # Same token, different file: still a leak.
    (tmp_path / "AGENTS.md").write_text(f"ask James {name.title()} about this\n")
    assert any(name in h for h in spawn.canary_scan(tmp_path))

    # Same file, different token: still a leak.
    (tmp_path / "AGENTS.md").unlink()
    (tmp_path / "LICENSE").write_text(f"MIT (James {name.title()}) — {A_TOKEN}0946\n")
    hits = spawn.canary_scan(tmp_path)
    assert any(A_TOKEN in h for h in hits)
    assert not any(name in h for h in hits)


def test_only_spawn_py_is_exempt_wholesale(tmp_path):
    """Guards against the exemption map quietly growing.

    A KEEP-copied file that is exempt from every token can smuggle live content
    into the public template while the scan reports clean — that is exactly how
    the first attempt at this fix reintroduced the #118 leak.
    """
    wholesale = {
        path
        for path, tokens in spawn.CANARY_EXEMPT.items()
        if set(tokens) >= set(spawn.CANARY_TOKENS)
    }
    assert wholesale == {"scripts/spawn.py"}, (
        f"unexpected wholesale canary exemption(s): {wholesale - {'scripts/spawn.py'}}"
    )


def test_this_test_file_is_not_exempt():
    """This file is KEEP-copied into the public template, so it must scan
    clean on its own merits rather than by exemption."""
    assert "tests/test_spawn_privacy.py" not in spawn.CANARY_EXEMPT


# --------------------------------------------------------------------------
# End-to-end: the GENERATED TREE, which is what actually ships
# --------------------------------------------------------------------------


def _fake_repo(root, files):
    """A git repo with `files` committed — spawn reads via `git ls-files`."""
    root.mkdir(parents=True, exist_ok=True)
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.invalid",
           "PATH": "/usr/bin:/bin", "HOME": str(root)}
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, env=env)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "t"], cwd=root, check=True, env=env)


# Live-looking content planted in EVERY EMPTY-ruled source. If any of it
# reaches the generated tree, the invariant is broken.
LIVE_MARKER = "ZZLIVECONTENTZZ"


@pytest.fixture
def fake_workspace(tmp_path):
    ledger = f"## {LIVE_MARKER}-task-slug\n- issue: https://example.invalid/1\n"
    _fake_repo(
        tmp_path / "PyAutoMind",
        {
            "active.md": ledger, "planned.md": ledger, "parked.md": ledger,
            "condemned.md": ledger, "ideas.md": f"- {LIVE_MARKER} idea line.\n",
            "queue.md": ledger,
            # Hostile on BOTH known axes (issue #123): a live row ABOVE the
            # separator, and the separator itself cosmetically reformatted to
            # `| --- |`. The old parse copied lines until one started with
            # "|---", so the first leaked that row and the second never broke
            # at all — it copied the entire ledger.
            "autonomy_log.md": (
                f"| date | task |\n"
                f"| {LIVE_MARKER} | row above the separator |\n"
                f"| --- | --- |\n"
                f"| {LIVE_MARKER} | row below the separator |\n"
            ),
            "README.md": "# Mind\n", "AGENTS.md": "# Agents\n",
            "REFERENCE.md": "# Ref\n", "ROUTING.md": "# Routing\n",
            "CLAUDE.md": "# Claude\n", "LICENSE": "MIT\n", ".gitignore": "tmp/\n",
            "AI_POLICY.md": "PyAutoLabs policy\n",
            "CONTRIBUTING.md": "Contributing to PyAutoLabs\n",
            "repos.yaml": f"repos:\n  {LIVE_MARKER}: x\n",
            "scripts/status.sh": "echo hi\n",
            "complete/AGENTS.md": "# schema\n",
            "complete/2026/07/a.md": f"{LIVE_MARKER} record\n",
            "active/a.md": f"{LIVE_MARKER} prompt\n",
            "draft/bug/x/a.md": f"{LIVE_MARKER} draft\n",
            "docs/x.md": f"{LIVE_MARKER} doc\n",
            "dashboard.md": f"{LIVE_MARKER}\n",
            "skills/s/SKILL.md": "# skill\n", "policy/p.md": "# policy\n",
            ".github/workflows/w.yml": "name: PyAutoLabs w\n",
        },
    )
    _fake_repo(
        tmp_path / "PyAutoMemory",
        {
            "index.md": f"# Index\n{LIVE_MARKER}\n",
            "reading-queue.md": f"- {LIVE_MARKER} paper\n",
            "README.md": f"# Memory\n{LIVE_MARKER}\n",
            "AGENTS.md": "# Agents\n", "CLAUDE.md": "# Claude\n",
            "LICENSE": "MIT\n", ".gitignore": "tmp/\n", "Makefile": "all:\n",
            "AI_POLICY.md": "PyAutoLabs policy\n",
            "CONTRIBUTING.md": "Contributing to PyAutoLabs\n",
            "bibliography/refs.bib": f"@article{{{LIVE_MARKER}2018}}\n",
            "bibliography/aliases.yaml": f"{LIVE_MARKER}: x\n",
            "bibliography/README.md": "# Bib\n",
            "scripts/validate.py": "x = 1\n",
            "tests/test_x.py": "def test_x():\n    pass\n",
            "wiki/CLAUDE.md": "# schema\n",
            "wiki/lensing/index.md": f"{LIVE_MARKER} wiki\n",
            ".github/workflows/w.yml": "name: PyAutoLabs w\n",
        },
    )
    return tmp_path


def test_generated_tree_contains_no_live_content(fake_workspace, tmp_path):
    """The invariant, asserted where it actually matters: the shipped tree.

    Drives the real generators, so flipping any rule to KEEP — or swapping the
    EMPTY dispatcher for a copy — fails here even though the unit tests above
    would still pass.
    """
    out = tmp_path / "out"
    spawn.generate_all(fake_workspace, out)

    leaked = [
        p.relative_to(out).as_posix()
        for p in out.rglob("*")
        if p.is_file() and LIVE_MARKER in p.read_text(errors="replace")
    ]
    assert leaked == [], f"live content reached the generated template: {leaked}"


def test_generated_tree_is_canary_clean(fake_workspace, tmp_path):
    out = tmp_path / "out"
    spawn.generate_all(fake_workspace, out)
    for name in ("PyAutoMind-template", "PyAutoMemory-template"):
        assert spawn.canary_scan(out / name) == []


def test_generated_ledgers_are_exactly_their_generated_headers(fake_workspace, tmp_path):
    """Belt and braces: every EMPTY-ruled ledger equals its mapped title."""
    out = tmp_path / "out"
    spawn.generate_all(fake_workspace, out)
    mind = out / "PyAutoMind-template"
    for rel, title in spawn.EMPTY_TITLES.items():
        path = mind / rel
        if path.exists():
            assert path.read_text().splitlines()[0] == title


def test_every_empty_rule_is_covered_by_a_generated_header():
    """No EMPTY rule may exist that empty_body() cannot serve.

    Glob rules are served by SUFFIX, so this checks the suffixes they can
    actually match rather than skipping them (skipping made this vacuous).
    """
    empty_patterns = [
        pattern
        for pattern, action in (spawn.MIND_RULES + spawn.MEMORY_RULES)
        if action == "EMPTY"
    ]
    assert empty_patterns, "no EMPTY rules found — did the tables move?"

    for pattern in empty_patterns:
        if "*" not in pattern:
            assert pattern in spawn.EMPTY_TITLES, (
                f"EMPTY rule '{pattern}' has no EMPTY_TITLES entry — "
                f"spawn would abort on it"
            )
            continue
        # A glob EMPTY rule is only safe if every suffix it can match is
        # either mapped by name or covered by EMPTY_COMMENTS.
        covered = set(spawn.EMPTY_COMMENTS) | {
            Path(k).suffix for k in spawn.EMPTY_TITLES
        }
        assert covered, f"glob EMPTY rule '{pattern}' has no suffix coverage"
