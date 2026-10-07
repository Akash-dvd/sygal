# Recursive Sandhi and Vichcheda Canonicalization

**Akash Dwivedi**  
akash.d.dwivedi@gmail.com  
https://www.linkedin.com/in/akash-dvd-3259402a/

## Introduction

Exterior products give a compact representation of antisymmetric
multi-vectors, but overlapping left-contraction panels require both structural
and scalar bookkeeping. The elementary pattern is

```text
(a < (b ^ s)) ^ (a < (s ^ c)).
```

The shared factor `s` is the seam. The two panels combine into one contraction
over the oriented concatenation, multiplied by the contraction of `a` with
the seam:

```text
(a . s) * (a < (b1 ^ s ^ c)).
```

This paper develops the grade-matched generalization in which a grade-`r`
contractor meets a grade-`r` seam blade. The local identity is proved by the
minor expansion of iterated contraction. Nested sandhi is then formulated as
repeated application of this local theorem, with the contractor and seam
growing together so that their pairing remains scalar.

The local grade-`r` identity and the fixed-schedule induction theorem are
proved for the well-formed panel grammar using a level-local visibility
closure lemma. Schedule-independent normalization remains open; cases through
nesting depth six have been checked by direct symbolic expansion.

The stitching identities themselves are machine-checked. The grade-\(r\)
identity, its vanishing branch, the Capelli coefficient, and a closed-form
nested identity of arbitrary depth are proved in Lean 4 with Mathlib, over any
commutative ring and any bilinear form (Section 8). Locating a seam inside a
given expression is a separate search problem, solved by the implementation
and not part of these theorems.

## 1. Setting

Let \(V\) be a vector space with a nondegenerate bilinear form. We use
\(\wedge\) for the exterior product, \(\lrcorner\) for left contraction, and
\(\mid\) for the scalar pairing of equal-grade blades. For a vector \(u\),
\[
u\lrcorner(X\wedge Y)
  =(u\lrcorner X)\wedge Y
   +(-1)^{\operatorname{grade}(X)}
     X\wedge(u\lrcorner Y).
\]

For a decomposable blade
\[
A=a_1\wedge\cdots\wedge a_r,
\]
left contraction is the ordered iteration
\[
A\lrcorner X
 =
a_1\lrcorner\bigl(
a_2\lrcorner(\cdots(a_r\lrcorner X)\cdots)
\bigr).
\]
Equivalently,
\[
(u\wedge A)\lrcorner X=u\lrcorner(A\lrcorner X).
\]
This recursive rule fixes the sign convention used below.

## 2. Base Identity

Let \(a\) be a vector and let \(A,B\) be decomposable blades with one
distinguished shared one-vector \(s\). After reordering their factors, write
\[
A=(-1)^{\sigma_A}U\wedge s,\qquad
B=(-1)^{\sigma_B}s\wedge V,
\]
where \(U\) and \(V\) have no common factors. Define
\[
A\sqcup B
  :=(-1)^{\sigma_A+\sigma_B}U\wedge s\wedge V.
\]

### Proposition: sole-shared-seam identity

\[
(a\lrcorner A)\wedge(a\lrcorner B)
 =
(a\cdot s)\bigl(a\lrcorner(A\sqcup B)\bigr).
\]

### Proof

Put \(p=\operatorname{grade}(U)\) and
\(\epsilon=(-1)^{\sigma_A+\sigma_B}\). The graded Leibniz rule gives
\[
\begin{aligned}
a\lrcorner A
 &=(-1)^{\sigma_A}
   \bigl((a\lrcorner U)\wedge s
   +(-1)^p(a\cdot s)U\bigr),\\
a\lrcorner B
 &=(-1)^{\sigma_B}
   \bigl((a\cdot s)V-s\wedge(a\lrcorner V)\bigr).
\end{aligned}
\]
Wedging these expressions and using \(s\wedge s=0\) gives
\[
\begin{aligned}
(a\lrcorner A)\wedge(a\lrcorner B)
={}&\epsilon(a\cdot s)\bigl[
(a\lrcorner U)\wedge s\wedge V
 +(-1)^p(a\cdot s)U\wedge V\\
&\qquad -(-1)^pU\wedge s\wedge(a\lrcorner V)
\bigr].
\end{aligned}
\]
The bracket is exactly
\[
\begin{aligned}
a\lrcorner(U\wedge s\wedge V)
={}&(a\lrcorner U)\wedge s\wedge V\\
&+(-1)^pU\wedge
\bigl((a\cdot s)V-s\wedge(a\lrcorner V)\bigr).
\end{aligned}
\]
Since \(A\sqcup B=\epsilon(U\wedge s\wedge V)\), the result follows.

If \(U\) and \(V\) share a factor, then \(U\wedge s\wedge V=0\), and the
same expansion makes the left-hand side vanish. Disjointness is therefore
needed for the sole-seam interpretation, not for the formal identity after
repeated factors are admitted.

## 3. Grade-\(r\) Theorem

Let \(A\) and \(S\) be decomposable blades of the same grade \(r\). Suppose
\[
B=\epsilon_B\,b\wedge S,\qquad
C=\epsilon_C\,S\wedge c,
\]
where the factors of \(b\) and \(c\) are disjoint from one another and from
the displayed seam factors. Define
\[
B\sqcup C:=\epsilon_B\epsilon_C\,b\wedge S\wedge c.
\]

### Theorem: grade-\(r\) sole-seam identity

\[
(A\lrcorner B)\wedge(A\lrcorner C)
 =
(A\mid S)\bigl(A\lrcorner(B\sqcup C)\bigr).
\]

### Proof

