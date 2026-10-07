"""Cross-check the Sygal implementation against the Lean-proved formulas.

  A. Sygal blade pairing ``K|S``     vs  Lean ``seamPairing``  (-1)^C(r,2) det[k_i.s_j]
  B. ``CapelliOptionB`` coefficient   vs  Lean ``seamPairing``
  C. ``sandhi_canon`` on flat panels  vs  Lean ``soleSeam_gradeR`` / ``soleSeam_vanish``
  D. nested sole-seam shapes          vs  Lean ``nested_soleSeam'`` / ``nested_vanish``,
     and whether ``sandhi_canon`` actually stitches them

A and B are compared symbolically. C and D are compared by exact evaluation
(rational vectors, random symmetric form, several seeds) of the fully expanded
Sygal expressions, so the result does not depend on Sygal's normal form.
Every comparison includes the sign.

Run from the parent of ``Sygal/`` with it on PYTHONPATH:

    python3 Sygal/paper/sandhi/tests/crosscheck_lean.py
"""

import os
import sys
from itertools import permutations
from math import comb

import sympy as sp

from Sygal.initial import *
from Sygal.operators.assop.canon.gextpcapelli import CapelliOptionB
from Sygal.operators.assop.test.sandhi_helpers import is_merged_panel, sandhi_canon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exterior_numeric as EN  # noqa: E402

KS = [d1, d2, d3, d4]
SS = [c1, c2, c3, c4]
US = [a1, a2, a3, a4]
VS = [b1, b2, b3, b4]
MODELS = [EN.Model([f"{p}{i}" for p in "abcd" for i in range(1, 5)], seed) for seed in (1, 2, 3)]

failures = []
notes = []


def wedge(xs):
  out = GExpr.Onl
  for x in xs:
    out = x if out == GExpr.Onl else out ^ x
  return out


def expand_all(v):
  v = GExpr.gdistribute(expand_iter(glcntrct)(v))
  v = sclrprdct.gexpand1(v)
  return GExpr.gdistribute(v)


def scalar(v):
  v = sclrprdct.gexpand1(v)
  if type(v) == Box:
    assert v.mv == GExpr.Onl.mv, v
    v = v.coeff
  return sp.expand(v)


def perm_sign(p):
  return (-1) ** sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])


def lean_pairing(ks, ss):
  r = len(ks)
  m = [[scalar(ks[i] | ss[j]) for j in range(r)] for i in range(r)]
  det = sp.S(0)
  for p in permutations(range(r)):
    term = sp.S(perm_sign(p))
    for i in range(r):
      term = term * m[i][p[i]]
    det = det + term
  if type(det) == Box:
    det = det.coeff
  return sp.expand((-1) ** comb(r, 2) * det)


def scalar_eq(x, y):
  d = x - y
  if type(d) == Box:
    return d == GExpr.Znl or sp.expand(d.coeff) == 0
  return sp.expand(d) == 0


def same(x, y):
  ex, ey = expand_all(x), expand_all(y)
  return all(EN.add(EN.evaluate(ex, m), EN.evaluate(ey, m), -1) == {} for m in MODELS)


def check(name, ok):
  print(("ok    " if ok else "FAIL  ") + name, flush=True)
  if not ok:
    failures.append(name)


def section_pairing():
  print("== A/B: pairing and CapelliOptionB coefficient")
  for r in range(1, 5):
    ks, ss = KS[:r], SS[:r]
    want = lean_pairing(ks, ss)
    check(f"A r={r}  Sygal (K|S) == seamPairing", scalar_eq(scalar(wedge(ks) | wedge(ss)), want))
    trace = CapelliOptionB.trace_coefficient(wedge(ks), wedge(ss))
    path = "strict" if trace.strict_scalar is not None else f"fallback, coeff_sum={trace.coeff_sum}"
    check(f"B r={r}  CapelliOptionB == seamPairing  [{path}]", scalar_eq(scalar(trace.final_scalar), want))


def stitched(out):
  """A single contraction panel, i.e. the two panels have been merged."""
  return is_merged_panel(out)


