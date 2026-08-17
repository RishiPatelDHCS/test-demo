# Agent Prompt: Validate a Data Dictionary

## Context

You are helping to maintain versioned CSV data dictionaries stored in the `data/` folder of this repository. The script `scripts/transform_data_dictionary.py` can validate these files.

A valid data dictionary CSV must have the following columns:
- `field_name`
- `data_type`
- `description`
- `required`
- `version`
- `last_updated`

## Task

Validate one or all data dictionary CSV files.

**Validate a single file:**

```bash
python scripts/transform_data_dictionary.py validate --file <CSV_FILENAME>
```

**Validate all CSV files:**

```bash
for f in data/*.csv; do
  python scripts/transform_data_dictionary.py validate --file "$(basename $f)"
done
```

## Expected Output

On success:
```
Validation PASSED for patient_data_dictionary.csv (7 fields, version 1.0.0)
```

On failure:
```
Validation FAILED for patient_data_dictionary.csv. Missing columns: {'allowed_values'}
```

## Instructions

1. Run the validation command above.
2. If validation fails, identify the missing columns and add them to the CSV.
3. Re-run validation to confirm all issues are resolved.
4. Run `python scripts/transform_data_dictionary.py changelog` to display the current state of all dictionaries.
