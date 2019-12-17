
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
		if all(c == '#' for c in around(y, x, lines)):
			total += y * x

print('Day 17, part 1:', total)

