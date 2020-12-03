import re

input_re = re.compile('''(?P<min>\d+)-(?P<max>\d+) (?P<letter>[a-z]): (?P<pwd>[a-z]+)''')


def read_input():
    specs = []
    with open('puzzle02.in', 'r') as f:
        for line in f:
            spec = input_re.match(line.strip()).groupdict()
            spec['min'] = int(spec['min'])
            spec['max'] = int(spec['max'])
            specs.append(spec)
    return specs


def valid(spec):
    letter_count = sum(1 for c in spec['pwd'] if c == spec['letter'])
    return spec['min'] <= letter_count <= spec['max']


def new_valid(spec):
    pos1, pos2, letter, pwd = spec['min'] - 1, spec['max'] - 1, spec['letter'], spec['pwd']
    if pos1 >= len(pwd):
        return False
    if pos2 >= len(pwd):
        return pwd[pos1] == letter
    return (pwd[pos1] == letter) != (pwd[pos2] == letter)


def part_1():
    specs = read_input()
    count = sum(1 for spec in specs if valid(spec))
    return count


def part_2():
    specs = read_input()
    count = sum(1 for spec in specs if new_valid(spec))
    return count
