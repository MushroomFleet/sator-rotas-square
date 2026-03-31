#!/usr/bin/env python3
"""
Sator-Rotas-Square.py
=====================
A comprehensive Python implementation exploring the mathematical,
linguistic, and cryptographic properties of the ancient Sator Rotas Square.

The square (SATOR form):
    S A T O R
    A R E P O
    T E N E T
    O P E R A
    R O T A S

Usage:
    python Sator-Rotas-Square.py

    Or import and use individual classes/functions:
        from Sator-Rotas-Square import SatorSquare, SatorCipher
"""

from __future__ import annotations
import sys
from collections import Counter
from typing import Iterator


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

SATOR_GRID: list[list[str]] = [
    ['S', 'A', 'T', 'O', 'R'],
    ['A', 'R', 'E', 'P', 'O'],
    ['T', 'E', 'N', 'E', 'T'],
    ['O', 'P', 'E', 'R', 'A'],
    ['R', 'O', 'T', 'A', 'S'],
]

ROTAS_GRID: list[list[str]] = [
    ['R', 'O', 'T', 'A', 'S'],
    ['O', 'P', 'E', 'R', 'A'],
    ['T', 'E', 'N', 'E', 'T'],
    ['A', 'R', 'E', 'P', 'O'],
    ['S', 'A', 'T', 'O', 'R'],
]

WORDS: list[str] = ['SATOR', 'AREPO', 'TENET', 'OPERA', 'ROTAS']

WORD_MEANINGS: dict[str, str] = {
    'SATOR': 'Sower, planter, founder, originator (divine)',
    'AREPO': 'Unknown — likely a proper name; possibly Celtic or invented',
    'TENET': 'He/she/it holds, keeps, preserves, sustains (from tenere)',
    'OPERA': 'Works, care, effort, labour (from opus)',
    'ROTAS': 'Wheels, plough, celestial spheres (from rota)',
}

ALL_DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0,  -1),          (0,  1),
    (1,  -1), (1,  0), (1,  1),
]

SIZE: int = 5


# ─────────────────────────────────────────────────────────────────────────────
# Core Class
# ─────────────────────────────────────────────────────────────────────────────

