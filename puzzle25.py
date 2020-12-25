from itertools import count


def read_input():
    with open('puzzle25.in', 'r') as f:
        card_pk = int(next(f).strip())
        door_pk = int(next(f).strip())
    return card_pk, door_pk


def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % 20201227
    return value


def find_loop_size(subject_number, target):
    value = 1
    for loop_size in count(start=1):
        value = (value * subject_number) % 20201227
        if value == target:
            return loop_size


def part_1():
    card_pk, door_pk = read_input()
    card_loop_size = find_loop_size(7, card_pk)
    door_loop_size = find_loop_size(7, door_pk)
    print(card_loop_size, door_loop_size)
    encryption_key = transform(card_pk, door_loop_size)
    encryption_key2 = transform(door_pk, card_loop_size)
    if encryption_key != encryption_key2:
        print('Keys do not match:', encryption_key, '!=', encryption_key2)
    return encryption_key


def part_2():
    pass
