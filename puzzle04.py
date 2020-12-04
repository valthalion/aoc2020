dec_set = set('0123456789')
hex_set = set('0123456789abcdef')
eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def read_input():
    records = []
    current_record = {}
    with open('puzzle04.in', 'r') as f:
        for line in f:
            data = line.strip()
            if current_record and not data:
                records.append(current_record)
                current_record = {}
            pairs = data.split()
            for pair in pairs:
                field, value = pair.split(':')
                if field in ('byr', 'iyr', 'eyr', 'cid'):
                    value = int(value)
                current_record[field] = value
    if current_record:
        records.append(current_record)
    return records


def valid(records):
    fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
    for record in records:
        if all(field in record for field in fields):
            yield record

def valid_height(height):
    if len(height) < 4:
        return False
    unit = height[-2:]
    if unit not in ('cm', 'in'):
        return False
    value = int(height[:-2])
    return (unit == 'cm' and 150 <= value <= 193) or (unit == 'in' and 59 <= value <= 76)


def valid_hair_color(hair_color):
    return len(hair_color) == 7 and hair_color[0] == '#' and set(hair_color[1:]) <= hex_set

def valid_pid(pid):
    return len(pid) == 9 and set(pid) <= dec_set


def valid_full(records):
    for record in records:
        if all((
                'byr' in record and 1920 <= record['byr'] <= 2002,
                'iyr' in record and 2010 <= record['iyr'] <= 2020,
                'eyr' in record and 2020 <= record['eyr'] <= 2030,
                'hgt' in record and valid_height(record['hgt']),
                'hcl' in record and valid_hair_color(record['hcl']),
                'ecl' in record and record['ecl'] in eye_colors,
                'pid' in record and valid_pid(record['pid']))):
            yield record


def part_1():
    records = read_input()
    valid_records = sum(1 for _ in valid(records))
    return valid_records


def part_2():
    records = read_input()
    valid_records = sum(1 for _ in valid_full(records))
    return valid_records
