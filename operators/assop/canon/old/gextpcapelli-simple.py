"""Option-B Capelli helpers for recursive sandhi.

This module now contains two concrete layers required by paper-style Option B:

1) C1 - Virtual algebra execution layer
   - graded virtual operators e_{a,b}
   - super-commutator [e_{a,b}, e_{c,d}]
   - adjoint-action over operator products (super-derivation)

2) C2 - Devirtualization core
   - iterated adjoint expansion for balanced monomials
   - projection hook from virtual expression to Sygal scalar coefficient

For canonical sandhi (C3), coefficient evaluation is routed through this C2
path only (no direct scalar-product callsite fallback in `gextpcanon`).
"""

from dataclasses import dataclass
from typing import List, Optional

from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import S
from Sygal.operators.assop.gextp import gextp


@dataclass(frozen=True)
class VirtualSymbol:
  """Auxiliary variable γ_d used at recursion depth d.

  parity:
    1 = odd (anticommuting), used by the theoretical model.
    In current integration, parity is retained in structure; coefficient
    extraction still devirtualizes through Sygal scalar product.
  """
  name: str
  depth: int
  parity: int = 1


@dataclass(frozen=True)
class VirtualEdge:
  """One virtual creation/annihilation edge e_{left,right}."""
  left: object
  right: object


@dataclass(frozen=True)
class BalancedMonomial:
  """Balanced monomial: creation part times annihilation part.

  This mirrors Brini's balanced monomial pattern:
  Π e_{x_i,γ_i} · Π e_{γ_i,x_j}
  """
  creation: List[VirtualEdge]
  annihilation: List[VirtualEdge]

@dataclass(frozen=True)
class VirtualOp:
  """Virtual operator e_{src,dst} with explicit Z2-parity metadata."""
  src: object
  dst: object
  src_parity: int
  dst_parity: int

  @property
  def parity(self) -> int:
    return (self.src_parity + self.dst_parity) % 2

@dataclass(frozen=True)
class VirtualMonomial:
  """Ordered product of virtual operators with scalar coefficient."""
  ops: List[VirtualOp]
  coeff: object = S(1)

@dataclass(frozen=True)
class VirtualExpr:
  """Sum of virtual monomials."""
  terms: List[VirtualMonomial]


