
#!/usr/bin/env python3
"""
Python Webhook Monitor
----------------------
Send test webhook events and validate endpoint responses.

Usage:
    python practice-advanced/python-webhook-monitor.py
    python practice-advanced/python-webhook-monitor.py --url http://localhost:5000/webhook
    python practice-advanced/python-webhook-monitor.py --timeout 10
    python practice-advanced/python-webhook-monitor.py --output webhook-report.json
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SAMPLE_EVENTS = [
    {
        "event": "user.registered",
        "event_id": "evt_001",
        "data": {
            "user_id": 101,
            "username": "demo_user",
        },
    },
    {
        "event": "payment.completed",
        "event_id": "evt_002",
        "data": {
            "payment_id": 501,
            "amount": 1500,
            "currency": "INR",
        },
    },
    {
        "event": "deployment.completed",
        "event_id": "evt_003",
        "data": {
            "application": "DevOps Demo",
            "environment": "staging",
            "status": "success",
        },
    },
]


def send_webhook(url, event, timeout, expected_status):
    """Send one webhook event and validate its response."""

    payload = json.dumps(event).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Python-Webhook-Monitor/1.0",
        },
    )

    start = time.perf_counter()

    result = {
        "event_id": event["event_id"],
        "event_type": event["event"],
        "url": url,
        "status": "FAILED",
        "http_status": None,
        "response_time_ms": None,
        "error": None,
    }

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            result["http_status"] = response.status
            result["status"] = (
                "SUCCESS"
                if response.status == expected_status
                else "FAILED"
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


def monitor_webhooks(url, timeout, expected_status):
    """Execute all sample webhook events."""

    results = []

    print("\nWEBHOOK MONITOR")
    print("=" * 65)

    for event in SAMPLE_EVENTS:
        print(f"\nSending event: {event['event']}")

        result = send_webhook(
            url,
            event,
            timeout,
            expected_status,
        )

        results.append(result)

        print(f"Status: {result['status']}")
        print(f"HTTP Status: {result['http_status']}")
        print(f"Response Time: {result['response_time_ms']} ms")

        if result["error"]:
            print(f"Error: {result['error']}")

    return results


def generate_summary(results):
    """Calculate webhook execution statistics."""

    total = len(results)
    successful = sum(
        result["status"] == "SUCCESS"
        for result in results
    )

    failed = total - successful

    latencies = [
        result["response_time_ms"]
        for result in results
    ]

    return {
        "total_events": total,
        "successful": successful,
        "failed": failed,
        "success_rate_percent": round(
            successful / total * 100, 2
        ) if total else 0,
        "average_response_time_ms": round(
            sum(latencies) / len(latencies), 2
        ) if latencies else 0,
    }


def save_report(results, summary, output):
    """Save webhook results to a JSON file."""

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
        description="Test and monitor webhook endpoints."
    )

    parser.add_argument(
        "--url",
        default="http://localhost:5000/webhook",
        help="Webhook endpoint URL.",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Request timeout in seconds.",
    )

    parser.add_argument(
        "--expected-status",
        type=int,
        default=200,
        help="Expected HTTP response status.",
    )

    parser.add_argument(
        "--output",
        default="webhook-report.json",
        help="JSON report output filename.",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero.")

    if not 100 <= args.expected_status <= 599:
        parser.error("Expected HTTP status must be between 100 and 599.")

    results = monitor_webhooks(
        args.url,
        args.timeout,
        args.expected_status,
    )

    summary = generate_summary(results)

    print("\n" + "=" * 65)
    print("WEBHOOK EXECUTION SUMMARY")
    print("=" * 65)

    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    save_report(results, summary, args.output)

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
