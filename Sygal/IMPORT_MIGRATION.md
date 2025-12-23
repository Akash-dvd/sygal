# Sygal Import Migration Guide

## Overview

The Sygal package has been reorganized to use clean, explicit imports instead of `import *` statements. This improves code clarity, reduces namespace pollution, and makes dependencies explicit.

## New Import Structure

### Focused Import Modules

All new import modules are in `Sygal/imports/`:

1. **`core.py`** - Core Sygal types
   - `GExpr`, `GAtom`, `Box`

2. **`sympy_basic.py`** - Basic SymPy imports
   - `Basic`, `S`, `Expr`, `Mul`, `Add`, `Pow`, etc.
   - `StrPrinter`, `Permutation`
   - `partitions`, `multiset_partitions`, `kbins`

3. **`strategies.py`** - Strategy functions
   - `exhaust`, `typed`, `do_one`, `chain`, `tryit`, etc.
   - `top_down`, `bottom_up`, `canon_iter`, `expand_iter`, etc.

4. **`utils.py`** - Utility functions
   - `bx_sift`, `is_uniGraded`, `is_devmode`, etc.
   - `kbin_distri`, `parity`, `GSortArgs`, etc.

5. **`psc.py`** - Pseudoscalar functions
   - `grd`, `spcdct`, `spclst`, `Ngrd`

6. **`operators.py`** - All operators (optional, import specific ones as needed)
   - All associative, binary, outermorphic, isomorphic, and transform operators

7. **`typing_helpers.py`** - Typing imports
   - `Tuple`, `List`, `Dict`, `Optional`, `Union`, etc.
   - `Iterable`, `defaultdict`, `reduce`, `product`

## Migration Pattern

### Before (Old Style)
```python
from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *
from Sygal.imports.import_util2 import *
```

### After (New Style)
```python
# Core imports
from Sygal.imports.core import Box, GExpr
from Sygal.imports.sympy_basic import Basic, Mul, S
from Sygal.imports.typing_helpers import Tuple
from Sygal.imports.strategies import exhaust, typed, do_one
from Sygal.imports.utils import bx_sift, is_devmode
from Sygal.imports.psc import spclst
from Sygal.imports.sympy_basic import StrPrinter

# Only import operators actually used
from Sygal.operators.assop.gadd import gadd
```

## Common Patterns

### Operator Files (gadd.py, gmul.py, etc.)
```python
# Core imports
from Sygal.imports.core import Box, GExpr
from Sygal.imports.sympy_basic import Basic, Mul, S
from Sygal.imports.typing_helpers import Tuple
from Sygal.imports.strategies import exhaust, typed, do_one
from Sygal.imports.utils import bx_sift, is_devmode
from Sygal.imports.psc import spclst
from Sygal.imports.sympy_basic import StrPrinter

from Sygal.operators.assop.assop import assop
```

### Expand/Canon/Higher Files
```python
# Core imports
from Sygal.imports.core import Box, GExpr
from Sygal.imports.sympy_basic import Expr, S
from Sygal.imports.typing_helpers import Union
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_perpendicularPair, is_vecBlade

# Only import operators actually used (not all!)
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.binop.glcntrct import glcntrct
```

## Benefits

1. **Explicit Dependencies**: Clear what each file depends on
2. **No Namespace Pollution**: Only imports what's needed
3. **Better IDE Support**: Autocomplete and type checking work better
4. **Easier Refactoring**: Can track where symbols are used
5. **Performance**: Faster imports (no loading unused modules)

## Migration Status

### Completed
- ✅ Created new import modules (`core.py`, `sympy_basic.py`, etc.)
- ✅ Updated `gadd.py`, `glcntrct.py`, `gmul.py`, `grcntrct.py`, `sclrprdct.py`
- ✅ Updated `gaddexpand.py`, `glcntrctcanon.py`, `glcntrcthigher.py`
- ✅ Updated `projection.py`

### Remaining
- ⏳ Update remaining operator files (gextp, ganticomm, gcomm, etc.)
- ⏳ Update remaining expand/canon/higher files (~33 files)
- ⏳ Update `__init__.py` and `initial.py`
- ⏳ Update test files
- ⏳ Remove old import files (after full migration)

## Notes

- Old import files (`import1head.py`, `import1tail.py`, `import_util2.py`) are kept for backward compatibility during migration
- Files can be migrated incrementally
- Test after each migration to ensure functionality

