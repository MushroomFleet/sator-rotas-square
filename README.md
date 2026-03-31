# Sator Rotas Square

> *"The sower Arepo holds the wheels with care."*
> — Latin palindrome, c. 1st century CE

A complete exploration of the **Sator Rotas Square** — one of history's most enigmatic artefacts. This repository contains a grounding document, a Python implementation, an interactive React/JSX component, and a standalone HTML demo.

```
S A T O R
A R E P O
T E N E T
O P E R A
R O T A S
```

---

## What is the Sator Rotas Square?

The Sator Rotas Square (also called the Rotas-Sator Square or Templar Magic Square) is a **5×5 two-dimensional Latin palindrome** — the oldest and most widely recognised lettered word square in the Western world. First discovered at Pompeii (pre-62 CE), it consists of five five-letter Latin words that read identically in **all four directions**: left-to-right, right-to-left, top-to-bottom, and bottom-to-top.

It uses only **8 distinct letters** (A, E, N, O, P, R, S, T), possesses full transpose symmetry (it equals its own matrix transpose), and centres on **TENET** — itself a palindrome — forming a cross that has been variously interpreted as a Roman wordplay puzzle, a Jewish protective symbol, and a hidden Christian cryptogram.

In 2022, the *Encyclopaedia Britannica* called it *"the most familiar lettered square in the Western world."* Christopher Nolan's 2020 film *Tenet* uses it as a structural blueprint.

---

## Repository Contents

