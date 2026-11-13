
#!/usr/bin/env python3
"""
Python Alert Manager
--------------------
Monitor system resource thresholds and generate alerts.

Features:
- Severity-based alerts
- CPU and memory threshold monitoring
- File-based logging
- Optional email notifications
- JSON alert records

Usage:
    python practice-advanced/python-alert-manager.py
    python practice-advanced/python-alert-manager.py --cpu 80 --memory 85
    python practice-advanced/python-alert-manager.py --cpu 90 --memory 95 --email
"""

import argparse
import json
import logging
import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path


LOG_FILE = Path("logs/alerts.log")
JSON_FILE = Path("logs/alerts.json")


class AlertManager:

    SEVERITIES = {
        "INFO": 10,
        "WARNING": 20,
        "ERROR": 30,
        "CRITICAL": 40,
    }

    def __init__(self):
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            force=True,
        )

        self.alerts = []

    def trigger(self, severity, title, message):
        """Create, log, and store an alert."""

        if severity not in self.SEVERITIES:
            raise ValueError(f"Invalid severity: {severity}")

        alert = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": severity,
            "title": title,
            "message": message,
        }

        self.alerts.append(alert)

        log_method = {
            "INFO": logging.info,
            "WARNING": logging.warning,
            "ERROR": logging.error,
            "CRITICAL": logging.critical,
        }

        log_method[severity](f"{title}: {message}")

        print(f"[{severity}] {title}")
        print(f"  {message}\n")

        return alert

    def save_json(self):
        """Persist generated alerts in JSON format."""

        existing = []

        if JSON_FILE.exists():
            try:
                existing = json.loads(
                    JSON_FILE.read_text(encoding="utf-8")
                )

                if not isinstance(existing, list):
                    existing = []

            except (json.JSONDecodeError, OSError):
                existing = []

        existing.extend(self.alerts)

        JSON_FILE.write_text(
            json.dumps(existing, indent=4),
            encoding="utf-8",
        )

        print(f"Alert report saved: {JSON_FILE}")

    def send_email(self, alert):
        """Send an alert using SMTP environment configuration."""

        host = os.getenv("SMTP_HOST")
        port = os.getenv("SMTP_PORT", "587")
        sender = os.getenv("ALERT_EMAIL_FROM")
        recipient = os.getenv("ALERT_EMAIL_TO")
        username = os.getenv("SMTP_USERNAME")
        password = os.getenv("SMTP_PASSWORD")

        required = [host, sender, recipient, username, password]

        if not all(required):
            print("[EMAIL SKIPPED] SMTP configuration is incomplete.")
            return False

        try:
            message = EmailMessage()
            message["Subject"] = (
                f"[{alert['severity']}] {alert['title']}"
            )
            message["From"] = sender
            message["To"] = recipient

            message.set_content(
                f"Severity: {alert['severity']}\n"
                f"Title: {alert['title']}\n"
                f"Message: {alert['message']}\n"
                f"Timestamp: {alert['timestamp']}"
            )

            with smtplib.SMTP(host, int(port), timeout=10) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(message)

            print("[EMAIL SENT] Notification delivered.")
            return True

        except (OSError, ValueError, smtplib.SMTPException) as error:
            print(f"[EMAIL FAILED] {error}")
            return False


def monitor_resources(manager, cpu_threshold, memory_threshold, email):
    """Check system CPU and memory usage."""

    try:
        import psutil
    except ImportError:
        raise SystemExit(
            "Install psutil first: pip install psutil"
        )

    print("\nSYSTEM RESOURCE MONITORING")
    print("-" * 40)

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%\n")

    checks = [
        (
            "CPU Usage",
            cpu_usage,
            cpu_threshold,
        ),
        (
            "Memory Usage",
            memory_usage,
            memory_threshold,
        ),
    ]

    for name, usage, threshold in checks:

        if usage >= threshold:
            alert = manager.trigger(
                "CRITICAL",
                f"{name} Threshold Exceeded",
                f"Current usage: {usage}% | "
                f"Configured threshold: {threshold}%",
            )

            if email:
                manager.send_email(alert)

        elif usage >= threshold * 0.8:
            manager.trigger(
                "WARNING",
                f"{name} Approaching Threshold",
                f"Current usage: {usage}% | "
                f"Configured threshold: {threshold}%",
            )

        else:
            manager.trigger(
                "INFO",
                f"{name} Normal",
                f"Current usage: {usage}%",
            )


def main():
    parser = argparse.ArgumentParser(
        description="Python system resource alert manager."
    )

    parser.add_argument(
        "--cpu",
        type=float,
        default=80,
        help="CPU usage alert threshold (default: 80).",
    )

    parser.add_argument(
        "--memory",
        type=float,
        default=85,
        help="Memory usage alert threshold (default: 85).",
    )

    parser.add_argument(
        "--email",
        action="store_true",
        help="Enable email notifications for critical alerts.",
    )

    args = parser.parse_args()

    if not (
        0 < args.cpu <= 100
        and 0 < args.memory <= 100
    ):
        parser.error("Thresholds must be greater than 0 and at most 100.")

    manager = AlertManager()

    monitor_resources(
        manager,
        args.cpu,
        args.memory,
        args.email,
    )

    manager.save_json()

    print("\nAlert monitoring completed.")


if __name__ == "__main__":
    main()
