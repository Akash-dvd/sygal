"""Clean import modules for Sygal.

This package provides organized, focused import modules to replace
the old `import1head`, `import1tail`, and `import_util2` modules.

Modules:
  - core: GExpr, GAtom, Box
  - sympy_basic: Basic SymPy types and functions
  - strategies: Strategy functions for rewrite rules
  - utils: Utility functions
  - psc: Pseudoscalar functions
  - operators: All geometric algebra operators
  - typing_helpers: Common typing imports
"""

from . import core
from . import sympy_basic
from . import strategies
from . import utils
from . import psc
from . import operators
from . import typing_helpers

__all__ = [
  'core', 'sympy_basic', 'strategies', 'utils', 'psc', 'operators', 'typing_helpers',
]

