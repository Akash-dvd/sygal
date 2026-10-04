"""Capelli Option B: overlap scalars for recursive sandhi (GA view).

Geometric-algebra role
----------------------
When `SandhiCanon.try_merge_two_contractions` hits the grade gate **x == 0**, sandhi has
aligned the contracting **up** blades and split the **down** wedges along a
shared **seam** (common factor). The merged term still needs a **scalar
coefficient**: how much the accumulated contractor overlaps that seam, including
signs from reordering wedge factors.

In GA language this module computes a scalar κ such that (at that level)

    merged_term  ∝  κ · ( blade12  <  Tsub1 )

where κ is built from:
  - **acc_blade**  — accumulated contracting blade `blade2` (= blade1 ^ blade12 ^ …)
  - **common_part** — shared down-blade factor from vichcheda (the seam)
  - **local_sign** — ±1 from `parity` when sorting `gextp` args (sign1 * sign2)

Sygal's native GA operations involved at the end:
  - **Wedge** `^`  — factors of acc / common come from `gextp` decompositions
  - **Inner product** `|`  — fallback kernel `(acc_blade | common_part)`
  - **Grade** — balanced wiring only if factor lists have equal length

Implementation layers (Brini Option B syntax, GA semantics)
-----------------------------------------------------------
C1 — Virtual wiring algebra (bookkeeping, not a second geometric product):
  - Wire each factor of acc to a factor of common through auxiliary 1-blades γᵢ
  - Rewrite wiring products using super-commutators (Grassmann signs)
  - **ad** = Lie adjoint [op, ·], i.e. push one wiring constraint through a product

C2 — Devirtualization (collapse wires to a number):
  - If all γᵢ cancel in-symbol → pure scalar
  - Else → (sum of signed wiring amplitudes) × (acc | common)

C3 — Sandhi hook (`SandhiCanon.overlap_coefficient_at_seam` only at x == 0).

This is **not** computing acc ∧ common or a meet/join directly; it is the
Capelli-style expansion of the **overlap scalar** used by sandhi, routed through
Sygal's inner product when virtual reduction does not fully close.
"""

from dataclasses import dataclass
from typing import List, Optional

from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import S
from Sygal.operators.assop.gextp import gextp


@dataclass(frozen=True)
class VirtualSymbol:
  """Auxiliary 1-blade γ used to couple acc factors to common factors.

  GA reading: a temporary **odd** vector placeholder in a wiring diagram between
  a factor of the accumulated contractor and a factor of the seam. Antisymmetric
  bookkeeping matches vector-grade anticommutation (γ ∧ γ = 0 if the same label).

  Not a physical blade in the original algebra — eliminated during devirtualization
  or folded into (acc | common).
  """
  name: str
  depth: int
  parity: int = 1  # 1 = odd (anticommuting), consistent with 1-vector grade


@dataclass(frozen=True)
class VirtualEdge:
  """Directed wire between two blade labels: left → right.

  GA reading: one **pairing** in an overlap diagram (which vector factor on the
  acc side connects to which on the common / γ side). Algebraic encoding of
  Brini's e_{left,right} before promotion to VirtualOp with parity.
  """
  left: object
  right: object


@dataclass(frozen=True)
class BalancedMonomial:
  """Balanced overlap wiring between acc and common factor lists.

  GA reading: acc and common are k-blades written as wedges of 1-blade factors
      acc  = a₁ ∧ a₂ ∧ … ∧ aₖ
      seam = c₁ ∧ c₂ ∧ … ∧ cₖ   (common_part)

  A balanced monomial pairs them through distinct γᵢ:

      creation:     aᵢ — γᵢ   for each i
      annihilation: γᵢ — cᵢ   for each i

  If k ≠ grade factor count on either side, no balanced diagram exists → coeff 0.
  Mirrors Brini: Π e_{xᵢ,γᵢ} · Π e_{γᵢ,cⱼ} with xᵢ from acc, cⱼ from common.
  """
  creation: List[VirtualEdge]
  annihilation: List[VirtualEdge]


@dataclass(frozen=True)
class VirtualOp:
  """One wiring operator e_{src,dst} with ℤ₂ parity for Grassmann signs.

  GA reading: not a geometric product in Cl(p,q); a **constraint** that src and
  dst are identified along this wire. Parity records whether src, dst behave as
  odd (vector) factors for sign flips when reordering wires — same role as
  (-1)^{grade} when swapping fermionic factors in a wedge expansion.
  """
  src: object
  dst: object
  src_parity: int
  dst_parity: int

  @property
  def parity(self) -> int:
    return (self.src_parity + self.dst_parity) % 2


