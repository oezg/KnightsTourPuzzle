from math import log10
from copy import deepcopy

knights_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))


def cell_marker(cell_size, marker="_"):
    if marker == "_":
        return marker * cell_size
    return marker.rjust(cell_size)


def draw_board(matrix_copy):
    rows = len(matrix_copy)
    columns = len(matrix_copy[0])
    cell_size = len(matrix_copy[0][0])
    horizontal_frame = " " * (int(log10(rows)) + 1) + "-" * (columns * (cell_size + 1) + 3)
    print(horizontal_frame)
    for r in range(rows, 0, -1):
        row = " " * (int(log10(rows)) - int(log10(r))) + str(r) + "| "
        for c in range(columns):
            row += matrix_copy[r - 1][c] + " "
        row += "|"
        print(row)
    print(horizontal_frame)
    labels = map(lambda n: str(n + 1).rjust(cell_size), range(columns))
    print(" " * (int(log10(rows)) + 2), *labels)


def get_dimensions():
    while True:
        try:
            col, row = [int(d) for d in input("Enter your board dimensions: ").split()]
            assert 0 < col and 0 < row
        except (ValueError, AssertionError):
            print("Invalid dimensions!")
        else:
            return row, col


def get_position(rows, columns):
    while True:
        try:
            c, r = [int(p) for p in input("Enter the knight's starting position: ").split()]
            assert 0 < c <= columns and 0 < r <= rows
        except (ValueError, AssertionError):
            print("Invalid position!")
        else:
            return r - 1, c - 1


def get_move(possibilities):
    while True:
        try:
            horizontal, vertical = [int(m) for m in input("Enter your next move: ").split()]
            assert (vertical - 1, horizontal - 1) in possibilities
        except (ValueError, AssertionError):
            print("Invalid move!", end=' ')
        else:
            return vertical - 1, horizontal - 1


def modify_matrix(matrix, next_position, current_position):
    cell_size = len(matrix[0][0])
    knight = cell_marker(cell_size, "X")
    asterisk = cell_marker(cell_size, "*")
    current_y, current_x = current_position
    next_y, next_x = next_position
    matrix[current_y][current_x] = asterisk
    matrix[next_y][next_x] = knight
    return matrix


def is_tour_complete(matrix):
    cell_size = len(matrix[0][0])
    asterisk = cell_marker(cell_size, "*")
    knight = cell_marker(cell_size, "X")
    for row in matrix:
        for cell in row:
            if cell not in {asterisk, knight}:
                return False
    return True


def copy_matrix(matrix, possibility_dict):
    cell_size = len(matrix[0][0])
    matrix_copy = deepcopy(matrix)
    for possible_square, possibilities in possibility_dict.items():
        possible_y, possible_x = possible_square
        matrix_copy[possible_y][possible_x] = cell_marker(cell_size, str(possibilities))
    return matrix_copy


def wants_to_try():
    while True:
        try_the_puzzle = input("Do you want to try the puzzle? (y/n): ")
        if try_the_puzzle == "y":
            return True
        elif try_the_puzzle == "n":
            return False
        else:
            print("Invalid input!")


def play(current, dimensions):
    cell_size = int(log10(dimensions[0] * dimensions[1])) + 1
    empty_cell = cell_marker(cell_size)
    matrix = [[empty_cell for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    knight = cell_marker(cell_size, 'X')
    matrix[current[0]][current[1]] = knight
    squares_visited = 1
    while True:
        possibilities = possible_moves(current, matrix)
        matrix_copy = copy_matrix(matrix, possibilities)
        draw_board(matrix_copy)
        if not possibilities:
            if is_tour_complete(matrix):
                print("What a great tour! Congratulations!")
            else:
                print("No more possible moves!")
                print("Your knight visited {} squares!".format(squares_visited))
            break
        next_position = get_move(possibilities)
        matrix = modify_matrix(matrix, next_position, current)
        current = next_position
        squares_visited += 1


def count_possible_moves(ix1, ix2, matrix, empty_cell):
    dimension_y = len(matrix)
    dimension_x = len(matrix[0])
    count = 0
    for i in knights_moves:
        index_1 = ix1 + i[0]
        index_2 = ix2 + i[1]
        try:
            assert 0 <= index_1 < dimension_y
            assert 0 <= index_2 < dimension_x
        except AssertionError:
            pass
        else:
            if matrix[index_1][index_2] == empty_cell:
                count += 1
    return count


def possible_moves(current_position, matrix):
    position_y, position_x = current_position
    dimension_y = len(matrix)
    dimension_x = len(matrix[0])
    cell_size = len(matrix[0][0])
    empty_cell = cell_marker(cell_size)
    possibility_dict = {}
    for i in knights_moves:
        index_1 = position_y + i[0]
        index_2 = position_x + i[1]
        try:
            assert 0 <= index_1 < dimension_y
            assert 0 <= index_2 < dimension_x
            assert matrix[index_1][index_2] == empty_cell
        except AssertionError:
            pass
        else:
            count_freedom = count_possible_moves(index_1, index_2, matrix, empty_cell)
            possibility_dict.update({(index_1, index_2): count_freedom})
    return possibility_dict


def is_possible(move, board):
    if 0 <= move[0] < len(board) and 0 <= move[1] < len(board[0]) and board[move[0]][move[1]] == -1:
        return True
    return False


def recursive_solver(solution_matrix, current_position, squares_visited):
    if squares_visited == len(solution_matrix) * len(solution_matrix[0]):
        return True
    for i in knights_moves:
        next_position = (current_position[0] + i[0], current_position[1] + i[1])
        if is_possible(next_position, solution_matrix):
            solution_matrix[next_position[0]][next_position[1]] = squares_visited
            if recursive_solver(solution_matrix, next_position, squares_visited + 1):
                return True
            solution_matrix[next_position[0]][next_position[1]] = -1
    return False


def solve_puzzle(start, dimensions):
    solution = [[-1 for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    solution[start[0]][start[1]] = 0
    squares_visited = 1
    if recursive_solver(solution, start, squares_visited):
        return True, solution
    else:
        return False, None


def to_matrix(solution):
    cell_size = len(solution) * len(solution[0])
    return [[cell_marker(cell_size, str(cell)) for cell in row] for row in solution]


def main():
    board_dimensions = get_dimensions()
    starting_position = get_position(*board_dimensions)
    solution_exists, solution = solve_puzzle(starting_position, board_dimensions)
    if wants_to_try() and solution_exists:
        play(starting_position, board_dimensions)
    elif solution_exists:
        print("Here's the solution!")
        solved_board = to_matrix(solution)
        draw_board(solved_board)
    else:
        print("No solution exists!")


if __name__ == "__main__":
    main()
