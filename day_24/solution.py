
def step(grid, n=5):
	new = []
	for i, r in enumerate(grid):
		new.append('')
		for j, c in enumerate(r):
			around = 0
			for x, y in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
				if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
					around += grid[x][y] == '#'
			if c == '#' and around == 1:
				new[-1] += '#'
			elif c == '.' and around in [1, 2]:
				new[-1] += '#'
			else:
				new[-1] += '.'
	return new


def bio_div(grid):
	total = 0
	i = 0
	for r in grid:
		for c in r:
			if c == '#':
				total += 2 ** i
			i += 1
	return total


def part1(grid):
	seen = {bio_div(grid)}
	while True:
		grid = step(grid)
		bd = bio_div(grid)
		if bd in seen:
			return bd
		seen.add(bd)


with open('input.txt') as f:
	grid = [line.strip() for line in f]

print('Day 24, part 1:', part1(grid))