Write \(A=a_1\wedge\cdots\wedge a_r\) and
\(S=s_1\wedge\cdots\wedge s_r\). For an ordered blade
\(X=x_1\wedge\cdots\wedge x_m\) and a position set
\(I=\{i_1<\cdots<i_r\}\subseteq\{1,\ldots,m\}\), put
\[
X_I=x_{i_1}\wedge\cdots\wedge x_{i_r},\qquad
X_{\widehat I}=x_1\wedge\cdots\wedge\widehat{x_{i_1}}\wedge\cdots
\wedge\widehat{x_{i_r}}\wedge\cdots\wedge x_m.
\]
With the contraction convention of Section 1, define
\[
\operatorname{sgn}(I)
 :=(-1)^{\,i_1+\cdots+i_r-r}.
\]
This is the sign of moving the selected factors to the contraction slots,
combined with the reversal forced by the iterated left contractions. Thus
\[
\Delta_A(I;X)
 :=\operatorname{sgn}(I)
\det\!\left[(a_\alpha\cdot x_{i_\beta})\right]_
             {\alpha,\beta=1}^{r}
\]
and the \(r\)-fold contraction is the explicit expansion
\[
A\lrcorner X
 =\sum_{\lvert I\rvert=r}\Delta_A(I;X)\,X_{\widehat I}.
\tag{3.1}
\]
For \(r=1\), this gives the usual sign
\((-1)^{i_1-1}\). For \(I=\{1,\ldots,r\}\), it gives the determinant
pairing with the displayed ordered block, including the sign dictated by the
contraction convention.

