
import math

asteroids = set()
with open('input.txt') as f:
	for y, line in enumerate(f):
		for x, c in enumerate(line.strip()):
			if c == '#':
				asteroids.add((x, y))


def theta(p0, p1):
	x, y = (a - b for a, b in zip(p1, p0))
	return math.atan2(y, x)


counts = {}
for p0 in asteroids:
	counts[p0] = len(set(theta(p0, p1) for p1 in asteroids - {p0}))

print('Day 10, part 1:', max(counts.values()))

