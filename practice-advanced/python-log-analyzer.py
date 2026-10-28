
#!/usr/bin/env python3
"""
Application Log Analyzer
------------------------
Analyze application logs, count log levels, and identify frequent errors.

Usage:
    python practice-advanced/python-log-analyzer.py
    python practice-advanced/python-log-analyzer.py app.log
    python practice-advanced/python-log-analyzer.py app.log --top 5
"""

import argparse
import re
from collections import Counter
from pathlib import Path


SAMPLE_LOGS = """\
2026-10-28 09:00:01 INFO Application started
2026-10-28 09:00:05 INFO Database connected
2026-10-28 09:01:12 WARNING High memory usage detected
2026-10-28 09:01:20 ERROR Database connection failed
2026-10-28 09:01:25 ERROR Database connection failed
2026-10-28 09:02:10 INFO Request processed successfully
2026-10-28 09:02:30 CRITICAL Service unavailable
2026-10-28 09:03:00 WARNING High memory usage detected
2026-10-28 09:03:15 ERROR API request timed out
2026-10-28 09:04:00 DEBUG Health check completed
"""

LOG_LEVELS = {
    "DEBUG", "INFO", "WARNING", "WARN",
    "ERROR", "CRITICAL", "FATAL"
}

LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\b",
    re.IGNORECASE
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze application log files."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the log file. Uses sample logs if omitted."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of frequent errors to display (default: 5)."
    )
    return parser.parse_args()


def load_logs(file_path=None):
    if file_path is None:
        print("Using built-in sample logs.\n")
        return SAMPLE_LOGS.splitlines()

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {path}")

    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def analyze_logs(lines):
    level_counts = Counter()
    error_messages = Counter()
    unmatched_lines = 0

    for line in lines:
        match = LEVEL_PATTERN.search(line)

        if not match:
            unmatched_lines += 1
            continue

        level = match.group(1).upper()

        if level == "WARN":
            level = "WARNING"
        elif level == "FATAL":
            level = "CRITICAL"

        level_counts[level] += 1

        if level in {"ERROR", "CRITICAL"}:
            # Remove timestamp and log level to group repeated errors.
            message = line[match.end():].strip()
            error_messages[message or "(empty error message)"] += 1

    return level_counts, error_messages, unmatched_lines


def print_report(lines, level_counts, error_messages, unmatched, top):
    print("=" * 55)
    print("APPLICATION LOG ANALYSIS REPORT")
    print("=" * 55)
    print(f"Total lines:       {len(lines)}")
    print(f"Parsed log entries: {sum(level_counts.values())}")
    print(f"Unmatched lines:   {unmatched}")

    print("\nLog Level Summary")
    print("-" * 30)

    if level_counts:
        for level, count in level_counts.most_common():
            print(f"{level:<12} {count:>5}")
    else:
        print("No recognized log levels found.")

    print("\nMost Frequent Errors")
    print("-" * 30)

    if error_messages:
        for message, count in error_messages.most_common(max(0, top)):
            print(f"[{count} occurrence(s)] {message}")
    else:
        print("No ERROR or CRITICAL entries found.")

    print("\nAnalysis complete.")


def main():
    args = parse_arguments()

    if args.top < 0:
        raise SystemExit("--top must be zero or greater.")

    try:
        lines = load_logs(args.file)
        levels, errors, unmatched = analyze_logs(lines)
        print_report(lines, levels, errors, unmatched, args.top)
    except (OSError, UnicodeError) as exc:
        raise SystemExit(f"Error reading log file: {exc}")


if __name__ == "__main__":
    main()
