
from math import gcd
from collections import defaultdict


pos = defaultdict(list)
vel = defaultdict(list)
with open('input.txt') as f:
	for line in f:
		line = line.strip('<>\n')
		for part in line.split(', '):
			k, v = part.split('=')
			pos[k].append(int(v))
			vel[k].append(0)


def energy(pos, vel):
	total = 0
	for p, k in zip(zip(*pos.values()), zip(*vel.values())):
		total += sum(map(abs, p)) * sum(map(abs, k))
	return total


def gravity(pos, vel):
	for i, p0 in enumerate(pos):
		for j, p1 in enumerate(pos[i+1:]):
			if p0 < p1:
				vel[i] += 1
				vel[i+1+j] -= 1
			elif p0 > p1:
				vel[i] -= 1
				vel[i+1+j] += 1


def step(pos, vel):
	gravity(pos, vel)
	for i, v in enumerate(vel):
		pos[i] += v
	return (*pos, *vel)


start = {k: (*pos[k], *vel[k]) for k in pos}
for i in range(1000):
	for x in pos:
		key = step(pos[x], vel[x])
		assert key != start[x]


total = energy(pos, vel)
print('Day 12, part 1:', total)
assert total == 10944


def find_repeat(pos, vel, start, t0=1000):
	repeat = 1
	for x in pos:
		i = t0 + 1
		key = start[x]
		while step(pos[x], vel[x]) != key:
			i += 1
		repeat *= i // gcd(repeat, i)
	return repeat


repeat = find_repeat(pos, vel, start)
print('Day 12, part 2:', repeat)
assert repeat == 484244804958744

