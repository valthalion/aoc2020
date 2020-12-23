from collections import deque


class Node:
    def __init__(self, value, nxt=None):
        self.value = value
        self.nxt = nxt

    def __str__(self):
        return f'Node(value={self.value}, nxt={self.nxt.value if self.nxt is not None else None})'


class CircularList:
    def __init__(self, initial_sequence, upto=1_000_000):
        n = len(initial_sequence)
        mod_sequence = [n - 1 for n in initial_sequence]
        self.nodes = [Node(value) for value in range(upto)]
        self.head = self.nodes[mod_sequence[0]]
        for pred, succ in zip(mod_sequence, mod_sequence[1:]):
            self.nodes[pred].nxt = self.nodes[succ]
        pred = self.nodes[succ]
        for succ in self.nodes[n:]:
            pred.nxt = succ
            pred = succ
        if upto > n:
            self.nodes[-1].nxt = self.head
        else:
            self.nodes[mod_sequence[-1]].nxt = self.nodes[mod_sequence[0]]
        self.bottom = 0
        self.top = upto - 1

    def __str__(self):
        return ''.join(str(n) for n in self)

    def __iter__(self):
        start = self.nodes[0]
        cursor = start.nxt
        while cursor is not start:
            yield cursor.value + 1
            cursor = cursor.nxt

    def insert(self, seq, target):
        end = self.nodes[target]
        restart = end.nxt
        end.nxt = seq[0]
        seq[-1].nxt = restart

    def extract(self):
        restart = self.head.nxt.nxt.nxt.nxt
        extracted = [self.head.nxt, self.head.nxt.nxt, self.head.nxt.nxt.nxt]
        extracted[-1].nxt = None
        self.head.nxt = restart
        return extracted

    def step(self):
        current = self.head.value
        picked = self.extract()
        target = current - 1
        while True:
            if self.nodes[target] in picked:
                target -= 1
                continue
            if target < self.bottom:
                target = self.top
                continue
            break
        self.insert(picked, target)
        self.head = self.head.nxt


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
    n_steps = 10_000_000
    initial_sequence = [int(n) for n in initial_positions]
    circle = CircularList(initial_sequence)
    for _ in range(n_steps):
        circle.step()
    node1 = circle.nodes[0]
    cup1, cup2 = node1.nxt.value + 1, node1.nxt.nxt.value + 1
    return cup1 * cup2
