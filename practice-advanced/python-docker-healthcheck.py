
#!/usr/bin/env python3
"""
Docker Application Health Check
--------------------------------
Checks whether an HTTP application endpoint is healthy.

Usage:
    python practice-advanced/python-docker-healthcheck.py
    python practice-advanced/python-docker-healthcheck.py \
        --url http://localhost:5000/health
    python practice-advanced/python-docker-healthcheck.py \
        --url https://example.com/health --retries 5
"""

import argparse
import time
import urllib.error
import urllib.request


def check_endpoint(url, timeout, expected_status):
    """Check an HTTP endpoint and validate its response status."""

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "DevOps-Health-Checker"},
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status

            if status == expected_status:
                print(f"[HEALTHY] HTTP {status} - {url}")
                return True

            print(
                f"[UNHEALTHY] Expected HTTP {expected_status}, "
                f"received HTTP {status}"
            )
            return False

    except urllib.error.HTTPError as error:
        print(f"[UNHEALTHY] HTTP {error.code} - {url}")

    except urllib.error.URLError as error:
        print(f"[UNHEALTHY] Connection failed: {error.reason}")

    except TimeoutError:
        print(f"[UNHEALTHY] Request timed out after {timeout}s")

    except OSError as error:
        print(f"[UNHEALTHY] Network error: {error}")

    return False


def run_health_check(args):
    """Retry the health check until success or attempts are exhausted."""

    print("=" * 50)
    print("APPLICATION HEALTH CHECK")
    print("=" * 50)
    print(f"URL: {args.url}")
    print(f"Retries: {args.retries}")
    print()

    for attempt in range(1, args.retries + 1):
        print(f"Attempt {attempt}/{args.retries}")

        if check_endpoint(
            args.url,
            args.timeout,
            args.expected_status,
        ):
            print("\nResult: Application is healthy.")
            return 0

        if attempt < args.retries:
            time.sleep(args.interval)

    print("\nResult: Application is unhealthy.")
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="HTTP application health checker."
    )

    parser.add_argument(
        "--url",
        default="http://localhost:5000/health",
        help="Application health endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Maximum number of attempts.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2,
        help="Delay between attempts in seconds.",
    )
    parser.add_argument(
        "--expected-status",
        type=int,
        default=200,
        help="Expected HTTP response status.",
    )

    args = parser.parse_args()

    if (
        args.timeout <= 0
        or args.retries < 1
        or args.interval < 0
        or not 100 <= args.expected_status <= 599
    ):
        parser.error("Invalid timeout, retries, interval, or HTTP status.")

    return run_health_check(args)


if __name__ == "__main__":
    raise SystemExit(main())
