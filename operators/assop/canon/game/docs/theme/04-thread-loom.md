# Theme 04 — Thread Loom

**Working titles:** Thread Calculus · Seam Loom · Wireworks

**Role:** Best diagrammatic UI language; strong secondary skin.

**Implemented:** [`../../loom.html`](../../loom.html) with
[`../../loom.js`](../../loom.js) and [`../../loom.css`](../../loom.css).

---

## Fantasy

Expressions are **thread bundles**. Sandhi is sewing shared strands together.
Vichcheda is cutting / unzipping a seam. The Capelli scalar is a knot of paired
threads that falls off as a bead of light.

---

## Visual language

| Algebra | Look |
|---------|------|
| Blade factors | Coloured threads |
| Wedge | Parallel bundle |
| Contraction | Thread pulled through a ring |
| Seam | Threads that can be cupped together |
| Scalar | Closed cups / pairing beads |
| Residual | Remaining open wires |
| Nested towers | Braided cables with depth tags |

---

## Strengths

- Exact string-diagram / tensor-network feel.
- Recursion and seams are *visible* without orbitals.
- Excellent for a 2D puzzle UI (drag wires, snap seams).

## Weaknesses

- Less cinematic than orbitals / factories for trailers.
- Can look abstract / academic if colour and motion are weak.
- Players may confuse it with knot games (see theme 08).

---

## Commercial use

- Default “serious mode” board renderer inside the foundry.
- Expert editor for sharing recipes as diagrams.
- Paper-friendly screenshots.

## Implemented game loop

- Five progressively unlocked patterns are loaded from `chamber-data.json`, so
  each accepted stitch, scalar and residual comes from a real `SandhiCanon`
  trace rather than a second JavaScript algebra.
- The board is a single SVG. A panel is drawn as a chain of contraction nodes
  (one small ring per pin, connected by a trunk) with one open leg per wedge
  factor fanning out of each ring. No cards, no boxes: only nodes and wires.
- Paired panels face each other across a central gutter, so shared legs point
  at their twins and a stitch reads as composition of two diagrams.
- The player drags (or click-selects) one loose leg end onto its twin in the
  facing diagram.
- A correct seam bends every shared leg into a **cup**; the closed loop that
  forms is exactly the overlap scalar, and it lifts off into the shuttle as a
  bead. Both diagrams are then replaced by the baked residual.
- Wrong stitches fray the loom, cost moves and lower the grade.
- The final bisector pattern intentionally repeats a strand and stamps `= 0`.
- An optional **Inspect** tool exposes the symbolic engine input and target;
  the normal play surface remains diagram-first.

---

## Decision notes

Prefer as **UI language** under the Fermionic Foundry fantasy, not as a separate
store page identity—unless targeting math-diagram audiences.
