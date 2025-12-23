"""Operator imports.

This module provides all geometric algebra operators.
Import specific operators as needed, or use this for all operators.
"""

# Ensure operators package is initialized first
# This prevents KeyError: 'Sygal.operators' when importing operators
import Sygal.operators

# Associative operators
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

# Binary operators
from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct

# Outermorphic operators
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection
from Sygal.operators.binop.outermorphic.outermorphic import outermorphic

# Isomorphic operators
from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic

# Transform operators
from Sygal.operators.binop.outermorphic.isomorphic.transforms.transforms import transforms
from Sygal.operators.binop.outermorphic.isomorphic.transforms.dilation import dilation
from Sygal.operators.binop.outermorphic.isomorphic.transforms.rotation import rotation
from Sygal.operators.binop.outermorphic.isomorphic.transforms.translation import translation

__all__ = [
  # Associative
  'gadd', 'gextp', 'gmul',
  # Binary
  'ganticomm', 'gcomm', 'sclrprdct', 'grcntrct', 'glcntrct',
  # Outermorphic
  'projection', 'rejection', 'outermorphic',
  # Isomorphic
  'inversion', 'isomorphic',
  # Transforms
  'transforms', 'dilation', 'rotation', 'translation',
]

