"""Helpers for glcntrct / sclrprdct expand regression tests."""

from __future__ import annotations

from typing import List, Optional, Tuple

from sympy import Float, Rational

from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.strategies.iters import expand_iter


def _distribute(expr):
    return GExpr.gdistribute(expr)


def iter_gadd_box_terms(expr) -> List[Tuple[object, object]]:
    """Top-level ``gadd`` of ``Box(mv, coeff)`` after distribute."""
    expr = _distribute(expr)
    if isinstance(expr, Box) and type(expr.mv) == gadd:
        args = expr.mv.args
    elif type(expr) == gadd:
        args = expr.args
    elif isinstance(expr, Box):
        return [(expr.mv, expr.coeff)]
    else:
        return [(expr, Rational(1))]

    out: List[Tuple[object, object]] = []
    for arg in args:
        if isinstance(arg, Box):
            out.append((arg.mv, arg.coeff))
        else:
            out.append((arg, Rational(1)))
    return out


def coeff_to_complex(c) -> complex:
    if c is None:
        return 1.0 + 0j
    if isinstance(c, complex) and not isinstance(c, (Rational, Float)):
        return c
    if isinstance(c, (int, float)):
        return complex(c)
    if isinstance(c, Rational):
        return complex(float(c))
    if isinstance(c, Float):
        return complex(float(c))
    try:
        from sympy import sympify

        return complex(sympify(c).evalf())
    except (TypeError, ValueError):
        raise ValueError(f"non-numeric coefficient: {c!r}")


def blade_atom_names(mv) -> List[str]:
    names: List[str] = []
    if isinstance(mv, Box):
        return blade_atom_names(mv.mv)
    if type(mv) == gextp:
        for a in mv.args:
            if isinstance(a, Box):
                names.extend(blade_atom_names(a.mv))
            elif hasattr(a, "name"):
                names.append(str(a.name))
            else:
                names.extend(blade_atom_names(a))
    elif hasattr(mv, "name") and getattr(mv, "is_atom", False):
        names.append(str(mv.name))
    return names


def missing_atom_from_blade(
    blade_atoms: Tuple[str, ...], full_atoms: Tuple[str, ...]
) -> Optional[str]:
    b_set = set(blade_atoms)
    f_set = set(full_atoms)
    if not b_set <= f_set:
        return None
    miss = f_set - b_set
    if len(miss) == 1:
        return min(miss)
    return None


def expand_panel_pipeline(panel) -> object:
    """test1–3 order: ``expand_iter(glcntrct)`` → distribute → ``sclrprdct.gexpand1``."""
    e1 = expand_iter(glcntrct)(panel)
    e2 = _distribute(e1)
    e3 = sclrprdct.gexpand1(e2)
    return _distribute(e3)


def miss_min_coeff(
    expanded,
    symdiff_names: Tuple[str, ...],
) -> Tuple[complex, int]:
    """Coeff on drop-one term with minimum missing atom name (lexicographic)."""
    best: Optional[complex] = None
    best_key: Optional[str] = None
    n_used = 0
    for mv, coeff in iter_gadd_box_terms(expanded):
        names = tuple(sorted(blade_atom_names(mv)))
        miss = missing_atom_from_blade(names, symdiff_names)
        if miss is None:
            continue
        n_used += 1
        c = coeff_to_complex(coeff)
        if best_key is None or miss < best_key:
            best_key, best = miss, c
    if best is None:
        return 0.0 + 0j, 0
    return best, n_used


def subset_sum_coeff(
    expanded,
    symdiff_names: Tuple[str, ...],
) -> Tuple[complex, int]:
    sym_set = set(symdiff_names)
    total = 0.0 + 0j
    n_used = 0
    for mv, coeff in iter_gadd_box_terms(expanded):
        names = tuple(blade_atom_names(mv))
        if set(names) <= sym_set:
            total += coeff_to_complex(coeff)
            n_used += 1
    return total, n_used


def count_sclrprdct_nodes(expr) -> int:
    n = 0
    if type(expr) == sclrprdct:
        return 1
    if isinstance(expr, Box):
        n += count_sclrprdct_nodes(expr.mv)
        if hasattr(expr, "coeff"):
            n += count_sclrprdct_nodes(expr.coeff)
        return n
    if hasattr(expr, "args"):
        return sum(count_sclrprdct_nodes(a) for a in expr.args)
    return 0
