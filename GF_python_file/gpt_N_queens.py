import time
def n_queens(board_size):
    def is_valid(state, row, col):
        for r, c in state:
            if c == col or r - c == row - col or r + c == row + col:
                return False
        return True

    def backtrack(state, row):
        if row == board_size:
            yield state
            return
        for col in range(board_size):
            if is_valid(state, row, col):
                yield from backtrack(state + [(row, col)], row + 1)

    return backtrack([], 0)


start_time = time.perf_counter()
num_solutions = len(list(n_queens(17)))
end_time = time.perf_counter()



print("Number of solutions:", num_solutions)
print("Execution time:", end_time - start_time, "seconds")
