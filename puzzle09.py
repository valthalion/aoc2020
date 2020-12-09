from itertools import islice

from puzzle01 import find_pair


preamble = 25
window = preamble


def read_input():
    with open('puzzle09.in', 'r') as f:
        sequence = [int(line.strip()) for line in f]
    return sequence


def find_invalid(sequence):
    for idx, value in enumerate(sequence[preamble:], start=preamble):
        if find_pair(value, set(islice(sequence, idx - window, idx))) is None:
            return idx, value
    return None


def find_chunk(target, sequence):
    start, end, chunk_sum = 0, 0, 0
    # do not allow empty or single-number chunks
    while end <= len(sequence):
        if chunk_sum == target and end - start > 1:
            return start, end
        if chunk_sum <= target:  # Include = to escape chunk that contains only target number
            chunk_sum += sequence[end]
            end += 1
        else:
            chunk_sum -= sequence[start]
            start += 1
    return None


def part_1():
    sequence = read_input()
    pos, first_invalid = find_invalid(sequence)
    return first_invalid


def part_2():
    sequence = read_input()
    pos, first_invalid = find_invalid(sequence)
    start, end = find_chunk(first_invalid, sequence)
    chunk = sequence[start:end]
    return min(chunk) + max(chunk)
