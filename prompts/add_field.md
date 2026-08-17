# Agent Prompt: Add a Field to a Data Dictionary

## Context

You are helping to maintain versioned CSV data dictionaries stored in the `data/` folder of this repository. Each CSV file represents a data dictionary for a specific dataset. The script `scripts/transform_data_dictionary.py` manages versioning and transformations.

## Task

Add a new field to the data dictionary CSV file specified below.

**Instructions:**

1. Run the following command, replacing the placeholder values:

```bash
python scripts/transform_data_dictionary.py add-field \
  --file <CSV_FILENAME> \
  --field <FIELD_NAME> \
  --type <DATA_TYPE> \
  --description "<DESCRIPTION>" \
  --allowed-values "<ALLOWED_VALUES>" \
  --required <true|false>
```

2. After running the command, verify the new field appears at the bottom of the CSV:

```bash
python scripts/transform_data_dictionary.py validate --file <CSV_FILENAME>
```

3. Show the changelog to confirm the version was bumped:

```bash
python scripts/transform_data_dictionary.py changelog
```

## Example

To add a `language_preference` field to `patient_data_dictionary.csv`:

```bash
python scripts/transform_data_dictionary.py add-field \
  --file patient_data_dictionary.csv \
  --field language_preference \
  --type string \
  --description "Patient's preferred language for communication" \
  --allowed-values "English, Spanish, Cantonese, Vietnamese, Other" \
  --required false
```

## Output

- The CSV file is updated in place with the new field row appended.
- All rows have their `version` and `last_updated` columns updated.
- `data/versions.json` is updated with the new version number.
