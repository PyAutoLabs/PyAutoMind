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


def _stub_curl(monkeypatch, answers):
    """Stub the alternate transport at its Python boundary."""
    calls = []

    def fake(url):
        calls.append(url)
        a = answers.pop(0)
        if isinstance(a, BaseException):
            raise a
        return a

    monkeypatch.setattr(af, "_curl_get", fake)
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


def test_get_uses_curl_immediately_on_urllib_406(monkeypatch, no_sleep):
    """A client-fingerprint 406 should switch transport before sleeping."""
    urllib_calls = _stub_urlopen(monkeypatch, [_http_error(406)])
    curl_calls = _stub_curl(monkeypatch, [b"<feed/>"])

    assert af._get({"q": 1}, delays=(1, 2, 3)) == b"<feed/>"
    assert len(urllib_calls) == 1
    assert len(curl_calls) == 1
    assert no_sleep == []


def test_get_still_backs_off_if_curl_is_also_refused(monkeypatch, no_sleep):
    """A real edge throttle still gets the existing retry ladder."""
    urllib_calls = _stub_urlopen(monkeypatch, [_http_error(406)] * 4)
    curl_calls = _stub_curl(
        monkeypatch, [_http_error(406)] * 3 + [b"<feed/>"]
    )

    assert af._get({"q": 1}, delays=(1, 2, 3)) == b"<feed/>"
    assert len(urllib_calls) == 4
    assert len(curl_calls) == 4
    assert no_sleep == [1, 2, 3]


def test_fetch_survives_urllib_406_via_curl(monkeypatch, no_sleep):
    """The fetch path is shared by both the lensing and interests digests."""
    urllib_calls = _stub_urlopen(monkeypatch, [_http_error(406)])
    curl_calls = _stub_curl(monkeypatch, [b"page"])

    assert af.fetch("q", 5, start=10) == b"page"
    assert len(urllib_calls) == 1 and len(curl_calls) == 1
    assert no_sleep == []
    assert "start=10" in urllib_calls[0] and "max_results=5" in urllib_calls[0]


def test_curl_get_parses_body_and_status(monkeypatch):
    seen = {}

    class Result:
        returncode = 0
        stdout = b"<feed/>\n__PYAUTO_HTTP_STATUS__:200"
        stderr = b""

    def fake_run(command, capture_output, check):
        seen["command"] = command
        assert capture_output is True
        assert check is False
        return Result()

    monkeypatch.setattr(af.subprocess, "run", fake_run)
    assert af._curl_get("https://example.test/query") == b"<feed/>"
    command = seen["command"]
    assert af.USER_AGENT in command
    assert f"Accept: {af.ACCEPT}" in command
