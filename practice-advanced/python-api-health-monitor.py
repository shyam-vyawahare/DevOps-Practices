
#!/usr/bin/env python3
"""
Python API Health Monitor
-------------------------
Monitor REST API endpoints and generate health reports.

Usage:
    python practice-advanced/python-api-health-monitor.py
    python practice-advanced/python-api-health-monitor.py --timeout 5
    python practice-advanced/python-api-health-monitor.py --output api-report.json
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


API_ENDPOINTS = [
    {
        "name": "JSONPlaceholder Posts",
        "url": "https://jsonplaceholder.typicode.com/posts",
        "method": "GET",
        "expected_status": 200,
    },
    {
        "name": "JSONPlaceholder Users",
        "url": "https://jsonplaceholder.typicode.com/users",
        "method": "GET",
        "expected_status": 200,
    },
    {
        "name": "GitHub API",
        "url": "https://api.github.com",
        "method": "GET",
        "expected_status": 200,
    },
]


def check_api(endpoint, timeout):
    """Check an API endpoint and measure response latency."""

    name = endpoint["name"]
    url = endpoint["url"]
    method = endpoint["method"]
    expected = endpoint["expected_status"]

    result = {
        "name": name,
        "url": url,
        "method": method,
        "status": "UNHEALTHY",
        "http_status": None,
        "expected_status": expected,
        "response_time_ms": None,
        "error": None,
    }

    request = urllib.request.Request(
        url,
        method=method,
        headers={
            "Accept": "application/json",
            "User-Agent": "Python-API-Health-Monitor/1.0",
        },
    )

    start = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            result["http_status"] = response.status
            result["status"] = (
                "HEALTHY"
                if response.status == expected
                else "UNHEALTHY"
            )

    except urllib.error.HTTPError as error:
        result["http_status"] = error.code
        result["error"] = f"HTTP error: {error.code}"

    except urllib.error.URLError as error:
        result["error"] = f"Connection error: {error.reason}"

    except TimeoutError:
        result["error"] = "Request timed out"

    except OSError as error:
        result["error"] = str(error)

    finally:
        result["response_time_ms"] = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

    return result


def monitor_apis(timeout):
    """Monitor all configured API endpoints."""

    results = []

    print("\nAPI HEALTH MONITOR")
    print("=" * 65)

    for endpoint in API_ENDPOINTS:
        print(f"\nChecking: {endpoint['name']}")

        result = check_api(endpoint, timeout)
        results.append(result)

        print(f"Status: {result['status']}")
        print(f"HTTP Code: {result['http_status']}")
        print(f"Response Time: {result['response_time_ms']} ms")

        if result["error"]:
            print(f"Error: {result['error']}")

    return results


def generate_summary(results):
    """Generate an overall API monitoring summary."""

    total = len(results)
    healthy = sum(
        result["status"] == "HEALTHY"
        for result in results
    )

    unhealthy = total - healthy

    latencies = [
        result["response_time_ms"]
        for result in results
        if result["response_time_ms"] is not None
    ]

    return {
        "total_apis": total,
        "healthy": healthy,
        "unhealthy": unhealthy,
        "availability_percent": round(
            healthy / total * 100, 2
        ) if total else 0,
        "average_latency_ms": round(
            sum(latencies) / len(latencies), 2
        ) if latencies else None,
    }


def save_report(results, summary, output):
    """Export API monitoring results to JSON."""

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "results": results,
    }

    Path(output).write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(f"\nReport saved: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor REST API endpoint health."
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Request timeout in seconds.",
    )

    parser.add_argument(
        "--output",
        default="api-health-report.json",
        help="JSON report filename.",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero.")

    results = monitor_apis(args.timeout)
    summary = generate_summary(results)

    print("\n" + "=" * 65)
    print("API MONITORING SUMMARY")
    print("=" * 65)

    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    save_report(results, summary, args.output)

    return 0 if summary["unhealthy"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
