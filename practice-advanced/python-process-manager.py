
#!/usr/bin/env python3
"""
Python System Process Manager
-----------------------------
Monitor running processes and system resource consumption.

Usage:
    python practice-advanced/python-process-manager.py
    python practice-advanced/python-process-manager.py --top 10
    python practice-advanced/python-process-manager.py --search chrome
    python practice-advanced/python-process-manager.py --output process-report.json
"""

import argparse
import json
from datetime import datetime, timezone

import psutil


def get_process_info(process):
    """Collect resource information for a process."""

    try:
        with process.oneshot():
            memory = process.memory_info()

            return {
                "pid": process.pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(interval=None),
                "memory_mb": round(memory.rss / (1024 ** 2), 2),
                "memory_percent": round(
                    process.memory_percent(), 2
                ),
                "username": process.username(),
            }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):
        return None


def collect_processes(search=None):
    """Collect information about running processes."""

    processes = []

    for process in psutil.process_iter():
        info = get_process_info(process)

        if info is None:
            continue

        if search and search.lower() not in info["name"].lower():
            continue

        processes.append(info)

    return processes


def display_system_summary():
    """Display overall CPU and memory statistics."""

    print("\nSYSTEM RESOURCE SUMMARY")
    print("-" * 65)

    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    print(f"CPU Usage       : {cpu_usage}%")
    print(f"RAM Usage       : {memory.percent}%")
    print(f"RAM Available   : {memory.available / (1024 ** 3):.2f} GB")
    print(f"Disk Usage      : {disk.percent}%")


def display_processes(processes, top):
    """Display the top resource-consuming processes."""

    processes.sort(
        key=lambda item: item["memory_mb"],
        reverse=True,
    )

    print("\nTOP PROCESSES BY MEMORY")
    print("-" * 90)

    print(
        f"{'PID':<10}"
        f"{'PROCESS':<25}"
        f"{'CPU %':<12}"
        f"{'MEMORY MB':<15}"
        f"{'STATUS':<15}"
    )

    print("-" * 90)

    for item in processes[:top]:
        print(
            f"{item['pid']:<10}"
            f"{item['name'][:23]:<25}"
            f"{item['cpu_percent']:<12}"
            f"{item['memory_mb']:<15}"
            f"{item['status']:<15}"
        )

    print(f"\nTotal matching processes: {len(processes)}")


def export_report(processes, output):
    """Export process statistics to JSON."""

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "memory_percent": psutil.virtual_memory().percent,
        },
        "process_count": len(processes),
        "processes": processes,
    }

    with open(output, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport exported: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor system processes and resource usage."
    )

    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of processes to display.",
    )

    parser.add_argument(
        "--search",
        help="Filter processes by name.",
    )

    parser.add_argument(
        "--output",
        help="Export process report to JSON.",
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1.")

    display_system_summary()

    processes = collect_processes(args.search)

    display_processes(processes, args.top)

    if args.output:
        export_report(processes, args.output)


if __name__ == "__main__":
    main()
