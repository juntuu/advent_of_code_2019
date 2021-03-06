

def trace_wire(wire):
	x = 0
	y = 0
	path = [(x, y)]
	for (dx, dy), n in wire:
		for _ in range(n):
			x += dx
			y += dy
			path.append((x, y))
	return path


directions = {
		'R': (1, 0),
		'L': (-1, 0),
		'U': (0, 1),
		'D': (0, -1),
		}

with open('input.txt') as f:
	wire_a, wire_b = (
			trace_wire(
				(directions[part[:1]], int(part[1:]))
				for part in line.split(','))
			for line in f)

crossing = set(wire_a[1:]) & set(wire_b[1:])
distance = min(sum(map(abs, pos)) for pos in crossing)

print('Day 3, part 1:', distance)

wire_length = min(
		wire_a.index(x) + wire_b.index(x)
		for x in crossing)

print('Day 3, part 2:', wire_length)

