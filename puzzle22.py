from collections import deque


def read_input():
    with open('puzzle22.in', 'r') as f:
        line = next(f)
        deck1, deck2 = deque(), deque()
        while (card := next(f).strip()):
            deck1.appendleft(int(card))
        line = next(f)
        for card in f:
            deck2.appendleft(int(card.strip()))
    return deck1, deck2


def play_game(deck1, deck2):
    while deck1 and deck2:
        card1, card2 = deck1.pop(), deck2.pop()
        if card1 > card2:
            deck1.appendleft(card1)
            deck1.appendleft(card2)
        else:  # card1 < card2
            deck2.appendleft(card2)
            deck2.appendleft(card1)
    return deck1 or deck2


def play_recursive_game(deck1, deck2):
    known_states = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in known_states:
            return deck1
        known_states.add(state)
        card1, card2 = deck1.pop(), deck2.pop()
        if len(deck1) >= card1 and len(deck2) >= card2:
            deck1_copy = deque(deck1[n] for n in range(-card1, 0))
            deck2_copy = deque(deck2[n] for n in range(-card2, 0))
            winner = play_recursive_game(deck1_copy, deck2_copy)
            if winner is deck1_copy:
                deck1.appendleft(card1)
                deck1.appendleft(card2)
            else:  # winner is deck2_copy
                deck2.appendleft(card2)
                deck2.appendleft(card1)
        else:
            if card1 > card2:
                deck1.appendleft(card1)
                deck1.appendleft(card2)
            else:  # card1 < card2
                deck2.appendleft(card2)
                deck2.appendleft(card1)
    return deck1 or deck2


def part_1():
    deck1, deck2 = read_input()
    winner = play_game(deck1, deck2)
    return sum(value * card for value, card in enumerate(winner, start=1))


def part_2():
    deck1, deck2 = read_input()
    winner = play_recursive_game(deck1, deck2)
    return sum(value * card for value, card in enumerate(winner, start=1))
