# Diagrammatic Geometry: Sandhi–Vichcheda Game Vision

A design note for representing Sygal’s recursive geometric algebra through compositional topology—threads, braids, stitch networks, and compression-as-play—without equating the system with classical knot theory.

---

## Purpose

We ask whether the algebra already implemented in Sygal—exterior products, left/right contractions, inner products, nested contraction chains, and sandhi–vichcheda canonicalization—admits a **faithful diagrammatic semantics**: one where equivalent expressions correspond to equivalent diagrams, rewrites look like geometric deformations, and composition is visible continuity.

The target is **not** a symbolic-algebra game with cosmetic graphics.

The target **is** an emergent game whose **topology carries the same compositional laws** as the algebra: the player manipulates continuity; canonicalization releases scalar reward.

---

## What we already have (Sygal)

### Recursive compositional algebra

Expressions are built from graded blades, contractions, and wedges. Sandhi merges compatible terms; vichcheda splits shared structure apart before recomposition.

**Sandhi rule (schematic):**

```text
(A < (B ^ C)) ^ (A < (C ^ D))  →  coeff · (A < (B ^ C ^ D))
```

**Reading:** two structures share hidden continuity `C`; the seam is extracted; geometry compresses into one contraction; a scalar overlap (`coeff`) is released. Implementation: `gextpcanon.concat.sandhi`, coefficients via `CapelliOptionB` (`gextpcapelli.py`). Tests: `Sygal/operators/assop/test/test_gextp.py`.

**Vichcheda (schematic):** at each level, split down-blades into common + unique parts, track reorder signs (`parity`), recurse on nested common contractions, then sandhi-merge. Documented algebraically as a Hopf-style split in `Sygal/operators/assop/canon/extsimp.md`.

### Depth and breadth of structure

| Shape | Algebraic character | Natural visual metaphor |
|-------|---------------------|-------------------------|
| **Wide** | Lateral `^`-chains, many parallel blades, distributed fabric | Braid strips, woven membranes, parallel strand nets |
| **Deep** | Nested `<` inside `^`, recursive embedding | Nested boxes, folded strands, “compression towers” |
| **Composite** | Shared crossing region + large-scale merge + scalar release | Braid compression, loop closure, resonance burst |

Deep example (from tests / docs):

```text
(D1 < (A1 ^ A2 ^ (D2 < (B1 ^ B2 ^ (D3 < (C1 ^ C2 ^ C3))))))
 ^
(D1 < (A3 ^ A4 ^ (D2 < (B3 ^ B4 ^ (D3 < (C1 ^ C2 ^ C3 ^ C4))))))
  →  ((D1 ^ D2 ^ D3) | (C1 ^ C2 ^ C3)) * (single merged contraction tree)
```

---

## Central insight

Sandhi–vichcheda already behaves like:

- continuity extraction along a shared seam,
- recursive stitching of compatible pieces,
- topological compression to a canonical form,
- release of a scalar coefficient from hidden overlap.

So the algebra may already possess a **hidden diagrammatic semantics**—not yet drawn as a formal calculus, but present in the rewrite rules and Hopf/coproduct reading (vichcheda ≈ split along Δ; sandhi ≈ collect compatible branches).

---

## The main mathematical question

Can primitive GA operators map **faithfully** (not merely metaphorically) to diagrammatic generators?

| Operation | Diagrammatic role (target semantics) |
|-----------|--------------------------------------|
| Exterior product `^` | Parallel composition of strands / tensoring of blades |
| Left contraction `<` | Strand attachment, cup–cap, projection onto a blade |
| Right contraction `>` | Reverse attachment (dual cup–cap orientation) |
| Inner product `\|` | Closed loop, evaluation, scalar closure |
| Associativity of valid merges | Isotopy / diagram equivalence in the allowed calculus |
| Recursive nesting | Boxes inside boxes (hierarchical string diagrams) |
| **Sandhi** | Canonical merge of diagrams sharing a sub-diagram |
| **Vichcheda** | Split along shared sub-diagram; expose common vs unique strands |

### What “faithful” means here

We do **not** require Reidemeister equivalence for arbitrary knots.

We **do** require:

1. Same canonical algebraic normal form ⇒ same diagram (up to legal deformation).
2. Legal rewrites ⇒ visible diagram moves (stitch, unweave, compress).
3. Composition in the game = composition in Sygal on a defined fragment.

Signs, grades, and `Box` coefficients must appear on diagrams (typed, oriented, graded strands)—not as afterthoughts.

---

## Mathematical neighbors (where to look)

