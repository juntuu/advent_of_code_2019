
import sys
from itertools import count
from intcode import Intcode, IO

deployed = set()
hit = set()


def compute(prog):
	buf = []
	io = IO(buf.pop, buf.append)
	cpu = Intcode(io, io)
	cache = {}

	def pos(x, y):
		if (x, y) not in cache:
			deployed.add((x, y))
			buf.extend([y, x])
			cpu(prog)
			if buf[0]:
				hit.add((x, y))
			cache[x, y] = buf.pop()
		return cache[x, y]
	return pos


def pull(pos, verbose=False):
	limit = 50
	total = 0
	min_x = 0
	skip = 1
	for y in range(limit):
		xs = 0
		x = min_x
		while x < limit:
			p = pos(x, y)
			if p and not xs:
				a = x, y
				min_x = x
				if x + skip < limit:
					xs += skip
				else:
					xs += limit - x
				x += skip
			else:
				xs += p
				x += 1
			if xs and not p:
				b = x, y
				break
		total += xs
		if verbose:
			print('.'*max(min_x-1, 0) + '#'*xs)
		skip = max(xs - 1, 1)
		if skip > 1 and not xs:
			break
	return total, a[0] / a[1], b[0] / b[1]


def start(y, pos, min_x=0, cache={}):
	if y not in cache:
		for x in count(min_x):
			if pos(x, y):
				cache[y] = x
				return x
	return cache[y]


def search(pos, a, b):
	N = 100
	y0 = ((N-1)*(a+1))/(b-a)
	x0 = (y0+N-1)*a
	x, y = int(x0), int(y0)
	step = N-1
	while True:
		x = start(y+N-1, pos, x)
		if pos(x+N-1, y):
			if step == 1:
				return x * 10000 + y
			y -= step
			x = int(a * y)
			step //= 2
		else:
			y += step


name = 'input.txt'
if '-f' in sys.argv:
	name = sys.argv[sys.argv.index('-f') + 1]
with open(name) as f:
	prog = [int(x) for x in f.read().strip().split(',')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv
res, a, b = pull(compute(prog), verbose)

print('Day 19, part 1:', res)
assert res == 223 or name != 'input.txt'

h1 = set(hit)
d1 = set(deployed)

res = search(compute(prog), a, b)

print('Day 19, part 2:', res)
assert res == 9480761 or name != 'input.txt'

print()
print(f'Part 1: hit: {len(h1)}, deployed: {len(d1)}')
print(f'Part 2: hit: {len(hit - h1)}, deployed: {len(deployed - d1)}')

print(f'Total: hit: {len(hit)}, deployed: {len(deployed)}')

