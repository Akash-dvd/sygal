# Theme decision pack

Choose **one commercial skin** and keep the algebra underneath fixed.
The engine (`SandhiCanon`, Capelli overlap, grade gate, Pauli zero) does not
change. Only how the player *sees* packets, merges, scalars, and failures.

Related:

- Inspiration notes: [`../INSPIRATION.md`](../INSPIRATION.md)
- Visual language demos: [`../../themes.html`](../../themes.html)
- Exact animation: [`../../chamber.html`](../../chamber.html)
- Arcade prototype: [`../../cascade.html`](../../cascade.html)

---

## How to decide

Score each theme on:

| Criterion | Question |
|-----------|----------|
| **Fantasy** | Would a Steam trailer sell the fantasy without saying “exterior algebra”? |
| **Readability** | Can a new player learn the rule in under 90 seconds? |
| **Juice** | Does a successful merge look and sound like a dopamine hit? |
| **Exactness** | How close is the metaphor to the real rewrite? |
| **Depth** | Can nested sandhi become a late-game mechanic, not only a tutorial? |
| **Differentiation** | Does it avoid being “another match-3” or “another Zachtronics clone”? |
| **Scope** | Can a vertical slice ship in weeks, not months? |

Commercial rule of thumb:

> Hide the symbols in the main mode. Keep the chamber / scientist view as an
> optional overlay for people who want the truth.

---

## Shortlist (decision matrix)

| Theme | Commercial fit | Exactness | Build cost | Verdict |
|-------|----------------|-----------|------------|---------|
| [Fermionic Foundry](01-fermionic-foundry.md) | ★★★★★ | ★★★★★ | Medium–high | **Primary commercial candidate** |
| [Orbital Cascade Arcade](02-orbital-cascade.md) | ★★★★ | ★★★★ | Low–medium | Strong mobile / demake companion |
| [Geometry Atlas](03-geometry-atlas.md) | ★★★ | ★★★★★ | Medium | Best for teaching / academic side |
| [Thread Loom](04-thread-loom.md) | ★★★★ | ★★★★★ | Medium | Best UI diagram language |
| [DNA Unzip](05-dna-unzip.md) | ★★★ | ★★ | Low | Skin only; do not claim biology |
| [Field Observer](06-field-observer.md) | ★★ | ★★★★ | High | Niche physics; later DLC / mode |
| [Sanskrit Sandhi](07-sanskrit-sandhi.md) | ★★ | ★★★★ | Medium | Strong brand story; weaker mainstream Steam |
| [Knot / Braid](08-knot-braid.md) | ★★ | ★★ | High | Beautiful but not the true home |

**Recommended path**

1. **Ship fantasy:** Fermionic Foundry (SpaceChem-like factory).
2. **Ship juice:** Orbital Cascade as trailer moments and tutorial “reaction feel.”
3. **Ship truth:** Geometry Atlas + Thread Loom as optional scientist skins.
4. **Avoid claiming:** DNA / knots as primary science.

---

## Shared semantic map (every theme must preserve)

Whatever the art style, these mappings stay fixed:

| Algebra | Game object |
|---------|-------------|
| Contraction panel `A⌋(…)` | Packet / tower / carrier |
| Nested shells | Depth levels the player must reach |
| Shared down symbols | Seam / dock / lock |
| Capelli / `(D)\|(C)` | Energy / coin / crystal burst |
| Residual merged panel | Output packet that continues |
| Repeated wedge symbol | Pauli overload → zero / line destroy |
| Vichcheda | Split / unzip / peel |
| Grade gate | Size filter / aperture |

If a theme cannot express **seam → scalar → residual → chain**, discard it.

---

## Files in this folder

| File | Theme |
|------|-------|
| [`01-fermionic-foundry.md`](01-fermionic-foundry.md) | Industrial Fock / reactor factory |
| [`02-orbital-cascade.md`](02-orbital-cascade.md) | Nested shell arcade / Puyo chains |
| [`03-geometry-atlas.md`](03-geometry-atlas.md) | CGA pin-through-plate / theorems |
| [`04-thread-loom.md`](04-thread-loom.md) | String diagrams / wire sewing |
| [`05-dna-unzip.md`](05-dna-unzip.md) | Helix metaphor skin |
| [`06-field-observer.md`](06-field-observer.md) | Electrodynamics observer |
| [`07-sanskrit-sandhi.md`](07-sanskrit-sandhi.md) | Pāṇinian merge/split brand |
| [`08-knot-braid.md`](08-knot-braid.md) | Knot / braid metaphor |

## Decision log

| Date | Choice | Notes |
|------|--------|-------|
| — | *undecided* | Fill when a flagship theme is locked. |

Suggested lock:

```text
Flagship fantasy : Fermionic Foundry
Reaction juice   : Orbital Cascade (in-reactor camera)
Truth skins      : Geometry Atlas + Thread Loom
Lore / naming    : Sandhi / Viccheda
Cosmetic only    : DNA, Knot
Later expansion  : Field Observer
```
