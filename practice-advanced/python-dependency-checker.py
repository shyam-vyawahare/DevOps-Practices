
import argparse
import json
import subprocess
import sys
from datetime import datetime


def get_installed_packages():
    """Retrieve installed Python packages."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True
    )

    return json.loads(result.stdout)


def get_outdated_packages():
    """Identify packages with newer available versions."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "list",
            "--outdated",
            "--format=json"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Unable to check outdated packages")

    return json.loads(result.stdout)


def generate_report(installed, outdated):
    """Build a dependency audit report."""
    outdated_names = {
        package["name"].lower()
        for package in outdated
    }

    report = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "python_version": sys.version.split()[0],
        "summary": {
            "total_installed": len(installed),
            "outdated_count": len(outdated),
            "up_to_date_count": len(installed) - len(outdated)
        },
        "packages": []
    }

    for package in installed:
        report["packages"].append({
            "name": package["name"],
            "version": package["version"],
            "status": (
                "outdated"
                if package["name"].lower() in outdated_names
                else "up-to-date"
            )
        })

    report["outdated_packages"] = outdated

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Python dependency audit tool"
    )

    parser.add_argument(
        "--output",
        default="dependency-report.json",
        help="Output JSON report filename"
    )

    args = parser.parse_args()

    try:
        print("Scanning installed Python packages...")

        installed = get_installed_packages()

        print("Checking for available updates...")

        outdated = get_outdated_packages()

        report = generate_report(installed, outdated)

        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        print("\nDependency audit completed!")
        print("-" * 45)
        print(f"Installed packages : {report['summary']['total_installed']}")
        print(f"Outdated packages  : {report['summary']['outdated_count']}")
        print(f"Up-to-date         : {report['summary']['up_to_date_count']}")
        print(f"\nReport saved to: {args.output}")

        if outdated:
            print("\nPackages requiring attention:")

            for package in outdated:
                print(
                    f"{package['name']}: "
                    f"{package['version']} -> {package['latest_version']}"
                )
        else:
            print("\nAll installed packages are up to date.")

    except (subprocess.CalledProcessError, RuntimeError, json.JSONDecodeError) as error:
        print(f"Dependency check failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
