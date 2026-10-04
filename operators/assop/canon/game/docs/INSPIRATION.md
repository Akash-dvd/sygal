# Sources of inspiration

Notes behind the Sandhi / Pattern Field games: what is mathematically exact,
what is borrowed from other games and films, and what should stay unique to
this project.

Related code and pages:

- Engine: [`../gextpcanon.py`](../../gextpcanon.py), [`../gextpcapelli.py`](../../gextpcapelli.py)
- Nested identity stress test: [`../../../../../test1.py`](../../../../../test1.py)
- Playable pages: `index.html`, `field.html`, `themes.html`, `cascade.html`, `chamber.html`
- Commercial theme decision pack: [`theme/README.md`](theme/README.md)

---

## 1. The algebraic fact (home phenomenon)

The games are skins around a real rewrite that the engine already performs.

### Flat sandhi (local law)

```text
(A < (B1 ^ B2)) ^ (A < (B2 ^ B3))
  →  κ · (A < (B1 ^ B2 ^ B3))
```

Shared upper blade + shared down seam → merge; Capelli / overlap may release a
scalar `κ`.

### Nested sandhi (recursive law)

Example from `test1.py` (verified merge under current `SandhiCanon`):

```text
(d1 < (a1^a2^(d2 < (b1^b2^(d3 < (c1^c2^c3))))))
  ^
(d1 < (a3^a4^(d2 < (b3^b4^(d3 < (c1^c2^c3^c4))))))
  →
((d1^d2^d3)|(c1^c2^c3))
  ·
(d1 < (a1^a2^a3^a4^(d2 < (b1^b2^b3^b4^(d3 < (c1^c2^c3^c4))))))
```

Reading:

| Piece | Role |
|--------|------|
| Nested `d_i < (…)` | Depth / shell / annihilation tower |
| Shared deep `c…` | Seam that can fully pair |
| `(D)\|(C)` | Scalar released on collapse |
| Merged outer layers | Residual structure kept after the cascade |

This nested identity is the design north star for a “fermionic orbital cascade”
mode: **align shared depth → collapse seam → catch scalar → keep residual tower**.

---

## 2. Exact physical / mathematical homes

These are not metaphors. They justify the scalar and the residual.

| Domain | Correspondence |
|--------|----------------|
| **Exterior algebra / GA** | Wedge + left contraction; sandhi as rewrite |
| **Capelli / classical invariant theory** | Overlap scalars of the form `(D)\|(C)` |
| **Fermionic Fock space** | `a† ↔ ∧`, `a ↔ ⌋`; Slater determinants |
| **Wick’s theorem** | Shared modes pair → number; leftover operators remain |
| **String / tensor diagrams** | Cups, caps, wire bundles; Viccheda ≈ split, sandhi ≈ collect |
| **CGA / nested plates** | Pin through plate; multi-scale incidence (geometry programme) |

### What is already widely known

Wick contractions, Slater overlaps, Capelli-type identities, and “fermions =
exterior algebra” are standard.

### What is uncommon (this project’s packaging)

- Recursive **sandhi / vichcheda** as the named rewrite steps  
- Grade gate + Capelli seam coefficient as a **normal-form engine**  
- Teaching geometry concurrence and fermionic cascade as the **same merge law**

Publish / teach as method and visualization, not as “we discovered Wick.”

---

## 3. Visual languages (`themes.html`)

| Theme | Status | Use |
|-------|--------|-----|
| Subspace plate | Exact geometry | Default teaching icon: pin ⊥ plate |
| Fermionic Fock | Exact | Truth story for nested cascade + scalar |
| Observer & field | Exact\* | Electrodynamics (`Eᵤ = F·u`); simple-plane caveat |
| Thread calculus | Exact diagrammatics | Best UI for recursion / seams |
| DNA helix | Metaphor only | Game skin for match / unzip / recombine |

\*General electromagnetic `F` need not be a single plane; orthogonality to the
observer remains the right lesson.

---

## 4. Game inspirations (match the mechanism)

Steal **feel** and **pacing**, not the factory genre.

### Strongest matches (nested collapse + residual)

