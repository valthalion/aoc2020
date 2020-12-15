from itertools import islice


def game(seed):
    memory = {}
    for turn, number in enumerate(seed[:-1], start=1):
        memory[number] = turn
        yield number

    turn += 1
    last_number = seed[-1]
    yield last_number

    while True:
        if last_number not in memory:
            current_number = 0
        else:
            current_number = turn - memory[last_number]
        memory[last_number] = turn
        turn +=1
        yield current_number
        last_number = current_number


def play_turns(seed, target):
    for number in islice(game(seed), target - 1, target):
        pass
    return number

def part_1():
    seed = [0, 8, 15, 2, 12, 1, 4]
    number = play_turns(seed, 2020)
    return number


def part_2():
    seed = [0, 8, 15, 2, 12, 1, 4]
    number = play_turns(seed, 30_000_000)
    return number


def main():
    tests = (
        ([0, 3, 6], 436, 175594),
        ([1, 3, 2], 1, 2578),
        ([2, 1, 3], 10, 3544142),
        ([1, 2, 3], 27, 261214),
        ([2, 3, 1], 78, 6895259),
        ([3, 2, 1], 438, 18),
        ([3, 1, 2], 1836, 362),
    )

    for seed, expected2020, expected30m in tests:
        number = play_turns(seed, 2020)
        print(seed, 2020, number, expected2020, 'ok' if number == expected2020 else 'error')
        number = play_turns(seed, 30_000_000)
        print(seed, 10_000_000, number, expected30m, 'ok' if number == expected30m else 'error')
        print()


if __name__ == '__main__':
    main()
