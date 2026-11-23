
import argparse
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


def check_website(url, timeout):
    """Check website availability and response time."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Python-Uptime-Monitor/1.0"}
    )

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout
        ) as response:

            elapsed = (time.perf_counter() - start_time) * 1000

            return {
                "url": url,
                "status": "UP",
                "status_code": response.status,
                "response_time_ms": round(elapsed, 2),
                "error": None
            }

    except urllib.error.HTTPError as error:
        elapsed = (time.perf_counter() - start_time) * 1000

        return {
            "url": url,
            "status": "UP" if error.code < 500 else "DOWN",
            "status_code": error.code,
            "response_time_ms": round(elapsed, 2),
            "error": str(error)
        }

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        elapsed = (time.perf_counter() - start_time) * 1000

        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": round(elapsed, 2),
            "error": str(error)
        }


def save_history(report, output_file):
    """Append monitoring results to a JSON history file."""

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        try:
            history = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                raise ValueError("History must be a JSON list.")
        except (json.JSONDecodeError, ValueError):
            raise ValueError("Existing history file is invalid.")
    else:
        history = []

    history.append(report)

    path.write_text(
        json.dumps(history, indent=4),
        encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Python website uptime monitoring tool"
    )

    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more website URLs to monitor"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="Request timeout in seconds"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Seconds between monitoring rounds (0 = one-time check)"
    )

    parser.add_argument(
        "--output",
        default="reports/uptime-history.json",
        help="JSON monitoring history file"
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    if args.interval < 0:
        parser.error("--interval cannot be negative")

    urls = [
        url if url.startswith(("http://", "https://"))
        else "https://" + url
        for url in args.urls
    ]

    print("=" * 65)
    print("                  WEBSITE UPTIME MONITOR")
    print("=" * 65)

    try:
        while True:
            timestamp = datetime.now(timezone.utc).isoformat()

            print(f"\nMonitoring time: {timestamp}")
            print("-" * 65)

            results = []

            for url in urls:
                result = check_website(url, args.timeout)
                results.append(result)

                print(
                    f"{result['status']:<5} | "
                    f"{result['status_code'] or 'N/A':<5} | "
                    f"{result['response_time_ms']:>9.2f} ms | "
                    f"{url}"
                )

                if result["error"]:
                    print(f"       Error: {result['error']}")

            report = {
                "timestamp": timestamp,
                "total": len(results),
                "up": sum(r["status"] == "UP" for r in results),
                "down": sum(r["status"] == "DOWN" for r in results),
                "results": results
            }

            save_history(report, args.output)

            print("-" * 65)
            print(
                f"Summary: {report['up']} UP | "
                f"{report['down']} DOWN"
            )
            print(f"History saved: {args.output}")

            if args.interval == 0:
                break

            print(f"\nNext check in {args.interval} seconds...")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


if __name__ == "__main__":
    main()