def section_flat():
  print("== C: flat stitching  K<(U^S) ^ K<(S^V)")
  cases = [(1, 1, 1), (1, 2, 1), (1, 1, 2), (2, 1, 1), (2, 2, 1), (2, 1, 2), (3, 1, 1), (2, 0, 1), (2, 1, 0)]
  for r, p, q in cases:
    ks, ss, us, vs = KS[:r], SS[:r], US[:p], VS[:q]
    K = wedge(ks)
    lhs = (K < wedge(us + ss)) ^ (K < wedge(ss + vs))
    want = (K | wedge(ss)) * (K < wedge(us + ss + vs))
    got = sandhi_canon(lhs)
    check(f"C r={r} |U|={p} |V|={q}  canon stitched={stitched(got)}, == Lean RHS", stitched(got) and same(got, want))
  for r, t in [(1, 2), (2, 3)]:
    ks, ss = KS[:r], SS[:t]
    K = wedge(ks)
    lhs = (K < wedge([a1] + ss)) ^ (K < wedge(ss + [b1]))
    got = sandhi_canon(lhs)
    check(f"C vanish |K|={r} |S|={t}  canon == 0", got == GExpr.Znl or same(got, GExpr.Znl))


def nest(levels, inner, wings):
  for level in reversed(levels):
    ks, w = level[0], wings(level)
    inner = wedge(ks) < (wedge(w) ^ inner if w else inner)
  return inner


def shuffle_sign(levels, ux):
  sigma = 0
  for i, (_, _, vs) in enumerate(levels):
    sigma += len(vs) * (ux + sum(len(u) for _, u, _ in levels[i + 1:]))
  return (-1) ** sigma


def section_nested():
  print("== D: nested stitching (seam at the innermost level)")
  cases = [
    ("depth2, sigma even", [([d1], [a1], [b1]), ([d2], [], [])], [], SS[:2], [c4]),
    ("depth2, sigma odd", [([d1], [a1], [b1]), ([d2], [a2], [])], [], SS[:2], [c4]),
    ("depth2, Ux, sigma odd", [([d1], [a1], [b1]), ([d2], [], [b2])], [a2], SS[:2], [c4]),
    ("depth2, grade-2 contractor", [([d1, d2], [a1], [b1]), ([d3], [], [])], [], SS[:3], [c4]),
    ("depth2, wings at both levels", [([d1], [a1], [b1]), ([d2], [a2], [b2])], [a3], SS[:2], [c4]),
    ("depth3, test1 shape", [([d1], [a1, a2], [a3, a4]), ([d2], [b1, b2], [b3, b4]), ([d3], [], [])], [], SS[:3], [c4]),
  ]
  unstitched = []
  for name, levels, ux, ss, ws in cases:
    lhs = nest(levels, wedge(ux + ss), lambda l: l[1]) ^ nest(levels, wedge(ss + ws), lambda l: l[2])
    acc = [k for ks, _, _ in levels for k in ks]
    want = shuffle_sign(levels, len(ux)) * (wedge(acc) | wedge(ss)) * nest(levels, wedge(ux + ss + ws), lambda l: l[1] + l[2])
    check(f"D {name}  Sygal expansion of LHS == Lean RHS", same(lhs, want))
    got = sandhi_canon(lhs)
    check(f"D {name}  canon output == Lean RHS", same(got, want))
    if not stitched(got):
      unstitched.append(name)
  levels = [([d1], [a1], [b1]), ([d2], [], [])]
  lhs = nest(levels, wedge(SS[:3]), lambda l: l[1]) ^ nest(levels, wedge(SS[:3] + [c4]), lambda l: l[2])
  check("D vanish |A|=2 |S|=3  Sygal expansion == 0", same(lhs, GExpr.Znl))
  if unstitched:
    notes.append(
      "sandhi_canon leaves these nested inputs unchanged (no visible seam at the outer level): "
      + "; ".join(unstitched)
    )


if __name__ == "__main__":
  only = sys.argv[1:] or ["pairing", "flat", "nested"]
  if "pairing" in only:
    section_pairing()
  if "flat" in only:
    section_flat()
  if "nested" in only:
    section_nested()
  print(f"\n{len(failures)} failure(s)")
  for f in failures:
    print("  " + f)
  for n in notes:
    print("note: " + n)
  sys.exit(1 if failures else 0)
