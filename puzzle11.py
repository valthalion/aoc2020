from collections import defaultdict


def read_input():
    with open('puzzle11.in', 'r') as f:
        seats = tuple(tuple(line.strip()) for line in f)
    return seats


def show(seats):
    for line in seats:
        print(''.join(line))
    print()


def build_neighbours_dict(seats, floor_is_neighbour):
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))
    nrows, ncols = len(seats), len(seats[0])
    neighbours = defaultdict(set)
    for row in range(nrows):
        for col in range(ncols):
            if seats[row][col] == '.':
                continue
            for dr, dc in directions:
                steps = 0
                r, c = row, col
                while steps < 1 or not floor_is_neighbour:
                    steps += 1
                    r += dr
                    c += dc
                    if not (0 <= r < nrows and 0 <= c < ncols):
                        break
                    if seats[r][c] == '.':
                        continue
                    neighbours[(r, c)].add((row, col))
                    break
    return neighbours


def new_state(row, col, seats, neighbours, empty_threshold):
    state = seats[row][col]
    if state == '.':
        return '.'
    count = sum(1 for r, c in neighbours[(row, col)] if seats[r][c] == '#')
    if state == 'L':
        return '#' if count == 0 else 'L'
    else:  # state == '#'
        return 'L' if count >= empty_threshold else '#'


def step(seats, neighbours, empty_threshold):
    return tuple(tuple(new_state(row, col, seats, neighbours, empty_threshold)
                       for col in range(len(seats[0])))
                 for row in range(len(seats)))


def find_equilibrium(floor_is_neighbour, empty_threshold):
    seats = read_input()
    neighbours = build_neighbours_dict(seats, floor_is_neighbour)
    while True:
        last = seats
        seats = step(seats, neighbours, empty_threshold)
        if seats == last:
            break
    return sum(1 for line in seats for seat in line if seat == '#')


def part_1():
    return find_equilibrium(floor_is_neighbour=True, empty_threshold=4)


def part_2():
    return find_equilibrium(floor_is_neighbour=False, empty_threshold=5)
