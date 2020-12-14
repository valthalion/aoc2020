from itertools import combinations


MASK = 0
MEM = 1
xto0 = {ord('X'): ord('0')}
xto1 = {ord('X'): ord('1')}
xto0_0to1 = {ord('X'): ord('0'), ord('0'): ord('1')}


def read_input():
    with open('puzzle14.in', 'r') as f:
        for line in f:
            if line.startswith('mem'):
                address, value = line.strip().split('=')
                address = int(address[4:-2])
                value = int(value[1:])
                yield MEM, (address, value)
            elif line.startswith('mask'):
                mask = line.strip()[7:]
                yield MASK, mask
            else:
                raise ValueError('Unknown command', line)


def run(program):
    mask = None
    memory = {}
    for cmd, args in program:
        if cmd == MASK:
            mask = args
            and_mask = int(mask.translate(xto1), 2)
            or_mask = int(mask.translate(xto0), 2)
        elif cmd == MEM:
            address, value = args
            memory[address] = (value & and_mask) | or_mask
        else:
            raise ValueError('Unknown command', cmd)
    return memory


def apply_mask(address, or_mask, and_mask, mask):
    address |= or_mask
    address &= and_mask
    switch = 1
    switches = [pow(2, pos) for pos, c in enumerate(reversed(mask)) if c == 'X']
    yield address
    for n in range(1, len(switches) + 1):
        yield from (address + sum(comb) for comb in combinations(switches, n))


def run2(program):
    mask = None
    memory = {}
    for cmd, args in program:
        if cmd == MASK:
            mask = args
            or_mask = int(mask.translate(xto0), 2)
            and_mask = int(mask.translate(xto0_0to1), 2)
        elif cmd == MEM:
            address, value = args
            addresses = apply_mask(address, or_mask, and_mask, mask)
            for address in addresses:
                memory[address] = value
        else:
            raise ValueError('Unknown command', cmd)
    return memory


def part_1():
    program = read_input()
    memory = run(program)
    return sum(memory.values())


def part_2():
    program = read_input()
    memory = run2(program)
    return sum(memory.values())
