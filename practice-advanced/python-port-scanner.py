
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP Alternate",
    27017: "MongoDB"
}


def check_port(host, port, timeout):
    """Check whether a TCP port accepts connections."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                return port, True

    except (socket.timeout, socket.gaierror, OSError):
        pass

    return port, False


def scan_ports(host, ports, timeout, workers):
    """Scan the selected TCP ports."""
    open_ports = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(check_port, host, port, timeout): port
            for port in ports
        }

        for future in as_completed(futures):
            port, is_open = future.result()

            if is_open:
                open_ports.append(port)

    return sorted(open_ports)


def main():
    parser = argparse.ArgumentParser(
        description="Basic TCP port scanner for authorized network testing"
    )

    parser.add_argument("host", help="Target hostname or IP address")

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Starting port (default: 1)"
    )

    parser.add_argument(
        "--end",
        type=int,
        default=1024,
        help="Ending port (default: 1024)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Connection timeout in seconds"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Maximum concurrent workers"
    )

    args = parser.parse_args()

    if not (1 <= args.start <= args.end <= 65535):
        parser.error("Ports must satisfy: 1 <= start <= end <= 65535")

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    if not (1 <= args.workers <= 100):
        parser.error("--workers must be between 1 and 100")

    try:
        target_ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        parser.error(f"Unable to resolve hostname: {args.host}")

    ports = range(args.start, args.end + 1)

    print("=" * 55)
    print("             PYTHON TCP PORT SCANNER")
    print("=" * 55)
    print(f"Target       : {args.host}")
    print(f"Resolved IP  : {target_ip}")
    print(f"Port range   : {args.start}-{args.end}")
    print(f"Started at   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)

    start_time = datetime.now()

    open_ports = scan_ports(
        target_ip,
        ports,
        args.timeout,
        args.workers
    )

    print("\nOPEN PORTS")
    print("-" * 55)

    if open_ports:
        for port in open_ports:
            service = COMMON_PORTS.get(port, "Unknown")
            print(f"Port {port:<6} | {service}")
    else:
        print("No open TCP ports found in the selected range.")

    elapsed = (datetime.now() - start_time).total_seconds()

    print("-" * 55)
    print(f"Total ports scanned : {len(ports)}")
    print(f"Open ports found    : {len(open_ports)}")
    print(f"Time taken          : {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
