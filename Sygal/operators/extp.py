from collections import defaultdict
from functools import cmp_to_key
import operator

from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters

from libs.Sygal.GExpr import GExpr
# internal marker to indicate:
#   "there are still non-commutative objects -- don't forget to process them"
class NC_Marker:
  is_Order = False
  is_Mul = False
  is_Number = False
  is_Poly = False

  is_commutative = False


# Key for sorting commutative args in canonical order
_args_sortkey = cmp_to_key(Basic.compare)
def _mulsort(args):
  # in-place sorting of args
  args.sort(key=_args_sortkey)


def _unevaluated_Mul(*args):
  """Return a well-formed unevaluated Mul: Numbers are collected and
  put in slot 0, any arguments that are Muls will be flattened, and args
  are sorted. Use this when args have changed but you still want to return
  an unevaluated Mul.

  Examples
  ========

  >>> from sympy.core.mul import _unevaluated_Mul as uMul
  >>> from sympy import S, sqrt, Mul
  >>> from sympy.abc import x
  >>> a = uMul(*[S(3.0), x, S(2)])
  >>> a.args[0]
  6.00000000000000
  >>> a.args[1]
  x

  Two unevaluated Muls with the same arguments will
  always compare as equal during testing:

  >>> m = uMul(sqrt(2), sqrt(3))
  >>> m == uMul(sqrt(3), sqrt(2))
  True
  >>> u = Mul(sqrt(3), sqrt(2), evaluate=False)
  >>> m == uMul(u)
  True
  >>> m == Mul(*m.args)
  False

  """
  args = list(args)
  newargs = []
  ncargs = []
  co = S.One
  while args:
    a = args.pop()
    if a.is_Mul:
      c, nc = a.args_cnc()
      args.extend(c)
      if nc:
        ncargs.append(Mul._from_args(nc))
    elif a.is_Number:
      co *= a
    else:
      newargs.append(a)
  _mulsort(newargs)
  if co is not S.One:
    newargs.insert(0, co)
  if ncargs:
    newargs.append(Mul._from_args(ncargs))
  return Mul._from_args(newargs)


