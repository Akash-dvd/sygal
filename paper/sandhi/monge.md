# Monge's Theorem by Stitching

## Setting: oriented circles as null vectors

Work in `R^{3,2}` with basis `e0, ex, ey, er, e_inf`, where

```
e0 . e_inf = -1,    ex . ex = ey . ey = 1,    er . er = -1
```

An **oriented** circle with centre `(x, y)` and **signed** radius `r` is

```
C = e0 + x ex + y ey + r er + ((x^2 + y^2 - r^2)/2) e_inf
```

**Null check.**

```
C . C = x^2 + y^2 + r^2 (er . er) - (x^2 + y^2 - r^2)
      = x^2 + y^2 - r^2 - x^2 - y^2 + r^2
      = 0
```

Every oriented circle is a null vector. This is Lie sphere geometry (Cecil),
not the conformal model: the extra coordinate `er` carries the radius, and the
sign of `r` is the orientation. The circles `r` and `-r` are the same point
set traversed oppositely.

## The radius annihilator

With the normalization above, `er . C = -r`.

**Lemma (homothety centre).** For circles `C1, C2` with signed radii
`r1 != r2`,

```
er ⌟ (C1 ^ C2) = (er . C1) C2 - (er . C2) C1
               = r2 C1 - r1 C2
```

The `er`-coefficient of the result is `r2 r1 - r1 r2 = 0`. A null vector with
zero radius is a **point**. Normalizing by its `e0`-coefficient `(r2 - r1)`:

```
centre = (r2 c1 - r1 c2) / (r2 - r1)
```

which is the homothety centre of the two circles. Write
`P_ij := er ⌟ (Ci ^ Cj)`.

So `er ⌟` is exactly the operation that annihilates radius and returns the
centre of similitude.

## Monge's theorem

**Statement.** For three circles in general position, the three homothety
centres `P_12`, `P_23`, `P_31` are collinear.

We show `P_12 ^ P_23 ^ P_31 = 0`.

### Step 1 — stitch on the seam `C2`

The panels `er ⌟ (C1 ^ C2)` and `er ⌟ (C2 ^ C3)` share the single visible
factor `C2`. Orient the seam toward the join:

```
C1 ^ C2    seam already rightmost     eps_L = +1,  b = C1
C2 ^ C3    seam already leftmost      eps_R = +1,  c = C3
```

Contractor `A = er` has grade 1; seam `S = C2` has grade 1. Grade-matched, so
the gate is balanced (`t = r = 1`) and the grade-`r` seam identity applies
with a scalar coefficient:

```
P_12 ^ P_23 = (er . C2) * ( er ⌟ (C1 ^ C2 ^ C3) )
            = -r2 * ( er ⌟ (C1 ^ C2 ^ C3) )
```

### Step 2 — stitch against `P_31`

```
P_12 ^ P_23 ^ P_31 = -r2 * ( er ⌟ (C1 ^ C2 ^ C3) ) ^ ( er ⌟ (C3 ^ C1) )
```

The two panels now share **two** visible factors, `C3` and `C1`, so the
accumulated seam is

```
S = C3 ^ C1        grade(S) = 2
```

while the accumulated contractor is still

```
A = er             grade(A) = 1
```

The grade condition requires `grade(S) = grade(A)`. Here

```
t - r = 2 - 1 = 1 > 0
```

which is the **vanishing branch** of the grade gate: every surviving summand
retains a repeated seam factor and dies by alternation. Hence

```
P_12 ^ P_23 ^ P_31 = 0
```

The three centres are collinear. **QED**

## Orientation: why this covers every configuration

Classical treatments state the external-centre version of Monge and then
handle the mixed internal/external configurations as separate cases, each with
its own diagram and argument. Here the case analysis disappears, and it is
worth saying why in plain terms.

The orientation of each circle is carried by the **sign of its radius**, which
sits inside the null vector `Ci` itself. The expression `er ⌟ (Ci ^ Cj)`
therefore returns whichever centre of similitude corresponds to the two
orientations supplied:

- if `ri` and `rj` have the **same sign**, the result is the **external**
  homothety centre;
- if they have **opposite signs**, the result is the **internal** homothety
  centre.

Nothing in the two-step derivation inspects the sign of any `ri`. Step 1 is a
grade-matched stitch, Step 2 is a grade overflow; both are determined by
grades alone. The same three lines therefore prove collinearity for every
assignment of orientations to the three circles: the classical external
theorem, and each of the mixed configurations in which one or two of the
centres are taken internally.

The one configuration not covered is the case where **all three** centres are
taken internally. That is not a failure of the algebra but a property of the
statement itself: the three internal centres of similitude are not in general
collinear, and the classical theorem does not assert that they are. Only the
orientation assignments realizable as a consistent choice of signed radii are
proved collinear here, and the all-internal configuration is not among them.

## Remarks

**1. The vanishing branch is the theorem.**
The result is not obtained by computing a quantity and observing that it is
degenerate. It falls out of the grade gate directly: the accumulated seam has
outgrown the contractor, so the expression is zero for structural reasons.
What is an error condition in the algorithm is the mathematical content here.

**2. Step count.**
Two stitches: one balanced merge emitting a single scalar, one grade overflow.
No expansion into coordinates; the largest intermediate is a grade-3 wedge of
three circle vectors.

**3. Degeneracies.**
Step 1 needs `r1 != r2` for `P_12` to be a finite point (equal radii send the
homothety centre to infinity). Step 2 needs `C1, C2, C3` linearly independent
in `R^{3,2}`, which is the general-position hypothesis.
