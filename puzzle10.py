from collections import Counter, defaultdict


def read_input():
    with open('puzzle10.in', 'r') as f:
        return sorted(int(line.strip()) for line in f)


def get_adaptors():
    adaptors = [0, *read_input()]
    built_in = adaptors[-1] + 3
    adaptors.append(built_in)
    return adaptors


def part_1():
    adaptors = get_adaptors()
    diffs = (succ - prev for prev, succ in zip(adaptors, adaptors[1:]))
    jumps = Counter(diffs)
    return jumps[1] * jumps[3]


def part_2():
    adaptors = get_adaptors()
    graph = {value: set(succ for succ in adaptors[idx+1:idx+4] if succ - value <= 3)
             for idx, value in enumerate(adaptors)}
    paths = defaultdict(int)
    paths[adaptors[0]] = 1
    for adaptor in adaptors:
        for succ in graph[adaptor]:
            paths[succ] += paths[adaptor]
    return paths[adaptors[-1]]
