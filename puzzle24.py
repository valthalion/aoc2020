from collections import Counter


def read_input():
    with open('puzzle24.in', 'r') as f:
        for line in f:
            yield sum(parse(line.strip()))


def parse(line):
    move = 0
    for c in line:
        if c == 'n':
            move += 1j
        elif c == 's':
            move += -1j
        elif c == 'e':
            if move:
                yield move + 1
                move = 0
            else:
                yield 2
        else:  # c == 'w'
            if move:
                yield move - 1
                move = 0
            else:
                yield -2


def neighbours(tile):
    for delta in (2, 1-1j, -1-1j, -2, -1+1j, 1+1j):
        yield tile + delta


def initial_board():
    flips = read_input()
    black_tiles = set()
    for tile in flips:
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    return black_tiles


def step(black_tiles):
    new_board = set()
    candidates = {neighbour for tile in black_tiles for neighbour in neighbours(tile)} | black_tiles
    for tile in candidates:
        count = sum(1 for neighbour in neighbours(tile) if neighbour in black_tiles)
        if (tile in black_tiles and 1 <= count <= 2) or (tile not in black_tiles and count == 2):
            new_board.add(tile)
    return new_board


def part_1():
    tiles = read_input()
    counts = Counter(tiles)
    blacks = sum(1 for tile, count in counts.items() if count % 2 != 0)
    return blacks


def part_2():
    black_tiles = initial_board()
    for _ in range(100):
        black_tiles = step(black_tiles)
    return len(black_tiles)