We now compare the coefficients of each residual wedge. Write
\[
B=b_1\wedge\cdots\wedge b_p\wedge s_1\wedge\cdots\wedge s_r,\qquad
C=s_1\wedge\cdots\wedge s_r\wedge c_1\wedge\cdots\wedge c_q,
\]
temporarily taking \(\epsilon_B=\epsilon_C=1\). Let \(P\subseteq\{1,\ldots,p\}\),
\(Q\subseteq\{1,\ldots,q\}\), and \(R\subseteq\{1,\ldots,r\}\) describe a
residual wedge
\[
Y_{P,R,Q}:=b_P\wedge s_R\wedge c_Q,
\]
where each subscript retains the original order. A term on the left can
produce this residual only by partitioning the residual seam indices as
\(R=T\mathbin{\dot\cup}(R\setminus T)\): the factors \(s_T\) come from the
first panel and \(s_{R\setminus T}\) from the second. Define
\[
\begin{aligned}
I_{P,T}
  &:=\bigl(\{1,\ldots,p\}\setminus P\bigr)
    \cup\bigl(p+\bigl(\{1,\ldots,r\}\setminus T\bigr)\bigr),\\
J_{T,Q}
  &:=\bigl(\{1,\ldots,r\}\setminus(R\setminus T)\bigr)
    \cup\bigl(r+\bigl(\{1,\ldots,q\}\setminus Q\bigr)\bigr),\\
K_{P,R,Q}
  &:=\bigl(\{1,\ldots,p\}\setminus P\bigr)
    \cup\bigl(p+\bigl(\{1,\ldots,r\}\setminus R\bigr)\bigr)\\
  &\qquad\cup\bigl(p+r+\bigl(\{1,\ldots,q\}\setminus Q\bigr)\bigr).
\end{aligned}
\]
Only the choices satisfying \(\lvert I_{P,T}\rvert
=\lvert J_{T,Q}\rvert=\lvert K_{P,R,Q}\rvert=r\) contribute. The seam
shuffle has sign
\[
\eta(R,T)
 :=(-1)^{\#\{(u,v)\in T\times(R\setminus T):u>v\}},
\]
because \(s_T\wedge s_{R\setminus T}=\eta(R,T)s_R\). Therefore the
coefficient of \(Y_{P,R,Q}\) in the left-hand side is
\[
\sum_T\eta(R,T)\,
\Delta_A(I_{P,T};B)\,
\Delta_A(J_{T,Q};C).
\tag{3.2}
\]

The Laplace--Cauchy--Binet minor identity, applied to the two copies of the
ordered seam block \(S\), gives
\[
\sum_T\eta(R,T)\,
\Delta_A(I_{P,T};B)\,
\Delta_A(J_{T,Q};C)
=(A\mid S)\,\Delta_A(K_{P,R,Q};b\wedge S\wedge c).
\tag{3.3}
\]
The sign comparison used in this convolution is the following elementary
index calculation.

### Lemma: sign in the minor convolution

Let \([n]=\{1,\ldots,n\}\), write \(t=\lvert T\rvert\), \(k=\lvert R\rvert\),
and put
\[
h(R,T):=\#\{(u,v)\in T\times(R\setminus T):u>v\}.
\]
Let
\[
\operatorname{sgn}_S:=(-1)^{\binom r2}
\]
be the sign of the ordered seam block considered by itself. Then
\[
\operatorname{sgn}(I_{P,T})\operatorname{sgn}(J_{T,Q})\eta(R,T)
=(-1)^{p(k-t-q+\lvert Q\rvert)+h(R,T)}
\operatorname{sgn}_S\operatorname{sgn}(K_{P,R,Q}).
\tag{3.4}
\]

#### Proof

Write
\[
\begin{aligned}
\sum I_{P,T}
 &=\sum([p]\setminus P)+p(r-t)+\sum([r]\setminus T),\\
\sum J_{T,Q}
 &=\sum([r]\setminus R)+\sum T
   +r(q-\lvert Q\rvert)+\sum([q]\setminus Q),\\
\sum K_{P,R,Q}
 &=\sum([p]\setminus P)+p(r-k)+\sum([r]\setminus R)\\
 &\qquad +(p+r)(q-\lvert Q\rvert)+\sum([q]\setminus Q).
\end{aligned}
\]
Using \(\operatorname{sgn}(I)=(-1)^{\sum I-r}\), subtraction gives
\[
\begin{aligned}
&\bigl(\sum I_{P,T}-r\bigr)
 +\bigl(\sum J_{T,Q}-r\bigr)
 -\bigl(\sum K_{P,R,Q}-r\bigr)
 +h(R,T)\\
&\qquad\equiv
p(k-t-q+\lvert Q\rvert)+\binom r2+h(R,T)
\pmod 2.
\end{aligned}
\]
Since \(\operatorname{sgn}_S=(-1)^{\binom r2}\), this is exactly (3.4).
The first term in the remaining exponent counts the index shifts across the
\(b\)-block and the \(c\)-block; \(h(R,T)\) counts the seam shuffle needed to
restore \(s_T\wedge s_{R\setminus T}\) to \(s_R\). These are precisely the
cofactor and shuffle signs in the Laplace expansion. Hence each \(T\)-term
has the sign on the right-hand side of (3.3), and the ordinary
Laplace--Cauchy--Binet minor identity proves (3.3).
\(\square\)

Thus (3.3) is not relying on an unspecified ``prescribed'' sign: the
selected-index signs, block shifts, and seam shuffle have all been reduced to
the explicit parity in (3.4).

### The Laplace identity being used

The determinant result invoked here is the generalized Laplace expansion for
complementary minors. For an \(n\times n\) matrix \(M\), and fixed row and
column sets \(I,J\subseteq\{1,\ldots,n\}\) of size \(k\),
\[
\det M
 =\sum_{\lvert L\rvert=k}
   (-1)^{\sum I+\sum L}
   \det M[I,L]\det M[I^c,L^c],
\tag{3.5}
\]
where the complementary row set is \(I^c\), the complementary column set is
\(L^c\), and all minors use increasing index order. This is the generalized
Laplace theorem, equivalently the Cauchy--Binet identity applied to compound
matrices; see Gantmacher [1959, Ch. I, §5].

For the present rectangular pairing matrix, the exact compound-minor
specialization is obtained by putting
\[
[I]_Y:=\det\!\left[(a_\alpha\cdot y_{i_\beta})\right]_
             {\alpha,\beta=1}^{r}.
\]
With the \(b,S,c\) column blocks and the index sets defined above, (3.5)
becomes
\[
\sum_T\eta(R,T)\,
\operatorname{sgn}(I_{P,T})\operatorname{sgn}(J_{T,Q})
[I_{P,T}]_B[J_{T,Q}]_C
=\operatorname{sgn}_S\operatorname{sgn}(K_{P,R,Q})
[K_{P,R,Q}]_{b\wedge S\wedge c}[S]_S.
\tag{3.6}
\]
The sign lemma verifies the conversion from the increasing-column minors in
(3.5) to the contraction minors \(\Delta_A\). Since
\(A\mid S=\operatorname{sgn}_S[S]_S\), equation (3.6) is exactly (3.3), not
an additional heuristic sign assertion.

### Recovery of the base case

Set \(r=1\), \(p=q=1\), \(A=a\), \(S=s\), \(b=b\), and \(c=c\). Then
\[
a\lrcorner(b\wedge s)=(a\cdot b)s-(a\cdot s)b,
\qquad
a\lrcorner(s\wedge c)=(a\cdot s)c-(a\cdot c)s.
\]
Their wedge is
\[
\begin{aligned}
&(a\lrcorner(b\wedge s))\wedge(a\lrcorner(s\wedge c))\\
&=(a\cdot s)\bigl[
 (a\cdot b)s\wedge c-(a\cdot s)b\wedge c
 +(a\cdot c)b\wedge s\bigr]\\
&=(a\cdot s)\bigl(a\lrcorner(b\wedge s\wedge c)\bigr).
\end{aligned}
\]
Here the term containing \(s\wedge s\) is the repeated-residual term that
vanishes. Since \(\operatorname{sgn}(\{1\})=1\) and
\(\operatorname{sgn}_S=1\), this is exactly the sole-shared-seam identity of
Section 2, including its sign convention.

There is an important qualification about vanishing. If a seam factor
\(s_k\) is omitted from both selected sets, then the residual wedge contains
\(s_k\wedge s_k\) and is zero by alternation. However, a term with
\(I\ne I_S\) need not vanish individually: its omitted seam factors may be
complementary to those omitted in the other panel. Such nonprincipal terms
are the \(T\)-summands in (3.2), and they combine by (3.3). It would therefore
be incorrect to discard every \(I\ne I_S\) term; only repeated-residual
terms vanish before the minor convolution.

Finally, (3.1) applied to \(b\wedge S\wedge c\), followed by (3.3), shows
\[
\begin{aligned}
(A\lrcorner B)\wedge(A\lrcorner C)
 &= (A\mid S)\bigl(A\lrcorner(b\wedge S\wedge c)\bigr)\\
 &= (A\mid S)\bigl(A\lrcorner(B\sqcup C)\bigr).
\end{aligned}
\]
Restoring the orientation factors multiplies both sides by
\(\epsilon_B\epsilon_C\), which is already part of \(B\sqcup C\).
\(\square\)

### Why the seam has grade \(r\)

If \(\operatorname{grade}(A)=r\), \(\operatorname{grade}(S)=t\),
\(\operatorname{grade}(b)=p\), and \(\operatorname{grade}(c)=q\), then the
two sides before the coefficient have grades
\[
(p+t-r)+(q+t-r)
\quad\text{and}\quad
p+t+q-r.
\]
Their difference is \(t-r\). A scalar coefficient is therefore possible
exactly when \(t=r\). The vector proposition is the \(r=t=1\) case.

## 4. Nested Recursion

### Orientation and parity

Before applying the seam identity, each panel is oriented so that the seam is
rightmost in the left panel and leftmost in the right panel:
\[
B=\epsilon_B\,b\wedge S,\qquad
C=\epsilon_C\,S\wedge c,
\qquad \epsilon_B,\epsilon_C\in\{+1,-1\}.
\]
The factors \(\epsilon_B\) and \(\epsilon_C\) record the parity of these
reorderings. They are part of the coefficient; alignment is therefore
mathematical data, not a cosmetic normalization step.

### Nested recursion

For an ordered contractor chain \(d_1,\ldots,d_k\), define
\[
A_{\mathrm{acc}}^{(r)}
  :=d_1\wedge\cdots\wedge d_r.
\]
The recursive contraction rule gives
\[
\iota_{A_{\mathrm{acc}}^{(r)}}(X)
 =
\iota_{d_1}\bigl(
\iota_{d_2}(\cdots\iota_{d_r}(X)\cdots)
\bigr).
\]
Thus the accumulated blade is shorthand for iterated vector contractions; no
vector Leibniz rule is being applied directly to a blade.

At the same recursive depth, the shared seam accumulates to
\[
S_{\mathrm{acc}}^{(r)}
  :=s_1\wedge\cdots\wedge s_r.
\]
The coefficient
\[
A_{\mathrm{acc}}^{(r)}\mid S_{\mathrm{acc}}^{(r)}
\]
is scalar because the contractor and seam have the same grade. Their matching
growth is forced by grade, not introduced as an arbitrary convention.

At each level, the grade-balance value is
\[
x=
\operatorname{grade}(D_L)+\operatorname{grade}(D_R)
-\operatorname{grade}(D_{\mathrm{merged}})
-\operatorname{grade}(A_{\mathrm{acc}}).
\]
Under the sole-seam invariant, the recursion takes the following branches:

| Condition | Action |
|---|---|
| \(x<0\) | Recurse into the merged down expression. |
| \(x=0\) | Apply the grade-\(r\) identity and emit its scalar. |
| \(x>0\) | The expression vanishes because residual seam factors remain repeated. |

The local grade-\(r\) seam identity gives the induction step once the
level-local sole-seam invariant is stated explicitly. Let \(h(\mathcal T)\)
be the number of unresolved recursive seam levels in a pair of nested panel
trees. We use the following invariant:

1. every down expression at a node is decomposable and homogeneous;
2. after orientation, the two panels have the form
   \(B=b\wedge S\) and \(C=S\wedge c\), with \(S\) their sole common
   *visible* factor;
3. a nested argument is opaque at its parent node and is inspected only when
   recursion reaches that argument's own node; and
4. all scalar factors and orientation parities produced above a node are
   carried unchanged into its merged child.

The word ``visible'' refers to immediate exterior-product arguments, not to
the labelled leaves occurring inside nested contractions.

### Level-local visibility

The closure argument uses a syntactic, rather than a global support,
property. The panel grammar has three relevant constructors:
\[
E ::= \text{atom}\mid E_1\wedge\cdots\wedge E_n
       \mid (U\lrcorner D).
\]
At a fixed exterior-product node \(D=E_1\wedge\cdots\wedge E_n\), define
\[
\operatorname{Vis}(D):=\{E_1,\ldots,E_n\}.
\]
The seam matcher compares elements of \(\operatorname{Vis}(D_L)\) and
\(\operatorname{Vis}(D_R)\); it does not compare arbitrary labelled leaves
inside a nested contraction. A proper descendant of \(E_i\) is therefore
opaque at this node. If the whole nested expression \(E_i\) occurs on both
sides, it is one visible seam, and its own descendants are inspected only
when recursion reaches that child node.

### Lemma: syntactic visibility of seam candidates

Let \(q\) be a proper descendant of an immediate factor \(E_i\) at an exterior
node \(D\). If \(q\ne E_i\), then \(q\notin\operatorname{Vis}(D)\) and cannot
be a seam candidate at \(D\). A repeated nested expression \(E_i\), by
contrast, is one candidate at \(D\); its internal factors are candidates only
at the nested node that contains them.

#### Proof

By definition, \(\operatorname{Vis}(D)\) contains exactly the immediate
arguments of the exterior node. A proper descendant of \(E_i\) is an argument
of a child of \(E_i\), not an argument of \(D\), so it is not in
\(\operatorname{Vis}(D)\). The seam matcher therefore cannot select it.

If the complete expression \(E_i\) occurs on both sides, the two immediate
argument lists contain the same element \(E_i\), so they expose one seam.
The recursive matcher receives \(E_i\) as its own node only after descending
to that node and then uses \(\operatorname{Vis}(E_i)\). No descendant is
lifted into the parent argument list. \(\square\)

### Lemma: semantic sibling separation

Let \(D=E_1\wedge\cdots\wedge E_n\), where each \(E_i\) is either a one-blade
or a nested contraction node, and let \(A\) be a blade of grade \(r\). In the
full multilinear expansion of \(A\lrcorner D\), expanding every nested node
down to leaves, each monomial has the form
\[
\pm\,\Delta\cdot(F_1\wedge\cdots\wedge F_n),
\]
where \(F_i\) is a fully expanded residual built only from the leaves in the
subtree \(E_i\), and \(\Delta\) is a product of pairings. No pairing term uses
down-side leaves from two distinct sibling subtrees \(E_i\) and \(E_j\).

#### Proof

For a flat exterior node, write \(A=a_1\wedge\cdots\wedge a_r\). Repeated
application of the graded Leibniz rule partitions the ordered contractor
factors among the siblings:
\[
A\lrcorner(E_1\wedge\cdots\wedge E_n)
=\sum_{I_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}I_n=[r]}
\varepsilon(I_1,\ldots,I_n)
\bigwedge_{i=1}^{n}(A_{I_i}\lrcorner E_i),
\]
where \(A_{I_i}\) retains the original order. To make the sign explicit, let
\(\iota(j)=i\) when \(j\in I_i\), let \(g_i=\operatorname{grade}(E_i)\), and
put
\[
\varepsilon(I_1,\ldots,I_n)
:=(-1)^{\,
 \sum_{j=1}^{r}\sum_{k<\iota(j)}g_k
 +\#\{(j,\ell):j<\ell,\ \iota(j)>\iota(\ell)\}}.
\]
The first term is the sum of the grades crossed by the \(j\)-th contraction;
the second is the inversion parity created when an earlier contraction lowers
the grade crossed by a later one. For a one-blade
\(E_i\), the factor is zero unless the assigned grade is admissible, and its
nonzero coefficient is the corresponding dot pairing. For a nested \(E_i\),
the same expression is expanded recursively inside that factor. Induction on
the total number of nested contraction nodes therefore expands each
\(A_{I_i}\lrcorner E_i\) independently. All pairings created there have both
their down-side leaves inside \(E_i\); wedging the residuals introduces only
signs and possible repeated-factor zeros, never a new pairing across siblings.
This proves the claim. \(\square\)

The syntactic visibility lemma is therefore a statement about what the
matcher can select, while semantic sibling separation supplies the algebraic
bridge. Together they justify ignoring a buried coincidence without defining
it away: Theorem 2 proves that the permitted stitches still equal full direct
left-contraction expansion. In particular, this covers the hidden-coincidence
configuration
\[
D_L=a_2\wedge a_3\wedge\bigl(a_4\lrcorner(b_1\wedge b_2)\bigr),
\qquad D_R=a_3\wedge b_1,
\]
which is also checked by the corresponding implementation regression test.

### Lemma: one-stitch closure

Let \(T_L,T_R\) be well-formed nested contraction trees of height \(h\)
satisfying the level-local sole-seam invariant and sharing a contraction
lineage. For the stitch defined in the Algorithm section, grammar preservation
follows directly from its definition: it concatenates immediate exterior
arguments and recursively visits a child only at that child's own node. If
\(T_M\) is the result of one valid root stitch, then \(T_M\) satisfies the same
invariant at every remaining level.

#### Proof

Induct on \(h\). For \(h=0\), there are no remaining levels.

For \(h>0\), orient the root down expressions as
\[
D_L=b\wedge S,\qquad D_R=S\wedge c.
\]
The stitch constructs
\[
D_M=b\wedge S\wedge c,
\]
with \(S\) counted once. At this node, the only possible seam candidates
come from the immediate argument lists. The syntactic visibility lemma
excludes every factor buried inside a nested argument. Thus a factor of \(c\)
that coincides with a buried factor of \(T_L\) cannot create a second seam at
the root. If it coincides with a complete immediate nested argument, that
complete argument is visible and the original sole-seam hypothesis already
excludes a second candidate.

By semantic sibling separation and the definition of the stitch, \(c\) is not
paired with a buried leaf of \(b\)'s nested child, nor is a child factor lifted
into the parent list. Hence every remaining comparison is either the unique
corresponding comparison inside \(S\), or a comparison at a separate child
node whose immediate arguments were already governed by the sole-seam
invariant. The former has strictly smaller height and is preserved by the
induction hypothesis; the latter cannot acquire a new cross-level candidate by
the visibility lemma.

Therefore the merged tree has exactly one active seam at every remaining
lineage level. Reordering signs and scalar overlap coefficients change
coefficients only, not the syntax or visibility relation. \(\square\)

The earlier hereditary-freshness condition is sufficient but stronger than
necessary: labelled leaves may coincide across levels, as long as nested
constructions remain opaque to seam matching at their parent node. The lemma
therefore applies unconditionally to the stated well-formed panel grammar.

### Theorem: nested sole-seam recursion under the invariant

For a fixed valid merge schedule, any pair of well-formed nested contraction
trees satisfying the level-local sole-seam invariant is reduced by repeated
grade-gated stitching to the same expression as direct left-contraction
expansion. The result includes all overlap scalars and exterior-algebra parity
signs.

#### Proof

We induct on \(h(\mathcal T)\). If \(h(\mathcal T)=0\), the current seam is
grade-matched with the accumulated contractor, so \(x=0\). The grade-\(r\)
sole-seam identity gives exactly the direct contraction expansion, including
the orientation factor in \(B\sqcup C\).

Now assume the claim for all trees of height at most \(h\), and consider a
tree of height \(h+1\). Orient the root panels and expand each contraction by
the graded Leibniz rule. If \(x>0\), semantic sibling separation says that
contractor factors assigned to one sibling cannot remove a seam factor through
a pairing with a buried leaf in another sibling. Since the visible seam has
grade larger than the available contractor grade, every summand retains a
common seam factor in both residual wedges. Each such summand is zero by
alternation, and the grade-gated recursion returns zero as well.

If \(x=0\), the current contractor and seam have equal grade. The root is
therefore exactly the grade-\(r\) situation of the theorem above; replacing
the two panels by their merged panel preserves the direct expansion and
extracts the scalar \(A_{\mathrm{acc}}\mid S_{\mathrm{acc}}\).

It remains to consider \(x<0\). The graded Leibniz expansion groups the
nonzero terms by the unique residual visible seam. By the one-stitch closure
lemma, this group is represented by a merged down-expression of height at
most \(h\), with exactly the scalar and parity factors recorded at the root.
The induction hypothesis identifies the recursive reduction of that merged
expression with its direct left-contraction expansion. Multiplying by the
unchanged root factors gives the direct expansion of the original tree. This
proves the claim for height \(h+1\), and hence for every finite height.

The theorem is deliberately stated for a fixed valid merge schedule. The
level-local closure lemma establishes its structural hypothesis for the
well-formed panel grammar. The theorem does not claim that different valid
schedules are confluent. Computational checks of nesting depths up to six,
including higher-grade decomposable blades, support the invariant but do not
replace its proof.

### Closed form for a nest with an innermost seam

When the shared seam sits at the bottom of a contraction chain, the recursion
above can be written in one formula. Let \(K_1,\ldots,K_k\) be contractor
blades and \(U_i,V_i\) wing blades, and let \(U_x\), \(S\), \(W\) be blades.
Put
\[
\begin{aligned}
\Phi^L&:=K_1\lrcorner\bigl(U_1\wedge K_2\lrcorner
  (U_2\wedge\cdots K_k\lrcorner(U_k\wedge U_x\wedge S))\bigr),\\
\Phi^R&:=K_1\lrcorner\bigl(V_1\wedge K_2\lrcorner
  (V_2\wedge\cdots K_k\lrcorner(V_k\wedge S\wedge W))\bigr),\\
\Phi^M&:=K_1\lrcorner\bigl(U_1\wedge V_1\wedge\cdots
  K_k\lrcorner(U_k\wedge V_k\wedge U_x\wedge S\wedge W)\bigr),
\end{aligned}
\]
and \(A_{\mathrm{acc}}:=K_1\wedge\cdots\wedge K_k\).

### Theorem: nested sole-seam identity, closed form

If \(\operatorname{grade}(A_{\mathrm{acc}})=\operatorname{grade}(S)\), then
\[
\Phi^L\wedge\Phi^R
=(-1)^{\sigma}\,(A_{\mathrm{acc}}\mid S)\,\Phi^M,
\qquad
\sigma=\sum_{i=1}^{k}\lvert V_i\rvert
  \Bigl(\lvert U_x\rvert+\sum_{j>i}\lvert U_j\rvert\Bigr),
\]
where \(\lvert\cdot\rvert\) is grade. If
\(\operatorname{grade}(A_{\mathrm{acc}})<\operatorname{grade}(S)\), then
\(\Phi^L\wedge\Phi^R=0\). No disjointness or nondegeneracy hypothesis is
needed.

#### Proof sketch

Prove the stronger statement in which \(\Phi^R\) is replaced by
\(E\lrcorner\Phi^R\) for an extra contractor \(E\), by induction on \(k\). At
each level the outer \(K_1\) annihilates \(\Phi^L\) and is pulled out of both
factors; the accumulated contractor \(E\wedge K_1\) is then pushed past
\(V_1\), and every error term is a deficient instance, hence zero. At the
bottom, \(S\wedge(E\lrcorner(S\wedge Y))=S\wedge(E\lrcorner S)\wedge Y\), and
\(E\lrcorner S=(E\mid S)\) by the Capelli extraction. The sign \(\sigma\) is
the shuffle parity of moving each \(V_i\) past the deeper left wings. The
full proof is machine-checked (Section 8). \(\square\)

For \(k=1\) this is the grade-\(r\) theorem. With juxtaposition denoting
\(\wedge\) and \(S=c_1c_2c_3\), the identity
\[
\begin{aligned}
&(d_1\lrcorner(a_1a_2\wedge d_2\lrcorner(b_1b_2\wedge d_3\lrcorner S)))
\wedge
(d_1\lrcorner(a_3a_4\wedge d_2\lrcorner(b_3b_4\wedge d_3\lrcorner(S\wedge c_4)))))\\
&\quad=(d_1d_2d_3\mid S)\;
d_1\lrcorner(a_1a_2a_3a_4\wedge d_2\lrcorner(b_1b_2b_3b_4\wedge
d_3\lrcorner(S\wedge c_4)))
\end{aligned}
\]
is the case \(k=3\), \(\sigma=4\).

