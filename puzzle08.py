from collections import defaultdict


def read_input():
    with open('puzzle08.in', 'r') as f:
        program = [parse(line.strip()) for line in f]
    return program


def parse(line):
    cmd, arg = line.split()
    return cmd, int(arg)


class Computer:
    def __init__(self, program, ip=0, acc=0):
        self.program = program
        self.ip = ip  # Instruction pointer
        self.accumulator = acc

    def nop(self, arg):
        pass

    def acc(self, arg):
        self.accumulator += arg

    def jmp(self, arg):
        self.ip += arg - 1  # will be incremented after the operation

    def execute_instruction(self):
        if not 0 <= self.ip < len(self.program):
            raise RuntimeError('Instruction Pointer out of bounds', self.ip)
        cmd, arg = self.program[self.ip]
        getattr(self, cmd)(arg)
        self.ip += 1

    def run(self):
        while self.ip != len(self.program):
            self.execute_instruction()

    def find_loop(self):
        executed = set()
        while self.ip not in executed:
            executed.add(self.ip)
            self.execute_instruction()


def find_valid_addresses(program):
    graph = {}
    for idx, (cmd, arg) in enumerate(program):
        if cmd in ('nop', 'acc'):
            delta = 1
        else:  # jmp
            delta = arg
        graph[idx] = idx + delta
    inverse_graph = defaultdict(set)
    for orig, dest in graph.items():
        inverse_graph[dest].add(orig)
    queue = set(inverse_graph[len(program)])
    valid_addresses = set()
    while queue:
        address = queue.pop()
        valid_addresses.add(address)
        queue |= inverse_graph[address] - valid_addresses
    return valid_addresses


def fix_program(program):
    valid_addresses = find_valid_addresses(program)
    if 0 in valid_addresses:
        return
    ip = 0
    seen = set()
    while ip not in seen:  # this cannot end by itself (otherwise 0 in valid_addresses)
        seen.add(ip)
        cmd, arg = program[ip]
        if cmd == 'acc':
            ip += 1
        elif cmd == 'nop':
            if ip + arg in valid_addresses:
                program[ip] = ('jmp', arg)
                return
            ip += 1
        else:  # jmp
            if ip + 1 in valid_addresses:
                program[ip] = ('nop', arg)
                return
            ip += arg
    raise RuntimeError('No solution')


def part_1():
    program = read_input()
    computer = Computer(program)
    computer.find_loop()
    return computer.accumulator


def part_2():
    program = read_input()
    fix_program(program)
    computer = Computer(program)
    computer.run()
    return computer.accumulator
