# Iterative Deepening Boggle Word Finder
# Expands search depth (word length) step by step until no new words are found.

from typing import List, Set, Tuple

# 8 directions: N, S, W, E, NW, NE, SW, SE
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

def all_prefixes(words: List[str]) -> Set[str]:
    """Return a set of all prefixes (including full words)."""
    prefixes = set()
    for w in words:
        for i in range(1, len(w) + 1):
            prefixes.add(w[:i])
    return prefixes

def iterative_deepening_boggle(board: List[List[str]], dictionary: List[str]) -> Set[str]:
    """
    Perform iterative deepening word search on the boggle board.
    Each iteration increases the max depth (word length).
    """
    if not board or not dictionary:
        return set()

    board = [[ch.upper() for ch in row] for row in board]
    dict_upper = [w.upper() for w in dictionary]
    words_lookup = set(dict_upper)
    prefix_lookup = all_prefixes(dict_upper)

    rows, cols = len(board), len(board[0])
    found_words: Set[str] = set()
    visited = [[False] * cols for _ in range(rows)]

    def dfs(r: int, c: int, current: str, depth: int, max_depth: int):
        if depth > max_depth:
            return
        next_word = current + board[r][c]
        if next_word not in prefix_lookup:
            return
        if next_word in words_lookup:
            found_words.add(next_word)

        visited[r][c] = True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                dfs(nr, nc, next_word, depth + 1, max_depth)
        visited[r][c] = False

    # Iteratively deepen search by increasing max word length
    for max_depth in range(3, 9):  # as in lab: lengths 5,6,7,8 — start smaller for safety
        print(f"Searching words up to length {max_depth}")
        for r in range(rows):
            for c in range(cols):
                dfs(r, c, "", 1, max_depth)

    return found_words


# --- Demo using the lab’s 4×4 board ---
if __name__ == "__main__":
    board = [
        list("MSEF"),
        list("RATD"),
        list("LONE"),
        list("KAFB"),
    ]
    dictionary = ["START", "NOTE", "SAND", "STONED"]

    result = iterative_deepening_boggle(board, dictionary)
    print("Words found:", sorted(result))
