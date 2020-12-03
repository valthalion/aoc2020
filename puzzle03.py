def read_input():
    with open('puzzle03.in', 'r') as f:
        field = [line.strip() for line in f]
    return field


def run(field, right, down):
    height, width = len(field), len(field[0])
    row, col = 0, 0
    trees = 0
    while row < height:
        if field[row][col] == '#':
            trees += 1
        row += down
        col = (col + right) % width
    return trees


def part_1():
    field = read_input()
    trees = run(field, 3, 1)
    return trees


def part_2():
    field = read_input()
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    result = 1
    for right, down in slopes:
        trees = run(field, right, down)
        result *= trees
    return result
