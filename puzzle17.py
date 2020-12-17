from itertools import product


def read_input(dim=3):
    active = set()
    additional_dims = (0,) * (dim - 2)
    with open('puzzle17.in', 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    active.add((x, y, *additional_dims))
    return active


def neighbours(point):
    deltas = product(*(range(-1, 2) for _ in point))
    for delta in deltas:
        if any(delta):
            yield tuple(x + dx for x, dx in zip(point, delta))


def step(active):
    candidates = set(active)
    for point in active:
        candidates |= set(neighbours(point))
    new_active = set()
    for point in candidates:
        active_neighbours = sum(1 for other_point in neighbours(point) if other_point in active)
        if any((point in active and 2 <= active_neighbours <= 3,
                point not in active and active_neighbours == 3)):
            new_active.add(point)
    return new_active


def run(dims, steps):
    active = read_input(dim=dims)
    for _ in range(steps):
        active = step(active)
    return len(active)


def part_1():
    return run(dims=3, steps=6)


def part_2():
    return run(dims=4, steps=6)
