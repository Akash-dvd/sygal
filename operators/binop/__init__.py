# Binop package initialization
from .binop import binop
from .ganticomm import ganticomm
from .gcomm import gcomm
from .glcntrct import glcntrct, _initialize_glcntrct
from .grcntrct import grcntrct, _initialize_grcntrct
from .sclrprdct import sclrprdct

# Initialize operators after all imports are complete to avoid circular dependencies
# This ensures higher/canon/expand modules can import operators without circular import errors
_initialize_glcntrct()
_initialize_grcntrct()

__all__ = ['binop', 'ganticomm', 'gcomm', 'glcntrct', 'grcntrct', 'sclrprdct']

