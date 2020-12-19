from operator import add, mul


ops = {
    '+': add,
    '*': mul
}


def read_input():
    with open('puzzle18.in', 'r') as f:
        for line in f:
            yield line.strip()


class Node:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        op = '+' if self.op is add else '*'
        left = str(self.left) if self.left is not None else "."
        right = str(self.right) if self.right is not None else "."
        return f'({left} {op} {right})'

    __str__ = __repr__

    @property
    def value(self):
        return self.op(self.left.value, self.right.value)


class Leaf:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)

    __str__ = __repr__

    @property
    def value(self):
        return self._value


def tokenize(line):
    tokens = []
    number = []
    for c in line:
        if c in '0123456789':
            number.append(c)
        elif c in ops:
            if number:
                tokens.append(Leaf(int(''.join(number))))
                number = []
            tokens.append(Node(ops[c]))
        elif c == ')':
            if number:
                tokens.append(Leaf(int(''.join(number))))
                number = []
            tokens.append(c)
        elif c == '(':
            tokens.append(c)
        elif c == ' ':
            if number:
                tokens.append(Leaf(int(''.join(number))))
                number = []
        else:
            raise ValueError('Invalid token', c)
    if number:
        tokens.append(Leaf(int(''.join(number))))
    return reversed(tokens)


def parse(tokens):
    token = next(tokens)
    if isinstance(token, Leaf):
        root = token
    elif token == ')':
        root = parse(tokens)
    else:
        raise RuntimeError('Unexpected token', token)

    try:
        token = next(tokens)
    except StopIteration:
        return root

    if isinstance(token, Node):
        token.right = root
        root = token
        root.left = parse(tokens)
        return root
    if token == '(':
        return root
    raise RuntimeError('Unexpected token', token)


def evaluate(line):
    tokens = tokenize(line)
    expr = parse(tokens)
    return expr.value


def apply_parens(tokens):
    grouped_tokens = []
    for token in tokens:
        if isinstance(token, (Node, Leaf)):
            grouped_tokens.append(token)
        elif token == ')':
            grouped_tokens.append(apply_parens(tokens))
        elif token == '(':
            break
    return grouped_tokens


def apply_op(tokens, op):
    def isop(t):
        return isinstance(t, Node) and t.op is op and t.right is None

    result = []
    for token in tokens:
        if not result:
            result.append(token)
            continue
        if isop(token):
            if isop(node := result[-1]):
                node.right = token
            else:
                token.left = result.pop()
                result.append(token)
        else:
            if isop(node := result[-1]):
                node.right = token
            else:
                result.append(token)
    return result


def parse2(tokens):
    preparsed = [parse2(token) if isinstance(token, list) else token for token in tokens]
    with_sums = apply_op(preparsed, add)
    with_muls = apply_op(with_sums, mul)
    expr = with_muls.pop()
    return expr


def evaluate2(line):
    tokens = tokenize(line)
    parenthesised = apply_parens(tokens)
    expr = parse2(parenthesised)
    return expr.value


def part_1():
    return sum(evaluate(line) for line in read_input())


def part_2():
    return sum(evaluate2(line) for line in read_input())


def main():
    tests = (
        ('1 + 2 * 3 + 4 * 5 + 6', 71, 231),
        ('1 + (2 * 3) + (4 * (5 + 6))', 51, 51),
        ('2 * 3 + (4 * 5)', 26, 46),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
        ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240, 669060),
        ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340),
    )
    print('Part 1')
    for line, expected, _ in tests:
        result = evaluate(line)
        print(line, '->', result, expected, 'ok' if result == expected else 'error')
    print()
    print('Part 2')
    for line, _, expected in tests:
        result = evaluate2(line)
        print(line, '->', result, expected, 'ok' if result == expected else 'error')


if __name__ == '__main__':
    main()
