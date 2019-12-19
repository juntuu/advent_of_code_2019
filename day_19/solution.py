
import sys
from itertools import count
from intcode import Intcode, IO


def compute(prog):
	buf = []
	io = IO(buf.pop, buf.append)
	cpu = Intcode(io, io)
	cache = {}

	def pos(x, y):
		if (x, y) not in cache:
			buf.extend([y, x])
			cpu(prog)
			cache[x, y] = buf.pop()
		return cache[x, y]
	return pos


def pull(pos, verbose=False):
	limit = 50
	total = 0
	min_x = 0
	for y in range(limit):
		xs = 0
		for x in range(min_x, limit):
			p = pos(x, y)
			if p and not xs:
				a = x, y
				min_x = x
			xs += p
			if xs and not p:
				b = x, y
				break
		total += xs
		if verbose:
			print('.'*max(min_x-1, 0) + '#'*xs)
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


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv
res, a, b = pull(compute(prog), verbose)

print('Day 19, part 1:', res)
assert res == 223

res = search(compute(prog), a, b)

print('Day 19, part 2:', res)

