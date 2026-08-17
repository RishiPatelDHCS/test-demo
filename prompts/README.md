# Data Dictionary CSV Versioning Agent Prompts

This folder contains prompt templates for AI-assisted transformation and versioning of CSV data dictionaries in the `data/` folder.

## How to Use

Each `.md` file in this folder is a prompt you can give to an AI coding assistant (e.g., GitHub Copilot, Claude) to perform a specific transformation task on the CSV data dictionaries.

The prompts reference the Python helper script at `scripts/transform_data_dictionary.py`.

## Available Prompts

| Prompt File | Purpose |
|---|---|
| `add_field.md` | Add a new field to an existing data dictionary |
| `bump_version.md` | Bump the version of a data dictionary |
| `validate_dictionary.md` | Validate a data dictionary for completeness |
| `create_dictionary.md` | Create a new data dictionary CSV from scratch |
| `generate_changelog.md` | Generate a human-readable changelog from version history |
