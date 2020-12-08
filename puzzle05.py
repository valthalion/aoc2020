def read_input():
    with open('puzzle05.in', 'r') as f:
        for line in f:
            yield parse_seat(line.strip())


def parse_seat(seat):
    seat_id = int(''.join('0' if c in 'FL' else '1' for c in seat), 2)
    return seat_id


def part_1():
    return max(read_input())


def part_2():
    occupied_seats = set(read_input())
    all_seats = set(range(min(occupied_seats), max(occupied_seats) + 1))
    return (all_seats - occupied_seats).pop()



def main():
    tests = {
        'BFFFBBFRRR': (70, 7, 567),
        'FFFBBBFRRR': (14, 7, 119),
        'BBFFBBFRLL': (102, 4, 820)
        }
    for seat, expected in tests.items():
        sid = parse_seat(seat)
        print(seat, sid, expected, 'ok' if sid == expected[2] else 'error')


if __name__ == '__main__':
    main()
