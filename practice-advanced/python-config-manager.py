
#!/usr/bin/env python3
"""
Python Configuration Manager
-----------------------------
Loads configuration from a .env-style file and environment variables.

Environment variables take priority over file values.

Usage:
    python practice-advanced/python-config-manager.py
    python practice-advanced/python-config-manager.py .env
"""

import os
import sys
from pathlib import Path


class ConfigManager:
    def __init__(self, file_path=".env"):
        self.values = {}
        self.file_path = Path(file_path)
        self._load_file()

    def _load_file(self):
        """Load KEY=VALUE pairs from the configuration file."""
        if not self.file_path.is_file():
            return

        for line_number, raw_line in enumerate(
            self.file_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                print(
                    f"Warning: Ignoring invalid line {line_number}",
                    file=sys.stderr,
                )
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                print(
                    f"Warning: Empty key on line {line_number}",
                    file=sys.stderr,
                )
                continue

            # Remove matching surrounding quotes.
            if len(value) >= 2 and value[0] == value[-1]:
                if value[0] in {"'", '"'}:
                    value = value[1:-1]

            self.values[key] = value

    def get(self, key, default=None, cast=str, required=False):
        """Return a setting with optional type conversion."""
        value = os.environ.get(key, self.values.get(key))

        if value is None or value == "":
            if required:
                raise ValueError(
                    f"Required configuration '{key}' is missing."
                )
            return default

        try:
            if cast is bool:
                normalized = value.strip().lower()

                if normalized in {"true", "1", "yes", "on"}:
                    return True

                if normalized in {"false", "0", "no", "off"}:
                    return False

                raise ValueError("Expected a boolean value.")

            return cast(value)

        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid value for '{key}': {value!r}"
            ) from exc

    def get_all(self):
        """Return non-secret configuration keys and values."""
        return {
            key: self.get(key)
            for key in self.values
        }


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else ".env"
    config = ConfigManager(file_path)

    # Example application settings.
    app_name = config.get("APP_NAME", "DevOps Demo")
    port = config.get("APP_PORT", 8000, cast=int)
    debug = config.get("DEBUG", False, cast=bool)
    retries = config.get("MAX_RETRIES", 3, cast=int)
    api_url = config.get("API_URL", "http://localhost")

    print("Configuration Loaded")
    print("-" * 35)
    print(f"Application : {app_name}")
    print(f"Port        : {port}")
    print(f"Debug       : {debug}")
    print(f"Max retries : {retries}")
    print(f"API URL     : {api_url}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Configuration error: {exc}")