| Work | Steal this |
|------|------------|
| **Cocoon** | Worlds nested in orbs; carry a residual world after a transition |
| **Patrick’s Parabox** | Boxes in boxes; recursion *is* the puzzle |
| **Recursed** | Enter a container, exit with changed state (scoped nests) |
| **Shapez / Shapez 2** | Layered parts fuse by overlap; leftover composite |
| **Atomas / Suika / merge games** | Same-kind merge → higher residual + score (scalar analogue) |
| **Puyo Puyo / Puzzle Fighter** | Shared groups collapse; chain multipliers ≈ Capelli streaks |
| **Tetris Effect** | Juice language for cascade ecstasy (not the math) |
| **Gorogoa** | Nested frames align → one revealed image |
| **Baba Is You** | Rules rewrite the world (sandhi as law) |
| **Ikaruga** | Polarity / exclusion mood (±, Pauli-flavoured matching) |
| **Mini Metro** | Shared stations as seams; network simplification |

### Zachtronics (Opus Magnum, SpaceChem, …)

Use for:

- tiny rule set, deep solutions  
- watching a process execute  
- optional optimization (cycles / cost → depth / Capelli size / moves)

Do **not** clone as the core genre. Those games are **assemble a machine**.
Sandhi is **collapse shared occupancy**. The verb stays:

```text
ALIGN shared depth → COLLAPSE seam → CATCH scalar → KEEP residual tower
```

---

## 5. Animation / film inspirations

| Work | Steal this |
|------|------------|
| **Powers of Ten** (Eames) | Nested scales = shell depth |
| **Outside In** (sphere eversion) | Impossible-looking identity made watchable |
| **Not Knot** | Diagrammatic topology cinema (thread / knot skin) |
| **CERN / annihilation clips** | Pair → energy (scalar) + residual products |
| **MO / orbital hybridization animations** | Overlapping lobes decide what combines |
| **Cocoon / Manifold Garden trailers** | Nested space as beauty, not HUD |
| **Tetris Effect Zone sequences** | How Capelli fire should *feel* |

---

## 6. Design shortlist

If only three references are studied for a fermionic cascade mode:

1. **Cocoon** — nested residual worlds  
2. **Patrick’s Parabox** — recursive containment  
3. **Puyo Puyo or Tetris Effect** — cascade satisfaction  

Truth layer: **Fock + Capelli + Wick**.  
Diagram layer: **threads**.  
Delight skins: **DNA / knots** (labelled metaphor only).

---

## 7. Working title direction

Concept name used in design talk:

> **Orbital Cascade** / **Cascade Shells** / **Seam Collapse**

Core fantasy: players engineer Wick-style collapses of nested towers, score the
overlap determinant, and keep the taller residual shell — Candy Crush dopamine
with a recursive GA theorem underneath.

Implemented as `cascade.html` / `cascade.css` / `cascade.js`:

- a tile is a **nested shell tower** `d1⌋(a… ∧ d2⌋(b… ∧ d3⌋(c…)))`;
- two towers dock when the pin lineage matches and the deep cores overlap;
- the overlap contracts out as the scalar `(d1∧d2∧d3) | (c…)` — the score burst —
  and leaves the residual tower, which may dock again (the chain);
- a symbol repeated inside any wedge annihilates the term to `0`, shown as a
  dashed blue partner: alternation as a visible game hazard.

The cascade page is the *arcade* reading: it removes the contracted symbols so
chains stay bounded, which is a game-balance choice rather than the engine rule.

### 7.1 Reaction chamber — the exact reading

`chamber.html` / `chamber.css` / `chamber.js` is the slow, faithful counterpart,
and every frame it draws is computed by the engine. `bake_chamber.py` runs
`SandhiCanon.sandhi` one merge at a time over a handful of input expressions and
writes `chamber-data.json`: the panels before and after each merge, the overlap
scalar, and that scalar's signed permutation expansion from `sclrprdct.gexpand1`.

The visual language:

- a panel is an **occupation ladder** — one rung per shell, the pin on the left,
  the shell's symbols as filled slots;
