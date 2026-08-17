# Agent Prompt: Bump the Version of a Data Dictionary

## Context

You are helping to maintain versioned CSV data dictionaries stored in the `data/` folder of this repository. The script `scripts/transform_data_dictionary.py` manages versioning and transformations.

Versioning follows **Semantic Versioning (semver)**:
- **major** – breaking changes (e.g., removed or renamed fields)
- **minor** – backwards-compatible additions (e.g., new optional fields)
- **patch** – minor corrections (e.g., fixing a description typo)

## Task

Bump the version of a data dictionary CSV file.

**Instructions:**

1. Decide which version part to bump based on the nature of the change.

2. Run the following command:

```bash
python scripts/transform_data_dictionary.py bump \
  --file <CSV_FILENAME> \
  --part <major|minor|patch>
```

3. Confirm the version was updated:

```bash
python scripts/transform_data_dictionary.py changelog
```

## Examples

Patch bump for a description correction in `claims_data_dictionary.csv`:

```bash
python scripts/transform_data_dictionary.py bump \
  --file claims_data_dictionary.csv \
  --part patch
```

Minor bump for adding new optional fields to `patient_data_dictionary.csv`:

```bash
python scripts/transform_data_dictionary.py bump \
  --file patient_data_dictionary.csv \
  --part minor
```

## Output

- All rows in the CSV have their `version` and `last_updated` columns updated.
- `data/versions.json` is updated with the new version.
