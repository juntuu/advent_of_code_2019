
with open('input.txt') as f:
	orbits = {}
	for line in f:
		origin, name = line.strip().split(')')
		if name in orbits:
			raise Exception(f'{name} orbits two origins')
		orbits[name] = origin


def count_orbits(*names, counts=None):
	if counts is None:
		counts = {}
	for name in names:
		if name not in orbits:
			yield name, 0
			continue
		origin = orbits[name]
		if origin not in counts:
			_, counts[origin] = next(count_orbits(origin, counts))
		yield name, counts[origin] + 1


total_orbits = sum(x for _, x in count_orbits(*orbits))
print('Day 5, part 1:', total_orbits)