class extp(GExpr, AssocOp):

  __slots__ = ()
  identity = S(1)
  _args_type = Expr
  
  @property
  def grade(self):
    sum = 0
    for elem in self.args:
      sum += elem.grade
    return sum


  def __neg__(self):
    c, args = self.as_coeff_mul()
    c = -c
    if c is not S.One:
      if args[0].is_Number:
        args = list(args)
        if c is S.NegativeOne:
          args[0] = -args[0]
        else:
          args[0] *= c
      else:
        args = (c,) + args
    return self._from_args(args, self.is_commutative)

  @classmethod
  def flatten(cls, seq):
    rv = None


    coeff = S.Zero  # coefficient (Number or zoo) to always be in slot 0
                    # e.g. 3 + ...
    order_factors = []

    extra = []
    for o in seq:
      if o.is_Number:
        if (o is S.NaN or coeff is S.ComplexInfinity and
          o.is_finite is False) and not extra:
              # we know for sure the result will be nan
          return [S.NaN], [], None
        if coeff.is_Number or isinstance(coeff, AccumBounds):
          coeff += o
          if coeff is S.NaN and not extra:
                  # we know for sure the result will be nan
            return [S.NaN], [], None
          continue


        # Add([...])
      elif isinstance(o, cls):
    #  THIS RMOVAL IS VERY EDGYY
        seq.remove(o)
        # NB: here we assume Add is always commutative
        seq.extend(o.args)  # TODO zerocopy?
        continue

      else:
            # everything else
        c = S.One
        s = o
    if ((len(seq)-len(set(seq))) == 0):    
      newseq = cls.sort_seq(seq)
      return [], newseq, None
    else :
      return [],[S(0)],None
  @classmethod
  def sort_seq(cls,seq):
    seq1 = []
    for elem in seq:
      if isinstance(elem,GExpr):
        if elem.is_atom:
          seq1.append(elem)
    seq2 = []
    for elem in seq:
      if isinstance(elem,GExpr):
        if not elem.is_atom:
          seq2.append(elem)

    newseq = sorted(seq1, 
    key=lambda name: name.name)
    
    newseq.extend(seq2)
    
    return newseq


  def __str__(self):
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'^'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self):
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.__hash__() == other.__hash__()
    )
  
  @classmethod
  def class_key(cls):
    # return 3, 0, cls.__name__
    raise 

  def _eval_evalf(self, prec):
    c, m = self.as_coeff_Mul()
    if c is S.NegativeOne:
      if m.is_Mul:
        rv = -AssocOp._eval_evalf(m, prec)
      else:
        mnew = m._eval_evalf(prec)
        if mnew is not None:
          m = mnew
        rv = -m
    else:
      rv = AssocOp._eval_evalf(self, prec)
    if rv.is_number:
      return rv.expand()
    return rv

  @cacheit
  def as_two_terms(self):
    """Return head and tail of self.

    This is the most efficient way to get the head and tail of an
    expression.

    - if you want only the head, use self.args[0];
    - if you want to process the arguments of the tail then use
      self.as_coef_mul() which gives the head and a tuple containing
      the arguments of the tail when treated as a Mul.
    - if you want the coefficient when self is treated as an Add
      then use self.as_coeff_add()[0]

    >>> from sympy.abc import x, y
    >>> (3*x*y).as_two_terms()
    (3, x*y)
    """
    args = self.args

    if len(args) == 1:
      return S.One, self
    elif len(args) == 2:
      return args

    else:
      return args[0], self._new_rawargs(*args[1:])

  @cacheit
  def as_coefficients_dict(self):
    """Return a dictionary mapping terms to their coefficient.
    Since the dictionary is a defaultdict, inquiries about terms which
    were not present will return a coefficient of 0. The dictionary
    is considered to have a single term.

    Examples
    ========

    >>> from sympy.abc import a, x
    >>> (3*a*x).as_coefficients_dict()
    {a*x: 3}
    >>> _[a]
    0
    """

    d = defaultdict(int)
    args = self.args

    if len(args) == 1 or not args[0].is_Number:
      d[self] = S.One
    else:
      d[self._new_rawargs(*args[1:])] = args[0]

    return d

  @cacheit
  def as_coeff_mul(self, *deps, **kwargs):
    if deps:
      from sympy.utilities.iterables import sift
      l1, l2 = sift(self.args, lambda x: x.has(*deps), binary=True)
      return self._new_rawargs(*l2), tuple(l1)
    rational = kwargs.pop('rational', True)
    args = self.args
    if args[0].is_Number:
      if not rational or args[0].is_Rational:
        return args[0], args[1:]
      elif args[0].is_extended_negative:
        return S.NegativeOne, (-args[0],) + args[1:]
    return S.One, args

  def as_coeff_Mul(self, rational=False):
    """
    Efficiently extract the coefficient of a product.
    """
    coeff, args = self.args[0], self.args[1:]

    if coeff.is_Number:
      if not rational or coeff.is_Rational:
        if len(args) == 1:
          return coeff, args[0]
        else:
          return coeff, self._new_rawargs(*args)
      elif coeff.is_extended_negative:
        return S.NegativeOne, self._new_rawargs(*((-coeff,) + args))
    return S.One, self

  def _matches_simple(self, expr, repl_dict):
    # handle (w*3).matches('x*5') -> {w: x*5/3}
    coeff, terms = self.as_coeff_Mul()
    terms = Mul.make_args(terms)
    if len(terms) == 1:
      newexpr = self.__class__._combine_inverse(expr, coeff)
      return terms[0].matches(newexpr, repl_dict)
    return

  def matches(self, expr, repl_dict={}, old=False):
    expr = sympify(expr)
    repl_dict = repl_dict.copy()
    if self.is_commutative and expr.is_commutative:
      return self._matches_commutative(expr, repl_dict, old)
    elif self.is_commutative is not expr.is_commutative:
      return None

    # Proceed only if both both expressions are non-commutative
    c1, nc1 = self.args_cnc()
    c2, nc2 = expr.args_cnc()
    c1, c2 = [c or [1] for c in [c1, c2]]

    # TODO: Should these be self.func?
    comm_mul_self = Mul(*c1)
    comm_mul_expr = Mul(*c2)

    repl_dict = comm_mul_self.matches(comm_mul_expr, repl_dict, old)

    # If the commutative arguments didn't match and aren't equal, then
    # then the expression as a whole doesn't match
    if repl_dict is None and c1 != c2:
      return None

    # Now match the non-commutative arguments, expanding powers to
    # multiplications
    nc1 = Mul._matches_expand_pows(nc1)
    nc2 = Mul._matches_expand_pows(nc2)

    repl_dict = Mul._matches_noncomm(nc1, nc2, repl_dict)

    return repl_dict or None

  @staticmethod
  def _matches_expand_pows(arg_list):
    new_args = []
    for arg in arg_list:
      if arg.is_Pow and arg.exp > 0:
        new_args.extend([arg.base] * arg.exp)
      else:
        new_args.append(arg)
    return new_args

  @staticmethod
  def _matches_noncomm(nodes, targets, repl_dict={}):
    """Non-commutative multiplication matcher.

    `nodes` is a list of symbols within the matcher multiplication
    expression, while `targets` is a list of arguments in the
    multiplication expression being matched against.
    """
    repl_dict = repl_dict.copy()
    # List of possible future states to be considered
    agenda = []
    # The current matching state, storing index in nodes and targets
    state = (0, 0)
    node_ind, target_ind = state
    # Mapping between wildcard indices and the index ranges they match
    wildcard_dict = {}
    repl_dict = repl_dict.copy()

    while target_ind < len(targets) and node_ind < len(nodes):
      node = nodes[node_ind]

      if node.is_Wild:
        Mul._matches_add_wildcard(wildcard_dict, state)

      states_matches = Mul._matches_new_states(wildcard_dict, state,
                           nodes, targets)
      if states_matches:
        new_states, new_matches = states_matches
        agenda.extend(new_states)
        if new_matches:
          for match in new_matches:
            repl_dict[match] = new_matches[match]
      if not agenda:
        return None
      else:
        state = agenda.pop()
        node_ind, target_ind = state

    return repl_dict

  @staticmethod
  def _matches_add_wildcard(dictionary, state):
    node_ind, target_ind = state
    if node_ind in dictionary:
      begin, end = dictionary[node_ind]
      dictionary[node_ind] = (begin, target_ind)
    else:
      dictionary[node_ind] = (target_ind, target_ind)

  @staticmethod
  def _matches_new_states(dictionary, state, nodes, targets):
    node_ind, target_ind = state
    node = nodes[node_ind]
    target = targets[target_ind]

    # Don't advance at all if we've exhausted the targets but not the nodes
    if target_ind >= len(targets) - 1 and node_ind < len(nodes) - 1:
      return None

    if node.is_Wild:
      match_attempt = Mul._matches_match_wilds(dictionary, node_ind,
                           nodes, targets)
      if match_attempt:
        # If the same node has been matched before, don't return
        # anything if the current match is diverging from the previous
        # match
        other_node_inds = Mul._matches_get_other_nodes(dictionary,
                                 nodes, node_ind)
        for ind in other_node_inds:
          other_begin, other_end = dictionary[ind]
          curr_begin, curr_end = dictionary[node_ind]

          other_targets = targets[other_begin:other_end + 1]
          current_targets = targets[curr_begin:curr_end + 1]

          for curr, other in zip(current_targets, other_targets):
            if curr != other:
              return None

        # A wildcard node can match more than one target, so only the
        # target index is advanced
        new_state = [(node_ind, target_ind + 1)]
        # Only move on to the next node if there is one
        if node_ind < len(nodes) - 1:
          new_state.append((node_ind + 1, target_ind + 1))
        return new_state, match_attempt
    else:
      # If we're not at a wildcard, then make sure we haven't exhausted
      # nodes but not targets, since in this case one node can only match
      # one target
      if node_ind >= len(nodes) - 1 and target_ind < len(targets) - 1:
        return None

      match_attempt = node.matches(target)

      if match_attempt:
        return [(node_ind + 1, target_ind + 1)], match_attempt
      elif node == target:
        return [(node_ind + 1, target_ind + 1)], None
      else:
        return None

  @staticmethod
  def _matches_match_wilds(dictionary, wildcard_ind, nodes, targets):
    """Determine matches of a wildcard with sub-expression in `target`."""
    wildcard = nodes[wildcard_ind]
    begin, end = dictionary[wildcard_ind]
    terms = targets[begin:end + 1]
    # TODO: Should this be self.func?
    mul = Mul(*terms) if len(terms) > 1 else terms[0]
    return wildcard.matches(mul)

  @staticmethod
  def _matches_get_other_nodes(dictionary, nodes, node_ind):
    """Find other wildcards that may have already been matched."""
    other_node_inds = []
    for ind in dictionary:
      if nodes[ind] == nodes[node_ind]:
        other_node_inds.append(ind)
    return other_node_inds

  @staticmethod
  def _combine_inverse(lhs, rhs):
    """
    Returns lhs/rhs, but treats arguments like symbols, so things
    like oo/oo return 1 (instead of a nan) and ``I`` behaves like
    a symbol instead of sqrt(-1).
    """
    from sympy.core.symbol import Dummy
    if lhs == rhs:
      return S.One

    def check(l, r):
      if l.is_Float and r.is_comparable:
        # if both objects are added to 0 they will share the same "normalization"
        # and are more likely to compare the same. Since Add(foo, 0) will not allow
        # the 0 to pass, we use __add__ directly.
        return l.__add__(0) == r.evalf().__add__(0)
      return False
    if check(lhs, rhs) or check(rhs, lhs):
      return S.One
    if any(i.is_Pow or i.is_Mul for i in (lhs, rhs)):
      # gruntz and limit wants a literal I to not combine
      # with a power of -1
      d = Dummy('I')
      _i = {S.ImaginaryUnit: d}
      i_ = {d: S.ImaginaryUnit}
      a = lhs.xreplace(_i).as_powers_dict()
      b = rhs.xreplace(_i).as_powers_dict()
      blen = len(b)
      for bi in tuple(b.keys()):
        if bi in a:
          a[bi] -= b.pop(bi)
          if not a[bi]:
            a.pop(bi)
      if len(b) != blen:
        lhs = Mul(*[k**v for k, v in a.items()]).xreplace(i_)
        rhs = Mul(*[k**v for k, v in b.items()]).xreplace(i_)
    return lhs/rhs

  def as_powers_dict(self):
    d = defaultdict(int)
    for term in self.args:
      for b, e in term.as_powers_dict().items():
        d[b] += e
    return d

  def as_numer_denom(self):
    # don't use _from_args to rebuild the numerators and denominators
    # as the order is not guaranteed to be the same once they have
    # been separated from each other
    numers, denoms = list(zip(*[f.as_numer_denom() for f in self.args]))
    return self.func(*numers), self.func(*denoms)

  def as_base_exp(self):
    e1 = None
    bases = []
    nc = 0
    for m in self.args:
      b, e = m.as_base_exp()
      if not b.is_commutative:
        nc += 1
      if e1 is None:
        e1 = e
      elif e != e1 or nc > 1:
        return self, S.One
      bases.append(b)
    return self.func(*bases), e1

  def _eval_is_polynomial(self, syms):
    return all(term._eval_is_polynomial(syms) for term in self.args)

  def _eval_is_rational_function(self, syms):
    return all(term._eval_is_rational_function(syms) for term in self.args)

  _eval_is_commutative = lambda self: _fuzzy_group(
    a.is_commutative for a in self.args)

  def _eval_is_finite(self):
    if all(a.is_finite for a in self.args):
      return True
    if any(a.is_infinite for a in self.args):
      if all(a.is_zero is False for a in self.args):
        return False

  def _eval_is_infinite(self):
    if any(a.is_infinite for a in self.args):
      if any(a.is_zero for a in self.args):
        return S.NaN.is_infinite
      if any(a.is_zero is None for a in self.args):
        return None
      return True

  def _eval_is_zero(self):
    zero = infinite = False
    for a in self.args:
      z = a.is_zero
      if z:
        if infinite:
          return  # 0*oo is nan and nan.is_zero is None
        zero = True
      else:
        if not a.is_finite:
          if zero:
            return  # 0*oo is nan and nan.is_zero is None
          infinite = True
        if zero is False and z is None:  # trap None
          zero = None
    return zero

  def _eval_is_extended_real(self):
    return self._eval_real_imag(True)

  def _eval_real_imag(self, real):
    zero = False
    t_not_re_im = None

    for t in self.args:
      if (t.is_complex or t.is_infinite) is False and t.is_extended_real is False:
        return False
      elif t.is_imaginary:  # I
        real = not real
      elif t.is_extended_real:  # 2
        if not zero:
          z = t.is_zero
          if not z and zero is False:
            zero = z
          elif z:
            if all(a.is_finite for a in self.args):
              return True
            return
      elif t.is_extended_real is False:
        # symbolic or literal like `2 + I` or symbolic imaginary
        if t_not_re_im:
          return  # complex terms might cancel
        t_not_re_im = t
      elif t.is_imaginary is False:  # symbolic like `2` or `2 + I`
        if t_not_re_im:
          return  # complex terms might cancel
        t_not_re_im = t
      else:
        return

    if t_not_re_im:
      if t_not_re_im.is_extended_real is False:
        if real:  # like 3
          return zero  # 3*(smthng like 2 + I or i) is not real
      if t_not_re_im.is_imaginary is False:  # symbolic 2 or 2 + I
        if not real:  # like I
          return zero  # I*(smthng like 2 or 2 + I) is not real
    elif zero is False:
      return real  # can't be trumped by 0
    elif real:
      return real  # doesn't matter what zero is

  def _eval_is_imaginary(self):
    z = self.is_zero
    if z:
      return False
    if self.is_finite is False:
      return False
    elif z is False and self.is_finite is True:
      return self._eval_real_imag(False)

  def _eval_is_composite(self):
    """
    Here we count the number of arguments that have a minimum value
    greater than two.
    If there are more than one of such a symbol then the result is composite.
    Else, the result cannot be determined.
    """
    number_of_args = 0 # count of symbols with minimum value greater than one
    for arg in self.args:
      if not (arg.is_integer and arg.is_positive):
        return None
      if (arg-1).is_positive:
        number_of_args += 1

    if number_of_args > 1:
      return True

  def as_content_primitive(self, radical=False, clear=True):
    """Return the tuple (R, self/R) where R is the positive Rational
    extracted from self.

    Examples
    ========

    >>> from sympy import sqrt
    >>> (-3*sqrt(2)*(2 - 2*sqrt(2))).as_content_primitive()
    (6, -sqrt(2)*(1 - sqrt(2)))

    See docstring of Expr.as_content_primitive for more examples.
    """

    coef = S.One
    args = []
    for i, a in enumerate(self.args):
      c, p = a.as_content_primitive(radical=radical, clear=clear)
      coef *= c
      if p is not S.One:
        args.append(p)
    # don't use self._from_args here to reconstruct args
    # since there may be identical args now that should be combined
    # e.g. (2+2*x)*(3+3*x) should be (6, (1 + x)**2) not (6, (1+x)*(1+x))
    return coef, self.func(*args)

  def as_ordered_factors(self, order=None):
    """Transform an expression into an ordered list of factors.

    Examples
    ========

    >>> from sympy import sin, cos
    >>> from sympy.abc import x, y

    >>> (2*x*y*sin(x)*cos(x)).as_ordered_factors()
    [2, x, y, sin(x), cos(x)]

    """
    cpart, ncpart = self.args_cnc()
    cpart.sort(key=lambda expr: expr.sort_key(order=order))
    return cpart + ncpart

  @property
  def _sorted_args(self):
    return tuple(self.as_ordered_factors())

  def dup_check(self):
    a_set = set(self.args)
    return (len(self.args) != len(a_set))

  def sign(self):
    cnt=0;
    N = len(self.args)
    i = 0
    while(i < N):
      j = i+1
      while(j < N):
        if ((self.args[i].name)>(self.args[j].name)):
          cnt +=1
        j+=1
      i+=1
    return cnt%2;

