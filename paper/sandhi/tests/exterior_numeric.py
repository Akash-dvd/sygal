"""Exact exterior algebra over Q with a random bilinear form, and an evaluator
that maps a fully expanded Sygal expression onto it.

Used by ``crosscheck_lean.py`` to compare Sygal results with the Lean formulas
independently of Sygal's symbolic normal form.
"""

import random
import re
from fractions import Fraction

import sympy as sp

from Sygal.GExpr import GExpr
from Sygal.operators.binop.sclrprdct import sclrprdct

N = 9
_ANSI = re.compile(r"\x1b\[[0-9;]*m")


class Model:
  """Random symmetric form ``G`` on Q^N (Sygal's ``|`` is symmetric) and
  random vectors for the named atoms."""

  def __init__(self, names, seed):
    rng = random.Random(seed)
    self.G = [[Fraction(0)] * N for _ in range(N)]
    for i in range(N):
      for j in range(i, N):
        self.G[i][j] = self.G[j][i] = Fraction(rng.randint(-3, 3))
    self.vecs = {n: [Fraction(rng.randint(-2, 2)) for _ in range(N)] for n in names}

  def dot(self, u, v):
    return sum(u[i] * self.G[i][j] * v[j] for i in range(N) for j in range(N))

  def vec(self, name):
    u = self.vecs[name]
    return {(i,): u[i] for i in range(N) if u[i] != 0}


def add(x, y, c=1):
  out = dict(x)
  for k, v in y.items():
    out[k] = out.get(k, 0) + c * v
    if out[k] == 0:
      del out[k]
  return out


def scale(c, x):
  return {k: c * v for k, v in x.items() if c * v != 0}


def _wedge_basis(a, b):
  if set(a) & set(b):
    return 0, None
  arr = list(a) + list(b)
  sign = 1
  for i in range(len(arr)):
    for j in range(len(arr) - 1 - i):
      if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        sign = -sign
  return sign, tuple(arr)


def wedge(x, y):
  out = {}
  for ka, va in x.items():
    for kb, vb in y.items():
      s, k = _wedge_basis(ka, kb)
      if s:
        out[k] = out.get(k, 0) + s * va * vb
  return {k: v for k, v in out.items() if v != 0}


def wedges(*xs):
  out = {(): Fraction(1)}
  for x in xs:
    out = wedge(out, x)
  return out


def _name(x):
  return _ANSI.sub("", str(x))


def _ev_scalar(e, m):
  e = sp.sympify(e)
  subs = {}
  for s in e.atoms(sclrprdct):
    x, y = [_name(t) for t in s.args]
    subs[s] = sp.Rational(m.dot(m.vecs[x], m.vecs[y]))
  return Fraction(str(sp.nsimplify(e.xreplace(subs))))


def _ev_mv(mv, m):
  if type(mv).__name__ == "gextp":
    return wedges(*[m.vec(_name(a)) for a in mv.args])
  if _name(mv) in m.vecs:
    return m.vec(_name(mv))
  if mv == GExpr.Onl.mv:
    return {(): Fraction(1)}
  raise ValueError(f"cannot evaluate {type(mv).__name__}: {_name(mv)}")


def evaluate(box, m):
  """Value of a fully expanded (contraction-free) Sygal expression."""
  if box == GExpr.Znl:
    return {}
  c = _ev_scalar(box.coeff, m)
  if type(box.mv).__name__ == "gadd":
    out = {}
    for b in box.mv.args:
      out = add(out, evaluate(b, m))
    return scale(c, out)
  return scale(c, _ev_mv(box.mv, m))
