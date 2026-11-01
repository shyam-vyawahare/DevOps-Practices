
#!/usr/bin/env python3
"""
Python Multi-Service Monitor
----------------------------
Monitor multiple service endpoints and generate a JSON report.

Usage:
    python practice-advanced/python-service-monitor.py
    python practice-advanced/python-service-monitor.py --timeout 3
    python practice-advanced/python-service-monitor.py --output report.json
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SERVICES = {
    "Example Website": "https://example.com",
    "Python Package Index": "https://pypi.org",
    "GitHub": "https://github.com",
}


def monitor_service(name, url, timeout):
    """Check a service and measure its response time."""

    start_time = time.perf_counter()

    result = {
        "service": name,
        "url": url,
        "status": "UNHEALTHY",
        "http_status": None,
        "response_time_ms": None,
        "error": None,
    }

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Python-Service-Monitor/1.0"},
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            result["http_status"] = response.status
            result["status"] = (
                "HEALTHY"
                if 200 <= response.status < 400
                else "UNHEALTHY"
            )

    except urllib.error.HTTPError as error:
        result["http_status"] = error.code
        result["error"] = f"HTTP error: {error.code}"

    except urllib.error.URLError as error:
        result["error"] = f"Connection error: {error.reason}"

    except TimeoutError:
        result["error"] = "Connection timed out"

    except OSError as error:
        result["error"] = str(error)

    finally:
        elapsed = time.perf_counter() - start_time
        result["response_time_ms"] = round(elapsed * 1000, 2)

    return result


def generate_report(results):
    """Create an overall monitoring summary."""

    total = len(results)
    healthy = sum(
        item["status"] == "HEALTHY" for item in results
    )
    unhealthy = total - healthy

    response_times = [
        item["response_time_ms"] for item in results
    ]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_services": total,
            "healthy": healthy,
            "unhealthy": unhealthy,
            "availability_percent": round(
                healthy / total * 100, 2
            ) if total else 0,
            "average_response_time_ms": round(
                sum(response_times) / total, 2
            ) if total else 0,
        },
        "services": results,
    }


def display_report(report):
    """Display monitoring results in the terminal."""

    print("\n" + "=" * 75)
    print("MULTI-SERVICE MONITORING REPORT")
    print("=" * 75)

    for service in report["services"]:
        status = service["status"]

        print(f"\nService: {service['service']}")
        print(f"URL: {service['url']}")
        print(f"Status: {status}")
        print(f"HTTP Status: {service['http_status']}")
        print(f"Response Time: {service['response_time_ms']} ms")

        if service["error"]:
            print(f"Error: {service['error']}")

    summary = report["summary"]

    print("\n" + "-" * 75)
    print("OVERALL SUMMARY")
    print("-" * 75)
    print(f"Total Services: {summary['total_services']}")
    print(f"Healthy: {summary['healthy']}")
    print(f"Unhealthy: {summary['unhealthy']}")
    print(f"Availability: {summary['availability_percent']}%")
    print(
        f"Average Response Time: "
        f"{summary['average_response_time_ms']} ms"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor multiple HTTP services."
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Request timeout in seconds (default: 5).",
    )

    parser.add_argument(
        "--output",
        default="service-monitor-report.json",
        help="JSON report output path.",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero.")

    results = []

    for name, url in SERVICES.items():
        print(f"Checking {name}...")
        results.append(
            monitor_service(name, url, args.timeout)
        )

    report = generate_report(results)
    display_report(report)

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(f"\nJSON report saved to: {output_path}")

    return 0 if report["summary"]["unhealthy"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
