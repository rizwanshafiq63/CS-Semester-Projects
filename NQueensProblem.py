class Solution:
    def solveNQueens(self, n: int):
        board = [["." for _ in range(n)] for _ in range(n)]
        ans = []
        self.nQueens(board, 0, n, ans)
        return [["".join(row) for row in solution] for solution in ans]

    def nQueens(self, board, row, n, ans):
        if row == n:
            # deep copy of current board
            ans.append([row[:] for row in board])
            return

        for col in range(n):
            if self.isSafe(board, row, col, n):
                board[row][col] = 'Q'
                self.nQueens(board, row + 1, n, ans)
                board[row][col] = '.'

    def isSafe(self, board, row, col, n):
        # horizontal
        for j in range(n):
            if board[row][j] == 'Q':
                return False

        # vertical
        for i in range(n):
            if board[i][col] == 'Q':
                return False

        # left diagonal
        i, j = row, col
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1

        # right diagonal
        i, j = row, col
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1

        return True


# ---------- Runner ----------
if __name__ == "__main__":
    try:
        n = int(input("Enter value of n: "))
    except:
        n = 4  # default

    sol = Solution()
    solutions = sol.solveNQueens(n)

    print(f"\nNumber of solutions: {len(solutions)}")
    for idx, solution in enumerate(solutions, 1):
        print(f"\nSolution {idx}:")
        for row in solution:
            print(row)