### The overlap coefficient via Capelli

The grade-\(r\) theorem identifies the coefficient as the scalar pairing
\[
\kappa=A_{\mathrm{acc}}\mid S_{\mathrm{acc}}.
\]
If
\[
A_{\mathrm{acc}}=d_1\wedge\cdots\wedge d_r,\qquad
S_{\mathrm{acc}}=s_1\wedge\cdots\wedge s_r,
\]
then
\[
\kappa=
(-1)^{\binom r2}\det\bigl[(d_i\cdot s_j)\bigr]_{i,j=1}^{r}.
\]
The factor \((-1)^{\binom r2}\) is the reversal forced by the iterated
contraction order of Section 1: for equal grades, \(A\lrcorner S\) is exactly
this scalar. The determinant is the finite Capelli contraction of the accumulated
contractor with the accumulated seam. It is a finite algebraic pairing, not an
additional geometric operation.

## 5. Algorithm (Stitching)

```text
canonicalize(expression):
    while a mergeable pair exists:
        choose panels with a common contraction lineage
        orient the panels around one shared seam
        record the two reordering parities
        accumulate the contractor and seam blades
        compute the grade-balance value x
        if x > 0:
            return zero under the sole-seam invariant
        if x < 0:
            recursively canonicalize the merged down expression
        if x == 0:
            multiply by the contractor-seam scalar and both parities
            replace the pair by the merged contraction
    return expression
```

