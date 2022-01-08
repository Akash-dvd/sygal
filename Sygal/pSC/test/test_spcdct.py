# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *


def test_init():
  test_cases = [

  (spcdct({GExpr.I41:1}),
  spcdct({GExpr.I41.mv:grd(1,4)})),
  
  (spcdct({GExpr.I41:5}),
  spcdct({GExpr.I41.mv:Ngrd}))
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_getitem():
  A1 = spcdct({GExpr.I5:2})

  test_cases = [
  
  (A1[GExpr.I8],
  Ngrd),
  
  (A1[GExpr.I8*4],
  Ngrd),  
  
  (A1[GExpr.I8.mv],
  Ngrd),

  (A1[GExpr.I5.mv],
  grd(2,5)),
  
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])

def test_sub_update():
  A1 = spcdct({})
  A1.sup_update({1:2})
  A1.sup_update({2:3})

  assert all([(i+1) == k for i,(k,v) in enumerate(A1.items())])

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
  spcdct({GExpr.I5.mv:grd(1,5)})),
  
  # (spcdct({GExpr.I41:5}),
  # spcdct({GExpr.I41.mv:Ngrd}))
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
  {GExpr.I31.mv:grd(1,3),GExpr.I5.mv:grd(1,5)})

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

def test_eq():
  assert spcdct({GExpr.nl:0}) == spcdct({GExpr.nl:grd(0,0)})

def test_canonicalize1():
  o  = GExpr.primmv[0]
  x  = GExpr.primmv[1]
  y  = GExpr.primmv[2]
  rx = GExpr.primmv[3]
  oo = GExpr.primmv[4]
  x1 = GExpr.primmv[5]
  x2 = GExpr.primmv[6]
  x3 = GExpr.primmv[7]
  x4 = GExpr.primmv[8]
  x5 = GExpr.primmv[9]
  x6 = GExpr.primmv[10]
  x7 = GExpr.primmv[11]
  x8 = GExpr.primmv[12]

  test_cases = [
  
  (spcdct({GExpr.I8:0,GExpr.I41:1}),
  spcdct({GExpr.I41:1})),
  
  (spcdct({GExpr.I8:0,GExpr.I41:0}),
  spcdct({GExpr.nl:0})),

  (spcdct({GExpr.I8:0,GExpr.I41:0,GExpr.nl:0}),
  spcdct({GExpr.nl:0})),

  (spcdct({x1:1,GExpr.I8:2}),
  spcdct({GExpr.I8:3})),

  (spcdct({x:1,o:1,GExpr.I31:2,GExpr.I5:2}),
  spcdct({GExpr.I31:3,GExpr.I5:3})),

  (spcdct({x:1,o:1,GExpr.I31:3,GExpr.I5:2}),
  spcdct({})),
  
  (spcdct({GExpr.nl:0,oo:1,GExpr.I31:3,GExpr.I5:2}),
  spcdct({})),

  (spcdct({GExpr.nl:0,rx:1,o:1,oo:1,GExpr.I31:1,GExpr.I41:1,GExpr.I5:1}),
  spcdct({GExpr.I31:2,GExpr.I41:2,GExpr.I5:2})),

  (spcdct({oo:1,x:1,y:1}),
  spcdct({GExpr.I31:3})),

  (spcdct({oo:1,x:1,x1:1,x2:1,x3:1,x4:1,x5:1,x6:1,x7:1,x8:1}),
  spcdct({oo:1,x:1,GExpr.I8:8})),

  (spcdct({o:1,x:1,y:1,oo:1,x1:1}),
  spcdct({GExpr.I41:4,x1:1})),

  (spcdct({rx:1,x:1,y:1,x1:1,oo:1}),
  spcdct({GExpr.I42:4,x1:1})),

  (spcdct({rx:1,x:1,y:1,x1:1,oo:1,GExpr.I13:1}),
  spcdct({GExpr.I42:4,GExpr.I13:2})),

  (spcdct({rx:1,x:1,oo:1,GExpr.I5:1,x1:1,GExpr.I13:1}),
  spcdct({GExpr.I5:4,GExpr.I13:2})),

  (spcdct({oo:1,x:1,y:1,GExpr.I5:1,x1:1,GExpr.I13:1}),
  spcdct({GExpr.I31:3,GExpr.I5:1,GExpr.I13:2})),

  (spcdct({oo:1,x:1,y:1,GExpr.I5:1,x1:1,GExpr.I8:1,GExpr.I13:1}),
  spcdct({GExpr.I31:3,GExpr.I5:1,GExpr.I8:2,GExpr.I13:1})),

  ]

  assert all([ele1 == ele2 for ele1,ele2 in test_cases])

def test_canonicalize2():

  o  = GExpr.primmv[0]
  x  = GExpr.primmv[1]
  y  = GExpr.primmv[2]
  rx = GExpr.primmv[3]
  oo = GExpr.primmv[4]
  x1 = GExpr.primmv[5]
  x2 = GExpr.primmv[6]
  x3 = GExpr.primmv[7]
  x4 = GExpr.primmv[8]
  x5 = GExpr.primmv[9]
  x6 = GExpr.primmv[10]
  x7 = GExpr.primmv[11]
  x8 = GExpr.primmv[12]

  test_cases = [

  (spcdct({GExpr.I5:3,GExpr.I42:3}),
  spcdct({})),

  (spcdct({GExpr.I31:2,GExpr.I41:3}),
  spcdct({})),

  (spcdct({GExpr.I5:3,GExpr.I42:3}),
  spcdct({})),

  (spcdct({GExpr.I5:3,GExpr.I42:3}),
  spcdct({})),

  ]

  assert all([ele1 == ele2 for ele1,ele2 in test_cases])