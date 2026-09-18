"""The arXiv API GET retries throttling, and the recall guard never fails on it.

Both digests died on 2026-09-14/15 with an HTTP 429 on their *first* request,
in `--livecheck`, before anything was fetched — so #papers went silent and the
Memory inbox stamp went stale, the two signals that are supposed to mean "the
run broke", for a cause that was arXiv throttling a shared runner egress. No
network here: urlopen and sleep are stubbed.
"""
import importlib.util
import io
import sys
import urllib.error
from pathlib import Path

import pytest

FETCH_PY = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "arxiv_fetch.py"
_spec = importlib.util.spec_from_file_location("arxiv_fetch_under_test", FETCH_PY)
af = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(af)


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _http_error(code, headers=None):
    return urllib.error.HTTPError("https://export.arxiv.org/api/query", code,
                                  "err", headers or {}, None)


@pytest.fixture
def no_sleep(monkeypatch):
    slept = []
    monkeypatch.setattr(af.time, "sleep", slept.append)
    return slept


def _stub_urlopen(monkeypatch, answers):
    """answers: a list of exceptions to raise or bytes to return, in order."""
    calls = []

    def fake(req, timeout=60):
        calls.append(req.full_url)
        a = answers.pop(0)
        if isinstance(a, BaseException):
            raise a
        return _Resp(a)

    monkeypatch.setattr(af.urllib.request, "urlopen", fake)
    return calls


def test_get_retries_429_then_succeeds(monkeypatch, no_sleep):
    calls = _stub_urlopen(monkeypatch, [_http_error(429), _http_error(429), b"<feed/>"])
    assert af._get({"q": 1}, delays=(1, 2, 3)) == b"<feed/>"
    assert len(calls) == 3
    assert no_sleep == [1, 2]


def test_get_honours_retry_after_within_cap(monkeypatch, no_sleep):
    _stub_urlopen(monkeypatch, [_http_error(429, {"Retry-After": "7"}),
                                _http_error(429, {"Retry-After": "9999"}),
                                b"ok"])
    af._get({}, delays=(1, 2, 30))
    # 7 > 1 so the header wins; 9999 is capped at the ladder's longest step.
    assert no_sleep == [7, 30]


def test_get_gives_up_after_the_ladder(monkeypatch, no_sleep):
    _stub_urlopen(monkeypatch, [_http_error(429)] * 3)
    with pytest.raises(urllib.error.HTTPError):
        af._get({}, delays=(1, 2))
    assert no_sleep == [1, 2]


def test_get_does_not_retry_a_bad_request(monkeypatch, no_sleep):
    calls = _stub_urlopen(monkeypatch, [_http_error(400), b"never"])
    with pytest.raises(urllib.error.HTTPError):
        af._get({}, delays=(1, 2))
    assert len(calls) == 1 and no_sleep == []


def test_get_retries_connection_errors(monkeypatch, no_sleep):
    _stub_urlopen(monkeypatch, [urllib.error.URLError("reset"), TimeoutError(), b"ok"])
    assert af._get({}, delays=(1, 2)) == b"ok"
    assert no_sleep == [1, 2]


def test_livecheck_network_failure_is_a_warning_not_a_failure(monkeypatch, no_sleep, capsys):
    monkeypatch.setattr(af, "RETRY_DELAYS", (1,))
    _stub_urlopen(monkeypatch, [_http_error(429)] * 2)
    assert af._livecheck() == 0
    err = capsys.readouterr().err
    assert "::warning::" in err and "SKIPPED" in err


def test_livecheck_still_fails_on_a_real_recall_regression(monkeypatch, no_sleep, capsys):
    ids = list(af.KNOWN_MATCHES)
    feed = ('<feed xmlns="http://www.w3.org/2005/Atom">'
            + "".join(f"<entry><id>http://arxiv.org/abs/{i}v1</id></entry>" for i in ids[1:])
            + "</feed>").encode()
    _stub_urlopen(monkeypatch, [feed])
    assert af._livecheck() == 1
    assert f"[FAIL] {ids[0]}" in capsys.readouterr().err


def test_fetch_goes_through_the_retrying_get(monkeypatch, no_sleep):
    calls = _stub_urlopen(monkeypatch, [_http_error(503), b"page"])
    monkeypatch.setattr(af, "RETRY_DELAYS", (1,))
    assert af.fetch("q", 5, start=10) == b"page"
    assert "start=10" in calls[0] and "max_results=5" in calls[0]


def test_get_retries_406_like_a_429(monkeypatch, no_sleep):
    """406 is edge mitigation against the shared runner egress, not a bad request.

    2026-09-17 and 2026-09-18 both died on an HTTP 406 where 09-15 died on a
    429 — same first request, same runner, same silence in #papers. The headers
    were probed live on 2026-09-18 and all four {bare UA, contact UA} x {no
    Accept, application/atom+xml} combinations answered 200 from a home IP, so
    the 406 is not content negotiation: it is the same throttle wearing a
    different status code, and it has to climb the same ladder.
    """
    calls = _stub_urlopen(monkeypatch, [_http_error(406)] * 3 + [b"<feed/>"])
    assert af._get({"q": 1}, delays=(1, 2, 3)) == b"<feed/>"
    assert len(calls) == 4
    assert no_sleep == [1, 2, 3]


def test_fetch_survives_a_406_sequence(monkeypatch, no_sleep):
    """The *fetch* step, not just the guard — this is what killed 09-17/18.

    `_livecheck()` warns and returns 0 on any HTTPError, so it survived the 406
    on its own; the run then died one step later in `fetch()`, which is also the
    entry point `arxiv_interests.py` calls. Both digests need this path.
    """
    calls = _stub_urlopen(monkeypatch, [_http_error(406)] * 3 + [b"page"])
    monkeypatch.setattr(af, "RETRY_DELAYS", (1, 2, 3))
    assert af.fetch("q", 5, start=10) == b"page"
    assert len(calls) == 4 and no_sleep == [1, 2, 3]
    assert "start=10" in calls[0] and "max_results=5" in calls[0]