**Repository:** [https://github.com/MushroomFleet/sator-rotas-square](https://github.com/MushroomFleet/sator-rotas-square)

```
sator-rotas-square/
├── Sator-Rotas-Square-grounding.md    ← Rich historical & technical reference
├── Sator-Rotas-Square.py              ← Python implementation & analysis toolkit
├── Sator-Rotas-Square-demo.html       ← Standalone interactive React demo
└── README.md                          ← This file
```

---

## Grounding Document

📄 [`Sator-Rotas-Square-grounding.md`](./Sator-Rotas-Square-grounding.md)

The grounding document is the authoritative reference for everything in this repository. It covers:

- **The five words** — meanings, etymology, and the mystery of *AREPO*
- **Historical timeline** — from Pompeii (pre-62 CE) to modern pop culture, with every confirmed archaeological discovery
- **Origin theories** — Roman wordplay, Jewish Tau symbol, Christian *Pater Noster* cryptogram, Mithraic connections
- **Medieval uses** — as a cure for rabies, a fire ward, a childbirth charm
- **Mathematical structure** — point symmetry, transpose symmetry, boustrophedon reading, the TENET cross
- **Python implementation guide** — annotated code patterns for grid representation, symmetry verification, palindrome checking, path finding, cipher encoding, and word square generation

Use this document as the foundation for understanding any other file in the repository.

---

## Python Script

🐍 [`Sator-Rotas-Square.py`](./Sator-Rotas-Square.py)

A self-contained Python module and CLI demonstration with no external dependencies (pure stdlib). Run it directly for a full analysis printout, or import individual classes.

### Quick Start

```bash
python3 Sator-Rotas-Square.py
```

### What it produces

The script runs a complete demonstration covering:

1. **Both forms** displayed — SATOR (medieval) and ROTAS (ancient Roman)
2. **Word meanings** for all five Latin words
3. **All reading directions** — rows L→R, R→L; columns T→B, B→T
4. **Symmetry verification** — point symmetry, transpose symmetry, palindrome checks
5. **Letter frequencies** — 25 letters, only 8 distinct
6. **Pater Noster analysis** — arithmetic verification of the anagram theory
7. **TENET cross** — highlighted in ASCII display
8. **Word path finding** — all valid straight-line paths spelling each word
9. **Boustrophedon reading** — the zigzag reading that eliminates AREPO
10. **Cipher demonstration** — Polybius-style positional encoding
11. **Transformation gallery** — rotations, reflections, transpose

### Importable Classes

```python
from Sator-Rotas-Square import SatorSquare, SatorCipher

# Create either form
sq = SatorSquare('SATOR')   # or 'ROTAS'

# Palindrome verification
print(sq.symmetry_report())

# Find all paths spelling a word
print(sq.find_word_paths('TENET'))

# Encode text using grid positions
cipher = SatorCipher(sq)
print(cipher.encode_to_string('SATOR'))   # → '00 01 02 03 04'

# Transform
rotated    = sq.rotate(1)          # 90° clockwise
flipped    = sq.flip_horizontal()
transposed = sq.transpose()

# Highlight the TENET cross
cross = sq.tenet_cross_positions()
print(sq.display(highlight=set(cross['cross'])))
```

### Utility Functions

```python
from Sator-Rotas-Square import (
    find_word_squares,          # Search any word list for Sator-type squares
    read_boustrophedon,         # Zigzag reading of any 5×5 grid
)
```

---

## Interactive Demo

🌐 [`Sator-Rotas-Square-demo.html`](./Sator-Rotas-Square-demo.html)

A fully self-contained HTML file. Open it in any modern browser — no server, no build step, no dependencies to install. React and Babel are loaded from CDN.

### How to use

```bash
# Just open the file
open Sator-Rotas-Square-demo.html

# Or serve locally
python3 -m http.server 8080
# then visit http://localhost:8080/Sator-Rotas-Square-demo.html
```

### Features

The demo is built as a React/JSX component with six interactive tabs:

| Tab | What it shows |
|---|---|
| **The Words** | Click any word to highlight its row and column in the grid; see etymology and meaning |
| **Readings** | All four cardinal reading directions; boustrophedon reading with explanation |
| **Symmetry** | All symmetry properties verified with a ✓/✗ grid |
| **History** | Full chronological timeline from 62 CE to 2022 |
| **Pater Noster** | The 1926 anagram theory with the cross visualised |
| **Cipher** | Live Polybius-style encoder — type any text and watch grid cells illuminate |

The grid responds to mode changes with cell highlighting:

- **Gold** — selected word's row and column
- **Red** — TENET cross positions  
- **Green** — all cells (Pater Noster mode)
- **Purple** — cipher input letter positions

Toggle between **SATOR** and **ROTAS** forms using the form buttons below the grid.

### JSX Component

The demo's component (`SatorSquare` in the HTML) is written in modern JSX and can be extracted and used in any React project. The component is self-contained with its own data, logic, and inline styles. Copy the `<script type="text/babel">` block, adjust imports, and drop it into any React app.

---

## How It Works

### The Palindrome

The square's defining property is that `grid[r][c] == grid[c][r]` (transpose symmetry) and `grid[r][c] == grid[4-r][4-c]` (point symmetry). These two constraints together mean the same five words appear in every row and every column, in both reading directions.

```
Reading L→R:  SATOR AREPO TENET OPERA ROTAS
Reading T→B:  SATOR AREPO TENET OPERA ROTAS  ← identical
Reading R→L:  ROTAS OPERA TENET AREPO SATOR
Reading B→T:  ROTAS OPERA TENET AREPO SATOR  ← identical
```

### The TENET Cross

The central word TENET occupies row 2 (horizontal) and column 2 (vertical), forming a cross at their intersection. TENET is itself a palindrome, making the cross readable in all directions from the centre cell N.

### The Pater Noster Theory

The 25 letters (A×4, E×4, O×4, R×4, T×4, N×1, P×2, S×2) can be rearranged so that PATERNOSTER appears twice in cross form, with A and O remaining — representing Alpha and Omega. This works because PATERNOSTER×2 requires exactly 22 letters (P×2, A×2, T×4, E×4, R×4, N×2, O×2, S×2 — but note N only appears once in the grid, making the theory rely on the shared cross-centre).

---

## Key Facts at a Glance

| Property | Value |
|---|---|
| Dimensions | 5×5 |
| Total cells | 25 |
| Distinct letters | 8 (A E N O P R S T) |
| Oldest known example | Pompeii, pre-62 CE |
| Form | ROTAS (ancient) / SATOR (medieval) |
| Symmetries | Point symmetry, transpose symmetry |
| Palindromic words | TENET (the only one) |
| Reading directions | 4 cardinal (all yield same words) |
| Known archaeological finds | 10+ across Europe and Middle East |

---

## References

- Wikipedia — [Sator Square](https://en.wikipedia.org/wiki/Sator_Square)
- Encyclopaedia Britannica (2022) — "the most familiar lettered square in the Western world"
- Fishwick, D. (1964). "On the origin of the Rotas-Sator Square." *Harvard Theological Review* 57(1), 39–53
- Sheldon, R.M. (2003). "The sator rebus: an unsolved cryptogram?" *Cryptologia* 27(3), 233–287
- Baines, W. (1987). "The Rotas-Sator Square: a new investigation." *New Testament Studies* 33(3), 469–476
- Nolan, C. (dir.) (2020). *Tenet*. Warner Bros.

---

## Licence

MIT — use freely, cite where appropriate.

---

## 📚 Citation

### Academic Citation

If you use this codebase in your research or project, please cite:

```bibtex
@software{sator_rotas_square,
  title = {Sator Rotas Square: A Python & Interactive Exploration of the Ancient Latin Palindrome},
  author = {Drift Johnson},
  year = {2025},
  url = {https://github.com/MushroomFleet/sator-rotas-square},
  version = {1.0.0}
}
```

### Donate

[![Ko-Fi](https://cdn.ko-fi.com/cdn/kofi3.png?v=3)](https://ko-fi.com/driftjohnson)

---

*SATOR · AREPO · TENET · OPERA · ROTAS*
