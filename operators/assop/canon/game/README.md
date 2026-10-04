# Sandhi — The Pattern Game

A dependency-free browser game inspired by the split/merge rules in
`gextpcanon.py`.

## Run

From this directory:

```bash
python3 -m http.server 8765
```

Then open <http://localhost:8765>.

Two pages are available:

- `index.html` — five guided theorem puzzles.
- `field.html` — a Candy-Crush-style free-play field with draggable matching,
  direct Sandhi merges, Viccheda splits, cascades, and inspectable hierarchical
  terms.
- `foundry.html` — the Fermionic Foundry slice: a reactor line where packets
  dock, peel, fuse to zero, and ship against a grade contract.
- `packets.html` — Occupation Table: fermionic packet cards on a felt table.
  Pair two cards that share an occupation, cash the seam, keep the residual,
  and chain if that leftover card can pair again.
- `germ.html` — the Germ Culture slice: the *same rules* staged as biology.
  Phages drift on a dish, prime and inject each other, cut their genome, lyse
  on a repeat, and infect a host that wants an exact genome size. Built as a
  head-to-head test of which theme wins, so neither page mixes the other's
  art: the foundry stays a factory, the culture stays a plate.
- `themes.html` — an interactive comparison of geometric plates, fermionic
  Fock space, electromagnetic observer splits, string diagrams, and a DNA
  game metaphor.
- `docs/INSPIRATION.md` — algebraic sources, exact vs metaphor themes, and
  game/animation references (Cocoon, Parabox, merge/cascade games, Zachtronics
  as craft not clone).

## Game model

- **Domain:** every atomic symbol is a grade-1 vector; higher blades are ordered
  wedges of those vectors. General versors are not atomic game pieces.
- **Sandhi:** combine panels with the same upper blade and a shared lower
  symbol.
- **Viccheda:** split a chain of grade three or higher into overlapping panels.
- **Invariant:** completing a closed chain clears it as an exterior-alternation
  zero.

This interface is a teaching abstraction. `SandhiCanon` remains the source of
truth for exact GA behavior, including grade gates, parity, nested contraction,
and Capelli overlap coefficients.
