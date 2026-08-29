"""Contract test for the curated Highlights band in `complete/index.md`.

`lifecycle.py index --check` is a byte-for-byte round trip over the WHOLE file,
so a hand-curated band that the renderer re-emits differently turns the CI drift
check red on a file nobody touched. The band is also the only hand-written thing
in a generated file — if regeneration ever ate it, the curation is lost silently
and the index still looks healthy.

Fictional fixtures only: `tests/**` is KEEP-copied verbatim into the public
template (see `test_spawn_privacy.py`), so nothing here names a real repository,
task or record.
"""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lifecycle  # noqa: E402


BAND = """## Highlights

### Flywheel calibration

- [sprocket-calibration](2026/08/sprocket-calibration.md) — a torque baseline
  measured on a warm rig cannot grade a cold one; re-measure both columns
  back-to-back.
- [widget-alignment](2026/08/widget-alignment.md) — the alignment jig reads its
  own last result when the output directory is not cleared."""


def _mind(root: Path, *, band: str) -> Path:
    """A tiny fictional Mind: two dated records + an index carrying `band`."""
    complete = root / "complete"
    bucket = complete / "2026" / "08"
    bucket.mkdir(parents=True)
    (bucket / "sprocket-calibration.md").write_text(
        "## sprocket-calibration\n- summary: re-measured the torque baseline\n"
    )
    (bucket / "widget-alignment.md").write_text(
        "## widget-alignment\n- summary: cleared the jig output directory\n"
    )
    (complete / "index.md").write_text(
        f"{lifecycle.CURATED_START}\n{band}\n{lifecycle.CURATED_END}\n"
    )
    return complete


def _point_lifecycle_at(monkeypatch, root: Path, complete: Path) -> None:
    monkeypatch.setattr(lifecycle, "ROOT", root)
    monkeypatch.setattr(lifecycle, "COMPLETE_DIR", complete)
    monkeypatch.setattr(lifecycle, "ARCHIVE_DIR", complete / "archive")
    monkeypatch.setattr(lifecycle, "INDEX_MD", complete / "index.md")


def test_a_curated_band_survives_index_regeneration_byte_for_byte(
    tmp_path, monkeypatch
):
    """Headings and markdown-link bullets inside the CURATED markers must come
    back out of `index --apply` unchanged, and `index --check` must then be
    clean — the band and the renderer have to agree on every byte."""
    complete = _mind(tmp_path, band=BAND)
    _point_lifecycle_at(monkeypatch, tmp_path, complete)

    assert lifecycle.cmd_index(SimpleNamespace(check=False, apply=True)) == 0

    rendered = (complete / "index.md").read_text()
    band_back = rendered.split(lifecycle.CURATED_START, 1)[1].split(
        lifecycle.CURATED_END, 1
    )[0]
    assert band_back == f"\n{BAND}\n"
    # the generated half is still built from the records themselves
    assert "- [sprocket-calibration](2026/08/sprocket-calibration.md)" in (
        rendered.split(lifecycle.GEN_START, 1)[1]
    )

    assert lifecycle.cmd_index(SimpleNamespace(check=True, apply=False)) == 0
