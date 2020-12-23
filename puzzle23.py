from collections import deque


def step(circle, bottom, top):
    current = circle[0]
    circle.rotate(-1)
    picked = [circle.popleft(), circle.popleft(), circle.popleft()]
    insertion_label = current - 1
    while True:
        if insertion_label in picked:
            insertion_label -= 1
            continue
        if insertion_label < bottom:
            insertion_label = top
            continue
        break
    insertion_index = circle.index(insertion_label) + 1
    for label in reversed(picked):
        circle.insert(insertion_index, label)


def part_1():
    # initial_positions = '389125467'
    initial_positions = '562893147'
    n_steps = 100
    circle = deque(int(n) for n in initial_positions)
    bottom, top = min(circle), max(circle)
    for _ in range(n_steps):
        step(circle, bottom, top)
    index1 = circle.index(1)
    circle.rotate(-index1)
    return ''.join(str(n) for n in list(circle)[1:])


def part_2():
    # initial_positions = '389125467'
    initial_positions = '562893147'
