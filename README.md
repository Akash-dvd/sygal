# Sygal

Geometric algebra expression language (operators, rewrite / canon, atoms).

This repository is the **language** layer only. Geometry applications (triangle charts, olympiad constructions, prover, etc.) live in a separate project that depends on Sygal.

## Sandhi paper

The main language-level algorithm writeup is in [`paper/sandhi/`](paper/sandhi/):

- [`draft.md`](paper/sandhi/draft.md) / [`draft.pdf`](paper/sandhi/draft.pdf) — recursive sandhi
- [`lean/`](paper/sandhi/lean/) — Lean sketches

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
