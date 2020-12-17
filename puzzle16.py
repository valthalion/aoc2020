from functools import reduce
from operator import mul


def read_input():
    with open('puzzle16.in', 'r') as f:
        field_rules = {}
        for line in f:
            data_line = line.strip()
            if not data_line:
                break
            field, data = data_line.split(':')
            interval_specs = [interval.strip().split('-') for interval in data.split(' or ')]
            intervals = tuple((int(low), int(high)) for low, high in interval_specs)
            field_rules[field] = intervals

        if (line := next(f).strip()) != 'your ticket:':
            raise ValueError(f'Unexpected line "{line}". Expected "your ticket:"')
        ticket = [int(n) for n in next(f).strip().split(',')]
        if (line := next(f).strip()):
            raise ValueError(f'Unexpected line "{line}". Expected blank line')

        if (line := next(f).strip()) != 'nearby tickets:':
            raise ValueError(f'Unexpected line "{line}". Expected "nearby tickets:"')
        tickets = [[int(n) for n in line.strip().split(',')] for line in f]

        return field_rules, ticket, tickets


def validity(field_rules):
    def valid_fields(value):
        return set(field
                   for field, intervals in field_rules.items()
                   if any(low <= value <= high for low, high in intervals))

    return valid_fields



def part_1():
    field_rules, my_ticket, tickets = read_input()
    valid_fields = validity(field_rules)
    return sum(value for ticket in tickets for value in ticket if not valid_fields(value))


def part_2():
    field_rules, my_ticket, tickets = read_input()
    valid_fields = validity(field_rules)
    feasible = [set(field_rules.keys()) for _ in my_ticket]
    for ticket in tickets:
        for feasible_fields, value in zip(feasible, ticket):
            if (valid := valid_fields(value)):
                feasible_fields &= valid
    determined = set()
    while any(len(feasible_fields) > 1 for feasible_fields in feasible):
        for feasible_fields in feasible:
            if len(feasible_fields) == 1:
                field, = feasible_fields
                determined |= feasible_fields
            else:
                feasible_fields -= determined
    fields = [feasible_fields.pop() for feasible_fields in feasible]
    values = (value for field, value in zip(fields, my_ticket) if field.startswith('departure'))
    return reduce(mul, values)
