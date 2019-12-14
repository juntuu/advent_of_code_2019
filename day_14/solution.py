
from collections import namedtuple

Chem = namedtuple('Chem', ['name', 'k', 'requires'])

chemicals = {'ORE': Chem('ORE', 1, {})}
with open('input.txt') as f:
	for line in f:
		*inp, _, n0, c0 = line.strip().replace(',', '').split()
		chem = Chem(c0, int(n0), {})
		for ni, ci in zip(inp[::2], inp[1::2]):
			chem.requires[ci] = int(ni)
		chemicals[c0] = chem


def ore_for(name, inv, amount=1):
	inv[name] -= amount
	if name == 'ORE':
		return
	req = -inv[name]
	c = chemicals[name]
	req = req // c.k + (req % c.k != 0)
	for ci, n in c.requires.items():
		ore_for(ci, inv, n * req)
	inv[name] += c.k * req
	return -inv['ORE']


inventory = {k: 0 for k in chemicals}
ore = ore_for('FUEL', inventory)
print('Day 14, part 1:', ore)

T = 10 ** 12
fuel = T // ore   # known lower bound from requirement for 1 fuel
step = fuel // 4
while step > 0:
	while True:
		fuel += step
		inventory = {k: 0 for k in chemicals}
		if ore_for('FUEL', inventory, fuel) > T:
			fuel -= step
			step //= 2
			break

print('Day 14, part 2:', fuel)

