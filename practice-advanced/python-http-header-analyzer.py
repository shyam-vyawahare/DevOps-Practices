
import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone


SECURITY_HEADERS = {
    "Strict-Transport-Security": (
        "HSTS",
        "Enforces HTTPS connections."
    ),
    "Content-Security-Policy": (
        "CSP",
        "Helps prevent cross-site scripting and injection attacks."
    ),
    "X-Content-Type-Options": (
        "MIME Protection",
        "Prevents MIME-type sniffing."
    ),
    "X-Frame-Options": (
        "Clickjacking Protection",
        "Controls whether a page can be embedded in frames."
    ),
    "Referrer-Policy": (
        "Referrer Protection",
        "Controls referrer information sent with requests."
    ),
    "Permissions-Policy": (
        "Browser Permissions",
        "Controls access to browser features."
    )
}


def analyze_headers(url, timeout):
    """Fetch a URL and analyze its HTTP response headers."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Python-HTTP-Header-Analyzer/1.0"},
        method="GET"
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout
    ) as response:

        return {
            "status_code": response.status,
            "final_url": response.url,
            "headers": dict(response.headers.items())
        }


def evaluate_security_headers(headers, is_https):
    """Identify present and missing security headers."""

    normalized = {
        key.lower(): value
        for key, value in headers.items()
    }

    results = []

    for header, details in SECURITY_HEADERS.items():
        name, description = details

        if header.lower() == "strict-transport-security" and not is_https:
            status = "NOT APPLICABLE"
        elif header.lower() in normalized:
            status = "PRESENT"
        else:
            status = "MISSING"

        results.append({
            "header": header,
            "name": name,
            "status": status,
            "description": description,
            "value": normalized.get(header.lower(), "Not configured")
        })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze HTTP response and security headers."
    )

    parser.add_argument(
        "url",
        help="Target URL, such as https://example.com"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="Request timeout in seconds"
    )

    parser.add_argument(
        "--output",
        default="http-header-report.json",
        help="JSON report filename"
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("Timeout must be greater than zero")

    url = args.url

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print("=" * 65)
    print("                 HTTP HEADER ANALYZER")
    print("=" * 65)

    try:
        result = analyze_headers(url, args.timeout)

        headers = result["headers"]
        is_https = result["final_url"].startswith("https://")

        security_results = evaluate_security_headers(
            headers,
            is_https
        )

        print(f"\nRequested URL : {url}")
        print(f"Final URL     : {result['final_url']}")
        print(f"HTTP Status   : {result['status_code']}")

        print("\nSECURITY HEADER ANALYSIS")
        print("-" * 65)

        for item in security_results:
            print(
                f"\n{item['name']} ({item['header']})"
            )
            print(f"Status      : {item['status']}")
            print(f"Description : {item['description']}")

            if item["status"] == "PRESENT":
                print(f"Value       : {item['value']}")

        present = sum(
            item["status"] == "PRESENT"
            for item in security_results
        )

        missing = sum(
            item["status"] == "MISSING"
            for item in security_results
        )

        report = {
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "url": url,
            "final_url": result["final_url"],
            "status_code": result["status_code"],
            "summary": {
                "present": present,
                "missing": missing
            },
            "security_headers": security_results,
            "all_response_headers": headers
        }

        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        print("\n" + "-" * 65)
        print("ANALYSIS SUMMARY")
        print(f"Present headers : {present}")
        print(f"Missing headers : {missing}")
        print(f"Report saved    : {args.output}")

    except urllib.error.HTTPError as error:
        print(f"HTTP Error: {error.code} - {error.reason}")

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Connection failed: {error}")


if __name__ == "__main__":
    main()
