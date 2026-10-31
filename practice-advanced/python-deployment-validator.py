
#!/usr/bin/env python3
"""
Python Deployment Configuration Validator
-----------------------------------------
Validates deployment prerequisites before application release.

Checks:
- Required environment variables
- Required configuration files
- Port validity
- Environment configuration
- Secret configuration

Usage:
    python practice-advanced/python-deployment-validator.py
    python practice-advanced/python-deployment-validator.py --strict
"""

import argparse
import os
from pathlib import Path


REQUIRED_ENV_VARS = [
    "APP_NAME",
    "APP_PORT",
    "APP_ENV",
]

REQUIRED_FILES = [
    "requirements.txt",
]

VALID_ENVIRONMENTS = {"development", "testing", "staging", "production"}


class DeploymentValidator:
    def __init__(self, strict=False):
        self.strict = strict
        self.errors = []
        self.warnings = []

    def check_environment_variables(self):
        print("\n[1] Environment Variable Validation")

        for variable in REQUIRED_ENV_VARS:
            value = os.getenv(variable)

            if not value:
                self.errors.append(
                    f"Missing required variable: {variable}"
                )
                print(f"[FAIL] {variable} is missing")
            else:
                print(f"[PASS] {variable} is configured")

        # Validate application port.
        port = os.getenv("APP_PORT")

        if port:
            try:
                port_number = int(port)

                if not 1 <= port_number <= 65535:
                    raise ValueError

                print(f"[PASS] APP_PORT is valid: {port_number}")

            except ValueError:
                self.errors.append("APP_PORT must be between 1 and 65535.")
                print("[FAIL] APP_PORT is invalid")

        # Validate deployment environment.
        environment = os.getenv("APP_ENV")

        if environment:
            if environment.lower() not in VALID_ENVIRONMENTS:
                self.errors.append(
                    f"Invalid APP_ENV: {environment}"
                )
                print(f"[FAIL] Unsupported environment: {environment}")
            else:
                print(f"[PASS] Environment: {environment}")

    def check_required_files(self):
        print("\n[2] Required File Validation")

        for filename in REQUIRED_FILES:
            if Path(filename).is_file():
                print(f"[PASS] {filename} exists")
            else:
                self.errors.append(
                    f"Required file not found: {filename}"
                )
                print(f"[FAIL] {filename} is missing")

    def check_optional_files(self):
        print("\n[3] Optional File Validation")

        optional_files = [".env", "Dockerfile", "docker-compose.yml"]

        for filename in optional_files:
            if Path(filename).exists():
                print(f"[PASS] {filename} found")
            else:
                self.warnings.append(
                    f"Optional file not found: {filename}"
                )
                print(f"[WARNING] {filename} not found")

    def check_secret_configuration(self):
        print("\n[4] Secret Configuration Validation")

        secret_names = ["SECRET_KEY", "DATABASE_URL"]

        for name in secret_names:
            if not os.getenv(name):
                message = f"Secret/configuration variable {name} is missing."

                if self.strict:
                    self.errors.append(message)
                    print(f"[FAIL] {name} is missing")
                else:
                    self.warnings.append(message)
                    print(f"[WARNING] {name} is missing")
            else:
                print(f"[PASS] {name} is configured")

    def run(self):
        print("=" * 55)
        print("DEPLOYMENT VALIDATION REPORT")
        print("=" * 55)

        self.check_environment_variables()
        self.check_required_files()
        self.check_optional_files()
        self.check_secret_configuration()

        print("\n" + "=" * 55)
        print("FINAL SUMMARY")
        print("=" * 55)

        print(f"Errors   : {len(self.errors)}")
        print(f"Warnings : {len(self.warnings)}")

        if self.errors:
            print("\nDeployment validation FAILED.")
            return 1

        print("\nDeployment validation PASSED.")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate application deployment prerequisites."
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing secrets as errors.",
    )

    args = parser.parse_args()

    validator = DeploymentValidator(strict=args.strict)

    return validator.run()


if __name__ == "__main__":
    raise SystemExit(main())