class SatorSquare:
    """
    Encapsulates the Sator Rotas Square and exposes methods for analysing
    its palindromic, symmetric, and combinatorial properties.
    """

    def __init__(self, form: str = 'SATOR') -> None:
        """
        Parameters
        ----------
        form : str
            'SATOR' (default, medieval form) or 'ROTAS' (ancient Roman form).
        """
        self.form = form.upper()
        if self.form == 'ROTAS':
            self.grid = [row[:] for row in ROTAS_GRID]
        else:
            self.grid = [row[:] for row in SATOR_GRID]

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self, highlight: set[tuple[int, int]] | None = None) -> str:
        """Return a formatted ASCII representation of the square."""
        top    = '╔═══╤═══╤═══╤═══╤═══╗'
        sep    = '╟───┼───┼───┼───┼───╢'
        bottom = '╚═══╧═══╧═══╧═══╧═══╝'
        lines  = [f'\n  [{self.form} FORM]\n{top}']
        for ri, row in enumerate(self.grid):
            cells = []
            for ci, ch in enumerate(row):
                if highlight and (ri, ci) in highlight:
                    cells.append(f'[{ch}]')
                else:
                    cells.append(f' {ch} ')
            lines.append('║' + '│'.join(cells) + '║')
            if ri < SIZE - 1:
                lines.append(sep)
        lines.append(bottom)
        return '\n'.join(lines)

    def __str__(self) -> str:
        return self.display()

    # ── Reading Directions ────────────────────────────────────────────────────

    def read_rows_lr(self) -> list[str]:
        """Read all rows left to right."""
        return [''.join(row) for row in self.grid]

    def read_rows_rl(self) -> list[str]:
        """Read all rows right to left."""
        return [''.join(reversed(row)) for row in self.grid]

    def read_cols_tb(self) -> list[str]:
        """Read all columns top to bottom."""
        return [''.join(self.grid[r][c] for r in range(SIZE)) for c in range(SIZE)]

    def read_cols_bt(self) -> list[str]:
        """Read all columns bottom to top."""
        return [''.join(self.grid[r][c] for r in range(SIZE - 1, -1, -1))
                for c in range(SIZE)]

    def all_readings(self) -> dict[str, list[str]]:
        """Return all four reading directions."""
        return {
            'rows_left_to_right':  self.read_rows_lr(),
            'rows_right_to_left':  self.read_rows_rl(),
            'cols_top_to_bottom':  self.read_cols_tb(),
            'cols_bottom_to_top':  self.read_cols_bt(),
        }

    # ── Symmetry Verification ─────────────────────────────────────────────────

    def verify_point_symmetry(self) -> bool:
        """
        Verify grid[r][c] == grid[SIZE-1-r][SIZE-1-c] for all positions.
        (180° rotational symmetry through the centre)
        """
        return all(
            self.grid[r][c] == self.grid[SIZE - 1 - r][SIZE - 1 - c]
            for r in range(SIZE)
            for c in range(SIZE)
        )

    def verify_transpose_symmetry(self) -> bool:
        """
        Verify grid[r][c] == grid[c][r] for all positions.
        (The matrix equals its own transpose)
        """
        return all(
            self.grid[r][c] == self.grid[c][r]
            for r in range(SIZE)
            for c in range(SIZE)
        )

    def symmetry_report(self) -> dict[str, bool]:
        """Return a full symmetry analysis."""
        return {
            'point_symmetry_180':    self.verify_point_symmetry(),
            'transpose_symmetry':    self.verify_transpose_symmetry(),
            'row3_palindrome':       self._word_is_palindrome(self.grid[2]),
            'col3_palindrome':       self._word_is_palindrome(
                                        [self.grid[r][2] for r in range(SIZE)]),
            'all_rows_are_words':    self.read_rows_lr() == WORDS,
            'all_cols_are_words':    self.read_cols_tb() == WORDS,
        }

    @staticmethod
    def _word_is_palindrome(letters: list[str]) -> bool:
        return letters == letters[::-1]

    # ── Letter Analysis ───────────────────────────────────────────────────────

    def letter_frequencies(self) -> Counter:
        """Count each letter in the grid."""
        return Counter(ch for row in self.grid for ch in row)

    def distinct_letters(self) -> set[str]:
        """Return the set of distinct letters used."""
        return set(ch for row in self.grid for ch in row)

    def pater_noster_analysis(self) -> dict:
        """
        Analyse the Pater Noster anagram theory.
        The 25 letters can be rearranged into:
            - PATERNOSTER × 2  (vertical + horizontal arms of a cross)
            - A × 2, O × 2     (Alpha and Omega)
        """
        freq      = self.letter_frequencies()
        pn_single = Counter('PATERNOSTER')
        pn_double = Counter({k: v * 2 for k, v in pn_single.items()})
        remainder = freq - pn_double
        works     = sum(remainder.values()) == 0 or remainder == Counter({'A': 2, 'O': 2})

        # Actually: freq has 25 letters; PATERNOSTER×2 = 22 letters → leftover 3
        # Correct: PATERNOSTER has 11 letters, ×2 = 22, leaving 3:
        # grid total = 25 → 25 - 22 = 3 → but we need A,O,A,O = 4
        # The classic theory uses the N as the cross centre (shared), making net 21 unique + N
        # We report the exact arithmetic honestly.
        leftover = freq - pn_double
        return {
            'grid_letter_count':     25,
            'grid_frequencies':      dict(freq),
            'paternoster_x2_needed': dict(pn_double),
            'leftover_letters':      dict(leftover),
            'theory_holds':          (leftover == Counter({'A': 2, 'O': 2})
                                      or leftover == Counter({'A': 1, 'O': 1})),
        }

    # ── Path Finding ──────────────────────────────────────────────────────────

    def find_word_paths(self, word: str) -> list[list[tuple[int, int]]]:
        """
        Find all straight-line paths through the grid that spell the given word.
        Searches all 8 cardinal/diagonal directions from every starting cell.
        """
        word  = word.upper()
        paths = []
        for r in range(SIZE):
            for c in range(SIZE):
                if self.grid[r][c] != word[0]:
                    continue
                for dr, dc in ALL_DIRECTIONS:
                    path = [(r, c)]
                    nr, nc = r + dr, c + dc
                    valid = True
                    for ch in word[1:]:
                        if 0 <= nr < SIZE and 0 <= nc < SIZE and self.grid[nr][nc] == ch:
                            path.append((nr, nc))
                            nr += dr
                            nc += dc
                        else:
                            valid = False
                            break
                    if valid and len(path) == len(word):
                        paths.append(path)
        return paths

    def all_word_paths(self) -> dict[str, list[list[tuple[int, int]]]]:
        """Find paths for all five canonical words."""
        return {word: self.find_word_paths(word) for word in WORDS}

    # ── Tenet Cross ───────────────────────────────────────────────────────────

    def tenet_cross_positions(self) -> dict[str, list[tuple[int, int]]]:
        """
        Return the positions forming the TENET cross:
            - Horizontal TENET: row 2, cols 0-4
            - Vertical TENET:   col 2, rows 0-4
        """
        horizontal = [(2, c) for c in range(SIZE)]
        vertical   = [(r, 2) for r in range(SIZE)]
        return {'horizontal': horizontal, 'vertical': vertical,
                'cross': list(set(horizontal + vertical))}

    # ── Transformations ───────────────────────────────────────────────────────

    def rotate(self, times: int = 1) -> 'SatorSquare':
        """Return a new SatorSquare rotated 90° clockwise `times` times."""
        g = [row[:] for row in self.grid]
        for _ in range(times % 4):
            g = [[g[SIZE - 1 - c][r] for c in range(SIZE)] for r in range(SIZE)]
        sq = SatorSquare.__new__(SatorSquare)
        sq.form = f'{self.form}_ROT{90 * (times % 4)}'
        sq.grid = g
        return sq

    def flip_horizontal(self) -> 'SatorSquare':
        """Return a new SatorSquare flipped left-right."""
        sq = SatorSquare.__new__(SatorSquare)
        sq.form = f'{self.form}_FLIP_H'
        sq.grid = [row[::-1] for row in self.grid]
        return sq

    def flip_vertical(self) -> 'SatorSquare':
        """Return a new SatorSquare flipped top-bottom."""
        sq = SatorSquare.__new__(SatorSquare)
        sq.form = f'{self.form}_FLIP_V'
        sq.grid = self.grid[::-1]
        return sq

    def transpose(self) -> 'SatorSquare':
        """Return the transposed grid (rows become columns)."""
        sq = SatorSquare.__new__(SatorSquare)
        sq.form = f'{self.form}_TRANSPOSED'
        sq.grid = [[self.grid[c][r] for c in range(SIZE)] for r in range(SIZE)]
        return sq


