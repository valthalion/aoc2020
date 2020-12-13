from functools import reduce
from operator import mul


def read_input():
    with open('puzzle13.in', 'r') as f:
        timestamp = int(f.readline().strip())
        lines = [(int(n), pos)
                 for pos, n in enumerate(f.readline().strip().split(','))
                 if n != 'x']
    return timestamp, lines


def part_1():
    timestamp, lines = read_input()

    def waiting_time(line):
        time_since_departure = timestamp % line
        if time_since_departure == 0:
            return 0
        return line - time_since_departure

    min_waiting_time, first_line = min((waiting_time(line), line) for line, _ in lines)
    print(first_line, min_waiting_time)
    return first_line * min_waiting_time


def cycle_start(lines):
    (cycle, start), *rest = lines
    for line_cycle, delay in rest:
        target = -delay % line_cycle
        while start % line_cycle != target:
            start += cycle
        cycle *= line_cycle
    return start


def part_2():
    _, lines = read_input()
    return cycle_start(lines)


def main():
    tests = (
        ('7,13', 77),
        ('7,13,x,x,59,x,31,19', 1068781),
        ('7,x,13,19', 3417),
        ('67,7,59,61', 754018),
        ('67,x,7,59,61', 779210),
        ('67,7,x,59,61', 1261476),
        ('1789,37,47,1889', 1202161486)
    )
    for input_spec, expected in tests:
        lines = [(int(n), pos)
                 for pos, n in enumerate(input_spec.split(','))
                 if n != 'x']
        result = cycle_start(lines)
        print(input_spec, result, expected, '->', 'ok' if result == expected else 'error')


if __name__ == '__main__':
    main()
