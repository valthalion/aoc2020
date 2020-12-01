def read_input():
    with open('puzzle01.in', 'r') as f:
        numbers = {int(line) for line in f}
    return numbers


def find_pair(target, numbers):
    for n in numbers:
        if target - n in numbers:
            return n * (target - n)


def part_1():
    numbers = read_input()
    return find_pair(2020, numbers)


def part_2():
    numbers = read_input()
    for n in numbers:
        rest = numbers - set((n,))
        if (pair := find_pair(2020 - n, rest)):
            return n * pair
