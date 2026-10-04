# Test Files Status and Standardization

## Summary

**Total Test Files**: 17  
**Files with Test Cases**: 4 (all standardized ✅)  
**Empty Test Files**: 13 (just `assert True`)

## Files with Test Cases (Standardized ✅)

### ✅ test_gadd.py
- **Status**: Standardized
- **Test Cases**:
  - `test_cases_distri` (12 cases) - Distribution over gadd
  - `test_cases_distri_coeff` (2 cases) - Distribution with coefficients
- **Transformation**: `GExpr.gdistribute`
- **Format**: Standard ✅

### ✅ test_gmul.py
- **Status**: Standardized
- **Test Cases**:
  - `test_cases_canon` (2 cases) - Canonicalization
  - `test_cases_higher_inv` (11 cases) - Higher form to inversion
  - `test_cases_higher_proj` (2 cases) - Higher form to projection
  - `test_cases_higher_rej` (4 cases) - Higher form to rejection
- **Transformations**: `canon_iter(gmul)`, `higher_iter(gmul)`
- **Format**: Standard ✅

### ✅ test_gextp.py
- **Status**: Standardized
- **Test Cases**:
  - `test_cases_sandhi` (7 cases) - Sandhi combination rule
  - `test_cases_gmul_2proj` (6 cases) - gmul to projection
- **Transformation**: `canon_iter(gextp)`
- **Format**: Standard ✅

### ✅ test_inversion.py
- **Status**: Standardized
- **Test Cases**:
  - `test_cases_higher` (1 case) - Higher form of inversion
- **Transformation**: `higher_iter(inversion)`
- **Format**: Standard ✅

**Total Test Cases Extracted**: ~39 cases

---

## Empty Test Files (Need Test Cases)

These files currently only have `assert True` and need actual test cases:

### ⚠️ Binary Operators
- `test_gcomm.py` - Commutator operator
- `test_ganticomm.py` - Anti-commutator operator
- `test_glcntrct.py` - Left contraction operator
- `test_grcntrct.py` - Right contraction operator
- `test_sclprdct.py` - Scalar product operator

### ⚠️ Outermorphic Operators
- `test_projection.py` - Projection operator
- `test_rejection.py` - Rejection operator
- `test_outermorphism.py` - Outermorphic operator

### ⚠️ Isomorphic Operators
- `test_isomorphism.py` - Isomorphic operator

### ⚠️ Transform Operators
- `test_transforms.py` - Base transforms class
- `test_dilation.py` - Dilation transformation
- `test_rotation.py` - Rotation transformation
- `test_translation.py` - Translation transformation

**Total Empty Files**: 13

---

## Standardization Status

| Category | Total | Standardized | Empty | Status |
|----------|-------|--------------|-------|--------|
| **Files with test cases** | 4 | 4 ✅ | 0 | **100% Complete** |
| **Empty files** | 13 | 0 | 13 | Need test cases |
| **Total** | 17 | 4 | 13 | **All files with cases standardized** |

---

## Next Steps

### For Empty Test Files

These files need test cases following the standard format:

```python
from Sygal.initial import *

# Example for test_glcntrct.py
test_cases_canon = [
  (glcntrct(a1, a2), expected_output1),
  (glcntrct(a1, a2^a3), expected_output2),
]

def test_glcntrct_canon():
  """Test canonicalization of left contraction."""
  transformation = canon_iter(glcntrct)
  assert all([transformation(x) == y for x, y in test_cases_canon])

# Example for test_projection.py
test_cases_expand = [
  (projection(a1, a2+a3), projection(a1, a2) + projection(a1, a3)),
]

def test_projection_expand():
  """Test expansion of projection."""
  transformation = expand_iter(projection)
  assert all([transformation(x) == y for x, y in test_cases_expand])
```

### Priority Order

1. **High Priority** (Core operators):
   - `test_glcntrct.py`
   - `test_grcntrct.py`
   - `test_sclprdct.py`
   - `test_projection.py`
   - `test_rejection.py`

2. **Medium Priority** (Other operators):
   - `test_gcomm.py`
   - `test_ganticomm.py`
   - `test_outermorphism.py`
   - `test_isomorphism.py`

3. **Low Priority** (Transform operators):
   - `test_transforms.py`
   - `test_dilation.py`
   - `test_rotation.py`
   - `test_translation.py`

---

## Conclusion

✅ **All test files with actual test cases have been standardized!**

The 4 files that contain test cases (`test_gadd.py`, `test_gmul.py`, `test_gextp.py`, `test_inversion.py`) are all in the standard format and can be automatically extracted.

The remaining 13 files are empty (just `assert True`) and need test cases to be added following the standard format.

---

**Last Updated**: 2025-01-14  
**Status**: ✅ Standardization complete for all files with test cases

