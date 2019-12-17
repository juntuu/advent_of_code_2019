
from intcode import Intcode, IO


def around(y, x, g):
	yield g[y][x]
	for j, i in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
		if 0 <= j < len(g) and 0 <= x < len(g[j]):
			yield g[j][i]
		else:
			yield '.'


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

view = []
io = IO(None, view.append)
Intcode(io, io)(prog)

lines = ''.join(map(chr, view)).splitlines()
total = 0
for y, l in enumerate(lines):
	for x, c in enumerate(l):
		if c in '<v>^':
			vac = (x, y, c)
		if all(c == '#' for c in around(y, x, lines)):
			total += y * x

print('Day 17, part 1:', total)


def step(x, y, c, grid):
	x += {'<': -1, '>': 1}.get(c, 0)
	y += {'^': -1, 'v': 1}.get(c, 0)
	try:
		if grid[y][x] == '#':
			return x, y
	except IndexError:
		pass


def path(start, c, grid):
	route = []
	turn = '<v>^<^'
	while True:
		i = 0
		pos = step(*start, c, grid)
		while pos:
			start = pos
			i += 1
			pos = step(*start, c, grid)
		if i:
			route.append(f'{i}')
		for x, t in [(1, 'L'), (-1, 'R')]:
			d = turn[turn.index(c) + x]
			pos = step(*start, d, grid)
			if pos:
				route.append(t)
				c = d
				break
		else:
			break
	return ','.join(route)


def sub_routines(prog, n, limit):
	if n == 1:
		if len(prog) < limit:
			return {prog}
	A, _, _ = prog[:limit+1].rpartition(',')
	while A:
		rest = set(filter(None, (x.strip(',') for x in prog.split(A))))
		fns = {A}
		for x in rest:
			new = sub_routines(x, n-1, limit)
			if new is None:
				break
			fns |= new
		else:
			if len(fns) <= n:
				return fns
		A, _, _ = A.rpartition(',')


def program(prog, verbose='n'):
	limit = 20
	A, B, C = sub_routines(prog, 3, limit)
	main = prog.replace(A, 'A').replace(B, 'B').replace(C, 'C')
	assert len(main) <= limit
	return '\n'.join([main, A, B, C, verbose, ''])


vac_prog = program(path(vac[:2], vac[-1], lines))
visit = map(ord, vac_prog)

io = IO(visit.__next__, lambda x: x < 256 or print('Day 17, part 2:', x))
prog[0] = 2
Intcode(io, io)(prog)

