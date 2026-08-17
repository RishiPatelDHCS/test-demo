# Agent Prompt: Create a New Data Dictionary

## Context

You are helping to create new versioned CSV data dictionaries stored in the `data/` folder of this repository. The script `scripts/transform_data_dictionary.py` manages versioning and transformations.

## Task

Create a new data dictionary CSV file for a dataset.

**Instructions:**

1. Create a new CSV file in `data/` with the following required columns:

```
field_name,data_type,description,allowed_values,required,version,last_updated
```

2. Start at version `1.0.0` and use today's date for `last_updated`.

3. Add one row per field in the dataset.

4. Register the file in `data/versions.json` by running:

```bash
python - <<'EOF'
import json
from pathlib import Path
from datetime import date

versions_path = Path("data/versions.json")
with open(versions_path) as f:
    versions = json.load(f)

filename = "<YOUR_CSV_FILENAME>"
versions["files"][filename] = "1.0.0"
versions["last_updated"] = date.today().isoformat()

with open(versions_path, "w") as f:
    json.dump(versions, f, indent=2)
    f.write("\n")

print(f"Registered {filename} in versions.json")
EOF
```

5. Validate the new file:

```bash
python scripts/transform_data_dictionary.py validate --file <YOUR_CSV_FILENAME>
```

## CSV Template

```csv
field_name,data_type,description,allowed_values,required,version,last_updated
example_id,string,Unique identifier,,true,1.0.0,<TODAY>
example_name,string,Human-readable name,,true,1.0.0,<TODAY>
```

## Naming Convention

Name CSV files using lowercase with underscores and the suffix `_data_dictionary.csv`:
- `patient_data_dictionary.csv`
- `claims_data_dictionary.csv`
- `provider_data_dictionary.csv`