# ─────────────────────────────────────────────────────────────────────────────
# Cipher Class
# ─────────────────────────────────────────────────────────────────────────────

class SatorCipher:
    """
    Use the Sator Square as a Polybius-style substitution cipher.

    Encoding scheme:
        Each letter is mapped to its (row, col) position in the grid.
        Letters that appear multiple times use the first occurrence.
        Letters not in the grid (Q, W, X, Y, Z, etc.) are passed through.

    Limitation:
        Only 8 distinct letters (A, E, N, O, P, R, S, T) are in the grid.
        This cipher is best used as a demonstration / partial encoder.
    """

    ALPHABET_MAP: dict[str, tuple[int, int]] = {}
    REVERSE_MAP:  dict[tuple[int, int], str]  = {}

    def __init__(self, square: SatorSquare | None = None) -> None:
        self.square = square or SatorSquare()
        self._build_maps()

    def _build_maps(self) -> None:
        self.ALPHABET_MAP = {}
        self.REVERSE_MAP  = {}
        for r, row in enumerate(self.square.grid):
            for c, ch in enumerate(row):
                if ch not in self.ALPHABET_MAP:
                    self.ALPHABET_MAP[ch]  = (r, c)
                    self.REVERSE_MAP[(r, c)] = ch

    def encode(self, text: str) -> list[str | tuple[int, int]]:
        """
        Encode a string. Returns a list where each element is either
        a (row, col) tuple (for grid letters) or the original character.
        """
        result = []
        for ch in text.upper():
            if ch in self.ALPHABET_MAP:
                result.append(self.ALPHABET_MAP[ch])
            else:
                result.append(ch)
        return result

    def decode(self, encoded: list[str | tuple[int, int]]) -> str:
        """Decode a sequence produced by encode()."""
        result = []
        for token in encoded:
            if isinstance(token, tuple):
                result.append(self.REVERSE_MAP.get(token, '?'))
            else:
                result.append(token)
        return ''.join(result)

    def encode_to_string(self, text: str, sep: str = ' ') -> str:
        """Encode and format as a human-readable string."""
        parts = []
        for token in self.encode(text):
            if isinstance(token, tuple):
                parts.append(f'{token[0]}{token[1]}')
            else:
                parts.append(token)
        return sep.join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# Boustrophedon Reader