## 6. CGA encoding

The applications use the standard conformal model rather than introducing a
new encoding. For \(x\in\mathbb R^n\), its conformal point is the null vector
\[
\dot{x}=x+e_0+\frac{x^2}{2}e_\infty,
\qquad
\dot{x}^{\,2}=0,
\]
with the usual normalization \(e_0\cdot e_\infty=-1\). A circle or sphere is
represented by the blade obtained from its defining points or carrier
objects. We write \(\vee\) for the standard dual/reduced meet. Incidence is
expressed by
\[
A\wedge\dot y=0.
\]
For a sphere with Euclidean centre \(c\) and radius \(\rho\), the dual
representation is
\[
\dot c-\frac{\rho^2}{2}e_\infty.
\]
These conventions, including the interpretation of lines, circles, spheres,
duality, and incidence, are standard; see Li [Li 2026], Doran and Lasenby
[Doran--Lasenby 2003], and Dorst, Fontijne, and Mann [Dorst--Fontijne--Mann
2007].
The present paper only applies stitching to the resulting exterior-product
and contraction expressions.

## 7. Applications

The step counts below count successful seam-resolution steps, not elementary
geometric constructions, scalar products, or final incidence tests.

### 7.1 A parameterized two-stitch incidence family

The Monge, perpendicular-bisector, and angle-bisector constructions have the
same algebraic shape when their chart encodings satisfy the same panel
hypotheses. Let \(X_1,X_2,X_3\) be oriented carrier blades and let \(K\) be a
fixed contractor. Put
\[
Q_{ij}:=K\mathbin{\lrcorner}(X_i\wedge X_j).
\]
Assume that the three panels are oriented so that \(Q_{12}\) and \(Q_{23}\)
have the sole seam \(X_2\), that \(Q_{12}\wedge Q_{23}\) exposes the
two-factor seam \(X_3\wedge X_1\) against \(Q_{31}\), and that
\(\operatorname{grade}(K)=\operatorname{grade}(X_2)=1\). The same two-stitch
proof then applies to every
geometric interpretation of the carriers.

