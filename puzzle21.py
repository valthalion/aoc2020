from functools import reduce


def read_input():
    foods = []
    with open('puzzle21.in', 'r') as f:
        for line in f:
            ingredients, allergens = line.strip().split('(')
            ingredients = set(ingredients.strip().split())
            allergens = set(allergens.strip()[9:-1].split(', '))
            foods.append((ingredients, allergens))
    return foods


def identify_allergens(foods):
    candidates = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in candidates:
                candidates[allergen] = candidates[allergen] & ingredients
            else:
                candidates[allergen] = ingredients
    return candidates


def part_1():
    foods = read_input()
    candidates = identify_allergens(foods)
    all_candidates = reduce(set.union, candidates.values())
    return sum(1 for ingredients, _ in foods for ingredient in ingredients if ingredient not in all_candidates)


def part_2():
    foods = read_input()
    candidates = identify_allergens(foods)
    identified = {}
    while candidates:
        for allergen, allergen_candidates in candidates.items():
            if len(allergen_candidates) == 1:
                identified[allergen] = allergen_candidates.pop()
            else:
                allergen_candidates -= set(identified.values())
        for allergen in identified:
            if allergen in candidates:
                del(candidates[allergen])
    return(','.join(identified[allergen] for allergen in sorted(identified)))
