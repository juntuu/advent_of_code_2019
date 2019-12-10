
import math

asteroids = set()
with open('input.txt') as f:
	for y, line in enumerate(f):
		for x, c in enumerate(line.strip()):
			if c == '#':
				asteroids.add((x, y))


def euclidean(p0, p1):
	return sum((i0 - i1) ** 2 for i0, i1 in zip(p0, p1))


def theta(p0, p1):
	x, y = (a - b for a, b in zip(p1, p0))
	x, y = -y, x  # clockwise starting at 0 from 12.00
	res = math.atan2(y, x)
	if res < 0:
		res += 2 * math.pi  # range from 0 to 2π
	return res


counts = {}
for p0 in asteroids:
	counts[p0] = len(set(theta(p0, p1) for p1 in asteroids - {p0}))

station, n = max(counts.items(), key=lambda x: x[1])
print('Day 10, part 1:', n)

asteroids.remove(station)
vaporized = 0
while vaporized < 200 and asteroids:
	last = None
	for a, _, target in sorted(
			(theta(station, p), euclidean(station, p), p)
			for p in asteroids):
		if a == last:
			continue
		vaporized += 1
		last = a
		asteroids.remove(target)
		if vaporized == 200:
			break

tx, ty = target
print('Day 10, part 2:', tx * 100 + ty)