### Proposition: parameterized pairwise-difference incidence

Under the preceding panel hypotheses, the three pairwise objects \(Q_{12}\),
\(Q_{23}\), and \(Q_{31}\) satisfy
\[
Q_{12}\wedge Q_{23}\wedge Q_{31}=0.
\]
Consequently, whenever the resulting blades represent the relevant affine
objects in a common chart, their three pairwise constructions have the
corresponding common incidence or collinearity relation.

#### Proof

The first seam is grade-matched, so the grade-\(r\) identity gives
\[
Q_{12}\wedge Q_{23}
=(K\mid X_2)\,
K\mathbin{\lrcorner}(X_1\wedge X_2\wedge X_3),
\]
up to the canonical orientation sign already fixed by the panel order.
Against \(Q_{31}\), the exposed seam is \(X_3\wedge X_1\), of grade two,
whereas \(K\) has grade one. The grade gate is therefore in its overflow
branch: every full-expansion term retains a repeated seam factor and vanishes
by alternation. Hence
\[
Q_{12}\wedge Q_{23}\wedge Q_{31}=0.
\]
The proof depends only on the contractor grade, seam pattern, and orientation;
the geometric meaning of \(X_i\) is the parameter.

The intended instantiations are summarized below. The first row is realized in
the Lie-sphere chart of this paper. The other two rows are algebraic targets
for a chart-specific encoding, not claims that the point-only CGA chart
automatically supplies those panels.
\[
\begin{array}{c|c|c|c|c}
\text{construction} & K & \text{carriers} & \text{pairwise result}
& \text{status here}\\
\hline
\text{Monge} & e_r & \text{oriented circles}
& \text{homothety centre} & \text{proved}\\
\text{perpendicular bisectors} & e_\infty & \text{points}
& \text{perpendicular bisector} & \text{encoding required}\\
\text{angle bisectors} & e_r & \text{lines}
& \text{angle bisector} & \text{encoding required}
\end{array}
\]
Thus the proposition expresses the common two-stitch architecture, while the
carrier chart must still be checked for each construction. In particular, the
often-suggested line representative
\[
L=x e_x+y e_y+e_r+d\,e_\infty,\qquad x^2+y^2=1,
\]
is null in the radius-augmented metric, but it does not make the angle-bisector
row valid by itself. For
\[
L_1=e_x+e_r+2e_\infty,\qquad
L_2=e_y+e_r-e_\infty,
\]
the direct metric calculation gives
\[
L_1^2=L_2^2=0,\qquad
e_r\mathbin{\lrcorner}(L_1\wedge L_2)=L_1-L_2,
\qquad
\bigl(L_1-L_2\bigr)^2=2\ne0.
\]
The contracted blade is therefore not null and cannot be identified with a
null line in this naive chart. This numerical check prevents the angle- and
perpendicular-bisector rows from being overstated; a different
representation, or a separate metric lemma, is required before they become
fully verified CGA applications.

