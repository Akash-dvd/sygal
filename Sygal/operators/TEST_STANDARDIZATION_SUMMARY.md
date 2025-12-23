# Test File Standardization Summary

## Overview

All test files have been standardized to a consistent format that enables automatic extraction of training examples.

## Standard Format

```python
from Sygal.initial import *

# Test cases: list of (input_expr, output_expr) tuples
test_cases_<descriptive_name> = [
  (input_expr1, output_expr1),
  (input_expr2, output_expr2),
  # ... more test cases
]

def test_<descriptive_name>():
  """Description of what this test checks."""
  transformation = canon_iter(gmul)  # or higher_iter, expand_iter, GExpr.gdistribute
  assert all([transformation(x) == y for x, y in test_cases_<descriptive_name>])
```

## Files Updated

### ✅ test_gadd.py
- **Before**: `test_cases1`, `test_cases2` with `reduce(lambda x, y: x and y, [...])`
- **After**: `test_cases_distri`, `test_cases_distri_coeff` with explicit `transformation = GExpr.gdistribute` and `assert all([...])`

### ✅ test_gmul.py
- **Before**: `test_cases1`, `test_cases2`, `test_cases3`, `test_cases4` inside functions with `reduce(...)`
- **After**: 
  - `test_cases_canon` with `transformation = canon_iter(gmul)`
  - `test_cases_higher_inv` with `transformation = higher_iter(gmul)`
  - `test_cases_higher_proj` with `transformation = higher_iter(gmul)`
  - `test_cases_higher_rej` with `transformation = higher_iter(gmul)`
  - All use `assert all([...])`

### ✅ test_gextp.py
- **Before**: `test_cases` inside functions with manual loops or `assert all([...])`
- **After**: 
  - `test_cases_sandhi` with `transformation = canon_iter(gextp)` and explicit comparison
  - `test_cases_gmul_2proj` with `transformation = canon_iter(gextp)` and `assert all([...])`

### ✅ test_inversion.py
- **Before**: `test_cases1` at module level with `assert all([...])`
- **After**: `test_cases_higher` with explicit `transformation = higher_iter(inversion)` and `assert all([...])`

## Benefits

1. **Consistent Format**: All tests follow the same pattern
2. **Easy Extraction**: Extractor can find all test cases automatically
3. **Clear Intent**: Transformation is explicit, not hidden in reduce loops
4. **Better Readability**: Descriptive test case names (e.g., `test_cases_distri` instead of `test_cases1`)
5. **Maintainability**: Easy to add new test cases

## Extractor Updates

The extractor now:
1. ✅ Looks for explicit `transformation = ...` assignment (standard format)
2. ✅ Falls back to parsing `assert all([...])` patterns (standard format)
3. ✅ Falls back to parsing `reduce(...)` patterns (legacy format)
4. ✅ Handles manual loops (legacy format)
5. ✅ Supports descriptive test case names (e.g., `test_cases_distri`, `test_cases_canon`)

## Migration Status

## Files with Test Cases (All Standardized ✅)

| File | Status | Test Cases Extracted |
|------|--------|---------------------|
| `test_gadd.py` | ✅ Standardized | `test_cases_distri` (12 cases), `test_cases_distri_coeff` (2 cases) |
| `test_gmul.py` | ✅ Standardized | `test_cases_canon` (2 cases), `test_cases_higher_inv` (11 cases), `test_cases_higher_proj` (2 cases), `test_cases_higher_rej` (4 cases) |
| `test_gextp.py` | ✅ Standardized | `test_cases_sandhi` (7 cases), `test_cases_gmul_2proj` (6 cases) |
| `test_inversion.py` | ✅ Standardized | `test_cases_higher` (1 case) |

**Total**: 4 files standardized, ~39 test cases extracted

## Empty Test Files (Need Test Cases)

These files currently only have `assert True` and need test cases following the standard format:

| File | Status | Notes |
|------|--------|-------|
| `test_glcntrct.py` | ⚠️ Empty | Left contraction operator |
| `test_grcntrct.py` | ⚠️ Empty | Right contraction operator |
| `test_sclprdct.py` | ⚠️ Empty | Scalar product operator |
| `test_gcomm.py` | ⚠️ Empty | Commutator operator |
| `test_ganticomm.py` | ⚠️ Empty | Anti-commutator operator |
| `test_projection.py` | ⚠️ Empty | Projection operator |
| `test_rejection.py` | ⚠️ Empty | Rejection operator |
| `test_outermorphism.py` | ⚠️ Empty | Outermorphic operator |
| `test_isomorphism.py` | ⚠️ Empty | Isomorphic operator |
| `test_transforms.py` | ⚠️ Empty | Base transforms class |
| `test_dilation.py` | ⚠️ Empty | Dilation transformation |
| `test_rotation.py` | ⚠️ Empty | Rotation transformation |
| `test_translation.py` | ⚠️ Empty | Translation transformation |

**Total**: 13 empty files need test cases

For complete status, see `TEST_FILES_STATUS.md`.

**Total Extracted**: ~39 test cases from standardized files

## Next Steps

1. ✅ Standardize existing test files - **DONE**
2. ⚠️ Add test cases to empty test files (`test_glcntrct.py`, `test_sclprdct.py`, etc.)
3. ✅ Update extractor to handle standard format - **DONE**
4. ⚠️ Test extractor on all test files
5. ⚠️ Document standard format for future tests

## Example: Before vs After

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
test_cases_canon = [
  (a1*a2, b1*b2),
]

def test_gmul_simp():
  """Test scalar simplification."""
  transformation = canon_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases_canon])
```

## Transformation Types

1. **Canonicalization**: `transformation = canon_iter(operator)`
2. **Higher form**: `transformation = higher_iter(operator)`
3. **Expansion**: `transformation = expand_iter(operator)`
4. **Distribution**: `transformation = GExpr.gdistribute`

---

**Last Updated**: 2025-01-14  
**Status**: ✅ Standardization complete for files with test cases

