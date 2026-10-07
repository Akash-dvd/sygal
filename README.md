# Sygal

Geometric algebra expression language (operators, rewrite / canon, atoms).

This repository is the **language** layer only. Geometry applications (triangle charts, olympiad constructions, prover, etc.) live in a separate project that depends on Sygal.

## Sandhi paper

The main language-level algorithm writeup is in [`paper/sandhi/`](paper/sandhi/):

- [`draft.md`](paper/sandhi/draft.md) / [`draft.pdf`](paper/sandhi/draft.pdf) — recursive sandhi
- [`lean/`](paper/sandhi/lean/) — Lean 4 / Mathlib formalization ([status](paper/sandhi/lean/README.md))

### Formal status

The core claim of the paper is **machine-checked in Lean** (no `sorry`):
when two contraction expressions share a seam $S$, their wedge product
stitches into one expression times the Capelli pairing $(A\mid S)$, with an
exact shuffle sign — for every grade and every nesting depth. When there are
fewer contractors than seam factors, the product is zero.

| Result | Lean |
|--------|------|
| Flat stitching, any grade | `soleSeam_gradeR`, `soleSeam_vanish` |
| Nested stitching, any depth | `nested_soleSeam'`, `nested_vanish` |
| Capelli pairing $A\lrcorner S = (A\mid S)$ | `contractBlade_ofList_eq_seamPairing` |

Finding the seam inside an arbitrary expression is a search / pattern-matching
problem; the Python canonicalizer does that and is not part of the proof. Also
open: the hidden-seam regime inside nests and schedule confluence.

### View the demo

Interactive step-by-step expression walkthrough (simple → grade-r → nested). No build step.

GitHub’s **blob** view shows HTML as source — it does **not** render the page live.

**Local:** after cloning, open [`docs/sandhi/index.html`](docs/sandhi/index.html) in a browser.

**Live demo (GitHub Pages):** [https://akash-dvd.github.io/sygal/sandhi/](https://akash-dvd.github.io/sygal/sandhi/) (served from [`docs/sandhi/`](docs/sandhi/)). The site may take a minute to deploy after the first Pages enable or a push to `main`.

## Layout

Package files live at the **repository root** (`GExpr.py`, `GAtom.py`, `operators/`, …).

For `import Sygal` to work, the clone directory must be named **`Sygal`** (capital S), and its **parent** directory must be on `PYTHONPATH`.

```text
parent/                 ← put this on PYTHONPATH
  Sygal/                ← this repo (folder name matters)
    GExpr.py
    GAtom.py
    operators/
    ...
```

## Requirements

- Python 3.10+ (use `python3`)
- [sympy](https://www.sympy.org/) (runtime)
- pytest (optional, for the test suite)

Do **not** `pip install` into the system Python on Debian/Ubuntu (PEP 668). Use a venv.

## Clone and run (standalone)

```bash
cd /path/to/parent          # e.g. ~/Project/env/dev/test
gh repo clone Akash-dvd/sygal Sygal
cd Sygal
python3 -m venv .venv
source .venv/bin/activate
pip install sympy pytest

export PYTHONPATH=/path/to/parent
python -c "import Sygal; from Sygal.GExpr import GExpr; print('ok', GExpr)"
pytest -q
```

Example with a concrete parent path:

```bash
cd ~/Project/env/dev/test
gh repo clone Akash-dvd/sygal Sygal
cd Sygal
python3 -m venv .venv
source .venv/bin/activate
pip install sympy pytest
export PYTHONPATH=~/Project/env/dev/test
python -c "import Sygal; from Sygal.GExpr import GExpr; print('ok', GExpr)"
pytest -q
```

### Notes

- Folder name must be `Sygal`, not `sygal` (Linux is case-sensitive).
- A bare `GAtom('a')` is not enough; atoms need metric metadata (`mtDt`). Prefer the smoke import above.
- The suite may report some known failures while the language is still under active cleanup; a successful `import Sygal` means the standalone install is working.

## Use as a git submodule

In a parent project:

```bash
git submodule add https://github.com/Akash-dvd/sygal.git Sygal
git submodule update --init --recursive
```

Then keep the parent project root on `PYTHONPATH` (or install the package later via `pyproject.toml` when added).

Language changes: commit and push **inside** `Sygal/`, then in the parent bump the submodule pin:

```bash
cd Sygal && git push origin main && cd ..
git add Sygal && git commit -m "Bump Sygal submodule"
```

## History

Extracted from a larger monorepo with `git filter-repo`, preserving commits that touched `solver/libs/Sygal/` and `Sygal/` (from 2021 onward).

## License

All rights reserved unless otherwise stated.