- **dock** slides two ladders together and lights the shared symbols (the seam);
- **pair** draws an arc from every pin to every seam symbol — the Gram matrix of
  pin-core pairings;
- **bloom** walks the signed permutations of that matrix one at a time, lighting
  the arcs and cells of each term, then drops the determinant into the tally;
- **fuse** collapses the consumed ladders and marks the arrived symbols green.

Baked reactions: a single pairing, a two-step chain, a 2-blade seam, the depth-3
tower from `test1.py`, and the three perpendicular bisectors — whose second merge
repeats a symbol and stamps `= 0`, which is the concurrence theorem.

---

## 8. Where physicists compute these merges (links)

In physics they do not write `sandhi`, but they **do** split operator strings,
pair (contract) shared pieces to scalars, and keep a residual expression.

### 8.1 Where people actually compute the merge / split

| Link | What you will see |
|------|-------------------|
| [Wick’s theorem (Wikipedia)](https://en.wikipedia.org/wiki/Wick%27s_theorem) | Product of create/annihilate → sum of **pairings (scalars)** + **normal-ordered residual** |
| [Molinari — Notes on Wick’s theorem (PDF)](http://wwwteor.mi.infn.it/~molinari/NOTES/WICK23.pdf) | Pedagogical operator form: rearrange, contract, collect |
| [ESQC Coupled Cluster notes (PDF)](https://www.esqc.org/lectures/CC_theory_2.pdf) | Explicit fermionic contractions, signs, nested `{ABC}{XYZ}` products |
| [KIT second quantization chapter (PDF)](https://www.ipc.kit.edu/theochem/download/Kapitel2.pdf) | Worked strings like `a a† a†` → δ’s (scalars) + leftover operators |
| [Saue — Second quantization II (PDF)](https://www.esqc.org/lectures/ESQC2022_saue_secQ_partII.pdf) | Same calculus used in quantum chemistry |

The nested rewrite is closest to:

```text
string of operators
  → split into all pairings   (vichcheda / Wick)
  → each full pairing = scalar (δ / overlap / Capelli-like)
  → leftover operators = merged residual tower
```

### 8.2 Software that expands and merges these expressions

| Link | Role |
|------|------|
| [fevangelista/wickd](https://github.com/fevangelista/wickd) | Python: apply Wick, contract, collect terms (CC / MBPT style) |
| [Tutorials in that repo](https://github.com/fevangelista/wickd/tree/main/tutorials) | Step-by-step “build product → contract → latex residual” |
| [Paper on WICK&D automation](https://doi.org/10.1063/5.0097858) | Why chemists automate recursive contractions |

This is the physics analogue of `concat.sandhi` on nested towers.

### 8.3 Capelli / exterior side (closer to `(D)|(C)` scalars)

| Link | Role |
|------|------|
| [On the Proof of Capelli Identities (exterior calculus PDF)](https://www.jstage.jst.go.jp/article/fesi/51/1/51_1_1/_pdf/-char/en) | Capelli via exterior algebra — our neighbourhood |
| [arXiv: Capelli generalization](https://arxiv.org/abs/math/0610799) | Algebraic identity producing determinant-like scalars |
| [Capelli in physics & representation theory](https://doi.org/10.1088/1751-8113/48/5/055203) | Capelli used in many-particle / RPA-style settings |

### 8.4 Dictionary vs `test1` merge

| Our GA move | Physics name in those links |
|-------------|-----------------------------|
| Split nested downs | Expand / Wick expansion |
| Shared deep `c…` pairs with `d…` | Nonzero contraction `a a† → δ` / overlap |
| `((d1^d2^d3)|(c1^c2^c3))` | Fully contracted scalar block |
| Merged outer tower | Normal-ordered residual / leftover operators |

**Suggested reading order:** Molinari PDF → KIT Kapitel2 examples → `wickd` tutorials.

---

## 9. Related docs in the engine

- [`../../extsimp.md`](../../extsimp.md) — Hopf / sandhi mapping  
- [`../../status.md`](../../status.md) — fragment contract  
- [`../../tutorial.md`](../../tutorial.md) — small checked sandhi examples  
- [`../../differential_form.md`](../../differential_form.md) — forms neighbourhood  
