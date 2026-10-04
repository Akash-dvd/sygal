"""Bake chamber-data.json from the real SandhiCanon engine.

The reaction chamber page animates one sandhi merge at a time. Every frame it
shows - the panels before, the seam that contracts, the signed permutation
expansion of the overlap scalar, and the residual panel - comes from running
the engine here, not from hand-written data.

Run from the repository root:

    python3 Sygal/operators/assop/canon/game/bake_chamber.py
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
if ROOT not in sys.path:
  sys.path.insert(0, ROOT)

import sympy

from Sygal.initial import *  # noqa: F401,F403  (atoms a1, d1, A1 ... live here)
from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.assop.canon.gextpcanon import SandhiCanon

ANSI = re.compile(r"\x1b\[[0-9;]*m")
PAIRING = re.compile(r"\(([A-Za-z]+\d*)\|([A-Za-z]+\d*)\)")
BLADE_PAIRING = re.compile(r"\(([^()|]+)\)\|\(([^()|]+)\)")

OUT_PATH = os.path.join(os.path.dirname(__file__), "chamber-data.json")


def plain(x):
  return ANSI.sub("", str(x))


def unwrap(x):
  """Strip a Box wrapper, returning (multivector, coefficient)."""
  if isinstance(x, Box):
    return x.mv, x.coeff
  return x, sympy.Integer(1)


def shells_of(term):
  """Walk one contraction tower into [{pin, nodes}], outermost shell first."""
  mv, _ = unwrap(term)
  shells = []
  while isinstance(mv, glcntrct):
    down, _ = unwrap(mv.down)
    args = list(down.args) if isinstance(down, gextp) else [down]
    nodes, nested = [], None
    for arg in args:
      inner, _ = unwrap(arg)
      if isinstance(inner, glcntrct):
        nested = inner
      else:
        nodes.append(plain(inner))
    shells.append({"pin": plain(mv.up), "nodes": nodes})
    mv = nested
    if mv is None:
      break
  return shells


def panels_of(expr):
  """Every contraction panel of a wedge, each as a tower of shells."""
  mv, _ = unwrap(expr)
  if mv == GExpr.Znl:
    return []
  args = list(mv.args) if isinstance(mv, gextp) else [mv]
  return [shells_of(arg) for arg in args if isinstance(unwrap(arg)[0], glcntrct)]


def _signed_terms(expr):
  terms = []
  for term in sympy.Add.make_args(sympy.expand(expr)):
    sign = 1
    pairs = []
    for f in sympy.Mul.make_args(term):
      if f.is_number:
        sign *= int(sympy.sign(f))
      else:
        pairs.append(plain(f).strip("()"))
    if pairs:
      terms.append({"sign": sign, "factors": pairs})
  return terms


def determinant_terms(factor):
  """Signed permutation expansion of an overlap scalar, straight from the engine."""
  scalars = [f for f in sympy.Mul.make_args(factor) if isinstance(f, sclrprdct)]
  if not scalars:
    return []

  product = sympy.Mul(*scalars)
  _, coeff = unwrap(sclrprdct.gexpand1(product))
  # A blade pairing expands into signed permutations; a grade-1 pairing is
  # already its own single term, and then the expansion carries no factors.
  terms = _signed_terms(coeff) or _signed_terms(product)

  # Carry the sign the engine put in front of the whole coefficient.
  outer = sympy.Mul(*[f for f in sympy.Mul.make_args(factor) if f.is_number])
  if outer.is_number and outer < 0:
    terms = [{"sign": -t["sign"], "factors": t["factors"]} for t in terms]
  return terms


def seam_of(factor):
  """Which pins pair with which seam symbols, and the resulting determinant."""
  label = plain(factor)
  blade = BLADE_PAIRING.search(label)
  if blade:
    rows = [s.strip() for s in blade.group(1).split("^")]
    cols = [s.strip() for s in blade.group(2).split("^")]
  else:
    pairs = PAIRING.findall(label)
    rows = [p[0] for p in pairs]
    cols = [p[1] for p in pairs]

  return {
    "label": label,
    "rows": rows,
    "cols": cols,
    "terms": determinant_terms(factor),
  }


def step_trace(expr):
  """Apply sandhi one merge at a time, recording each frame."""
  steps = []
  current = expr
  guard = 0

  while guard < 24:
    guard += 1
    nxt = SandhiCanon.sandhi(current)
    if nxt == current:
      break

    before_mv, before_coeff = unwrap(current)
    after_mv, after_coeff = unwrap(nxt)
    # A vanishing merge comes back either as Znl or as a zero-coefficient Box.
    zero = after_mv == GExpr.Znl or after_coeff == 0

    # Plain division: sympy's Mul already cancels the shared scalar factors, and
    # simplify() cannot rebuild the custom GAtom nodes.
    factor = sympy.Integer(0) if zero else after_coeff / before_coeff
    steps.append({
      "before": plain(current),
      "after": plain(nxt),
      "panelsBefore": panels_of(current),
      "panelsAfter": [] if zero else panels_of(nxt),
      "coeff": plain(factor),
      "zero": bool(zero),
      "seam": {"label": "0", "rows": [], "cols": [], "terms": []} if zero else seam_of(factor),
    })

    current = nxt
    if zero:
      break

  return steps, current


def case(cid, title, note, expr):
  steps, final = step_trace(expr)
  mv, coeff = unwrap(final)
  return {
    "id": cid,
    "title": title,
    "note": note,
    "input": {"expr": plain(expr), "panels": panels_of(expr)},
    "steps": steps,
    "result": {
      "expr": plain(final),
      "coeff": plain(coeff),
      "panels": [] if (mv == GExpr.Znl or coeff == 0) else panels_of(final),
      "zero": mv == GExpr.Znl or coeff == 0,
    },
  }


def build():
  return [
    case(
      "flat",
      "One seam, one scalar",
      "Two panels share the symbol a3. It contracts out as the pairing (a1|a3) and "
      "the survivors wedge into a single panel.",
      (a1 < (a2 ^ a3)) ^ (a1 < (a3 ^ a4)),
    ),
    case(
      "chain",
      "A chain of two collapses",
      "Three panels, two seams. The residual of the first merge is still mergeable, "
      "so the scalars multiply.",
      (a1 < (a2 ^ a3)) ^ (a1 < (a3 ^ a4)) ^ (a1 < (a4 ^ b1)),
    ),
    case(
      "rank2",
      "A two-blade seam",
      "The shared core is a 2-blade, so the overlap scalar is a 2x2 determinant "
      "rather than a single pairing.",
      ((A1 ^ A2) < (B1 ^ B2 ^ C1)) ^ ((A1 ^ A2) < (B1 ^ B2 ^ C2)),
    ),
    case(
      "deep",
      "Three nested shells",
      "The seam sits three shells down. One merge collapses the whole tower and "
      "emits a 3x3 determinant of pin-core pairings.",
      (d1 < (a1 ^ a2 ^ (d2 < (b1 ^ b2 ^ (d3 < (c1 ^ c2 ^ c3))))))
      ^ (d1 < (a3 ^ a4 ^ (d2 < (b3 ^ b4 ^ (d3 < (c1 ^ c2 ^ c3 ^ c4)))))),
    ),
    case(
      "bisector",
      "Three perpendicular bisectors",
      "Each panel is a bisector. Merging all three repeats a symbol inside the "
      "wedge, so the product is exactly zero: the three lines are concurrent.",
      (A1 < (a1 ^ a2)) ^ (A1 < (a2 ^ a3)) ^ (A1 < (a3 ^ a1)),
    ),
  ]


if __name__ == "__main__":
  data = build()
  with open(OUT_PATH, "w") as fh:
    json.dump(data, fh, indent=2)
  print(f"wrote {OUT_PATH}")
  for c in data:
    print(f"  {c['id']:10} steps={len(c['steps'])}  result={c['result']['expr']}")