**Verified instantiation: Monge.**

Monge's theorem has the same pairwise-construction architecture but a
different Euclidean incidence statement. For three oriented circle blades
\(\mathcal C_1,\mathcal C_2,\mathcal C_3\), let
\(\ell_{ij}^{+},\ell_{ij}^{-}\) be the two common tangent lines and define
\[
H_{ij}:=\ell_{ij}^{+}\vee\ell_{ij}^{-}.
\]
The point \(H_{ij}\) is the homothety centre, and the three points satisfy
\[
H_{12}\wedge H_{23}\wedge H_{31}\wedge e_\infty=0.
\]
This is collinearity, not radical-center concurrency. In the dual CGA
encoding, its tangent and homothety panels exhibit the same repeated-seam
stitch pattern as the pairwise-difference proposition; it therefore serves
as the corresponding dual/collinearity instance. Its reduction uses the two
seam-resolution steps in the proposition: one balanced merge and one grade
overflow.

### 7.3 Concyclic four-point boundary case

The concyclic four-point case uses a different termination mechanism and is
not an instance of the parameterized proposition. For null point
representatives \(\dot p_1,\ldots,\dot p_4\), concyclicity is the incidence
condition
\[
\dot p_1\wedge\dot p_2\wedge\dot p_3\wedge\dot p_4=0.
\]
Here the computation terminates because the four point representatives are
linearly dependent, not because an accumulated seam has exceeded the
contractor grade. This distinction matters: the example shows that the
stitching calculus uses geometric hypotheses such as concyclicity in addition
to grade balance. We therefore record it as a boundary case rather than claim
a two-stitch contraction proof for it.

