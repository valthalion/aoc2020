import re


def read_input():
    ruleset = {}
    with open('puzzle19.in.test2', 'r') as f:
        while (line := next(f).strip()):
            rule_no, rule_spec = line.split(': ')
            ruleset[int(rule_no)] = Rule.from_spec(rule_spec, ruleset)
        messages = [line.strip() for line in f]
    return ruleset, messages


class Rule:
    def __init__(self, spec, ruleset):
        self._regex = None
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

    def regex(self, bounds=True):
        if self._regex is None:
            self._regex = self._eval_regex()
        if bounds:
            return f'^{self._regex}$'
        return self._regex

    def _eval_regex(self):
        raise NotImplementedError


class LeafRule(Rule):
    def _eval_regex(self):
        return self._spec


class SequenceRule(Rule):
    def _eval_regex(self):
        return ''.join(self._ruleset[rule].regex(bounds=False) for rule in self._spec)


class AlternativeRule(Rule):
    def _eval_regex(self):
        regexstr = '|'.join(
            ''.join(self._ruleset[rule].regex(bounds=False) for rule in group)
            for group in self._spec)
        return f'({regexstr})'


def part_1():
    ruleset, messages = read_input()
    regex = re.compile(ruleset[0].regex())
    return sum(1 for msg in messages if regex.match(msg))


def part_2():
    pass
