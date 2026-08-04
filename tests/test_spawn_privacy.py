"""The privacy invariant required by docs/pyautobrain/spawn_spec.md.

    "no live wiki page, bibliography entry, reading-queue line, prompt, or
     registry entry may ever appear in a template output. The implementation
     must include a test asserting the generated tree contains none of a
     canary list of live-content markers."

The regression these lock down (issue #118): `empty_body()` used to return
line 1 of the live file. `planned.md` and `ideas.md` carry no H1 at all, so
their first line is a registry entry, and spawn stamped it into the public
fresh-slate templates. A heading-shape test would NOT have caught it —
`## rhayes-audit-validation-phases-2-4` is a valid `##` heading.

Hermetic: everything below runs on synthetic inputs, so the suite needs no
live PyAutoMind/PyAutoMemory checkout.
"""

import importlib.util
from pathlib import Path

import pytest

SPAWN_PY = Path(__file__).resolve().parents[1] / "scripts" / "spawn.py"

_spec = importlib.util.spec_from_file_location("spawn", SPAWN_PY)
spawn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spawn)


# Content shaped like the real leaks: a registry H2 slug, a raw idea bullet,
# and an instance-flavoured H1 that a heading test would have waved through.
HOSTILE_BODIES = [
    "## rhayes-audit-validation-phases-2-4\n- issue: https://example/1\n",
    "- lens_calc_zero_contour_jax autolens workspace guide.\n",
    "# Pytree variant queue\n\n1. slacs0946 refit\n",
    "",
]


# Read lazily so the suite still COLLECTS against a spawn.py that predates
# EMPTY_TITLES. Otherwise the decisive regression tests below never run — they
# would be masked by a collection error, which proves only that the API moved.
EMPTY_TITLES = getattr(spawn, "EMPTY_TITLES", {})


def test_planned_md_never_carries_a_registry_entry(tmp_path):
    """The exact issue #118 regression, in the smallest form that catches it.

    Depends on nothing but `empty_body`, so it fails with a clean assertion
    against the pre-fix implementation rather than erroring at import.
    """
    src = tmp_path / "planned.md"
    src.write_text("## rhayes-audit-validation-phases-2-4\n- issue: https://x/1\n")
    assert "rhayes" not in spawn.empty_body(src)


def test_ideas_md_never_carries_an_idea_line(tmp_path):
    """The leak that actually reached the published template."""
    src = tmp_path / "ideas.md"
    src.write_text("- lens_calc_zero_contour_jax autolens workspace guide.\n")
    assert "lens_calc_zero_contour_jax" not in spawn.empty_body(src)


@pytest.mark.parametrize("name,title", sorted(EMPTY_TITLES.items()))
@pytest.mark.parametrize("body", HOSTILE_BODIES)
def test_empty_output_contains_no_source_bytes(tmp_path, name, title, body):
    """Every EMPTY output is exactly the generated title + marker."""
    src = tmp_path / name
    src.write_text(body)

    out = spawn.empty_body(src)

    assert out.startswith(title + "\n\n"), f"{name} lost its generated title"
    # The only lines are the title, a blank, and the schema-pointer marker.
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 2, f"{name} emitted unexpected lines: {lines!r}"
    assert lines[0] == title

    # Nothing from the source survived. Checked line-wise so a title that
    # legitimately shares a word with the body cannot mask a real leak.
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


@pytest.mark.parametrize(
    "filename,lead",
    [("pyautomemory.bib", "%"), ("bibkey_aliases.yaml", "#"), ("x.yml", "#")],
)
def test_glob_matched_empty_files_get_comment_headers(tmp_path, filename, lead):
    """spawn_spec.md rule 2: bibliography files keep a generated header comment.

    The header and marker must both be comments — a YAML/BibTeX consumer parses
    every non-comment line, so an HTML comment would read as content.
    """
    src = tmp_path / filename
    src.write_text("@article{Nightingale2018, title={SLACS lens}}\n")

    out = spawn.empty_body(src)

    assert out.startswith(lead)
    for line in [ln for ln in out.splitlines() if ln.strip()]:
        assert line.startswith(lead), f"non-comment line in {filename}: {line!r}"
    assert "Nightingale2018" not in out
    assert "SLACS" not in out


def test_canary_scan_catches_a_leaked_registry_slug(tmp_path):
    """The scan must flag a task slug, not just a science dataset name."""
    (tmp_path / "planned.md").write_text("## rhayes-audit-validation-phases-2-4\n")
    hits = spawn.canary_scan(tmp_path)
    assert any("rhayes" in h for h in hits), hits


def test_canary_scan_catches_dataset_tokens(tmp_path):
    (tmp_path / "notes.md").write_text("refit of SLACS0946 with arctic clocking\n")
    hits = spawn.canary_scan(tmp_path)
    assert any("slacs" in h for h in hits)
    assert any("arctic" in h for h in hits)


def test_licence_may_name_its_copyright_holder(tmp_path):
    """Attribution in a licence is the point of a licence, not a leak."""
    (tmp_path / "LICENSE").write_text("MIT\n  (James Nightingale / Jammy2211).\n")
    assert spawn.canary_scan(tmp_path) == []


def test_the_licence_exemption_is_narrow(tmp_path):
    """The exemption is per-file AND per-token — it must not become a hole."""
    # Same name, different file: still a leak.
    (tmp_path / "AGENTS.md").write_text("ask James Nightingale about this\n")
    assert any("nightingale" in h for h in spawn.canary_scan(tmp_path))

    # Same file, different token: still a leak.
    (tmp_path / "AGENTS.md").unlink()
    (tmp_path / "LICENSE").write_text("MIT (James Nightingale) — slacs0946\n")
    hits = spawn.canary_scan(tmp_path)
    assert any("slacs" in h for h in hits)
    assert not any("nightingale" in h for h in hits)


def test_spawn_py_is_exempt_from_its_own_token_list(tmp_path):
    """spawn.py DEFINES the tokens; that definition is not leaked content."""
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "spawn.py").write_text(f"CANARY_TOKENS = {spawn.CANARY_TOKENS!r}\n")
    assert spawn.canary_scan(tmp_path) == []


def test_every_empty_rule_is_covered_by_a_generated_header():
    """No EMPTY rule may exist that empty_body() cannot serve.

    Guards the seam between the partition tables and the header maps: adding
    an EMPTY rule without a title is caught here rather than at spawn time.
    """
    empty_globs = [
        pattern
        for pattern, action in (spawn.MIND_RULES + spawn.MEMORY_RULES)
        if action == "EMPTY"
    ]
    assert empty_globs, "no EMPTY rules found — did the tables move?"

    for pattern in empty_globs:
        if "*" in pattern:
            # Glob rules are served by suffix; every suffix they can match
            # must have a generated comment header.
            continue
        name = Path(pattern).name
        assert name in spawn.EMPTY_TITLES, (
            f"EMPTY rule '{pattern}' has no EMPTY_TITLES entry — "
            f"spawn would abort on it"
        )
