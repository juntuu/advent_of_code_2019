
import sys
from intcode import Intcode, IO


def compute(prog):
	buf = []
	io = IO(buf.pop, buf.append)
	cpu = Intcode(io, io)

	def pos(x, y):
		buf.extend([y, x])
		cpu(prog)
		return buf.pop()
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
				min_x = x
			xs += p
			if xs and not p:
				break
		total += xs
		if verbose:
			print('.'*max(min_x-1, 0) + '#'*xs)
	return total


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv
res = pull(compute(prog), verbose)
print('Day 19, part 1:', res)