@dataclass(frozen=True)
class VirtualMonomial:
  """Ordered product of wiring ops × scalar coefficient.

  GA reading: one **ordered** way to realize the overlap diagram (order matters
  for signs, like ordered wedge products before simplification). Coeff carries
  accumulated ± from virtual rewrites.
  """
  ops: List[VirtualOp]
  coeff: object = S(1)


@dataclass(frozen=True)
class VirtualExpr:
  """Sum of virtual monomials — signed alternative overlap expansions.

  GA reading: before all constraints are resolved, the overlap scalar may be a
  **sum** of diagrammatically distinct routings (analogous to a short sum of
  Clifford basis coefficients).
  """
  terms: List[VirtualMonomial]


@dataclass(frozen=True)
class BracketTraceTerm:
  """One local commutator branch when two wires share an endpoint.

  branch: "direct" | "twisted" — which δ-contraction fired in [e_ab, e_cd].
  Used for debugging / game traces, not for GA semantics directly.
  """
  branch: str
  coeff: object
  result: VirtualMonomial


@dataclass(frozen=True)
class AdTraceStep:
  """One step of pushing a wiring constraint through an ordered product.

  GA reading: Leibniz term when a derivation hits the i-th factor of an ordered
  wedge-like product of wirings; deriv_sign is the Grassmann sign from moving
  an odd operator across the prefix.
  """
  target_index: int
  target: VirtualOp
  prefix: List[VirtualOp]
  suffix: List[VirtualOp]
  left_parity_sum: int
  deriv_sign: object
  branches: List[BracketTraceTerm]


@dataclass(frozen=True)
class AdTrace:
  """Full record of ad(op) on one virtual monomial: ad(op)(M) = [op, M].

  GA reading: **Lie adjoint**, not reversion (†) or Clifford dual. Expands how one
  overlap constraint propagates through a product of pairings, producing a sum
  of monomials with explicit ± (orientation / fermionic sign).
  """
  op: VirtualOp
  input_monomial: VirtualMonomial
  steps: List[AdTraceStep]
  output_terms: List[VirtualMonomial]

  @property
  def output_expr(self) -> VirtualExpr:
    return VirtualExpr(terms=self.output_terms)


@dataclass(frozen=True)
class IteratedAdjointTrace:
  """Trace of ad(c₁)…ad(cₖ) applied to the common-side wiring product.

  GA reading: push all acc-side (creation) constraints through the seam-side
  (annihilation) wiring, in order — full Capelli expansion before scalar collapse.
  """
  creation_ops: List[VirtualOp]
  annihilation_ops: List[VirtualOp]
  ad_traces: List[AdTrace]
  result_expr: VirtualExpr


@dataclass(frozen=True)
class CapelliTrace:
  """Audit trail for one coefficient call (debug / diagram game).

  Exposes strict scalar vs fallback (acc|common), vichcheda local_sign, and
  intermediate virtual algebra — same numbers as coefficient(), with GA bookkeeping.
  """
  balanced: Optional[BalancedMonomial]
  creation_ops: List[VirtualOp]
  annihilation_ops: List[VirtualOp]
  iterated_adjoint: Optional[IteratedAdjointTrace]
  strict_scalar: Optional[object]
  coeff_sum: object
  fallback_kernel: object
  scalar_before_local_sign: object
  local_sign: object
  final_scalar: object


