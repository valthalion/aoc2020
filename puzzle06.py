def read_input():
    group = []
    with open('puzzle06.in', 'r') as f:
        for line in f:
            answer = line.strip()
            if not answer and group:
                yield group
                group = []
                continue
            group.append(set(answer))
    if group:
        yield group


def count_anyone(group):
    total_answers = group.pop()
    for answer in group:
        total_answers |= answer
    return len(total_answers)


def count_everyone(group):
    total_answers = group.pop()
    for answer in group:
        total_answers &= answer
    return len(total_answers)


def part_1():
    return sum(count_anyone(group) for group in read_input())


def part_2():
    return sum(count_everyone(group) for group in read_input())
