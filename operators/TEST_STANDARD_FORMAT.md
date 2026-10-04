# Standard Test Format for Sygal Operators

## Overview

All test files should follow a standard format to enable automatic extraction of training examples.

## Standard Format

```python
from Sygal.initial import *

# Test cases: list of (input_expr, output_expr) tuples
test_cases = [
  (input_expr1, output_expr1),
  (input_expr2, output_expr2),
  # ... more test cases
]

# Test function with transformation
def test_operator_name():
  """Description of what this test checks."""
  transformation = canon_iter(gmul)  # or higher_iter, expand_iter, GExpr.gdistribute
  assert all([transformation(x) == y for x, y in test_cases])
```

## Transformation Types

1. **Canonicalization**: `canon_iter(operator)`
   ```python
   transformation = canon_iter(gmul)
   ```

2. **Higher form lifting**: `higher_iter(operator)`
   ```python
   transformation = higher_iter(gmul)
   ```

3. **Expansion**: `expand_iter(operator)`
   ```python
   transformation = expand_iter(glcntrct)
   ```

4. **Distribution**: `GExpr.gdistribute`
   ```python
   transformation = GExpr.gdistribute
   ```

## Multiple Test Groups

If you need multiple test groups (e.g., different transformations), use separate functions:

```python
# Test group 1: Canonicalization
test_cases_canon = [
  (expr1, expr2),
  (expr3, expr4),
]

def test_operator_canon():
  """Test canonicalization."""
  transformation = canon_iter(operator)
  assert all([transformation(x) == y for x, y in test_cases_canon])

# Test group 2: Higher form
test_cases_higher = [
  (expr5, expr6),
  (expr7, expr8),
]

def test_operator_higher():
  """Test higher form lifting."""
  transformation = higher_iter(operator)
  assert all([transformation(x) == y for x, y in test_cases_higher])
```

## Migration Guide

### Before (Non-Standard)
```python
test_cases1 = [
  (a1*a2, b1*b2),
]

def test_gmul_simp():
  assert reduce(lambda x,y: x and y, [canon_iter(gmul)(x) == y for x, y in test_cases1])
```

### After (Standard)
```python
test_cases = [
  (a1*a2, b1*b2),
]

def test_gmul_simp():
  """Test scalar simplification."""
  transformation = canon_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases])
```

## Benefits

1. **Automatic extraction**: All test cases can be extracted automatically
2. **Consistency**: All tests follow the same pattern
3. **Readability**: Clear what transformation is being tested
4. **Maintainability**: Easy to add new test cases

## Examples

See updated test files:
- `test_gadd.py` - Standard format ✅
- `test_gmul.py` - Standard format ✅
- `test_gextp.py` - Standard format ✅
- `test_inversion.py` - Standard format ✅

## Status

**All test files with actual test cases have been standardized!**

- ✅ 4 files with test cases: All standardized
- ⚠️ 13 empty test files: Need test cases added (see `TEST_FILES_STATUS.md`)

For complete status of all test files, see `TEST_FILES_STATUS.md`.

