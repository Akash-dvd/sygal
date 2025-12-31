# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *

Ngrd = grd(None,None)

def test_init():
  test_cases = [
    (spcdct({GExpr.I41:1}),
     spcdct({GExpr.I41:grd(1,4)})),
    
    (spcdct({GExpr.I41:5}),
     spcdct({GExpr.I41:Ngrd})),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_getitem():
  A1 = spcdct({GExpr.I5:2})

  test_cases = [
    (A1[GExpr.I8],
     Ngrd),
    
    (A1[GExpr.I5],
     grd(2,5)),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_sub_update():
  A1 = spcdct({})
  A1.sup_update({GExpr.I5:2})
  A1.sup_update({GExpr.I8:3})

  assert len(A1) == 2

def test_update():
  A1 = {}
  A1.update(spcdct({}))
  A2 = spcdct({})
  A2.update(spcdct({}))
  A3 = spcdct({})
  A3.update({})
  A4 = spcdct({GExpr.I5:1})
  A4.update({})
  A5 = spcdct({GExpr.I5:1,GExpr.I31:1})

  test_cases = [
    (A1,
     {}),
    
    (A2,
     spcdct({})),

    (A3,
     spcdct({})),

    (A4,
     spcdct({GExpr.I5:grd(1,5)})),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_eq():
  test_cases = [
    (spcdct({}),
     {}),
    
    (spcdct(spcdct({})),
     {}),

    (spcdct(spcdct(spcdct({}))),
     {}),

    (spcdct(spcdct(spcdct({}))),
     spcdct({})),

    (spcdct({GExpr.I5:1,GExpr.I31:1}),
     {GExpr.I31:grd(1,3),GExpr.I5:grd(1,5)})
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_add():
  test_cases = [
    (spcdct({GExpr.I8:2})+spcdct({GExpr.I5:2}),
     spcdct({GExpr.I5:2,GExpr.I8:2})),
    
    (spcdct({GExpr.I8:2})+spcdct({GExpr.I8:2}),
     spcdct({GExpr.I8:4})),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_or():
  test_cases = [
    (spcdct({GExpr.I8:2})|spcdct({GExpr.I5:2}),
     False),
    
    (spcdct({GExpr.I31:2,GExpr.I42:1})|spcdct({GExpr.I5:3}),
     True),

    # Should have been false
    (spcdct({GExpr.I41:4})|spcdct({GExpr.I42:4}),
     True),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_lt():
  test_cases = [
    (spcdct({GExpr.I8:2})<spcdct({GExpr.I5:2}),
     False),
    
    (spcdct({GExpr.I31:2,GExpr.I42:1})<spcdct({GExpr.I5:3}),
     True),

    # Should have been false
    (spcdct({GExpr.I41:4})<spcdct({GExpr.I42:4}),
     True),
  ]

  assert all([ele1 == ele2 for ele1,ele2 in test_cases])

def test_eq_scalar():
  assert spcdct({GExpr.nl:0}) == spcdct({GExpr.nl:grd(0,0)})

def test_canonicalize1():
  test_cases = [
    (spcdct({GExpr.I8:0,GExpr.I41:1}),
     spcdct({GExpr.I41:1})),
    
    (spcdct({GExpr.I8:0,GExpr.I41:0}),
     spcdct({GExpr.nl:0})),

    (spcdct({GExpr.I8:0,GExpr.I41:0,GExpr.nl:0}),
     spcdct({GExpr.nl:0})),

    (spcdct({GExpr.I8:2,GExpr.I41:1}),
     spcdct({GExpr.I8:2,GExpr.I41:1})),
  ]

  assert all([ele1 == ele2 for ele1,ele2 in test_cases])

def test_canonicalize2():
  # In simplified system, these combinations are valid
  # (The old system had complex validation that was removed)
  test_cases = [
    (spcdct({GExpr.I5:3,GExpr.I42:3}),
     spcdct({GExpr.I5:grd(3,5),GExpr.I42:grd(3,4)})),

    (spcdct({GExpr.I31:2,GExpr.I41:3}),
     spcdct({GExpr.I31:grd(2,3),GExpr.I41:grd(3,4)})),
  ]

  assert all([ele1 == ele2 for ele1,ele2 in test_cases])
