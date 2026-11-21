import argparse
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

DEFAULT_URL = "http://192.168.56.10:30080/health"
DEFAULT_TIMEOUT = 5.0


def check_health(url: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """Odpytuje endpoint /health i zwraca True dla odpowiedzi HTTP 200."""
    try:
        with urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except (HTTPError, URLError, TimeoutError, OSError):
        return False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke test sprawdzający dostępność endpointu /health."
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=os.getenv("HEALTH_URL", DEFAULT_URL),
        help="Adres URL endpointu /health (domyślnie HEALTH_URL lub k3s).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Limit czasu odpowiedzi w sekundach.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if check_health(args.url, timeout=args.timeout):
        print(f"OK: {args.url} odpowiedział statusem 200.")
        return 0
    print(f"BŁĄD: {args.url} nie odpowiada poprawnie.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
