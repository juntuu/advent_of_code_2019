
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


class Grid:
	def __init__(self, g=None, inner=None, outer=None, level=0):
		self.g = g or [[0] * 5 for _ in range(5)]
		self.inner = inner
		self.g[2][2] = self.inner
		self.outer = outer
		self.level = level

	def around(self, i, j):
		total = 0
		for x, y in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
			if x == 2 and y == 2:
				if not self.inner:
					continue
				if i == 1:
					total += sum(self.inner.g[0])
				elif i == 3:
					total += sum(self.inner.g[4])
				elif j == 1:
					total += sum(r[0] for r in self.inner.g)
				elif j == 3:
					total += sum(r[4] for r in self.inner.g)
			elif 0 <= x < 5 and 0 <= y < 5:
				total += self.g[x][y]
			else:
				if not self.outer:
					continue
				if x == -1:
					total += self.outer.g[1][2]
				elif x == 5:
					total += self.outer.g[3][2]
				if y == -1:
					total += self.outer.g[2][1]
				elif y == 5:
					total += self.outer.g[2][3]
		return total

	def step(self):
		new = set()
		for i, j in ((i, j) for i in range(5) for j in range(5) if i != 2 or j != 2):
			if i == 2 and j == 2:
				continue
			x = self.around(i, j)
			if self.g[i][j] == 1 and x == 1:
				new.add((i, j))
			elif self.g[i][j] == 0 and x in [1, 2]:
				new.add((i, j))
		if self.inner and self.level > -1:
			self.inner.step()
		if self.outer and self.level < 1:
			self.outer.step()
		for i, j in ((i, j) for i in range(5) for j in range(5) if i != 2 or j != 2):
			self.g[i][j] = int((i, j) in new)

	@property
	def count(self):
		total = 0
		total += sum(1 for r in self.g for i in r if i == 1)
		if self.level < 1 and self.outer is not None:
			total += self.outer.count
		if self.level > -1 and self.inner is not None:
			total += self.inner.count
		return total


def part2(grid):
	g = Grid([[int(c == '#') for c in line] for line in grid])
	inner = g
	outer = g
	for i in range(200):
		if i % 2 == 0:
			inner.inner = Grid(outer=inner, level=i+1)
			inner = inner.inner
			outer.outer = Grid(inner=outer, level=-i-1)
			outer = outer.outer
		g.step()
	return g.count


with open('input.txt') as f:
	grid = [line.strip() for line in f]

print('Day 24, part 1:', part1(grid))
print('Day 24, part 2:', part2(grid))

