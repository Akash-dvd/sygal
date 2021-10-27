"""Strategies to Traverse a Tree."""
from __future__ import print_function, division

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.GExpr import GExpr 
from libs.Sygal.Box import Box 

from libs.Sygal.strategies.util import gen_traverse,spe_traverse
from libs.Sygal.strategies.core import chain, do_one


def top_down(rule, fns=gen_traverse):
    """Apply a rule down a tree running it on the top nodes first."""
    return chain(rule, lambda expr: bxsall(top_down(rule, fns), fns)(expr))


def bottom_up(rule, fns=gen_traverse):
    """Apply a rule down a tree running it on the bottom nodes first."""
    return chain(lambda expr: bxsall(bottom_up(rule, fns), fns)(expr), rule)


def top_down_once(rule, fns=gen_traverse):
    """Apply a rule down a tree - stop on success."""
    return do_one(rule, lambda expr: bxsall(top_down(rule, fns), fns)(expr))


def bottom_up_once(rule, fns=gen_traverse):
    """Apply a rule up a tree - stop on success."""
    return do_one(lambda expr: bxsall(bottom_up(rule, fns), fns)(expr), rule)


def bxsall(rule, fns=gen_traverse):
    """Strategic all - apply rule to args."""
    op, new, children, leaf,coeff_flag = map(fns.get, ('op', 'new', 'children', 'leaf','coeff_flag'))

    def all_rl(expr):
        if leaf(expr):
            return expr
        else:
            # Here Box -> Box , GExpr -> GExpr , Expr -> Expr
            new = op(expr).__new__
            fct1 = issubclass(type(expr), Expr)
            fct2 = issubclass(type(expr), GExpr)
            fct3 = issubclass(type(expr), Box)
            if coeff_flag :
                if(fct3):
                    args = map(rule, children(expr))
                    argsmv = next(args)
                    argscoeff = next(args)
                    if(type(argscoeff)==Box):
                        m_argscoeff = argscoeff.coeff
                        if(argscoeff.mv != GExpr.nl):
                            raise
                    else :
                        m_argscoeff = argscoeff
                    m_args = (argsmv , m_argscoeff)    
                    return new(op(expr), *m_args)
                elif (fct2):
                    args = map(rule, children(expr))
                    t = new(op(expr), *args)
                    if(type(t)!=Box):
                        raise
                    else:
                        # CHANGED HERE
                        if(t.mv==GExpr.nl):
                            return t.coeff
                        else:
                            return t.mv
                else :
                    # fct1
                    args = map(rule, children(expr))
                    m_args = []
                    
                    for arg in args:
                        ifct1 = issubclass(type(arg), Expr)
                        ifct2 = issubclass(type(arg), GExpr)
                        ifct3 = issubclass(type(arg), Box)
                        if(ifct3):
                            bx = arg
                            argsmv = bx.mv
                            argscoeff = bx.coeff
                            m_args.append(argscoeff)
                            if(argsmv!=GExpr.nl):
                                raise
                        else :
                            m_args.append(arg)
                            # CHANGED HERE
                        # elif (ifct2):
                        #     # How did you reach here
                        #     # ANS -> Add with 0 grade <
                        #     m_args.append(arg)
                        
                        # else :
                        #     # ifct1
                        #     m_args.append(arg)

                    return new(op(expr), *m_args)
            else :
                if(fct3):
                    argsmv = next(map(rule, expr.args[:1]))
                    argscoeff = expr.coeff
                    if(type(argsmv)==Box):
                        m_argsmv = argsmv.mv
                    else :
                        m_argsmv = argsmv
                    m_args = (m_argsmv , argscoeff)    
                    return new(op(expr), *m_args)
                elif (fct2):
                    args = map(rule, children(expr))
                    t = new(op(expr), *args)
                    if(type(t)!=Box):
                        raise
                    else:
                        # CHANGED HERE
                        if(t.mv==GExpr.nl):
                            return t.coeff
                        else:
                            return t.mv
                else :
                    # fct1
                    raise

    return all_rl
