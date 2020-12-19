from itertools import product
import re


def read_input():
    ruleset = {}
    with open('puzzle19.in', 'r') as f:
        while (line := next(f).strip()):
            rule_no, rule_spec = line.split(': ')
            ruleset[int(rule_no)] = Rule.from_spec(rule_spec, ruleset)
        messages = [line.strip() for line in f]
    return ruleset, messages


class Rule:
    def __init__(self, spec, ruleset):
        self._patterns = None
        self._spec = spec
        self._ruleset = ruleset

    @classmethod
    def from_spec(cls, spec, ruleset):
        if spec.startswith('"'):
            return LeafRule(spec[1:-1], ruleset)
        groups = spec.split('|')
        if len(groups) == 1:
            rule_nos = [int(n) for n in groups[0].strip().split()]
            return SequenceRule(rule_nos, ruleset)
        rule_nos = [[int(n) for n in group.strip().split()] for group in groups]
        return AlternativeRule(rule_nos, ruleset)

    @property
    def patterns(self):
        if self._patterns is None:
            self._patterns = self._eval_patterns()
        return self._patterns

    def _eval_patterns(self):
        raise NotImplementedError

    def match(self, txt):
        return txt in self.patterns


class LeafRule(Rule):
    def _eval_patterns(self):
        return {self._spec}


class SequenceRule(Rule):
    def _eval_patterns(self):
        combinations = product(*(self._ruleset[rule].patterns for rule in self._spec))
        return set(''.join(patterns) for patterns in combinations)


class AlternativeRule(Rule):
    def _eval_patterns(self):
        patterns = set()
        for group in self._spec:
            combinations = product(*(self._ruleset[rule].patterns for rule in group))
            patterns |= set(''.join(pattern_pair) for pattern_pair in combinations)
        return patterns


def match(ruleset, msg):
    rule42, rule31 = ruleset[42].patterns, ruleset[31].patterns
    sample = rule42.pop()
    chunksize = len(sample)
    rule42.add(sample)
    n = len(msg)
    if n % chunksize != 0:
        return False
    chunks = tuple(msg[idx : idx+chunksize] for idx in range(0, n, chunksize))
    n_chunks = len(chunks)

    start42s = 0
    for chunk in chunks:
        if chunk in rule42:
            start42s += 1
        else:
            break

    if not 1 <= start42s < n_chunks:
        return False
    if start42s < n_chunks - start42s + 1:
        return False

    for chunk in chunks[start42s:]:
        if chunk not in rule31:
            return False
    return True


def part_1():
    ruleset, messages = read_input()
    rule = ruleset[0]
    return sum(1 for msg in messages if rule.match(msg))


def part_2():
    ruleset, messages = read_input()
    return sum(1 for msg in messages if match(ruleset, msg))
