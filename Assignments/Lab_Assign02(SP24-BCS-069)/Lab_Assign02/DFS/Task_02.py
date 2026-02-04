# Boggle word finder.
# Searches all 8 directions, never reuses a cell in the same word,
# and prunes paths using a simple prefix set.

from typing import List, Set, Tuple

# 8-direction movements
DIRECTIONS: List[Tuple[int, int]] = [
    (-1,  0), (1, 0),  (0, -1), (0, 1), # N, S, W, E
    (-1, -1), (-1, 1), (1, -1), (1, 1), # NW, NE, SW, SE
]

def all_prefixes(words: List[str]) -> Set[str]:
    """Return a set containing every prefix of every word (word included)."""
    prefixes: Set[str] = set()
    for word in words:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])
    return prefixes

def find_boggle_words(board: List[List[str]], dictionary: List[str]) -> Set[str]:
    """
    Find all dictionary words that can be formed by walking adjacent cells
    (8 directions) without revisiting a cell in the same word.
    """
    if not board or not board[0] or not dictionary:
        return set()

    # Normalize everything to uppercase for consistent comparison
    normalized_board = [[ch.upper() for ch in row] for row in board]
    words_upper = [w.upper() for w in dictionary]
    words_lookup: Set[str] = set(words_upper)
    prefix_lookup: Set[str] = all_prefixes(words_upper)

    num_rows, num_cols = len(normalized_board), len(normalized_board[0])
    used_in_path = [[False] * num_cols for _ in range(num_rows)]
    found_words: Set[str] = set()

    def explore_from_cell(row: int, col: int, current_word: str) -> None:
        """DFS from (row, col), extending current_word and collecting matches."""
        next_word = current_word + normalized_board[row][col]

        # If no dictionary word starts with this prefix, stop exploring.
        if next_word not in prefix_lookup:
            return

        if next_word in words_lookup:
            found_words.add(next_word)

        used_in_path[row][col] = True
        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, col + dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols and not used_in_path[nr][nc]:
                explore_from_cell(nr, nc, next_word)
        used_in_path[row][col] = False  # backtrack

    for r in range(num_rows):
        for c in range(num_cols):
            explore_from_cell(r, c, "")

    return found_words


# ----- Demo with the prompt's 4x4 board -----
if __name__ == "__main__":
    board = [
        list("MSEF"),
        list("RATD"),
        list("LONE"),
        list("KAFB"),
    ]
    dictionary = ["START", "NOTE", "SAND", "STONED"]

    results = find_boggle_words(board, dictionary)
    print("Found words:", sorted(results))   # Expected: ['NOTE', 'SAND', 'STONED']
