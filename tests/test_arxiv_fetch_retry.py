"""A 429 from arXiv must cost a retry, never the morning's digest.

On 2026-09-14 both arXiv digests died on a single unretried `HTTP Error 429`:
the lensing one in `--livecheck`, which runs *before* the fetch, so #papers got
no post at all; the interests one on the first page of its band sweep, so
PyAutoMemory's interests list did not move either. arXiv throttles — the
interests digest pages a whole day of astro-ph back to back — and a throttle is
weather, not a broken query.

These pin the two halves of the fix in `.github/scripts/arxiv_fetch.py`:
requests are paced and retried, and the recall guard passes rather than kills
the run when the API will not answer. Hermetic: `urlopen` and `sleep` are both
replaced, so nothing here touches the network or spends wall-clock.
"""

import importlib.util
import sys
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "arxiv_fetch.py"


def _load():
    """Fresh module each test — `get()` keeps a process-wide pacing clock."""
    spec = importlib.util.spec_from_file_location("arxiv_fetch_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Response:
    def __init__(self, body):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _throttle(code=429, headers=None):
    return urllib.error.HTTPError("https://arxiv", code, "Too Many Requests",
                                  headers or {}, None)


@pytest.fixture
def mod(monkeypatch):
    module = _load()
    monkeypatch.setattr(module.time, "sleep", lambda _s: None)
    return module


def _answers(mod, monkeypatch, *outcomes):
    """Queue one outcome per call — an exception is raised, bytes are returned."""
    calls = []

    def fake_urlopen(req, timeout=None):
        outcome = outcomes[len(calls)]
        calls.append(req.full_url)
        if isinstance(outcome, Exception):
            raise outcome
        return _Response(outcome)

    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)
    return calls


def test_a_429_is_retried_and_the_papers_still_arrive(mod, monkeypatch):
    calls = _answers(mod, monkeypatch, _throttle(), _throttle(), b"<feed/>")
    assert mod.get("https://export.arxiv.org/api/query?x=1") == b"<feed/>"
    assert len(calls) == 3


def test_a_429_that_never_clears_still_raises(mod, monkeypatch):
    calls = _answers(mod, monkeypatch, *[_throttle()] * mod.MAX_ATTEMPTS)
    with pytest.raises(urllib.error.HTTPError):
        mod.get("https://export.arxiv.org/api/query?x=1")
    assert len(calls) == mod.MAX_ATTEMPTS


def test_a_bad_query_is_not_weather_and_fails_at_once(mod, monkeypatch):
    calls = _answers(mod, monkeypatch, _throttle(code=400), b"<feed/>")
    with pytest.raises(urllib.error.HTTPError):
        mod.get("https://export.arxiv.org/api/query?x=1")
    assert len(calls) == 1, "a 400 is a broken query — retrying only hides it"


def test_requests_are_paced_so_a_page_sweep_does_not_earn_a_429(mod, monkeypatch):
    slept = []
    monkeypatch.setattr(mod.time, "sleep", slept.append)
    _answers(mod, monkeypatch, b"<feed/>", b"<feed/>", b"<feed/>")
    for _ in range(3):
        mod.get("https://export.arxiv.org/api/query?x=1")
    # The first request goes straight out; each one after it waits out the floor.
    assert len(slept) == 2
    assert all(0 < s <= mod.MIN_REQUEST_INTERVAL for s in slept)


def test_retry_after_is_honoured_when_arxiv_sends_one(mod, monkeypatch):
    slept = []
    monkeypatch.setattr(mod.time, "sleep", slept.append)
    _answers(mod, monkeypatch, _throttle(headers={"Retry-After": "7"}), b"<feed/>")
    mod.get("https://export.arxiv.org/api/query?x=1")
    assert 7 in slept


def test_an_unanswerable_livecheck_passes_rather_than_killing_the_digest(
    mod, monkeypatch, capsys
):
    _answers(mod, monkeypatch, *[_throttle()] * mod.MAX_ATTEMPTS)
    assert mod._livecheck() == 0
    assert "SKIPPED" in capsys.readouterr().err


def test_a_livecheck_the_api_answers_still_catches_a_recall_regression(
    mod, monkeypatch
):
    _answers(mod, monkeypatch, b"<feed xmlns='http://www.w3.org/2005/Atom'/>")
    assert mod._livecheck() == 1, "an empty answer means the query lost the papers"


def test_a_rejected_livecheck_query_fails(mod, monkeypatch):
    _answers(mod, monkeypatch, _throttle(code=400))
    assert mod._livecheck() == 1
