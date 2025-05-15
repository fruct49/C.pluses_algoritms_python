def solve_n_queens(n):
    def is_safe(board, row, col):
        # Проверяем вертикаль и диагонали
        for i in range(row):
            if board[i] == col or \
                    board[i] - i == col - row or \
                    board[i] + i == col + row:
                return False
        return True

    def backtrack(row):
        if row == n:
            solution = []
            for i in range(n):
                line = []
                for j in range(n):
                    if board[i] == j:
                        line.append("Q")
                    else:
                        line.append(".")
                solution.append("".join(line))
            solutions.append(solution)
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Откат

    solutions = []
    board = [-1] * n  # board[i] = столбец ферзя в строке i
    backtrack(0)
    return solutions[0] if solutions else []


# Ввод и вывод
n = int(input("Введите N: "))
solution = solve_n_queens(n)
for row in solution:
    print(row)