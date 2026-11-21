
import argparse
import socket
import ssl
from datetime import datetime, timezone


def check_certificate(host, port, timeout):
    """Retrieve and validate an SSL/TLS certificate."""

    context = ssl.create_default_context()

    with socket.create_connection(
        (host, port),
        timeout=timeout
    ) as connection:

        with context.wrap_socket(
            connection,
            server_hostname=host
        ) as secure_socket:

            certificate = secure_socket.getpeercert()

    return certificate


def get_certificate_date(date_string):
    """Convert certificate date into a datetime object."""

    return datetime.strptime(
        date_string,
        "%b %d %H:%M:%S %Y %Z"
    ).replace(tzinfo=timezone.utc)


def extract_name(certificate_name):
    """Convert certificate subject/issuer into readable text."""

    values = []

    for group in certificate_name:
        for key, value in group:
            values.append(f"{key}={value}")

    return ", ".join(values)


def main():
    parser = argparse.ArgumentParser(
        description="SSL/TLS certificate expiration checker"
    )

    parser.add_argument(
        "host",
        help="Domain name to inspect"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=443,
        help="HTTPS port (default: 443)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Connection timeout in seconds"
    )

    args = parser.parse_args()

    if not (1 <= args.port <= 65535):
        parser.error("Port must be between 1 and 65535")

    if args.timeout <= 0:
        parser.error("Timeout must be greater than zero")

    print("=" * 55)
    print("          SSL/TLS CERTIFICATE CHECKER")
    print("=" * 55)

    print(f"Domain : {args.host}")
    print(f"Port   : {args.port}")

    try:
        certificate = check_certificate(
            args.host,
            args.port,
            args.timeout
        )

        expiry_date = get_certificate_date(
            certificate["notAfter"]
        )

        current_time = datetime.now(timezone.utc)
        remaining = expiry_date - current_time
        days_remaining = remaining.days

        subject = extract_name(certificate["subject"])
        issuer = extract_name(certificate["issuer"])

        print("\nCERTIFICATE DETAILS")
        print("-" * 55)

        print(f"Subject       : {subject}")
        print(f"Issuer        : {issuer}")
        print(f"Valid From    : {certificate['notBefore']}")
        print(f"Expires On    : {certificate['notAfter']}")
        print(f"Days Remaining: {days_remaining}")

        print("\nCERTIFICATE STATUS")
        print("-" * 55)

        if remaining.total_seconds() <= 0:
            print("EXPIRED: Certificate validity period has ended.")

        elif days_remaining <= 30:
            print("WARNING: Certificate expires within 30 days.")

        else:
            print("VALID: Certificate is not close to expiration.")

    except ssl.SSLCertVerificationError as error:
        print(f"\nCERTIFICATE VALIDATION FAILED: {error}")

    except (socket.timeout, socket.gaierror, OSError) as error:
        print(f"\nCONNECTION FAILED: {error}")

    except (KeyError, ValueError) as error:
        print(f"\nCERTIFICATE DATA ERROR: {error}")


if __name__ == "__main__":
    main()
