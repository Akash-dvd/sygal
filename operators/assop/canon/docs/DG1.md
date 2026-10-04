# Diagrammatic Geometry (II): Inherit, Adapt, Embody

Companion to [DG.md](./DG.md). Corrects a common overreach: Brini/Capelli and related theory are **not** “just symbolic manipulation.” The open problem is usually **not** inventing new algebra from zero—it is **choosing and embodying** a faithful compositional semantics that players can see and touch.

---

## The right question

Do we need to **invent** a new diagrammatic calculus?

Or can we **inherit and adapt** one that already exists for virtual variables, contractions, and canonical reduction?

**Working answer:** adaptation and reinterpretation—not invention from scratch.

| Layer | Status |
|-------|--------|
| Formal algebra (Sygal, sandhi, Capelli coefficients) | In repo |
| Combinatorial / superalgebra semantics (Brini, tableaux, pairings) | Published; partially implemented in `gextpcapelli.py` |
| Tensor-like contractions, Hopf split/collect | Documented in `extsimp.md` |
| Formal string / tensor diagrams | Standard math; not wired to Sygal UI |
| **Phenomenological continuity (game / intuitive topology)** | **Missing** |

Originality likely sits in the **last row**: making topology visible and playable, not in rediscovering Capelli’s identity.

---

## What Brini-style algebra already carries

Virtual-variable methods (Brini 2015; lineage in PNAS 1990/1993) already encode:

- combinatorial pairing and contraction structure,
- antisymmetry and permutation signs,
- balanced creation–annihilation monomials,
- tableaux-like organization,
- devirtualization (Capelli epimorphism),
- Hopf-flavored split/collect behavior (your vichcheda/sandhi reading).

Sygal’s Option B path (`CapelliOptionB`: balanced monomials, adjoint expansion, `coefficient`) is an **algorithmic** slice of that territory—not a separate symbolic trick.

**What it was built for:** algebraic computation and proof-style reduction.

**What it was not built for:** embodied continuity, game feel, or player-facing seam/stitch metaphors.

That gap is the **missing layer**—not the underlying mathematics.

---

## Formal vs phenomenological semantics

Existing diagrammatics in Capelli theory, superalgebra, invariant theory, tensor calculus, Hopf algebras, and category theory tend to be:

- formal and expert-oriented,
- dense in notation,
- correct but not visually or emotionally continuous.

The DG program asks for something rarer:

> **Intuitive, continuity-preserving phenomenological semantics**—same structure, different embodiment.

| Expert sees | Player could see |
|-------------|----------------|
| Balanced monomial pairings | Two braid halves sharing a middle strand |
| Common/unique split (vichcheda) | Unweave along a visible seam |
| Sandhi merge | Stitch; fabric pulls tight |
| Scalar from `CapelliOptionB` | Light / resonance released from a closed loop |

Same compositional laws; different projection onto perception. That projection is a **design and engineering** problem, not a new theorem.

---

## Why sandhi–vichcheda invites topology

Sandhi–vichcheda in `gextpcanon` already behaves more geometrically than many purely syntactic rewrite systems:

- **Shared structure extraction** — find the common sub-blade (seam).
- **Recursive factorization** — peel nested contractions level by level.
- **Canonical recomposition** — one merged term plus overlap scalar.

Those operations resemble continuity manipulation, seam detection, and compression more than they resemble “replace substring A with B.” The knot/braid intuition in DG.md is a **natural reading**, not an arbitrary skin—provided diagrams are typed, ordered, and grade-aware (see DG.md feasibility section).

Brini-style systems already have **implicit** topology via pairings, signs, and virtual balancing. The leap is:

> Can that topology become **explicit, visible, and playable**?

---

## Historical parallel (symbol → geometry)

Several fields moved from index-heavy algebra to diagrammatic embodiment:

| Before | After |
|--------|--------|
| Tensor indices | Penrose diagrams |
| Quantum amplitudes | Feynman / ZX diagrams |
| Categorical composition | String diagrams |
| Invariants of links | Knot / tangle diagrams |

Pattern: symbolic algebra stabilizes first; **geometry follows** as a faithful projection. Sygal + sandhi may be at a similar transition: algebra and canon engine exist; a minimal visual calculus does not.

---

## What is *not* merely combinatorial

Sygal’s fragment is **recursive compositional geometry**: nested `<` inside `^`, accumulated blades across recursion, scalar release at each merge. That is why threads, braids, stitching, and “fabric” metaphors attach without forcing.

Coefficient extraction via overlap pairings is close to:

- tensor-network contraction,
- Temperley–Lieb loop evaluation,
- spin-network amplitude closure.

So the game vision sits in **real** mathematical territory—not a decorative skin on arbitrary rewrite rules.

---

## Research problem (precise)

Avoid asking: *“Does the exact game diagram already exist in a textbook?”*

Ask instead:

> **Is there a mathematically faithful compositional semantics we can embody visually—and if so, what is the minimal calculus?**

**Likely answer:** yes, **partially**, as a hybrid of:

- geometric algebra (blades, grades, contractions),
- string / tensor diagrams (composition, cups, caps),
- Temperley–Lieb–style pairings,
- ordered braid-like structure for `^`,
- superalgebra combinatorics for signs (virtual variables),
- recursive rewrite systems (sandhi / vichcheda / `canon_iter`).

**Unlikely need:** entirely new algebra.

**Likely need:** a **new playable projection** of existing compositional algebra onto continuity, chunks, and reward—still sound against `gextpcanon` on a defined fragment.

---

## Why embodiment is still hard

Games require:

- perceptual chunking (what is one “move”?),
- visual continuity (strands don’t lie),
- feedback (compression → reward),
- learnability without GA notation.

Mathematical notation and Brini’s virtual variables supply **truth**; they do not supply **feel**. Embodiment—IR, renderer, level design, verified moves—is the expensive layer. DG.md outlines product direction; this note clarifies **what not to reinvent**.

---

## Pipeline (conceptual)

```text
[Published: Brini / Capelli / Hopf / string diagrams]
            ↓ adapt (choose fragment, types, signs)
[Formal: diagram AST ↔ GExpr on test fragment]
            ↓ verify (round-trip, sandhi = stitch)
[Engine: Sygal gextpcanon + CapelliOptionB]
            ↓ embody (art, UX, game loop)
[Phenomenology: stitch, unweave, compress, release]
```

Only the bottom box is greenfield for product; the rest is integration and design discipline.

---

## Honest assessment

| Claim | Verdict |
|-------|---------|
| “We invented new mathematics” | Weak; heavy prior art |
| “We need a new formal calculus from zero” | Probably no |
| “We need a faithful visual calculus + game embodiment” | Yes; potentially original and deep |
| “Knot theory alone is the semantics” | No for full Sygal; yes as metaphor in a typed fragment |

**Strongest position:** discover the **right phenomenological projection** of algebra you already implement—not replace Brini, but **make his structure playable** on top of sandhi–vichcheda and Capelli coefficients.

If that minimal calculus is found and kept sound, emergent complexity (wide fabrics, deep towers, mixed ecosystems) can follow from composition laws—the same way depth in DG.md’s game vision follows from a few primitives.

---

## See also

- [DG.md](./DG.md) — game vision, operator map, feasibility, in-repo references
- `Sygal/operators/assop/canon/extsimp.md` — Hopf / sandhi mapping
- `Sygal/operators/assop/canon/gextpcapelli.py` — Brini-style balanced monomials and devirtualization
