# Diagrammatic Geometry (III): Diagram Monoids and Monoidal Categories

Companion to [DG.md](./DG.md) (vision, feasibility) and [DG1.md](./DG1.md) (inherit vs invent). This note anchors the project in **existing** diagrammatic algebra: not “force GA into knots,” but **embed Sygal contractions and sandhi–vichcheda** in the ecosystem of diagram monoids, tensor categories, and string diagrams.

---

## What external work confirms

Research on **diagrammatic monoids** and related structures (e.g. work collected around [Matthias Fresacher’s homepage](https://matthias-fresacher.github.io/)) sits in the same landscape as this project:

- monoidal and tensor categories,
- Temperley–Lieb and Brauer (and partition) diagram algebras,
- oriented Brauer monoids,
- Kauffman-type diagram monoids,
- diagram categories with generators and rewrite presentations,
- compositional calculi (string diagrams, ZX, tensor networks).

That is **not** fringe knot aesthetics—it is a mature “algebra as process / topology diagrams” field. Your sandhi–vichcheda intuition aligns with that territory more than with classical knot theory alone.

---

## Sharpened research question

**Too broad (original):** Can knots represent our algebra?

**Better:** Can Sygal’s geometric-algebra contractions and recursive sandhi–vichcheda be embedded **faithfully** in a diagrammatic monoidal (or graded/super) category?

| Question | Status |
|----------|--------|
| Can diagrams represent algebra in general? | **Yes** — standard (Penrose, string diagrams, TL, ZX, …) |
| Can *our* recursive contraction + sandhi fragment map cleanly? | **Partially** — algebra and rewrites exist; drawable diagram IR does not |

This is sharper, more falsifiable, and easier to prototype than “build a knot game.”

---

## Already partially present (in Sygal)

The diagrammatic story is **not starting from zero**. Several layers already implement—or document—the same compositional moves that TL/string diagrams describe graphically.

| Layer | What exists | Diagram analogue | Gap |
|-------|-------------|------------------|-----|
| **Sandhi / vichcheda** | `gextpcanon.py`: merge compatible contractions, `_split_common_unique`, recursive `iter` | Canonical **compression** / **split along shared sub-diagram** | No drawable graph; runs on `GExpr` / `Box` trees |
| **Hopf semantics** | `extsimp.md`: Δ = vichcheda, sandhi = collect; contraction = pairing after coproduct | Coproduct + evaluation (tensor-network style) | Option C not fully runtime (`gextpsimp_hopf.py` falls back to Option B) |
| **Scalar / loop closure** | `CapelliOptionB.coefficient`, overlap extraction in sandhi | **Loop evaluation** / closed-wire amplitude | Virtual algebra in code, not cup–cap pictures |
| **Compositional syntax** | `GExpr` trees (`gextp`, `glcntrct`, nesting) | String-diagram **syntax tree** (composition = tree shape) | Tree ≠ embedded monoidal diagram with typed wires |
| **Rewrite calculus** | `canon_iter`, `gextpsimp`, tests in `test_gextp.py` | Diagram **rewrite to normal form** | No proof that rewrites = diagram isotopy on a chosen category |
| **Proof / construction graphs** | `GraphForest`, QGraph, `semantics_to_syntax.py` | Dependency **diagrams** (geo commands → algebra) | Different layer: construction DAG, not GA operator diagrams |
| **Legacy sketch** | `canon/docs/sandhi.drawio` | Control-flow of old sandhi loop | Not compositional semantics |

**Correct reading:** Sygal already has an **implicit diagrammatic semantics in operation**—sandhi is diagram merge, vichcheda is diagram split, coefficients are loop scalars—implemented as **term rewriting on expressions**, with a **Hopf algebraic gloss** written down.

**What is still missing** is the usual next step in the Penrose/Feynman pipeline:

1. A **diagram IR** (strands, cups, caps, boxes, grades).
2. An explicit **functor** Diagram ↔ `GExpr` on a fragment.
3. A **renderer** and game moves that edit diagrams and call `gextpcanon` for verification.

So DG2’s external literature (TL, Brauer, string diagrams) is not only “where to look”—it is largely **naming and tightening what you already do algebraically**.

---

## Knots vs process diagrams

| Diagram type | Encodes well | Weak for Sygal without extra structure |
|--------------|--------------|--------------------------------------|
| **Classical knots / links** | Global topology, Reidemeister type | Order, grade, signs, `Box` coefficients |
| **Monoidal / string / tensor** | Composition, contraction, pairing, orientation, recursion | Needs typing (graded/super) for full GA |

Sygal operators map more naturally to the second column:

| Sygal | Diagrammatic reading |
|-------|----------------------|
| `^` (exterior) | Parallel composition (tensor / braid juxtaposition) |
| `<` / `>` | Cup–cap attachment, boundary gluing, projection |
| `\|` (inner / scalar) | Loop closure, evaluation |
| Nesting | Boxes in string diagrams |
| **Vichcheda** | Split diagram along shared sub-diagram (coproduct side) |
| **Sandhi** | Canonical merge / diagram compression |
| **Coeff release** | Loop evaluation (TL / tensor-network scalar) |

You need **compositional topological semantics**, not literal knot equivalence (see [DG.md](./DG.md)).

---

## Strongest mathematical neighbors

| Structure | Role for this project |
|-----------|------------------------|
| **Temperley–Lieb** | Pairings, loops, projection idempotents; TL monoid as *-semigroup over projections (relevant to projection-heavy GA) |
| **Brauer / partition monoids** | More general pairings, partial matchings |
| **Oriented Brauer monoids** | Directional, antisymmetric pairings—closer to ordered `^` and signed contractions ([arXiv:2512.17177](https://arxiv.org/pdf/2512.17177)) |
| **String diagrams** | Compositional semantics in monoidal categories |
| **Tensor networks** | Multi-leg contraction, scalar closure |
| **Compact closed categories** | Duals for left/right contraction |
| **Kauffman / diagram monoids** | Knot-flavored composition where useful |
| **ZX calculus** | Rewrite-based diagrammatics (game moves ≈ legal rewrites) |

**Clue from presentations literature:** “Presentations for tensor categories” and TL presentations (e.g. [Temperley–Lieb presentations](https://www.researchgate.net/publication/349517863_Presentations_for_Temperley-Lieb_Algebras)) emphasize generators + relations—the same spirit as a **sound diagram calculus** for a Sygal fragment.

**Clue from sandhi:** Canonical diagram reduction in knot/tensor/string calculi parallels sandhi–vichcheda as **merge after split** toward normal form (`gextpcanon`).

---

## Working name: Diagrammatic Geometric Algebra (DGA)

A plausible target semantics (to be made precise on a fragment):

| GA concept | Diagram level |
|------------|----------------|
| Blade | Oriented boundary / typed strand |
| Wedge `^` | Parallel composition |
| Contraction `<` | Boundary gluing / cup–cap |
| Inner product `\|` | Closed evaluation loop |
| Sandhi | Canonical compression of compatible diagrams |
| Coefficient (`CapelliOptionB`) | Amplitude / loop scalar (TL or spin-network style) |

Ordinary TL may be **too symmetric** for full Sygal; **oriented** diagram monoids plus **graded/super** labels are the likely sweet spot (signs from `parity`, virtual variables from Brini—see [DG1.md](./DG1.md)).

---

## What remains unsolved (here)

Not “do diagrams exist?” and not “does sandhi behave diagrammatically?”—that behavior is **already in code**.

The frontier is **making the semantics explicit and visual**:

1. **Fragment** — freeze `test_gextp` (and chosen nested cases) as the contract.
2. **Diagram category** — objects = wire types/grades; morphisms = oriented diagrams (likely super/graded, not plain TL).
3. **Functor** — Diagram ↔ `GExpr` such that `concat.sandhi` = diagram merge and `_split_common_unique` = split; coefficients match `CapelliOptionB`.
4. **Option C (optional)** — runtime Hopf/coproduct path aligned with the same functor, not only prose in `extsimp.md`.
5. **Embodiment** — renderer + game moves verified by `gextpcanon` ([DG.md](./DG.md)).

Until (2)–(3) exist, the **game** layer is vision only; the **algebraic diagrammatic layer is already partially there**.

---

## Game and product consequence

If the embedding in §“What remains unsolved” is faithful on a fragment:

- stitch / unweave / compress = algebraically legal moves,
- reward = loop evaluation / overlap scalar,
- wide vs deep play = tensor width vs nesting depth.

The product is better described as a **diagrammatic process topology game** than a **knot game**—broader, and aligned with how monoidal diagram calculi are actually used.

---

## Study roadmap (before full knot embeddings)

Priority order for mapping Sygal:

1. Temperley–Lieb diagrams and TL monoid presentations  
2. Brauer and partition monoids  
3. Oriented Brauer diagrams ([arXiv:2512.17177](https://arxiv.org/pdf/2512.17177))  
4. String diagrams in monoidal categories
5. Penrose tensor notation
6. ZX calculus (rewrites as gameplay)  
7. Compact closed categories (duality for `<` / `>`)  
8. Diagrammatic tensor contraction / tensor networks  

Defer **general knot invariants** until a typed fragment is sound; use knots as metaphor, not as the core semantics.

Further reading examples: [Blob algebra and periodic TL](https://www.researchgate.net/publication/2071317_The_Blob_Algebra_and_the_Periodic_Temperley-Lieb_Algebra) (loop / periodic variants).

---

## Assessment

| Claim | Verdict |
|-------|---------|
| “Diagrammatic semantics is fantasy” | **No** — established field |
| “Knots alone are enough” | **No** for full Sygal |
| “Monoidal/tensor/TL family fits contractions + sandhi” | **Plausible** — sandhi/vichcheda already act like merge/split |
| “Diagrammatic behavior already in Sygal” | **Yes (partial)** — rewriting + Hopf doc + Capelli scalars |
| “Explicit diagram IR + functor” | **Not yet** — main engineering/math task |
| “Clean embedding for full recursive GA” | **Unproven** on full operator set |

You are inside a real landscape (diagram monoids, topological composition, categorical diagrammatics) **and** you already run a slice of it symbolically. The remaining work is **naming it as diagrams**, proving equivalence on a fragment, then embodiment ([DG1.md](./DG1.md)).

---

## Sygal anchors (implementation)

| Topic | Location |
|-------|----------|
| Sandhi / vichcheda (operational diagram merge/split) | `Sygal/operators/assop/canon/gextpcanon.py` |
| Hopf / coproduct reading | `Sygal/operators/assop/canon/extsimp.md` |
| Hopf backend scaffold | `Sygal/operators/assop/canon/gextpsimp_hopf.py` |
| Coefficients / virtual vars (loop scalars) | `Sygal/operators/assop/canon/gextpcapelli.py` |
| Backend selector (Option B default) | `Sygal/operators/assop/canon/gextpsimp.py` |
| Tests (fragment contract) | `Sygal/operators/assop/test/test_gextp.py` |
| Procedural sandhi flowchart (legacy) | `Sygal/operators/assop/canon/docs/sandhi.drawio` |
| Construction graphs (separate layer) | `GraphForest`, `neural_prover/algebra/semantics_to_syntax.py` |

---

## arXiv:2512.17177 — fit vs exact match

[Fresacher, Stewart, Tubbenhauer, arXiv:2512.17177](https://arxiv.org/pdf/2512.17177) (*Generalized diagram categories and monoids, and their representations*) is a strong **neighbor**, not a drop-in spec for Sygal.

| Your need | Paper provides? |
|-----------|-----------------|
| Parallel composition (`^`) | **Yes** — monoidal juxtaposition |
| Pairing / contraction | **Partially** — cups/caps, Brauer/TL matchings |
| Orientation / order | **Partially** — oriented Brauer is one example among many |
| Grades, nested GA, sandhi–vichcheda | **No** — flat rectangle diagrams + rep theory, not `gextpcanon` |
| Capelli / virtual variables | **No** |
| Game / GExpr functor | **No** |

Use it for **composition language and oriented pairings**; still build a **custom graded fragment + sandhi rewrite rules** verified against `test_gextp`.

---

## Exact diagram creation — feasibility and confidence

**Feasible: yes.** **High confidence on a defined fragment; moderate confidence for “exact” on all of Sygal.**

Here **exact** means: every legal diagram maps to a `GExpr`; every sandhi/vichcheda step matches diagram merge/split; canonical form agrees with `gextpcanon` on that fragment—not “one published paper already gives the full recipe.”

### Why confidence is reasonably high

| Factor | Role |
|--------|------|
| Algebra already diagram-like | Merge, split, scalar closure are implemented; drawing is exposition |
| `test_gextp` | Acceptance suite for “exact on this fragment” |
| `extsimp.md` | Target semantics (Δ, pairing, collect) already written |
| TL / Brauer / string diagrams | Supply **composition rules**, not guesswork |
| `gextpcanon` + `CapelliOptionB` | Oracle; diagrams explain and drive, not replace |

The task is **formalize + implement a functor on a chosen slice**, not discover unknown mathematics.

### Diagram creation methodology (feasible pipeline)

1. **Freeze fragment** — e.g. `test_gextp` sandhi cases, then one nesting depth at a time.
2. **Choose diagram kind** — oriented planar diagrams with **typed wires** (grade labels), not classical knots.
3. **Generators** — strand (1-blade), box (nested contraction), cup/cap (`<` / `>`), juxtaposition (`^`), scalar loop (`|` / coefficient).
4. **Layout rules** — how to draw `(A < (B ^ C))` (stack = compose, side-by-side = `^`).
5. **Rewrite rules** — diagram merge/split **iff** `concat.sandhi` / `_split_common_unique` on the image.
6. **Verify** — round-trip and `canon_iter(gextp)(expr) == expr_from_diagram(diagram(expr))` on the fragment.
7. **Extend** — widen only while (6) still passes.

Steps 1–6 are a **creation methodology**; focused work can complete v0 on the test fragment without years of pure research.

### Confidence by scope

| Scope | Confidence | Exact feasible? |
|-------|------------|-----------------|
| `test_gextp` sandhi fragment | **High (~80–90%)** | Yes, with test-driven iteration |
| + deep nested (D1/D2/D3-style) | **Medium–high** | Yes if grades/signs on wires are designed early |
| Full Sygal (all ops, all grades) | **Medium** | Likely a **family** of calculi, not one picture |
| Match arXiv:2512.17177 alone | **Low** | No — customize on top |

**High confidence** = a methodology that is **exact on a fragment**; **not** that one existing diagram algebra needs no extension.

### Risks (what breaks “exact”)

- Grades or signs omitted from diagrams → wrong algebra despite good art.
- Merge defined before types → visually legal, `gextpcanon` rejects.
- Scope creep → full GA before sandhi fragment is sound.
- Treating Option C / full Hopf expansion as blocking v1 — Option B + tests may suffice first.

### Practical stance

Treat **exact diagrams** as **verified functor + renderer on `test_gextp` first**. Success there justifies wider coverage; failure tells you which wire labels (orientation, grade, parity) the calculus must carry—still progress, not refutation.

**Next artifact (recommended):** one-page **Diagram creation spec v0** — generators, layout, merge = sandhi — checked against the first sandhi cases in `test_gextp`.

---

## Series map

| Doc | Focus |
|-----|--------|
| [DG.md](./DG.md) | Game vision, operator map, feasibility, commercial/patent context |
| [DG1.md](./DG1.md) | Inherit Brini/Capelli; embodiment gap |
| **DG2.md** (this) | Diagram monoids, partial presence, feasibility, arXiv:2512.17177 |
