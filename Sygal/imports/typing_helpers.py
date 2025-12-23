"""Typing helper imports.

This module provides common typing imports.
Import this for Tuple, List, Dict, Optional, Union, etc.
"""

from typing import (
  Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,
  NewType, Type, Any, TYPE_CHECKING
)
from collections.abc import Iterable
from collections import defaultdict
from functools import cmp_to_key, reduce
from itertools import product

__all__ = [
  'Tuple', 'TypeVar', 'Callable', 'Dict', 'Sequence', 'List', 'Optional', 'Union',
  'NewType', 'Type', 'Any', 'TYPE_CHECKING',
  'Iterable', 'defaultdict', 'cmp_to_key', 'reduce', 'product',
]