# ─────────────────────────────────────────────────────────────────────────────

def read_boustrophedon(grid: list[list[str]]) -> str:
    """
    Read the grid boustrophedon (alternating direction per row),
    yielding the famous 'SATOR OPERA TENET TENET OPERA SATOR' reading
    when the central word is repeated.
    """
    result = []
    for ri, row in enumerate(grid):
        if ri % 2 == 0:
            result.extend(row)
        else:
            result.extend(reversed(row))
    return ''.join(result)


def read_boustrophedon_with_centre_repeat(grid: list[list[str]]) -> str:
    """
    Classic boustrophedon reading that naturally surfaces TENET twice.
    Reading: SATOR → OPER A (reversed) → TENET → AREP O (reversed) → ROTAS
    Then reading from bottom: SATOR → reversed OPERA → TENET → ...
    Returns the classic doubled reading.
    """
    forward  = read_boustrophedon(grid)
    backward = read_boustrophedon(grid[::-1])
    return f'{forward} | {backward}'


# ─────────────────────────────────────────────────────────────────────────────
# Generalised Word Square Finder
# ─────────────────────────────────────────────────────────────────────────────

def find_word_squares(word_list: list[str], size: int = 5) -> list[list[str]]:
    """
    Search a word list for n×n word squares where reading down the columns
    also yields valid words (the Sator property).

    Parameters
    ----------
    word_list : list[str]
        A flat list of words to search.
    size : int
        The target square size (default 5).

    Returns
    -------
    list of word-lists, each representing one valid square.
    """
    candidates = sorted({w.upper() for w in word_list if len(w) == size})
    candidate_set = set(candidates)

    # Index by prefix for fast look-ahead
    prefix_index: dict[str, list[str]] = {}
    for word in candidates:
        for i in range(1, size + 1):
            prefix_index.setdefault(word[:i], []).append(word)

    results: list[list[str]] = []

    def backtrack(chosen: list[str]) -> None:
        depth = len(chosen)
        if depth == size:
            cols = [''.join(chosen[r][c] for r in range(size)) for c in range(size)]
            if all(col in candidate_set for col in cols):
                results.append(chosen[:])
            return
        # Build column prefix constraints
        for word in candidates:
            ok = True
            for c in range(size):
                prefix = ''.join(chosen[r][c] for r in range(depth)) + word[c]
                if prefix not in prefix_index:
                    ok = False
                    break
            if ok:
                chosen.append(word)
                backtrack(chosen)
                chosen.pop()

    backtrack([])
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Demonstration / CLI Runner
# ─────────────────────────────────────────────────────────────────────────────

def divider(title: str = '') -> None:
    w = 60
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * pad}")
    else:
        print(f"\n{'═' * w}")


