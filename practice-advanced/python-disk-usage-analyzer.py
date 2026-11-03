
#!/usr/bin/env python3
"""
Python Disk Usage Analyzer
--------------------------
Analyze directory storage and identify large files.

Usage:
    python practice-advanced/python-disk-usage-analyzer.py .
    python practice-advanced/python-disk-usage-analyzer.py ./project --top 10
    python practice-advanced/python-disk-usage-analyzer.py . --output disk-report.json
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def format_size(size_bytes):
    """Convert bytes into a human-readable storage format."""

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"
        size /= 1024


def analyze_directory(root):
    """Scan files and collect storage statistics."""

    root = root.resolve()

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    total_size = 0
    file_count = 0
    directory_sizes = defaultdict(int)
    largest_files = []
    errors = []

    for current_dir, dirs, files in __import__("os").walk(root):
        # Avoid traversing symbolic-link directories.
        dirs[:] = [
            name for name in dirs
            if not (Path(current_dir) / name).is_symlink()
        ]

        for filename in files:
            file_path = Path(current_dir) / filename

            try:
                if file_path.is_symlink():
                    continue

                size = file_path.stat().st_size
                total_size += size
                file_count += 1

                relative_path = file_path.relative_to(root)
                parent = relative_path.parent

                directory_key = (
                    str(parent) if str(parent) != "." else "."
                )

                directory_sizes[directory_key] += size

                largest_files.append({
                    "path": str(relative_path),
                    "size_bytes": size,
                    "size": format_size(size),
                })

            except OSError as error:
                errors.append({
                    "path": str(file_path),
                    "error": str(error),
                })

    largest_files.sort(
        key=lambda item: item["size_bytes"],
        reverse=True,
    )

    return {
        "root": str(root),
        "total_size_bytes": total_size,
        "total_size": format_size(total_size),
        "file_count": file_count,
        "directory_sizes": [
            {
                "directory": directory,
                "size_bytes": size,
                "size": format_size(size),
            }
            for directory, size in sorted(
                directory_sizes.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
        "largest_files": largest_files,
        "scan_errors": errors,
    }


def display_report(report, top):
    """Print the storage analysis report."""

    print("\n" + "=" * 60)
    print("DISK USAGE ANALYSIS REPORT")
    print("=" * 60)

    print(f"Directory: {report['root']}")
    print(f"Total Files: {report['file_count']}")
    print(f"Total Storage: {report['total_size']}")

    print("\nDIRECTORY STORAGE USAGE")
    print("-" * 60)

    for item in report["directory_sizes"][:top]:
        print(f"{item['directory']:<40} {item['size']:>12}")

    print("\nLARGEST FILES")
    print("-" * 60)

    for item in report["largest_files"][:top]:
        print(f"{item['size']:<12} {item['path']}")

    print("\nSCAN SUMMARY")
    print("-" * 60)
    print(f"Files scanned: {report['file_count']}")
    print(f"Scan errors: {len(report['scan_errors'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze directory storage consumption."
    )

    parser.add_argument(
        "directory",
        help="Directory to analyze.",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of entries to display (default: 10).",
    )

    parser.add_argument(
        "--output",
        help="Optional JSON report output path.",
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1.")

    try:
        report = analyze_directory(Path(args.directory))
        display_report(report, args.top)

        if args.output:
            output_path = Path(args.output)

            output_path.write_text(
                json.dumps(report, indent=4),
                encoding="utf-8",
            )

            print(f"\nJSON report saved: {output_path}")

        return 1 if report["scan_errors"] else 0

    except (OSError, ValueError) as error:
        print(f"\n[ERROR] {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
