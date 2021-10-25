"""Strategies to Traverse a Tree."""
from __future__ import print_function, division

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.GExpr import GExpr 
from libs.Sygal.Box import Box 

from sympy.strategies.util import basic_fns
from sympy.strategies.core import chain, do_one


def top_down(rule, fns=basic_fns):
    """Apply a rule down a tree running it on the top nodes first."""
    return chain(rule, lambda expr: bxsall(top_down(rule, fns), fns)(expr))


def bottom_up(rule, fns=basic_fns):
    """Apply a rule down a tree running it on the bottom nodes first."""
    return chain(lambda expr: bxsall(bottom_up(rule, fns), fns)(expr), rule)


def top_down_once(rule, fns=basic_fns):
    """Apply a rule down a tree - stop on success."""
    return do_one(rule, lambda expr: bxsall(top_down(rule, fns), fns)(expr))


def bottom_up_once(rule, fns=basic_fns):
    """Apply a rule up a tree - stop on success."""
    return do_one(lambda expr: bxsall(bottom_up(rule, fns), fns)(expr), rule)


def bxsall(rule, fns=basic_fns):
    """Strategic all - apply rule to args."""
    op, new, children, leaf = map(fns.get, ('op', 'new', 'children', 'leaf'))

    def all_rl(expr):
        if leaf(expr):
            return expr
        else:
            new = op(expr).__new__
            fct1 = issubclass(type(expr), Expr)
            fct2 = issubclass(type(expr), GExpr)
            fct3 = issubclass(type(expr), Box)
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
            

    return all_rl