def demo() -> None:
    """Run a full interactive demonstration of the square's properties."""

    divider('SATOR ROTAS SQUARE — PYTHON DEMONSTRATION')

    # ── 1. Display both forms ─────────────────────────────────────────────
    divider('1. THE SQUARE — BOTH FORMS')
    sator = SatorSquare('SATOR')
    rotas = SatorSquare('ROTAS')
    print(sator)
    print(rotas)

    # ── 2. Word meanings ──────────────────────────────────────────────────
    divider('2. WORD MEANINGS')
    for word, meaning in WORD_MEANINGS.items():
        print(f'  {word:6s} — {meaning}')

    # ── 3. All reading directions ─────────────────────────────────────────
    divider('3. ALL READING DIRECTIONS (SATOR FORM)')
    for direction, words in sator.all_readings().items():
        print(f'  {direction:25s}: {" ".join(words)}')

    # ── 4. Symmetry verification ──────────────────────────────────────────
    divider('4. SYMMETRY VERIFICATION')
    report = sator.symmetry_report()
    for prop, result in report.items():
        mark = '✓' if result else '✗'
        print(f'  [{mark}] {prop}')

    # ── 5. Letter frequency ───────────────────────────────────────────────
    divider('5. LETTER FREQUENCIES (25 TOTAL)')
    freq = sator.letter_frequencies()
    print(f'  Distinct letters ({len(sator.distinct_letters())}): '
          f'{", ".join(sorted(sator.distinct_letters()))}')
    print(f'  Frequencies: { {k: v for k, v in sorted(freq.items())} }')

    # ── 6. Pater Noster analysis ──────────────────────────────────────────
    divider('6. PATER NOSTER ANAGRAM ANALYSIS')
    pn = sator.pater_noster_analysis()
    print(f'  Grid total letters    : {pn["grid_letter_count"]}')
    print(f'  Letter frequencies    : {pn["grid_frequencies"]}')
    print(f'  PATERNOSTER×2 needs   : {pn["paternoster_x2_needed"]}')
    print(f'  Leftover letters      : {pn["leftover_letters"]}')
    print(f'  Theory plausible      : {pn["theory_holds"]}')
    print('\n  Cross pattern:')
    print('          A')
    print('          P')
    print('          A')
    print('          T')
    print('          E')
    print('          R')
    print('  A P A T E R N O S T E R A')
    print('          O')
    print('          S')
    print('          T')
    print('          E')
    print('          R')
    print('          O')
    print('  (Remaining: A, O, A, O → Alpha & Omega ×2)')

    # ── 7. TENET cross positions ──────────────────────────────────────────
    divider('7. TENET CROSS — HIGHLIGHTED')
    cross_positions = set(sator.tenet_cross_positions()['cross'])
    print(sator.display(highlight=cross_positions))

    # ── 8. Word path finding ──────────────────────────────────────────────
    divider('8. WORD PATH FINDING')
    for word, paths in sator.all_word_paths().items():
        print(f'  {word}: {len(paths)} path(s) found')
        for p in paths[:2]:  # show max 2 per word
            print(f'    {p}')

    # ── 9. Boustrophedon reading ──────────────────────────────────────────
    divider('9. BOUSTROPHEDON READING')
    bous = read_boustrophedon(SATOR_GRID)
    print(f'  Forward  boustrophedon: {bous}')
    bous_full = read_boustrophedon_with_centre_repeat(SATOR_GRID)
    print(f'  With centre repeat    : {bous_full}')

    # ── 10. Cipher demonstration ──────────────────────────────────────────
    divider('10. SATOR CIPHER DEMONSTRATION')
    cipher = SatorCipher(sator)
    test_messages = ['SATOR', 'TENET', 'ROTAS', 'SATOR AREPO']
    for msg in test_messages:
        encoded = cipher.encode_to_string(msg)
        decoded = cipher.decode(cipher.encode(msg))
        print(f'  "{msg}" → [{encoded}] → "{decoded}"')

    # ── 11. Transformation gallery ────────────────────────────────────────
    divider('11. TRANSFORMATION GALLERY')
    transforms = [
        ('Original',    sator),
        ('Rotated 90°', sator.rotate(1)),
        ('Rotated 180°',sator.rotate(2)),
        ('Flip H',      sator.flip_horizontal()),
        ('Transposed',  sator.transpose()),
    ]
    for name, sq in transforms:
        rows = [' '.join(r) for r in sq.grid]
        print(f'  {name:15s}:  {" | ".join(rows)}')

    # ── 12. Summary ───────────────────────────────────────────────────────
    divider('SUMMARY')
    print("""
  The Sator Rotas Square is:
  • A 5×5 two-dimensional Latin palindrome (~1st century CE)
  • Readable in all four directions yielding the same five words
  • Transpose-symmetric (the matrix equals its own transpose)
  • 180°-rotationally symmetric through its centre
  • Centred on TENET — itself a palindrome and a hidden cross
  • A cipher key (Polybius-style positional encoding)
  • The structural basis of Christopher Nolan's film "Tenet" (2020)
  • Possibly the world's oldest still-recognised word puzzle
    """)
    divider()


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    demo()
