# Agent Prompt: Generate a Changelog

## Context

You are helping to maintain versioned CSV data dictionaries stored in the `data/` folder of this repository. The script `scripts/transform_data_dictionary.py` can generate a changelog summary.

## Task

Generate and display a changelog of all data dictionary versions.

**Instructions:**

1. Run the changelog command:

```bash
python scripts/transform_data_dictionary.py changelog
```

2. List all CSV files and their current state:

```bash
python scripts/transform_data_dictionary.py list
```

## Example Output

```
Data Dictionary Changelog (last updated: 2026-08-17)
------------------------------------------------------------
  patient_data_dictionary.csv                   v1.2.0  (9 fields)
  claims_data_dictionary.csv                    v1.1.0  (8 fields)
```

## Extended Task: Write a Markdown Changelog

If you need a human-readable changelog document, generate one using the current state of the data dictionaries:

```bash
python - <<'EOF'
import csv, json
from pathlib import Path
from datetime import date

data_dir = Path("data")
versions = json.loads((data_dir / "versions.json").read_text())

lines = [
    "# Data Dictionary Changelog",
    "",
    f"_Generated on {date.today().isoformat()}_",
    "",
]

for filename, version in sorted(versions["files"].items()):
    path = data_dir / filename
    if not path.exists():
        continue
    with open(path) as f:
        rows = list(csv.DictReader(f))
    lines += [
        f"## {filename}",
        "",
        f"**Current version:** {version}  ",
        f"**Fields:** {len(rows)}",
        "",
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['field_name']}` | {row['data_type']} | {row['required']} | {row['description']} |"
        )
    lines.append("")

print("\n".join(lines))
EOF
```

You can redirect the output to a markdown file:

```bash
python ... > data/CHANGELOG.md
```