class CapelliOptionB:
  """Option-B overlap engine: virtual expansion → GA scalar for sandhi.

  Preferred public API
  --------------------
  overlap_scalar_at_seam(acc_blade, seam_blade, local_sign)  →  κ

  GA inputs (from SandhiCanon after DOWN vichcheda):
    acc_blade   — accumulated contractor blade2
    seam_blade  — common_part (shared down wedge factor)
    local_sign  — sign1 * sign2 from wedge parity

  Pipeline: build_seam_wiring → expand_acc_constraints_on_seam
            → project_virtual_expr_to_scalar (strict or acc|seam fallback)

  Legacy names coefficient / build_balanced_monomial / devirtualize_scalar
  remain as aliases.
  """

  @staticmethod
  def _blade_factors(blade):
    """Expand a blade into ordered 1-blade factors for wiring.

    GA: if blade is a k-vector written as gextp(a,b,…), return [a,b,…].
    Scalar 1 → []. Single vector → [blade]. Box unwraps mv only.
    """
    if isinstance(blade, Box):
      blade = blade.mv
    if blade == GExpr.Onl:
      return []
    if isinstance(blade, gextp):
      return list(blade.args)
    return [blade]

  @staticmethod
  def _make_virtuals(depth_start: int, n: int):
    """Create n auxiliary odd 1-blades γᵢ for balanced pairing."""
    return [VirtualSymbol(name=f"gamma_{depth_start+i}", depth=depth_start+i, parity=1)
            for i in range(n)]

  @staticmethod
  def _symbol_parity(symbol) -> int:
    """ℤ₂ parity of a wire endpoint for Grassmann sign rules.

    Virtual γ and Sygal vector atoms are treated as odd (grade 1) so that
    super-commutators reproduce wedge antisymmetry signs in the wiring algebra.
    """
    if isinstance(symbol, VirtualSymbol):
      return symbol.parity
    return 1

  @staticmethod
  def _edge_to_op(edge: VirtualEdge) -> VirtualOp:
    """Promote a diagram edge to VirtualOp with correct parities."""
    return VirtualOp(
      src=edge.left,
      dst=edge.right,
      src_parity=CapelliOptionB._symbol_parity(edge.left),
      dst_parity=CapelliOptionB._symbol_parity(edge.right),
    )

  @staticmethod
  def build_balanced_monomial(acc_blade, common_part):
    """Build γ-mediated wiring between acc and common factor lists.

    GA: requires the same number of 1-blade factors on both sides (same k for
    acc and seam as wedges of vectors). Otherwise overlap pattern is undefined → None.

    Diagram (k=3):

        a₁ ── γ₀ ── c₁
        a₂ ── γ₁ ── c₂     acc factors aᵢ, common factors cᵢ
        a₃ ── γ₂ ── c₃
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
  def _super_bracket_with_trace(a: VirtualOp, b: VirtualOp) -> List[BracketTraceTerm]:
    """Super-commutator [a,b] on wiring basis elements.

    Lie algebra of virtual pairings (Grassmann-Cayley bookkeeping):

        [e_{a,b}, e_{c,d}] = δ_{b,c} e_{a,d}
                           - (-1)^{|ab||cd|} δ_{a,d} e_{c,b}

    GA: when two wirings share an intermediate label (often γ), fuse them;
    the twisted term is the antisymmetric exchange with graded sign.
    """
    out = []
    # δ_{b,c}: shared inner endpoint → fuse wires a—b and b—d into a—d
    if a.dst == b.src:
      out.append(BracketTraceTerm(
        branch="direct",
        coeff=S(1),
        result=VirtualMonomial(
          ops=[VirtualOp(a.src, b.dst, a.src_parity, b.dst_parity)],
          coeff=S(1),
        ),
      )
      )
    # δ_{a,d}: exchange route with (-1)^{|a||b|} (vector-grade sign)
    if a.src == b.dst:
      phase = (-1) ** (a.parity * b.parity)
      out.append(BracketTraceTerm(
        branch="twisted",
        coeff=-S(1) * phase,
        result=VirtualMonomial(
          ops=[VirtualOp(b.src, a.dst, b.src_parity, a.dst_parity)],
          coeff=-S(1) * phase,
        ),
      )
      )
    return out

  @staticmethod
  def _super_bracket(a: VirtualOp, b: VirtualOp) -> List[VirtualMonomial]:
    return [branch.result for branch in CapelliOptionB._super_bracket_with_trace(a, b)]

  @staticmethod
  def _multiply_prefix_suffix(prefix: List[VirtualOp], mid: VirtualMonomial, suffix: List[VirtualOp], coeff):
    """Insert a rewritten middle factor into an ordered wiring product."""
    return VirtualMonomial(ops=[*prefix, *mid.ops, *suffix], coeff=coeff * mid.coeff)

  @staticmethod
  def _ad(op: VirtualOp, monomial: VirtualMonomial) -> VirtualExpr:
    """ad(op)(M) = [op, M] on one monomial; return as VirtualExpr."""
    return CapelliOptionB._ad_with_trace(op, monomial).output_expr

  @staticmethod
  def _ad_with_trace(op: VirtualOp, monomial: VirtualMonomial) -> AdTrace:
    """Graded derivation ad(op) on ordered wiring product.

    GA: analogous to applying a derivation through an ordered wedge product —
    hit each factor with [op, ·], carry prefix/suffix, multiply by (-1)^{|op||prefix|}
    when op is odd and crosses odd factors (deriv_sign).

    Empty monomial → zero contribution.
    """
    if len(monomial.ops) == 0:
      return AdTrace(
        op=op,
        input_monomial=monomial,
        steps=[],
        output_terms=[],
      )
    out_terms = []
    trace_steps = []
    prefix = []
    left_parity_sum = 0
    for idx, target in enumerate(monomial.ops):
      brackets = CapelliOptionB._super_bracket_with_trace(op, target)
      if not brackets:
        # op does not interact with this factor; commute past it
        prefix.append(target)
        left_parity_sum = (left_parity_sum + target.parity) % 2
        continue
      # Grassmann sign for moving op across prefix factors
      deriv_sign = (-1) ** (op.parity * left_parity_sum)
      suffix = monomial.ops[idx + 1:]
      step_branches = []
      for branch in brackets:
        multiplied = CapelliOptionB._multiply_prefix_suffix(
            prefix=prefix,
            mid=branch.result,
            suffix=suffix,
            coeff=monomial.coeff * deriv_sign,
          )
        out_terms.append(multiplied)
        step_branches.append(
          BracketTraceTerm(
            branch=branch.branch,
            coeff=branch.coeff,
            result=multiplied,
          )
        )
      trace_steps.append(
        AdTraceStep(
          target_index=idx,
          target=target,
          prefix=list(prefix),
          suffix=list(suffix),
          left_parity_sum=left_parity_sum,
          deriv_sign=deriv_sign,
          branches=step_branches,
        )
      )
      prefix.append(target)
      left_parity_sum = (left_parity_sum + target.parity) % 2
    return AdTrace(
      op=op,
      input_monomial=monomial,
      steps=trace_steps,
      output_terms=out_terms,
    )

  @staticmethod
  def _iterated_adjoint(creation_ops: List[VirtualOp], annihilation_ops: List[VirtualOp]) -> VirtualExpr:
    return CapelliOptionB._iterated_adjoint_with_trace(creation_ops, annihilation_ops).result_expr

  @staticmethod
  def _iterated_adjoint_with_trace(creation_ops: List[VirtualOp], annihilation_ops: List[VirtualOp]) -> IteratedAdjointTrace:
    """Apply ad(c₁)…ad(cₖ) to the product of common-side wirings.

    GA: enforce acc-side constraints (creation) on the seam-side wiring product
    (annihilation), one after another — full Capelli / virtual overlap expansion
    before extracting a scalar.
    """
    expr = VirtualExpr(terms=[VirtualMonomial(ops=annihilation_ops, coeff=S(1))])
    ad_traces = []
    for cop in reversed(creation_ops):
      next_terms = []
      for mon in expr.terms:
        ad_trace = CapelliOptionB._ad_with_trace(cop, mon)
        ad_traces.append(ad_trace)
        next_terms.extend(ad_trace.output_terms)
      expr = VirtualExpr(terms=next_terms)
    return IteratedAdjointTrace(
      creation_ops=list(creation_ops),
      annihilation_ops=list(annihilation_ops),
      ad_traces=ad_traces,
      result_expr=expr,
    )

  @staticmethod
  def _devirtualize_virtual_expr(expr: VirtualExpr) -> Optional[object]:
    """If all γ / wiring cancelled, return the pure scalar sum.

    GA: algebraic closure — overlap reduced to a number with no blade labels left.
    If any wiring remains, return None (need Capelli fallback with inner product).
    """
    if not expr.terms:
      return S(0)
    if all(len(t.ops) == 0 for t in expr.terms):
      return sum((t.coeff for t in expr.terms), S(0))
    return None

  @staticmethod
  def _capelli_map(expr: VirtualExpr, acc_blade, common_part):
    """Collapse virtual expansion to a GA scalar.

    1) Strict: all wires gone → sum of monomial coefficients.
    2) Fallback: amplitude_sum × (acc_blade | common_part) using Sygal inner product.

    GA: (acc | common) is the **scalar part of the inner product** of the two
    blades — the natural Sygal encoding of overlap magnitude when the virtual
    expansion does not fully simplify in the wiring algebra alone.
    """
    strict_scalar = CapelliOptionB._devirtualize_virtual_expr(expr)
    if strict_scalar is not None:
      return strict_scalar

    coeff_sum = sum((t.coeff for t in expr.terms), S(0))
    if coeff_sum == S(0):
      return S(0)
    return coeff_sum * (acc_blade | common_part)

  @staticmethod
  def _trace_capelli_map(expr: VirtualExpr, acc_blade, common_part):
    """Same as _capelli_map but split strict vs fallback for CapelliTrace."""
    strict_scalar = CapelliOptionB._devirtualize_virtual_expr(expr)
    coeff_sum = sum((t.coeff for t in expr.terms), S(0))
    fallback_kernel = acc_blade | common_part
    if strict_scalar is not None:
      return strict_scalar, strict_scalar, coeff_sum, fallback_kernel
    if coeff_sum == S(0):
      return S(0), None, coeff_sum, fallback_kernel
    return coeff_sum * fallback_kernel, None, coeff_sum, fallback_kernel

  @staticmethod
  def devirtualize_scalar(acc_blade, common_part, balanced: Optional[BalancedMonomial] = None):
    """C2: balanced wiring → iterated ad → scalar (strict or acc|common).

    GA shortcuts:
      common_part == 1  → no seam, scalar 1
      balanced is None  → grade/factor mismatch, scalar 0
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
    """Sandhi overlap coefficient at one merge level (x == 0 only).

    GA output: scalar κ = overlap(acc, common) × local_sign, where
      overlap is computed via Option-B virtual expansion + (acc | common) fallback,
      local_sign encodes wedge reordering from vichcheda (± from parity).

    Prefer overlap_scalar_at_seam(); alias of this method.
    """
    balanced = CapelliOptionB.build_balanced_monomial(acc_blade, common_part)
    scalar = CapelliOptionB.devirtualize_scalar(acc_blade, common_part, balanced)
    return scalar * local_sign

  @staticmethod
  def overlap_scalar_at_seam(acc_blade, seam_blade, local_sign=S(1)):
    """Primary name: overlap scalar κ at seam (x == 0 sandhi level)."""
    return CapelliOptionB.coefficient(acc_blade, seam_blade, local_sign)

  @staticmethod
  def trace_coefficient(acc_blade, common_part, local_sign=S(1)) -> CapelliTrace:
    """coefficient() plus full expansion trace (sign branches, strict vs fallback).

    Same κ as coefficient(); use for debugging, tests, or diagram-game UX.
    """
    balanced = CapelliOptionB.build_balanced_monomial(acc_blade, common_part)
    if common_part == GExpr.Onl:
      scalar_before_local_sign = S(1)
      return CapelliTrace(
        balanced=balanced,
        creation_ops=[],
        annihilation_ops=[],
        iterated_adjoint=None,
        strict_scalar=S(1),
        coeff_sum=S(1),
        fallback_kernel=S(1),
        scalar_before_local_sign=scalar_before_local_sign,
        local_sign=local_sign,
        final_scalar=scalar_before_local_sign * local_sign,
      )

    if balanced is None:
      return CapelliTrace(
        balanced=None,
        creation_ops=[],
        annihilation_ops=[],
        iterated_adjoint=None,
        strict_scalar=None,
        coeff_sum=S(0),
        fallback_kernel=S(0),
        scalar_before_local_sign=S(0),
        local_sign=local_sign,
        final_scalar=S(0),
      )

    creation_ops = [CapelliOptionB._edge_to_op(e) for e in balanced.creation]
    annihilation_ops = [CapelliOptionB._edge_to_op(e) for e in balanced.annihilation]
    iterated = CapelliOptionB._iterated_adjoint_with_trace(creation_ops, annihilation_ops)
    scalar_before_local_sign, strict_scalar, coeff_sum, fallback_kernel = (
      CapelliOptionB._trace_capelli_map(iterated.result_expr, acc_blade, common_part)
    )
    return CapelliTrace(
      balanced=balanced,
      creation_ops=creation_ops,
      annihilation_ops=annihilation_ops,
      iterated_adjoint=iterated,
      strict_scalar=strict_scalar,
      coeff_sum=coeff_sum,
      fallback_kernel=fallback_kernel,
      scalar_before_local_sign=scalar_before_local_sign,
      local_sign=local_sign,
      final_scalar=scalar_before_local_sign * local_sign,
    )

  # --- Semantic aliases -------------------------------------------------------
  build_seam_wiring = build_balanced_monomial
  collapse_wiring_to_scalar = devirtualize_scalar
  expand_acc_constraints_on_seam = _iterated_adjoint
  expand_acc_constraints_on_seam_traced = _iterated_adjoint_with_trace
  commutator_on_wiring = _super_bracket
  lie_derivation_on_wiring = _ad
  project_virtual_expr_to_scalar = _capelli_map
