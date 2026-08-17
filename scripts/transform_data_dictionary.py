#!/usr/bin/env python3
"""
transform_data_dictionary.py

Utilities for versioning and transforming CSV data dictionary files in the data/ folder.

Usage:
    python scripts/transform_data_dictionary.py --help
    python scripts/transform_data_dictionary.py bump --file patient_data_dictionary.csv --part minor
    python scripts/transform_data_dictionary.py add-field --file patient_data_dictionary.csv \
        --field new_field --type string --description "A new field" --required false
    python scripts/transform_data_dictionary.py validate --file patient_data_dictionary.csv
    python scripts/transform_data_dictionary.py changelog
"""

import argparse
import csv
import json
import os
import sys
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
VERSIONS_FILE = DATA_DIR / "versions.json"
REQUIRED_COLUMNS = {"field_name", "data_type", "description", "required", "version", "last_updated"}

TODAY = date.today().isoformat()


def load_versions() -> dict:
    """Load the versions.json tracking file."""
    if VERSIONS_FILE.exists():
        with open(VERSIONS_FILE) as f:
            return json.load(f)
    return {"version": "1.0.0", "last_updated": TODAY, "files": {}}


def save_versions(versions: dict) -> None:
    """Persist versions.json."""
    versions["last_updated"] = TODAY
    with open(VERSIONS_FILE, "w") as f:
        json.dump(versions, f, indent=2)
        f.write("\n")


def bump_version(version_str: str, part: str) -> str:
    """Increment a semver version string by the given part (major/minor/patch)."""
    major, minor, patch = (int(x) for x in version_str.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Unknown version part: {part}. Use major, minor, or patch.")


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resolve_file(filename: str) -> Path:
    path = DATA_DIR / filename
    if not path.exists():
        print(f"Error: {path} does not exist.", file=sys.stderr)
        sys.exit(1)
    return path


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_bump(args) -> None:
    """Bump the version of every row in a data dictionary CSV."""
    path = resolve_file(args.file)
    rows = read_csv(path)
    if not rows:
        print("No rows found.", file=sys.stderr)
        sys.exit(1)

    old_version = rows[0].get("version", "1.0.0")
    new_version = bump_version(old_version, args.part)

    for row in rows:
        row["version"] = new_version
        row["last_updated"] = TODAY

    write_csv(path, rows, list(rows[0].keys()))

    versions = load_versions()
    versions["files"][args.file] = new_version
    save_versions(versions)

    print(f"Bumped {args.file}: {old_version} -> {new_version}")


def cmd_add_field(args) -> None:
    """Append a new field row to a data dictionary CSV."""
    path = resolve_file(args.file)
    rows = read_csv(path)

    # Ensure field doesn't already exist
    if any(r["field_name"] == args.field for r in rows):
        print(f"Error: field '{args.field}' already exists in {args.file}.", file=sys.stderr)
        sys.exit(1)

    current_version = rows[0].get("version", "1.0.0") if rows else "1.0.0"
    new_version = bump_version(current_version, "patch")

    fieldnames = list(rows[0].keys()) if rows else list(REQUIRED_COLUMNS)

    new_row = {k: "" for k in fieldnames}
    new_row["field_name"] = args.field
    new_row["data_type"] = args.type
    new_row["description"] = args.description
    new_row["allowed_values"] = args.allowed_values or ""
    new_row["required"] = args.required
    new_row["version"] = new_version
    new_row["last_updated"] = TODAY

    # Also bump existing rows to the new version
    for row in rows:
        row["version"] = new_version
        row["last_updated"] = TODAY

    rows.append(new_row)
    write_csv(path, rows, fieldnames)

    versions = load_versions()
    versions["files"][args.file] = new_version
    save_versions(versions)

    print(f"Added field '{args.field}' to {args.file} (version {new_version})")


def cmd_validate(args) -> None:
    """Validate that a CSV data dictionary has the required columns."""
    path = resolve_file(args.file)
    rows = read_csv(path)

    if not rows:
        print(f"Warning: {args.file} is empty.")
        return

    columns = set(rows[0].keys())
    missing = REQUIRED_COLUMNS - columns
    if missing:
        print(f"Validation FAILED for {args.file}. Missing columns: {missing}", file=sys.stderr)
        sys.exit(1)

    # Check no blank field_name
    blank = [i + 2 for i, r in enumerate(rows) if not r.get("field_name", "").strip()]
    if blank:
        print(f"Validation FAILED: blank field_name on rows {blank}", file=sys.stderr)
        sys.exit(1)

    print(f"Validation PASSED for {args.file} ({len(rows)} fields, version {rows[0].get('version')})")


def cmd_changelog(args) -> None:
    """Print a summary of current versions for all tracked CSV files."""
    versions = load_versions()
    print(f"Data Dictionary Changelog (last updated: {versions.get('last_updated', 'unknown')})")
    print("-" * 60)
    for filename, ver in versions.get("files", {}).items():
        path = DATA_DIR / filename
        rows = read_csv(path) if path.exists() else []
        print(f"  {filename:<45} v{ver}  ({len(rows)} fields)")


def cmd_list(args) -> None:
    """List all CSV data dictionaries in the data/ folder."""
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in data/.")
        return
    for f in csv_files:
        rows = read_csv(f)
        ver = rows[0].get("version", "unknown") if rows else "unknown"
        print(f"  {f.name:<45} v{ver}  ({len(rows)} fields)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Version and transform CSV data dictionaries."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # bump
    p_bump = subparsers.add_parser("bump", help="Bump the version of a data dictionary")
    p_bump.add_argument("--file", required=True, help="CSV filename (relative to data/)")
    p_bump.add_argument(
        "--part",
        choices=["major", "minor", "patch"],
        default="patch",
        help="Which part of the semver to bump (default: patch)",
    )
    p_bump.set_defaults(func=cmd_bump)

    # add-field
    p_add = subparsers.add_parser("add-field", help="Add a new field to a data dictionary")
    p_add.add_argument("--file", required=True, help="CSV filename (relative to data/)")
    p_add.add_argument("--field", required=True, help="Field name to add")
    p_add.add_argument("--type", required=True, help="Data type of the field")
    p_add.add_argument("--description", required=True, help="Description of the field")
    p_add.add_argument("--allowed-values", default="", help="Allowed values (optional)")
    p_add.add_argument(
        "--required", choices=["true", "false"], default="false", help="Is the field required?"
    )
    p_add.set_defaults(func=cmd_add_field)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate a data dictionary CSV")
    p_val.add_argument("--file", required=True, help="CSV filename (relative to data/)")
    p_val.set_defaults(func=cmd_validate)

    # changelog
    p_cl = subparsers.add_parser("changelog", help="Show version changelog for all dictionaries")
    p_cl.set_defaults(func=cmd_changelog)

    # list
    p_ls = subparsers.add_parser("list", help="List all CSV data dictionaries")
    p_ls.set_defaults(func=cmd_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
