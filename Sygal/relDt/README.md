# relDt Module

## Status

**relDt has been removed from the main Sygal codebase.**

This folder is kept for reference and contains:
- `relDt.py` - The original relDt class implementation
- `example_usage.py` - Example code showing how relDt could be used
- `test/test_relDt.py` - Original test file

## What was relDt?

`relDt` (relationship dictionary) was a dictionary-like class designed to store relationships between geometric algebra expressions (GExpr objects). It provided special handling for Box objects and was used to track relationships between multivectors.

## Why was it removed?

The relDt functionality has been removed from the main project code to simplify the codebase. All references to `relDt` and `rlDt` attributes have been removed from the project.

## Usage

If you need relationship tracking functionality, you can refer to:
- `relDt.py` - The original implementation
- `example_usage.py` - Example code showing how to use relDt

However, **relDt is no longer integrated into the Sygal project** and will not be automatically initialized or used.

