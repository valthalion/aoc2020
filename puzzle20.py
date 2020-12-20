from collections import defaultdict, deque
from functools import reduce
from operator import mul


monster_spec = ("                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   ")
monster = {
    'width': len(monster_spec[0]),
    'height': len(monster_spec),
    'positions': {(r, c)
                  for r, row in enumerate(monster_spec)
                  for c, char in enumerate(row)
                  if char == '#'}
}


def rotate(img):
    n = len(img[0])
    return tuple(''.join(row[col] for row in img) for col in range(n-1, -1, -1))


def flip_vertical(img):
    return tuple(reversed(img))


def flip_horizontal(img):
    return tuple(row[::-1] for row in img)


class Tile:
    def __init__(self, tile_id, tile):
        self.id = tile_id
        self.tile = tuple(row[1:-1] for row in tile[1:-1])
        self.boundaries = self.extract_boundaries(tile)
        self.potential_boundaries = self.expand_boundaries()
        self.links = None
        self.connectivity = None

    def extract_boundaries(self, tile):
        n = len(tile)
        boundaries = []
        boundaries.append(tile[0])
        boundaries.append(''.join(tile[r][-1] for r in range(n)))
        boundaries.append(tile[-1])
        boundaries.append(''.join(tile[r][0] for r in range(n)))
        return boundaries

    def expand_boundaries(self):
        boundaries = set(self.boundaries)
        boundaries |= {boundary[::-1] for boundary in boundaries}
        return boundaries

    def is_compatible_with(self, other):
        return any(boundary in other.potential_boundaries for boundary in self.potential_boundaries)

    def set_compatibility(self, compatibilities, tiles):
        self.links = []
        neighbours = {tiles[neighbour] for neighbour in compatibilities[self.id]}
        for boundary in self.boundaries:
            for neighbour in neighbours:
                if boundary in neighbour.potential_boundaries:
                    self.links.append(neighbour)
                    break
            else:
                self.links.append(None)
        self.connectivity = len(neighbours)
        if self.connectivity != sum(1 for n in self.links if n is not None):
            raise RuntimeError('Houston, we have a problem!')

    def rotate(self):  # ccw
        self.tile = rotate(self.tile)
        self.boundaries = [
            self.boundaries[1],
            self.boundaries[2][::-1],
            self.boundaries[3],
            self.boundaries[0][::-1]
        ]
        self.links = [*self.links[1:], self.links[0]]

    def flip_vertical(self):
        self.tile = flip_vertical(self.tile)
        self.boundaries = [
            self.boundaries[2],
            self.boundaries[1][::-1],
            self.boundaries[0],
            self.boundaries[3][::-1]
        ]
        self.links[0], self.links[2] = self.links[2], self.links[0]

    def flip_horizontal(self):
        self.tile = flip_horizontal(self.tile)
        self.boundaries = [
            self.boundaries[0][::-1],
            self.boundaries[3],
            self.boundaries[2][::-1],
            self.boundaries[1],
        ]
        self.links[1], self.links[3] = self.links[3], self.links[1]


def read_input():
    tiles = []
    with open('puzzle20.in', 'r') as f:
        while True:
            line = next(f).strip()
            tile_number = int(line[5:-1])
            tile = Tile(tile_number, tuple(next(f).strip() for _ in range(10)))
            tiles.append(tile)
            try:
                next(f)
            except StopIteration:
                break
    return tiles


def assess_compatibilities(tiles):
    compatibilities = defaultdict(set)
    for idx, tile in enumerate(tiles[:-1]):
        for other_tile in tiles [idx + 1:]:
            if tile.is_compatible_with(other_tile):
                compatibilities[tile.id].add(other_tile.id)
                compatibilities[other_tile.id].add(tile.id)
    return compatibilities


def match(tile, left, top):
    rotations = 0
    while tile.links[0] is not top:
        tile.rotate()
        rotations += 1
        if rotations >= 4:
            raise RuntimeError('Cannot align tile')
    if tile.links[3] is not left:
        tile.flip_horizontal()
    if tile.links[3] is not left:
        raise RuntimeError('No corners found.')


def stitch(img):
    return tuple(''.join(tile.tile[subrow] for tile in row)
                 for row in img
                 for subrow in range(len(row[0].tile))
                )


def build_image(tiles):
    img = []
    for tile in tiles.values():
        if tile.connectivity == 2:
            break
    else:
        raise RuntimeError('No corners found.')

    row = []

    match(tile, None, None)
    row.append(tile)
    prev_tile, tile = tile, tile.links[1]

    while tile.connectivity == 3:
        match(tile, prev_tile, None)
        row.append(tile)
        prev_tile, tile = tile, tile.links[1]

    match(tile, prev_tile, None)
    row.append(tile)
    img.append(row)

    prev_row, row = row, []
    col = 0
    tile = prev_row[col].links[2]

    while tile:
        match(tile, None, prev_row[col])
        row.append(tile)
        prev_tile, tile = tile, tile.links[1]
        col += 1

        while True:
            match(tile, prev_tile, prev_row[col])
            row.append(tile)
            prev_tile, tile = tile, tile.links[1]
            col += 1
            if tile is None:
                break

        img.append(row)
        prev_row, row = row, []
        col = 0
        tile = prev_row[col].links[2]

    return stitch(img)


def mark_monsters(image):
    marked = set()
    for row in range(len(image) - monster['height'] + 1):
        for col in range(len(image[0]) - monster['width'] + 1):
            monster_positions = set((row + r, col + c) for r, c in monster['positions'])
            if all(image[row][col] == '#' for row, col in monster_positions):
                marked |= monster_positions
    return marked

def part_1():
    tiles = read_input()
    compatibilities = assess_compatibilities(tiles)
    corners = [tile for tile, compatible_tiles in compatibilities.items() if len(compatible_tiles) == 2]
    return reduce(mul, corners)


def part_2():
    tiles = read_input()
    compatibilities = assess_compatibilities(tiles)
    tiles = {tile.id: tile for tile in tiles}
    for tile in tiles.values():
        tile.set_compatibility(compatibilities, tiles)
    image = build_image(tiles)
    rotations = 0
    while True:
        if (marked := (mark_monsters(image) or
                       mark_monsters(flip_horizontal(image)) or
                       mark_monsters(flip_vertical(image)))):
            hashes = set((r, c)
                         for r in range(len(image))
                         for c in range(len(image[0]))
                         if image[r][c] == '#')
            return len(hashes) - len(marked)
        rotations += 1
        if rotations >= 4:
            raise RuntimeError('No monsters found')
        image = rotate(image)