class CapelliOptionB:
  """Minimal Option-B engine used by gextpcanon.

  Notes:
  - We explicitly build a balanced-monomial representation from
    (accumulated_blade, common_part).
  - Devirtualization currently maps to Sygal scalar product `(A|B)`.
    This preserves current runtime behavior while giving a direct place
    to evolve into a full virtual-algebra backend later.
  """

  @staticmethod
  def _blade_factors(blade):
    # Accept both raw multivectors and boxed multivectors.
    if isinstance(blade, Box):
      blade = blade.mv
    if blade == GExpr.Onl:
      return []
    if isinstance(blade, gextp):
      return list(blade.args)
    return [blade]

  @staticmethod
  def _make_virtuals(depth_start: int, n: int):
    return [VirtualSymbol(name=f"gamma_{depth_start+i}", depth=depth_start+i, parity=1)
            for i in range(n)]

  @staticmethod
  def _symbol_parity(symbol) -> int:
    """Parity convention for virtual execution layer.

    - Virtual symbols are odd by definition.
    - Proper Sygal symbols are treated as odd in this Option-B layer so
      super-commutator signs match Grassmann-Cayley style antisymmetry.
    """
    if isinstance(symbol, VirtualSymbol):
      return symbol.parity
    return 1

  @staticmethod
  def _edge_to_op(edge: VirtualEdge) -> VirtualOp:
    return VirtualOp(
      src=edge.left,
      dst=edge.right,
      src_parity=CapelliOptionB._symbol_parity(edge.left),
      dst_parity=CapelliOptionB._symbol_parity(edge.right),
    )

  @staticmethod
  def build_balanced_monomial(acc_blade, common_part):
    """Build balanced monomial for this recursion level.

    We pair factors of accumulated blade and common part through virtual symbols.
    If grades do not match, no valid balanced monomial exists.
    """
    left = CapelliOptionB._blade_factors(acc_blade)
    right = CapelliOptionB._blade_factors(common_part)
    if len(left) != len(right):
      return None

    gammas = CapelliOptionB._make_virtuals(depth_start=0, n=len(left))
    creation = [VirtualEdge(left=l, right=g) for l, g in zip(left, gammas)]
    annihilation = [VirtualEdge(left=g, right=r) for g, r in zip(gammas, right)]
    return BalancedMonomial(creation=creation, annihilation=annihilation)

  @staticmethod
  def _super_bracket(a: VirtualOp, b: VirtualOp) -> List[VirtualMonomial]:
    """Compute [a,b] in gl-superalgebra basis form.

    [e_{a,b}, e_{c,d}] = delta_{b,c} e_{a,d}
                        - (-1)^{|e_ab||e_cd|} delta_{a,d} e_{c,b}
    """
    out = []
    # First term: delta_{b,c} e_{a,d}
    if a.dst == b.src:
      out.append(
        VirtualMonomial(
          ops=[VirtualOp(a.src, b.dst, a.src_parity, b.dst_parity)],
          coeff=S(1),
        )
      )
    # Second term with graded sign.
    if a.src == b.dst:
      phase = (-1) ** (a.parity * b.parity)
      out.append(
        VirtualMonomial(
          ops=[VirtualOp(b.src, a.dst, b.src_parity, a.dst_parity)],
          coeff=-S(1) * phase,
        )
      )
    return out

  @staticmethod
  def _multiply_prefix_suffix(prefix: List[VirtualOp], mid: VirtualMonomial, suffix: List[VirtualOp], coeff):
    return VirtualMonomial(ops=[*prefix, *mid.ops, *suffix], coeff=coeff * mid.coeff)

  @staticmethod
  def _ad(op: VirtualOp, monomial: VirtualMonomial) -> VirtualExpr:
    """Adjoint action ad(op)(monomial) as graded derivation."""
    if len(monomial.ops) == 0:
      return VirtualExpr(terms=[])
    out_terms = []
    prefix = []
    left_parity_sum = 0
    for idx, target in enumerate(monomial.ops):
      brackets = CapelliOptionB._super_bracket(op, target)
      if not brackets:
        prefix.append(target)
        left_parity_sum = (left_parity_sum + target.parity) % 2
        continue
      # Super-derivation sign while moving `op` across prefix.
      deriv_sign = (-1) ** (op.parity * left_parity_sum)
      suffix = monomial.ops[idx + 1:]
      for bterm in brackets:
        out_terms.append(
          CapelliOptionB._multiply_prefix_suffix(
            prefix=prefix,
            mid=bterm,
            suffix=suffix,
            coeff=monomial.coeff * deriv_sign,
          )
        )
      prefix.append(target)
      left_parity_sum = (left_parity_sum + target.parity) % 2
    return VirtualExpr(terms=out_terms)

  @staticmethod
  def _iterated_adjoint(creation_ops: List[VirtualOp], annihilation_ops: List[VirtualOp]) -> VirtualExpr:
    """Compute ad(c1)...ad(ck)(annihilation_product)."""
    expr = VirtualExpr(terms=[VirtualMonomial(ops=annihilation_ops, coeff=S(1))])
    for cop in reversed(creation_ops):
      next_terms = []
      for mon in expr.terms:
        next_terms.extend(CapelliOptionB._ad(cop, mon).terms)
      expr = VirtualExpr(terms=next_terms)
    return expr

  @staticmethod
  def _devirtualize_virtual_expr(expr: VirtualExpr) -> Optional[object]:
    """Project virtual expression to scalar if fully devirtualized.

    Current strict rule:
    - if every resulting monomial has no operators, sum coefficients;
    - otherwise return None (caller may use compatibility fallback).
    """
    if not expr.terms:
      return S(0)
    if all(len(t.ops) == 0 for t in expr.terms):
      return sum((t.coeff for t in expr.terms), S(0))
    return None

  @staticmethod
  def _capelli_map(expr: VirtualExpr, acc_blade, common_part):
    """Project virtual expression through a Capelli-style map surrogate.

    Rules:
    - Fully reduced scalar terms (no ops) contribute directly as coefficients.
    - Partially reduced terms are projected through a structural scalar kernel
      `(acc_blade | common_part)` with summed virtual coefficients.

    This keeps coefficient evaluation inside the C2 pipeline while remaining
    compatible with current Sygal operator representation.
    """
    strict_scalar = CapelliOptionB._devirtualize_virtual_expr(expr)
    if strict_scalar is not None:
      return strict_scalar

    # Coefficient carrier from virtual expression amplitudes.
    coeff_sum = sum((t.coeff for t in expr.terms), S(0))
    if coeff_sum == S(0):
      return S(0)
    return coeff_sum * (acc_blade | common_part)

  @staticmethod
  def devirtualize_scalar(acc_blade, common_part, balanced: Optional[BalancedMonomial] = None):
    """Capelli devirtualization with adjoint-action core.

    C2 core:
    - Build virtual operator products from balanced monomial.
    - Run iterated adjoint action.
    - Project through Capelli-style map.
    """
    if common_part == GExpr.Onl:
      return S(1)
    if balanced is None:
      balanced = CapelliOptionB.build_balanced_monomial(acc_blade, common_part)

    if balanced is not None:
      creation_ops = [CapelliOptionB._edge_to_op(e) for e in balanced.creation]
      annihilation_ops = [CapelliOptionB._edge_to_op(e) for e in balanced.annihilation]
      vexpr = CapelliOptionB._iterated_adjoint(creation_ops, annihilation_ops)
      return CapelliOptionB._capelli_map(vexpr, acc_blade, common_part)

    return S(0)

  @staticmethod
  def coefficient(acc_blade, common_part, local_sign=S(1)):
    """Return this-level Option-B coefficient.

    local_sign carries structural orientation from vichcheda ordering in
    `gextpcanon` (sign1*sign2). The balanced monomial is still built so the
    Option-B representation is explicit and inspectable.
    """
    balanced = CapelliOptionB.build_balanced_monomial(acc_blade, common_part)
    scalar = CapelliOptionB.devirtualize_scalar(acc_blade, common_part, balanced)
    return scalar * local_sign