def prod(a, start=1):
  """Return product of elements of a. Start with int 1 so if only
     ints are included then an int result is returned.

  Examples
  ========

  >>> from sympy import prod, S
  >>> prod(range(3))
  0
  >>> type(_) is int
  True
  >>> prod([S(2), 3])
  6
  >>> _.is_Integer
  True

  You can start the product at something other than 1:

  >>> prod([1, 2], 3)
  6

  """
  return reduce(operator.mul, a, start)


def _keep_coeff(coeff, factors, clear=True, sign=False):
  """Return ``coeff*factors`` unevaluated if necessary.

  If ``clear`` is False, do not keep the coefficient as a factor
  if it can be distributed on a single factor such that one or
  more terms will still have integer coefficients.

  If ``sign`` is True, allow a coefficient of -1 to remain factored out.

  Examples
  ========

  >>> from sympy.core.mul import _keep_coeff
  >>> from sympy.abc import x, y
  >>> from sympy import S

  >>> _keep_coeff(S.Half, x + 2)
  (x + 2)/2
  >>> _keep_coeff(S.Half, x + 2, clear=False)
  x/2 + 1
  >>> _keep_coeff(S.Half, (x + 2)*y, clear=False)
  y*(x + 2)/2
  >>> _keep_coeff(S(-1), x + y)
  -x - y
  >>> _keep_coeff(S(-1), x + y, sign=True)
  -(x + y)
  """

  if not coeff.is_Number:
    if factors.is_Number:
      factors, coeff = coeff, factors
    else:
      return coeff*factors
  if coeff is S.One:
    return factors
  elif coeff is S.NegativeOne and not sign:
    return -factors
  elif factors.is_Add:
    if not clear and coeff.is_Rational and coeff.q != 1:
      q = S(coeff.q)
      for i in factors.args:
        c, t = i.as_coeff_Mul()
        r = c/q
        if r == int(r):
          return coeff*factors
    return Mul(coeff, factors, evaluate=False)
  elif factors.is_Mul:
    margs = list(factors.args)
    if margs[0].is_Number:
      margs[0] *= coeff
      if margs[0] == 1:
        margs.pop(0)
    else:
      margs.insert(0, coeff)
    return Mul._from_args(margs)
  else:
    return coeff*factors


def expand_2arg(e):
  from sympy.simplify.simplify import bottom_up
  def do(e):
    if e.is_Mul:
      c, r = e.as_coeff_Mul()
      if c.is_Number and r.is_Add:
        return _unevaluated_Add(*[c*ri for ri in r.args])
    return e
  return bottom_up(e, do)


from sympy.core.numbers import Rational
from sympy.core.power import Pow
from sympy.core.add import Add, _addsort, _unevaluated_Add
