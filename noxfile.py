import json
from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv"


@nox.session(python=["3.11"])
def test(session):
    session.install("-e .[dev]")
    session.run(
        "pytest",
        "--disable-warnings",
        "--junitxml=junit.xml",
        "--cov=starbridge",
        "--cov-report=term-missing",
        "--cov-report=html:coverage_html",
        "--cov-report=xml:coverage.xml",
    )


@nox.session(python=["3.11"])
def lint(session):
    session.install("-e .[dev]")
    session.run("ruff", "check", ".")
    session.run(
        "ruff",
        "format",
        "--check",
        ".",
    )


@nox.session(python=["3.11"])
def audit(session):
    session.install("-e .[dev]")
    session.run("pip-audit", "-f", "json", "-o", "vulnerabilities.json")
    session.run("jq", ".", "vulnerabilities.json", external=True)
    session.run("pip-licenses", "--format=json", "--output-file=licenses.json")
    session.run("jq", ".", "licenses.json", external=True)
    # Read and parse licenses.json
    licenses_data = json.loads(Path("licenses.json").read_text(encoding="utf-8"))

    # Create inverted structure
    licenses_inverted = {}
    for pkg in licenses_data:
        license_name = pkg["License"]
        package_info = {"Name": pkg["Name"], "Version": pkg["Version"]}

        if license_name not in licenses_inverted:
            licenses_inverted[license_name] = []
        licenses_inverted[license_name].append(package_info)

    # Write inverted data
    Path("licenses-inverted.json").write_text(
        json.dumps(licenses_inverted, indent=2), encoding="utf-8"
    )
    session.run("jq", ".", "licenses-inverted.json", external=True)
    session.run("cyclonedx-py", "environment", "-o", "sbom.json")
    session.run("jq", ".", "sbom.json", external=True)
