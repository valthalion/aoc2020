from collections import defaultdict
import re


container_re = re.compile('''(?P<container>\w+ \w+) bags''')
content_re = re.compile(''' (?P<num>\d+) (?P<color>\w+ \w+) bags?''')


def read_input():
    rules = {}
    with open('puzzle07.in', 'r') as f:
        for line in f:
            container, contents = rule_from_line(line.strip())
            rules[container] = contents
    return rules


def rule_from_line(line):
    container_part, contents_part = line.split('contain')
    container = container_re.match(container_part).group('container')
    content_blocks = contents_part.split(',')
    if len(content_blocks) == 1 and content_blocks[0].startswith(' no'):
        contents = None
    else:
        contents = {}
        for block in content_blocks:
            content = content_re.match(block).groupdict()
            contents[content['color']] = int(content['num'])
    return container, contents


def count(color, rules, acc=None):
    if acc is None:
        acc = {}
    if color in acc:
        return acc[color]
    total = 1  #self
    if rules[color] is not None:
        for other_color, num in rules[color].items():
            total += num * count(other_color, rules, acc)
    acc[color] = total
    return total


def part_1():
    rules = read_input()
    containment_graph = defaultdict(set)
    for container, contents in rules.items():
        if contents is None:
            continue
        for color in contents:
            containment_graph[color].add(container)
    queue = {'shiny gold'}
    valid = set()
    while queue:
        color = queue.pop()
        new_colors = containment_graph[color] - valid
        queue |= new_colors
        valid |= new_colors
    return len(valid)


def part_2():
    rules = read_input()
    return count('shiny gold', rules) - 1  # remove tha shiny gold bag
