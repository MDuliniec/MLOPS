from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from smoke_test import check_health, main, parse_args


def test_check_health_returns_true_on_200() -> None:
    mock_response = MagicMock()
    mock_response.status = 200

    with patch("smoke_test.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response
        result = check_health("http://192.168.56.10:30080/health", timeout=3.0)

    assert result is True
    mock_urlopen.assert_called_once_with("http://192.168.56.10:30080/health", timeout=3.0)


def test_check_health_returns_false_on_non_200() -> None:
    mock_response = MagicMock()
    mock_response.status = 503

    with patch("smoke_test.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response
        result = check_health("http://192.168.56.10:30080/health")

    assert result is False


def test_check_health_returns_false_on_http_error() -> None:
    error = HTTPError(
        url="http://192.168.56.10:30080/health",
        code=500,
        msg="Internal Server Error",
        hdrs=None,
        fp=None,
    )
    with patch("smoke_test.urlopen", side_effect=error):
        assert check_health("http://192.168.56.10:30080/health") is False


def test_check_health_returns_false_on_url_error() -> None:
    with patch("smoke_test.urlopen", side_effect=URLError("Connection refused")):
        assert check_health("http://192.168.56.10:30080/health") is False


def test_check_health_returns_false_on_timeout() -> None:
    with patch("smoke_test.urlopen", side_effect=TimeoutError("timed out")):
        assert check_health("http://192.168.56.10:30080/health") is False


def test_parse_args_reads_health_url_from_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HEALTH_URL", "http://127.0.0.1:9000/health")
    args = parse_args([])
    assert args.url == "http://127.0.0.1:9000/health"


def test_main_returns_zero_when_healthy() -> None:
    with patch("smoke_test.check_health", return_value=True):
        assert main(["http://192.168.56.10:30080/health"]) == 0


def test_main_returns_one_when_unhealthy() -> None:
    with patch("smoke_test.check_health", return_value=False):
        assert main(["http://192.168.56.10:30080/health"]) == 1