| Area | Use for this project |
|------|----------------------|
| **String diagrams** | Compositional semantics for monoidal / graded categories |
| **Temperley–Lieb** | Pairings and contractions as cups/caps |
| **Tensor networks** | Wide fabrics, contraction networks, scalar loops |
| **Hopf algebras** | Vichcheda/sandhi as coproduct split and collect (already in `extsimp.md`) |
| **Braid groups** | Ordered `^`-chains; order matters (non-commutativity) |
| **ZX calculus** | Rewrite-as-game; scalars as phases / rewards |
| **Rational tangles** | Recursive composition of low-complexity topological pieces |
| **Knot theory** | Metaphor for continuity; **not** a full encoding of Sygal without extra structure |

Brini-style virtual variables and Capelli devirtualization (`gextpcapelli.py`, Brini 2015 arXiv:1501.03639) supply the **coefficient / sign** side of diagrams, not classical knot invariants.

The end state could be a **diagrammatic geometric algebra calculus**: a specialized string-diagram fragment plus sandhi–vichcheda rewrite laws, sound against `gextpcanon`.

---

## What exists vs what is missing

| Layer | Status |
|-------|--------|
| Sandhi/vichcheda engine | Implemented (`gextpcanon.py`, Option B default in `gextpsimp.py`) |
| Hopf / coproduct reading | Documented (`extsimp.md`); Option C scaffold only (`gextpsimp_hopf.py`) |
| Geometry → algebra (proof graph) | `GraphForest` / QGraph, `semantics_to_syntax.py` (Sem → Syn) |
| **Diagram IR + GExpr ↔ diagram** | **Not built** |
| Game / renderer | **Not built** |
| `sandhi.drawio` | Control-flow sketch of old sandhi loop, not compositional semantics |

---

## Game vision

The player does not edit formulas. The player manipulates:

- threads and braids,
- luminous strands and membranes,
- stitch networks and recursive knots (in the **diagram** sense: nested compositional boxes, not only classical knots).

### Core actions

| Player action | Algebraic meaning |
|---------------|-------------------|
| **Stitch** | Sandhi merge |
| **Unweave** | Vichcheda split |
| **Align** | Contraction compatibility (shared upper blade / seam) |
| **Braid** | Exterior composition `^` |
| **Compress** | Run canonicalization (`canon_iter` / sandhi exhaust) |
| **Release** | Extract scalar overlap (coefficient reward) |

### Reward

Compression releases light, resonance, harmony—or plainly: **the coefficient** from overlap extraction. More elegant, recursive, and globally compressed structures yield larger scalar release. Algebraic beauty becomes gameplay reward when the diagram calculus matches `CapelliOptionB` / normal form.

### Playstyles

- **Wide:** distributed braid nets, lateral continuity, modular fabrics.
- **Deep:** nested contractions, compression towers, high nested coefficient release.
- **Mixed:** woven ecosystems; local stitch vs global canonical form.

---

## Feasibility (honest scope)

**Possible**

- Phenomenological diagrammatic semantics for a **fragment** (sandhi test shapes, then depth).
- Game whose moves are sandhi, vichcheda, and canonicalization, with win/equilibrium = normal form.
- Wide/deep visuals as tensor networks and nested string diagrams.

**Partial / requires design**

- Full Sygal (all grades, signs, `Box`, inv/proj/rej) on one untyped knot picture.
- Classical knot invariants as the sole semantics—order, grade, and parity need explicit diagram data.

**Recommended path**

1. Define a **diagram AST** (strands, cups, caps, boxes, scalar loops) for the `test_gextp` sandhi fragment.
2. Implement `GExpr → Diagram` and partial inverse; prove round-trip on tests.
3. Prototype stitch/unweave/compress on 2–3 blade merges; reward = released scalar.
4. Extend depth and visuals once soundness matches `gextpcanon`.

---

## Unified goal

Discover a **phenomenologically meaningful diagrammatic semantics** for recursive geometric-algebra composition such that:

- algebra (Sygal rewrites),
- topology (diagram equivalence),
- visuals (threads, fabrics, knots-as-boxes),
- emergence (complexity from few primitives),
- gameplay (stitch, compress, release)

are different views of **one compositional system**—not five ad hoc layers.

If the primitive operators map correctly on a sound fragment, later complexity can emerge the way it does in mathematics: from composition laws, not from hand-authored special cases.

---

## References (in-repo)

| Topic | Location |
|-------|----------|
| Sandhi / vichcheda implementation | `Sygal/operators/assop/canon/gextpcanon.py` |
| Capelli / virtual variables (coefficients) | `Sygal/operators/assop/canon/gextpcapelli.py` |
| Hopf mapping | `Sygal/operators/assop/canon/extsimp.md` |
| Tests | `Sygal/operators/assop/test/test_gextp.py` |
| Procedural sandhi sketch (legacy) | `Sygal/operators/assop/canon/docs/sandhi.drawio` |
