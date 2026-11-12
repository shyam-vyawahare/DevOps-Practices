
#!/usr/bin/env python3
"""
Python Network Monitor
----------------------
Monitor network interfaces, bandwidth, and active connections.

Usage:
    python practice-advanced/python-network-monitor.py
    python practice-advanced/python-network-monitor.py --interval 5
    python practice-advanced/python-network-monitor.py --connections
    python practice-advanced/python-network-monitor.py --output network-report.json
"""

import argparse
import json
import time
from datetime import datetime, timezone

import psutil


def format_bytes(value):
    """Convert bytes into a readable format."""

    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if value < 1024 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024


def get_network_interfaces():
    """Collect network interface information."""

    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    print("\nNETWORK INTERFACES")
    print("-" * 65)

    for name, addresses in interfaces.items():
        status = stats.get(name)

        print(f"\nInterface: {name}")
        print(f"Status: {'UP' if status and status.isup else 'DOWN'}")

        for address in addresses:
            if address.family == psutil.AF_LINK:
                print(f"MAC Address: {address.address}")
            elif address.family.name == "AF_INET":
                print(f"IPv4 Address: {address.address}")
            elif address.family.name == "AF_INET6":
                print(f"IPv6 Address: {address.address}")


def get_bandwidth(interval):
    """Measure network upload and download speed."""

    before = psutil.net_io_counters()

    print(f"\nMeasuring bandwidth for {interval} seconds...")
    time.sleep(interval)

    after = psutil.net_io_counters()

    sent = after.bytes_sent - before.bytes_sent
    received = after.bytes_recv - before.bytes_recv

    upload_speed = sent / interval
    download_speed = received / interval

    return {
        "sent_bytes": sent,
        "received_bytes": received,
        "upload_speed_bytes_sec": round(upload_speed, 2),
        "download_speed_bytes_sec": round(download_speed, 2),
        "upload_speed": f"{format_bytes(upload_speed)}/s",
        "download_speed": f"{format_bytes(download_speed)}/s",
    }


def get_network_totals():
    """Get cumulative network transfer statistics."""

    counters = psutil.net_io_counters()

    return {
        "total_sent": counters.bytes_sent,
        "total_received": counters.bytes_recv,
        "packets_sent": counters.packets_sent,
        "packets_received": counters.packets_recv,
        "errors_in": counters.errin,
        "errors_out": counters.errout,
        "dropped_in": counters.dropin,
        "dropped_out": counters.dropout,
    }


def get_active_connections():
    """Collect active network connections where permissions allow."""

    connections = []

    try:
        for connection in psutil.net_connections(kind="inet"):
            connections.append({
                "protocol": (
                    "TCP" if connection.type == 1 else "UDP"
                ),
                "local_address": (
                    f"{connection.laddr.ip}:{connection.laddr.port}"
                    if connection.laddr else None
                ),
                "remote_address": (
                    f"{connection.raddr.ip}:{connection.raddr.port}"
                    if connection.raddr else None
                ),
                "status": connection.status,
                "pid": connection.pid,
            })

    except psutil.AccessDenied:
        print("\n[WARNING] Permission denied while reading connections.")

    return connections


def display_report(bandwidth, totals, connections):
    """Display network monitoring results."""

    print("\n" + "=" * 65)
    print("NETWORK MONITORING REPORT")
    print("=" * 65)

    print("\nBANDWIDTH USAGE")
    print("-" * 40)
    print(f"Upload Speed   : {bandwidth['upload_speed']}")
    print(f"Download Speed : {bandwidth['download_speed']}")
    print(f"Data Sent      : {format_bytes(bandwidth['sent_bytes'])}")
    print(f"Data Received  : {format_bytes(bandwidth['received_bytes'])}")

    print("\nCUMULATIVE NETWORK STATISTICS")
    print("-" * 40)
    print(f"Total Sent     : {format_bytes(totals['total_sent'])}")
    print(f"Total Received : {format_bytes(totals['total_received'])}")
    print(f"Packets Sent   : {totals['packets_sent']}")
    print(f"Packets Received: {totals['packets_received']}")
    print(f"Incoming Errors: {totals['errors_in']}")
    print(f"Outgoing Errors: {totals['errors_out']}")

    print(f"\nActive Connections: {len(connections)}")

    for connection in connections[:10]:
        print(
            f"{connection['protocol']:<5} "
            f"{connection['local_address']} -> "
            f"{connection['remote_address']} "
            f"[{connection['status']}]"
        )


def export_report(bandwidth, totals, connections, output):
    """Export monitoring information to JSON."""

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bandwidth": bandwidth,
        "network_totals": totals,
        "active_connections": connections,
    }

    with open(output, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor network bandwidth and connections."
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=3,
        help="Bandwidth measurement interval in seconds.",
    )

    parser.add_argument(
        "--connections",
        action="store_true",
        help="Display active network connections.",
    )

    parser.add_argument(
        "--output",
        help="Export monitoring report to JSON.",
    )

    args = parser.parse_args()

    if args.interval <= 0:
        parser.error("--interval must be greater than zero.")

    get_network_interfaces()

    bandwidth = get_bandwidth(args.interval)
    totals = get_network_totals()

    connections = (
        get_active_connections()
        if args.connections or args.output
        else []
    )

    display_report(bandwidth, totals, connections)

    if args.output:
        export_report(
            bandwidth,
            totals,
            connections,
            args.output,
        )


if __name__ == "__main__":
    main()