## 8. Formal Verification and Implementation

The stitching identities are proved in Lean 4 (v4.33.1) with Mathlib, in
`paper/sandhi/lean/` of the Sygal repository, with no unproved assumptions
beyond Lean's standard axioms. The setting is \(\Lambda M\) for a module \(M\)
over an arbitrary commutative ring, with left contraction by an arbitrary
bilinear form; neither nondegeneracy nor disjointness of wing factors is
required.

| Machine-checked result | Lean name |
|---|---|
| Base identity (Section 2) | `soleSeam_grade1` |
| Grade-\(r\) identity (Section 3) | `soleSeam_gradeR` |
| Flat overflow (\(\operatorname{grade}S>\operatorname{grade}A\)) gives \(0\) | `soleSeam_vanish` |
| Capelli: \(A\lrcorner S=(-1)^{\binom r2}\det[a_i\cdot s_j]\) | `contractBlade_ofList_eq_seamPairing` |
| Nested closed form (Section 4) | `nested_soleSeam'` |
| Nested overflow gives \(0\) | `nested_vanish` |
| Up vichcheda: \((K\lrcorner S)\wedge K\lrcorner(w_1\wedge S\wedge w_2)=0\) | `upVichcheda_vanish` |
| Expansion (3.1) for \(r=1\) | `contractVec_ofList_eq_expandSum` |

In the up-vichcheda row the contractors are \(K\wedge P\) and \(K\), the seam
is the peeled panel \(S=P\lrcorner X\), and
\(\operatorname{grade}S>\lvert K\rvert\); the result holds over a field, for
arbitrary wings, because \(P\lrcorner X\) is again a blade when \(X\) is a
wedge of vectors (`contractBlade_ofList_blade`). It is false for a general
homogeneous \(S\).

The expansion (3.1) for \(r>1\), and the visibility, sibling-separation, and
one-stitch closure lemmas of Section 4, have paper proofs only; schedule
independence is open.

The Lean proof of the grade-\(r\) identity does not use the minor expansion
of Section 3. It uses self-annihilation (each contractor factor annihilates
\(A\lrcorner(b\wedge S)\)), the fact that any term spending a contractor on
\(b\) leaves a seam factor that dies against \(S\), and a Laplace expansion
along the last row for the Capelli coefficient.

The implementation (the Sygal canonicalizer) does two things: it searches an
expression for panels sharing a seam and orients them, and it then replaces
the pair by the right-hand side of the applicable theorem. Only the second
step is a mathematical claim, and it is the one covered above. The search is
pattern matching; its correctness amounts to applying the theorem with the
correct seam, contractors, orientation parities, and coefficient.

An exact cross-check against the Lean formulas (`tests/crosscheck_lean.py`,
evaluating both sides with rational vectors and random symmetric forms) finds
that the implementation's pairing and Capelli coefficient equal
\((-1)^{\binom r2}\det[k_i\cdot s_j]\) for \(r\le 4\), and that each flat
stitch it performs equals the right-hand side of the grade-\(r\) theorem,
sign included; its up-vichcheda reductions return \(0\) exactly in the cases
covered by `upVichcheda_vanish`. The implementation does not yet apply the
nested closed form:
when the outer levels share no visible factor it leaves the product
unchanged, which is correct but not reduced. The three-level identity in
Section 4 is therefore checked by expansion and by Lean, not by the
canonicalizer.

## 9. Limitations

The grade-\(r\) seam identity is machine-checked for arbitrary blades given
as wedge products of vectors; the sole-seam hypotheses are needed only to
interpret the result as a unique stitch. The fixed-schedule induction theorem
is proved for the well-formed, level-local panel grammar;
schedule-independent normalization remains open, despite verification through
depth six. The nested identity is machine-checked for a seam at the innermost
level of a shared contractor chain; configurations in which seam factors are
distributed across levels rely on the paper proof of the nested recursion
theorem. The result does not claim a normal-form theorem for arbitrary
mixed-grade or nondecomposable multivectors.

## References

\([Li 2026]\) H. Li, “Null geometric algebra with geometric
interpretation,” *Philosophical Transactions of the Royal Society A*,
384:20250096, 2026.
\url{https://doi.org/10.1098/rsta.2025.0096}

\([Doran--Lasenby 2003]\) C. Doran and A. Lasenby, *Geometric Algebra for
Physicists*, Cambridge University Press, 2003.

\([Dorst--Fontijne--Mann 2007]\) L. Dorst, D. Fontijne, and S. Mann, *Geometric Algebra
for Computer Science*, Morgan Kaufmann, 2007.

\([Gantmacher 1959]\) F. R. Gantmacher, *The Theory of Matrices*, Vol. 1,
Chelsea Publishing Company, 1959, Chapter I, \S5.
