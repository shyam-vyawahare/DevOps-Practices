
import argparse
import gzip
import logging
import shutil
from logging.handlers import RotatingFileHandler
from pathlib import Path


def compress_log(source, destination):
    """Compress a rotated log file using GZIP."""
    with open(source, "rb") as source_file:
        with gzip.open(destination, "wb") as compressed_file:
            shutil.copyfileobj(source_file, compressed_file)

    Path(source).unlink()


def setup_logger(log_file, max_bytes, backup_count, compress):
    """Configure a rotating application logger."""
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ApplicationLogger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )

    if compress:
        handler.namer = lambda name: name + ".gz"
        handler.rotator = compress_log

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def main():
    parser = argparse.ArgumentParser(
        description="Application log rotation and compression manager"
    )

    parser.add_argument(
        "--log-file",
        default="logs/application.log",
        help="Path to the application log file"
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=1024 * 1024,
        help="Maximum log size before rotation (default: 1 MB)"
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=5,
        help="Number of rotated log files to retain"
    )
    parser.add_argument(
        "--entries",
        type=int,
        default=20,
        help="Number of sample log entries to generate"
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Disable GZIP compression"
    )

    args = parser.parse_args()

    if args.max_bytes <= 0 or args.keep < 0 or args.entries < 0:
        parser.error("--max-bytes must be positive; --keep and --entries cannot be negative")

    logger = setup_logger(
        args.log_file,
        args.max_bytes,
        args.keep,
        not args.no_compress
    )

    levels = [
        logging.INFO,
        logging.WARNING,
        logging.ERROR
    ]

    for index in range(args.entries):
        level = levels[index % len(levels)]
        logger.log(
            level,
            "Sample application event #%d - Log rotation demonstration.",
            index + 1
        )

    # Close handlers before listing files.
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    print("\nLog rotation completed!")
    print(f"Log file: {args.log_file}")

    log_directory = Path(args.log_file).parent

    print("\nGenerated log files:")
    for file in sorted(log_directory.glob(Path(args.log_file).name + "*")):
        size = file.stat().st_size
        print(f"  {file.name:<35} {size:>8} bytes")


if __name__ == "__main__":
    main()
