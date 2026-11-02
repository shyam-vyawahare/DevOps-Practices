
#!/usr/bin/env python3
"""
Python Automated Backup Manager
--------------------------------
Create, verify, and manage timestamped ZIP backups.

Usage:
    python practice-advanced/python-backup-manager.py ./project ./backups
    python practice-advanced/python-backup-manager.py ./project ./backups --keep 5
    python practice-advanced/python-backup-manager.py ./important.txt ./backups
"""

import argparse
import zipfile
from datetime import datetime
from pathlib import Path


def create_backup(source, destination):
    """Create a timestamped ZIP backup."""

    source = source.resolve()
    destination = destination.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source does not exist: {source}")

    # Prevent recursively backing up the destination.
    if source == destination or source in destination.parents:
        raise ValueError(
            "Backup destination cannot be inside the source directory."
        )

    if source.is_dir() and destination in source.parents:
        raise ValueError(
            "Backup destination cannot contain the source directory."
        )

    destination.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = destination / f"backup_{timestamp}.zip"

    print(f"Creating backup: {archive_path.name}")

    with zipfile.ZipFile(
        archive_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        if source.is_file():
            archive.write(source, arcname=source.name)

        else:
            for item in source.rglob("*"):
                if item.is_file():
                    archive.write(
                        item,
                        arcname=item.relative_to(source.parent),
                    )

    print("[SUCCESS] Backup created.")
    return archive_path


def verify_backup(archive_path):
    """Verify that the ZIP archive is readable and uncorrupted."""

    print("\nVerifying backup...")

    with zipfile.ZipFile(archive_path, "r") as archive:
        bad_file = archive.testzip()

        if bad_file:
            print(f"[FAILED] Corrupted file: {bad_file}")
            return False

    print("[SUCCESS] Backup integrity verified.")
    return True


def apply_retention(destination, keep):
    """Keep only the most recent specified number of backups."""

    backups = sorted(
        destination.glob("backup_*.zip"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    print("\nApplying retention policy...")

    for old_backup in backups[keep:]:
        old_backup.unlink()
        print(f"[DELETED] {old_backup.name}")

    print(f"Retained backups: {min(len(backups), keep)}")


def display_backup_info(archive_path):
    """Display backup file information."""

    size_kb = archive_path.stat().st_size / 1024

    print("\nBackup Information")
    print("-" * 35)
    print(f"File: {archive_path.name}")
    print(f"Location: {archive_path}")
    print(f"Size: {size_kb:.2f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Automated ZIP backup manager."
    )

    parser.add_argument(
        "source",
        help="File or directory to back up.",
    )

    parser.add_argument(
        "destination",
        help="Directory where backups will be stored.",
    )

    parser.add_argument(
        "--keep",
        type=int,
        default=5,
        help="Number of recent backups to retain (default: 5).",
    )

    args = parser.parse_args()

    if args.keep < 1:
        parser.error("--keep must be at least 1.")

    try:
        source = Path(args.source)
        destination = Path(args.destination)

        backup = create_backup(source, destination)

        if not verify_backup(backup):
            backup.unlink(missing_ok=True)
            raise RuntimeError("Backup verification failed.")

        apply_retention(destination.resolve(), args.keep)
        display_backup_info(backup)

        print("\nBackup operation completed successfully.")

    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"\n[ERROR] {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
